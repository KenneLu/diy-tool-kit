# -*- coding: utf-8 -*-
"""update_ui 本地视觉验收 demo（不联网、不动安装目录、不启服务）。

用途：在任意借用模板的工具仓里看「下载更新」弹窗的真实效果。模拟一次下载（进度条
走满），截图「下载中」「已完成」两态后自动关窗。CI/门禁不要跑它（会产生真实窗口）。

用法（工具仓根目录）：

    python src\\template\\update_ui\\demo.py
    python src\\template\\update_ui\\demo.py --lang en
    python src\\template\\update_ui\\demo.py --shots .cache\\update-ui
"""
import sys
import time
from pathlib import Path

SCRIPT = Path(__file__).resolve()
TOOL_SRC = SCRIPT.parents[2]
TOOL_ROOT = TOOL_SRC.parent
if not (TOOL_SRC / "template" / "update_ui").is_dir():
    print("update_ui demo: run this from a tool repo that borrows the template")
    raise SystemExit(2)
sys.path.insert(0, str(TOOL_SRC))

from template import update_ui  # noqa: E402

LATEST_SIZE = 17_519_328   # reme-helper 1.2.18 的 zip 实况大小，纯展示用


def simulated_download(progress, total=LATEST_SIZE, steps=40, delay=0.06):
    """假下载：只喂进度，不写任何文件。"""
    for step in range(1, steps + 1):
        progress(int(total * step / steps), total)
        time.sleep(delay)
    time.sleep(0.8)
    return "demo-pending.bat"


def main(argv):
    lang, shots, app_name, icon = "zh", None, "dsh-helper", None
    args = list(argv[1:])
    while args:
        arg = args.pop(0)
        if arg == "--lang" and args:
            lang = args.pop(0)
        elif arg == "--shots" and args:
            shots = args.pop(0)
        elif arg == "--app-name" and args:
            app_name = args.pop(0)
        elif arg == "--icon" and args:
            icon = args.pop(0)
        else:
            print("unknown argument: %r" % arg)
            return 2
    if icon is None:
        candidate = TOOL_ROOT / "resources" / "icons" / "default" / "48.png"
        if candidate.is_file():
            icon = str(candidate)
    decision = update_ui.run_download_dialog(
        simulated_download, lang=lang, app_name=app_name, log=print, icon=icon,
        screenshot_dir=shots)
    print("demo decision:", decision)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
