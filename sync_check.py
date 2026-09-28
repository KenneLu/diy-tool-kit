# TEMPLATE-MODULE: sync_check | TEMPLATE-VER: 2.0.2
# 2.0.2（W5 前段）：E 组补两条 1.5.0 marker 腿（F14-①②）：giveup 段写 FAILED marker /
#   install_dead 段写 marker 且 KEPT 按实况。段切片用**行级标签锚**（^:label$）——
#   裸 split 会被 bat 注释里的字面 ':giveup is unreachable' 劫持（W5 实测：正确模板恒红）。
# 2.0.1（W1 收尾步）：四仓已全部迁到 src/template/ 并换新头——**拆除 2.0.0 的全部过渡垫片**
#   （_norm_rel 归一、src/modules 布局兜底、头部 modules/ 前缀容忍），布局与头部只认 template/。
# 2.0.0（W1 改名，执行文档-20260927，D8）：模板仓 modules/ → template/；双布局过渡（垫片已在 2.0.1 拆除）。
# 1.9.0（#57，与 ls2t-dev 往复产出）：**三处静默出口分成三档可观测量** + NOT-WIRED 升格为申报口。
#   原先 `scan_tool` 有三处 `continue` 都表示"当作这个文件没有出处"，而"没有出处"正是
#   **工具自有文件**的正确观测量 ⇒ "头被覆盖/模块名写错/目标不存在"这类**缺陷输入**与
#   合法输入落在**同一个**可观测量上 —— 那不是漏判，是**无判据**（喂进已知缺陷输入，
#   没有任何可观测量会变）。判准用可执行问法，不用循环问法（"兜底能否只在输入正确时生效"
#   对"兜底自身供给目标"的装置是循环的）。
#   现在：无头（工具自有，另有两腿兜底） / **申报了但解析不出 = [BAD-HDR]（红灯）** / 解析得出。
#   新增四条腿，各有反向单元 + 控制单元：
#     ① [BAD-HDR]      申报的出处不可解析 ⇒ 红灯（实测四家 0 命中）
#     ② [NO-HDR-COPY]  无头但归一化内容等于模板件 ⇒ 拷贝被剥了头，红灯（实测 0 命中；
#                      "缺头⇒报"靠这条**可量化**：工具自有件不匹配任何模板件，天然不刷屏，
#                      而剥掉任一头立刻变红）
#     ③ [NO-HDR]       `src/modules/**` 下无任何出处头 ⇒ 黄灯（该命名空间里"无头"是歧义；
#                      实测仅 reme `src/modules/__init__.py` 一件）
#     ④ NOT-WIRED.md   模块目录下有此件 = **有意未接入**的申报 ⇒ 该模块缺失项记 [decl]
#                      而不进 missing-module/file（原先 sync_check 完全不认这份已在野外
#                      使用的申报件，"申报了"与"没人注意"是同一个可观测量）
#   退出码口径不变：仍只有 drift/missing（+ 新增 BAD-HDR / NO-HDR-COPY）阻断。
# 1.8.4：E 组补 **`budget_s` 必须与实参 `limit` 同源**——`update_helper.py` 的 docstring 早就写明“判据落点在 sync_check --selftest 的 update_helper 组”，而这里**此前没有这条腿** ⇒ **承诺的判据不存在，等于没判据**。三条腿：limit=2 ⇒ `budget 2s`；limit=120 ⇒ `budget 120s`（两个输入两个输出）；**反向格 = 真变异**（把源码改回取模块常量，重新加载后 limit=2 **必须不再**出 `budget 2s`）。
# T10 · 模板漂移检查（防漂移四件套之二，执行文档 D1）。
#
# 1.8.2：E 组补第二条可达路径——**回铺源为空**（SNAPSHOT 没内容）+ 替换失败：真跑一场
#   （故障注入把 STAGE→TARGET 换成 goto install_failed），断言 0.4s 退出 / 落 :install_dead
#   （日志 RESTORE FAILED）/ 不启动任何 exe / marker + 现场保留；另加静态要点
#   "回铺后 start 前也验 exe"。**两次踩同一个坑**：正文里是 cmd 变量不是展开路径。
# 1.8.1：E 组跟随 update_helper 1.4.1——空暂存包如今**保留现场**（`:cleanup_keep`），
#   真跑断言从"暂存已删"翻成"暂存还在"，并加静态要点"stage_invalid 走 cleanup_keep"。
# 1.8.0：`--selftest` E 组新增**真跑反例**（`_apply_bat_runtime_cases`）：把生成的 apply.bat
#   放进 %TEMP% 沙箱、以**空暂存包**执行，断言"秒级退出（模态框会挂死）/ 写 update.failed
#   marker / **安装目录没被动过**（/purge 没跑）/ 暂存被收尾删除 / 脚本自删"。
#   为什么必须真跑：文本断言只能证明"守卫写在那儿"，证明不了"那条路真的被拦住"——而
#   失效形态恰恰是**带 GUI 子系统的模态框**（DETACHED_PROCESS 挡不住），表现为永久挂起。
#   安全性：沙箱内目标目录**没有 exe**，即使误走 start 分支也不会拉起任何进程。
# 1.7.0：`--selftest` 新增 **F 组：tray_kit 探针语义**（`mutex_name_is_valid`，2.1.0/D3.3）。
#   探针要被 `--smoke` 用来覆盖"名字合法"，必须同时满足：非法名判 False、**名字被占用仍判
#   True**（否则用户实例在跑时冒烟假红）、**探测后不留句柄**（否则探针自己占锁）、内核不可用
#   时放行。四条各对应一次真实踩坑，故逐条钉住而不是只测"返回 bool"。仅 sync_check 自身变更，
#   **不产生任何级联**。
# 1.6.0：E 组再扩 5 条——照 reme 基准文档 §9-1/§9-2 落地后要能**反向自证**：
#   模块里没有 `global` 重绑、`UPDATE_READY`/`PENDING_CMD` 不是模块全局、
#   就地改容器即刻对外可见、**`import *` 不搬运派生名**（旧缺陷无法静默复现）、
#   以及 bat 的两处新守卫（空暂存包前置拦截 / start 前存在性检查）。
## 1.5.0：`--selftest` 新增 **E 组：update_helper 1.3.0 替换脚本语义回归**。1.3.0 按用户仲裁
#   规则照 reme 已验证链路补齐"失败回退"（快照先于替换、rc>=8 不启动新 exe、回铺、失败
#   marker），这些语义**只存在于生成的 .bat 文本里**，py 层测不到；E 组对脚本生成器做
#   正向断言 + 对"旧合成形态"做**反向断言**（证明断言不是空转）。仅 sync_check 自身变更，
#   **不产生任何级联**。
#
# 1.4.0：扫描范围从 `*.py` 扩到**模块文件夹内全部比对件（.py + .md）**——"整文件夹采纳"
#   按定义是 **README + __init__.py + 代码** 三件套，而模块 README 此前从未被比对
#   （CONFORMANCE §4.1.10 第 4 盲区）。模板专属目录 baseline/ build_release/ 排除
#   （它们不是 src/modules/ 的拷贝源），__pycache__ 等生成目录排除（避免 .pyc 刷屏）。
#   仅 sync_check 自身变更，**不产生任何级联**。
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
#           工具侧没有（例：模板新增 `icons/__init__.py` 或模块 `README.md` 而工具未拷）
#           —— 黄灯（复核员实测漏检）。
#   [DIFF]  非代码件（.md）与正本**逐字节不一致** —— 黄灯（§4.1.10a）。
#           口径：模块 README 与正本**逐字节一致、不带任何 TEMPLATE 头**——头机制是为
#           代码副本设计的（剔掉 TEMPLATE-* 行再比哈希），而 markdown 标题也以 `#` 开头，
#           沿用会静默吞掉 `# TEMPLATE-FROM:`，使"带头/不带头"都判相等。故 .md：
#           要么逐字节相同（[ok]），要么 [DIFF]；**不产生 [NOHDR]**，也不参与头/VER 判定。
#           例外：若同模块的任一 .py 已申报 TEMPLATE-LOCAL-OVERRIDE（整模块有意分叉，
#           如 reme 的重形态 i18n），其 README 差异记 [decl]（已申报），不记 [DIFF]。
#           [NOHDR] 仅保留给 .py —— 那里 TEMPLATE 头是必需品；文档不需要也不应有头。
#
# 用法：
#   python my-diy-tool-template/sync_check.py                    # 检查 my_diy_tools 下所有工具
#   python my-diy-tool-template/sync_check.py --roots dsh-helper opencodex-helper

import argparse
import hashlib
import re
import shutil
import sys
import tempfile
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
# 旧头部路径 → 新布局的别名（副本未跟上布局时兜底）
LEGACY_ALIAS = {
    "update_helper.py": "template/update_helper/update_helper.py",
    "appconfig.py": "template/appconfig/appconfig.py",
    "paths.py": "template/paths/paths.py",
    "autostart.py": "template/autostart/autostart.py",
    "i18n.py": "template/i18n/i18n.py",
    "icons.py": "template/icons/icons.py",
    "tray_kit.py": "template/tray_kit/tray_kit.py",
    "log_kit.py": "template/log_kit/log_kit.py",
}

# 模板仓目录名（W1 改名后为 template/）
TPL_DIR_NAME = "template"


def repo_identity(path) -> str:
    """`repo=<name> rev=<short sha> dirty=<yes|no>` —— **被检仓库**的修订与脏净。

    只印 checker 自身身份，看不出"这条结论建立在哪个修订、是否建立在**未提交**改动上"
    （lead 2026-09-19，采用 ls2t-dev 的形态）。取不到 git 就印 `?`：非 git 目录 / 无 git /
    超时都不许让判据崩。两个 checker（本件与 conformance_check）都打这一行。
    """
    import subprocess as _sp
    path = Path(path)
    rev, dirty = "?", "?"
    try:
        r = _sp.run(["git", "-C", str(path), "rev-parse", "--short", "HEAD"],
                    capture_output=True, text=True, timeout=5)
        if r.returncode == 0 and r.stdout.strip():
            rev = r.stdout.strip()
            s = _sp.run(["git", "-C", str(path), "status", "--porcelain"],
                        capture_output=True, text=True, timeout=5)
            if s.returncode == 0:
                dirty = "yes" if s.stdout.strip() else "no"
    except Exception:
        pass
    return f"rev={rev} dirty={dirty}"


def identity_line() -> str:
    """checker 自身身份：`# sync_check <VER> sha256:<raw> norm:<norm>`（运行时自算）。

    写死的哈希会自己过期——那正是它要解决的问题；两种口径都给（`.py` 比对用 norm、
    `.md` 用逐字节，见 ALIGNMENT §0），只印一种迟早被人拿另一种去对。
    """
    import hashlib
    import re as _re
    raw = Path(__file__).read_bytes()
    text = raw.decode("utf-8", "replace")
    norm = "\n".join(ln for ln in text.splitlines()
                     if not _re.match(r"^\s*#\s*TEMPLATE-", ln))
    m = _re.search(r"TEMPLATE-VER:\s*([\d.]+)", text[:2000])
    return ("# sync_check %s  sha256:%s  norm:%s"
            % (m.group(1) if m else "?", hashlib.sha256(raw).hexdigest()[:12],
               hashlib.sha256(norm.encode("utf-8")).hexdigest()[:12]))


def _rmtree_strict(path, tries: int = 10, delay: float = 0.2) -> bool:
    """删目录并**回读确认**；删不掉 → 打印 `[FAIL]` 并返回 False（绝不静默吞）。

    为什么模板仓的工具也要守 C-30：`ignore_errors=True` 会把"删不掉"（Windows 上句柄
    未释放是常态）翻译成"看起来删掉了"，每跑一次泄漏一个 `%TEMP%` 目录而门禁全绿。
    调用方**必须消费返回值**（"我加了重试 ≠ 失败可见"）。
    """
    import time
    p = Path(path)
    for _ in range(max(1, tries)):
        shutil.rmtree(p, ignore_errors=True)
        if not p.exists():
            return True
        time.sleep(delay)
    print("[FAIL] temp dir not removed (leak): %s" % p)
    return False


def sha256_text(text: str) -> str:
    """代码副本用：剔除 `# TEMPLATE-*` 元信息行后归一化哈希。"""
    norm = "\n".join(line for line in text.splitlines() if not META_LINE.match(line))
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


def sha256_bytes(path: Path) -> str:
    """非代码件（.md）用：**逐字节哈希、不剔任何行**。

    剔行归一化是为**代码副本**设计的（去掉出处声明行再比）。markdown 标题也以 `#`
    开头，若沿用剔行，`# TEMPLATE-FROM:` 会被静默吞掉 —— "带头的 README"与"不带头的
    README"会比对成相等（CONFORMANCE §4.1.10a）。故 .md 必须逐字节比。
    """
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return ""


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


TEMPLATE_FILE_SUFFIXES = {".py", ".md"}   # "整文件夹采纳" = README + __init__.py + 代码（1.4.0）
# 模板专属目录：只服务模板仓库自身，不作为 src/modules/ 的拷贝源（否则造成 4×N 假 MISSING）
TEMPLATE_ONLY_MODULES = {"baseline", "build_release"}
SCAN_SKIP_DIRS = {"__pycache__", ".git", "build", "out", "dist", ".mypy_cache", ".pytest_cache"}


def is_scan_target(path: Path) -> bool:
    """只比对 .py / .md，且跳过 __pycache__ 等生成目录（复核员第一版漏排 .pyc 刷屏）。"""
    return (path.suffix.lower() in TEMPLATE_FILE_SUFFIXES
            and not (set(path.parts) & SCAN_SKIP_DIRS))


def _script_form_cases():
    """脚本形态采纳的真值表（四例）。**没有样本的分支等于没有判据**。"""
    P = Path("src/icons.py")
    cases = [
        ("脚本形态：被消费 + 无包目录 + 有具体文件 → True",
         is_script_form_adoption("icons", {"icons"}, {"icons": [P]}, False), True),
        ("有 src/modules/icons/ 目录 → False（那是包形态，缺件就是缺口）",
         is_script_form_adoption("icons", {"icons"}, {"icons": [P]}, True), False),
        ("没有任何文件消费它 → False（交给 [MISSING-MODULE]）",
         is_script_form_adoption("icons", set(), {}, False), False),
        ("消费记录为空 → False（说不出'就地'在哪，就不下结论）",
         is_script_form_adoption("icons", {"icons"}, {"icons": []}, False), False),
    ]
    return [(label, got == want, f"got={got} want={want}")
            for label, got, want in cases]


def is_script_form_adoption(mod, consumed, consumed_files, has_mod_dir) -> bool:
    """该模块是否以**脚本形态就地采纳**（不是导入包）。

    判据（三条同时成立，**不猜命名**）：
      ① 模块被采纳（`mod in consumed`——头部通道有文件申报来自它）；
      ② 工具侧**没有** `src/modules/<mod>/` 目录（`has_mod_dir` 为假）；
      ③ 有**具体的工具侧文件**消费了它（`consumed_files` 非空，用于输出"就地"路径）。

    为什么需要这条：`icons` 在 dsh/ocx/l-s2t 都是 `src/icons.py` + `python src\\icons.py`
    的**构建期脚本**用法，三家的 `[MISSING-FILE]`（缺 `__init__.py` / `README.md`）
    完全相同。实测把它改成包形态会炸 `ModuleNotFoundError: No module named 'modules'`
    ——`from modules.appconfig import ...` 依赖文件所在深度。所以"缺 `__init__.py`"
    不是缺口，是**另一种采纳形态**；判据必须能说出这一点，而不是把它算成漏拷。
    """
    return bool(mod in consumed and not has_mod_dir and consumed_files.get(mod))


def iter_tool_py(tool_dir: Path):
    """工具侧参与头解析的 .py（跳过 __pycache__ 等生成目录）。"""
    return sorted(p for p in tool_dir.rglob("*.py")
                  if p.is_file() and not (set(p.parts) & SCAN_SKIP_DIRS))


def scan_tool(tool_dir: Path):
    """头部通道：返回 `(found, anomalies)`。

    found     = [(tool_file, template_rel, declared, tool_ver)]
    anomalies = [(tool_file, kind, detail)] —— **申报了出处却解析不出来**的件。

    **为什么把"解析不出来"单列**（2026-09-19，由 ls2t-dev 的往复产出，#57）：
    本函数原先有三处静默 `continue`，语义都是"当作这个文件没有出处"；而"没有出处"正是
    **工具自有文件**的正确观测量 ⇒ 缺陷输入（头被覆盖 / 模块名写错 / 目标不存在）与合法
    输入**落在同一个可观测量上**——那不是"漏判"，是**无判据**（拿已知缺陷输入喂进去，
    没有任何一个可观测量会变）。现在分成三档，各占一个**不同**的可观测量：
      ① 无任何出处头          → "工具自有"（由 `no_header_legs` 的两条腿兜底）；
      ② 申报了出处但解析不出  → `[BAD-HDR]`（阻断，本条）；
      ③ 解析得出              → 照常比对。
    判准用的是可执行问法"**拿一个已知缺陷输入喂进去，有没有任何一个可观测量会变？**"
    而不是循环问法"这条兜底能不能只在输入正确时生效"（对"兜底自身供给目标"的装置是循环的）。

    **只收 .py**：头部机制是为**代码副本**设计的（剔掉出处行再比哈希）。模块 README
    按口径不带任何 TEMPLATE 头、与正本逐字节一致（CONFORMANCE §4.1.10a），因此 .md
    一律走布局通道，绝不在这里被头解析。
    """
    found, anomalies = [], []
    for py in iter_tool_py(tool_dir):
        head = read_text(py)[:4096]
        match = FROM_RE.search(head)
        if match:
            rel = match.group(1)
        else:
            mmod = MODULE_RE.search(head)
            if not mmod:
                continue          # ① 合法：无出处头 = 工具自有件
            mod = mmod.group(1)
            # `TEMPLATE-MODULE: <模块>` 只标模块，不标文件名：__init__.py 必须映射到
            # 模板的同名 __init__.py（1.3.0 起模板 __init__.py 也带此头，否则会拿
            # __init__.py 去比 <模块>.py，产生假 DRIFT）。
            if py.name == "__init__.py":
                rel = f"{TPL_DIR_NAME}/{mod}/__init__.py"
                if not (TEMPLATE_DIR / rel).exists():
                    anomalies.append((py, "BAD-HDR",
                                      f"TEMPLATE-MODULE: {mod} 推导出 {rel}，模板中不存在"))
                    continue
            else:
                rel = f"{TPL_DIR_NAME}/{mod}/{mod}.py"
            if not (TEMPLATE_DIR / rel).exists():
                # 布局兜底：模块文件夹下唯一 py 时按唯一者解析；不唯一则**出声**（原先静默跳过）
                mod_dir = TEMPLATE_DIR / TPL_DIR_NAME / mod
                cands = sorted(mod_dir.rglob("*.py")) if mod_dir.is_dir() else []
                if len(cands) != 1:
                    anomalies.append((py, "BAD-HDR",
                                      f"TEMPLATE-MODULE: {mod} → {rel} 不存在，"
                                      f"且 {TPL_DIR_NAME}/{mod}/ 下候选 {len(cands)} 个（兜底不唯一）"))
                    continue
                rel = cands[0].relative_to(TEMPLATE_DIR).as_posix()
        ver = VER_RE.search(head)
        found.append((py, rel, bool(OVERRIDE_RE.search(head)),
                      ver.group(1) if ver else ""))
    return found, anomalies


def template_norm_index() -> dict:
    """模板 .py 的**归一化哈希 → [相对路径]**（`sha256_text` 口径，与副本比对同一把尺子）。"""
    out = {}
    for p in sorted(TEMPLATE_DIR.rglob("*.py")):
        if p.is_file() and not (set(p.parts) & SCAN_SKIP_DIRS):
            out.setdefault(sha256_text(read_text(p)), []).append(
                p.relative_to(TEMPLATE_DIR).as_posix())
    return out


def declared_not_wired(mod_dir: Path) -> str:
    """模块级"有意未接入"申报口：模块目录下的 `NOT-WIRED.md`（存在即有申报）。

    **为什么要有这个出口**（#57）：`NOT-WIRED.md` 是**已在野外使用的申报件**
    （reme `src/modules/service_link/` 就有一份），而 sync_check 原先完全不认它——
    于是"申报了"与"没人注意"在输出上是**同一个可观测量**（都表现为缺口）。
    升格后：缺失项记 `[decl]`（带申报件名）而不进 missing-module/file 计数。
    """
    return "NOT-WIRED.md" if (mod_dir / "NOT-WIRED.md").is_file() else ""


def no_header_legs(tool_dir: Path):
    """"缺头 ⇒ 报"的两条腿。返回 `(copies, ns_files)`。

    **腿① `copies`（阻断）**：**无出处头、但归一化内容等于某个模板件**的 .py
    ⇒ 这是一份**被剥掉头的拷贝**。之所以这条能兑现"缺头 ⇒ 报"而不刷屏：工具自有件
    （main.py / tests / scripts）**不匹配任何模板件**，天然落在判据之外；只有"本该带头
    的拷贝"会命中。实测（2026-09-19，四家）命中 **0** ——于是这条腿**今天零噪声**，
    而**剥掉任一头立刻变红**（拿已知缺陷输入喂进去，可观测量必须变）。

    **腿② `ns_files`（黄灯）**：`src/modules/**` 下**无任何出处头**的 .py——
    这是模板拷贝的命名空间，"无头"在这里是**歧义**的（工具自有 marker？漏头的拷贝？），
    必须看得见。实测当前只有 reme `src/modules/__init__.py` 一件（模板无此件，属工具自有）。
    """
    idx = template_norm_index()
    copies, ns_files = [], []
    for py in iter_tool_py(tool_dir):
        head = read_text(py)[:4096]
        if FROM_RE.search(head) or MODULE_RE.search(head) or OVERRIDE_RE.search(head):
            continue
        rel_to_tool = py.relative_to(tool_dir).as_posix()
        if rel_to_tool.startswith("src/template/"):
            ns_files.append(py)
        hit = idx.get(sha256_text(read_text(py)))
        if hit:
            copies.append((py, hit))
    return copies, ns_files


def template_modules() -> dict:
    """模板 `modules/<模块>/` → [该模块的全部比对件]（.py + .md，1.4.0 起）。

    "整文件夹采纳" = **README + `__init__.py` + 代码**；只扫 .py 会让模块 README
    完全隐身（CONFORMANCE §4.1.10 第 4 盲区）。模板专属目录（baseline/build_release）
    不是拷贝源，排除；__pycache__ 等生成目录排除。
    """
    out = {}
    base = TEMPLATE_DIR / TPL_DIR_NAME
    if not base.is_dir():
        return out
    for mod_dir in sorted(base.iterdir()):
        if not mod_dir.is_dir() or mod_dir.name in TEMPLATE_ONLY_MODULES:
            continue
        files = sorted(p for p in mod_dir.rglob("*") if p.is_file() and is_scan_target(p))
        if files:
            out[mod_dir.name] = files
    return out


def compare(tool_file: Path, rel: str, is_blueprint: bool, is_declared: bool,
            tool_ver: str, has_header: bool):
    """返回 (kind, note, tool_ver, tpl_ver)。

    kind ∈ miss/ok/param/nohdr/lag/decl/drift（.py 语义）
         ∪ diff（.md：逐字节不一致 —— 黄灯，不引入 NOHDR）。
    """
    template_file = TEMPLATE_DIR / rel
    if not template_file.exists():
        return "miss", "", tool_ver, "?"
    if tool_file.suffix.lower() == ".md":
        # 非代码件：逐字节比，不做"头/VER"判定（口径见 CONFORMANCE §4.1.10a）。
        # 但**模块级** OVERRIDE 例外：整个模块是有意分叉时（如 reme 重形态 i18n），
        # 其 README 不可能与正本一致，应记 [decl] 而非 [DIFF]——差异已申报，不是漂移。
        if sha256_bytes(tool_file) == sha256_bytes(template_file):
            return "ok", "", "", "?"
        if is_declared:
            # is_declared 此处是**申报来源文件名**（字符串），带到输出里让"有意分叉"一眼可辨
            return "decl", f" (declared via {is_declared})", "", "?"
        return "diff", "", "", "?"
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
        return "decl", note + " (declared override)", tool_ver, tpl_ver
    return "drift", note, tool_ver, tpl_ver


BLUEPRINTS = load_blueprints()


def _i18n_state_cases():
    """D 组：模板 `modules/i18n` 包状态回归（2.1.1）。返回 [(label, ok, detail)]。

    缺陷原型：包门面 `from .i18n import *` 把 `LANG` 拷成静态副本 → `init('en')` 后
    从**包命名空间**读仍是 'zh'，而 `t()` 已英文。断言必须**从包读**（只读子模块测不出）。
    """
    import importlib.util
    pkg_init = TEMPLATE_DIR / TPL_DIR_NAME / "i18n" / "__init__.py"
    if not pkg_init.exists():
        return [("D i18n package state", False, "模板 modules/i18n/__init__.py 不存在")]
    name = "_tpl_i18n_selftest"
    spec = importlib.util.spec_from_file_location(
        name, pkg_init, submodule_search_locations=[str(pkg_init.parent)])
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    out = []
    try:
        spec.loader.exec_module(mod)
        out.append(("D1 LANG not a static copy in package ns",
                    "LANG" not in vars(mod),
                    "package ns: " + ",".join(sorted(
                        k for k in vars(mod) if not k.startswith("__")))))
        mod.init("en")
        out.append(("D2 package ns reports en after init('en')", mod.LANG == "en", str(mod.LANG)))
        out.append(("D3 current_lang()", mod.current_lang() == "en", str(mod.current_lang())))
        out.append(("D4 t() follows", mod.t("menu_quit") == "Quit", str(mod.t("menu_quit"))))
        mod.init("zh")
        out.append(("D5 switch back immediate (package)", mod.LANG == "zh", str(mod.LANG)))
        out.append(("D6 t() follows back", mod.t("menu_quit") == "退出", str(mod.t("menu_quit"))))
    except Exception as exc:   # 导入即坏（例如改了包结构）也要报，不能静默
        out.append(("D i18n package state", False, "异常: %r" % (exc,)))
    finally:
        for k in (name, name + ".i18n"):
            sys.modules.pop(k, None)
    return out


_TOK = re.compile(r'"[^"]*"|\S+')


def _split_cmd(line):
    """把一行拆成 (命令名, 参数 token 列表)，**命令名与拼写无关**。

    归一：首 token → 剥引号 → 取最后一段路径 → 去 `.exe` → 小写。
    于是 `find` / `%SystemRoot%\\System32\\find.exe` / `FIND.EXE` 得到同一个名字；
    而 `findstr` 得到 `findstr`，**不会被当成 `find`**——旧的 `startswith("find")` 会吃掉它。

    参数 token 原样保留（含引号与 `%VAR%`），因为**顺序与变量名正是要判的东西**。
    """
    parts = line.strip().split(None, 1)
    if not parts:
        return "", []
    head = parts[0].strip('"').replace("/", "\\")
    head = head.rsplit("\\", 1)[-1]
    if head.lower().endswith(".exe"):
        head = head[:-4]
    return head.lower(), (_TOK.findall(parts[1]) if len(parts) > 1 else [])


def _apply_bat_keypoints(text, exe, target, stage, snapshot, backup, work, failed, limit):
    """检查一份更新 .bat 是否具备 reme 已验证的语义要点，返回 [(label, ok)]。

    ⚠️ 四条实测教训（各来自一次真实误判）：
      * 脚本正文里出现的是 **cmd 变量**（`%SNAPSHOT%` / `%WORK%` / `%FAILED%`），**不是**
        Python 侧展开后的路径——拿展开路径去 grep 正文必然找不到。路径值只能从
        `set "X=..."` 行解析后单独断言（"备份在 target 之外"就是这么判的）。
      * 刻意**按命令行判定**（只取非 `rem` 行），不做全文子串匹配：脚本注释里写着
        `"tasklist | find" NEVER RETURNS` 这句**反例说明**，全文 grep 会把解释文字当成真管道。
      * **判据必须锚"语义"，不锚"拼写"。** 旧实现按 `ln.startswith("find")` 分类、按
        `'robocopy "%TARGET%" "%SNAPSHOT%"'` 字面量定位，于是把命令改成绝对路径
        （`%SystemRoot%\\System32\\find.exe`，**语义完全等价、而且是修一个真缺陷**）就会
        打出 6 条**假红**。现在命令名走 `_split_cmd()` 归一、次序锚点走 `idx_cmd()` 按
        **位置参数**比——大小写与路径前缀都不参与匹配。
      * **未命中不许返回 -1。** `-1` 会流进 `>` 比较（`x > -1` 恒真）⇒ 判据空转成
        **假绿**（实测：删掉安装那一行，"检查 rc" 仍然报绿），也会流进切片
        （`cmds[-1:]` 取到最后一个元素）。现在返回 `None`，误用会立刻抛 `TypeError`。
    """
    lines = [ln.strip() for ln in text.splitlines()]
    cmds = [ln for ln in lines if ln and not ln.lower().startswith("rem")]

    def has(frag):
        return any(frag in ln for ln in cmds)

    def idx(frag):
        """按**字面量**定位（用于标签/if 行）。未命中返回 None，绝不返回 -1。"""
        for i, ln in enumerate(cmds):
            if frag in ln:
                return i
        return None

    def idx_cmd(cmd, *args):
        """按**命令名 + 位置参数**定位，不按拼写。

        参数按**位置**逐位比（忽略大小写），因为顺序本身就是要判的东西：
        `"%TARGET%" "%SNAPSHOT%"`（快照）与 `"%SNAPSHOT%" "%TARGET%"`（回铺）是两条不同的行。

        ⚠️ **已知未归一的第三条轴：变量名。** 本选择器与调用方传进来的参数字面量里含
        `"%TARGET%"` / `"%STAGE%"` / `"%SNAPSHOT%"`——**前缀与大小写已归一，变量名没有**。
        reme 的真实 bat 用的是 `%INSTALL%`（`reme-helper/src/main.py:7233` 一带），
        所以若模板哪天与 reme 的变量名收敛，这些锚点会**全部失配**。
        **失败方向是响的**（`before()` 任一侧 None 即 False ⇒ 变红，不会静默变绿），
        所以这是**登记项不是缺陷**；真到那天请**把这条轴也归一，不要放宽断言**。
        """
        for i, ln in enumerate(cmds):
            c, a = _split_cmd(ln)
            if c != cmd or len(a) < len(args):
                continue
            if all(a[j].lower() == s.lower() for j, s in enumerate(args)):
                return i
        return None

    def before(a, b):
        """a 严格在 b 之前。**任一侧未命中即 False**——次序判据必须显式依赖两侧都存在。"""
        return a is not None and b is not None and a < b

    def outside(path, tgt):
        p, t = Path(path).resolve(), Path(tgt).resolve()
        return p != t and t not in p.parents

    newexe = str(Path(target) / exe)
    vars_ = {}
    for ln in cmds:
        if ln.startswith('set "') and "=" in ln:
            k, _, v = ln[5:].partition("=")
            vars_[k.upper()] = v.rstrip('"')
    tl = [ln for ln in cmds if _split_cmd(ln)[0] == "tasklist"]
    fl = [ln for ln in cmds if _split_cmd(ln)[0] == "find"]
    snap_i = idx_cmd("robocopy", '"%TARGET%"', '"%SNAPSHOT%"')
    copy_i = idx_cmd("robocopy", '"%STAGE%"', '"%TARGET%"')
    restore_i = idx_cmd("robocopy", '"%SNAPSHOT%"', '"%TARGET%"')
    rc_i = idx("if %RC% geq 8 goto install_failed")
    rot_i = idx('move /y "%SNAPSHOT%" "%BACKUP%"')
    delbak_i = idx('rmdir /s /q "%BACKUP%"')
    dead_i = idx(":install_dead")
    keep_i = idx(":cleanup_keep")
    stage_i = idx('if not exist "%%STAGE%%\\%s" goto stage_invalid' % exe)
    guard_i = idx('if not exist "%s" goto install_failed' % newexe)
    deadguard_i = idx('if not exist "%s" goto install_dead' % newexe)
    tail = cmds[dead_i:keep_i if (keep_i is not None and dead_i is not None
                                  and keep_i > dead_i) else len(cmds)] if dead_i is not None else []
    # 1.5.0 两段级断言的切片：**行级标签锚**（`^:label$`），不能用裸 split——bat 注释里
    # 出现过字面 `:giveup is unreachable`（解释 :wait 循环的 rem 块），裸 split 会把切段
    # 锚到注释上，段内容完全错位（W5 前段实测：F14-1 腿对正确模板恒红）。
    import re as _re

    def _seg(start_label, end_label):
        m = _re.search(r"(?m)^%s\s*$" % _re.escape(start_label), text)
        if not m:
            return ""
        rest = text[m.end():]
        m2 = _re.search(r"(?m)^%s\s*$" % _re.escape(end_label), rest)
        return rest[: m2.start()] if m2 else rest
    giveup_seg = _seg(":giveup", ":cleanup")
    dead_seg = _seg(":install_dead", ":giveup")
    return [
        # 节拍必须是**不依赖网络配置**的睡眠：`ping` 在丢 loopback ICMP 的机器上一拍 9.0s
        # （实测），名义 120s 变 ~18 分钟。见 C-33 / CONFORMANCE §4.1.20。
        ("等待循环 :wait", ":wait" in text and has("Start-Sleep -Milliseconds")),
        ("tasklist 行不含管道", bool(tl) and all("|" not in ln for ln in tl)),
        ("tasklist 写文件", any(">" in ln for ln in tl)),
        ("find 读该文件", bool(fl) and all('"%POLL%"' in ln for ln in fl)),
        ("等待有上限 %d" % limit, has(f"if %tries% geq {limit} goto giveup")),
        ("超时放弃路径", ":giveup" in text),
        ("变量指向约定值", vars_.get("TARGET") == target and vars_.get("STAGE") == stage
         and vars_.get("WORK") == work and vars_.get("BACKUP") == backup
         and vars_.get("SNAPSHOT") == snapshot and vars_.get("FAILED") == failed),
        ("备份在 target 之外", outside(vars_.get("BACKUP", backup), target)),
        ("替换前先快照", before(snap_i, copy_i)),
        ("空暂存包前置拦截（不碰安装目录）", stage_i is not None and before(stage_i, snap_i)),
        ("start 前有存在性守卫（缺 exe 不弹模态框）",
         before(copy_i, guard_i)
         and 'if exist "%s" start "" "%s"' % (newexe, newexe) in text),
        ("检查 rc，失败不启动新 exe", before(copy_i, rc_i)),
        ("成功后才轮转备份（失败时旧备份还在）", before(rc_i, rot_i) and before(rc_i, delbak_i)),
        ("失败回铺快照", before(rc_i, restore_i)),
        ("回铺也失败则不启动", before(rc_i, dead_i)
         and not any(ln.startswith("start") for ln in tail)),
        ("stage_invalid 保留现场（goto cleanup_keep）",
         idx(":stage_invalid") is not None and ":cleanup_keep" in text
         and text.split(":stage_invalid")[1].split(":install_failed")[0].find("goto cleanup_keep") >= 0),
        ("回铺后 start 前也验 exe（否则回铺源为空时又是一条死路）",
         before(idx(":install_failed"), deadguard_i)),
        ("失败 marker", has('> "%FAILED%" echo')),
        # 1.5.0（W5 前段，F14-①②）：两条失败路径的 marker 可见性——日志随暂存被清扫，
        # marker（用户数据区）是应用退出后唯一幸存的报告通道；pop_failed_update_note 读它。
        ("超时放弃写失败 marker（1.5.0 F14-1：giveup 段）",
         '> "%FAILED%" echo update aborted' in giveup_seg),
        ("install_dead 写 marker 且 KEPT 按实况（1.5.0 F14-2：不指向不存在的路径）",
         '> "%FAILED%" echo update failed' in dead_seg and 'if not defined KEPT' in dead_seg),
        ("cleanup 删暂存", has('if exist "%WORK%" rmdir /s /q "%WORK%"')),
        ("脚本自删", has('del "%~f0"')),
        ("ASCII-only", text.isascii()),
    ]


def _update_helper_cases():
    """E 组：update_helper 替换脚本语义（1.3.0，照 reme 已验证链路）。返回 [(label, ok, detail)]。

    正向：模板 `build_apply_script()` 生成的脚本必须逐项具备要点；
    反向：喂一份"1.0.x 合成形态"（无等待/无快照/无 rc 检查）必须**被判缺项**——否则断言空转。
    """
    import importlib.util
    out = []
    path = TEMPLATE_DIR / TPL_DIR_NAME / "update_helper" / "update_helper.py"
    if not path.exists():
        return [("E update_helper script", False, "模板 modules/update_helper/update_helper.py 不存在")]
    spec = importlib.util.spec_from_file_location("_tpl_update_helper_selftest", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_tpl_update_helper_selftest"] = mod
    need = str(TEMPLATE_DIR)
    added = need not in sys.path
    if added:
        sys.path.insert(0, need)
    try:
        spec.loader.exec_module(mod)
        # 1.4.0：状态必须是"就地修改的容器 + 只读派生"，不得再有可被 global 重绑的标量
        import ast as _ast
        src = path.read_text(encoding="utf-8")
        tree = _ast.parse(src)
        rebound = sorted({n for node in _ast.walk(tree) if isinstance(node, _ast.Global)
                          for n in node.names})
        out.append(("E 模块里没有 global 重绑", not rebound, "global: " + ",".join(rebound)))
        out.append(("E UPDATE_READY/PENDING_CMD 不是模块全局",
                    "UPDATE_READY" not in vars(mod) and "PENDING_CMD" not in vars(mod),
                    "模块命名空间里%s该名" % ("有" if "UPDATE_READY" in vars(mod) else "没有")))
        mod._PUBLISHED["ready"] = "9.9.9"
        out.append(("E 就地改容器即刻对外可见（派生读法）",
                    mod.update_ready() == "9.9.9" and mod.UPDATE_READY == "9.9.9",
                    "update_ready()=%r UPDATE_READY=%r" % (mod.update_ready(), mod.UPDATE_READY)))
        mod._PUBLISHED["ready"] = None
        # 反向自证：老形状（包门面 import *）在 1.4.0 上拿不到派生状态 ⇒ 缺陷无法静默复现
        star_ns = {}
        exec("from template.update_helper.update_helper import *", star_ns)
        out.append(("E import * 不搬运 UPDATE_READY（结构上防死副本）",
                    "UPDATE_READY" not in star_ns and "PENDING_CMD" not in star_ns,
                    "import * 后%s" % ("含该名（危险）" if "UPDATE_READY" in star_ns else "不含该名")))
        out.append(("E 拉起脚本的语义在本模块（DETACHED+无窗口）",
                    "def launch_pending_cmd" in src and "DETACHED_PROCESS" in src
                    and "CREATE_NO_WINDOW" in src, "见 launch_pending_cmd"))
        tgt, stage, work = r"C:\t\target", r"C:\t\upd\stage", r"C:\t\upd"
        snap, bak, failed = r"C:\t\_backup.pre", r"C:\t\_backup", r"C:\t\update.failed"
        text = mod.build_apply_script(tgt, stage, work, bak, r"C:\t\update.log",
                                      limit=mod.UPDATE_WAIT_LIMIT)
        kp = _apply_bat_keypoints(text, mod.EXE_NAME, tgt, stage, snap, bak, work, failed,
                                  mod.UPDATE_WAIT_LIMIT)
        for label, ok in kp:
            out.append(("E " + label, ok, "ok" if ok else "缺失"))
        # 反向：旧合成形态必须被判缺项（证明上面每一条都不是空转）
        old = ('@echo off\r\nset "STAGE=%s"\r\nset "TARGET=%s"\r\n'
               'timeout /t 2 /nobreak >nul\r\n'
               'robocopy "%%STAGE%%" "%%TARGET%%" /e /njh /njs\r\n'
               'start "" "%%TARGET%%\\%s"\r\n' % (stage, tgt, mod.EXE_NAME))
        rev = dict(_apply_bat_keypoints(old, mod.EXE_NAME, tgt, stage, snap, bak, work, failed,
                                        mod.UPDATE_WAIT_LIMIT))
        missing = sorted(k for k, v in rev.items() if not v)
        out.append(("E 反向：旧合成形态被判缺项", len(missing) >= 6, "缺 " + "、".join(missing)))
        # 2026-09-19：**`budget_s` 必须与实参 `limit` 同源**（1.4.4 修的缺陷）。
        # `update_helper.py` 的 docstring 早就写明"判据落点在 sync_check --selftest 的
        # update_helper 组"，而这里此前**没有这条腿** ⇒ **承诺的判据不存在，等于没判据**
        # （§4.1.18 的同族：判据存在 ≠ 它真的在跑）。
        # 判别力靠三格：limit=2 ⇒ budget 2s；limit=120 ⇒ budget 120s（**两个不同输入给出
        # 两个不同输出** ⇒ 证明它跟着实参走，而不是恒等于某个常量）；再加一格**真变异**。
        b2 = mod.build_apply_script(tgt, stage, work, bak, r"C:\t\update.log", limit=2)
        out.append(("E budget_s 取自实参 limit（limit=2 ⇒ budget 2s）",
                    "budget 2s" in b2,
                    "budget 片段: %s"
                    % ([ln.strip() for ln in b2.splitlines() if "nominal budget" in ln][:1] or "无")))
        b120 = mod.build_apply_script(tgt, stage, work, bak, r"C:\t\update.log",
                                      limit=mod.UPDATE_WAIT_LIMIT)
        out.append(("E budget_s 跟着实参走（limit=120 ⇒ budget 120s）",
                    "budget 120s" in b120, "limit=%d" % mod.UPDATE_WAIT_LIMIT))
        # **反向格 = 真变异**：把源码改回旧写法（budget 取模块常量），重新加载后渲染
        # `limit=2` ⇒ 上面那条断言**必须失败**。没有这一格，"渲染里恰好印了 budget"也能过。
        old_form = "budget_s=limit * UPDATE_WAIT_TICK_MS // 1000"
        new_form = "budget_s=UPDATE_WAIT_BUDGET_S"
        src_u = path.read_text(encoding="utf-8")
        if old_form in src_u:
            import tempfile as _tf
            mut_dir = Path(_tf.mkdtemp(prefix="uh-mut-"))
            try:
                mut_path = mut_dir / "uh_mut.py"
                mut_path.write_text(src_u.replace(old_form, new_form), encoding="utf-8")
                mspec = importlib.util.spec_from_file_location("_tpl_uh_mut_budget", mut_path)
                mmod = importlib.util.module_from_spec(mspec)
                mspec.loader.exec_module(mmod)
                mtext = mmod.build_apply_script(tgt, stage, work, bak, r"C:\t\update.log",
                                                limit=2)
                out.append(("E 反向：budget 取模块常量时 limit=2 必须**不再是** budget 2s",
                            "budget 2s" not in mtext,
                            "变异后 budget 片段: %s"
                            % ([ln.strip() for ln in mtext.splitlines()
                                if "budget" in ln][:1] or "无")))
            except Exception as exc:
                out.append(("E 反向：budget 取模块常量时 limit=2 必须**不再是** budget 2s",
                            False, "变异加载失败: %r" % (exc,)))
            finally:
                import shutil as _sh
                _sh.rmtree(mut_dir, ignore_errors=True)
        else:
            out.append(("E 反向：budget 取模块常量时 limit=2 必须**不再是** budget 2s",
                        False, "找不到待变异的写法 `%s`（判据与实现已脱节，请同步）" % old_form))
    except Exception as exc:
        out.append(("E update_helper script", False, "异常: %r" % (exc,)))
    finally:
        if added and need in sys.path:
            sys.path.remove(need)
        sys.modules.pop("_tpl_update_helper_selftest", None)
    return out


def _apply_bat_mutation_cases():
    """E-mut 组：**变异矩阵**——每条判据"还能不能失败"。返回 [(label, ok, detail)]。

    为什么必须要有它：判据**通过**的那一侧，"正常工作"与"已经停止工作"是**完全同形**的。
    实测（2026-09-19）：删掉真正执行安装的那一行 robocopy，21 条判据只有 1 条变红——
    「检查 rc，失败不启动新 exe」因为 `rc_i > copy_i` 在 `copy_i == -1` 时**恒真**而悄悄哑掉。
    原来那条聚合反向样本（"旧合成形态 ≥6 缺项"）看不见这种事：它报了 6 条红，
    **谁也看不出其中一条已经不会失败了**。

    两条设计约束（都是踩过的）：
      * **变异必须真的改变文本**（否则"没变红"会被读成"判据很健康"）；
      * **"应该死"的集合要按判据自己声称的语义写**：它守护的那一行没了，它就该红。
        守护不到 ⇒ **空真**（判据已不会失败），单独报出来，不与"未覆盖"混为一谈。

    已知**覆盖缺口**（登记，不假装有判据）：删掉 `if errorlevel 1 goto gone` 之后
    没有任何判据变红——"等待循环能退出"这件事今天没有判据覆盖。
    """
    import importlib.util
    out = []
    path = TEMPLATE_DIR / TPL_DIR_NAME / "update_helper" / "update_helper.py"
    if not path.exists():
        return [("E-mut 变异矩阵", False, "模板 update_helper.py 不存在")]
    spec = importlib.util.spec_from_file_location("_tpl_uh_mut", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_tpl_uh_mut"] = mod
    need = str(TEMPLATE_DIR)
    added = need not in sys.path
    if added:
        sys.path.insert(0, need)
    try:
        spec.loader.exec_module(mod)
        tgt, stage, work = r"C:\t\target", r"C:\t\upd\stage", r"C:\t\upd"
        snap, bak, failed = r"C:\t\_backup.pre", r"C:\t\_backup", r"C:\t\update.failed"
        limit = mod.UPDATE_WAIT_LIMIT
        text = mod.build_apply_script(tgt, stage, work, bak, r"C:\t\update.log", limit=limit)

        def verdict(t):
            return dict(_apply_bat_keypoints(t, mod.EXE_NAME, tgt, stage, snap, bak,
                                             work, failed, limit))

        base = verdict(text)
        red_base = sorted(k for k, v in base.items() if not v)
        out.append(("E-mut 控制组：原样 bat 必须 0 红", not red_base,
                    "红: " + "、".join(red_base) if red_base else "0 红"))

        # ---- 绿侧控制：语义等价改写的拼写，不得改变任何结论 ----
        # 基底由**当前那份渲染文本**来决定：先把四条命令的首 token 一律归到**裸名**，
        # 再从裸名派生各个形态。这样无论模板正文此刻是裸名还是绝对路径，绿侧都成立。
        BARE = {"tasklist": "tasklist", "find": "find",
                "robocopy": "robocopy", "powershell": "powershell"}
        ABS = {"tasklist": "tasklist.exe", "find": "find.exe",
               "robocopy": "Robocopy.exe",
               "powershell": "WindowsPowerShell\\v1.0\\powershell.exe"}
        ABS_PREFIX = "%SystemRoot%\\System32\\"

        def _set_tokens(t, names, prefix):
            """把 names 里那些命令的**首 token**换成 prefix + 可执行名。"""
            out_lines = []
            for ln in t.splitlines():
                c, _a = _split_cmd(ln)
                stripped = ln.lstrip()
                if c in names and stripped:
                    parts = stripped.split(None, 1)
                    tail = (" " + parts[1]) if len(parts) > 1 else ""
                    out_lines.append(ln[:len(ln) - len(stripped)] + prefix + names[c] + tail)
                else:
                    out_lines.append(ln)
            return "\n".join(out_lines)

        bare = _set_tokens(text, BARE, "")
        green_forms = [
            ("裸名基底（归一后的对照）", bare),
            ("四条命令绝对路径化（跟 reme 蓝图）", _set_tokens(bare, ABS, ABS_PREFIX)),
            ("只把 robocopy 改成 reme 的大小写拼写",
             _set_tokens(bare, {"robocopy": "Robocopy.exe"}, ABS_PREFIX)),
        ]
        seen = {text}
        for label, mutated in green_forms:
            if mutated in seen:
                out.append(("E-mut 绿侧 %s：变异必须真的改变文本" % label, False, "文本未变"))
                continue
            seen.add(mutated)
            r = sorted(k for k, v in verdict(mutated).items() if not v)
            out.append(("E-mut 绿侧 %s 必须仍 0 红" % label, not r,
                        "红: " + "、".join(r) if r else "0 红"))

        # ---- 红侧：删掉某一行，它守护的判据必须变红 ----
        MUTATIONS = [
            ("删安装复制行（robocopy STAGE→TARGET）",
             lambda l: _split_cmd(l)[0] == "robocopy" and '"%STAGE%"' in l and '"%TARGET%"' in l,
             ("检查 rc，失败不启动新 exe", "替换前先快照",
              "start 前有存在性守卫（缺 exe 不弹模态框）")),
            ("删快照行（robocopy TARGET→SNAPSHOT）",
             lambda l: _split_cmd(l)[0] == "robocopy" and '"%TARGET%"' in l and '"%SNAPSHOT%"' in l,
             ("替换前先快照", "空暂存包前置拦截（不碰安装目录）")),
            ("删 rc 判定行",
             lambda l: l.startswith("if %RC% geq 8 goto install_failed"),
             ("检查 rc，失败不启动新 exe", "成功后才轮转备份（失败时旧备份还在）",
              "失败回铺快照", "回铺也失败则不启动")),
            ("删回铺行（robocopy SNAPSHOT→TARGET）",
             lambda l: _split_cmd(l)[0] == "robocopy" and '"%SNAPSHOT%"' in l and '"%TARGET%"' in l,
             ("失败回铺快照",)),
            ("删轮转行（move SNAPSHOT→BACKUP）",
             lambda l: l.startswith("move /y") and "%SNAPSHOT%" in l,
             ("成功后才轮转备份（失败时旧备份还在）",)),
            ("删 :install_dead 标签",
             lambda l: l.strip() == ":install_dead",
             ("回铺也失败则不启动",)),
        ]
        empty_truth = []
        for label, match, should_die in MUTATIONS:
            lines = text.splitlines(keepends=True)
            keep = [l for l in lines if not match(l.strip())]
            mutated = "".join(keep)
            if mutated == text:
                out.append(("E-mut %s：变异必须真的改变文本" % label, False, "没有任何行被删"))
                continue
            after = verdict(mutated)
            survived = [s for s in should_die if after.get(s, False)]
            if survived:
                empty_truth.extend((label, s) for s in survived)
            out.append(("E-mut %s ⇒ 应死判据全部变红" % label, not survived,
                        "空真: " + "、".join(survived) if survived else "已死 " + str(len(should_die))))
        out.append(("E-mut **空真集合为空**（没有判据停止工作）", not empty_truth,
                    "空真 %d 处" % len(empty_truth) if empty_truth else "0 处"))
    except Exception as exc:
        out.append(("E-mut 变异矩阵", False, "异常: %r" % (exc,)))
    finally:
        if added and need in sys.path:
            sys.path.remove(need)
        sys.modules.pop("_tpl_uh_mut", None)
    return out


def _tray_kit_probe_cases():
    """F 组：`tray_kit.mutex_name_is_valid` 探针语义（2.1.0，D3.3）。返回 [(label, ok, detail)]。

    探针要被 `--smoke` 用来覆盖"互斥体名合法"这条，它必须满足四个性质——**每条都对应一次
    真实的踩坑**，所以逐条钉住，而不是只测"返回值是 bool"：
      ① 合法名 → True；
      ② 非法名（`Local\\` 之后再出现反斜杠，SINGLE-01 的根因）→ False；
      ③ 名字**已被占用** → 仍 True（`ERROR_ALREADY_EXISTS` 也算内核接受；否则用户实例在跑时
         冒烟会假红——这正是不能拿 `single_instance_free` 当探针的原因）；
      ④ 探测完**不留句柄**（否则探针自己把锁占了，用户接下来的托盘会被判"已有实例"）；
      ⑤ 内核不可用 → 放行（失败方向同守卫：宁可漏判，不可把工具判死）。
    """
    import importlib.util
    import ctypes as _ctypes
    out = []
    path = TEMPLATE_DIR / TPL_DIR_NAME / "tray_kit" / "tray_kit.py"
    if not path.exists():
        return [("F tray_kit probe", False, "模板 modules/tray_kit/tray_kit.py 不存在")]
    spec = importlib.util.spec_from_file_location("_tpl_tray_kit_selftest", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_tpl_tray_kit_selftest"] = mod
    try:
        spec.loader.exec_module(mod)
        name = r"Local\my-helper-single-instance"
        bad = r"Local\my-helper\SingleInstance"
        out.append(("F 合法名 → True", mod.mutex_name_is_valid("my-helper", name) is True, name))
        out.append(("F 非法名 → False（SINGLE-01 根因）",
                    mod.mutex_name_is_valid("my-helper", bad) is False, bad))
        # 2.2.0：形状判据单一化——同一条规则同时约束守卫/探针/空闲探测（不写两份规则）
        shapes = [(None, False), ("", False), ("helper", False), (r"Global\helper", False),
                  (r"Local\helper", True), (r"Local\helper-single-instance", True), (123, False)]
        out.append(("F 形状判据（空/非串/无前缀/多反斜杠）",
                    all(mod.mutex_name_ok(v) is want for v, want in shapes),
                    "mutex_name_ok 覆盖 %d 例" % len(shapes)))
        logs = []
        guard_ok = mod.acquire_single_instance("my-helper", bad, log=logs.append) is True
        out.append(("F 守卫遇非法名放行且记日志（D3.2）", guard_ok and bool(logs),
                    logs[0][:60] if logs else "无日志"))
        # ③ 自己先占住同名的另一个句柄，探针仍须判 True
        k32 = _ctypes.WinDLL("kernel32", use_last_error=True)
        k32.CreateMutexW.restype = _ctypes.c_void_p
        _ctypes.set_last_error(0)
        held = k32.CreateMutexW(None, False, name)
        _ctypes.set_last_error(0)
        out.append(("F 名字被占用仍算合法（否则冒烟假红）",
                    mod.mutex_name_is_valid("my-helper", name) is True,
                    "err=%s" % _ctypes.get_last_error()))
        if held:
            k32.CloseHandle(held)
        # ④ 探针没留下句柄：关掉 held 后再建应拿到 err=0（无人持有）
        _ctypes.set_last_error(0)
        again = k32.CreateMutexW(None, False, name)
        err = _ctypes.get_last_error()
        if again:
            k32.CloseHandle(again)
        out.append(("F 探针不留句柄（不占锁）", err == 0, "err=%s" % err))
        # ⑤ 内核不可用 → 放行
        real = mod.ctypes

        class _Boom:
            @staticmethod
            def WinDLL(*_a, **_k):
                raise OSError("simulated: kernel32 unavailable")

        mod.ctypes = _Boom
        try:
            out.append(("F 内核不可用 → 放行（失败方向同守卫）",
                        mod.mutex_name_is_valid("my-helper", name) is True, "True"))
        finally:
            mod.ctypes = real
    except Exception as exc:
        out.append(("F tray_kit probe", False, "异常: %r" % (exc,)))
    finally:
        sys.modules.pop("_tpl_tray_kit_selftest", None)
    return out


def _apply_bat_runtime_cases():
    """E 组（**真跑**）：把生成的 apply.bat 放进沙箱执行，验"空暂存包"这条路。

    为什么必须真跑：模态框卡死在**文本断言里看不出来**——脚本里确实有 `start` 语句，
    只是那条路不该被走到；只有跑一遍、看它**秒级退出** + marker 落地 + 安装目录没被动过，
    才能证伪。文本断言（E 组另外几条）只能证明"守卫写在那儿"，不能证明"路真的被拦住"。

    ⚠️ **别把沙箱当成"即便守卫失效也安全"**（lead 纠正，2026-09-19）：沙箱的目标目录里没有
    exe，所以**不会有进程被真正拉起**；但 `start "" "<不存在的路径>"` 仍然会弹出
    **"Windows 找不到文件"的模态框并永久阻塞**——弹框取决于**路径在不在**，与目录里有没有
    exe 无关。也就是说：**守卫一旦失效，这条用例自己就会挂住**（这正是它有价值的原因，
    断言"秒级退出"抓的就是这个；同时也说明它必须带 timeout）。

    对照的故障链（lead 实测）：STAGE 空 ⇒ `robocopy /e /purge` 返回 0–7 被判成功
    ⇒ **安装目录被清空** ⇒ `start "" <不存在的 exe>` 弹**模态框**永久阻塞。
    """
    import importlib.util
    import subprocess
    import time as _time
    out = []
    path = TEMPLATE_DIR / TPL_DIR_NAME / "update_helper" / "update_helper.py"
    if not path.exists():
        return [("E-runtime apply.bat", False, "模板 update_helper.py 不存在")]
    spec = importlib.util.spec_from_file_location("_tpl_uh_runtime", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["_tpl_uh_runtime"] = mod
    need = str(TEMPLATE_DIR)
    added = need not in sys.path
    if added:
        sys.path.insert(0, need)
    base = Path(tempfile.mkdtemp(prefix="apply_bat_runtime_"))
    try:
        spec.loader.exec_module(mod)
        stage = base / "stage"; stage.mkdir()               # 空暂存包（rc=0 的陷阱源）
        install = base / "install"; install.mkdir()
        (install / "sentinel.txt").write_text("old install payload", encoding="utf-8")
        work = base / "work"; work.mkdir()
        log = base / "update.log"
        text = mod.build_apply_script(str(install), str(stage), str(work),
                                      str(base / "_backup"), str(log))
        bat = base / "apply.bat"
        try:
            bat.write_text(text, encoding="mbcs", errors="replace")
        except (LookupError, UnicodeError):
            bat.write_text(text, encoding="utf-8")
        t0 = _time.time()
        hung = False
        try:
            subprocess.run(["cmd", "/c", str(bat)], capture_output=True, timeout=60,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except subprocess.TimeoutExpired:
            hung = True
        elapsed = _time.time() - t0
        marker = base / "update.failed"
        out.append(("E-runtime 空暂存包：正常退出不阻塞（模态框会挂死）",
                    not hung and elapsed < 30, "%.1fs%s" % (elapsed, " 超时!" if hung else "")))
        out.append(("E-runtime 空暂存包：写了 update.failed marker",
                    marker.is_file(), "存在" if marker.is_file() else "缺失"))
        out.append(("E-runtime 空暂存包：安装目录没被动过（/purge 没跑）",
                    (install / "sentinel.txt").is_file(),
                    "sentinel %s" % ("在" if (install / "sentinel.txt").is_file() else "被清掉了")))
        out.append(("E-runtime 空暂存包：**保留现场**（走 :cleanup_keep，暂存还在）",
                    work.exists(), "work %s" % ("保留" if work.exists() else "被删了！")))
        out.append(("E-runtime 脚本自删（收尾走到 cleanup_tail）", not bat.exists(),
                    "bat %s" % ("还在" if bat.exists() else "已删")))

        # ---- 场景二：**回铺源为空**（SNAPSHOT 没内容）+ 替换失败（rc>=8）----
        # 第二条可达路径：`%SNAPSHOT%` 本身可能是空的（快照那步对**空安装目录**同样返回 0），
        # 于是回铺 rc=0 骗过 `errorlevel 8`，走到 `start` 一个不存在的 exe —— 失效形态同样是
        # **模态框永久阻塞**。断言点：必须落到 `:install_dead`（日志出现 "RESTORE FAILED"）、
        # 不启动任何 exe、marker 落地、现场保留。
        # 触发方式：**故障注入**——把 STAGE→TARGET 那条 robocopy 换成 `goto install_failed`，
        # 比"造一个真让 robocopy 返回 >=8 的目录"确定得多（l-s2t 的 test_update_safety 同法）。
        stage2 = base / "stage2"; stage2.mkdir()
        (stage2 / mod.EXE_NAME).write_bytes(b"MZ")          # 过"动手前先验暂存包"
        install2 = base / "install2"; install2.mkdir()
        (install2 / "sentinel.txt").write_text("old", encoding="utf-8")  # 关键：**没有 exe**
        work2 = base / "work2"; work2.mkdir()
        snap2 = base / "_snapshot2"                          # 不存在 ⇒ 回铺"成功但什么都没铺"
        log2 = base / "update2.log"
        text2 = mod.build_apply_script(str(install2), str(stage2), str(work2),
                                       str(base / "_backup2"), str(log2),
                                       snapshot_dir=str(snap2))
        # ⚠️ 正文里是 **cmd 变量**（`%STAGE%`/`%TARGET%`），不是展开后的路径——拿 str(stage2)
        # 去匹配永远找不到（E 组 harness 第二次踩这个坑）。按变量名选那一条。
        # 按**命令名**选那一条，不按拼写：`l.strip().startswith("robocopy")` 在脚本改成
        # 绝对路径（`%SystemRoot%\System32\Robocopy.exe`）之后就一条都选不到，`[0]` 直接
        # IndexError。这是"锚拼写"同一个病的第五处——前四处是 21 条判据里的三处分类器锚点
        # 与两处次序锚点。
        candidates = [l for l in text2.splitlines()
                      if _split_cmd(l.strip())[0] == "robocopy"
                      and "%STAGE%" in l and "%TARGET%" in l]
        if not candidates:
            # 具名失败，不用 `[0]`：`IndexError: list index out of range` 不告诉任何人
            # **是哪条轴**失配，而这里已知至少还有第三条轴没归一。
            raise AssertionError(
                "E-runtime：按命令名选不到 STAGE→TARGET 那条 robocopy。"
                "本选择器用的是 `%STAGE%`/`%TARGET%` **字面量**——与 idx_cmd / 变异 lambda 同轴。"
                "若哪天变量名与 reme（`%INSTALL%`）收敛，这里会先响：那时**把这条轴也归一，"
                "不要把断言放宽**。")
        copy_line = candidates[0]
        text2 = text2.replace(copy_line, "goto install_failed")
        bat2 = base / "apply2.bat"
        try:
            bat2.write_text(text2, encoding="mbcs", errors="replace")
        except (LookupError, UnicodeError):
            bat2.write_text(text2, encoding="utf-8")
        t0 = _time.time()
        hung2 = False
        try:
            subprocess.run(["cmd", "/c", str(bat2)], capture_output=True, timeout=60,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
        except subprocess.TimeoutExpired:
            hung2 = True
        elapsed2 = _time.time() - t0
        logtext = log2.read_text(encoding="utf-8", errors="replace") if log2.exists() else ""
        exe2 = install2 / mod.EXE_NAME
        out.append(("E-runtime 回铺源为空：正常退出不阻塞（模态框会挂死）",
                    not hung2 and elapsed2 < 30, "%.1fs%s" % (elapsed2, " 超时!" if hung2 else "")))
        out.append(("E-runtime 回铺源为空：落到 :install_dead（日志见 RESTORE FAILED）",
                    "RESTORE FAILED" in logtext,
                    "log %s" % ("命中" if "RESTORE FAILED" in logtext else "没有该行")))
        out.append(("E-runtime 回铺源为空：没启动任何 exe（目录里仍无 exe）",
                    not exe2.exists(), "exe %s" % ("出现了！" if exe2.exists() else "不存在")))
        out.append(("E-runtime 回铺源为空：marker 落地 + 现场保留",
                    (base / "update.failed").is_file() and work2.exists(),
                    "marker=%s work=%s" % ((base / "update.failed").is_file(), work2.exists())))
    except Exception as exc:
        out.append(("E-runtime apply.bat", False, "异常: %r" % (exc,)))
    finally:
        if added and need in sys.path:
            sys.path.remove(need)
        sys.modules.pop("_tpl_uh_runtime", None)
        # 删不掉就**抛**（这里在 finally 里，抛出会替换返回值 = fail closed）：
        # 本函数是判据的一部分，"临时目录泄漏"必须比"某个检查的结论"更响。
        if not _rmtree_strict(base):
            raise RuntimeError("temp dir not removed (leak): %s" % base)
    return out


def _header_silence_cases(base: Path):
    """1.9.0 四条腿的**反向单元 + 控制单元**（最小变量法）。返回 [(label, ok, detail)]。

    四腿各要一个"该红"的样本和一个"看起来像但该绿"的对照——只有一边的样本等于
    "没有样本的分支"（§4.1.13 同款教训：没有样本的分支等于没有判据）。
    """
    cases = []
    tpl_paths = TEMPLATE_DIR / TPL_DIR_NAME / "paths" / "paths.py"
    if not tpl_paths.exists():
        return [("1.9.0 样本前置：模板 modules/paths/paths.py 存在", False, "缺模板件")]
    tpl_text = read_text(tpl_paths)
    # ① 剥掉出处行 = "拷贝被剥了头"（内容其余部分与模板一致）
    stripped = "\n".join(l for l in tpl_text.splitlines() if not META_LINE.match(l))

    # 腿① 命中：无头 + 内容等于模板件
    d1 = base / "leg1copy" / "src" / "template" / "paths"
    d1.mkdir(parents=True)
    (d1 / "paths.py").write_text(stripped, encoding="utf-8")
    copies, ns = no_header_legs(base / "leg1copy")
    cases.append(("腿① 无头拷贝 ⇒ 命中 NO-HDR-COPY", len(copies) == 1,
                  f"copies={len(copies)} ns={len(ns)}"))
    # 腿① 控制：**只加回出处行**（最小变量），其余一字节不动 ⇒ 不再命中
    d2 = base / "leg1ctl" / "src" / "template" / "paths"
    d2.mkdir(parents=True)
    (d2 / "paths.py").write_text(
        "# TEMPLATE-MODULE: paths | TEMPLATE-VER: 1.1.4\n" + stripped, encoding="utf-8")
    copies2, _ = no_header_legs(base / "leg1ctl")
    cases.append(("腿① 控制：同内容 + 出处头 ⇒ 不命中", len(copies2) == 0,
                  f"copies={len(copies2)}"))

    # 腿② 命中：src/modules/ 下无头、内容与模板无一相同（既不是拷贝也必须看得见）
    d3 = base / "leg2ns" / "src" / "template" / "zzz"
    d3.mkdir(parents=True)
    (d3 / "zzz.py").write_text("MARKER = 'tool-owned'\n", encoding="utf-8")
    copies3, ns3 = no_header_legs(base / "leg2ns")
    cases.append(("腿② src/modules/ 下无头 ⇒ 黄灯可见（且不误报成拷贝）",
                  len(ns3) == 1 and len(copies3) == 0,
                  f"ns={len(ns3)} copies={len(copies3)}"))
    # 腿② 控制：同样的文件放到 src/ 之外（工具自有件的地盘）⇒ 两条腿都不响
    d4 = base / "leg2ctl" / "src"
    d4.mkdir(parents=True)
    (d4 / "main.py").write_text("MARKER = 'tool-owned'\n", encoding="utf-8")
    copies4, ns4 = no_header_legs(base / "leg2ctl")
    cases.append(("腿② 控制：同内容放 src/（非 modules 命名空间）⇒ 不响",
                  len(ns4) == 0 and len(copies4) == 0, f"ns={len(ns4)}"))

    # 腿③ BAD-HDR 两种形态：模块名不存在 / MODULE 头推导不出目标
    d5 = base / "leg3bad" / "src"
    d5.mkdir(parents=True)
    (d5 / "a.py").write_text("# TEMPLATE-MODULE: nosuchmod\nX = 1\n", encoding="utf-8")
    (d5 / "b.py").write_text("# TEMPLATE-FROM: my-diy-tool-template/template/nope.py\nX = 1\n",
                             encoding="utf-8")
    found5, anom5 = scan_tool(base / "leg3bad")
    # 该目录里还有 b.py（FROM 指向不存在的模板件）：它**应当**进 found 并走原有 [MISS] 出口。
    # 本条要钉的性质是"坏头的 a.py **既不静默消失、也不混进 found**"——两份文件两种命运。
    names5 = sorted(p.name for p, _r, _d, _v in found5)
    cases.append(("腿③ 申报的模块不存在 ⇒ BAD-HDR（且该件不进 found，另一件照常）",
                  len(anom5) == 1 and names5 == ["b.py"],
                  f"anom={len(anom5)} found={names5}"))
    # 腿③ 控制：合法头 ⇒ 无 anomaly、进 found；FROM 指向不存在的模板件走 [MISS]（原有出口）
    d6 = base / "leg3ok" / "src"
    d6.mkdir(parents=True)
    (d6 / "c.py").write_text("# TEMPLATE-FROM: my-diy-tool-template/template/paths/paths.py\n"
                             "X = 1\n", encoding="utf-8")
    found6, anom6 = scan_tool(base / "leg3ok")
    cases.append(("腿③ 控制：合法出处头 ⇒ 无 anomaly 且进 found",
                  len(anom6) == 0 and len(found6) == 1,
                  f"anom={len(anom6)} found={len(found6)}"))

    # 腿④ 申报口：NOT-WIRED.md 存在 ⇒ 认；不存在 ⇒ 不认（最小变量：一个文件）
    d7 = base / "leg4" / "src" / "template" / "service_link"
    d7.mkdir(parents=True)
    before = declared_not_wired(d7)
    (d7 / "NOT-WIRED.md").write_text("有意未接入（selftest 样本）\n", encoding="utf-8")
    after = declared_not_wired(d7)
    cases.append(("腿④ NOT-WIRED.md：无 ⇒ 空 / 有 ⇒ 认（同一目录，只加一个文件）",
                  before == "" and after == "NOT-WIRED.md",
                  f"before={before!r} after={after!r}"))
    return cases


def selftest() -> int:
    """回归样本（`--selftest`，可重复执行）：锁死本家族两条判据。

      A 带 TEMPLATE 头的 .md            → 必须 [DIFF]（旧归一化会误判 [ok]，§4.1.10a）
      B 逐字节相同的 .md                → 必须 [ok]
      C 同模块 .py 带 OVERRIDE、README 不同 → 必须 [decl]
      D 模板 i18n 包状态（2.1.1）：init 切换后**从包命名空间**读到的语言必须立即变
      E 模板 update_helper 替换脚本（1.3.0）：等待/上限/快照/rc/回铺/marker/收尾逐项在位，
        且旧合成形态被判缺项（反向）

    为什么固化成开关而不是跑一次：一次性命令会随会话消失，判据下次被改坏时无人察觉
    ——"已知样本反向验证"必须是可重跑的资产。D 组原先是一个根目录独立脚本，无调用方
    （=死代码），折进来后自动获得"改坏即 exit 1"的保障（CONFORMANCE §4.1.13 同款教训）。
    """
    tpl = TEMPLATE_DIR / TPL_DIR_NAME / "paths" / "README.md"
    if not tpl.exists():
        print("[selftest] FAIL: 模板 modules/paths/README.md 不存在")
        return 1
    tpl_bytes = tpl.read_bytes()
    rel = "template/paths/README.md"
    base = Path(tempfile.mkdtemp(prefix="sync_check_selftest_"))
    try:
        cases = []
        a = base / "a" / "src" / "template" / "paths"
        a.mkdir(parents=True)
        (a / "README.md").write_bytes(
            b"# TEMPLATE-FROM: my-diy-tool-template/template/paths/README.md\n" + tpl_bytes)
        cases.append(("A header-bearing .md", a / "README.md", False, "diff", None))

        b = base / "b" / "src" / "template" / "paths"
        b.mkdir(parents=True)
        (b / "README.md").write_bytes(tpl_bytes)
        cases.append(("B byte-identical .md", b / "README.md", False, "ok", None))

        c = base / "c" / "src" / "template" / "paths"
        c.mkdir(parents=True)
        (c / "README.md").write_bytes(b"# overridden shape\n" + tpl_bytes)
        (c / "paths.py").write_text(
            "# TEMPLATE-FROM: my-diy-tool-template/template/paths/paths.py | TEMPLATE-VER: 1.1.3\n"
            "# TEMPLATE-LOCAL-OVERRIDE: selftest - module intentionally diverged\n"
            "X = 1\n", encoding="utf-8")
        cases.append(("C module-level OVERRIDE .md", c / "README.md", "paths.py",
                      "decl", "declared via paths.py"))

        failed = 0
        for label, cand, declared, want, want_note in cases:
            got, note = compare(cand, rel, False, declared, "", False)[:2]
            ok = got == want and (want_note is None or want_note in note)
            failed += 0 if ok else 1
            print(f"[selftest] {'PASS' if ok else 'FAIL'}  {label}: "
                  f"got {got}{note!r}, want {want}")

        for label, ok, detail in _i18n_state_cases():
            failed += 0 if ok else 1
            print(f"[selftest] {'PASS' if ok else 'FAIL'}  {label}: {detail}")

        for label, ok, detail in _update_helper_cases():
            failed += 0 if ok else 1
            print(f"[selftest] {'PASS' if ok else 'FAIL'}  {label}: {detail}")

        for label, ok, detail in _apply_bat_mutation_cases():
            failed += 0 if ok else 1
            print(f"[selftest] {'PASS' if ok else 'FAIL'}  {label}: {detail}")

        for label, ok, detail in _tray_kit_probe_cases():
            failed += 0 if ok else 1
            print(f"[selftest] {'PASS' if ok else 'FAIL'}  {label}: {detail}")

        for label, ok, detail in _apply_bat_runtime_cases():
            failed += 0 if ok else 1
            print(f"[selftest] {'PASS' if ok else 'FAIL'}  {label}: {detail}")

        for label, ok, detail in _script_form_cases():
            failed += 0 if ok else 1
            print(f"[selftest] {'PASS' if ok else 'FAIL'}  {label}: {detail}")

        for label, ok, detail in _header_silence_cases(base):
            failed += 0 if ok else 1
            print(f"[selftest] {'PASS' if ok else 'FAIL'}  {label}: {detail}")

        print(f"[selftest] {'ALL PASS' if not failed else '%d FAILED' % failed}")
        rc = 1 if failed else 0
    finally:
        # C-30 的作者自己也得守 C-30：删完**回读确认**，删不掉就让退出码变红
        # （旧写法 `rmtree(base, ignore_errors=True)` 把"删不掉"变成"看起来删掉了"）。
        if not _rmtree_strict(base):
            rc = 1
    return rc


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
    parser.add_argument("--selftest", action="store_true",
                        help="用合成样本回归 .md 判定语义（A[DIF]/B[ok]/C[decl]）后退出")
    args = parser.parse_args()
    if args.selftest:
        return selftest()

    tpl_modules = template_modules()
    drift, declared, missing, params, lags, nohdr, miss_mod, miss_file, diffs = (
        [], [], [], [], [], [], [], [], [])
    # 1.9.0 新增四条腿的可观测量（详见 scan_tool / no_header_legs 的 docstring）
    bad_hdr, nohdr_copy, nohdr_ns, not_wired = [], [], [], []

    def emit(kind, name, tool_dir, tool_file, rel, note, tool_ver, tpl_ver, is_declared):
        leaf = tool_file.relative_to(tool_dir)
        if kind == "ok":
            print(f"[ok]    {name}/{leaf} == {TEMPLATE_DIR.name}/{rel}{note}")
        elif kind == "diff":
            diffs.append((name, tool_file, rel))
            print(f"[DIFF]  {name}/{leaf} != {TEMPLATE_DIR.name}/{rel}"
                  f" —— 模块文档须与正本逐字节一致、不带任何 TEMPLATE 头（§4.1.10a）")
        elif kind == "param":
            params.append(name)
            print(f"[param] {name}/{leaf} (参数文件，按设计豁免)")
        elif kind == "nohdr":
            nohdr.append((name, tool_file, rel))
            print(f"[NOHDR] {name}/{leaf} != {TEMPLATE_DIR.name}/{rel}{note}"
                  f" —— 该 .py 缺 TEMPLATE-FROM/MODULE 头，补头后纳入版本/申报机制"
                  f"（README 等 .md 不走头机制、**不得补头**）")
        elif kind == "lag":
            dec = "，已申报 override 但未跟到新版" if is_declared else ""
            lags.append((name, tool_file, rel, tool_ver, tpl_ver))
            print(f"[lag]  {name}/{leaf} lags {TEMPLATE_DIR.name}/{rel}{note}{dec}")
        elif kind == "decl":
            declared.append((name, tool_file, rel))
            print(f"[decl ] {name}/{leaf} deviates from {TEMPLATE_DIR.name}/{rel}{note}")
        elif kind == "drift":
            drift.append((name, tool_file, rel))
            print(f"[DRIFT] {name}/{leaf} deviates from {TEMPLATE_DIR.name}/{rel}{note}")
        else:  # miss
            missing.append((name, tool_file, rel))
            print(f"[MISS ] {name}/{leaf} -> {TEMPLATE_DIR.name}/{rel} 不存在")

    print(identity_line())   # checker 自身身份（VER + 两种哈希）

    for name in args.roots:
        tool_dir = ROOT / name
        if not tool_dir.is_dir():
            print(f"[skip]  {name}: no such dir")
            continue
        # 被检仓库的修订与脏净：`dirty=yes` 一行暴露"这条结论建立在未提交改动上"
        print(f"[repo] {name}: {repo_identity(tool_dir)}")
        is_blueprint = name in BLUEPRINTS
        if is_blueprint:
            print(f"[bp  ] {name}: blueprint —— 逐文件比对，落后报 [lag]（不阻断）")

        compared, compared_rels, consumed = set(), set(), set()
        # 头部通道消费掉的模块 → 该模块被用到的**工具侧文件**（判定"脚本形态采纳"用）
        consumed_files = {}

        # ① 头部通道：工具自报出处的文件
        scanned, hdr_anoms = scan_tool(tool_dir)
        for tool_file, rel, is_declared, tool_ver in scanned:
            rel = LEGACY_ALIAS.get(rel, rel)
            compared.add(tool_file.resolve())
            compared_rels.add(rel)
            parts = rel.split("/")
            if len(parts) >= 2 and parts[0] == TPL_DIR_NAME:
                consumed.add(parts[1])
                consumed_files.setdefault(parts[1], []).append(tool_file)
            kind, note, tv, pv = compare(tool_file, rel, is_blueprint, is_declared,
                                         tool_ver, True)
            emit(kind, name, tool_dir, tool_file, rel, note, tv, pv, is_declared)

        # ①b **申报了出处却解析不出来**（原先是静默 continue）——缺陷输入必须与"无出处"分开
        for py, kind, detail in hdr_anoms:
            bad_hdr.append((name, py, detail))
            print(f"[{kind}] {name}/{py.relative_to(tool_dir).as_posix()}: {detail}"
                  f" —— 头部申报的出处不可解析（不是'工具自有'，是**头坏了**）")

        # ①c **缺头 ⇒ 报**的两条腿（见 no_header_legs）
        hdr_copies, ns_files = no_header_legs(tool_dir)
        for py, hits in hdr_copies:
            nohdr_copy.append((name, py, hits))
            print(f"[NO-HDR-COPY] {name}/{py.relative_to(tool_dir).as_posix()} 无出处头，"
                  f"但内容等于 {TEMPLATE_DIR.name}/{hits[0]} —— 拷贝被剥掉了头"
                  f"（补 TEMPLATE-FROM/MODULE 头，或申报 TEMPLATE-LOCAL-OVERRIDE）")
        for py in ns_files:
            nohdr_ns.append((name, py))
            print(f"[NO-HDR] {name}/{py.relative_to(tool_dir).as_posix()} 位于 src/modules/ "
                  f"命名空间却无任何出处头 —— 是工具自有件还是漏了头？需人判断")

        # ② 布局通道：src/modules/<模块>/ 下与模板同名者，**不要求工具侧有头**
        for mod, pys in sorted(tpl_modules.items()):
            mod_dir = tool_dir / "src" / TPL_DIR_NAME / mod
            if mod_dir.is_dir():
                consumed.add(mod)
            # **脚本形态采纳**（lead 2026-09-19 裁定 (B)）：模块代码以 `src/<name>.py`
            # **就地**被采纳（头部通道消费过它），且工具侧**没有** `src/modules/<mod>/`
            # ——那它就不是"导入包"，`__init__.py` 与 `README.md` 都**不是缺口**，
            # 不报 [MISSING-FILE]，改报一条 [script] 说明。
            # 为什么不能一律要求：实测把 `src/icons.py` 移进 `src/modules/icons/` 后以
            # **脚本**方式运行会炸 `ModuleNotFoundError: No module named 'modules'`
            # ——`from modules.appconfig import ...` 依赖所在深度，模板 docstring 那句
            # "与本模块所在深度无关"**只对 ICON_ASSET 的路径解析成立**。为纯形态收益给
            # 一个 shipped 模块加 sys.path 兜底 = 引入复杂度换零功能（三家现在都能跑且
            # 代码逐字节一致）。
            script_form = is_script_form_adoption(mod, consumed, consumed_files,
                                                  mod_dir.is_dir())
            if script_form:
                paths = ", ".join(sorted({f.relative_to(tool_dir).as_posix()
                                          for f in consumed_files[mod]}))
                print(f"[script] {name}: modules/{mod}/ 以**脚本形态就地采纳**（{paths}）"
                      f"—— 不要求 __init__.py / README.md（本模块不作导入包使用）")
            # 模块级申报：该工具模块目录里任一 .py 带 TEMPLATE-LOCAL-OVERRIDE，
            # 即视整模块为有意分叉；其 README 差异随之记 [decl] 而非 [DIFF]。
            # 记下**申报来源文件名**，输出里带上，便于与"漏拷"一眼区分。
            mod_declared = ""
            if mod_dir.is_dir():
                for f in sorted(mod_dir.rglob("*.py")):
                    if (f.is_file() and not (set(f.parts) & SCAN_SKIP_DIRS)
                            and OVERRIDE_RE.search(read_text(f)[:4096])):
                        mod_declared = f.name
                        break
            # 模块级"有意未接入"申报口（#57）：见 declared_not_wired()
            not_wired_md = declared_not_wired(mod_dir)
            for tpl_py in pys:
                tpl_rel = tpl_py.relative_to(TEMPLATE_DIR).as_posix()
                cand = mod_dir / tpl_py.relative_to(TEMPLATE_DIR / TPL_DIR_NAME / mod)
                if not cand.exists():
                    # 模块已被采纳（有目录或头部通道消费了它的其它文件），却缺这一件
                    # → [MISSING-FILE] 黄灯。整个模块都没采纳的交给 [MISSING-MODULE]，
                    # 避免同一件事报两遍刷屏。
                    # **例外：脚本形态采纳**——代码以 `src/<name>.py` 就地使用，
                    # `__init__.py`/`README.md` 不是缺口（[script] 已单独说明）。
                    if script_form:
                        continue
                    if not_wired_md:
                        # 已申报（模块目录下有 NOT-WIRED.md）：不是"漏拷"，是"有意未接入"。
                        # [decl] 与 [MISSING-*] 必须是**两个不同的可观测量**，否则
                        # "已批准"与"没人注意"永远分不开（#57）。
                        print(f"[decl ] {name}: 缺 {TEMPLATE_DIR.name}/{tpl_rel}"
                              f"（已申报 via {not_wired_md}）")
                        continue
                    if mod in consumed and tpl_rel not in compared_rels:
                        miss_file.append((name, tpl_rel))
                        print(f"[MISSING-FILE] {name}: 缺 {TEMPLATE_DIR.name}/{tpl_rel}"
                              f"（模块 modules/{mod}/ 已采纳，此件未拷）")
                    continue
                if cand.resolve() in compared:
                    continue
                head = read_text(cand)[:4096]
                mver = VER_RE.search(head)
                # .md 用模块级申报；.py 仍用文件级申报
                decl_here = (mod_declared if cand.suffix.lower() == ".md"
                             else bool(OVERRIDE_RE.search(head)))
                kind, note, tv, pv = compare(
                    cand, tpl_rel, is_blueprint, decl_here,
                    mver.group(1) if mver else "", has_template_header(head))
                emit(kind, name, tool_dir, cand, tpl_rel, note, tv, pv, decl_here)

        # ③ 模板有、工具没有 → 整模块缺失（黄灯）；**已申报者除外**
        for mod in sorted(tpl_modules):
            if mod in consumed:
                continue
            mod_dir3 = tool_dir / "src" / TPL_DIR_NAME / mod
            if declared_not_wired(mod_dir3):
                not_wired.append((name, mod, mod_dir3 / "NOT-WIRED.md"))
                print(f"[decl ] {name}: 模板 modules/{mod}/ 未采纳（已申报 via "
                      f"src/modules/{mod}/NOT-WIRED.md）—— 不是遗漏，是有意未接入")
                continue
            miss_mod.append((name, mod))
            print(f"[MISSING-MODULE] {name}: 模板 modules/{mod}/ 有代码，工具无 "
                  f"src/modules/{mod}/ 且无文件申报来自该模块（可能内联实现或未采纳）"
                  f"；若是有意不接入，放一份 src/modules/{mod}/NOT-WIRED.md 申报")

    print()
    for name, tool_file, rel in missing:
        print(f"[MISS ] {name}: {TEMPLATE_DIR.name}/{rel} 不存在（检查头部路径）")
    if lags or nohdr or miss_mod or miss_file or diffs or nohdr_ns:
        print(f"needs human decision (yellow, non-blocking): "
              f"lag={len(lags)}, doc-md-diff={len(diffs)}, nohdr={len(nohdr)}, "
              f"missing-module={len(miss_mod)}, missing-file={len(miss_file)}, "
              f"no-header-in-modules={len(nohdr_ns)}"
              f" —— 见 my-diy-tool-template/对齐台账.md 对应格子")
    print(f"summary: {len(drift)} undeclared drift, {len(lags)} blueprint lag(s), "
          f"{len(declared)} declared override(s), {len(params)} param file(s), "
          f"{len(diffs)} doc byte-diff(s), {len(nohdr)} no-header mismatch(es), "
          f"{len(miss_mod)} missing module(s), {len(miss_file)} missing file(s), "
          f"{len(missing)} missing template(s), {len(bad_hdr)} bad header(s), "
          f"{len(nohdr_copy)} stripped-header copy(ies), {len(nohdr_ns)} unheaded-in-modules, "
          f"{len(not_wired)} declared not-wired")
    if drift or missing or bad_hdr or nohdr_copy:
        print("fix: 把模板修复同步到该工具（独立 commit + 门禁绿），或在文件头申报 TEMPLATE-LOCAL-OVERRIDE。")
        print("     [BAD-HDR]（申报的出处不可解析）与 [NO-HDR-COPY]（拷贝被剥掉头）为**红灯**：")
        print("     它们让'缺陷输入'与'工具自有'落在不同观测量上，不再静默。")
        print("     [DIFF]/[NOHDR]/[MISSING-*]/[lag]/[NO-HDR] 为黄灯：需人判断跟/不跟，不阻断门禁。")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
