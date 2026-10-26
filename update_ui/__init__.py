# -*- coding: utf-8 -*-
"""update_ui 包门面：统一更新交互的 Tk 实现（与 update_helper 的下载/暂存解耦）。"""
from .update_ui import STRINGS, format_progress, run_download_dialog

__all__ = ["STRINGS", "format_progress", "run_download_dialog"]
