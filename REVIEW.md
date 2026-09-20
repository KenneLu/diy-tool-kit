# 三轮复审机制（家族内各工具 ↔ 模板一一对应保障）

> 目标：模板与家族内各工具的代码**对应关系可机器验证、可人工追责、可回归复验**。
> 原则：不为抽象而抽象——能一致的一致，因业务特性必须分叉的**申报留痕**，不强改
> （颗粒度护栏）；同时**全量模板化不搞特殊**（2026-09-18 用户定，STANDARDS B4 原则③）——
> 四工具一律往模板收敛，合不上优先改模板接口，豁免名单只减不增。
>
> **逐条符合度看 [CONFORMANCE.md](CONFORMANCE.md)**（76 条 × 四工具状态矩阵 + 检查命令）；
> 本文件只管"三轮怎么跑、跑了什么"。R1 机械比对 = `sync_check.py` + CONFORMANCE §5.1 清单。

## 一、对应关系矩阵（现状，更新本表 = 复审的一部分）

| 模块 | reme-helper | local-speak2text | dsh-helper | opencodex-helper |
|---|---|---|---|---|
| T1 appconfig | **src/modules/appconfig 副本（param；W-f）** | 蓝本（paths.py 内联） | **src/modules/appconfig 整文件夹（param）** | **src/modules/appconfig 整文件夹（param）** |
| T2 paths | **src/modules/paths 副本（OVERRIDE：dev RUN_DIR=仓库根；W-f）** | **paths.py 蓝本复制** | **src/modules/paths 副本 == 模板 1.1.1** | **同 dsh** |
| T3 autostart | 内联（OVERRIDE 申报：APP_ID 键名 + sync_autostart_path 修复语义） | main.py 三件套（蓝本正身） | main.py reg 版等构（声明） | main.py reg 版等构（声明） |
| T4 update_helper | 内联（OVERRIDE 申报：bat+备份目录链路，行为差异大） | updater.py 变体（稳定位形态，蓝本） | **src/modules/update_helper 副本 == 模板 1.0.1** | **同 dsh** |
| T5 i18n | **src/modules/i18n 重形态模块 + pairs.json（OVERRIDE：与轻量 T5 不同构；W-f）** | **src/modules/i18n 副本 == 模板 2.1.0** | ⏳ 未启用（T1 触发条件已满足，待办） | ⏳ 同左 |
| T6 icons | 内联（OVERRIDE 申报：运行态着色 vs 构建期静态） | **icons.py 蓝本复制** | assets png（未触发改造，声明） | 无（代码画圆） |
| T7 tray_kit | **src/modules/tray_kit 副本·mutex 机制（OVERRIDE：显式互斥名；W-f）+ 签名/退出留 main** | main.py 内联等构（单实例/ui_q）；**无 `--quit`**（2026-09-19 更正：本行曾称 l-s2t 是 `--quit` 蓝本，磁盘无此机制）+ 互斥体名非法致启动误报（CONFORMANCE SINGLE-01/02） | **src/modules/tray_kit 副本 == 模板 1.0.1** | **同 dsh** |
| T8/T9 build_release | 蓝本（build+release+CI 全套） | **build.bat/release.bat/workflows 正身** | build.bat + workflows 变体（含 sync_check 闸、--paths src） | 同 dsh |
| T10 sync_check | 不适用（被审方） | 不适用（蓝本豁免，临时态） | **build.bat 门禁闸** | **build.bat 门禁闸** |
| T12 log_kit | **src/modules/log_kit 副本（OVERRIDE：root-logger 形态；W-f）** | **log_kit.py 蓝本复制** | **src/modules/log_kit 副本 == 模板 1.0.2** | **同 dsh** |
| T11 baseline | README 双语/CHANGELOG 全齐 | 全齐 | ✅ 1.7.0 补齐 + 双语 | ✅ 1.1.0 补齐 + 双语 |
| service_link（G4.2） | 语义已接入 1.2.4（勾选持久化 + only_attached 有界清理）；**模块预置，状态机接线待办**（含 ADOPTED 优雅 API，REVIEW #8） | main.py 内联等构（接管设计） | ⏳ 待接入 | ⏳ 待接入（且退出签名击杀需按 G4.2 改造） |

形态图例：**副本** = 与模板归一化一致的拷贝（sync_check [ok]）；`（param）` = 参数文件豁免；
`（声明）` = 内联等构，已在 REVIEW 备案，不强制抽文件；`蓝本` = 该工具是模板的来源，sync_check 豁免。

## 二、三轮定义

| 轮 | 名称 | 做什么 | 通过标准 | 何时跑 |
|---|---|---|---|---|
| **R1** | 机械比对 | ① `python my-diy-tool-template/sync_check.py`（全工具）；② 模板全部 .py `py_compile`；③ 各工具编译门禁 | 0 未申报漂移、0 缺失模板；编译全绿 | 模板或工具**每次相关提交后**（CI 自动覆盖大半）；发版前必跑 |
| **R2** | 语义对照 | 逐模块读"工具实现 ↔ 模板 README 的接口承诺"：签名一致？行为一致？`（声明）`的偏差是否仍然成立？待办（如 T5）是否该升级？ | 矩阵与现实无出入；发现即登记 | 模板 TEMPLATE-VER 升位后；工具大改后 |
| **R3** | 回归验证 | 各工具自己的门禁/测试真跑一遍（l-s2t 测试+lang-audit；dsh/ocx import+更新逻辑+build.bat；reme-helper 测试套件+lang-audit）；**+ 人工功能回归（D16 发版闸：自动化不可替代）**；文档 ↔ 现实抽查 | 各工具绿 + **人工回归通过**；抽查 3 条文档描述与磁盘一致 | 工具发版前必跑；每月例行一轮 |

## 三、记录（每轮一行起，只追加不删改）

| 日期 | 轮 | 范围 | 结果 | 发现与处置 | 执行者 |
|---|---|---|---|---|---|
| 2026-09-18 | R1 | 全家族工具 + 全部模块 | ✅ | sync_check：0 漂移 / 0 申报偏差 / 2 参数文件；模板 9 文件 py_compile 绿；本日完成接口化——dsh/ocx 的 update_helper 从"申报偏差"升级为"归一化一致" | AI |
| 2026-09-18 | R2 | 10 模块 | ✅（2 项登记） | ① dsh/ocx 的 T5 i18n 触发条件已满足（公开仓库）但未实现 → 登记待办，按需排期；② dsh/ocx 的 T2/T3/T12 内联等构**保留现状**（不为抽象而抽象：拆文件收益低、自由度重要），需要微调时直接改工具内联代码 | AI |
| 2026-09-18 | R3 | 3 工具（reme-helper 当日已随 v1.2.3 全套 CI 绿） | ✅ | dsh/ocx：py_compile + import + 更新逻辑（dsh 真实查到 v1.7.0）绿；l-s2t：py_compile + i18n 断言绿（当日 v1.2.0 CI 全绿佐证） | AI |
| 2026-09-18 | R1+R2+R3 | W1 模板升级（i18n v2 数据驱动 / paths 回填 / autostart 参数化）+ W2–W4 四工具接口化重构 | ✅ 全绿 | sync_check：dsh/ocx 的 update_helper/paths/log_kit/tray_kit 归一化一致、appconfig param；l-s2t i18n v2 74 词条 JSON 断言绿；dsh/ocx py_compile+import+更新逻辑绿；三工具已 tag 发版（1.3.0/1.8.0/1.2.0） | AI |
| 2026-09-18 | R1+R2 | W-e/W-f 收尾 + reme 全量模板化（文档三裁决后） | ✅ 全绿 | sync_check 全家族 0 漂移（模板红灯→dsh/ocx 副本同步→归零，"接口不动实现换血"首次实战：log_kit 1.0.2 回退分支 / tray_kit 1.0.1 探测函数 / i18n 2.1.0 向上查找）；reme：--smoke PASS、8 套件绿、lang-audit missing=0；l-s2t/dsh 冻结冒烟 PASS；reme 冻结冒烟留版本号落定后（W-g） | AI |
| 2026-09-19 | R1+R2+R3（新增 CONFORMANCE 层） | 四工具 76 条款全量审计（9 智能体，含对抗复核）+ l-s2t 首轮整改 | ✅ 审计完成；l-s2t 修复后 **1 FAIL / 2 WARN**（修前 5 FAIL）；全门禁绿 | **根因**：l-s2t 单实例互斥体名 `Local\<app>\SingleInstance` 含第二个反斜杠 → `CreateMutexW` 恒失败 → 被当成"已有实例" → 自 1.2.0 起完全无法启动，而 --smoke 绕过守卫使三层防护全绿。已修：合法命名 + 失败放行 + 两个新回归套件进 GATE 2b + `_DATA_DIR` 数据根重定向 + 冒烟双 env 隔离 + 测试注册表备份还原 + README 切换行 + 词表补 2 键。**新增 CONFORMANCE.md（76 条款矩阵）与 conformance_check.py（20 项机械检查，首版修掉 6 处误判）**。未做：C-12 菜单签名重画（需 GUI 目视）、T4/T5 自检命令、T7 guide、E2-06 --quit | AI |

| 2026-09-19 | R2 | 语言菜单文案统一（`menu_language` → `English / 中文`） | ✅ 全绿 | 用户裁定：语言切换项应**直接列出两个语言名**（reme 形态），不用 "Language 语言" 这类功能名。模板 `modules/i18n/README.md` 采纳步骤 3 已改，并**逐字节重拷** dsh/ocx/l-s2t 三份副本；三家 `locales/{zh,en}.json` 的 `menu_language` 值同步统一（每仓 2 文件各 1 行，**行尾剖面不变**：dsh/ocx 保持 LF、l-s2t 保持 CRLF）。`sync_check` 0 undeclared drift / 0 doc byte-diff。reme 本来就是该形态（蓝图），未动。**产物生效需重建**（并入下一波，本波不构建） | AI |

| 2026-09-20 | R1+R2+R3（**新增四批**：内化 / 脱敏 / 行文 / 清理） | **模板仓自身**（全是文档，未动 `modules/**`） | ✅ | ① **内化**：把四工具开发经验与「多主体协作过程本身」凝练进 `STANDARDS §K`／`§L`／`§D3.5`／`§D9`、`CONFORMANCE §4.1.62–66`、`§9.1–§9.7`；`§9` 现为完整对应体系 —— **「无落点亦无丢弃理由」= 0**。② **脱敏**：全仓去个人绝对路径／机器名／内网 IP／用户名；**独立第二判据实测残留 0**（⚠ 首轮报的「残留 0」是**自证循环**：替换表与自检**共用同一个错模式** ⇒ 实测真残留 **47 处**，已修）。③ **行文**：`§K`／`§L` 各补一览表；`§K` 箭头 **17.1** vs `§J` **15.4**（同体裁同区间）；`§L` **24.4** 是「正文逐字保留」保真约束下的**下界**，不是缺陷。④ **清理**：以「见 ＜某文档＞ §X」整类句式重扫 61 处 ⇒ **第一类对第二类的「内容外包」= 0**；第二类已移出视野（**改名，非硬删**，留反悔窗口）。⚠ **本轮三次自伤，均已入条文**：取词面窄于被核对象（×3）、「改完不重测同一个量」（`§K` 16.7→21.4→17.1）、归一化编辑后不回读被归一化的那一层（×2，靠数字节发现）| AI |

## 四、发现登记簿（跨轮待办）

| # | 发现 | 处置 | 状态 |
|---|---|---|---|
| 7 | **发布动作完成却未汇报/未记录**（v1.2.4 于 13:10-13:13 已 commit/push/tag/Release，次轮报告仍称"待发版"，并向用户提出已作废的 A/B 问题）——过程记忆断裂 | 流程纪律：**发布/推送动作完成的当轮，必须在回复与文档中同步状态**；纳入 REVIEW R3 检查项 | ✅ 纪律已立 |
| 8 | reme-helper 退出清理走"按接入 pid 终止"，G4.2 条款 3 的首选路径（服务优雅关闭 API）未接 | 待办：接入 graceful 分支 | ⏳ 待办 |
| 9 | dsh CHANGELOG 的 Unreleased 条目（双语 README）未随 1.8.0 转正 | **已随 1.8.0 转正**（dsh `d74ed1b`，2026-09-19 13:19:58 +0800，commit message 明写 "the stray Unreleased block is folded into 1.8.0 (DOC-08)"）；本轮只读复核确认，未改版本号（D4） | ✅ 已结 |
| 5 | helper 类退出语义：G4.2 新规范（唯一性/接入/有界清理）+ service_link 模板已就绪；reme-helper 退出勾选（默认不清理，持久化）按此实现 → 判级 +0.1 → 1.3.0 | ✅ 已落地并发布 v1.2.4（2026-09-18；判级实际为 +0.0.1——退出语义变化经用户验证后按补丁级发布） | 已结 |
| 6 | opencodex-helper `kill_target_procs` 按命令行签名无差别击杀隧道进程（含外部手起的），违反 G4.2 条款 3 | **可达条件（ocx `e34a7cd` 2026-09-19 17:17:05 +0800 取证）**：5 处调用、**无定时器 / 无启动路径 / 无后台自动路径**，全部需**用户显式动作**——`main.py:284`（`start_target`，仅 `:280` 探测为假 + 用户点启动）、`:316`/`:320`（`stop_target`，用户点停止）、`:566`（删除确认框点是）、`:695`（`on_quit` 的 `if stop_tunnels:` 分支，用户勾选「同时停服务」）；默认退出分支只 terminate OWNED 句柄。与 **#45**（口令型目标探测假阴性 ⇒ 冷启动杀在用隧道）**同路径**。<br>**R-EVID 附注（本次复核实测）**：上列行号是**取证修订 `e34a7cd`** 的；当前工作树因后续提交整体位移为 `297`/`320`/`324`/`570`/`714`——**数量一致（5 处）**，语义对应。**行号必须连修订号一起引用**，否则会像本条一样"对不上却各自都对"。 | ✅ 已结（ocx `ed53b50`，2026-09-20：删去命令行签名扫场，只终止 OWNED 句柄；G4.2 条款 3） |
| 1 | dsh/ocx UI 文案中文硬编码，T1 触发条件（开源发布）已满足 | 排期接入 T5 i18n 模板 | ⏳ 待办 |
| 2 | dsh/ocx/l-s2t 的 T2/T3/T12 以内联等构形态服役 | ~~保留（不为抽象而抽象）~~ **2026-09-18 转向**：用户裁定全量模板化不搞特殊（STANDARDS B4 原则③）——收敛为 `src/modules/` 模块副本（颗粒度护栏仍适用）；剩余项归执行文档 W-e/W-f | ♻️ 已转向 |
| 3 | reme-helper 不消费模板（7924 行单体是诸蓝本之源） | ~~维持蓝本定位~~ **2026-09-18 被用户裁决推翻**：四工具一律模板化（原则③/D6）——reme 纳入消费范围，`src/modules/` 整文件夹补齐 = 执行文档 W-f（判级 +0.1 待确认）；小步推进、每步门禁+人工回归 | ♻️ 已转向 |
| 4 | 模板库目录未推远端 | 用户拍板（D5） | ⏳ 待用户 |
