# TEMPLATE-FROM: _template/sync_check.py | TEMPLATE-VER: 1.0.0
# T10｜模板漂移检查（防漂移四件套之一，执行文档 D1）。
#
# 原理：扫描各工具目录里带 `# TEMPLATE-FROM: _template/xxx.py` 头的文件，与模板
# 正本比对哈希；文件头带 `TEMPLATE-LOCAL-OVERRIDE: <原因>` 的是"已申报偏差"，
# 单独列出而非报错。退出码：0=全部一致或已申报；1=存在未申报漂移。
#
# 用法：
#   python _template/sync_check.py                     # 检查 my_diy_tools 下所有工具
#   python _template/sync_check.py --roots dsh-helper opencodex-helper
#
# 蓝本豁免：local-speak2text 是模板的来源（blueprint），在 BLUEPRINT_TOOLS 里登记，
# 不参与比对——它的修改应当"反向沉淀"到模板（升 TEMPLATE-VER）。

import argparse
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent      # my_diy_tools/
TEMPLATE_DIR = Path(__file__).resolve().parent
BLUEPRINT_TOOLS = {"local-speak2text"}             # 模板来源，豁免比对
FROM_RE = re.compile(r"^#\s*TEMPLATE-FROM:\s*_template/([\w./-]+)", re.M)
OVERRIDE_RE = re.compile(r"^#\s*TEMPLATE-LOCAL-OVERRIDE:", re.M)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_tool(tool_dir):
    """返回该工具的 [(tool_file, template_name, declared)] 列表。"""
    found = []
    for py in sorted(tool_dir.rglob("*.py")):
        if ".git" in py.parts or "__pycache__" in py.parts:
            continue
        try:
            head = py.read_text(encoding="utf-8", errors="replace")[:2048]
        except OSError:
            continue
        m = FROM_RE.search(head)
        if not m:
            continue
        declared = bool(OVERRIDE_RE.search(head))
        found.append((py, m.group(1), declared))
    return found


def main():
    parser = argparse.ArgumentParser(description="template drift check")
    parser.add_argument("--roots", nargs="*", default=sorted(
        d.name for d in ROOT.iterdir()
        if d.is_dir() and not d.name.startswith(("_", ".")) and d.name != "__pycache__"
    ), help="tool dirs under my_diy_tools (default: all non-underscore dirs)")
    args = parser.parse_args()

    drift, declared, missing_tpl = [], [], []
    for name in args.roots:
        if name in BLUEPRINT_TOOLS:
            print(f"[skip] {name}: blueprint (template source)")
            continue
        tool_dir = ROOT / name
        if not tool_dir.is_dir():
            print(f"[skip] {name}: no such dir")
            continue
        for tool_file, tpl_name, is_declared in scan_tool(tool_dir):
            template_file = TEMPLATE_DIR / tpl_name
            if not template_file.exists():
                missing_tpl.append((tool_file, tpl_name))
                continue
            if sha256(tool_file) == sha256(template_file):
                print(f"[ok]   {name}/{tool_file.relative_to(tool_dir)} == _template/{tpl_name}")
            elif is_declared:
                declared.append((name, tool_file, tpl_name))
                print(f"[decl ] {name}/{tool_file.relative_to(tool_dir)} deviates from _template/{tpl_name} (declared override)")
            else:
                drift.append((name, tool_file, tpl_name))
                print(f"[DRIFT] {name}/{tool_file.relative_to(tool_dir)} deviates from _template/{tpl_name}")

    print()
    if missing_tpl:
        for f, t in missing_tpl:
            print(f"[MISSING TEMPLATE] {f} references _template/{t}")
    print(f"summary: {len(drift)} undeclared drift, {len(declared)} declared override(s), "
          f"{len(missing_tpl)} missing template(s)")
    if drift or missing_tpl:
        print("fix: apply the template fix to this tool (independent commit + gate green), "
              "or declare TEMPLATE-LOCAL-OVERRIDE with a reason in the file header.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
