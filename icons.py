# -*- coding: utf-8 -*-
# TEMPLATE-FROM: _template/icons.py | TEMPLATE-VER: 1.0.0
"""T6｜代码生成双 ico（蓝本 local-speak2text/icons.py）。

图标由代码画出来（appconfig.ICON_DRAW），构建时喂给 PyInstaller——仓库里不进
二进制图标资源。write_app_icons 一次生成托盘 ico（多尺寸帧）+ 任务栏小 ico。
"""
import argparse

from PIL import Image, ImageDraw

from appconfig import APP_ID, ICON_DRAW


def make_image(size=64, **style):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    ICON_DRAW(d, size, **style) if _accepts_style() else ICON_DRAW(d, size)
    return img


def _accepts_style():
    import inspect
    return len(inspect.signature(ICON_DRAW).parameters) > 2


def write_app_icons(out_dir="."):
    tray_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    frame = make_image(256)
    # PIL 的 ICO 多尺寸帧：save 一次带 sizes 即可
    frame.save(out_dir + f"/{APP_ID}.ico", format="ICO", sizes=tray_sizes)
    small = make_image(24).resize((24, 24))
    small.save(out_dir + f"/{APP_ID}-taskbar.ico", format="ICO", sizes=[(16, 16), (24, 24)])
    return {"tray": out_dir + f"/{APP_ID}.ico", "taskbar": out_dir + f"/{APP_ID}-taskbar.ico"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"generate {APP_ID} icons")
    parser.add_argument("--out", default=".")
    args = parser.parse_args()
    print(write_app_icons(args.out))
