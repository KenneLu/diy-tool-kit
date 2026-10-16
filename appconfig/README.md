# appconfig —— 参数区（参数卡机制）

## 定位

工具之间的全部差异参数收敛到**一处参数卡**。kit 侧 `appconfig.py` 只放**出厂默认值**、
保持可独立 import；每个工具自持一张参数卡 `src/app_params.py`（放在借条外，工具自己保管）。
运行时 `appconfig` 执行 `try: import app_params` 读取覆盖——无参数卡则沿用出厂默认值。

业务代码 `from template.appconfig import APP_ID, ...` **一行不改**；工具差异只住在参数卡里。

## 参数卡机制

kit 侧 `appconfig.py` 形如：

```python
# 出厂默认值（kit 独立可用）
APP_ID = "my-helper"
APP_NAME = "My Helper"
AUTOSTART_KEY = APP_NAME
...

# 运行时覆盖（可选）
try:
    import app_params as _card
except ImportError:
    _card = None
if _card is not None:
    APP_ID = getattr(_card, "APP_ID", APP_ID)
    ...
```

工具侧 `src/app_params.py` **只写要覆盖的键**，未写的键保留出厂默认值。

## 对外接口（稳定承诺）

| 名称 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `APP_ID` | str | ✅ | 机器标识：数据目录名 / 互斥体 / 日志文件名 / 更新包名前缀。小写连字符 |
| `APP_NAME` | str | ✅ | 展示名（托盘 title、弹窗标题），可中文 |
| `VERSION` | str | 按工具 | 三段 semver |
| `REPO_OWNER` / `REPO_NAME` | str | 更新器需要 | GitHub `owner/repo`，update_helper 消费 |
| `EXE_NAME` | str | 更新器需要 | 打包产物 exe 名。**不带版本号**（自启注册表存完整路径） |
| `AUTOSTART_KEY` | str | 可选 | 开机自启 HKCU Run 键名。**默认 = `APP_NAME`**（动态跟随）；参数卡显式给则用之 |
| `ICON_DRAW(size)` | callable | 二选一 | 图标绘制函数：**单参** size → `PIL.Image`（icons 以 `ICON_DRAW(256)` 调用） |
| `ICON_ASSET` | str \| None | 二选一 | 手工 png 路径；非 None 时**优先于** `ICON_DRAW`。与 `ICON_DRAW` 至少给一个 |
| `ICON_STATE_ARTISTS` | dict \| None | 可选 | 状态绘制器表 `[状态名 → callable(base256) -> Image256]`。默认 `None`，icons 消费 |

## 采纳步骤

1. 在工具仓挂借条：`git submodule add <模板仓地址> src/template`（公共模块落到 `src/template/`）；
2. 写工具自持的参数卡 `src/app_params.py`，填上表字段（**只给要覆盖的键**）；
3. 业务代码 `from template.appconfig import ...` 取用——无需改动。

## 边界与坑

- 业务密码 / 密钥**永不入内**（凭据单独文件且不入库）。
- 一个字段两处定义 = 迟早漂移：新增参数先问「是不是所有工具都该有」，是 → 改 kit 与本文档；
  否 → 放工具自己的配置。
- `AUTOSTART_KEY` 默认跟随 `APP_NAME`：只覆盖 `APP_NAME` 时它自动跟随；需固定 ASCII 键名时显式给。
