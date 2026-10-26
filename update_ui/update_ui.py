# -*- coding: utf-8 -*-
# TEMPLATE-MODULE: update_ui | TEMPLATE-VER: 1.0.1
"""update_ui｜统一更新交互：下载进度弹窗 → 下载完成 → 立即更新 / 稍后更新。

为什么在模板：四个工具的「下载并更新」原本各自弹气泡/甚至没有反馈（点了像没反应）。
交互与文案必须统一，且**只能有一份实现**，否则每个工具都会慢慢长出自己的分支。

流程（``run_download_dialog`` 一次模态完成）：

1. 打开即显示「正在下载更新…」+ 进度条（服务端给了 Content-Length 就是确定进度，
   否则不确定动画）；下载中实时刷新百分比 / 已下载字节。
2. 下载到 100% 后显示「下载完成，正在校验并准备更新…」。
3. 准备完成：进度条满格，标题变为「更新已下载完成」，出现「立即更新 / 稍后更新」两个
   按钮，并明确说明：**更新需要退出本软件后才能应用**。
   - 立即更新 → 返回 ``"apply"``（调用方负责走退出路径并拉起 pending 替换脚本）；
   - 稍后更新 / 关窗 → 返回 ``"later"``（pending 脚本保留，下次退出时自动执行）；
   - 下载失败 → 弹窗内显示错误 + 「关闭」，返回 ``None``。

线程契约：**必须在拥有 Tk 的线程调用**（工具的 ui_post / UI 队列负责封送）。``download``
回调在后台线程执行；对话框用 ``after()`` 轮询结果队列，Tk 对象不跨线程。

``screenshot_dir=`` 只给**本地视觉验收**用（自动截「下载中」「已完成」两态然后自动关窗），
CI/门禁不要传：测试不得产生真实窗口副作用。
"""
import queue
import threading
import tkinter as tk
from pathlib import Path
from tkinter import ttk

STRINGS = {
    "zh": {
        "title": "{app} 更新",
        "downloading": "正在下载更新…",
        "preparing": "下载完成，正在校验并准备更新…",
        "downloaded": "更新已下载完成",
        "progress": "{percent}%（{done} / {total}）",
        "progress_unknown": "正在下载更新…（已下载 {done}）",
        "progress_done": "100%",
        "download_hint": "下载完成后可选择「立即更新」或「稍后更新」；更新需要退出本软件后才能应用。",
        "hint": (
            "更新文件已就绪，但需要退出本软件后才能应用。\n"
            "· 点「立即更新」：立即退出软件，自动替换文件并重新启动。\n"
            "· 点「稍后更新」：继续使用当前版本，下次退出软件时自动执行更新。"
        ),
        "apply": "立即更新",
        "later": "稍后更新",
        "close": "关闭",
        "error": "下载更新失败：{detail}",
        "wait": "下载中，请稍候…",
    },
    "en": {
        "title": "Update {app}",
        "downloading": "Downloading update…",
        "preparing": "Download complete — verifying and preparing the update…",
        "downloaded": "Update downloaded",
        "progress": "{percent}% ({done} / {total})",
        "progress_unknown": "Downloading update… ({done} downloaded)",
        "progress_done": "100%",
        "download_hint": "When the download finishes you can choose Apply now or Later; the update needs the app to quit before it can be applied.",
        "hint": (
            "The update has been downloaded but cannot be applied while this app is running.\n"
            "· Apply now: quit the app immediately; files are replaced and the app restarts.\n"
            "· Later: keep using the current version; the update runs the next time you quit."
        ),
        "apply": "Apply now",
        "later": "Later",
        "close": "Close",
        "error": "Update download failed: {detail}",
        "wait": "Downloading, please wait…",
    },
}


def _mb(num):
    try:
        num = float(num)
    except (TypeError, ValueError):
        return "?"
    if num >= 1024 * 1024:
        return "%.1f MB" % (num / (1024 * 1024))
    if num >= 1024:
        return "%.0f KB" % (num / 1024)
    return "%.0f B" % num


def format_progress(done, total, lang="zh"):
    """进度文案（纯函数，便于无 UI 回归断言）。"""
    table = STRINGS.get(lang) or STRINGS["zh"]
    if total and total > 0:
        percent = max(0, min(100, int(done * 100 / total)))
        return table["progress"].format(percent=percent, done=_mb(done), total=_mb(total))
    return table["progress_unknown"].format(done=_mb(done))


def _center(root, width, height):
    root.update_idletasks()
    screen_w = root.winfo_screenwidth()
    screen_h = root.winfo_screenheight()
    x = max(0, (screen_w - width) // 2)
    y = max(0, (screen_h - height) // 3)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))


def _grab(root, out_dir, name, log):
    """本地视觉验收截图（仅当调用方传了 screenshot_dir）。"""
    try:
        from PIL import ImageGrab
        root.update_idletasks()
        x, y = root.winfo_rootx(), root.winfo_rooty()
        w, h = root.winfo_width(), root.winfo_height()
        img = ImageGrab.grab(bbox=(x - 10, y - 36, x + w + 10, y + h + 10))
        img.save(str(Path(out_dir) / name))
        log("screenshot:", str(Path(out_dir) / name))
    except Exception as exc:  # noqa: BLE001 - 截图失败绝不影响更新流程
        log("screenshot failed:", exc)


def _apply_window_icon(root, icon, log):
    """把弹窗标题栏图标换成各工具自己的图标（.ico 或 .png；失败不影响更新流程）。"""
    if not icon:
        return
    try:
        path = Path(str(icon))
        if path.suffix.lower() == ".ico":
            root.iconbitmap(default=str(path))
        else:
            image = tk.PhotoImage(file=str(path))
            root.iconphoto(True, image)
            root._update_ui_icon_ref = image   # 防 PhotoImage 被回收 → 标题栏空白
    except Exception as exc:  # noqa: BLE001 - 换图标失败绝不影响更新
        log("window icon skipped:", exc)


def run_download_dialog(download, *, lang="zh", app_name="", parent=None, log=print,
                        icon=None, screenshot_dir=None):
    """模态更新对话框。返回 ``"apply"`` / ``"later"`` / ``None``（失败或关窗）。

    download(progress) 在后台线程执行；progress(done, total) 由本模块转成进度条。
    ``icon=``：标题栏图标（各工具自己的 .ico/.png；缺省保留 Tk 默认图标）。
    必须在 Tk 线程调用（内部自己 ``mainloop()``，对话框关闭后返回）。
    """
    table = STRINGS.get(lang) or STRINGS["zh"]
    shots = Path(screenshot_dir) if screenshot_dir else None
    if shots is not None:
        shots.mkdir(parents=True, exist_ok=True)

    root = tk.Tk() if parent is None else tk.Toplevel(parent)
    root.withdraw()
    root.title(table["title"].format(app=app_name or ""))
    _apply_window_icon(root, icon, log)
    root.resizable(False, False)
    try:
        root.attributes("-topmost", True)
    except tk.TclError:
        pass

    frame = ttk.Frame(root, padding=18)
    frame.pack(fill="both", expand=True)
    status_var = tk.StringVar(value=table["downloading"])
    pct_var = tk.StringVar(value="")
    detail_var = tk.StringVar(value=table["download_hint"])

    ttk.Label(frame, textvariable=status_var, font=("Microsoft YaHei UI", 11, "bold")).pack(
        anchor="w")
    bar = ttk.Progressbar(frame, mode="indeterminate", length=470)
    bar.pack(fill="x", pady=(10, 4))
    bar.start(12)
    ttk.Label(frame, textvariable=pct_var, foreground="#555555").pack(anchor="w")
    ttk.Label(frame, textvariable=detail_var, wraplength=470, justify="left",
              foreground="#444444").pack(anchor="w", pady=(10, 0))

    buttons = ttk.Frame(frame)
    buttons.pack(fill="x", pady=(14, 0))
    btn_apply = ttk.Button(buttons, text=table["apply"])
    btn_later = ttk.Button(buttons, text=table["later"])
    btn_close = ttk.Button(buttons, text=table["close"])

    state = {"phase": "downloading", "decision": None, "determinate": False,
             "shot_running": False, "shot_done": False}
    result_q = queue.Queue()

    def do_apply():
        state["decision"] = "apply"
        root.destroy()

    def do_later():
        if state["decision"] is None:
            state["decision"] = "later"
        root.destroy()

    btn_apply.configure(command=do_apply)
    btn_later.configure(command=do_later)
    btn_close.configure(command=do_later)

    def show_done_buttons():
        btn_apply.pack(side="left")
        btn_later.pack(side="left", padx=(10, 0))

    def show_close_button():
        btn_close.pack(side="left")

    def on_close():
        if state["phase"] == "downloading":
            status_var.set(table["wait"])
            return
        do_later()

    root.protocol("WM_DELETE_WINDOW", on_close)

    def poll():
        if not root.winfo_exists():
            return
        try:
            while True:
                kind, payload = result_q.get_nowait()
                if kind == "progress":
                    done, total = payload
                    if total and total > 0:
                        percent = max(0, min(100, int(done * 100 / total)))
                        if not state["determinate"]:
                            bar.stop()
                            bar.configure(mode="determinate", maximum=100)
                            state["determinate"] = True
                        bar["value"] = percent
                        pct_var.set(format_progress(done, total, lang))
                    else:
                        pct_var.set(format_progress(done, 0, lang))
                    if (shots is not None and not state["shot_running"]
                            and state["phase"] == "downloading"
                            and (not total or done * 2 >= total)):
                        state["shot_running"] = True
                        _grab(root, shots, "01-downloading.png", log)
                elif kind == "done":
                    state["phase"] = "done"
                    bar.stop()
                    bar.configure(mode="determinate", maximum=100)
                    bar["value"] = 100
                    status_var.set(table["downloaded"])
                    pct_var.set(table["progress_done"])
                    detail_var.set(table["hint"])
                    show_done_buttons()
                    if shots is not None and not state["shot_done"]:
                        state["shot_done"] = True
                        root.after(200, lambda: _grab(root, shots, "02-downloaded.png", log))
                        root.after(1200, do_later)   # 本地视觉验收：截完自动关窗
                elif kind == "error":
                    state["phase"] = "error"
                    bar.stop()
                    bar.configure(mode="determinate", maximum=100)
                    bar["value"] = 0
                    status_var.set(table["error"].format(detail=payload))
                    pct_var.set("")
                    show_close_button()
        except queue.Empty:
            pass
        root.after(80, poll)

    def worker():
        try:
            def progress(done, total):
                result_q.put(("progress", (done, total)))
            download(progress)
            result_q.put(("done", None))
        except Exception as exc:  # noqa: BLE001 - 任何失败都要显示在同一个弹窗里
            result_q.put(("error", str(exc)))

    _center(root, 520, 250)
    root.deiconify()
    try:
        root.grab_set()
    except tk.TclError:
        pass
    threading.Thread(target=worker, name="update-download", daemon=True).start()
    root.after(80, poll)
    if parent is None:
        root.mainloop()
    else:
        # parent=(Toplevel) 时不能 mainloop()（Toplevel 没有这个方法）；wait_window 在
        # 已存在的 Tk 解释器里跑**嵌套事件循环**，同样模态，且不会跟工具的常驻 mainloop 打架。
        root.wait_window(root)
    try:
        root.destroy()
    except tk.TclError:
        pass
    return state["decision"]
