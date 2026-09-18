# TEMPLATE-MODULE: sync_check | TEMPLATE-VER: 1.1.0
# T10 · 模板漂移检查（防漂移四件套之二，执行文档 D1）。
#
# 原理：扫描各工具目录里带 `# TEMPLATE-FROM: _template/<相对路径>` 头的文件，
# 与模板正本做**归一化哈希**比对——双方剔除 `# TEMPLATE-*` 元信息行后哈希相等
# 即为一致（副本头标明出处，正本头标明模块身份，这两行差异不计入）。
#
# 判定：
#   [ok]    归一化后一致，且 TEMPLATE-VER 相同
#   [decl ] 内容有差异，但文件头申报了 TEMPLATE-LOCAL-OVERRIDE: <原因>
#   [DRIFT] 内容或 VER 不一致且未申报 —— 红灯，退出码 1
#   [param] appconfig.py —— 参数文件，按设计豁免比对
#   [skip]  蓝本工具（BLUEPRINT_TOOLS）：模板的来源，修改应反向沉淀进模板
#
# 用法：
#   python _template/sync_check.py                    # 检查 my_diy_tools 下所有工具
#   python _template/sync_check.py --roots dsh-helper opencodex-helper

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent      # my_diy_tools/
TEMPLATE_DIR = Path(__file__).resolve().parent     # _template/
BLUEPRINT_TOOLS = {"local-speak2text", "reme-helper"}
FROM_RE = re.compile(r"^#\s*TEMPLATE-FROM:\s*_template/([\w./-]+)", re.M)
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


def scan_tool(tool_dir: Path):
    """返回 [(tool_file, template_rel, declared, tool_ver)]。"""
    found = []
    for py in sorted(tool_dir.rglob("*.py")):
        parts = py.parts
        if ".git" in parts or "__pycache__" in parts or "build" in parts or "out" in parts:
            continue
        try:
            head = py.read_text(encoding="utf-8", errors="replace")[:4096]
        except OSError:
            continue
        match = FROM_RE.search(head)
        if not match:
            continue
        ver = VER_RE.search(head)
        found.append((py, match.group(1), bool(OVERRIDE_RE.search(head)),
                      ver.group(1) if ver else ""))
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description="template drift check")
    parser.add_argument("--roots", nargs="*", default=sorted(
        d.name for d in ROOT.iterdir()
        if d.is_dir() and not d.name.startswith(("_", "."))
        and d.name not in {"__pycache__"}
    ), help="tool dirs under my_diy_tools (default: all non-underscore dirs)")
    args = parser.parse_args()

    drift, declared, missing, params = [], [], [], []
    for name in args.roots:
        if name in BLUEPRINT_TOOLS:
            print(f"[skip]  {name}: blueprint (template source)")
            continue
        tool_dir = ROOT / name
        if not tool_dir.is_dir():
            print(f"[skip]  {name}: no such dir")
            continue
        for tool_file, rel, is_declared, tool_ver in scan_tool(tool_dir):
            rel = LEGACY_ALIAS.get(rel, rel)
            template_file = TEMPLATE_DIR / rel
            if not template_file.exists():
                missing.append((name, tool_file, rel))
                print(f"[MISS ] {name}/{tool_file.relative_to(tool_dir)} -> _template/{rel} 不存在")
                continue
            same = sha256_text(tool_file.read_text(encoding="utf-8", errors="replace")) \
                == sha256_text(template_file.read_text(encoding="utf-8", errors="replace"))
            tpl_ver = (VER_RE.search(template_file.read_text(encoding="utf-8", errors="ignore")) or [None, "?"])[1]
            ver_note = ""
            if tool_ver and tpl_ver != "?" and tool_ver != tpl_ver:
                same = False
                ver_note = f" (VER {tool_ver} != {tpl_ver})"
            label = tool_file.relative_to(tool_dir)
            if same:
                print(f"[ok]    {name}/{label} == _template/{rel}")
            elif tool_file.name == "appconfig.py":
                params.append(name)
                print(f"[param] {name}/{label} (参数文件，按设计豁免)")
            elif is_declared:
                declared.append((name, tool_file, rel))
                print(f"[decl ] {name}/{label} deviates from _template/{rel}{ver_note} (declared override)")
            else:
                drift.append((name, tool_file, rel))
                print(f"[DRIFT] {name}/{label} deviates from _template/{rel}{ver_note}")

    print()
    for name, tool_file, rel in missing:
        print(f"[MISS ] {name}: _template/{rel} 不存在（检查头部路径）")
    print(f"summary: {len(drift)} undeclared drift, {len(declared)} declared override(s), "
          f"{len(params)} param file(s), {len(missing)} missing template(s)")
    if drift or missing:
        print("fix: 把模板修复同步到该工具（独立 commit + 门禁绿），或在文件头申报 TEMPLATE-LOCAL-OVERRIDE。")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
