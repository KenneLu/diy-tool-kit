# -*- coding: utf-8 -*-
# TEMPLATE-MODULE: appconfig | TEMPLATE-VER: 1.0.0
"""T1｜工具参数区：拷贝模板后**唯一允许（也需要）修改的文件**。

工具差异只允许存在于一处（house 标准 D6 / D15）：
  APP_ID        机器标识（目录名/互斥体/日志名），小写连字符，如 "dsh-helper"
  APP_NAME      展示名（托盘/弹窗标题），可中文
  VERSION       三段 semver（执行文档 D15：日常 +0.0.1，大功能 +0.1，方向性 +1）
  REPO_OWNER / REPO_NAME   GitHub 仓库（更新器用）
  EXE_NAME      打包产物 exe 文件名（更新器替换目标）
  ICON_DRAW(ctx, size)     托盘图标绘制函数（画什么图形是工具唯一真正的"个性"）
"""
APP_ID = "my-helper"
APP_NAME = "My Helper"
VERSION = "1.0.0"

REPO_OWNER = "KenneLu"
REPO_NAME = "my-helper"
EXE_NAME = "my-helper.exe"


def ICON_DRAW(d, size):
    """默认图标：圆形占位。工具应替换成自己的图形（参考 local-speak2text/icons.py）。"""
    d.ellipse((4, 4, size - 4, size - 4), fill=(76, 175, 80, 255))
