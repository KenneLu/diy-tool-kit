# -*- coding: utf-8 -*-
# TEMPLATE-MODULE: appconfig | TEMPLATE-VER: 2.0.0
# 2.0.0：参数卡机制——出厂默认值 + 运行时读取工具侧 app_params 覆盖（拷贝模式→submodule 引用）
"""appconfig｜工具参数区（参数卡机制）。

kit 出厂默认值留在本文件，kit 自身**始终可独立 import**（无参数卡不崩、用默认值）。
每个工具自持一张参数卡 `src/app_params.py`（放在借条外，工具自己保管）：
appconfig 运行时 `try: import app_params`，导入成功则用参数卡覆盖默认值，
导入失败（kit 独立使用 / 无参数卡）则沿用出厂默认值。

工具业务代码 import 一行不改：仍 `from template.appconfig import APP_ID, ...`。

参数卡可覆盖键（与出厂默认值一一对应）：
  APP_ID        机器标识（目录名/互斥体/日志名），小写连字符
  APP_NAME      展示名（托盘/弹窗标题），可中文
  VERSION       三段 semver
  REPO_OWNER / REPO_NAME   GitHub 仓库（更新器用）
  EXE_NAME      打包产物 exe 文件名（更新器替换目标）
  AUTOSTART_KEY 开机自启 HKCU Run 键名；**默认 = APP_NAME**，参数卡未显式给则跟随覆盖后的 APP_NAME
  ICON_DRAW(size) -> PIL.Image   托盘图标绘制函数（icons.py 以 ICON_DRAW(256) 调用）
  ICON_ASSET    png 路径或 None 手工资产（与 ICON_DRAW 二选一，ICON_ASSET 优先）
  ICON_STATE_ARTISTS  dict[状态名, callable(base256)->Image256]；默认 None，icons 消费
"""

# ===================== 出厂默认值（kit 独立可用） =====================
APP_ID = "my-helper"
APP_NAME = "My Helper"
VERSION = "1.0.0"

REPO_OWNER = "your-github-id"
REPO_NAME = "my-helper"
EXE_NAME = "my-helper.exe"

AUTOSTART_KEY = APP_NAME   # 默认 = APP_NAME；参数卡可覆盖

ICON_ASSET = None          # 手工 png（相对仓库根）；与 ICON_DRAW 二选一，非 None 时优先
ICON_STATE_ARTISTS = None  # 状态绘制器表；工具以参数卡提供，icons 消费


def ICON_DRAW(size):
    """默认图标：圆形占位，返回 PIL.Image。工具应替换成自己的图形。

    与 `icons.py` 的契约：单参 size → Image（参考 local-speak2text 的 draw_mic）。
    """
    from PIL import Image, ImageDraw
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(img).ellipse((4, 4, size - 4, size - 4), fill=(76, 175, 80, 255))
    return img


# ===================== 参数卡覆盖（工具侧 app_params，可选） =====================
try:
    import app_params as _card
except ImportError:
    _card = None

if _card is not None:
    # 标量 / 对象参数：参数卡有定义则覆盖，否则保留出厂默认值
    APP_ID = getattr(_card, "APP_ID", APP_ID)
    APP_NAME = getattr(_card, "APP_NAME", APP_NAME)
    VERSION = getattr(_card, "VERSION", VERSION)
    REPO_OWNER = getattr(_card, "REPO_OWNER", REPO_OWNER)
    REPO_NAME = getattr(_card, "REPO_NAME", REPO_NAME)
    EXE_NAME = getattr(_card, "EXE_NAME", EXE_NAME)
    ICON_ASSET = getattr(_card, "ICON_ASSET", ICON_ASSET)
    ICON_STATE_ARTISTS = getattr(_card, "ICON_STATE_ARTISTS", ICON_STATE_ARTISTS)

    # ICON_DRAW：参数卡提供绘制函数则覆盖
    if hasattr(_card, "ICON_DRAW"):
        ICON_DRAW = _card.ICON_DRAW

    # AUTOSTART_KEY：参数卡显式给则用之；否则跟随（覆盖后的）APP_NAME
    AUTOSTART_KEY = getattr(_card, "AUTOSTART_KEY", APP_NAME)

del _card
