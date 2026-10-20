# TEMPLATE-MODULE: log_kit | TEMPLATE-VER: 1.0.5
from .log_kit import *  # noqa: F401,F403

# `from .log_kit import *` 会把 LAST_INIT_ERROR 的**导入时快照**（空串）绑到包上，
# 而它会在初始化失败后被实现模块改写。这里删掉快照、改为实时委托，避免调用方
# 读到“永远为空”的假信号（1.0.5 包门面遗漏；工具侧 log_failopen 测试在英文 CI 上
# 依赖这个信号，2026-10-20 实测）。
globals().pop("LAST_INIT_ERROR", None)


def __getattr__(name):
    from . import log_kit as _impl

    if name == "LAST_INIT_ERROR":
        return getattr(_impl, name)
    raise AttributeError("module %r has no attribute %r" % (__name__, name))


def last_init_error():
    """实时读取最近一次日志初始化失败原因（空串 = 正常）。"""
    from . import log_kit as _impl

    return getattr(_impl, "LAST_INIT_ERROR", "")
