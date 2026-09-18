# 三轮复审机制（家族内各工具 ↔ 模板一一对应保障）

> 目标：模板与家族内各工具的代码**对应关系可机器验证、可人工追责、可回归复验**。
> 原则：不为抽象而抽象——能一致的一致，因业务特性必须分叉的**申报留痕**，不强改。

## 一、对应关系矩阵（现状，更新本表 = 复审的一部分）

| 模块 | reme-helper | local-speak2text | dsh-helper | opencodex-helper |
|---|---|---|---|---|
| T1 appconfig | 蓝本（常量区内联） | 蓝本（paths.py 内联） | **appconfig.py 副本（param）** | **appconfig.py 副本（param）** |
| T2 paths | 蓝本（内联四区） | **paths.py 蓝本复制** | main.py 内联等构（声明） | main.py 内联等构（声明） |
| T3 autostart | 蓝本（sync_autostart_path 路线） | main.py 三件套（蓝本正身） | main.py reg 版等构（声明） | main.py reg 版等构（声明） |
| T4 update_helper | 蓝本（内联更新链） | updater.py 变体（稳定位形态，蓝本） | **副本 == 模板（归一化一致）** | **副本 == 模板（归一化一致）** |
| T5 i18n | 蓝本（重形态） | **i18n.py 蓝本复制** | ⏳ 未启用（T1 触发条件已满足，待办） | ⏳ 同左 |
| T6 icons | 蓝本（write_app_icon） | **icons.py 蓝本复制** | assets png（未触发改造，声明） | 无（代码画圆） |
| T7 tray_kit | 蓝本（三循环/签名/自愈正身） | main.py 内联等构（单实例/ui_q） | main.py 内联等构（互斥体/N7 掩码） | main.py 内联等构 |
| T8/T9 build_release | 蓝本（build+release+CI 全套） | **build.bat/release.bat/workflows 正身** | build.bat + workflows 变体（含 sync_check 闸） | 同 dsh |
| T10 sync_check | 不适用（被审方） | 不适用（蓝本豁免） | **build.bat 门禁闸** | **build.bat 门禁闸** |
| T12 log_kit | 蓝本（1MB×3 参数出处） | **log_kit.py 蓝本复制** | main.py 内联等构（声明） | main.py 内联等构（声明） |
| T11 baseline | README 双语/CHANGELOG 全齐 | 全齐 | ✅ 1.7.0 补齐 + 双语 | ✅ 1.1.0 补齐 + 双语 |

形态图例：**副本** = 与模板归一化一致的拷贝（sync_check [ok]）；`（param）` = 参数文件豁免；
`（声明）` = 内联等构，已在 REVIEW 备案，不强制抽文件；`蓝本` = 该工具是模板的来源，sync_check 豁免。

## 二、三轮定义

| 轮 | 名称 | 做什么 | 通过标准 | 何时跑 |
|---|---|---|---|---|
| **R1** | 机械比对 | ① `python my-diy-tool-template/sync_check.py`（全工具）；② 模板全部 .py `py_compile`；③ 各工具编译门禁 | 0 未申报漂移、0 缺失模板；编译全绿 | 模板或工具**每次相关提交后**（CI 自动覆盖大半）；发版前必跑 |
| **R2** | 语义对照 | 逐模块读"工具实现 ↔ 模板 README 的接口承诺"：签名一致？行为一致？`（声明）`的偏差是否仍然成立？待办（如 T5）是否该升级？ | 矩阵与现实无出入；发现即登记 | 模板 TEMPLATE-VER 升位后；工具大改后 |
| **R3** | 回归验证 | 各工具自己的门禁/测试真跑一遍（l-s2t 测试+lang-audit；dsh/ocx import+更新逻辑+build.bat；reme-helper 测试套件+lang-audit）；文档 ↔ 现实抽查 | 各工具绿；抽查 3 条文档描述与磁盘一致 | 工具发版前必跑；每月例行一轮 |

## 三、记录（每轮一行起，只追加不删改）

| 日期 | 轮 | 范围 | 结果 | 发现与处置 | 执行者 |
|---|---|---|---|---|---|
| 2026-09-18 | R1 | 全家族工具 + 全部模块 | ✅ | sync_check：0 漂移 / 0 申报偏差 / 2 参数文件；模板 9 文件 py_compile 绿；本日完成接口化——dsh/ocx 的 update_helper 从"申报偏差"升级为"归一化一致" | AI |
| 2026-09-18 | R2 | 10 模块 | ✅（2 项登记） | ① dsh/ocx 的 T5 i18n 触发条件已满足（公开仓库）但未实现 → 登记待办，按需排期；② dsh/ocx 的 T2/T3/T12 内联等构**保留现状**（不为抽象而抽象：拆文件收益低、自由度重要），需要微调时直接改工具内联代码 | AI |
| 2026-09-18 | R3 | 3 工具（reme-helper 当日已随 v1.2.3 全套 CI 绿） | ✅ | dsh/ocx：py_compile + import + 更新逻辑（dsh 真实查到 v1.7.0）绿；l-s2t：py_compile + i18n 断言绿（当日 v1.2.0 CI 全绿佐证） | AI |

## 四、发现登记簿（跨轮待办）

| # | 发现 | 处置 | 状态 |
|---|---|---|---|
| 1 | dsh/ocx UI 文案中文硬编码，T1 触发条件（开源发布）已满足 | 排期接入 T5 i18n 模板 | ⏳ 待办 |
| 2 | dsh/ocx/l-s2t 的 T2/T3/T12 以内联等构形态服役 | 保留（不为抽象而抽象）；下次大改时顺手换成模块副本 | ♾️ 备案 |
| 3 | reme-helper 不消费模板（7924 行单体是诸蓝本之源） | 维持蓝本定位；D12-A"另立项目"时再做模块化 | ♾️ 备案 |
| 4 | 模板库目录未推远端 | 用户拍板（D5） | ⏳ 待用户 |
