# -*- coding: utf-8 -*-
# TEMPLATE-MODULE: conformance_check | TEMPLATE-VER: 1.8.0
# 1.8.0：新增 **C-30**：测试里对 **mkdtemp 根目录**的清理必须可验证——禁 `ignore_errors` 吞掉。
#   根因（实测）：四工具在 %TEMP% 积了 **133~138 个**自家前缀目录，每个里恰好一个文件
#   `<app>/log/<app>.log`——**`log_kit` 的 FileHandler 句柄还开着**（Windows 拒删在用文件），
#   而 `rmtree(..., ignore_errors=True)` 把失败静默吞掉 → 每跑一次泄漏一个，**门禁全绿**。
#   **判据刻意收窄**防误伤 best-effort 清理：只报"**mkdtemp 根目录**"被 ignore_errors 删；
#   删子目录 / 固定路径 / 用有返回值的助手一律放行。四条样本，含 `neg_ignore_errors_on_scratch_subdir`。
#   **首跑真实树即发现自身**一处**漏报**并修掉：reme 写的是 `root = Path(tempfile.mkdtemp(...))`，
#   只认裸调用会让最该检查的文件报"本条不适用"——现在按"赋值右侧含 mkdtemp"判定（l-s2t 的
#   `scratch_dir(...)` 包装形态也一并认了，根目录计数由 4→9）。真实树现值：四工具 0 FAIL。
# 1.7.2：C-11 补收 **`.Path` + 目录精确比较**这一族（不带 `-Name` 的写法，如
#   `Get-Process | Where-Object {$_.Path -eq ...}`）——它比 `tasklist | findstr` 的**子串匹配
#   更强**（无子串歧义，直接比"运行实例所在目录 == 本次构建目标"），此前会掉进"认不出形态"
#   的 WARN 里，等于**对着更强的实现报"判不了"**。样本按 lead 点名的名字对齐：
#   `pos_ps_getprocess` / `pos_tasklist_findstr` / `neg_no_detection`(WARN)，
#   另加 `pos_ps_path_compare`、`neg_substring_only`(FAIL)、`neg_no_c_literal`(WARN)。
# 1.7.1：设计纪律 ④ 升级——**"不认识形态" ≠ "检出违规"**（lead 裁定，本轮最强的一条判据要求）。
#   ① C-10 的两处兜底（既无探针也无守卫调用节点 / 有 --smoke 但无 `def smoke`）改报 **WARN**：
#     判据看不出"绕过"（那取决于 `--smoke` 与守卫在 main() 里的先后），只能说"不认识这个形态"。
#   ② C-11 拆成三档：`tasklist|findstr` 取得出字面量且对得上 → ok；**对不上 → FAIL（确证）**；
#     看得到 `tasklist|findstr` 但取不出 `/c:"字面量"` → **WARN（形态不认识）**。
#   ③ 保留 FAIL 的两处（C-10 的 AST 真跑守卫节点、C-11 的错误字面量）**其余措辞改成"确证"**，
#     让消息与检出物一致（纪律 ④a）。
#   ④ C-11 补三条样本：`pos_tasklist_findstr`（此前**正中靶心的分支反而没有样本**）、
#     `neg_substring_only`（带版本号字面量 = D1-02 真实违规 ⇒ FAIL）、`neg_no_c_literal`（⇒ WARN）。
#     C-10 的两条 WARN 样本也补上 sev 断言（原先只断言 ok，severity 变了没人知道）。
# 1.7.0：新增 **C-29**：交给模板件的日志函数必须接受可变参数（print 形态）。
#   根因是 `update_helper`（7 处多参调用）与 `log_kit` 1.0.2（单参闭包）**说不同的话**，
#   而 dsh/ocx/l-s2t 各写了一份互不相同的本地 log 包装把冲突分别盖住/藏住。
#   首跑真实树即报出 **l-s2t**（`src/main.py:80 def log(message)` + 231/998/1043 三处
#   `log=log`），并附实测证据：模板件 L257/L390 的两个位置参数直接 TypeError。
#   三条样本：varargs_log_ok / single_arg_wired_flagged / single_arg_unused_ok。
#   同时 **log_kit 1.0.3 把 log 统一为 print 形态**（这是判据能成立的前提）。
# 1.6.0：① **修 C-11 假红灯**（dsh/ocx）：它们用 PowerShell `Get-Process -Name <APPNAME>`
#   做运行检测，旧实现只认 `tasklist | findstr` → 报"未找到运行检测"（一句与事实相反的诊断）。
#   现在两种形态都认；**两者都没有时按 WARN 报**——框架支持检查按分支返回级别（3 元组）。
# 1.5.0：① **修 C-10 假红灯**（reme）："结果被消费"≠"必须写成 if"——探针**作为参数交给
#   check() 助手**也算消费；兜底分支改按 **AST 调用节点**找真跑守卫（原来对函数体做文本匹配，
#   把注释里的 single_instance_free() 当成了真调用 → 打印与事实相反的诊断）。新增两条样本：
#   pos_probe_passed_to_check_helper / pos_guard_name_in_comment_only。
#   ② 新增 **C-28（WARN）**：本仓 `.md` 不得含 0x09 TAB（lead 裁定：不扩到所有文本文件，
#   只挑手写中文文档这一类，误报成本低）。
# 1.4.0：新增三条「当天缺陷没有现役条款能拦」的机械判据（各带正负样本）：
#   C-25 门禁步骤必须**既存在又能被执行**（reme build.bat:201 被 TAB 写坏 ⇒ 该步从未执行）
#   C-26 `start` 前必须存在性守卫——外部程序"成功"不能只靠排除失败码（robocopy rc=0 ≠ 成功）
#   C-27 模块采纳 = 拷贝 + 接线（README `<!-- MUST-WIRE: sym -->` 声明的符号须在**工具代码**里被引用）
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
  ④ **"不认识形态"与"检出违规"必须分开**（2026-09-19 由 lead 升级，合并原有两条口径）：
     (a) 判据的"不通过消息"**必须与它实际检出的东西一致**——检不出就说检不出，不许拿不相干
         的模式去解释失败（C-10 曾把"消费形态不认识"说成"真跑守卫"，误导出错误修法）；
     (b) 遇到**判据自己不认识的形态**时，一律 **WARN + "形态不认识，需人工确认"**，并在消息里
         写明"期望什么形态 / 实际看到什么"。**不认识 ≠ 违规**；**FAIL 只能用在确实检出违规
         证据的时候**（AST 调用节点、行号 + 实际值这类）。
     * 为什么升级：同一元缺陷一天内出现**三次**——C-10 的 `check()` 形态、C-10 的正则读注释、
       C-11 的 PowerShell 形态；每次都是"判据只认自己那一款，别款一律报违规"。误判一次，
       人就再也不信这个工具（纪律 ①）。
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
# 真跑守卫：命中即说明冒烟可能弹模态框把构建挂死（**只在探针缺失时**拿来作提示）。
_GUARD_NAMES = {"acquire_single_instance", "single_instance_free", "warn_duplicate_instance"}


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


def _calls(fn, names) -> bool:
    """AST 级：函数体里是否存在对 `names` 之一**真正的调用节点**（注释/字符串不算）。"""
    return any(isinstance(n, ast.Call) and _callee_name(n) in names for n in ast.walk(fn))


def _guarded_probe_calls(fn) -> tuple:
    """在函数体里找**结果被消费**的探针调用，返回 (已消费数, 只调未判数)。

    **判据是"返回值有没有被用"，不是"必须写成 `if`"**（2026-09-19 修，reme 假红灯）：
      * **裸表达式语句** `mutex_name_is_valid(...)` → 值被丢弃 → `plain`（覆盖 ≠ 调用）；
      * **其余一切**都算已消费 → `guarded`：条件里、`assert`、布尔组合、**作为参数交给
        `check()`/断言助手**（reme 的形态）、赋给变量……。

    旧判据只认 `if`/`while`/`assert` 的 test，于是 reme
    `check("single-instance name valid", mutex_name_is_valid(...))` 落在两种之间 →
    `guarded=0, plain=0` → **假红灯**。这正是"假红灯比漏报更伤信任"那一条。
    """
    dropped = {id(n.value) for n in ast.walk(fn)
               if isinstance(n, ast.Expr) and _callee_name(n.value) in _PROBE_NAMES}
    guarded = plain = 0
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and _callee_name(n) in _PROBE_NAMES:
            if id(n) in dropped:
                plain += 1
            else:
                guarded += 1
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
        return False, ("**判不了（形态不认识）**：入口里有 `--smoke`，但没有名为 `smoke` 的函数可查"
                       "——本判据要求冒烟逻辑落在具名函数里，才判得了'覆盖'与'绕过'。"
                       "这**可能**是形态不认识（冒烟代码写在别处），而非没有覆盖。"
                       "期望形态：`def smoke(): ...`；实际看到：入口文件里没有该函数定义。"), "WARN"
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
    # 只能按 **AST 调用节点**判定守卫——**绝不能对函数体做文本匹配**：守卫名出现在
    # 注释里（如"别用它 single_instance_free()"这种说明）会把诊断带偏，报出一句与事实
    # 相反的话（reme 2026-09-19 实例：它既有注释又有正确的探针，却被报成"真跑守卫"）。
    hit = sorted({n for fn in smokes for n in _GUARD_NAMES if _calls(fn, {n})})
    if hit:
        return False, ("**确证**（AST 直接调用节点，不是文本猜测）：smoke() 里调用了 %s —— 真跑守卫。"
                       "用户常驻实例在跑时会弹模态重复启动框，把构建挂死。"
                       "改用探针 tray_kit.mutex_name_is_valid()" % "/".join(hit))
    # 既没检出探针、也没检出真跑守卫 —— 这是**未检出**，不是**确证违规**（设计纪律 ④）。
    # 判据只认识"已知形态"；工具完全可能把覆盖包在别的助手函数里。所以报 WARN 并写明
    # 期望形态与实际所见，把判断交回人——**不认识 ≠ 违规**。
    return False, ("**判不了（形态不认识）**：smoke() 里既没有探针 `mutex_name_is_valid(...)` 的"
                   "调用节点，也没有真跑守卫的调用节点。**若你确实绕过了守卫，那才是 SINGLE-04/"
                   "D3.1 违规**——但本判据看不出'绕过'（那取决于 `--smoke` 与守卫在 main() 里的"
                   "先后），所以只报 WARN，请人工确认。期望形态：`if not "
                   "tray_kit.mutex_name_is_valid(APP_ID): raise RuntimeError(...)`；"
                   "实际看到：smoke() 里没有任何已知守卫符号的调用节点。"), "WARN"


@check("C-11", "FAIL", "运行检测匹配串能命中当前 exe 名（SINGLE-05/D1-02）")
def c11(c: Ctx):
    """三种形态，**认不出时只报 WARN**（2026-09-19 修假红灯，与 C-10 同类）。

    dsh/ocx 用 **PowerShell `Get-Process -Name <APPNAME>`** 做运行检测，旧实现只认
    `tasklist | findstr`，于是对它们报"未找到运行检测"——**假红灯 + 误导诊断**（人家明明有）。
    现在：① `tasklist | findstr /c:"..."`；② `Get-Process ... -Name <名>`；③ 两者都没有 ⇒
    **WARN**（判不了就不硬判，见设计纪律 ①）。
    """
    text = c.build_blob
    if not text:
        return True, "无 build.bat"
    appname = re.search(r'set\s+APPNAME=(\S+)', text)
    app = appname.group(1) if appname else c.app_id
    exe = app + ".exe"
    saw_tasklist_without_literal = False
    for line in text.splitlines():
        if "tasklist" in line and "findstr" in line:
            mm = re.search(r'/c:"([^"]+)"', line)
            if mm:
                probe = mm.group(1).replace("%APPNAME%", app)
                if probe and probe in exe:
                    return True, "tasklist 匹配串 %r 能命中 %s" % (probe, exe)
                return False, ("**确证**：`%s` 的匹配串 %r 与当前 exe 名 %s 对照不上——只有旧版"
                               "带版本号的 exe 会被命中，当前实例在跑也拦不住构建"
                               % (line.strip()[:70], probe, exe))
            saw_tasklist_without_literal = True
        if "Get-Process" in line:
            mm = re.search(r"-Name\s+'?\"?([\w.%\[\]]+)", line)
            if mm:
                probe = mm.group(1).replace("%APPNAME%", app)
                if probe and probe in exe:
                    return True, "PowerShell 匹配名 %r 能命中 %s" % (probe, exe)
                return False, ("**确证**：PowerShell 匹配名 %r 与当前 exe 名 %s 对照不上"
                               % (probe, exe))
        # **`.Path` + 目录精确比较**这一族（dsh/ocx 的形态）：它比 `tasklist | findstr`
        # 的**子串匹配更强**——没有子串歧义，且直接比"运行实例所在目录是不是本次构建目标"。
        # 不带 `-Name` 时（如 `Get-Process | Where-Object {$_.Path -eq ...}`）此前会掉进
        # "认不出形态"的 WARN 里，那是对着更强的实现报"判不了"。认得就明确放行。
        if "Get-Process" in line and ".Path" in line:
            return True, ("PowerShell `Get-Process` 取 `.Path` 做**目录精确比较**（SINGLE-05 的"
                          "强化形态：无子串歧义）")
    if saw_tasklist_without_literal:
        return False, ("**判不了（形态不认识）**：看到 `tasklist | findstr`，但取不出 `/c:\"...\"` "
                       "字面量来与 exe 名对照——它可能用别的方式写匹配串。期望形态："
                       "`tasklist ... | findstr /i /c:\"%APPNAME%.exe\"`；"
                       "实际看到：该行没有 `/c:\"...\"`。"), "WARN"
    # 判不了就不硬判（设计纪律 ①④）：认不出形态 ⇒ **WARN**，并给出补形态的指引。
    return False, ("**判不了（形态不认识）**：既无 `tasklist | findstr` 也无 `Get-Process`，"
                   "本判据不认识该工具的运行检测形态——**不认识 ≠ 违规**，请人工确认。"
                   "若该工具确有自有实现，请把它的形态补进本检查"), "WARN"


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


# ---------------------------------------------------------------- C-25..C-27
# 三条都来自 2026-09-19 当天暴露的缺陷，**现役 76 条款一条都拦不住**：
#   C-25 门禁步骤"可执行 + 可被执行"   （reme build.bat:201 被 TAB 写坏 ⇒ 该步从未执行）
#   C-26 外部程序"成功"必须含正向要求   （robocopy rc=0 = 没复制也没出错 ⇒ 空 STAGE 被判成功）
#   C-27 采纳 = 拷贝 + 接线             （dsh/ocx 拷了 update_helper，README 承诺的调用零引用）
_PATHISH = re.compile(r"[A-Za-z0-9_%~.\\/-]+\.(?:py|bat|cmd)\b")


def _bat_invocations(path: Path):
    """返回 [(行号, 相对路径)]：bat 里**以脚本文件为参数**的调用（注释行不算）。

    只认不含 `%` 的路径字面量——带变量的（例如以 `%RELEASE_DIR%` 开头的）解析不了，不硬判。
    """
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        s = line.strip()
        if not s or s.lower().startswith(("rem ", "rem\t", "::")):
            continue
        for tok in _PATHISH.findall(s):
            if "%" in tok or "~" in tok or tok.startswith(("-", "/", "\\")):
                continue
            # 只认**看起来是路径**的（带分隔符）：`dsh.cmd` / `appconfig.py` 这类裸文件名
            # 是当参数或当命令用的，是否存在由 PATH/调用方决定，不硬判（首版实测的误报）。
            if "\\" not in tok and "/" not in tok:
                continue
            out.append((i, tok.strip('"\'')))
    return out


@check("C-25", "FAIL", "门禁步骤必须既存在又能被执行（D1-05/J 坑）")
def c25(c: Ctx):
    """两步都要过：**(a) 被调用的路径在磁盘存在**；**(b) 该步不在死代码里**。

    反面教材（2026-09-19）：`reme/scripts/build.bat:201` 被写成
    `"%PY%" tests<TAB>est_update_bat.py` —— 转义把文件名撕开，**整行测试门禁从未执行过**；
    又因 D1-01 排在它前面，即使不修也永远不暴露。**"写了"不等于"跑了"**。
    """
    files = [p for p in _bat_files(c.dir)
             if p.name.lower() in ("build.bat", "release.bat", "run.bat", "clean.bat")]
    if not files:
        return True, "无 build/release bat"
    missing, dead = [], []
    for p in files:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        # 死代码判定：**顶层无条件**的 `exit /b` / `goto :eof` 之后、下一个标签之前的调用。
        # ⚠️ 括号块内（`if errorlevel 1 ( ... exit /b 1 )`）与 `if ... exit /b` 都是**条件**出口，
        # 成功路径根本不走——把它们当无条件会把每个工具的正常门禁全误报成"死代码"（首版实测）。
        terminated, depth = False, 0
        for i, line in enumerate(lines, 1):
            s = line.strip()
            if s.startswith(":"):
                terminated = False
            elif depth == 0 and not s.lower().startswith("if ") \
                    and re.match(r"^(exit\s+/b|goto\s+:eof)", s, re.I):
                terminated = True
            elif terminated and s and not s.lower().startswith(("rem", "::", ")")):
                for tok in _PATHISH.findall(s):
                    if "%" not in tok:
                        dead.append("%s:%d %s（前有顶层 exit/goto :eof，永不执行）"
                                    % (p.relative_to(c.dir).as_posix(), i, tok))
            depth = max(0, depth + s.count("(") - s.count(")"))
        for lineno, rel in _bat_invocations(p):
            if Path(rel).is_absolute():
                continue
            # 家族约定：模板库与工具**同级**，跨仓引用（`..\my-diy-tool-template\x.py`）
            # 要按"工具的父目录"再找一遍——首版只找工具内，把正常的 sync 门禁误报成缺失。
            cands = [p.parent / rel, c.dir / rel, c.dir.parent / rel]
            if not any(x.exists() for x in cands):
                missing.append("%s:%d %s" % (p.relative_to(c.dir).as_posix(), lineno, rel))
    bad = missing + dead
    return (not bad), ("；".join(bad[:6]) if bad
                       else "%d 个 bat 的步骤调用都在磁盘上且不在死代码里" % len(files))


_START_WITH_PATH = re.compile(r'^\s*start\s+"[^"]*"\s+"(?P<path>[^"]+)"', re.I | re.M)


@check("C-26", "FAIL", "start 前必须存在性守卫：外部程序的\"成功\"不能只靠排除失败码（J 坑）")
def c26(c: Ctx):
    """`robocopy` 的 `rc=0` 意为**没有任何文件被复制、也没出错**——所以"只排除 >=8"会把
    **空/损坏的暂存包判成成功**，随后 `start` 指向不存在的 exe ⇒ Windows"找不到文件"
    **模态框**（`DETACHED_PROCESS` 挡不住，GUI 子系统）⇒ 脚本永久阻塞。

    判据：每一条 `start "" "<路径>"` 都必须有存在性守卫——同行 `if exist "<路径>"`
    或更早的 `if not exist "<路径>" goto …`。**负向排除 ≠ 成功，必须额外校验目标产物存在。**

    ⚠️ **同时扫 `.py`**：更新链的 bat 是**渲染生成**的，模板本体是 Python 里的字符串
    （模板 `update_helper._APPLY_BAT`、l-s2t `updater.py` 的 apply 模板）——只扫 `.bat`
    等于把真正的现场漏掉（首版实测：四个工具全报"无 start 调用"）。
    """
    bad, checked = [], 0
    sources = list(_bat_files(c.dir)) + [p for p in c.py_files()]
    for p in sources:
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in _START_WITH_PATH.finditer(text):
            target = m.group("path")
            if "%" in target:
                continue
            checked += 1
            lineno = text[:m.start()].count("\n") + 1
            line = text.splitlines()[lineno - 1]
            earlier = "\n".join(text.splitlines()[:lineno - 1])
            inline = re.search(r'if\s+exist\s+"%s"' % re.escape(target), line, re.I)
            before = re.search(r'if\s+not\s+exist\s+"%s"' % re.escape(target), earlier, re.I)
            if not (inline or before):
                bad.append("%s:%d start 指向 %s，但**没有任何存在性守卫**"
                           % (p.relative_to(c.dir).as_posix(), lineno, target))
    return (not bad), ("；".join(bad) if bad
                       else "%d 处 start 都有存在性守卫" % checked if checked
                       else "无 start 调用")


_MUST_WIRE = re.compile(r"<!--\s*MUST-WIRE:\s*([A-Za-z_][A-Za-z0-9_]*)\s*-->")


@check("C-27", "FAIL", "模块采纳 = 拷贝 + 接线：README 声明的必接符号须在代码里被引用（B4/D14）")
def c27(c: Ctx):
    """**`sync_check` 的模块 `[ok]` 只证明"拷全了"，不证明"接上了"**。

    反面教材（2026-09-19）：dsh/ocx 把 `update_helper` 三件拷到位（哈希全绿），但
    `sweep_stale_update_dirs` / `pop_failed_update_note` 在 `src/` 下**只出现在被拷进去的
    README 里，代码零引用** —— README 承诺的两件事一件都没发生（失败通知永不触发、%TEMP%
    残留越积越多），而所有机械检查都是绿的。**SAME ≠ 在役。**

    机制：模块 README 用 `<!-- MUST-WIRE: symbol -->` 声明"启动/退出时必须调用"的入口；
    检查器在**工具代码**（`src/**/*.py`，排除 `src/modules/**` 的拷贝本体与 `__init__.py`
    的转发导出）里找引用；找不到即报。
    """
    mods = c.src / "modules"
    if not mods.is_dir():
        return True, "无 src/modules/"
    code = [p for p in c.py_files()
            if "modules" not in p.relative_to(c.src).parts[:1]
            and p.name != "__init__.py"]
    bad, declared = [], 0
    for d in sorted(x for x in mods.iterdir() if x.is_dir()):
        # 声明取**模板正本**（`TEMPLATE_DIR/modules/<m>/README.md`）优先：要求是模块的属性，
        # 不该等工具把带锚点的 README 拷过去之后才生效——否则锚点加上当天所有工具都"无声明"，
        # 检查空转（首版实测）。工具侧 README 也读，兼容工具自己追加的声明。
        readmes = [p for p in (TEMPLATE_DIR / "modules" / d.name / "README.md",
                               d / "README.md") if p.exists()]
        syms = sorted({s for r in readmes for s in _MUST_WIRE.findall(c.read(r))})
        for sym in syms:
            declared += 1
            if not any(re.search(r"\b%s\b" % re.escape(sym), c.read(p)) for p in code):
                bad.append("%s 声明必接 %s，但工具代码里零引用" % (d.name, sym))
    if not declared:
        return True, "无 MUST-WIRE 声明"
    return (not bad), ("；".join(bad) if bad else "%d 个必接符号都已接线" % declared)


@check("C-28", "WARN", "本仓 .md 不得出现 0x09 TAB（手写文档，出现 TAB 必属事故）")
def c28(c: Ctx):
    """**只扫 `.md`，WARN 级**——误报成本低，但能覆盖一类真实事故。

    背景：写 CHANGELOG 时用 Python 字符串拼内容，`"\\t"` 被当成**转义**，于是文件里落进一个
    **真 TAB**（2026-09-19 本人实例）。bat 有 C-22 管，`.py` 的 TAB 是缩进（合法）、`.json`
    里也可能是合法转义——所以**只挑 `.md`**：本仓的 `.md` 全是手写中文文档，TAB 没有任何
    正当用途。lead 裁定：不扩到所有文本文件，但这一条值得有。
    """
    bad = []
    for p in sorted(c.dir.rglob("*.md")):
        if any(part in _BAT_SKIP_DIRS for part in p.parts):
            continue
        data = p.read_bytes()
        if b"\x09" not in data:
            continue
        lines = [i for i, ln in enumerate(data.split(b"\n"), 1) if b"\x09" in ln]
        bad.append("%s: TAB 行 %d 处（第 %s 行）"
                   % (p.relative_to(c.dir).as_posix(), len(lines),
                      ",".join(str(n) for n in lines[:5])))
    return (not bad), ("；".join(bad) if bad else "手写文档无 TAB")


# ---------------------------------------------------------------- C-29
_LOG_DEF = re.compile(r"^[ \t]*def\s+(log|_log)\s*\(([^)]*)\)", re.M)
_LOG_WIRED = re.compile(r"\blog\s*=\s*([A-Za-z_]\w*)")


@check("C-29", "FAIL", "交给模板件的日志函数必须接受可变参数（print 形态）")
def c29(c: Ctx):
    """**"替身比真实实现更宽容"会盖住契约冲突**——本条是它的机械落地。

    根因（2026-09-19 定）：`update_helper` 全文 7 处按 print 形态调用
    （`log("downloading", stem)`、`log("update staged:", staged, "->", target, "(bat %s)" % s)`），
    而 `log_kit.make_logger` 1.0.2 给的是**单参闭包** `log(message)`。

    **为什么一直没炸**：dsh / ocx 各自在工具侧写了 `def log(*parts)` 把它兜住（两处都留了
    "模板 log_kit 待统一"的注释），l-s2t 写了单参包装却照样 `log=log` 传给
    `tray_kit` / `update_helper` —— **冲突被三份互不相同的本地包装分别盖住或藏住**，
    模板层面于是长期保持"两个派发件说不同的话"。

    判据：工具代码里出现 `log=<name>`（把函数交给模板件），而该 `<name>` 在**工具代码内**
    的定义是单参、没有 `*args`/`*parts` → 报，并点名定义处与第一处传参点。

    **✅ 合规正例（写在最前，防后人误伤）**：**工具侧自建 `def log(*parts)` 包装是正确做法，
    不是要消灭的偏差**——dsh `src/main.py:120` 与 ocx `src/main.py:80`（`def _log(*parts)`）
    就是这么写的，C-29 对它们判 `[ok]`（首跑只报 l-s2t 是对的）。判据说要消灭的是
    **"只收一个参数"**的包装，不是"自己写包装"这件事本身。
    `✶` 为什么要把这句写进判据说明：**判据的措辞会塑造后人的行为**——若这里只写"传给模板件的
    log 必须收可变参数"，读者很容易把它读成"凡自建包装皆偏差"，从而去"统一"掉 dsh/ocx 那种
    **本来就正确**的写法。样本 `pos_tool_side_vararg_wrapper` 专门钉住这一形态。

    不做的事（避免假红灯）：`log=` 后面的名字**不是工具内的函数定义**时**不下判**——
    例如 reme 的 `log=HELPER_UPDATE_LOG` 是**日志文件路径**（交给 bat 模板的），
    不是日志函数；拿它开火就是一句与事实相反的诊断（本文件的设计纪律 ④）。
    """
    code = [p for p in c.py_files()
            if "modules" not in p.relative_to(c.src).parts[:1] and p.name != "__init__.py"]
    if not code:
        return True, "无工具代码"
    wired = {}
    for p in code:
        rel = p.relative_to(c.dir).as_posix()
        for i, line in enumerate(c.read(p).splitlines(), 1):
            for m in _LOG_WIRED.finditer(line):
                wired.setdefault(m.group(1), []).append("%s:%d" % (rel, i))
    if not wired:
        return True, "没有把日志函数交给模板件（log= 零命中）"
    defs = {}
    for p in code:
        text = c.read(p)
        for m in _LOG_DEF.finditer(text):
            name = m.group(1)
            if name in wired and name not in defs:
                defs[name] = (p.relative_to(c.dir).as_posix(),
                              text[:m.start()].count("\n") + 1, m.group(2).strip())
    if not defs:
        return True, ("log= 命中的 %d 处都不是工具内的函数定义（如日志路径常量），本条判不了"
                      % sum(len(v) for v in wired.values()))
    bad = []
    for name, (rel, lineno, params) in sorted(defs.items()):
        if "*" in params:
            continue
        bad.append("%s:%d `def %s(%s)` 只收一个参数，却由 %s 交给模板件——"
                   "模板件按 print 形态调用时（如 `log(\"downloading\", stem)`）直接 TypeError"
                   % (rel, lineno, name, params, wired[name][0]))
    if bad:
        return False, "；".join(bad)
    return True, "%d 个交给模板件的日志函数都是 print 形态（%s）" % (
        len(defs), ", ".join(sorted(defs)))


# ---------------------------------------------------------------- C-30
_RMTREE_CALL = re.compile(r"(?:shutil\.)?rmtree\s*\(\s*([A-Za-z_]\w*)")
_ASSIGN_LINE = re.compile(r"^\s*([A-Za-z_]\w*)\s*=")
_DEF_HEAD = re.compile(r"^\s*def\s+([A-Za-z_]\w*)\s*\([^)]*\)\s*:", re.M)


def _mkdtemp_producers(texts) -> set:
    """哪些**函数名**会产生 mkdtemp 根目录：`mkdtemp` 本身 + 工具自己的包装。

    l-s2t 的测试写的是 `_TMP = scratch_dir("l-s2t-startup-")`，而 `scratch_dir` 是
    `tests/_cleanup.py` 里包了 `mkdtemp` 的助手。只认 `mkdtemp` 字面量会**漏掉真实形态**
    （判据会对着真正泄漏的地方报绿灯），所以把"函数体里出现 `mkdtemp(`"的本地函数也算生产者。
    """
    producers = {"mkdtemp"}
    for text in texts:
        for m in _DEF_HEAD.finditer(text):
            if "mkdtemp(" in text[m.end():m.end() + 800]:
                producers.add(m.group(1))
    return producers


def _mkdtemp_roots(text, producers) -> set:
    """本文件里哪些**变量**是 mkdtemp 根目录。

    必须按"赋值语句右侧含不含 mkdtemp"判定，而不是只认 `X = mkdtemp(...)` 这一种写法：
    reme 的测试是 `root = Path(tempfile.mkdtemp(prefix="reme-update-bat-"))`——
    外面套了 `Path(...)`。**只认裸调用会让最需要检查的文件报"本条不适用"**
    （2026-09-19 真实树首跑实测：reme 就是这样被漏掉的）。
    """
    lines = text.splitlines()
    roots = set()
    for i, line in enumerate(lines):
        m = _ASSIGN_LINE.match(line)
        if not m:
            continue
        # 右侧可能续行：把本行 + 后两行拼起来看
        rhs = " ".join(lines[i:i + 3])
        if "mkdtemp(" in rhs or any(p + "(" in rhs for p in producers if p != "mkdtemp"):
            roots.add(m.group(1))
    return roots


@check("C-30", "FAIL", "测试里对 mkdtemp 根目录的清理必须可验证（禁 ignore_errors 吞掉）")
def c30(c: Ctx):
    """**"删不掉"必须变成红，而不是被 `ignore_errors=True` 吞掉**（2026-09-19 实测）。

    背景：四个工具在 `%TEMP%` 积了 **133~138 个**自家前缀目录，每个里面**恰好一个文件**
    `<app>/log/<app>.log`。根因不是窗口 cwd，而是 **`log_kit` 的 FileHandler 句柄还开着**
    （Windows 拒绝删除在用文件），而 `rmtree(..., ignore_errors=True)` 把失败**静默吞掉** →
    每跑一次泄漏一个目录，**而所有门禁照旧全绿**。

    **判据刻意收窄**（避免误伤真正的 best-effort 清理——那是本条最容易做错的地方）：
      * 只盯**由 `mkdtemp` 产生的根目录**（含工具自己的包装函数，如 `scratch_dir`）；
      * 只有那个**根目录**被 `rmtree(..., ignore_errors=True)` 删时才报；
      * 删**子目录**、删固定路径、用 `_rmtree_retry` 之类**有返回值**的助手 → **不报**。

    正确形态：删前释放日志句柄（`logging.shutdown()` / 关 FileHandler）→ 删 → **回读确认不存在**
    → 不存在才算成功，失败即红。本条只否掉"吞掉失败"这一种写法，不规定必须用哪个助手。

    **本条不猜命名**（STANDARDS §D7 硬要求 8）：mkdtemp 根目录是**从源码枚举**出来的
    （赋值语句右侧是否调用 `mkdtemp(`，含 `Path(...)` / `scratch_dir(...)` 等包装形态），
    **不做 `prefix="xxx"` 的字符串匹配**——前缀怎么改、新增几个，判据自动跟着变。
    """
    tests = c.dir / "tests"
    if not tests.is_dir():
        return True, "无 tests/"
    files = [p for p in sorted(tests.rglob("*.py")) if "__pycache__" not in p.parts]
    if not files:
        return True, "tests/ 下无 .py"
    texts = [c.read(p) for p in files]
    producers = _mkdtemp_producers(texts)
    roots_total, bad = 0, []
    for p, text in zip(files, texts):
        roots = _mkdtemp_roots(text, producers)
        roots_total += len(roots)
        if not roots:
            continue
        rel = p.relative_to(c.dir).as_posix()
        for m in _RMTREE_CALL.finditer(text):
            if m.group(1) not in roots:
                continue
            # ignore_errors 可能写在续行上——看调用点之后 160 字符，而不是只看同一行
            if "ignore_errors" not in text[m.end():m.end() + 160]:
                continue
            bad.append("%s:%d `rmtree(%s, ignore_errors=True)` —— %s 是 mkdtemp 根目录"
                       % (rel, text[:m.start()].count("\n") + 1, m.group(1), m.group(1)))
    if bad:
        return False, ("；".join(bad) + "。【正确形态】删前释放日志句柄（logging.shutdown()）、"
                       "删后**回读确认目录已不存在**，失败即红")
    if not roots_total:
        return True, "测试里没有 mkdtemp 根目录（本条不适用）"
    return True, "%d 个 mkdtemp 根目录都用可验证的清理（无 ignore_errors）" % roots_total


def selftest() -> int:
    """C-21..C-29 反向自证：合成样本，正例须点名，反例须放行。"""
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
            # 未检出（不是确证违规）⇒ WARN
            ("neg_no_guard",
             "def smoke():\n    return 0\n", False, "WARN"),
            ("neg_real_guard_modalfree",
             "def smoke():\n    if not tray_kit.acquire_single_instance(APP_ID):\n"
             "        return 1\n", False),
            ("neg_probe_unchecked",
             "def smoke():\n    tray_kit.mutex_name_is_valid(APP_ID)\n    return 0\n", False),
            # 子串判据会**误收**这一条（名字只出现在注释里）；AST 不会。这就是升级判据的理由。
            ("neg_comment_only",
             "def smoke():\n    # TODO: should call mutex_name_is_valid(APP_ID) here\n"
             "    return 0\n", False, "WARN"),
            # reme 的真实形态：探针**作为参数交给 check() 助手**——值被消费了，必须放行。
            # 旧判据只认 if/while/assert 的 test，这里 guarded=0/plain=0 → 假红灯。
            ("pos_probe_passed_to_check_helper",
             "def smoke():\n"
             "    check('single-instance name valid',\n"
             "          mutex_name_is_valid(APP_ID, mutex_name=SINGLE_INSTANCE_NAME))\n", True),
            # 守卫名**只出现在注释里** + 有正确探针 → 必须放行（reme 那条假红灯的根因）
            ("pos_guard_name_in_comment_only",
             "def smoke():\n"
             "    # 不许用 single_instance_free()：用户实例在跑时它为真\n"
             "    check('ok', mutex_name_is_valid(APP_ID))\n", True),
            # 真跑守卫（AST 调用节点）才 FAIL
            ("neg_real_guard_ast",
             "def smoke():\n    tray_kit.acquire_single_instance(APP_ID)\n", False),
        )
        for case in c10_cases:
            name, body, want = case[:3]
            want_sev = case[3] if len(case) > 3 else None
            d = base / ("c10_" + name) / "src"
            d.mkdir(parents=True)
            (d / "main.py").write_text(c10_head + body, encoding="utf-8")
            res = c10(Ctx(name, base / ("c10_" + name)))
            ok, detail = res[0], res[1]
            sev = res[2] if len(res) == 3 else "FAIL"
            # 设计纪律 ④：**未检出 ≠ 确证违规**。这两种形态（既无探针也无守卫调用节点）
            # 必须是 **WARN**——判据说不出"绕过了"，只能说"不认识这个形态"。
            good = (ok == want) and (want_sev is None or sev == want_sev)
            failed += 0 if good else 1
            print("[selftest] %s  C-10 %s: ok=%s want=%s sev=%s want_sev=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, sev, want_sev, detail[:80]))

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

        # C-25：路径不存在 → 报；顶层 exit 之后的调用（死代码）→ 报；合规 → 放行
        def _mk_tool(name, bat, extra=()):
            d = base / name
            (d / "tests").mkdir(parents=True, exist_ok=True)
            for rel in extra:
                (d / rel).write_text("x = 1\n", encoding="utf-8")
            (d / "build.bat").write_bytes(bat)
            return d

        c25_cases = (
            ("pos_missing_path", b'@echo off\r\n"%PY%" tests\\gone.py\r\n', (), False),
            ("pos_dead_code", b'@echo off\r\n"%PY%" tests\\t.py\r\nexit /b 1\r\n"%PY%" tests\\t.py\r\n',
             ("tests/t.py",), False),
            ("neg_conditional_exit", b'@echo off\r\nif errorlevel 1 (\r\n  exit /b 1\r\n)\r\n'
                                     b'"%PY%" tests\\t.py\r\n', ("tests/t.py",), True),
        )
        for name, blob, extra, want in c25_cases:
            ok, detail = c25(Ctx(name, _mk_tool("c25_" + name, blob, extra)))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-25 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:90]))

        # C-26：无守卫 start → 报；同行 if exist → 放行；前置 if not exist → 放行
        c26_cases = (
            ("pos_unguarded", b'@echo off\r\nstart "" "C:\\t\\a.exe"\r\n', False),
            ("neg_inline_guard", b'@echo off\r\nif exist "C:\\t\\a.exe" start "" "C:\\t\\a.exe"\r\n', True),
            ("neg_prior_guard", b'@echo off\r\nif not exist "C:\\t\\a.exe" goto dead\r\n'
                                b'start "" "C:\\t\\a.exe"\r\n:dead\r\n', True),
        )
        for name, blob, want in c26_cases:
            ok, detail = c26(Ctx(name, _mk_tool("c26_" + name, blob)))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-26 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:90]))

        # C-27：README 的 MUST-WIRE 符号在工具代码里查引用
        for name, main_src, want in (("pos_unwired", "x = 1\n", False),
                                     ("neg_wired", "def f():\n    sweep_stale()\n", True)):
            d = base / ("c27_" + name) / "src" / "modules" / "demo"
            d.mkdir(parents=True)
            (d / "README.md").write_text("<!-- MUST-WIRE: sweep_stale -->\n", encoding="utf-8")
            (base / ("c27_" + name) / "src" / "main.py").write_text(main_src, encoding="utf-8")
            ok, detail = c27(Ctx(name, base / ("c27_" + name)))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-27 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:90]))

        # C-28：.md 里的真 TAB 必须被点名（这是本人踩过的形态）。
        # ⚠️ 用**显式字节值**构造，不写 b"...TAB..."——写下这段样本时，正是 `TAB` 被当转义
        # 解释、把真 TAB 落进了源文件（本 J 坑同一天第三次出现，且出现在"检测 TAB"的检查里）。
        _tab, _crlf = bytes([9]), bytes([13, 10])
        d = base / "c28_pos"
        d.mkdir(parents=True)
        (d / "CHANGELOG.md").write_bytes(b"# x" + _crlf + b"line" + _tab + b"with tab" + _crlf)
        ok, detail = c28(Ctx("c28_pos", d))
        good = ok is False
        failed += 0 if good else 1
        print("[selftest] %s  C-28 pos_md_tab: ok=%s want=False | %s"
              % ("PASS" if good else "FAIL", ok, detail[:70]))
        d = base / "c28_neg"
        d.mkdir(parents=True)
        (d / "CHANGELOG.md").write_bytes(b"# x" + _crlf + b"clean line" + _crlf)
        ok, detail = c28(Ctx("c28_neg", d))
        good = ok is True
        failed += 0 if good else 1
        print("[selftest] %s  C-28 neg_clean_md: ok=%s want=True | %s"
              % ("PASS" if good else "FAIL", ok, detail[:70]))

        # C-11：认形状（tasklist / PowerShell 两种），认不出只 WARN。
        # 用显式字节值构造样本（CRLF 转义在多个 heredoc 里被解释成真字节——本日第 4 次）。

        _crlf = bytes([13, 10])
        _e = base / "c11_none"
        _e.mkdir(parents=True)
        (_e / "build.bat").write_bytes(b"@echo off" + _crlf + b"set APPNAME=my-helper" + _crlf)
        ok, detail, sev = c11(Ctx("c11_none", _e))
        good = (ok is False and sev == "WARN")
        failed += 0 if good else 1
        print("[selftest] %s  C-11 neg_no_detection: ok=%s sev=%s | %s"
              % ("PASS" if good else "FAIL", ok, sev, detail[:60]))
        _p = base / "c11_ps"
        _p.mkdir(parents=True)
        (_p / "build.bat").write_bytes(
            b"@echo off" + _crlf + b"set APPNAME=my-helper" + _crlf
            + b"powershell -NoProfile -Command \"(Get-Process -Name %APPNAME%"
            + b" -ErrorAction SilentlyContinue).Path\"" + _crlf)
        ok, detail = c11(Ctx("c11_ps", _p))
        good = ok is True
        failed += 0 if good else 1
        print("[selftest] %s  C-11 pos_ps_getprocess: ok=%s | %s"
              % ("PASS" if good else "FAIL", ok, detail[:70]))

        # C-11 补齐三条（2026-09-19 lead 点名）：此前**只有** PowerShell 形态与"认不出"两条样本，
        # `tasklist | findstr` 这条**正中靶心**的分支反而没有任何样本兜着——判据改了没人知道。
        _c11 = (
            # ① tasklist 形态的**合规**样本（l-s2t build.bat:86 的真实写法）
            ("pos_tasklist_findstr", b"tasklist /fo csv 2>nul | findstr /i /c:\"%APPNAME%.exe\" >nul",
             True, None),
            # ② **确证违规**：匹配串写成**带版本号**的字面量——只有旧版 exe 会被命中，
            #    当前（无版本号）实例在跑也拦不住构建（D1-02 的真实形态）⇒ FAIL
            ("neg_substring_only", b"tasklist | findstr /i /c:\"%APPNAME%-1.0.exe\"", False, "FAIL"),
            # ③ 看到 tasklist|findstr 但取不出 `/c:"字面量"` ⇒ **形态不认识**，不是违规 ⇒ WARN
            ("neg_no_c_literal", b"tasklist /fo csv | findstr /i \"%APPNAME%\"", False, "WARN"),
            # ④ `.Path` + 目录精确比较（**不带 `-Name`** 的那一族）：比子串匹配更强，
            #    必须放行而不是掉进"认不出形态"的 WARN（对着更强的实现报"判不了"）
            ("pos_ps_path_compare",
             b"powershell -NoProfile -Command \"(Get-Process | Where-Object "
             b"{$_.Path -eq '%CD%\\release\\x\\my-helper.exe'}).Count\"", True, None),
        )
        for name, cmdline, want, want_sev in _c11:
            _d = base / ("c11_" + name)
            _d.mkdir(parents=True)
            (_d / "build.bat").write_bytes(
                b"@echo off" + _crlf + b"set APPNAME=my-helper" + _crlf + cmdline + _crlf)
            res = c11(Ctx(name, _d))
            ok, detail = res[0], res[1]
            sev = res[2] if len(res) == 3 else "FAIL"
            good = (ok == want) and (want_sev is None or sev == want_sev)
            failed += 0 if good else 1
            print("[selftest] %s  C-11 %s: ok=%s want=%s sev=%s want_sev=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, sev, want_sev, detail[:80]))

        # C-29：交给模板件的 log 必须是 print 形态。
        # 命名按"该不该报"写清楚：本文件的样本命名在两代检查里刚好相反
        # （C-25/26 的 pos = 该报、C-11 的 pos = 合规），所以这里不用 pos/neg，
        # 直接用 `_ok` / `_flagged` / `_unused` 三个词，读的人不必猜。
        c29_cases = (
            ("varargs_log_ok",
             "def log(*parts):\n    pass\n\n\nupdate_helper.download_and_prepare(log=log)\n", True),
            # dsh `main.py:120` / ocx `main.py:80` 的**真实形态**：工具侧自建包装，把
            # 任意个位置参数拼成一行再转交 log_kit。**这是正解，不是偏差**——判据的措辞
            # 若让人以为"自建包装"该被消灭，这份样本就是挡它的那道闸。
            ("pos_tool_side_vararg_wrapper",
             "from modules import log_kit\n\n"
             "_LOG_HANDLE = log_kit.make_logger(LOG_DIR)\n\n\n"
             "def log(*parts):\n"
             '    """模板件的日志契约是 print 形态（log("a", b)），这里按契约收参再拼接。"""\n'
             '    _LOG_HANDLE[0](" ".join(str(p) for p in parts))\n'
             "\n\n"
             "def check_update_menu(_icon=None, _item=None):\n"
             "    update_helper.download_and_prepare(latest, APP_DIR, UPDATE_DIR, log=log)\n", True),
            ("single_arg_wired_flagged",
             "def log(message):\n    pass\n\n\ntray_kit.acquire_single_instance(log=log)\n", False),
            ("single_arg_unused_ok",
             "def log(message):\n    pass\n\n\nx = 1\n", True),
        )
        for name, main_src, want in c29_cases:
            d = base / ("c29_" + name) / "src"
            d.mkdir(parents=True)
            (d / "main.py").write_text(main_src, encoding="utf-8")
            ok, detail = c29(Ctx(name, base / ("c29_" + name)))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-29 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:100]))

        # C-30：只有"mkdtemp 根目录被 ignore_errors 吞掉"才报；子目录/固定路径要放行。
        # 命名按该不该报写清楚（与 C-29 同一约定），不靠 pos/neg 猜。
        _cleanup_ok = ("import shutil, logging, tempfile\n"
                       "TMP = tempfile.mkdtemp(prefix='t-')\n"
                       "logging.shutdown()\n"
                       "shutil.rmtree(TMP)\n"
                       "assert not TMP.exists()\n")
        _cleanup_bad = ("import shutil, tempfile\n"
                        "TMP = tempfile.mkdtemp(prefix='t-')\n"
                        "shutil.rmtree(TMP, ignore_errors=True)\n")
        # 包装函数（l-s2t 真实形态）：scratch_dir 内部调 mkdtemp
        _cleanup_wrapper = ("import shutil, tempfile\n"
                            "def scratch_dir(prefix):\n"
                            "    return tempfile.mkdtemp(prefix=prefix)\n"
                            "TMP = scratch_dir('t-')\n"
                            "shutil.rmtree(TMP, ignore_errors=True)\n")
        # 非 mkdtemp 根：目录是 mkdir 出来的，删它吞错不算泄漏
        _cleanup_subdir = ("import shutil, tempfile\n"
                           "TMP = tempfile.mkdtemp(prefix='t-')\n"
                           "sub = TMP / 'sub'\n"
                           "shutil.rmtree(sub, ignore_errors=True)\n"
                           "shutil.rmtree(TMP)\n")
        c30_cases = (
            ("verified_cleanup_ok", _cleanup_ok, True),
            ("ignore_errors_on_mkdtemp_root_flagged", _cleanup_bad, False),
            ("ignore_errors_through_wrapper_flagged", _cleanup_wrapper, False),
            ("ignore_errors_on_scratch_subdir_ok", _cleanup_subdir, True),
        )
        for name, body, want in c30_cases:
            d = base / ("c30_" + name) / "tests"
            d.mkdir(parents=True)
            (d / "test_x.py").write_text(body, encoding="utf-8")
            ok, detail = c30(Ctx(name, base / ("c30_" + name)))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-30 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:100]))

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
            res = fn(c)
            # 允许检查**按分支**返回级别：`(ok, detail, "WARN")`——"判不了"不该按 FAIL 算
            # （设计纪律 ①：判不了的宁可 WARN；C-11 的"认不出形态"就是这一档）。
            if isinstance(res, tuple) and len(res) == 3:
                ok, detail, severity = res
            else:
                ok, detail = res
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
