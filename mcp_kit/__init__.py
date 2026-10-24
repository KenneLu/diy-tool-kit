# -*- coding: utf-8 -*-
# TEMPLATE-MODULE: mcp_kit | TEMPLATE-VER: 1.0.0
"""mcp_kit｜模型上下文协议服务公共层。

工具只写一个薄适配模块：定义工具、提示词、资源清单和三个回调，然后调用
`serve(config)`。协议处理、错误响应、提示词/资源读取都留在这里。
"""
from .server import ServerConfig, serve

__all__ = ["ServerConfig", "serve"]
