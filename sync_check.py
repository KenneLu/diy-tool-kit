# TEMPLATE-MODULE: sync_check | TEMPLATE-VER: 3.0.0
# 3.0.0：借条检查器——对每个工具仓的 `src/template` submodule 借条做两条检查。
#
#   ① 指针落后（黄，不阻断）：借条钉住的 commit 落后于模板仓最新
#      ⇒ [LAG]，打印 工具SHA -> 模板SHA；跟不跟由人决定（写 REVIEW）。
#   ② 私改（红，阻断）：绕过借条的本地改动
#      ⇒ [LOCAL-MOD]     借条工作树有未提交改动；
#      ⇒ [POINTER-MOVED] 借条实际 HEAD ≠ 记录 gitlink（静默移指针）。
#
# 退出码：仅「私改」红灯阻断（exit 1）；指针落后 / 尚未 submodule 化为黄或信息，exit 0。
#
# 用法：
#   python sync_check.py                     # 检查与模板仓同级、含 src/template 的各工具仓
#   python sync_check.py --roots dsh-helper  # 只查指定工具仓

import argparse
import subprocess
import sys
from pathlib import Path

try:  # Windows 控制台默认 GBK，中文判定标签会变乱码
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

TEMPLATE_DIR = Path(__file__).resolve().parent   # 模板仓根（借条的被引方）
PARENT = TEMPLATE_DIR.parent                       # 各工具仓的父目录（如 my_diy_tools/）
SUBMODULE = "src/template"                          # 工具侧借条落地目录（import 面 template.*）


def git(repo: Path, *args: str) -> str:
    """在 repo 里跑 git，返回 stdout（去空白）；失败返回空串。"""
    r = subprocess.run(["git", "-C", str(repo), *args],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return (r.stdout or "").strip()


def default_roots() -> list[str]:
    """与模板仓同级、且含 src/template 的目录即候选工具仓。"""
    out = []
    for p in sorted(PARENT.iterdir()):
        if p.is_dir() and p.name != TEMPLATE_DIR.name and (p / "src" / "template").exists():
            out.append(p.name)
    return out


def gitlink_sha(tool: Path) -> str | None:
    """工具 HEAD 中 src/template 的 gitlink（mode 160000）SHA；非借条返回 None。"""
    line = git(tool, "ls-tree", "HEAD", SUBMODULE)   # 形如 "160000 commit <sha>\tsrc/template"
    if line.startswith("160000 commit"):
        return line.split()[2]
    return None


def check_tool(name: str) -> tuple[bool, list[str]]:
    """检查单个工具仓。返回 (是否红灯, 输出行)。"""
    tool = PARENT / name
    if not (tool / ".git").exists():
        return False, [f"[skip] {name}: 非 git 仓，跳过"]

    sha = gitlink_sha(tool)
    if sha is None:
        return False, [f"[migrate] {name}: src/template 非 submodule 借条（尚未迁移）——"
                       f"Wave 2 迁移前属预期，非红灯"]

    sub = tool / SUBMODULE
    if not sub.exists():
        return False, [f"[uninit] {name}: 借条已登记但工作树未初始化"
                       f"（补救：git submodule update --init {SUBMODULE}）"]

    lines: list[str] = []
    red = False

    # —— 职责② 私改（红，阻断）——
    dirty = git(sub, "status", "--porcelain")
    if dirty:
        red = True
        lines.append(f"[LOCAL-MOD] {name}: 借条工作树有未提交改动（绕过借条的私改）")
        for ln in dirty.splitlines()[:10]:
            lines.append(f"          {ln}")
    sub_head = git(sub, "rev-parse", "HEAD")
    if sub_head and sub_head != sha:
        red = True
        lines.append(f"[POINTER-MOVED] {name}: 借条 HEAD {sub_head[:8]} ≠ 记录 gitlink {sha[:8]}"
                     f"（静默移指针 = 私改）")

    # —— 职责① 指针落后（黄，不阻断）——
    tpl_head = git(TEMPLATE_DIR, "rev-parse", "HEAD")
    if not red:
        if sha == tpl_head:
            lines.append(f"[ok] {name}: 借条 @ {sha[:8]} = 模板仓最新，工作树干净")
        else:
            lines.append(f"[LAG] {name}: 借条钉住 {sha[:8]} 落后于模板仓最新 {tpl_head[:8]}"
                         f" —— 该升级未升级（黄，跟不跟由人定）")

    return red, lines


def main() -> int:
    ap = argparse.ArgumentParser(description="submodule 借条检查：指针落后→黄 / 私改→红")
    ap.add_argument("--roots", nargs="*", default=None,
                    help="要检查的工具仓目录名（默认：与模板仓同级且含 src/template 的目录）")
    args = ap.parse_args()
    roots = args.roots if args.roots is not None else default_roots()

    any_red = False
    for name in roots:
        red, out_lines = check_tool(name)
        any_red = any_red or red
        for ln in out_lines:
            print(ln)

    print(f"\n结果：{'红——存在绕过借条的私改，阻断（exit 1）' if any_red else '绿——无阻断项（黄灯不阻断，exit 0）'}")
    return 1 if any_red else 0


if __name__ == "__main__":
    sys.exit(main())
