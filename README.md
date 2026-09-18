# my_diy_tools 模板库总文档（拷贝式 · 单一事实源分工）

> **去重原则**：规范性条款（必须/禁止/判级）的唯一家是 [`../TOOL_DEVELOPMENT.md`](../TOOL_DEVELOPMENT.md)；
> 本目录只放**操作层**——模块接口、采纳步骤、模板代码。两者冲突时以 TOOL_DEVELOPMENT 为准并回改这里。

## 目录结构

```
_template\
  README.md            ← 本文档：标准索引 + 拼接指南
  sync_check.py        ← T10 漂移检查（构建门禁的一个闸）
  REVIEW.md            ← 三轮复审机制 + 对应关系矩阵 + 复审记录
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
| [baseline](modules/baseline/README.md) (T11) | README 双语/CHANGELOG/LICENSE/.gitignore | A1 基线 7/8、G5 | reme/local-speak2text | 全部四工具 |

## 新工具拼接指南（从零到发布）

1. **定级**：对照 TOOL_DEVELOPMENT §A 全表逐条过（别只看触发列——基线 8 这类挂在
   "开源/交付他人"下的条目最容易漏，2026-09-18 实测翻过车）；
2. **必拷**：`modules/appconfig/`（填参数）+ `modules/paths/`；
3. **按需选模块**：托盘工具 → `tray_kit` + `log_kit` + `autostart` + `build_release`；
   公开发布 → `baseline`（双语 README）+ `update_helper`；要图标 → `icons`；双语 UI → `i18n`；
4. 每个拷贝文件**顶部加**：`# TEMPLATE-FROM: _template/modules/<模块>/<文件> | TEMPLATE-VER: <模板版本>`；
   有意定制改加 `# TEMPLATE-LOCAL-OVERRIDE: <原因>`；
5. `main()` 装配顺序：单实例 → paths.seed → 日志 → 自启自愈 → 托盘（D14 八段）→ 更新检查；
6. build.bat 门禁加 sync_check 闸（本地；CI 检出不含 _template，跑不了）；
7. `--smoke` 写上、CHANGELOG 开张、tag `v<semver>` 发版。

## 同步与复审（摘要有意短，细节各自成文）

- **模板升级**：改 `modules/<x>/` → 升该文件 `TEMPLATE-VER` → 各工具跑 sync_check →
  逐工具独立 commit + 门禁绿 + semver 判级（先报后动，push 是用户决定权）；
- **三轮复审**：R1 机械比对 / R2 语义对照 / R3 回归验证——机制、矩阵与记录见
  [REVIEW.md](REVIEW.md)。模板升位后必跑三轮；工具发版前至少跑 R1。

## 两条红线（全文最短、违者必翻车）

1. **实例隔离**：测试/工具链实例必须 `<APP>_DATA_DIR` 重定向独立数据区，
   严禁与常驻实例共享任何落盘文件（F11 血案）；
2. **路径只出自 T2**：任何模块禁止自己拼 config/log/update 路径。
