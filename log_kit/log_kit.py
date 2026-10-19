# -*- coding: utf-8 -*-
# TEMPLATE-MODULE: log_kit | TEMPLATE-VER: 1.0.5
# 1.0.5：日志初始化彻底 fail-safe：目录创建/滚动/普通文件处理器全部失败时退化为
#   NullHandler，并把原因记入 LAST_INIT_ERROR；`open_log_dir` 同样吞异常。
#   此前「滚动失败→FileHandler」的回退在文件被占用时两者都失败，异常会逃到模块导入，
#   直接崩掉助手启动（2026-10-19 用户实测；工具侧已各自兜底，本版把承诺落到模板层）。
# 1.0.4：模块互引改双式导入（try modules. / except template.）；收尾步统一。
# 1.0.3：`log` 改 **print 形态**（`def log(*parts)`，空格拼接 `str(part)`）。
#   根因是**契约冲突**：`update_helper`（同批派发件）里 7 处按 print 形态调用
#   （`log("downloading", stem)` / `log("update staged:", a, "->", b, "(bat %s)" % s)`），
#   而这里给的是单参闭包 → 传进来的那一刻就在**每条真路径上** TypeError
#   （L407 每次下载 / L257 每次拉起替换脚本 / L390 有失败 marker 时）。
#   为什么以前没炸：dsh/ocx 各自在工具侧写了 `def log(*parts)` 兜住（且都留了
#   "模板 log_kit 待统一"的注释）；l-s2t 的包装更窄（`def log(message)`），
#   **却照样 `log=log` 交给了模板件** → 真缺陷（已实测：传进 launch_pending_cmd /
#   pop_failed_update_note 时，模板件 L257 / L390 直接 TypeError）。
#   **冲突被三份互不相同的本地包装分别盖住 / 藏住**，模板层面于是长期保持
#   "两个派发件说不同的话"。统一到 print 形态：与 `update_helper` / `tray_kit` 的
#   调用形态一致，也与 `print` 直觉一致；工具侧的本地包装可以退化成直接转发或删除。
"""log_kit｜运行日志：RotatingFileHandler 单文件 1MB、保留 3 个滚存（总量 ~4MB 封顶）。

参数与 reme-helper 的日志方案一致（house 标准）：日志跟数据区走
%LOCALAPPDATA%\\<工具名>\\log\\，托盘「打开日志目录」一键到达。
任何日志失败都静默——日志永远不能把主流程弄死。
"""
import os

from template.appconfig import APP_ID

LOG_MAX_BYTES = 1 << 20      # 1 MB per file
LOG_BACKUPS = 3              # <app>.log.1 ... .3

_logger = None
# 最近一次初始化失败的原因（成功为空串）。工具想在崩溃日志里交代“日志为什么没写”时读它；
# 不读也不影响任何行为——初始化失败已退化为 NullHandler，绝不把主流程弄死。
LAST_INIT_ERROR = ""

def get_logger(log_dir):
    global _logger, LAST_INIT_ERROR
    if _logger is None:
        import logging
        from logging.handlers import RotatingFileHandler

        lg = logging.getLogger(APP_ID)
        if not lg.handlers:
            handler = None
            try:
                log_dir.mkdir(parents=True, exist_ok=True)
                try:
                    handler = RotatingFileHandler(
                        log_dir / (APP_ID + ".log"),
                        maxBytes=LOG_MAX_BYTES,
                        backupCount=LOG_BACKUPS,
                        encoding="utf-8",
                    )
                except Exception:
                    # 升级窗口期另一实例还开着日志文件时改名会失败（Windows）：
                    # 宁可这一轮不滚，也不要因为日志装不上而启动失败（reme-helper 语义，1.0.2 沉淀）
                    handler = logging.FileHandler(
                        log_dir / (APP_ID + ".log"), encoding="utf-8")
            except Exception as exc:
                # 1.0.5：目录不可建 / 两次打开都失败（文件被另一实例占用等）也绝不外抛，
                # 退化为 NullHandler；启动继续，原因留给 LAST_INIT_ERROR 与调用方自报。
                LAST_INIT_ERROR = "%s: %s" % (type(exc).__name__, exc)
                handler = logging.NullHandler()
            try:
                handler.setFormatter(
                    logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
            except Exception:
                pass
            lg.addHandler(handler)
            lg.setLevel(logging.INFO)
            lg.propagate = False
        _logger = lg
    return _logger

def make_logger(log_dir):
    """返回 (log, open_log_dir) 两个闭包；工具初始化时调用一次。

    `log` 是 **print 形态**：接受任意个位置参数，用空格拼接（1.0.3 起的稳定承诺）。
    `update_helper` / `tray_kit` 都按这个形态调用；log-accepts-varargs 会机械检查工具传给模板件的
    日志函数能否接受可变参数。
    """
    logger = get_logger(log_dir)

    def log(*parts):
        try:
            logger.info(" ".join(str(part) for part in parts))
        except Exception:
            pass

    def open_log_dir():
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
            os.startfile(str(log_dir))  # noqa: S606
        except Exception:
            # 1.0.5：目录不可建/系统没注册打开程序时也不能在产品里抛异常
            pass

    return log, open_log_dir
