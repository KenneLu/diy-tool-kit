# my-diy-tool-template —— 家族工具模板库与开发流程框架（拷贝式）

> **四件套框架**（开发新工具 = 按此顺序走完）：
> ① **README**（本文件）——怎么拼：概述引导 + 模块索引 + 拼接指南；
> ② **[STANDARDS.md](STANDARDS.md)**——必须做什么：家族规范正文（能力分级 / 工程纪律 / 界面 / 数据 / 发布 / 坑清单），执行时依此；
> ③ **[CONFORMANCE.md](CONFORMANCE.md)**——做到没有：**76 条原子条款 × 四工具状态矩阵** + 可复现检查命令 + 退出/单实例/服务/命名/文档五张深挖表；
> ④ **[REVIEW.md](REVIEW.md)**——本轮改了什么：三轮复审机制 + 家族工具对应关系矩阵 + 记录。
>
> ⚠ **接手/换班必读**：**[HANDOFF/](HANDOFF/README.md)** —— 交接文件夹（全部交接材料收在一处）：
> - **[HANDOFF/README.md](HANDOFF/README.md)** —— 索引：阅读顺序 + 复量命令 + 哪些证据在哪（**从这里进**）
> - **[HANDOFF/HANDOFF-2026-09-19.md](HANDOFF/HANDOFF-2026-09-19.md)** —— 主封存单：现场状态 / 已完成（勿重做）/ 待办 T1–T13 / **12 个坑** / **明确未验证项**
> - **[HANDOFF/HANDOFF-2026-09-19-TASKLEDGER.md](HANDOFF/HANDOFF-2026-09-19-TASKLEDGER.md)** —— 台账附件：63 条任务索引 + 五个主题的关系 + 核心思路例程 + **18 条关键决策（带理由）**
> - **[HANDOFF/PROMPT-for-next-team.md](HANDOFF/PROMPT-for-next-team.md)** —— 可直接粘贴给下一个 agent team 的交接话术
>
> **它的「坑」比「待办」更重要** —— 坑的形态是"证据是真的、推理是通的、结论是反的"。
> ⚠ 主封存单里的现场数字**几分钟就旧** ⇒ **先跑它的 §1.1 复量命令，不要照着数字规划**。
>
> `modules/<模块>/` 是规范对应的**实现件**（模块超详细文档 + 模板代码）。
> 规范与实现冲突时：以 STANDARDS.md 为准，回改模板并登记 REVIEW；文档与磁盘冲突时改文档或改代码，禁止并存。

## 目录结构

```
my-diy-tool-template\
  README.md            ← 本文档：标准索引 + 拼接指南
  STANDARDS.md         ← 规范正文（A–J 分节）
  CONFORMANCE.md       ← 逐条对照表：76 条款 × 四工具状态 + 检查命令 + 重点域深挖
  REVIEW.md            ← 三轮复审机制 + 对应关系矩阵 + 复审记录
  sync_check.py        ← T10 漂移检查（构建门禁的一个闸）
  conformance_check.py ← 机械判据（C-xx 条款的判据本体）
  HANDOFF\             ← 交接文件夹（接手必读；索引见其 README.md）
  blueprints.txt       ← 蓝本/待对齐工具名单（只减不增）
  CHANGELOG.md / LICENSE / .gitignore
  modules\<模块名>\
    README.md          ← 该模块的超详细文档（接口/采纳/坑）
    <代码文件>          ← 一份可直接拷贝的模板代码
```

## 模块索引（选型表）

| 模块 | 能力 | 规范出处 | 蓝本 | 现役用户 |
|---|---|---|---|---|
| [appconfig](modules/appconfig/README.md) (T1) | 参数区：唯一要改的文件 | F2、D6/D15 | — | dsh、opencodex |
| [paths](modules/paths/README.md) (T2) | 数据区/播种/稳定位/**数据根重定向** | F1、F11/D12 | local-speak2text | （dsh/ocx 内联等构，见 REVIEW 矩阵） |
| [autostart](modules/autostart/README.md) (T3) | 自启三件套 | G4.1 | local-speak2text | 同上 |
| [update_helper](modules/update_helper/README.md) (T4) | 在线更新三段式 | G4、H6 | reme + l-s2t + dsh/ocx | **dsh、opencodex（字节级一致）** |
| [i18n](modules/i18n/README.md) (T5) | 轻量中英双表 | E4、A2-T1 | local-speak2text | local-speak2text（完整版蓝本） |
| [icons](modules/icons/README.md) (T6) | 代码生成双 ico | G5 | local-speak2text | local-speak2text |
| [tray_kit](modules/tray_kit/README.md) (T7) | 单实例/--quit/token 掩码/签名重画/三循环 | E2(D14)、F13 | reme + local-speak2text | （机制以蓝本内联形态服役） |
| [build_release](modules/build_release/README.md) (T8+T9) | 门禁构建 + tag 发版链 | D1、G3/G4、H | local-speak2text | dsh、opencodex（工作流变体）、local-speak2text |
| [log_kit](modules/log_kit/README.md) (T12) | 滚动日志 1MB×3 + 打开日志目录 | D4(D13) | reme-helper | local-speak2text（dsh/ocx 内联等构） |
| [baseline](modules/baseline/README.md) (T11) | README 双语/CHANGELOG/LICENSE/.gitignore | A1 基线 7/8、G5 | reme/local-speak2text | 家族内各工具 |
| [service_link](modules/service_link/README.md) | 服务唯一性/接入/有界清理（状态机） | G4.2 | reme（探测+managed 语义）、dsh（接管设计） | ⏳ 模板就绪，工具接入待排期 |

> **"现役用户/蓝本"列的目标态（2026-09-18 用户定，STANDARDS B4 原则③）**：四个工具**全部**
> 消费模板（`src/modules/<模块>/` 整文件夹采纳，路径统一）；"蓝本""内联等构"都是迁移中的
> 临时形态——工具与模板合不上时，优先优化模板的接口与架构，不给工具留豁免；sync_check
> 的豁免名单（blueprints.txt）只减不增。

## 新工具拼接指南（从零到发布）

1. **定级**：对照 STANDARDS §A 全表逐条过（别只看触发列——基线 8 这类挂在
   "开源/交付他人"下的条目最容易漏，2026-09-18 实测翻过车）；
   **收尾时对照 CONFORMANCE §2 全表逐行自查**，每行给出 `文件:行号` 证据；
2. **必拷**：`modules/appconfig/`（填参数）+ `modules/paths/`；
3. **按需选模块**：托盘工具 → `tray_kit` + `log_kit` + `autostart` + `build_release`；
   公开发布 → `baseline`（双语 README）+ `update_helper`；要图标 → `icons`；双语 UI → `i18n`；
4. 每个拷贝文件**顶部加**：`# TEMPLATE-FROM: my-diy-tool-template/modules/<模块>/<文件> | TEMPLATE-VER: <模板版本>`；
   有意定制改加 `# TEMPLATE-LOCAL-OVERRIDE: <原因>`；
5. `main()` 装配顺序：单实例 → paths.seed → 日志 → 自启自愈 → 托盘（D14 八段）→ 更新检查；
6. build.bat 门禁加 sync_check 闸（本地；CI 检出不含 my-diy-tool-template，跑不了）；
7. `--smoke` 写上、CHANGELOG 开张、tag `v<semver>` 发版。

## 同步与复审（摘要有意短，细节各自成文）

- **模板升级**：改 `modules/<x>/` → 升该文件 `TEMPLATE-VER` → 各工具跑 sync_check →
  逐工具独立 commit（**每个 commit 前验证修改有效**）+ 门禁绿 + semver 判级
  （+0.0.1 可自判；**+0.1 / +1 仅用户确认**——D16；push 是用户决定权）；
  **日常维护一般不发版，commit 累计较多才集中发版**，发版前必须人工功能回归（G3 第 6 条）；
- **三轮复审**：R1 机械比对 / R2 语义对照 / R3 回归验证——机制、矩阵与记录见
  [REVIEW.md](REVIEW.md)。模板升位后必跑三轮；工具发版前至少跑 R1。

## 两条红线（全文最短、违者必翻车）

1. **实例隔离**：测试/工具链实例必须 `<APP>_DATA_DIR` 重定向独立数据区，
   严禁与常驻实例共享任何落盘文件（F11 血案）；
2. **路径只出自 T2**：任何模块禁止自己拼 config/log/update 路径。
