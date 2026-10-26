# diy-tool-kit —— DIY 工具模板：公共模块多工具复用 + 一致性检查

> 原名 `my-diy-tool-template`，2026-10-19 更名为 **`diy-tool-kit`**（旧地址自动跳转）。

> DIY 小工具（托盘/GUI/命令行）的**共享模块库**：一套公共模块，多个工具以 **git submodule 借条**复用——
> 改一次、全家生效，不再有 N 份拷贝的人工同步。一致性由 `sync_check.py`（借条检查）把关。

## 快速接入（首屏）

**拉取本库（含子模块）**：

```bash
git clone --recurse-submodules <本库 git 地址>
```

> 忘了 `--recurse-submodules`、模块目录为空？补救：
>
> ```bash
> git submodule update --init
> ```

**在你的工具仓里挂借条**（把公共模块落到 `src/template/`，import 面恒为 `template.*`）：

```bash
git submodule add <本库 git 地址> src/template
```

之后工具业务代码直接 `from template.appconfig import ...`、`from template.paths import ...`——
本库对工具的 import 面完全透明，业务代码一行不改。

## 参数卡（工具差异只住一处）

工具的差异参数（托盘显示名、版本号、图标、GitHub 仓库坐标等）**不改公共模块**，而是写在工具
自持的**参数卡** `src/app_params.py`（放在借条外，工具自己保管）。公共模块 `appconfig` 运行时
`try: import app_params` 读取覆盖；无参数卡时用出厂默认值（kit 自身始终可独立 import）。

```python
# src/app_params.py（示例）
APP_ID = "my-tool"
APP_NAME = "我的工具"
VERSION = "1.0.0"
```

可覆盖键与默认值见 [appconfig](appconfig/README.md)。

## 仓库内容

- **代码**：12 个公共模块（位于仓库根）+ 2 个模板自有件（[baseline](baseline/README.md) 仓库基线规范、
  [build_release](build_release/README.md) 构建脚手架，内含 `version_file.py` 版本元数据写入器）+ 各模块 README。
- **验收**：[ota_test/](ota_test/README.md) —— 模板自带的本地 OTA 验收测试（无网络/无真应用）；
  工具仓构建与 CI 直接调用。
- **规范**：[docs/README.md](docs/README.md)（公共规范 + 工具类型规范索引）+ 本 README + [CHANGELOG.md](CHANGELOG.md)。旧版综合规范保留在 [docs/归档/](docs/归档/)。
- **检查**：[sync_check.py](sync_check.py)（借条检查）。

## 模块索引

| 模块 | 能力 |
|---|---|
| [appconfig](appconfig/README.md) | 参数区（参数卡机制：出厂默认值 + `app_params` 覆盖） |
| [paths](paths/README.md) | 数据区 / 播种 / 稳定位 / 数据根重定向 |
| [autostart](autostart/README.md) | 自启三件套（Run 键名参数化） |
| [update_helper](update_helper/README.md) | 在线更新三段式（查→下→换，含 marker 语义；包根按内容解析、路径不带版本号） |
| [mcp_kit](mcp_kit/README.md) | 模型上下文协议服务公共层（协议循环 + 生成器 + 薄适配） |
| [i18n](i18n/README.md) | 轻量中英双表 |
| [icons](icons/README.md) | 代码生成双 ico |
| [tray_kit](tray_kit/README.md) | 单实例 / `--quit` / token 掩码 / 签名重画 / 三循环 |
| [tray_icons](tray_icons/README.md) | 托盘状态贴图运行时加载 |
| [log_kit](log_kit/README.md) | 滚动日志 1MB×3 + 打开日志目录 |
| [service_link](service_link/README.md) | 服务唯一性 / 接入 / 有界清理（状态机） |
| [tunnel_kit](tunnel_kit/README.md) | ssh 反向隧道统一（三层探测 / 退避自愈 / OWNED-only 停止） |
| [baseline](baseline/README.md) | 仓库基线件规范（双语 README / CHANGELOG / LICENSE / .gitignore） |
| [build_release](build_release/README.md) | 门禁构建 + tag 发版链 |

## 一致性检查（sync_check）

`sync_check.py` 对每个工具仓的 `src/template` 借条做两条检查（构建门禁的一个闸）：

- **指针落后**（黄，不阻断）：借条钉住的 commit 落后于本库最新 ⇒ `[LAG]`，跟不跟由人定。
- **私改**（红，阻断）：借条工作树有未提交改动 `[LOCAL-MOD]`；或借条 HEAD ≠ 记录 gitlink
  （静默移指针）`[POINTER-MOVED]`。

```bash
python sync_check.py --roots <工具仓名>   # 或不带 --roots，查与本库同级的全部工具仓
```

## 工程规范

规范按“公共规范 + 工具类型”分层，入口见 **[docs/README.md](docs/README.md)**：

- [公共规范](docs/公共规范.md)：所有工具都必须遵守；
- [托盘工具](docs/工具类型/托盘工具.md)：托盘/GUI/自启/更新器/服务/隧道；
- [命令行工具](docs/工具类型/命令行工具.md)：无托盘、按需运行、打包 exe、无 Python 用户环境；
- [归档](docs/归档/)：旧版综合规范，仅作历史参考。

规范与实现冲突时以公共规范为准，回改实现并登记；不采用项必须写明原因和触发条件。

优先级：**公共规范 > 工具类型规范 > 归档参考 > 模块 README**。模块 README 只解释模块自身，不覆盖规范。

迁移与工具对照（含四个既有工具和旧规范映射）见 [docs/迁移与工具对照.md](docs/迁移与工具对照.md)。

## 两条红线（违者必翻车）

1. **实例隔离**：测试 / 工具链实例必须 `<APP>_DATA_DIR` 重定向独立数据区，严禁与常驻实例共享任何落盘文件。
2. **路径只出自 paths**：任何模块禁止自己拼 config / log / update 路径。
