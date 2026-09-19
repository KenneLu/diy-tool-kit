# -*- coding: utf-8 -*-
# TEMPLATE-MODULE: conformance_check | TEMPLATE-VER: 1.3.0
# 1.3.0：新增 **C-22 bat/cmd 字节卫生**（CRLF + 无 0x09 + 纯 ASCII，逐文件逐行报位置）。
#   把"bat 必须 CRLF + 纯 ASCII"从口头纪律升级成可执行判据；五条 selftest 样本（TAB / LF-only /
#   非 ASCII / 混合 / 合规）。构建产物与脚手架目录（release/out/dist/_internal/.cache/.verify-scratch）
#   跳过——它们不是作者手写、也不入库。
# 1.2.0：C-10 判据重写——旧判据只要 smoke() 里出现 `mutex|single_instance` **任意子串**就算过，
#   太松（"把 --smoke 提前分派 + 留一句注释"就能骗过），**区分不了"覆盖了"与"绕过了"**。
#   现判据（D3.3）：smoke() 内必须有**探针** `mutex_name_is_valid(...)` 且**判了结果**；
#   真跑守卫（acquire_single_instance）判 FAIL 并说明会弹模态框挂死构建；
#   `single_instance_free` 不算探针（用户实例在跑时返回 False → 假红）。四种形态各一条 selftest。
# 1.1.0：新增 C-23（模块级状态被 global 重绑 = 脆形态）与 C-24（菜单读的容器状态未进签名 /
#   有菜单无签名机制），补 STANDARDS §D6 的机械阶梯 C-21 → C-23 → C-24；两条都有 --selftest
#   正反样本。C-22 号被"bat/cmd 字节卫生"占用，故本组从 C-23 起编号。
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


# 探针 = "验名字合法性，不占锁不弹窗"。**不能**认 single_instance_free：用户常驻实例
# 在跑时它返回 False，拿它当冒烟断言会假红（D3.3 的禁忌之一）。
_PROBE_NAMES = {"mutex_name_is_valid"}
# 真跑守卫的证据：出现即说明冒烟可能弹模态框把构建挂死——仅在探针缺失时拿来作提示。
_GUARD_NAMES = {"acquire_single_instance", "single_instance_free", "warn_duplicate_instance"}
_SMOKE_PROBE = re.compile("|".join(_PROBE_NAMES))
_SMOKE_GUARD = re.compile("|".join(_GUARD_NAMES))


def _callee_name(node) -> str:
    """调用表达式取被调名：`f()` / `mod.f()` / `self.f()` 都归一到 `f`。"""
    if not isinstance(node, ast.Call):
        return ""
    fn = node.func
    if isinstance(fn, ast.Name):
        return fn.id
    if isinstance(fn, ast.Attribute):
        return fn.attr
    return ""


def _guarded_probe_calls(fn) -> tuple:
    """在函数体里找**被判断过的探针调用**，返回 (命中数, 只调未判数)。

    "判过"= 调用出现在 `if` / `while` / `assert` 的条件里，或参与 `not`/`and`/`or`
    布尔组合——即**结果被消费**。只出现在表达式语句里的 `mutex_name_is_valid(...)` 不算：
    覆盖 ≠ 调用（D3.3 的判据要求"能打红构建"）。
    """
    guarded = plain = 0
    for node in ast.walk(fn):
        if isinstance(node, (ast.If, ast.While)):
            conds = [node.test]
        elif isinstance(node, ast.Assert):
            conds = [node.test]
        else:
            continue
        for cond in conds:
            for sub in ast.walk(cond):
                if _callee_name(sub) in _PROBE_NAMES:
                    guarded += 1
    for node in ast.walk(fn):
        if isinstance(node, ast.Expr) and _callee_name(node.value) in _PROBE_NAMES:
            plain += 1
    return guarded, plain


@check("C-10", "FAIL", "诊断参数不绕过正常启动路径：smoke 须有守卫**探针**并判结果（D3.1/D3.3）")
def c10(c: Ctx):
    """判据要能区分"**覆盖了**"和"**绕过了**"——这是本条两轮修正的核心。

    * 旧判据（2.0.x）：`smoke()` 里出现 `mutex|single_instance` **任意子串**就算过。
      太松：把 `--smoke` 提前分派、函数体里留一句注释提到 mutex 都能骗过它。
    * 现判据（D3.3）：**AST 取 `def smoke` 的 body 范围**，要求其中有**探针调用**
      `mutex_name_is_valid(...)`，且该调用**被条件/断言消费**（`if not …` / `assert`）。
      只调用不判断 = 没有覆盖；写在注释里 = 更不算（子串判据会误收，AST 不会）。
    * 反例（不许当解）：`acquire_single_instance()` **真跑** —— 用户常驻实例在跑时会弹
      **模态**重复启动框，把无人值守的构建挂死（本家族已踩两次）。
    """
    if c.entry is None:
        return True, "无入口文件"
    text = c.read(c.entry)
    if "--smoke" not in text:
        return True, "无 --smoke"
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return False, "入口文件语法错误，无法判定：%s" % exc
    smokes = [n for n in ast.walk(tree)
              if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "smoke"]
    if not smokes:
        return False, ("有 --smoke 但没有 `def smoke` 可查（AST 判据要求冒烟逻辑落在具名函数里，"
                       "这样才判得了'覆盖'与'绕过'）")
    guarded = plain = 0
    for fn in smokes:
        g, p = _guarded_probe_calls(fn)
        guarded += g
        plain += p
    if guarded:
        return True, "smoke 用探针覆盖了守卫名字合法性，且结果被条件/断言消费"
    if plain:
        return False, ("smoke 调了 mutex_name_is_valid 但**没判结果**（覆盖 ≠ 调用："
                       "要么 if not … 中止，要么 assert）")
    body_src = "\n".join(c.read(c.entry).splitlines()[smokes[0].lineno - 1:smokes[0].end_lineno])
    if _SMOKE_GUARD.search(body_src):
        return False, ("smoke 里是**真跑守卫**（acquire_single_instance/…）：用户常驻实例在跑时"
                       "会弹模态重复启动框，把构建挂死。改用探针 tray_kit.mutex_name_is_valid()")
    return False, ("smoke() 没有守卫覆盖（SINGLE-04/D3.1）。把 --smoke 提到守卫之前"
                   "**不算**覆盖——那是把守卫从被测路径里删掉；正确形态是探针："
                   "`if not tray_kit.mutex_name_is_valid(APP_ID): raise RuntimeError(...)`")


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


# ---------------------------------------------------------------- C-21
def _star_copied_state(mod_dir: Path, read) -> tuple:
    """返回 (module_name, [被静态拷贝的状态名])；无风险时 module_name 为空。

    形状（已出现两例：`i18n.LANG`、`update_helper.PENDING_CMD`，**两次都静默失效**）：
      ① `__init__.py` 用 `from .<m> import *` → 包命名空间拿到一份**值拷贝**；
      ② 子模块里存在**模块级公有名**且被函数内 `global` **重绑** → 真值只改子模块那份；
      ③ 外部读 `包.名字` → 永远是导入时定格的旧值。
    """
    init = mod_dir / "__init__.py"
    py = mod_dir / f"{mod_dir.name}.py"
    if not (init.exists() and py.exists()):
        return "", []
    m = re.search(r"^\s*from\s+\.(\w+)\s+import\s+\*", read(init), re.M)
    if not m:
        return "", []
    try:
        tree = ast.parse(read(py))
    except SyntaxError:
        return "", []
    top = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for tg in node.targets:
                if isinstance(tg, ast.Name) and not tg.id.startswith("_"):
                    top.add(tg.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
                and not node.target.id.startswith("_"):
            top.add(node.target.id)
    rebound = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Global):
            rebound.update(n for n in node.names if not n.startswith("_"))
    return m.group(1), sorted(top & rebound)


@check("C-21", "FAIL", "包 import * 不得复制可变状态（外部读会拿到过期值）")
def c21(c: Ctx):
    """机械化"状态副本"这一形状——它已静默失效两次（i18n.LANG / update_helper.PENDING_CMD）。

    命中即说明：包门面用 `import *` 拷了状态，而子模块会用 `global` 重绑它 →
    外部读包拿到永久旧值（i18n 表现为菜单不刷新；update_helper 表现为 apply.cmd 永不拉起）。
    修法：门面只绑函数 + PEP 562 `__getattr__` 委派子模块（见两模块 2.1.1 / 1.1.0）。
    """
    mods = c.src / "modules"
    if not mods.is_dir():
        return True, "无 src/modules/"
    bad = []
    for d in sorted(p for p in mods.iterdir() if p.is_dir()):
        mod, names = _star_copied_state(d, c.read)
        if names:
            bad.append("%s: %s" % ((d / "__init__.py").relative_to(c.dir).as_posix(),
                                   ",".join(names)))
    return (not bad), ("会被 import * 静态拷贝的状态（外部读恒旧值）: " + "; ".join(bad)
                       if bad else "无 import * 状态复制")


# ---------------------------------------------------------------- C-22..C-24
_CONTAINERS = (ast.Dict, ast.List, ast.Set, ast.ListComp, ast.DictComp, ast.SetComp)

# --- C-22：bat/cmd 字节卫生 -------------------------------------------------
# 只扫**源**：构建产物（release/out/dist/_internal）与脚手架/缓存目录（.cache/.verify-scratch，
# 两者都在 .gitignore 里）跳过——它们不是作者手写的、也不入库，报出来只会淹没真问题。
# ⚠️ 但"生成的 bat 是 LF"这件事本身仍要记在案：恰恰是脚本写文件把 CRLF 写丢了的现场（见 J 坑）。
_BAT_SKIP_DIRS = {".git", "__pycache__", "build", "dist", "release", "out", "_internal",
                  "node_modules", ".verify-scratch", ".cache"}


def _bat_files(root: Path):
    out = []
    for p in root.rglob("*"):
        if p.suffix.lower() not in (".bat", ".cmd") or not p.is_file():
            continue
        if any(part in _BAT_SKIP_DIRS for part in p.parts):
            continue
        out.append(p)
    return sorted(out)


def _bat_hygiene(path: Path) -> list:
    """返回 [`第N行:原因`]；空列表 = 合规。判据：**CRLF / 无 0x09 / 纯 ASCII**。

    为什么是字节级而不是"看着没问题"：`write_text("...\\t...")` 会把 `\\t` 当**转义**解释，
    写进 .bat 就成了真 TAB——`"%PY%" tests<TAB>est_update_bat.py` 这种行**永远跑不起来**；
    若它前面还有别的门禁先把构建拦下，这条坏行就**永远不会暴露**（2026-09-19 reme 实例）。
    LF-only 更隐蔽：cmd 对 `for`/`goto` 行的解析在 LF 下会异常。中文则按 OEM 码页撕碎后续行。
    """
    data = path.read_bytes()
    lf_only, tabs, nonascii = [], [], []
    line = 1
    for i, b in enumerate(data):
        if b == 0x0A:
            if i == 0 or data[i - 1] != 0x0D:
                lf_only.append(line)
            line += 1
        elif b == 0x09:
            tabs.append(line)
        elif b > 0x7F and (not nonascii or nonascii[-1] != line):
            nonascii.append(line)
    bad = []
    if lf_only:
        bad.append("LF-only 行 %d 处（首见 第%d 行；必须 CRLF）" % (len(lf_only), lf_only[0]))
    if tabs:
        bad.append("含 0x09 TAB %d 处（第 %s 行）"
                   % (len(tabs), ",".join(str(n) for n in tabs[:6])))
    if nonascii:
        bad.append("非 ASCII %d 行（第 %s 行；cmd 按 OEM 码页解析）"
                   % (len(nonascii), ",".join(str(n) for n in nonascii[:6])))
    return bad


@check("C-22", "FAIL", "bat/cmd 字节卫生：CRLF + 无 TAB + 纯 ASCII（B3/J 坑）")
def c22(c: Ctx):
    """把"bat 必须 CRLF + 纯 ASCII"从口头纪律升级成**可执行判据**（逐文件逐行报位置）。

    三个判据各对应一次真实事故：TAB（转义写坏行 ⇒ 门禁从未执行）、LF-only（cmd 解析异常）、
    非 ASCII（OEM 码页撕碎后续行）。**每次新增/修改 bat 行后必须跑一次本检查自证**——
    这类损坏不会报错，只会让某行静默失效。
    """
    files = _bat_files(c.dir)
    if not files:
        return True, "无 .bat/.cmd（本工具用别的方式构建）"
    bad = []
    for p in files:
        for item in _bat_hygiene(p):
            bad.append("%s: %s" % (p.relative_to(c.dir).as_posix(), item))
    return (not bad), ("；".join(bad) if bad
                       else "%d 个 bat/cmd 全部 CRLF+ASCII 且无 TAB" % len(files))




def _is_container(node) -> bool:
    if isinstance(node, _CONTAINERS):
        return True
    if isinstance(node, ast.Call):
        fn = node.func
        name = fn.id if isinstance(fn, ast.Name) else (
            fn.attr if isinstance(fn, ast.Attribute) else "")
        return name in {"dict", "list", "set", "defaultdict", "OrderedDict", "deque"}
    return False


def _rebound_state(py_path: Path, read) -> list:
    """返回 [`名字:行号(形态)`]：模块级公有名被函数内 `global` **重绑**。

    这正是两次静默失效的形状（`i18n.LANG`、`update_helper.PENDING_CMD`）：
    `global` 重绑 = 换了一个对象/值，而**导入方手里的引用不会跟着变**
    （`import *` 拷的是对象引用，标量更是直接拷值）⇒ 外部读到的是死副本。
    **就地修改**（`d.update(...)` / `d["k"]=v`）不受影响——那两条路是 STANDARDS §D6 认可的：
    容器就地改，或经访问器暴露。容器**重绑**同样在禁列（与标量同理），故两类都报、分别标注。
    """
    try:
        tree = ast.parse(read(py_path))
    except SyntaxError:
        return []
    kinds = {}
    for node in tree.body:
        targets = []
        if isinstance(node, ast.Assign):
            targets = [t for t in node.targets if isinstance(t, ast.Name)]
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            targets = [node.target]
        for tg in targets:
            if not tg.id.startswith("_"):
                kinds[tg.id] = ("容器重绑" if _is_container(node.value) else "标量", node.lineno)
    rebound = {n for node in ast.walk(tree) if isinstance(node, ast.Global)
               for n in node.names}
    return ["%s:%d(%s)" % (n, kinds[n][1], kinds[n][0]) for n in sorted(rebound & set(kinds))]


@check("C-23", "WARN", "模块级状态不得被 global 重绑（外部读会拿到死副本，STANDARDS §D6）")
def c23(c: Ctx):
    """C-21 的**前一层**：C-21 查"已经坏了"（`import *` 真的拷了状态），本条查**脆形态**——
    状态写成模块级名字、由函数 `global` 重绑。这样写今天可能没事（门面若用 `__getattr__`
    委派就挡住了），但任何人把 `import *` 加回来就静默复发。

    正路只有两条（§D6）：**可变容器就地改**（`d.update()` / `d[k]=v`），或**经访问器暴露**。
    """
    mods = c.src / "modules"
    if not mods.is_dir():
        return True, "无 src/modules/"
    bad = []
    for p in sorted(mods.rglob("*.py")):
        if p.name == "__init__.py":
            continue
        for hit in _rebound_state(p, c.read):
            bad.append("%s: %s" % (p.relative_to(c.dir).as_posix(), hit))
    return (not bad), ("模块级状态被 global 重绑（改为容器就地改/访问器）: " + "; ".join(bad)
                       if bad else "无 global 重绑的模块级状态")


# ⚠️ 参数表用 `[^)]*`，**不能**用 `.*?\):`：带返回注解的签名（`def f() -> tuple:`）里没有
# 紧跟的 `):`，非贪婪展开会一路吞到别处的 `):`，于是"签名体"取到的是**另一个函数**——
# 实测把 reme 的 `tray_signature` 误判成不含 HELPER_UPDATE_STATE（假红灯）。
_SIG_DEF = re.compile(r"^def (\w*signature\w*)\s*\([^)]*\)[^:\n]*:(.*?)(?=^\S|\Z)", re.M | re.S)
_MENU_KW = re.compile(r"(?:enabled|checked|visible|default)\s*=\s*(.+)")


def _menu_state_tokens(text: str, read) -> list:
    """菜单动态项里引用的**模块级容器**名（如 `CFG` / `HELPER_UPDATE_STATE`）。

    刻意**只认容器**：函数式读取（`service_is_healthy()`）与类属性状态由各自的重画路径负责，
    本检查看不到，也就不硬判（宁可窄、不可误报——误报会让人不再信任工具，见文件头纪律①）。
    """
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    containers = set()
    for node in tree.body:
        if isinstance(node, ast.Assign) and _is_container(node.value):
            containers.update(t.id for t in node.targets if isinstance(t, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
                and node.value is not None and _is_container(node.value):
            containers.add(node.target.id)
    if not containers:
        return []
    used = set()
    for line in text.splitlines():
        m = _MENU_KW.search(line)
        if not m:
            continue
        used.update(n for n in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", m.group(1)) if n in containers)
    return sorted(used)


@check("C-24", "WARN", "驱动托盘菜单的状态必须进入菜单签名（E2-09/§D6）")
def c24(c: Ctx):
    """菜单只在**签名变化**时重画；签名漏掉某个状态 ⇒ 该状态变了菜单也不刷新。

    reme 已实测踩过（`tray_signature()` 原先不含更新状态 ⇒ 后台查到新版后「下载并更新」
    不亮，2026-09-19 修）。本条只管**模块级容器**这一种载体（高置信）：容器在菜单项里被读、
    却不进签名 → 报。函数式读取与类属性状态不在范围内（见 `_menu_state_tokens` 的说明）。
    """
    menu_files = [p for p in c.py_files() if "MenuItem(" in c.read(p)]
    if not menu_files:
        return True, "未见托盘菜单（无 MenuItem(）"
    problems, checked = [], 0
    for p in menu_files:
        text = c.read(p)
        m = _SIG_DEF.search(text)
        has_sigobj = "MenuSignature(" in text
        tokens = _menu_state_tokens(text, c.read)
        if not m and not has_sigobj:
            problems.append("%s 有菜单但无签名函数/MenuSignature（状态变了不会重画）"
                            % p.relative_to(c.dir).as_posix())
            continue
        if not tokens:
            checked += 1
            continue
        body = (m.group(2) if m else text)
        missing = [t for t in tokens if t not in body]
        if missing:
            problems.append("%s: 菜单读了 %s 但签名不含它"
                            % (p.relative_to(c.dir).as_posix(), ",".join(missing)))
        checked += 1
    return (not problems), ("；".join(problems) if problems
                            else "签名覆盖菜单容器状态（受检文件 %d）" % checked)


def selftest() -> int:
    """C-21/C-23/C-24 反向自证（`--selftest`，可重复执行）：合成样本，正例须点名、反例须放行。"""
    import shutil
    import tempfile
    base = Path(tempfile.mkdtemp(prefix="conf_selftest_"))
    try:
        cases = []
        for name, init_src, want in (
            ("pos", "from .demo import *  # noqa: F401,F403\n", False),   # 复制 → 应报
            ("neg", "from .demo import set_state\n", True),               # 显式导入 → 放行
        ):
            d = base / name / "src" / "modules" / "demo"
            d.mkdir(parents=True)
            (d / "demo.py").write_text(
                "STATE = None\n\n\ndef set_state():\n    global STATE\n    STATE = 1\n",
                encoding="utf-8")
            (d / "__init__.py").write_text(init_src, encoding="utf-8")
            cases.append((name, base / name, want))
        failed = 0
        for name, tool_dir, want in cases:
            ok, detail = c21(Ctx(name, tool_dir))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-21 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail))

        # C-23：标量/容器被 global 重绑 → 报；就地改容器 → 放行
        c23_cases = (
            ("pos_scalar", "STATE = None\n\n\ndef f():\n    global STATE\n    STATE = 1\n", False),
            ("pos_container_rebind", "STATE = {}\n\n\ndef f():\n    global STATE\n    STATE = {\"a\": 1}\n", False),
            ("neg_inplace", "STATE = {}\n\n\ndef f():\n    STATE[\"a\"] = 1\n", True),
        )
        for name, body, want in c23_cases:
            d = base / ("c23_" + name) / "src" / "modules" / "demo"
            d.mkdir(parents=True)
            (d / "demo.py").write_text(body, encoding="utf-8")
            (d / "__init__.py").write_text("from .demo import f\n", encoding="utf-8")
            ok, detail = c23(Ctx(name, base / ("c23_" + name)))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-23 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail))

        # C-24：菜单读容器却不在签名里 → 报；进了签名 → 放行；无菜单 → 放行
        menu_pos = ("import pystray\nCFG = {}\n\n\ndef _menu_signature():\n    return (1,)\n\n\n"
                    "def build():\n    return pystray.MenuItem('x', None, enabled=lambda i: CFG.get('a'))\n")
        menu_neg = menu_pos.replace("return (1,)", "return (CFG.get('a'),)")
        c24_cases = (("pos_missing", menu_pos, False), ("neg_covered", menu_neg, True),
                     ("neg_no_menu", "CFG = {}\n", True))
        for name, body, want in c24_cases:
            d = base / ("c24_" + name) / "src"
            d.mkdir(parents=True)
            (d / "main.py").write_text(body, encoding="utf-8")
            ok, detail = c24(Ctx(name, base / ("c24_" + name)))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-24 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail))

        # C-10：判据要能区分"覆盖了"与"绕过了"——四种形态各一个样本
        c10_head = "import sys\nif '--smoke' in sys.argv:\n    pass\n\n\n"
        c10_cases = (
            ("pos_probe_guarded",
             "def smoke():\n"
             "    if not tray_kit.mutex_name_is_valid(APP_ID):\n"
             "        raise RuntimeError('bad mutex name')\n"
             "    return 0\n", True),
            ("neg_no_guard",
             "def smoke():\n    return 0\n", False),
            ("neg_real_guard_modalfree",
             "def smoke():\n    if not tray_kit.acquire_single_instance(APP_ID):\n"
             "        return 1\n", False),
            ("neg_probe_unchecked",
             "def smoke():\n    tray_kit.mutex_name_is_valid(APP_ID)\n    return 0\n", False),
            # 子串判据会**误收**这一条（名字只出现在注释里）；AST 不会。这就是升级判据的理由。
            ("neg_comment_only",
             "def smoke():\n    # TODO: should call mutex_name_is_valid(APP_ID) here\n"
             "    return 0\n", False),
        )
        for name, body, want in c10_cases:
            d = base / ("c10_" + name) / "src"
            d.mkdir(parents=True)
            (d / "main.py").write_text(c10_head + body, encoding="utf-8")
            ok, detail = c10(Ctx(name, base / ("c10_" + name)))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-10 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail))

        # C-22：字节卫生——三种损坏各一条样本（都会让**某一行**静默失效），合规的必须放行
        c22_cases = (
            ("pos_tab", b"@echo off\r\necho a\tb\r\n", False),
            ("pos_lf_only", b"@echo off\necho ok\n", False),
            ("pos_nonascii", b"@echo off\r\nrem \xd6\xd0\xce\xc4\r\n", False),
            ("pos_mixed_tab_lf", b"@echo off\nset x=1\r\n\tbad\n", False),
            ("neg_clean", b"@echo off\r\necho ok\r\nif errorlevel 1 exit /b 1\r\n", True),
        )
        for name, blob, want in c22_cases:
            d = base / ("c22_" + name)
            d.mkdir(parents=True)
            (d / "build.bat").write_bytes(blob)
            ok, detail = c22(Ctx(name, d))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-22 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail))

        print("[selftest] " + ("ALL PASS" if not failed else "%d FAILED" % failed))
        return 1 if failed else 0
    finally:
        shutil.rmtree(base, ignore_errors=True)


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
    ap.add_argument("--selftest", action="store_true",
                    help="用合成样本反向自证 C-21（状态副本检测器）后退出")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

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
