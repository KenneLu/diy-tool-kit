# update_ui —— 统一更新交互（模板正本）

> 1.0.0（2026-10-26）：四个工具的「下载并更新」原本各自弹气泡/无反馈；本模块把
> **下载进度弹窗 → 下载完成 → 立即更新 / 稍后更新** 收敛成唯一实现与唯一文案。

## 流程（一次模态）

1. 打开即显示「正在下载更新…」+ 进度条（有 `Content-Length` 时确定进度，否则不确定）；
2. 下载中实时刷新百分比与已下载/总大小；
3. 下载到 100% → 「下载完成，正在校验并准备更新…」；
4. 准备完成 → 标题「更新已下载完成」，进度条满格，出现「立即更新 / 稍后更新」；
5. 明确说明：**更新需要退出本软件后才能应用**：
   - 立即更新 → 返回 `"apply"`，调用方退出并拉起 pending 替换脚本；
   - 稍后更新/关窗 → 返回 `"later"`，pending 脚本保留，下次退出时自动执行；
   - 下载失败 → 弹窗内显示错误 + 「关闭」，返回 `None`。

## 用法

```python
from template import update_ui

def download(progress):
    return update_helper.download_and_prepare(
        latest, APP_DIR, UPDATE_DIR, log=log, progress=progress)

decision = ui_post(lambda: update_ui.run_download_dialog(
    download, lang=i18n.current_lang(), app_name=APP_NAME, log=log))
if decision == "apply":
    ...退出并拉起替换脚本...
elif decision == "later":
    ...保留 pending，下次退出执行...
```

- **必须在拥有 Tk 的线程调用**（工具用 `ui_post` / UI 队列封送）；内部自己 `mainloop()`，
  关闭后返回。
- `download(progress)` 在后台线程执行；`progress(done, total)` 由 `update_helper
  .download_and_prepare(progress=...)` 提供（total 可能为 0）。
- `screenshot_dir=` 只给本地视觉验收（自动截「下载中」「已完成」两态并自动关窗），
  **CI/构建门禁不要传**——测试不得产生真实窗口副作用。

## API

| 函数 | 语义 |
|---|---|
| `run_download_dialog(download, *, lang="zh", app_name="", parent=None, log=print, icon=None, screenshot_dir=None)` | 模态对话框；返回 `"apply"` / `"later"` / `None`；`icon=` 传各工具自己的 .ico/.png 作为标题栏图标 |
| `format_progress(done, total, lang="zh")` | 纯函数进度文案（无 UI 可断言） |
| `STRINGS["zh"/"en"]` | 唯一文案表（改文案只改这里，工具不要各自复制） |

## 文案（唯一正本，2026-10-26 用户定）

- 下载中：`正在下载更新…` + `{n}%（{done} / {total}）`
- 完成：`更新已下载完成`
- 说明：更新需要退出本软件后才能应用；「立即更新」立即退出并自动替换重启；
  「稍后更新」继续使用，下次退出时自动执行。

## 本地看效果

工具仓里跑（任意借用模板的仓）：

```bat
python src\template\update_ui\demo.py --lang zh --shots .cache\update-ui
```

会打开真实弹窗、模拟一次下载（进度条走满），自动截图两态后关窗；截图在
`--shots` 目录。**不产生任何服务/安装目录副作用。**

## 不覆盖

- 网络/校验/替换逻辑：属于 `update_helper`；
- 失败回滚：属于替换 bat（`update_helper.build_apply_script`）；
- 版本检查与“有新版才可点”：由工具菜单状态控制。
