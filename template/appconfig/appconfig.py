# -*- coding: utf-8 -*-
# TEMPLATE-MODULE: appconfig | TEMPLATE-VER: 1.0.2
"""T1｜工具参数区：拷贝模板后**唯一允许（也需要）修改的文件**。

工具差异只允许存在于一处（house 标准 D6 / D15）：
  APP_ID        机器标识（目录名/互斥体/日志名），小写连字符，如 "dsh-helper"
  APP_NAME      展示名（托盘/弹窗标题），可中文
  AUTOSTART_KEY 开机自启的 HKCU Run 键名（T3 autostart 消费；默认 = APP_NAME。
                reme 覆盖为 APP_ID——其 APP_NAME 是中文展示名，注册表键名须 ASCII）
  VERSION       三段 semver（执行文档 D15：日常 +0.0.1，大功能 +0.1，方向性 +1）
  REPO_OWNER / REPO_NAME   GitHub 仓库（更新器用）
  EXE_NAME      打包产物 exe 文件名（更新器替换目标）
  ICON_DRAW(size) -> PIL.Image   托盘图标绘制函数（T6 icons.py 以 ICON_DRAW(256) 调用）
  ICON_ASSET     png 路径或 None 手工资产（T6，与 ICON_DRAW 二选一，ICON_ASSET 优先）

1.0.2（W4，随 autostart 1.2.0）：新增 `AUTOSTART_KEY`——Run 键名参数化，差异进参数件。
1.0.1：修正自相矛盾——原先注释写 `ICON_DRAW(ctx, size)` 且未定义 ICON_ASSET，
而 icons.py 2.0.0 实际 `from modules.appconfig import APP_ID, ICON_DRAW, ICON_ASSET`
并以 `ICON_DRAW(256)` **单参**调用。现与 icons.py 正本对齐（参数文件，无级联）。
"""
APP_ID = "my-helper"
APP_NAME = "My Helper"
AUTOSTART_KEY = APP_NAME
VERSION = "1.0.0"

REPO_OWNER = "your-github-id"
REPO_NAME = "my-helper"
EXE_NAME = "my-helper.exe"

ICON_ASSET = None   # 手工 png（相对仓库根）；与 ICON_DRAW 二选一，非 None 时优先


def ICON_DRAW(size):
    """默认图标：圆形占位，返回 PIL.Image。工具应替换成自己的图形。

    与 T6 `icons.py` 的契约：单参 size → Image（参考 local-speak2text 的 draw_mic）。
    """
    from PIL import Image, ImageDraw
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(img).ellipse((4, 4, size - 4, size - 4), fill=(76, 175, 80, 255))
    return img
