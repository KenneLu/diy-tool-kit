# tray_icons — 托盘状态贴图运行时加载

运行时**只加载资产、零绘制代码**。资产由构建期 `icons.make_state_icons`
产出为 `resources/icons/<state>/<size>.png`（按档存帧——resize 状态角标会偏移）。

## 消费方装配

```python
from template.tray_icons import tray_icons
tray_icons.init(config_icon_dir=CFG.get("icon_dir"))   # 启动一次
icon = pystray.Icon(...)
tray_icons.bind(icon, "default")
# 状态变化处：
tray_icons.set_state("running")   # 去重；同状态重复调用零闪动
```

### 初态必须来自当前业务状态（1.8.8 教训，强制）

`bind()` 的 `initial_state` **不得硬编码默认图**：它必须按“此刻已经解析出来的业务
状态”计算（例如 `running if phase == "running" else "stopped"`）。

为什么：典型启动顺序是“先刷新一次状态 → 再建托盘”。如果刷新时已经接管了一个正在
运行的服务（phase=running），那次刷新往往已经把新签名记进 `MenuSignature`；托盘建好
后状态不再变化 ⇒ 重建不会被触发 ⇒ 图标永久停在初态。硬编码 `stopped` 就会得到
“菜单显示运行中、图标却是灰的”这种自相矛盾的界面（dsh-helper 1.8.5–1.8.7 实测）。

判据：`tray_icons.get(bind 时传入的 state)` 渲染出的图，必须与同一时刻菜单首行显示的
状态一致。消费方测试应直接断言“初态函数”在 running/stopped 下的返回值。

## API

| 函数 | 语义 |
|---|---|
| `init(config_icon_dir=None)` | 解析目录优先级：config `icon_dir` > APP_DIR/resources/icons > 打包内置（_MEIPASS）；同名状态图高优先级覆盖 |
| `get(state, size=None)` | 取帧（(state,size) 双键缓存；size 缺省按 DPI 选档 `pick_size()`）；缺图回退 default，永不抛（回退日志每状态一次） |
| `pick_size(scale_hint=None)` | `max(16, 32*scale/96)` 取 `TRAY_FRAMES` 最近档 |
| `bind(pystray_icon, initial_state)` | 绑定图标对象并设初态 |
| `set_state(state)` | 去重换图（返回是否真的切了） |

## 与 icons.py（构建工具）的分工

`icons` 在构建期**生成**全套状态帧（`make_state_icons`，工具经 appconfig 提供
`ICON_STATE_ARTISTS` 状态绘制器表）；`tray_icons` 在运行时**加载**。包内不发行
任何绘制代码。

## 断言（消费方测试，test_i18n_keys 同款手法）

`ICON_STATES 键集 == 资产目录状态集`（防"状态定义了没生成/生成了没定义"漂移）。
