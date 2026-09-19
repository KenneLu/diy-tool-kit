# TEMPLATE-MODULE: sync_check | TEMPLATE-VER: 1.3.0
# T10 · 模板漂移检查（防漂移四件套之二，执行文档 D1）。
#
# 原理：**双通道扫描**——
#   ① 头部通道：工具文件带 `# TEMPLATE-FROM: <模板库目录>/<相对路径>` 头时，按该路径比对；
#   ② 布局通道（1.3.0 新增）：工具 `src/modules/<模块>/` 下**同名文件**只要模板存在，
#      就纳入比对，**不要求工具侧有头**（CONFORMANCE §4.1.9 盲区 1/3）。
# 两通道都做**归一化哈希**：双方剔除 `# TEMPLATE-*` 元信息行后哈希相等即为一致
# （副本头标明出处、正本头标明模块身份，这些行差异不计入）。
#
# 判定（黄灯一律不阻断退出码）：
#   [ok]    归一化后一致，且 TEMPLATE-VER 相同
#   [decl ] 内容有差异，但文件头申报了 TEMPLATE-LOCAL-OVERRIDE: <原因>
#   [DRIFT] 有头、内容或 VER 不一致且未申报 —— **红灯，退出码 1**
#   [param] appconfig.py —— 参数文件，按设计豁免比对
#   [lag]   蓝本工具（blueprints.txt 名单）的副本落后于模板 VER —— 黄灯。
#           1.3.0 起蓝本不再整体 skip（旧行为是盲区：模板前进而蓝本原地不动无人
#           发现，CONFORMANCE §4.1.6 教训），打印 副本VER -> 模板VER；跟不跟由人
#           决定（写 REVIEW）。蓝本件若 VER 相同而内容仍有差异 = 真实分叉，仍红灯。
#   [NOHDR] 工具侧无 TEMPLATE 头，但落在 `src/modules/<模块>/` 且与模板不一致
#           —— 黄灯，提示补头（§4.1.9 盲区 1）。补头后由头部通道接管。
#   [MISSING-MODULE] 模板 `modules/<模块>/` 有代码，而工具既无 `src/modules/<模块>/`
#           目录、也无任何文件申报来自该模块 —— 黄灯（§4.1.9 盲区 2）。
#           是否采纳取决于触发条件，故不阻断。
#   [MISSING-FILE] 模块已被采纳（目录在，或有文件申报来自该模块），但模板里的某个件
#           工具侧没有（例：模板新增 `icons/__init__.py` 而四工具未拷；reme 只有散文件
#           `service_link.py` 而缺 `service_link/__init__.py`）—— 黄灯（复核员实测漏检）。
#
# 用法：
#   python my-diy-tool-template/sync_check.py                    # 检查 my_diy_tools 下所有工具
#   python my-diy-tool-template/sync_check.py --roots dsh-helper opencodex-helper

import argparse
import hashlib
import re
import sys
from pathlib import Path

try:  # Windows 控制台默认 GBK，中文判定标签会变乱码
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent      # my_diy_tools/
TEMPLATE_DIR = Path(__file__).resolve().parent     # 模板库根（目录名可改，逻辑不依赖）


def load_blueprints() -> set[str]:
    """蓝本名单从 blueprints.txt 读（每行一个目录名）——家族增长不改代码。"""
    cfg = Path(__file__).resolve().parent / "blueprints.txt"
    if not cfg.exists():
        return set()
    return {line.strip() for line in cfg.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")}


FROM_RE = re.compile(r"^#\s*TEMPLATE-FROM:\s*[A-Za-z0-9_.-]+/([\w./-]+)", re.M)
# 副本误用正本风格头（TEMPLATE-MODULE: <模块名>，无库名路径）时按模块名推导路径（1.2.0）
MODULE_RE = re.compile(r"^#\s*TEMPLATE-MODULE:\s*([\w-]+)\s*(?:\||$)", re.M)
VER_RE = re.compile(r"TEMPLATE-VER:\s*([\d.]+)")
OVERRIDE_RE = re.compile(r"^#\s*TEMPLATE-LOCAL-OVERRIDE:", re.M)
META_LINE = re.compile(r"^\s*#\s*TEMPLATE-")
# 旧头部路径 → 新 modules 布局的别名（副本未跟上布局时兜底）
LEGACY_ALIAS = {
    "update_helper.py": "modules/update_helper/update_helper.py",
    "appconfig.py": "modules/appconfig/appconfig.py",
    "paths.py": "modules/paths/paths.py",
    "autostart.py": "modules/autostart/autostart.py",
    "i18n.py": "modules/i18n/i18n.py",
    "icons.py": "modules/icons/icons.py",
    "tray_kit.py": "modules/tray_kit/tray_kit.py",
    "log_kit.py": "modules/log_kit/log_kit.py",
}


def sha256_text(text: str) -> str:
    norm = "\n".join(line for line in text.splitlines() if not META_LINE.match(line))
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


def ver_tuple(ver: str) -> tuple:
    """VER 按数值比较，避免字符串序埋雷（1.10.0 应大于 1.9.0）。"""
    return tuple(int(x) for x in re.findall(r"\d+", ver)) or (0,)


def ver_lt(a: str, b: str) -> bool:
    return ver_tuple(a) < ver_tuple(b)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def has_template_header(head: str) -> bool:
    return bool(FROM_RE.search(head) or MODULE_RE.search(head) or OVERRIDE_RE.search(head))


def scan_tool(tool_dir: Path):
    """头部通道：返回 [(tool_file, template_rel, declared, tool_ver)]。"""
    found = []
    for py in sorted(tool_dir.rglob("*.py")):
        parts = py.parts
        if ".git" in parts or "__pycache__" in parts or "build" in parts or "out" in parts:
            continue
        head = read_text(py)[:4096]
        match = FROM_RE.search(head)
        if match:
            rel = match.group(1)
        else:
            mmod = MODULE_RE.search(head)
            if not mmod:
                continue
            mod = mmod.group(1)
            # `TEMPLATE-MODULE: <模块>` 只标模块，不标文件名：__init__.py 必须映射到
            # 模板的同名 __init__.py（1.3.0 起模板 __init__.py 也带此头，否则会拿
            # __init__.py 去比 <模块>.py，产生假 DRIFT）。
            if py.name == "__init__.py":
                rel = f"modules/{mod}/__init__.py"
                if not (TEMPLATE_DIR / rel).exists():
                    continue
            else:
                rel = f"modules/{mod}/{mod}.py"
            if not (TEMPLATE_DIR / rel).exists():
                # 布局兜底：模块文件夹下唯一 py 时按唯一者解析；否则视为无有效出处，跳过
                mod_dir = TEMPLATE_DIR / "modules" / mod
                cands = sorted(mod_dir.rglob("*.py")) if mod_dir.is_dir() else []
                if len(cands) != 1:
                    continue
                rel = cands[0].relative_to(TEMPLATE_DIR).as_posix()
        ver = VER_RE.search(head)
        found.append((py, rel, bool(OVERRIDE_RE.search(head)),
                      ver.group(1) if ver else ""))
    return found


def template_modules() -> dict:
    """模板 `modules/<模块>/` 下有 .py 的模块 → [模板 py 路径]（§4.1.9 盲区 2/3 的基准）。"""
    out = {}
    base = TEMPLATE_DIR / "modules"
    if not base.is_dir():
        return out
    for mod_dir in sorted(base.iterdir()):
        if not mod_dir.is_dir():
            continue
        pys = sorted(mod_dir.rglob("*.py"))
        if pys:
            out[mod_dir.name] = pys
    return out


def compare(tool_file: Path, rel: str, is_blueprint: bool, is_declared: bool,
            tool_ver: str, has_header: bool):
    """返回 (kind, note, tool_ver, tpl_ver)；kind ∈ miss/ok/param/nohdr/lag/decl/drift。"""
    template_file = TEMPLATE_DIR / rel
    if not template_file.exists():
        return "miss", "", tool_ver, "?"
    same = sha256_text(read_text(tool_file)) == sha256_text(read_text(template_file))
    m = VER_RE.search(read_text(template_file))
    tpl_ver = m.group(1) if m else "?"
    behind = bool(tool_ver) and tpl_ver != "?" and ver_lt(tool_ver, tpl_ver)
    note = ""
    if tool_ver and tpl_ver != "?" and tool_ver != tpl_ver:
        same = False
        note = f" (VER {tool_ver} -> {tpl_ver})"
    if same:
        return "ok", note, tool_ver, tpl_ver
    if tool_file.name == "appconfig.py":
        return "param", "", tool_ver, tpl_ver
    if not has_header:
        return "nohdr", note, tool_ver, tpl_ver
    if is_blueprint and behind:
        return "lag", note, tool_ver, tpl_ver
    if is_declared:
        return "decl", note, tool_ver, tpl_ver
    return "drift", note, tool_ver, tpl_ver


BLUEPRINTS = load_blueprints()


def default_roots() -> list:
    """默认只扫**家族工具**：有 src/ 且有门禁 build.bat——避免把同目录下的
    无关项目（cc-haha-src 等）当成"整模块缺失"刷屏。显式 --roots 不受此限。"""
    out = []
    for d in sorted(ROOT.iterdir()):
        if not d.is_dir() or d.name.startswith(("_", ".")) or d.name == TEMPLATE_DIR.name:
            continue
        if (d / "src").is_dir() and ((d / "build.bat").exists()
                                     or (d / "scripts" / "build.bat").exists()):
            out.append(d.name)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description="template drift check")
    parser.add_argument("--roots", nargs="*", default=default_roots(),
                        help="tool dirs under my_diy_tools (default: family tools only)")
    args = parser.parse_args()

    tpl_modules = template_modules()
    drift, declared, missing, params, lags, nohdr, miss_mod, miss_file = (
        [], [], [], [], [], [], [], [])

    def emit(kind, name, tool_dir, tool_file, rel, note, tool_ver, tpl_ver, is_declared):
        leaf = tool_file.relative_to(tool_dir)
        if kind == "ok":
            print(f"[ok]    {name}/{leaf} == {TEMPLATE_DIR.name}/{rel}{note}")
        elif kind == "param":
            params.append(name)
            print(f"[param] {name}/{leaf} (参数文件，按设计豁免)")
        elif kind == "nohdr":
            nohdr.append((name, tool_file, rel))
            print(f"[NOHDR] {name}/{leaf} != {TEMPLATE_DIR.name}/{rel}{note}"
                  f" —— 该文件缺 TEMPLATE 头，补头后纳入版本/申报机制")
        elif kind == "lag":
            dec = "，已申报 override 但未跟到新版" if is_declared else ""
            lags.append((name, tool_file, rel, tool_ver, tpl_ver))
            print(f"[lag]  {name}/{leaf} lags {TEMPLATE_DIR.name}/{rel}{note}{dec}")
        elif kind == "decl":
            declared.append((name, tool_file, rel))
            print(f"[decl ] {name}/{leaf} deviates from {TEMPLATE_DIR.name}/{rel}{note} (declared override)")
        elif kind == "drift":
            drift.append((name, tool_file, rel))
            print(f"[DRIFT] {name}/{leaf} deviates from {TEMPLATE_DIR.name}/{rel}{note}")
        else:  # miss
            missing.append((name, tool_file, rel))
            print(f"[MISS ] {name}/{leaf} -> {TEMPLATE_DIR.name}/{rel} 不存在")

    for name in args.roots:
        tool_dir = ROOT / name
        if not tool_dir.is_dir():
            print(f"[skip]  {name}: no such dir")
            continue
        is_blueprint = name in BLUEPRINTS
        if is_blueprint:
            print(f"[bp  ] {name}: blueprint —— 逐文件比对，落后报 [lag]（不阻断）")

        compared, compared_rels, consumed = set(), set(), set()

        # ① 头部通道：工具自报出处的文件
        for tool_file, rel, is_declared, tool_ver in scan_tool(tool_dir):
            rel = LEGACY_ALIAS.get(rel, rel)
            compared.add(tool_file.resolve())
            compared_rels.add(rel)
            parts = rel.split("/")
            if len(parts) >= 2 and parts[0] == "modules":
                consumed.add(parts[1])
            kind, note, tv, pv = compare(tool_file, rel, is_blueprint, is_declared,
                                         tool_ver, True)
            emit(kind, name, tool_dir, tool_file, rel, note, tv, pv, is_declared)

        # ② 布局通道：src/modules/<模块>/ 下与模板同名者，**不要求工具侧有头**
        for mod, pys in sorted(tpl_modules.items()):
            mod_dir = tool_dir / "src" / "modules" / mod
            if mod_dir.is_dir():
                consumed.add(mod)
            for tpl_py in pys:
                tpl_rel = tpl_py.relative_to(TEMPLATE_DIR).as_posix()
                cand = mod_dir / tpl_py.relative_to(TEMPLATE_DIR / "modules" / mod)
                if not cand.exists():
                    # 模块已被采纳（有目录或头部通道消费了它的其它文件），却缺这一件
                    # → [MISSING-FILE] 黄灯。整个模块都没采纳的交给 [MISSING-MODULE]，
                    # 避免同一件事报两遍刷屏。
                    if mod in consumed and tpl_rel not in compared_rels:
                        miss_file.append((name, tpl_rel))
                        print(f"[MISSING-FILE] {name}: 缺 {TEMPLATE_DIR.name}/{tpl_rel}"
                              f"（模块 modules/{mod}/ 已采纳，此件未拷）")
                    continue
                if cand.resolve() in compared:
                    continue
                head = read_text(cand)[:4096]
                mver = VER_RE.search(head)
                kind, note, tv, pv = compare(
                    cand, tpl_rel, is_blueprint, bool(OVERRIDE_RE.search(head)),
                    mver.group(1) if mver else "", has_template_header(head))
                emit(kind, name, tool_dir, cand, tpl_rel, note, tv, pv,
                     bool(OVERRIDE_RE.search(head)))

        # ③ 模板有、工具没有 → 整模块缺失（黄灯）
        for mod in sorted(tpl_modules):
            if mod not in consumed:
                miss_mod.append((name, mod))
                print(f"[MISSING-MODULE] {name}: 模板 modules/{mod}/ 有代码，工具无 "
                      f"src/modules/{mod}/ 且无文件申报来自该模块（可能内联实现或未采纳）")

    print()
    for name, tool_file, rel in missing:
        print(f"[MISS ] {name}: {TEMPLATE_DIR.name}/{rel} 不存在（检查头部路径）")
    if lags or nohdr or miss_mod or miss_file:
        print(f"needs human decision (yellow, non-blocking): "
              f"lag={len(lags)}, nohdr={len(nohdr)}, missing-module={len(miss_mod)}, "
              f"missing-file={len(miss_file)}"
              f" —— 见 my-diy-tool-template/ALIGNMENT.md 对应格子")
    print(f"summary: {len(drift)} undeclared drift, {len(lags)} blueprint lag(s), "
          f"{len(declared)} declared override(s), {len(params)} param file(s), "
          f"{len(nohdr)} no-header mismatch(es), {len(miss_mod)} missing module(s), "
          f"{len(miss_file)} missing file(s), {len(missing)} missing template(s)")
    if drift or missing:
        print("fix: 把模板修复同步到该工具（独立 commit + 门禁绿），或在文件头申报 TEMPLATE-LOCAL-OVERRIDE。")
        print("     [NOHDR]/[MISSING-MODULE]/[lag] 为黄灯：需人判断跟/不跟，不阻断门禁。")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
