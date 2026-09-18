# -*- coding: utf-8 -*-
# TEMPLATE-MODULE: i18n | TEMPLATE-VER: 1.0.0
"""T5｜轻量 i18n 骨架（蓝本 local-speak2text/i18n.py，重 i18n 见 reme-helper/src/i18n.py，二期）。

zh 键同时充当 key，en 缺失回退中文，永远不会 KeyError。
拷贝后把 _ZH/_EN 换成本工具的词表；键名约定：menu_* / notify_* / tray_* / status_*。
"""
import json
import os

_ZH = {
    "menu_quit": "退出",
    "menu_open_logs": "打开日志目录",
    "menu_check_update": "检查更新",
    "menu_update_now": "立即更新",
}

_EN = {
    "menu_quit": "Quit",
    "menu_open_logs": "Open log folder",
    "menu_check_update": "Check for updates",
    "menu_update_now": "Update now",
}

TABLES = {"zh": _ZH, "en": _EN}
LANG = "zh"


def detect_system_lang():
    try:
        import ctypes
        return "zh" if ctypes.windll.kernel32.GetUserDefaultUILanguage() & 0xFF == 0x04 else "en"
    except Exception:
        return "zh"


def init(language="auto"):
    global LANG
    if language == "auto":
        language = detect_system_lang()
    LANG = language if language in TABLES else "zh"


def t(key, *args):
    text = TABLES.get(LANG, _ZH).get(key) or _ZH.get(key) or key
    if args and "%" in text:
        text = text % args
    return text


def load_language_from_config(config_path):
    try:
        with open(config_path, "r", encoding="utf-8-sig") as f:
            return str(json.load(f).get("language", "auto"))
    except Exception:
        return "auto"


def save_language_to_config(config_path, language):
    try:
        cfg = {}
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8-sig") as f:
                cfg = json.load(f)
        cfg["language"] = language
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
