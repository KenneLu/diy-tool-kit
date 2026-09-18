# T6 · icons —— 代码生成双 ico

> 规范出处：TOOL_DEVELOPMENT.md §G5。
> 蓝本：local-speak2text/icons.py + reme-helper 的多尺寸帧表。

## 定位

图标由代码绘制（`appconfig.ICON_DRAW`），构建时生成 ico 喂给 PyInstaller——
仓库不进二进制图标资源，改图标 = 改一个函数。

## 对外接口（稳定承诺）

| 名称 | 说明 |
|---|---|
| `make_image(size=64)` | 调 `ICON_DRAW` 画一张 RGBA |
| `write_app_icons(out_dir=".")` | 生成 `<APP_ID>.ico`（托盘态，7 档尺寸帧）+ `<APP_ID>-taskbar.ico`（任务栏态） |
| CLI | `python icons.py --out .` |

## 采纳步骤

1. `appconfig.ICON_DRAW` 画出本工具图形（状态色与运行时托盘绘制同语言）；
2. 构建前跑 `python icons.py`，PyInstaller `--icon <APP_ID>-taskbar.ico`；
3. 交付物检查断言 ico 在发布包里。

## 边界与坑

- 任务栏 ico 要铺满真实索取的像素档（reme-helper 用 15 档覆盖 100%–200% DPI），缺档被外壳缩放会发糊；
- 运行态指示（如 蓝=空闲/橙=录制）与 ico 默认态同一设计语言。
