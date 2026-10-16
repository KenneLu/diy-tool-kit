# my-diy-tool-template —— 家族工具模板库与开发流程框架（拷贝式）

> **规范与实现**：本仓是托盘/GUI 小工具的共享模块库。
> 工程规范正文见 **[托盘工具工程规范.md](托盘工具工程规范.md)**（能力分级 / 工程纪律 / 界面 / 数据 / 发布 / 判据工程 / 过程纪律 / 坑清单），执行时依此。
> 各模块目录（如 `appconfig/`、`paths/`）是规范对应的**实现件**（模块超详细文档 + 模板代码）。
> 规范与实现冲突时：以 托盘工具工程规范.md 为准，回改实现并登记；文档与磁盘冲突时改文档或改代码，禁止并存。

## 目录结构

```
my-diy-tool-template\
  README.md              ← 本文档：标准索引 + 拼接指南
  托盘工具工程规范.md ← 工程规范正文（A–K 分节）
  sync_check.py          ← 借条检查（指针落后→黄 / 私改→红，构建门禁的一个闸）
  CHANGELOG.md / LICENSE / .gitignore
  <模块名>\
    README.md          ← 该模块的超详细文档（接口/采纳/坑）
    <代码文件>          ← 一份可直接拷贝的模板代码
```

## 模块索引（选型表）

| 模块 | 能力 | 规范出处 | 蓝本 | 现役用户 |
|---|---|---|---|---|
| [appconfig](appconfig/README.md) | 参数区：唯一要改的文件 | F2 | — | dsh、opencodex |
| [paths](paths/README.md) | 数据区/播种/稳定位/**数据根重定向** | F1 | local-speak2text | （dsh/ocx 内联等构，见 REVIEW 矩阵） |
| [autostart](autostart/README.md) | 自启三件套（Run 键名参数化） | G4.1 | —（基线已归模板正本） | dsh、opencodex、local-speak2text、reme |
| [update_helper](update_helper/README.md) | 在线更新三段式（含 marker 语义） | G4、H6 | — | dsh、opencodex、local-speak2text、reme （字节级一致） |
| [i18n](i18n/README.md) | 轻量中英双表 | E4、A2-i18n | local-speak2text | local-speak2text（完整版蓝本） |
| [icons](icons/README.md) | 代码生成双 ico | G5 | local-speak2text | local-speak2text |
| [tray_kit](tray_kit/README.md) | 单实例/--quit/token 掩码/签名重画/三循环 | E2 | reme + local-speak2text | （机制以蓝本内联形态服役） |
| [build_release](build_release/README.md) | 门禁构建 + tag 发版链 | D1、G3/G4、H | local-speak2text | dsh、opencodex（工作流变体）、local-speak2text |
| [log_kit](log_kit/README.md) | 滚动日志 1MB×3 + 打开日志目录 | — | reme-helper | local-speak2text（dsh/ocx 内联等构） |
| [baseline](baseline/README.md) | README 双语/CHANGELOG/LICENSE/.gitignore | A1 基线 7/8、G5 | reme/local-speak2text | 家族内各工具 |
| [service_link](service_link/README.md) | 服务唯一性/接入/有界清理（状态机） | G4.2 | reme（探测+managed 语义）、dsh（接管设计） | opencodex、reme（已接入） |
| [tunnel_kit](tunnel_kit/README.md) | ssh 反向隧道统一（三层探测/退避自愈/N=3 确认/OWNED-only 停止） | — | opencodex、reme（前内联形态） | opencodex、reme |

> **"现役用户/蓝本"列的目标态（2026-09-18 用户定，§公共模板库 原则③）**：四个工具**全部**
> 消费模板（`src/template/<模块>/` 整文件夹采纳，路径统一）；"蓝本""内联等构"都是迁移中的
> 临时形态——工具与模板合不上时，优先优化模板的接口与架构，不给工具留豁免。

## 新工具拼接指南（从零到发布）

1. **定级**：对照 §能力分级总表 全表逐条过（别只看触发列——基线 8 这类挂在
   "开源/交付他人"下的条目最容易漏，2026-09-18 实测翻过车）；
   **收尾时对照 §2 全表逐行自查**，每行给出 `文件:行号` 证据；
2. **必拷**：`appconfig/`（填参数）+ `paths/`；
3. **按需选模块**：托盘工具 → `tray_kit` + `log_kit` + `autostart` + `build_release`；
   公开发布 → `baseline`（双语 README）+ `update_helper`；要图标 → `icons`；双语 UI → `i18n`；
4. 每个拷贝文件**顶部加**：`# TEMPLATE-FROM: my-diy-tool-template/<模块>/<文件> | TEMPLATE-VER: <模板版本>`；
   有意定制改加 `# TEMPLATE-LOCAL-OVERRIDE: <原因>`；
5. `main()` 装配顺序：单实例 → paths.seed → 日志 → 自启自愈 → 托盘（八段）→ 更新检查；
6. build.bat 门禁加 sync_check 闸（本地；CI 检出不含 my-diy-tool-template，跑不了）；
7. `--smoke` 写上、CHANGELOG 开张、tag `v<semver>` 发版。

## 同步与复审（摘要有意短，细节各自成文）

- **通用经验的内化来源**：见 [托盘工具工程规范.md](托盘工具工程规范.md)（通用工程规范的落点）。

- **模板升级**：改 `template/<x>/` → 升该文件 `TEMPLATE-VER` → 各工具跑 sync_check →
  逐工具独立 commit（**每个 commit 前验证修改有效**）+ 门禁绿 + semver 判级
  （+0.0.1 可自判；**+0.1 / +1 仅用户确认**——；push 是用户决定权）；
  **日常维护一般不发版，commit 累计较多才集中发版**，发版前必须人工功能回归；
- **三轮复核**：机械比对 / 语义对照 / 回归验证——机制见 [托盘工具工程规范.md](托盘工具工程规范.md) 的「复核方法论」。模板升位后必跑三轮；工具发版前至少跑机械比对（三轮之一）。

## 两条红线（全文最短、违者必翻车）

1. **实例隔离**：测试/工具链实例必须 `<APP>_DATA_DIR` 重定向独立数据区，
   严禁与常驻实例共享任何落盘文件（血案）；
2. **路径只出自 paths**：任何模块禁止自己拼 config/log/update 路径。
