# -*- coding: utf-8 -*-
# TEMPLATE-MODULE: conformance_check | TEMPLATE-VER: 1.0.0
"""CONFORMANCE §5.1 的机械化落地：把"靠 AI 记得住"变成"不绿就报"。

与 sync_check.py 的分工：
  sync_check.py        只管「拷贝件与模板正本是否一致」（哈希级）
  conformance_check.py 管「条款是否落地」（语义级，但仍要求可机械判定）

设计纪律（来自 2026-09-19 首轮审计的教训）：
  ① 只写**能给出证据**的检查；判不了的宁可 WARN，不硬判 FAIL——误判会让人不再信任工具；
  ② 每条检查的输出必须带 `文件:行号` 或实际值，否则等于没说；
  ③ FAIL = 硬违规（默认让退出码非 0）；WARN = 需要人判断，只提示。

用法：
  python my-diy-tool-template/conformance_check.py                  # my_diy_tools 下全部工具
  python my-diy-tool-template/conformance_check.py --roots dsh-helper local-speak2text
  python my-diy-tool-template/conformance_check.py --strict         # WARN 也计入退出码
  python my-diy-tool-template/conformance_check.py --only C-08 C-09
"""
import argparse
import ast
import re
import subprocess
import sys
from pathlib import Path

try:  # Windows 控制台默认 GBK，中文检查标题会变乱码
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = Path(__file__).resolve().parent

# 蓝本工具（内容以模板正本为准，不按"消费方"判定）
def load_blueprints() -> set:
    cfg = TEMPLATE_DIR / "blueprints.txt"
    if not cfg.exists():
        return set()
    return {ln.strip() for ln in cfg.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")}


class Ctx:
    """一个工具的检查上下文（惰性探测，避免检查项各自重复读盘）。"""

    def __init__(self, name: str, tool_dir: Path):
        self.name = name
        self.dir = tool_dir
        self._cache = {}

    def _find(self, *cands):
        for c in cands:
            p = self.dir / c
            if p.exists():
                return p
        return None

    @property
    def src(self) -> Path:
        return self.dir / "src"

    @property
    def entry(self):
        if "entry" not in self._cache:
            self._cache["entry"] = self._find("src/main.py", "main.py")
        return self._cache["entry"]

    @property
    def build_bat(self):
        """只认真正含门禁的那个 bat（有些工具根 build.bat 只是转发壳）。"""
        if "build" not in self._cache:
            cands = [p for p in (self.dir / "build.bat",
                                 self.dir / "scripts" / "build.bat",
                                 self.dir / "build_release" / "build.bat")
                     if p.exists()]
            real = [p for p in cands if "PyInstaller" in self.read(p)
                    or "pyinstaller" in self.read(p)]
            self._cache["build"] = (real or cands or [None])[0]
        return self._cache["build"]

    @property
    def build_blob(self) -> str:
        """全部门禁 bat 的合并文本（有的工具把步骤拆在多个 bat 里）。"""
        if "bblob" not in self._cache:
            parts = []
            for p in (self.dir / "build.bat", self.dir / "scripts" / "build.bat",
                      self.dir / "build_release" / "build.bat",
                      self.dir / "release.bat"):
                if p.exists():
                    parts.append(self.read(p))
            self._cache["bblob"] = "\n".join(parts)
        return self._cache["bblob"]

    def py_files(self):
        if "py" not in self._cache:
            out = []
            for p in self.src.rglob("*.py"):
                if any(part in {".git", "__pycache__", "build", "out", "dist"}
                       for part in p.parts):
                    continue
                out.append(p)
            self._cache["py"] = sorted(out)
        return self._cache["py"]

    def read(self, path) -> str:
        try:
            return Path(path).read_text(encoding="utf-8", errors="replace")
        except OSError:
            return ""

    @property
    def app_id(self) -> str:
        """先从 appconfig 找 APP_ID，退回 paths.py。"""
        if "app_id" not in self._cache:
            found = ""
            for p in self.py_files():
                m = re.search(r'^\s*APP_ID\s*=\s*["\']([^"\']+)["\']', self.read(p), re.M)
                if m:
                    found = m.group(1)
                    break
            self._cache["app_id"] = found or self.name
        return self._cache["app_id"]

    def find_line(self, path, pattern):
        """返回 (行号, 行内容) 或 None —— 证据必须是行号。"""
        for i, line in enumerate(self.read(path).splitlines(), 1):
            if re.search(pattern, line):
                return i, line.strip()
        return None

    @property
    def guard_file(self):
        """单实例守卫的实现文件：先看模板件副本，再看内联定义。"""
        if "guard" not in self._cache:
            guess = self._find("src/modules/tray_kit/tray_kit.py")
            if guess is None:
                for p in self.py_files():
                    if re.search(r"^\s*def\s+acquire_single_instance\b",
                                 self.read(p), re.M):
                        guess = p
                        break
            self._cache["guard"] = guess
        return self._cache["guard"]

    def has_i18n(self) -> bool:
        return bool(self._find("src/modules/i18n/i18n.py", "src/i18n.py")
                    or self._find("locales", "src/locales"))

    def git_files(self, *patterns):
        try:
            r = subprocess.run(["git", "-C", str(self.dir), "ls-files", *patterns],
                               capture_output=True, timeout=30)
        except (OSError, subprocess.SubprocessError):
            return None
        if r.returncode != 0:
            return None
        return [ln for ln in r.stdout.decode("utf-8", "replace").splitlines() if ln.strip()]


CHECKS = []


def check(cid, severity, title):
    def deco(fn):
        CHECKS.append((cid, severity, title, fn))
        return fn
    return deco


# ---------------------------------------------------------------- C-01 / C-02
@check("C-01", "FAIL", "一级目录不出现 .py（B1-02）")
def c01(c: Ctx):
    hits = sorted(p.name for p in c.dir.glob("*.py"))
    return (not hits), ("根目录 .py: " + ", ".join(hits)) if hits else "一级无 .py"


@check("C-02", "FAIL", "不存在 src/tests（B1-01）")
def c02(c: Ctx):
    p = c.src / "tests"
    return (not p.exists()), str(p) if p.exists() else "无 src/tests"


# ---------------------------------------------------------------- C-03 / C-04
@check("C-03", "FAIL", "版本单一事实源，只写一处（A1-03）")
def c03(c: Ctx):
    hits = []
    for p in c.py_files():
        for i, line in enumerate(c.read(p).splitlines(), 1):
            if re.match(r'^\s*VERSION\s*=\s*["\']', line):
                hits.append("%s:%d" % (p.relative_to(c.dir).as_posix(), i))
    return (len(hits) == 1), ("VERSION 定义: " + ", ".join(hits)) if hits else "未找到 VERSION"


@check("C-04", "WARN", "登记表版本 == 磁盘版本（B2-01）")
def c04(c: Ctx):
    std = TEMPLATE_DIR / "STANDARDS.md"
    if not std.exists():
        return True, "无 STANDARDS.md"
    text = std.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"\|\s*%s\s*\|[^|]*\|[^|]*\|\s*`([\d.]+)`" % re.escape(c.name), text)
    if not m:
        return False, "B2 登记表无 %s 行" % c.name
    table_ver = m.group(1)
    disk = ""
    for p in c.py_files():
        mm = re.search(r'^\s*VERSION\s*=\s*["\']([^"\']+)["\']', c.read(p), re.M)
        if mm:
            disk = mm.group(1)
            break
    if not disk:
        return False, "无法读到磁盘 VERSION"
    return (table_ver == disk), "表 %s / 磁盘 %s" % (table_ver, disk)


# ---------------------------------------------------------------- C-05..C-07
@check("C-05", "FAIL", "README 语言切换行精确格式（A1-08/DOC-02）")
def c05(c: Ctx):
    en, zh = c.dir / "README.md", c.dir / "README.zh-CN.md"
    if not (en.exists() and zh.exists()):
        return False, "缺 README.md 或 README.zh-CN.md"
    problems = []
    if not re.search(r"^\*\*English\*\*\s*\|\s*\[简体中文\]\(README\.zh-CN\.md\)",
                     c.read(en), re.M):
        problems.append("README.md 第 3 行未写成 **English** | [简体中文](...)")
    if not re.search(r"^\[English\]\(README\.md\)\s*\|\s*\*\*简体中文\*\*",
                     c.read(zh), re.M):
        problems.append("README.zh-CN.md 未写成 [English](...) | **简体中文**")
    return (not problems), "; ".join(problems) if problems else "两份切换行格式正确"


@check("C-06", "WARN", "两份 README 都随 release 复制（DOC-05）")
def c06(c: Ctx):
    text = c.build_blob
    if not text:
        return False, "找不到 build.bat"
    has_zh = "README.zh-CN.md" in text
    return has_zh, ("build.bat 未复制 README.zh-CN.md" if not has_zh else "两份 README 均随包")


@check("C-07", "FAIL", "代码生成的 ico 不入库（A1-01/G2-01/G5-01）")
def c07(c: Ctx):
    files = c.git_files("*.ico", "*.png")
    if files is None:
        return True, "无 git 或非仓库，跳过"
    ico = [f for f in files if f.lower().endswith(".ico")]
    if ico:
        return False, "生成物入库: " + ", ".join(ico[:6])
    return True, "无 ico 入库（png 手工资产按 B1 允许）"


# ---------------------------------------------------------------- C-08..C-11
def _literal_value(raw: bool, text: str) -> str:
    """把源码里的字符串字面量还原成"值"：普通字符串 `\\\\` 是**一个**反斜杠。"""
    if raw:
        return text
    return re.sub(r"\\\\", lambda _m: "\\", text)


def _indent_block(lines, idx):
    """取 lines[idx] 所属 if 语句的块体（缩进更深的那些行）。"""
    head = lines[idx]
    indent = len(head) - len(head.lstrip())
    out = []
    for j in range(idx + 1, len(lines)):
        ln = lines[j]
        if not ln.strip():
            continue
        if (len(ln) - len(ln.lstrip())) <= indent:
            break
        out.append((j, ln))
    return out


@check("C-08", "FAIL", "互斥体名合法：Local\\ 前缀后不得再有反斜杠（SINGLE-01）")
def c08(c: Ctx):
    """用 AST 取字面量的**值**——注释里引用的反例（如本模块头部的说明）不算违规。"""
    gf = c.guard_file
    if gf is None:
        return True, "未发现自建守卫（可能未启用 T12）"
    rel = gf.relative_to(c.dir).as_posix()
    try:
        tree = ast.parse(c.read(gf))
    except SyntaxError as exc:
        return False, "%s 语法错误: %s" % (rel, exc)
    bad = []
    for node in ast.walk(tree):
        value = None
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value
        elif isinstance(node, ast.JoinedStr):     # f-string：把字面片段拼起来看整体
            value = "".join(p.value for p in node.values
                            if isinstance(p, ast.Constant) and isinstance(p.value, str))
        if value and "Local\\" in value and value.count("\\") >= 2:
            bad.append("%s:%d %s" % (rel, node.lineno, value))
    return (not bad), ("非法互斥体名（含第二个反斜杠）: " + "; ".join(bad)) if bad else "命名合法"


@check("C-09", "FAIL", "守卫自身失败必须放行（SINGLE-02/D3.2）")
def c09(c: Ctx):
    gf = c.guard_file
    if gf is None:
        return True, "未发现自建守卫"
    text = c.read(gf)
    m = re.search(r"def\s+acquire_single_instance\b[\s\S]*?(?=\ndef |\Z)", text)
    if not m:
        return True, "无 acquire_single_instance 定义"
    body = m.group(0)
    lines = body.splitlines()
    fail_open = re.search(r"except[^\n]*:[\s\S]{0,300}?return\s+True", body) is not None
    for idx, ln in enumerate(lines):
        if re.match(r"\s*if\s+not\s+handle\b", ln):
            block = [b for _j, b in _indent_block(lines, idx)]
            if any(re.search(r"return\s+False", b) for b in block):
                return False, ("`if not handle` 的块体直接 return False = 失败即拒绝"
                               "（守卫自身失败必须放行）")
            if any(re.search(r"return\s+True", b) for b in block):
                fail_open = True
    if not fail_open:
        return False, "守卫失败时没有显式放行路径（既无 try/except→True，也无 not handle→True）"
    return True, "失败方向为打开"


@check("C-10", "FAIL", "诊断参数不绕过正常启动路径（SINGLE-04/D3.1）")
def c10(c: Ctx):
    if c.entry is None:
        return True, "无入口文件"
    text = c.read(c.entry)
    if "--smoke" not in text:
        return True, "无 --smoke"
    m = re.search(r"def\s+smoke\b[\s\S]*?(?=\ndef |\Z)", text)
    body = m.group(0) if m else ""
    covered = bool(re.search(r"single_instance|mutex|MUTEX", body, re.I))
    return covered, ("smoke() 未覆盖单实例守卫（--smoke 绕过守卫，测不到真实启动路径）"
                     if not covered else "smoke 覆盖了守卫")


@check("C-11", "FAIL", "运行检测匹配串能命中当前 exe 名（SINGLE-05/D1-02）")
def c11(c: Ctx):
    text = c.build_blob
    if not text:
        return True, "无 build.bat"
    appname = re.search(r'set\s+APPNAME=(\S+)', text)
    exe = (appname.group(1) if appname else c.app_id) + ".exe"
    literal = None
    for line in text.splitlines():
        if "tasklist" in line and "findstr" in line:
            mm = re.search(r'/c:"([^"]+)"', line)
            if mm:
                literal = mm.group(1)
                break
    if literal is None:
        return False, "未找到运行检测（tasklist | findstr）的匹配串"
    probe = literal.replace("%APPNAME%", appname.group(1) if appname else c.app_id)
    if probe and probe in exe:
        return True, "匹配串 %r 能命中 %s" % (probe, exe)
    return False, ("匹配串 %r 匹配不到 %s —— 只有旧版带版本号的 exe 会被命中，"
                   "当前实例在跑也拦不住构建" % (probe, exe))


# ---------------------------------------------------------------- C-12..C-15
@check("C-12", "FAIL", "菜单签名重画被消费（E2-09）")
def c12(c: Ctx):
    if c.entry is None:
        return True, "无入口文件"
    text = c.read(c.entry)
    # 两种合法形态：直接用模板类，或内联等构（模板类名 / 自带签名+菜单占用探测）
    if "MenuSignature" in text:
        return True, "使用模板 MenuSignature"
    inline = ("menu_is_open" in text and
              ("tray_signature" in text or "MENU_DIRTY" in text
               or "GUI_INMENUMODE" in text))
    if inline:
        return True, "内联等构（签名比较 + 菜单占用探测）"
    return False, "既无 MenuSignature 也无内联签名/占用探测（菜单每拍全量重建，开着会被打断）"


@check("C-13", "WARN", "存在队列封送骨架（E1-03/I-03）")
def c13(c: Ctx):
    hits = [p.relative_to(c.dir).as_posix() for p in c.py_files()
            if re.search(r"\bui_q\b|\bui_post\b|\bui_call\b", c.read(p))]
    return bool(hits), ("队列封送在: " + ", ".join(hits)) if hits else "未发现 ui_q/ui_post"


@check("C-14", "FAIL", "日志轮转 1MB x 3（D4-02）")
def c14(c: Ctx):
    lk = c._find("src/modules/log_kit/log_kit.py", "src/log_kit.py", "log_kit.py")
    if lk is None:
        return False, "未找到 log_kit"
    text = c.read(lk)
    ok = ("maxBytes" in text or "LOG_MAX_BYTES" in text) and \
         ("backupCount" in text or "LOG_BACKUPS" in text)
    rel = lk.relative_to(c.dir).as_posix()
    return ok, ("%s 缺 maxBytes/backupCount" % rel) if not ok else "%s 轮转参数在位" % rel


@check("C-15", "WARN", "托盘有「打开日志目录」（D4-02/A3-02）")
def c15(c: Ctx):
    pats = ("打开日志目录", "open_log_dir", "Open log folder", "open_logs")
    hits = [p.relative_to(c.dir).as_posix() for p in c.py_files()
            if any(k in c.read(p) for k in pats)]
    locale = c.dir / "locales"
    if not hits and locale.is_dir():
        hits = [p.name for p in locale.glob("*.json")
                if any(k in c.read(p) for k in pats)]
    return bool(hits), ("日志目录入口在: " + ", ".join(hits)) if hits else "未发现「打开日志目录」入口"


# ---------------------------------------------------------------- C-16..C-20
@check("C-16", "FAIL", "实例隔离：_CONFIG 与 _DATA_DIR 两个 env 都要有（B3-04/B4-04）")
def c16(c: Ctx):
    """找**实际读取点**，两种写法都要认：
        os.environ.get("LOCALSPEAK2TEXT_DATA_DIR")          # 字面量
        os.environ.get(_ENV_PREFIX + "_DATA_DIR")           # 常量拼接（l-s2t 收敛后用这种）
    2026-09-19 修：原实现只认字面量，l-s2t 改成拼接式后被误报成"两个 env 都没有"。
    """
    # 判据：同一行里既有 `environ` 又有该后缀。三种写法都能覆盖：
    #   environ.get("APP_DATA_DIR") / environ.get(_PREFIX + "_DATA_DIR") / environ.get(f"{X}_DATA_DIR")
    # （2026-09-19 修：先前用"紧贴引号的完整键名"正则，把 f-string / 拼接式全判成缺失，
    #   造成 dsh/ocx 的 `_DATA_DIR` 与 l-s2t 的两个 env 都被误报。）
    # 只认 environ 的**取参表达式**，避免把 `DEFAULT_CONFIG` 这类含 `_CONFIG` 的标识符误判
    # （2026-09-19 第二轮修正：先用"整键名"，漏了拼接/f-string；改用"同行含子串"，又误收 DEFAULT_CONFIG）。
    env_arg = re.compile(r"environ(?:\.get\(\s*|\[\s*)([^)\]\n]{0,160})")
    want, missing = {}, []
    for suffix in ("_CONFIG", "_DATA_DIR"):
        hits = []
        for p in c.py_files():
            rel = p.relative_to(c.dir).as_posix()
            for i, line in enumerate(c.read(p).splitlines(), 1):
                for arg in env_arg.findall(line):
                    # 后缀之后不能紧跟标识符字符，否则 NPM_CONFIG_PREFIX 会被当成 `_CONFIG`
                    # （2026-09-19 第三轮修正：dsh/ocx 的 NPM_CONFIG_PREFIX 曾骗过本检查）
                    if re.search(re.escape(suffix) + r"(?![A-Za-z0-9_])", arg):
                        hits.append("%s:%d" % (rel, i))
                        break
        want[suffix] = hits
        if not hits:
            missing.append(suffix)
    if missing:
        return False, ("缺 %s 环境变量读取点（测试/自检无法钉住配置或隔离数据根）"
                       % "、".join(missing))
    return True, "; ".join("%s@%s" % (s, ",".join(h[:2])) for s, h in want.items())


@check("C-17", "FAIL", "测试不触碰用户真实注册表/数据区（B4-04/D3-03）")
def c17(c: Ctx):
    tdir = c.dir / "tests"
    if not tdir.is_dir():
        return True, "无 tests/（已在 B1-01 单列）"
    bad = []
    for p in tdir.rglob("*.py"):
        text = c.read(p)
        if not re.search(r"HKEY_CURRENT_USER|HKCU", text):
            continue
        # 允许"写注册表"的用例，但必须备份+还原（finally/restore），否则跑测试会改坏用户配置
        if re.search(r"finally|restore|backup", text, re.I):
            continue
        bad.append(p.relative_to(c.dir).as_posix())
    return (not bad), ("测试写用户注册表且无还原: " + ", ".join(bad)) if bad else "测试未触碰用户注册表（或已备份还原）"


@check("C-18", "FAIL", "build.bat 门禁含 sync_check 与测试（B4-03/D1-05/D3-02）")
def c18(c: Ctx):
    text = c.build_blob
    if not text:
        return False, "找不到 build.bat"
    problems = []
    if "sync_check" not in text and c.name not in load_blueprints():
        problems.append("门禁无 sync_check 步")
    if not c.dir.joinpath("tests").is_dir():
        problems.append("无 tests/ 目录（D1 门禁 3 / 故障回归无载体）")
    elif "tests\\" not in text and "tests/" not in text:
        problems.append("门禁不跑 tests/")
    return (not problems), "; ".join(problems) if problems else "门禁含 sync_check 与测试"


@check("C-19", "WARN", "模板件头部 TEMPLATE-FROM/TEMPLATE-VER 齐（B4-01/B4-03）")
def c19(c: Ctx):
    mods = c.src / "modules"
    if not mods.is_dir():
        return True, "无 src/modules/"
    missing = []
    for p in sorted(mods.rglob("*.py")):
        if p.name == "__init__.py":
            continue
        head = c.read(p)[:4096]
        if "TEMPLATE-FROM" not in head and "TEMPLATE-MODULE" not in head \
                and "TEMPLATE-LOCAL-OVERRIDE" not in head:
            missing.append(p.relative_to(c.dir).as_posix())
    return (not missing), ("无模板头: " + ", ".join(missing)) if missing else "模板件头部齐全"


CJK = re.compile(r"[\u4e00-\u9fff]")


def _call_name(node) -> str:
    f = getattr(node, "func", None)
    if isinstance(f, ast.Attribute):
        return f.attr
    if isinstance(f, ast.Name):
        return f.id
    return ""


@check("C-20", "WARN", "启用 i18n 的工具无词表外中文（A1-10/E4-02）")
def c20(c: Ctx):
    mods = c.src / "modules" / "i18n"
    if (mods / "pairs.json").exists():
        return True, "重形态（pairs.json 中文即键，STANDARDS §E4 明示许可），跳过"
    if not c.has_i18n():
        return True, "未启用 i18n（T1 未触发或待办）"
    if c.entry is None:
        return True, "无入口文件"
    try:
        tree = ast.parse(c.read(c.entry))
    except SyntaxError as exc:
        return False, "入口文件语法错误: %s" % exc
    bad = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if _call_name(node) == "t":        # i18n.t(...) / t(...) —— 正当出口
            continue
        args = list(node.args) + [k.value for k in node.keywords]
        for a in args:
            # 递归展开 BinOp("..." % x) / IfExp / f-string，否则拼出来的文案会被漏掉
            for sub in ast.walk(a):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str) \
                        and CJK.search(sub.value):
                    bad.append("%s:%d %s" % (c.entry.relative_to(c.dir).as_posix(),
                                             sub.lineno, sub.value[:60]))
    return (not bad), ("词表外中文 %d 处: %s" % (len(bad), " | ".join(bad[:4]))
                       if bad else "未发现词表外中文（AST 级）")


# ---------------------------------------------------------------- 主流程
def run_tool(name: str, only=None) -> tuple:
    c = Ctx(name, ROOT / name)
    rows = []
    for cid, severity, title, fn in CHECKS:
        if only and cid not in only:
            continue
        try:
            ok, detail = fn(c)
        except Exception as exc:  # 检查自身出错不应让整轮崩
            ok, detail = False, "检查异常: %r" % (exc,)
        rows.append((cid, severity, title, ok, detail))
    return c, rows


def main() -> int:
    ap = argparse.ArgumentParser(description="family conformance check")
    ap.add_argument("--roots", nargs="*", default=None)
    ap.add_argument("--strict", action="store_true", help="WARN 也计入退出码")
    ap.add_argument("--only", nargs="*", default=None, help="只跑指定检查 ID")
    args = ap.parse_args()

    def is_family_tool(d: Path) -> bool:
        """家族工具 = src\\ + 构建脚本（避免把同目录下的无关项目也拉进来）。"""
        return (d / "src").is_dir() and (
            (d / "build.bat").exists() or (d / "scripts" / "build.bat").exists())

    names = args.roots or sorted(
        d.name for d in ROOT.iterdir()
        if d.is_dir() and not d.name.startswith(("_", "."))
        and d.name not in {"__pycache__", TEMPLATE_DIR.name}
        and is_family_tool(d)
    )

    fails = warns = 0
    for name in names:
        tool_dir = ROOT / name
        if not tool_dir.is_dir():
            print("[skip] %s: no such dir" % name)
            continue
        c, rows = run_tool(name, set(args.only) if args.only else None)
        print("=" * 78)
        print("%s  (APP_ID=%s)" % (name, c.app_id))
        print("=" * 78)
        for cid, severity, title, ok, detail in rows:
            tag = "ok  " if ok else ("FAIL" if severity == "FAIL" else "WARN")
            if not ok:
                if severity == "FAIL":
                    fails += 1
                else:
                    warns += 1
            print("  [%s] %-5s %-46s %s" % (tag, cid, title, detail))
        print()

    print("summary: %d FAIL, %d WARN" % (fails, warns))
    if fails:
        print("fix: 逐条见 my-diy-tool-template/CONFORMANCE.md 对应 ID。")
        return 1
    if warns and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
