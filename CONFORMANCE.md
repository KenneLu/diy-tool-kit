# CONFORMANCE.md —— 家族工具规范符合度对照表（模板库三件套之"对照"）

> **定位**：`STANDARDS.md` 回答"必须做到什么"，本文件回答"**具体到每一条，模板件在哪、四个工具现在什么状态、怎么机械验证、差多少、怎么补**"。
> 三件套职责：**README**（怎么拼）→ **STANDARDS**（必须做什么）→ **CONFORMANCE**（本条做到没有）→ **REVIEW**（本轮改了什么）。
>
> 2026-09-19 建立。起因：l-s2t 1.4.0 的 exe 从 1.2.0 起就无法启动（单实例守卫误报），
> 自检、门禁、review 三层全绿却无人发现——**因为"该检查什么"散落在 536 行散文规范里，
> AI 每次执行都会漏**。本表把规范拆成 76 条带编号的原子条款 + 五张重点域深挖表，
> 每行都必须能回答"凭什么说它符合/不符合"。

---

## 0. 怎么用这张表

### 0.1 三个使用时机

| 时机 | 动作 |
|---|---|
| **开发前**（新工具/新功能） | 查 §1 三级分解：这一条属于 L1（拷模板）/ L2（照格式写）/ L3（自己写但别进模板） |
| **提交前** | 跑 §5 的机械检查命令；不绿不提交 |
| **发版前** | 逐行扫 §2 全表 + §3 重点域；任何 ⚠️/❌ 要么修、要么在工具 README 写"偏离第 X 条，原因是…" |

### 0.2 状态图例

| 符号 | 含义 |
|---|---|
| ✅ | 符合（有证据） |
| ⚠️ | 部分符合（缺一半，`缺口` 列写明缺哪半） |
| ❌ | 缺失/违规 |
| — | 不适用（触发条件不成立，**但 README 必须注明"未启用，因为未满足触发条件"**） |
| 📌 | 已申报偏离（`TEMPLATE-LOCAL-OVERRIDE` 或工具 README 留痕） |

### 0.3 三条使用纪律

1. **禁止靠文件名推断**：判定状态必须给出 `文件:行号` 或可复现命令。本表 2026-09-19 首版全部证据由对抗复核验证过，误判已修正（见 §4.3）。
2. **验证优先于修复**：⚠️/❌ 先写一条会红的断言，再改代码。**没有断言兜住的修复会在下次重构时复发**（l-s2t 单实例就是活例）。
3. **文档本身也要被检查**：§4 登记了规范/文档与现实不符的条目——文档说 A、磁盘是 B 时，**必须改文档或改代码，不许并存**。

---

## 1. 三级分解（模板库制品分类）

### L1 代码级共性 —— 业务无关，整文件拷贝即用

| 模板件 | 能力 | 对外接口（稳定承诺） | 版本 |
|---|---|---|---|
| `modules/appconfig/appconfig.py` | 参数区：**唯一要改的文件** | `APP_ID` / `APP_NAME` / `REPO_OWNER` / `REPO_NAME` / `EXE_NAME` / `VERSION` / `ICON_DRAW(d, size)` | 1.0.1 |
| `modules/paths/paths.py` | 数据区/播种/稳定位/**数据根重定向** | `APP_DIR` `RUN_DIR` `USER_DATA_DIR` `CONFIG_PATH` `LEGACY_CONFIG_PATH` `LOG_DIR` `LOG_PATH` `UPDATE_DIR` `INSTALL_DIR` `INSTALL_EXE` `is_stable_install()` `ensure_user_dirs()` `seed_config()` `process_pending_update()`（⛔ 已弃用） | 1.1.4 |
| `modules/autostart/autostart.py` | 自启三件套 | `get_autostart_cmd(target="stable")` `is_autostart_enabled()` `set_autostart(bool)` `migrate_autostart(log=…)` | 1.1.3 |
| `modules/update_helper/update_helper.py` | 更新三段式（查/下/换） | `check_update(cur, force=False, repo=None)` `download_and_prepare(..., repo=None, exe_name=None)` `build_apply_script(..., exe_name=None)` `UPDATE_READY` `PENDING_CMD` | 1.4.5 |
| `modules/i18n/i18n.py` | 轻量中英双表（机制词表分离） | `init(lang)` `t(key,*args)` `load_language_from_config` `save_language_to_config` `detect_system_lang()` `load_tables()` `available_langs()` | 2.2.0 |
| `modules/icons/icons.py` | 代码生成双 ico | `make_image(size)` `write_app_icons(out_dir)` / CLI | 2.0.0 |
| `modules/tray_kit/tray_kit.py` | 单实例 / 退出请求 / token 掩码 / 签名重画 / **退出确认框** | `acquire_single_instance(app_id, mutex_name=None, log=…)` `single_instance_free(name)` `warn_duplicate_instance` `confirm_quit_dialog(app, text, init, parent=None, on_change=None)` `make_quit_request_path(dir)` `quit_watch_loop(stop, path, on_quit, beat)` `mask_token(url)` `MenuSignature(rebuild, menu_is_open, log)` | 2.2.1 |
| `modules/log_kit/log_kit.py` | 滚动日志 1MB×3 + 打开日志目录 | `make_logger(log_dir)`（**log 为 print 形态**，见 D4-04/C-29） `get_logger(log_dir)` `LOG_MAX_BYTES` `LOG_BACKUPS` | 1.0.3 |
| `modules/service_link/service_link.py` | 服务唯一性/接入/有界清理状态机 | `ServiceLink(probe, launch, terminate, graceful=None, adopt_pid=None, log)` `.refresh()` `.can_start()` `.start()` `.stop()` `.state` `.spectators`（**属性**，非方法） `.note_spectators()` | 0.1.0 |
| `sync_check.py` | 防漂移哈希比对 + **无头/坏头/未接入申报**（1.9.0 起） | `python my-diy-tool-template/sync_check.py [--roots …]` | 1.9.0 |
| `conformance_check.py` | 规范符合度机械检查（本条表与 §5.1 的执行者） | `python …/conformance_check.py [--roots …] [--only …] [--selftest] [--temp-leak[-save/-baseline]]` | 1.9.24 |

> **版本列 = 磁盘上的 `TEMPLATE-VER`**（与 §2.4 B2 的"登记表版本 == 磁盘版本"同一口径）。
> 2026-09-19 复核发现本表**长期无人更新**：9 行里 **6 行落后**（最远的是 `update_helper`
> 1.0.1 vs 1.4.3、`tray_kit` 2.0.1 vs 2.2.0），已按磁盘值逐行同步；登记为 **§4.1.23**。
> ⚠️ 这一列**当前没有任何机械判据**（C-04 只查四工具的 B2 表），所以它一定会再漂。

### L2 文本级规范 —— 格式统一，内容逐工具各异

| 制品 | 统一的"格式" | 逐工具各异的部分 |
|---|---|---|
| `modules/build_release/build.bat` | 门禁顺序、每步失败判定、`norun/nopause` 参数、ASCII-only、反斜杠 | `APPNAME`、编译清单、业务自测命令、`--add-data` 内容 |
| `modules/build_release/release.bat` | 读版本→四项拒绝闸（脏树/暂存/非 main/本地≠远程）→打 tag 推送 | 版本读取路径随 src layout 调整 |
| `.github/workflows/tests.yml` | 全分支+PR 触发、`PYTHONUTF8=1`、每门禁独立 step、失败上传日志工件 | 测试矩阵、大资源下载/skip |
| `.github/workflows/release.yml` | `v*` tag 触发、zip + `.sha256`、`workflow_dispatch` 只出工件、run-name 区分 | 资源下载、构建步骤 |
| `README.md` + `README.zh-CN.md` | 顶部语言切换行**精确格式**、同信息集八段（安装/交互/资源/配置与数据/更新/排障/开发/许可）、键名路径两语言一致 | 全部正文内容 |
| `CHANGELOG.md` | `## <版本>` 节名与 tag 一一对应；未发版挂 `## Unreleased` | 每条改动 |
| `LICENSE` / `.gitignore` | MIT 文本；忽略清单（`build/ dist/ out/ release/ __pycache__ *.pyc *.spec *.log 活配置 大资源 生成 ico`） | 版权行、额外忽略项 |
| `locales/zh.json` + `locales/en.json` | 扁平 KV、utf-8、zh 为基准键、en 缺失回退 | 全部词条 |
| `config.json`（出厂模板） | JSON、与用户配置物理分离、随包分发 | 全部字段与默认值 |
| `modules/*/README.md` | 四段式：定位 / 对外接口 / 采纳步骤 / 边界与坑 | 各模块内容 |
| `blueprints.txt` | 一行一目录名、`#` 注释 | 名单（**只减不增**） |

### L3 纯业务 —— 必须留在工具内，**禁止进模板**

| 工具 | 纯业务（留工具内） | 说明 |
|---|---|---|
| reme-helper | ReMe 安装布局判定、官方 `default.yaml`→三模式配置生成、job 白名单、dream 日志解析、LLM/Embedding 探针、SSH 隧道目标建模、接入文档生成 | 数据配表（GLOSSARY/默认值表）应外置为数据文件 |
| local-speak2text | VAD 断句状态机、滑动窗口实时识别、AGC、麦克风后端探测、ASR 模型布局判型、键盘钩子、WASAPI 探测、注入键入、浮窗生长 | 模型布局知识与识别参数**不可**进模板 |
| dsh-helper | dsh CLI 路径探测、dsh 进程识别规则、CTRL_C_EVENT 停止策略、启动端口回退 | 有界清理的**机制**属模板，**dsh 特有停止实现**留工具 |
| opencodex-helper | SSH 隧道生命周期、令牌生成与公钥部署、ocx CLI 集成与健康探测、目标 CRUD 对话框 | 有界清理机制同 dsh |

> **镜像问题（同样是解耦债）**：L1 的机制被内联进业务文件，等于"业务文件里混着模板代码"。
> 已知：reme-helper 的 autostart/update/icons/退出确认内联在 `main.py`（已 OVERRIDE 申报）；
> dsh/ocx 的 autostart 内联。方向是**机制回流模板，工具只留参数与业务回调**。

---

## 2. 逐条对照表（76 条 × 4 工具）

> 列说明：**状态** 依据见 §4.3 的复核结论（原始审计中的误判已修正）。
> **检查** 列给出可复现命令或断言点；标 `⚙` 的可脚本化，见 §5。

### 2.1 A1 基线（无条件必须）

| ID | 要求 | reme | l-s2t | dsh | ocx | 模板件 | 检查 |
|---|---|---|---|---|---|---|---|
| A1-01 | git + `.gitignore`，产物/用户数据/大资源/生成物不入库 | ❌ 双 ico 入库 | ⚠️ `run.bat:3` 硬编码解释器路径无回退 | ✅ | ✅ | `baseline` | `git ls-files \| grep -iE '\.ico$\|release/\|build/'` ⚙ |
| A1-02 | LICENSE + CHANGELOG 与版本一一对应 | ✅ | ✅ | ✅ | ✅ | `baseline` | 逐 tag 与 CHANGELOG 节名比对 ⚙ |
| A1-03 | 版本单一事实源，只写一处 | ✅ | ⚠️ `release.bat:24` 读根 `paths.py`（实际在 `src/`），发版脚本第一步即失败 | ✅ | ✅ | `build_release` | `grep -rn 'VERSION = "' src/ \| wc -l` ⚙ |
| A1-04 | 用户数据区 `%LOCALAPPDATA%\<工具名>\` | ✅ | ⚠️ `update.pending.json` 落 exe 旁（`paths.py:44`） | ✅ | ✅ | `paths` | 首跑后查 AppData；exe 旁无新增运行态文件 |
| A1-05 | 门禁构建，测试不绿不出包 | ✅ | ⚠️ `tests/` 7 套件**无一处**被 build.bat/CI 调用 | ✅ | ⚠️ 无业务自测门禁 | `build_release` | 故意改坏一处，构建须非 0 ⚙ |
| A1-06 | 冻结 `--smoke` 真跑 | ✅ | ⚠️ `--smoke` 绕过正常启动路径（见 D3-01） | ✅（CI 走 nosmoke 需注明） | ⚠️ `--smoke` 只 print 恒 return 0；CI 走 nosmoke | `build_release` | `build.bat` 内 `--smoke` 有 errorlevel 判定 ⚙ |
| A1-07 | README 四要素与本版同步 | ⚠️ 退出语义写反（README:108 仍称退出即停服务，实际 1.2.4 起默认不停） | ✅ | ⚠️ `README:15` 旧包路径；配置示例缺 `quit_stop_dsh` | ⚠️ 标题仍 v1.1.0（源 1.2.1）；旧 `out\` 布局 | `baseline` | 抽 3 个配置键与源码比对 |
| A1-08 | 双语 README + 顶部语言切换行精确格式 | ⚠️ 切换行**未加粗** | ⚠️ 未加粗 | ✅ | ⚠️ 格式对但内容滞后 | `baseline` | `sed -n '3p' README.md` 须含 `**English**` ⚙ |
| A1-09 | 代码生成双 ico + exe 图标资源 | ✅ | ✅ | ✅ | ✅ | `icons` | `ls release/*/_internal/*.ico` ⚙ |
| A1-10 | 文案集中一处，为 i18n 留缝 | ✅（重形态，规范许可） | ⚠️ `main.py:147` 重复实例弹窗、`:352` 语言通知硬编码 | ❌ 全部内联 | ❌ 全部内联 | `i18n` | `grep -nP '[\x{4e00}-\x{9fff}]' src/main.py \| grep -v i18n.t` ⚙ |
| A1-11 | 交付三件套（产物路径+运行标识+门禁结果） | ⚠️ 门禁结果无留痕 | ✅ | ✅ | ✅ | `baseline` | 构建输出含 `[DONE]` + 路径 ⚙ |

### 2.2 A2 触发式能力

| ID | 触发条件 | reme | l-s2t | dsh | ocx | 规范所在 |
|---|---|---|---|---|---|---|
| T1 i18n | 交付他人/开源 | ✅ | ⚠️ 缺 `--lang-audit` + 2 处文案残留 | ❌ 公开仓库仍纯中文 | ❌ 同左 | E4 |
| T2 深色模式 | 大尺寸交互窗口+复杂交互 | ✅ | — （**README 未注明未启用**） | ⚠️ 未触发但未注明 | ✅（复核更正：确未触发） | E3 |
| T3 设置窗口 | 配置 >8 项或复杂输入形态 | ✅ | ✅（7 键，未触发） | ❌ 有文件选择形态却无设置窗口 | ❌ 9 键+文件选择+凭据 | E6 |
| T4 `--ui-check` | **有任何真实窗口** | ✅ | ❌ | ❌ | ❌ | D3 |
| T5 `--lang-audit` | 启用 T1 | ✅ | ❌ | ⚠️（T1 补齐后即必须） | ❌ | D3 |
| T6 harness 探针 | 启用 T3 | ✅ | ✅（未触发） | ❌ | ✅（复核更正：T3 未启用故不要求） | D3 |
| T7 内置 guide | 配置多/依赖复杂/交付他人 | ✅ | ❌ | ❌ | ❌ | F4 |
| T8 CI tests.yml | 建远端仓库 | ✅ | ⚠️ 无失败日志工件 | ⚠️ 同左 | ⚠️ 同左 | G3 |
| T9 CI release.yml + release.bat | 远端+需分发 | ✅ | ⚠️ release.bat 版本读取坏 | ⚠️ 无 release.bat | ⚠️ 无 release.bat | G3 |
| T10 升级检查/自动升级 | 远端+第二台机器 | ⚠️ 无节流、无 `update_repo` | ⚠️ apply.cmd 固定 timeout、不判 robocopy | ⚠️ 无 `update_repo` | ⚠️ 同左 | G4 |
| T11 性能日志 | 性能敏感路径 | — | ✅ | — | — | D4 |
| T12 单实例+运行检测 | 托盘常驻 | ⚠️ **build 运行检测匹配串失效**（`reme-helper-` 匹配不到 `reme-helper.exe`） | ❌ **互斥体名非法→每次启动误报"已在运行"** | ✅ | ✅ | D1/tray_kit |
| T13 资源自动识别 | 同类资源 ≥2 | — | ✅ | — | — | D5 |
| T14 优先级队列 | ≥2 类优先级积压 | — | ✅ | — | — | D5 |

### 2.3 A3 暂缓/不采用

| ID | 结论 | reme | l-s2t | dsh | ocx |
|---|---|---|---|---|---|
| A3-01 | 主题持久化暂缓 | ⚠️ 已实现且存 config（与 F2 一致），缺偏离登记 | ✅ 未实现 | ✅ | ✅ |
| A3-02 | 应用内日志查看器暂缓 | ⚠️ 无查看器，但**缺托盘"打开日志目录"**（路径还指向 ReMe 的 root/logs） | ✅ | ✅ | ✅ |
| A3-03 | 命名互斥量暂缓 | ✅（模板 2.0.1 已吸收为标准接口） | ⚠️ 已用但无偏离留痕 | ✅（复核更正） | ⚠️ 无偏离留痕 |
| A3-04 | 禁止重框架 | ✅ | ✅ | ✅ | ✅ |
| A3-05 | 禁止 onefile | ✅ | ✅ | ✅ | ✅ |

### 2.4 B 项目骨架 / 命名 / 模板纪律

| ID | 要求 | reme | l-s2t | dsh | ocx | 检查 |
|---|---|---|---|---|---|---|
| B1-01 | src layout；`tests/` 顶层与 src 平级 | ✅ | ✅ | ⚠️ **无 tests/** | ⚠️ **无 tests/** | `ls src/tests` 须不存在 ⚙ |
| B1-02 | 一级目录白名单，禁止一级 `.py` | ⚠️ 一级出现 `scripts/`（白名单外） | ⚠️ 一级出现 `tools/`（含 6 个入库 .py） | ✅ | ✅ | `find <tool> -maxdepth 1 -name '*.py'` ⚙ |
| B1-03 | dev 态锚定层级写明 + dev 态路径断言 | ⚠️ 有注释，`--smoke` 只 print 不断言 | ⚠️ 同左 | ⚠️ 同左 | ⚠️ `main.py:36` 自持 APP_DIR 与 `paths.APP_DIR` 冲突→dev 态 plink 失效 | `--smoke` 含路径关系断言 ⚙ |
| B2-01 | 登记表版本列 = 磁盘当前值 | ❌ 表 1.2.4 / 磁盘 1.2.5 | ✅ | ✅ | ✅ | 表 vs `VERSION` 比对 ⚙ |
| B3-01 | 目录名 = exe 名主体 = 包名前缀 | ✅ | ✅ | ✅ | ✅ | 三处比对 |
| B3-02 | semver 判级档位与改动性质自洽 | ⚠️ 判级依据无留痕 | ⚠️ 1.3.0 自述"无可见行为变化"却 +0.1 | ⚠️ 1.8.0 同款 | ✅（复核更正） |
| B3-03 | commit 前验证；+0.1/+1 仅用户确认 | ⚠️ 无逐 commit 验证记录 | ⚠️ 残留 1.3.0 无确认记录 | ⚠️ 无人工回归留痕 | ❌ `ca8d381`/`932cdbb` 提交信息自承 "Build skipped: tool in use"、"files were untouched" |
| B3-04 | `<APP>_CONFIG` + `<APP>_DATA_DIR` | ⚠️ 只有 `_CONFIG`，**无 `_DATA_DIR`** | ⚠️ 只有 `_CONFIG`，**无 `_DATA_DIR`** | ⚠️ 只有 `_DATA_DIR`，**无 `_CONFIG`** | ⚠️ 同 dsh |
| B4-01 | 拷贝件归一化一致或已申报 | ⚠️ `service_link` 预置未接线 | ⚠️ `log_kit` 头指向不存在的 `_template/`、`icons` 无头 | ✅ | ✅ |
| B4-02 | 分叉留痕；代码与数据配表分离 | ✅ | ⚠️ 分叉已由蓝本名单登记 | ⚠️ 文案未外置 | ⚠️ 文案未外置 |
| B4-03 | 防漂移四件套齐 + 门禁加 sync_check | ⚠️ 门禁无 sync_check | ❌ 四件套只剩一件半（仅 2 文件有头） | ✅ | ✅ |
| B4-04 | **实例隔离：测试/构建必须重定向数据根** | ❌ 测试共享用户 config/log | ❌ 测试改写用户真实注册表 Run 键；冒烟写真实 AppData | ⚠️ CI `import main` 污染真实 AppData | ❌ 同左 |

### 2.5 D 工程纪律

| ID | 要求 | reme | l-s2t | dsh | ocx | 检查 |
|---|---|---|---|---|---|---|
| D1-01 | 读版本 + 拒绝已有 release 目录 | ✅ | ✅ | ✅ | ✅ | 预建同名目录须 exit≠0 ⚙ |
| D1-02 | 运行检测前缀匹配**且匹配串正确** | ❌ 匹配串 `reme-helper-` 漏掉当前 exe | ✅ | ✅ | ✅ | 起一个实例后构建须 exit≠0 ⚙ |
| D1-03 | 编译门禁（**须含真实 import**） | ⚠️ 无 py_compile，靠 import 覆盖；未接线模块漏检 | ⚠️ `pipeline.py:387/394` `from i18n import t` 是坏的（应为 `from modules import i18n`），py_compile 全绿 | ✅ | ✅ |
| D1-04 | i18n 关键键 zh/en 断言 | ✅ | ⚠️ 只断言 **1 个键**（74 键中 72 键无闸） | ❌ | ❌ |
| D1-05 | 业务自测真跑核心链路 | ✅ | ✅ | ⚠️ 无独立步骤（并进冻结冒烟且排在打包后） | ❌ 完全缺失 |
| D1-06 | 构建期生成图标 | ✅ | ✅ | ✅ | ✅ |
| D1-07 | `--onedir --noconsole --icon` + 组装 release | ✅ | ✅ | ✅ | ✅ |
| D1-08 | 交付物检查（exe / `_internal` 运行时 / 资源） | ✅ | ✅ | ✅ | ✅ | 清空 `_internal` 须 exit≠0 ⚙ |
| D1-09 | 冻结冒烟（`<APP>_CONFIG` 钉配置）+ 清理诊断产物 | ✅ | ✅ | ✅ | ⚠️ `--smoke` 无断言 + CI nosmoke |
| D1-10 | `[DONE]` + 路径 + `norun/nopause`；便宜在前 | ⚠️ 缺 py_compile 步、运行检测失效 | ✅ | ⚠️ 缺业务自测步 | ⚠️ 缺 i18n + 业务自测步 |
| D2-01 | 自检钉配置 + 相对路径向上回退 + 双布局测试 | ✅ | ⚠️ 无 paths 测试；冒烟仍写真实 LOG_DIR | ⚠️ 无 `_CONFIG`、无测试 | ⚠️ 同左 |
| D2-02 | 发布前删 log/ 与 smoke.log | ✅ | ✅ | ✅ | ✅ |
| D3-01 | 自检命令分级；**`--smoke` 不得绕过正常启动路径** | ⚠️ `--smoke` 在守卫前 return（ef9b381 的 TypeError 因此漏网） | ⚠️ 同款，且掩盖了 T12 崩溃 | ⚠️ 同款 | ⚠️ 同款 |
| D3-02 | 测试是门禁 / 失败带实际值 / 每故障补断言；T6 探针 | ✅ | ❌ 测试非门禁、硬编码绝对 `sys.path`、无 conftest | ⚠️ 无 tests/ | ❌ 无 tests/ |
| D3-03 | 测试与自检**只读**，禁启停真实服务 | ✅ | ❌ `test_autostart_migrate.py:11-17` 改写用户真实 HKCU Run 值 | ✅ | ✅ |
| D4-01 | 异常必写日志 + 计数，禁静默失败 | ⚠️ 3 处 `except: pass` | ⚠️ 多处静默 + 无异常计数 | ⚠️ `main.py:881` 吞异常 | ❌ 29 处 `except Exception`、17 处裸 pass |
| D4-02 | 轮转 1MB×3 + 托盘"打开日志目录" | ⚠️ **菜单无"打开日志目录"** | ✅ | ✅ | ✅ | `grep -c 'maxBytes' src/log_kit.py` ⚙ |
| D4-03 | 性能日志结构化行 | — | ✅ | — | — |
| **D4-04** | **传给模板件的 `log` 必须是 print 形态**（收任意个位置参数）。**注：工具侧自建 `def log(*parts)` 包装是正解，不是要消灭的偏差**——判据要消灭的是"只收一个参数"的包装 | ✅ 取 `log_kit.make_logger`（1.0.3 起 `*parts`）；自身调用点全是单参 f-string | ✅ **已改（2026-09-19，#36 在途）**：`src/main.py:80` 现为 `def log(*parts)`。**修前**为 `def log(message)` 单参却照样由三处 `log=log` 交给模板件 → **实测**模板件 L257/L390 两个位置参数直接 `TypeError` | ✅ 自建 `def log(*parts)`（`src/main.py:120`） | ✅ 自建 `def _log(*parts)`（`src/main.py:80`） | `conformance_check.py --only C-29` ⚙；**l-s2t 修完提交后 C-29 应转 `[ok]`**——本次级联的验收判据 |
| D5-01 | 优先级队列（final 插队） | — | ✅ | — | — |
| D5-02 | 过期任务**执行前**丢弃 | — | ✅ | — | — |
| D5-03 | 布局自动识别，目录名与实现解耦 | — | ✅ | — | — |
| D5-04 | 相对路径向上查找回退（限 3 层） | ⚠️ 固定候选点枚举，非逐级查找 | ⚠️ 回退候选硬编码两个模型名，自定义 `model_dir` 找不到 | — | — |

### 2.6 E 界面工程

| ID | 要求 | reme | l-s2t | dsh | ocx | 检查 |
|---|---|---|---|---|---|---|
| E1-01 | 单解释器：根窗口只建一次不销毁 | ✅ | ✅ | ✅（复核更正：纯托盘无根窗口，模板明示临时根形态） | ❌ 每次对话框新建/销毁 `tk.Tk()` |
| E1-02 | 单 UI 线程归属 | ✅ | ✅ | ✅（复核更正） | ❌ 对话框在工作线程内创建 |
| E1-03 | 队列封送 `ui_q/ui_post/ui_call` | ✅ | ✅ | ❌ 零命中，监控线程直接 `icon.update_menu()` | ❌ 零命中 |
| E1-04 | 退出路径 `finally` 收尾三项 | ⚠️ 更新脚本在下载成功即起（功能等价、位置不符） | ✅ | ⚠️ 无 try/finally | ⚠️ 无 try/finally |
| E1-05 | 回调异常计数 → `--ui-check` 红灯 | ✅ | ⚠️ 有 crash.log 无计数、无 `--ui-check` | ❌ | ❌ |
| E2-01 | 八段式菜单，`default=True` 唯一，退出恒最后 | ✅ | ✅ | ✅ | ⚠️ 实际九段（服务控制被业务段切两半） |
| E2-02 | 动词条对象名 = 服务名，禁"本工具" | ✅ | ✅ | ✅ | ✅ |
| E2-03 | "…"后缀专指开界面 | ✅ | ✅ | ⚠️ "选择路径"弹文件框却无"…" | ✅ |
| E2-04 | 开关项 = 状态短语 + 勾选 | ✅ | ✅ | ✅ | ✅ |
| E2-05 | 只读信息行完整句子 + 仅第一段 | ✅ | ✅ | ✅ | ✅ |
| E2-06 | "退出"恒最后；`--quit` 不被确认弹窗阻塞 | ✅ | ⚠️ **无 `--quit`**（模板 README 却称 l-s2t 是 `--quit` 蓝本） | ✅（复核更正：`--quit` 非强制项） | ⚠️ 无 `--quit` |
| E2-07 | 面板地址行 token 掩码 + 复制项紧贴 | ✅（不适用，复核更正） | ✅（不适用） | ✅ | ⚠️ 无地址行/复制项，且完整 URL 含 token 时明文进日志 |
| E2-08 | 文案延迟求值 + 变化后显式重建 | ✅ | ⚠️ 普通条即时求值，靠"语言切换必 rebuild"兜 | ⚠️ 无签名机制 | ⚠️ T1 未实现故无法验证 |
| E2-09 | 状态签名比较 + 菜单占用探测 | ✅ | ❌ 无条件 `update_menu()`，无签名/占用探测 | ❌ 同左 | ❌ 同左 | `grep -n 'MenuSignature\|GUI_INMENUMODE'` ⚙ |
| E2-10 | 条件项 enabled + 二态勾选 + 状态色同源 | ✅ | ✅ | ✅ | ⚠️ "启动服务"在线时仍可点 |
| E3-01/02 | 单引擎双调色板 + 对比度阈值断言 | ⚠️ 正文 ≥8:1 无断言（测试只到 2:1） | — | — | — |
| E4-01 | zh 基准 + en 回退 + `auto` 跟随系统 + `t()` 支持格式化 | ⚠️ 无 `auto`、`t()` 只接单参 | ✅ | ❌ | ❌ |
| E4-02 | 词表覆盖全部用户可见文案 | ✅ | ⚠️ 2 处残留 | ❌ | ❌ |
| E4-03 | 词表即数据 + 关键键断言进构建 | ✅ | ⚠️ 无静态覆盖扫描 | ❌ | ❌ |
| E5-01 | 配置项"效果+默认值+为何不是越大越好"；危险动作预告；长任务互斥+真实回显；依赖缺失自助出口 | ✅ | ⚠️ 三个数值项无成组说明；依赖缺失走通知而非"标红+禁用+复制提示词" | ⚠️ 无自助出口 | ⚠️ 配置项无说明 |
| E5-02 | 浮窗向上生长/最大行数/不越屏 | ⚠️ 有 tooltip/toast 浮窗但无上生长与边界约束 | ✅ | — | — |
| E6-01/02 | 草稿-基线-保存；失败回滚不关窗；身份项与公共项分开；harness | ✅ | — | ❌ 即点即存 | ❌ 即点即存 |

### 2.7 F 数据与配置

| ID | 要求 | reme | l-s2t | dsh | ocx |
|---|---|---|---|---|---|
| F1-01 | config/log 在 AppData | ✅ | ✅ | ✅ | ✅ |
| F1-02 | 播种：旧位置只首跑读一次 | ✅ | ✅ | ✅ | ✅ |
| F1-03 | `<APP>_CONFIG` 可钉配置；出厂模板与用户配置分离；大资源不入库 | ⚠️ 无 `_DATA_DIR` | ✅ | ⚠️ 无 `_CONFIG` | ⚠️ 无 `_CONFIG` |
| F2-01 | 每类信息一个真源，禁双写；凭据掩码/留空不改 | ✅ | ✅ | ⚠️ 自启状态注册表与 config 双写，config 字段无读取方 | ✅ |
| F3-01 | 保存链五段 | ✅ | — | ⚠️ 只实现"校验不写盘" | ⚠️ 缺回滚/告知/基线刷新 |
| F4-01 | guide.py 随包 + 占位符现场生成 + 走 i18n | ✅ | ❌ | ❌ | ❌ |
| F4-02 | guide 脱敏门禁 | ✅ | ❌ | ❌ 且仓库含 `H:\Tools\Python\...` 绝对路径 | ❌ 且仓库含内网 IP `192.168.190.128` + 用户名 `xzy_admin` |

### 2.8 G 打包、发布与升级

| ID | 要求 | reme | l-s2t | dsh | ocx |
|---|---|---|---|---|---|
| G1-01 | release 布局，exe 不带版本号，已存在即拒 | ✅ | ✅ | ✅ | ✅ |
| G2-01 | `.gitignore` 排除清单完整 | ❌ 双 ico 入库 | ✅ | ✅ | ✅ |
| G2-02 | LICENSE/CHANGELOG 与仓库同生，节名对应 tag | ✅ | ✅ | ✅ | ✅ |
| G3-01 | tests.yml：全分支+PR、独立 step、`PYTHONUTF8=1`、失败上传日志 | ✅ | ⚠️ 无失败上传 | ⚠️ 无失败上传、无用例集 | ⚠️ 同左 |
| G3-02 | release.yml：tag 触发、zip+SHA256、dispatch 只出工件 | ✅ | ✅ | ✅ | ✅ |
| G3-03 | tag 与版本一致；发版前人工回归；禁自动升版+push 连招 | ⚠️ 无人工回归留痕 | ⚠️ 同左 | ⚠️ 同左 | ⚠️ tag 一致性未断言 |
| G3-04 | 双语 README 两份都随 release 复制 | ⚠️ 只拷 `README.md`，`README.zh-CN.md` 未随包 | ⚠️ 切换行未加粗 | ✅ | ⚠️ 内容滞后 |
| G3-05 | release.bat 本地零构建发版 | ✅ | ⚠️ 版本读取路径坏，实际不可用 | ⚠️ **缺件** | ❌ **缺件** |
| G4-01 | 检查节流 + `update_repo` 未配置静默降级 | ⚠️ 无节流、无 `update_repo` | ✅ | ⚠️ 无 `update_repo` | ⚠️ 无 `update_repo` |
| G4-02 | 下载校验→暂存→退出替换；pending 幂等 | ⚠️ 无启动 pending 兜底 | ⚠️ apply.cmd 固定 timeout、不判 robocopy errorlevel | ⚠️ pending 未接线 | ⚠️ 同左 |
| G4.1-01 | 稳定安装位 `app\` | ❌ 无（升级必留自启死链） | ✅ | ❌ | ❌ |
| G4.1-02 | 自启指向稳定位 | ❌ | ✅ | ❌ | ❌ 实机注册表指向已删除的 `out\...\opencodex-helper-1.0.exe` |
| G4.1-03 | 自启自愈 | ✅ | ✅ | ❌ | ❌ |
| G4.1-04 | 退出二次确认（红底/取消持焦点/模态/关窗=取消） | ✅ | ✅ | ✅ | ✅ |
| G4.1-05 | 存量旧键靠自愈纠正 | ✅ | ✅ | ❌ | ❌ |
| G4.2-01 | 服务唯一性守卫（探测不到才允许启动） | ✅ | — | ✅ | ⚠️ 隧道侧有守卫，菜单未禁用；ocx 服务侧无守卫 |
| G4.2-02 | 接入 (adopt) 信息登记后固定 | ⚠️ 接入 pid 随轮询漂移；`service_link` 未接线 | — | ⚠️ 每拍重写 pid | ❌ 无 adopt 概念 |
| G4.2-03 | 有界清理，禁全量签名击杀 | ⚠️ 无优雅关闭 API 分支 | — | ✅ | ⚠️ `kill_target_procs` 仍按签名全量击杀（停止/删除路径） |
| G4.2-04 | 放行是合法状态 | ✅ | — | ✅ | ⚠️ 无 ADOPTED 概念，仅近似 |
| G4.2-05 | 退出清理勾选持久化默认不勾；降级链不得跳过确认 | ✅ | — | ✅ | ⚠️ 缺"关闭服务"勾选；降级第三级在 UI 可用时也无确认退出 |
| G5-01 | 代码生成，零美术素材，形状/状态色同源 | ⚠️ 生成物入库 | ✅ | ✅（`resources/img` 手工资产属 B1 允许，已 OVERRIDE 申报） | ✅ |
| G5-02 | 双 ico 帧档齐全 | ✅ | ✅ | ✅ | ✅ | 逐档比对 ⚙ |
| G5-03 | `--icon` + `--add-data` + 交付物断言 | ✅ | ⚠️ 只断言任务栏 ico，未断言托盘态 | ✅ | ✅ |

### 2.9 I 落地清单（自查项）

| ID | 要求 | reme | l-s2t | dsh | ocx |
|---|---|---|---|---|---|
| I-01 | 登记 B2 + 四件套齐 | ✅ | ✅ | ✅ | ✅ |
| I-02 | 先写 paths，其他模块不自拼路径 | ⚠️ `main.py` 仍自拼 update 日志/备份路径 | ⚠️ `pipeline.py:41-52` 自拼模型路径，违反"路径只出自 T2" | ✅ | ⚠️ `main.py:36/39/52` 自持 APP_DIR/SSH_KEYGEN/PLINK_PATH |
| I-03 | 入口 + 托盘 + 队列封送 + `--smoke` 骨架 | ✅ | ✅（但被 T12 阻断，骨架跑不到） | ⚠️ 缺队列封送 | ⚠️ 缺队列封送 |
| I-04 | 业务与界面解耦，可脱离 UI 自测 | ✅ | ⚠️ 解耦达标但错误分支 `from i18n import t` 会炸 | ⚠️ 业务全在 1592 行 main.py | ❌ 业务全内联，`import main` 有落盘副作用 |
| I-05 | 首版即建词表/常量区 | ✅ | ⚠️ 2 处文案未进词表 | ❌ | ❌ |
| I-06 | icons.py 生成双图标 | ✅ | ✅ | ✅ | ✅ |
| I-07 | build.bat 全门禁跑绿 | ⚠️ 运行检测失效 + 无 sync_check 闸 | ⚠️ 门禁不含 tests/ | ⚠️ 缺 i18n + 业务自测 | ⚠️ 缺 i18n + 业务自测 |
| I-08 | 远端 + workflows + release.bat | ✅ | ⚠️ release.bat 坏 | ⚠️ 缺 release.bat | ⚠️ 缺 release.bat |
| I-09 | updater + 托盘更新菜单 + config 模板加 `update_repo` | ⚠️ config 模板无 `update_repo` | ✅ | ⚠️ 同 reme | ⚠️ 同 reme |
| I-10 | 交付前三件套 + 五项自查（含**未触发能力逐条注明**） | ⚠️ 未注明 T11/T13/T14 | ⚠️ 未注明 T2/T3/T7 等 | ⚠️ 未注明 | ❌ 自查清单多项缺失、README 滞后两个版本 |

---

## 3. 重点域深挖（用户点名的四个易漏域）

> §2 是规范视角；§3 是**执行视角**——把最常漏、后果最重的四类拆到"函数签名级"。

### 3.1 退出机制（EXIT）

| # | 检查点 | 模板件/参考 | reme | l-s2t | dsh | ocx |
|---|---|---|---|---|---|---|
| EXIT-01 | 托盘"退出"恒为最后一项，名称固定 | `tray_kit` / E2-06 | ✅ | ✅ | ✅ | ✅ |
| EXIT-02 | 人工路径必经二次确认（红底确认钮在左 + 取消持默认焦点 + `grab_set` 模态防叠加 + `WM_DELETE_WINDOW`/Esc = 取消） | `tray_kit.confirm_quit_dialog` | ✅ | ⚠️ **Esc 无效**（GUI 实测 + `main.py:918-947` 无 `<Escape>` 绑定；模板有） | ✅ | ✅ |
| EXIT-03 | 程序化路径（`--quit`）**不得**被确认弹窗卡住 | `tray_kit.quit_watch_loop` | ✅ | ⚠️ **无 `--quit`** | ⚠️ 无 `--quit` | ⚠️ 无 `--quit` |
| EXIT-04 | 清理勾选：持久化到 config、**默认不勾**、勾选动作即落盘（点取消也留存） | `tray_kit` + `service_link` | ✅ | — | ✅ | ⚠️ 缺服务勾选 |
| EXIT-05 | 不勾选 = 服务/隧道越过托盘生命周期继续运行（放行是合法状态） | G4.2-04 | ✅ | — | ✅ | ⚠️ |
| EXIT-06 | 降级链：富对话框 → 原生确认框（按持久化配置清理）→ 放行且默认不清理；**任何一级都不得跳过确认** | G4.2-05 | ✅ | ✅ | ✅ | ⚠️ 第三级在 UI 可用时也直接无确认退出 |
| EXIT-07 | 退出路径在 `finally` 收尾：停钩子 + 停托盘 + **若有待应用更新则启动替换脚本** | E1-04 | ⚠️ 位置不符（下载成功即起） | ✅ | ⚠️ 无 `finally` | ⚠️ 无 `finally` |
| EXIT-08 | 退出排空在途动作 + 防重入 + 超时兜底强退 | `tray_kit` README | ✅ | ✅ | ✅ | ✅ |
| EXIT-09 | 更新换装期间服务与隧道零中断（更新链显式放行） | G4.2 参考实现 | ✅ | — | — | — |

**EXIT 域违规代价**：EXIT-03 缺失 = 脚本/更新链无法让工具退出，只能杀进程；
EXIT-06 破坏 = 用户可能在"以为只是关窗口"时把正在跑的服务停掉。

### 3.2 单实例与启动（SINGLE）

| # | 检查点 | 模板件/参考 | reme | l-s2t | dsh | ocx |
|---|---|---|---|---|---|---|
| SINGLE-01 | 互斥体名合法：**命名空间前缀 `Local\` 之后不得再出现反斜杠** | `tray_kit` `Local\{app_id}-single-instance` | ✅ | ❌ `main.py:113` `Local\{APP_ID}\SingleInstance` → `CreateMutexW` 返回 NULL(err=3) | ✅ | ✅ |
| SINGLE-02 | **守卫自身失败必须放行**（宁可多开，不能打不开） | `tray_kit` 契约 | ✅ | ❌ `main.py:134` `if not handle or …: return False` → 失败即拒绝启动 | ✅ | ✅ |
| SINGLE-03 | 重复启动要有可见提示（无 console 用弹窗，不能 print） | `warn_duplicate_instance` | ✅ | ✅ | ✅ | ✅ |
| SINGLE-04 | `--smoke` 等诊断参数**不得绕过**正常启动路径（守卫/自启自愈/托盘） | J 坑 + D3-01 | ⚠️ | ❌ 掩盖了 SINGLE-01 | ⚠️ | ⚠️ |
| SINGLE-05 | build.bat 运行检测前缀匹配，且匹配串与 exe 名相符 | D1-02 | ❌ `reme-helper-` ≠ `reme-helper.exe` | ✅ `local-speak2text` | ✅ | ✅ |
| SINGLE-06 | 测试可跳过守卫（`<APP>_ALLOW_MULTI=1` 之类），但**生产路径不带** | l-s2t 参考 | ✅ | ✅ | — | — |
| SINGLE-07 | 守卫有断言覆盖（建互斥体→第二次调用须 False；失败注入须 True） | D3-02 | ⚠️ | ⚠️ 已有断言，但见 SINGLE-08 | ⚠️ | ⚠️ |
| SINGLE-08 | **测试实例的互斥体名不与生产实例冲突**（`<APP>_DATA_DIR` 隔离不了内核对象） | F11 的补充（2026-09-19 新增） | — | ⚠️ 用默认名，实例在跑时手动跑测试会假红灯（门禁路径由 build.bat 运行检测闸兜住） | — | — |

> **SINGLE-08 的由来（2026-09-19）**：`<APP>_DATA_DIR` 被当作"实例隔离总开关"，
> 但**它的作用域只到磁盘**——互斥体、端口、命名管道都在内核/系统全局命名空间里，重定向数据根管不到。
> 后果：测试哪怕把数据根指到临时目录，只要用户的托盘实例在跑，"抢锁应当成功"的断言就会假红灯。
> 处置口径（已下发给实现者）：**命名正确性用纯字符串断言（不占锁）＋ 抢锁/拒绝用测试专属名**
> （模板 `acquire_single_instance(app_id, mutex_name=None)` 本就支持显式传名）。
> **前提是不能为了"测试好跑"而削弱断言**——若拆完不再保证"运行期真的用这个名字"，宁可不拆，
> 改为在测试头部写明前提。见 §5.2 R-09。

**SINGLE 域教训（2026-09-19 实战）**：SINGLE-01 + SINGLE-02 两个缺陷叠加，
配合 SINGLE-04（冒烟绕过）+ SINGLE-07（无断言），造出"**四层防护全绿、工具完全不可用**"。
`✶` 这类"守卫的失败方向"是最容易写反的地方——**任何守卫类代码都必须回答：
"守卫自己坏了，系统是打开还是关闭？"** 家族统一答案：**打开**。

### 3.3 服务托管（SVC，helper 类专用）

| # | 检查点 | 模板件/参考 | reme | dsh | ocx |
|---|---|---|---|---|---|
| SVC-01 | 唯一性守卫：健康探测探不到才允许启动；菜单禁用 + `start()` 首行守卫**双保险** | `service_link.can_start()` | ✅ | ✅ | ⚠️ 隧道侧有、服务侧无、菜单未禁用 |
| SVC-02 | 外部多开属业务自由：不阻止、不清理、不告警刷屏 | G4.2-01 | ✅ | ✅ | ✅ |
| SVC-03 | 接入对象 = **规范端点实际应答者**，多候选取应答者 | G4.2-02 | ⚠️ 显示用枚举 seq[0] | ✅ | ❌ 无概念 |
| SVC-04 | 接入信息（pid/句柄）**登记后固定，不随轮询漂移** | `service_link` | ⚠️ 停止时才重查 | ⚠️ 每拍重写 pid | ❌ |
| SVC-05 | OWNED 用进程句柄终止整棵树；ADOPTED 优先优雅关闭 API，失败再按 pid | `service_link.stop()` | ⚠️ 无优雅分支 | ✅ | ⚠️ 无优雅分支 |
| SVC-06 | **禁止全量签名击杀** | G4.2-03 | ✅ | ✅ | ⚠️ `kill_target_procs` 被 4 处调用 |
| SVC-07 | 退出/停止后服务继续运行是预期行为；下次启动自动重新接入 | G4.2-04 | ✅ | ✅ | ⚠️ 仅近似 |
| SVC-08 | 等待/轮询节拍可配置 + 超时兜底 + 首拍立即执行 | `tray_kit` 三循环 | ✅ | ✅ | ✅ |
| SVC-09 | 服务停止是显式菜单入口，对 ADOPTED 同样可用 | G4.2-04 | ✅ | ✅ | ✅ |
| SVC-10 | 测试/构建**不得启停真实服务**（mock / DATA_DIR 重定向 / 独立实例） | D3-03 | ✅ | ✅ | ✅ |

### 3.4 软件命名（NAME）

| # | 检查点 | 规则来源 | reme | l-s2t | dsh | ocx |
|---|---|---|---|---|---|---|
| NAME-01 | 目录名 = exe 名主体 = `APP_ID`，匹配 `^[a-z0-9-]+$` | B3 | ✅ | ✅ | ✅ | ✅ |
| NAME-02 | exe **不带版本号** | B3 | ✅ | ✅ | ✅ | ⚠️ 历史注册表键含 `opencodex-helper-1.0.exe` |
| NAME-03 | 包名前缀一致（家族统一 `modules`） | B3 | ✅ | ✅ | ✅ | ✅ |
| NAME-04 | 互斥体名合法且含 APP_ID | SINGLE-01 | ✅ | ❌ | ✅ | ✅ |
| NAME-05 | 自启注册表键名 = `APP_NAME`（或约定的稳定键） | B3 | ✅ | ✅ | ✅ | ✅ |
| NAME-06 | 日志文件名 = `<APP_ID>.log` | B3 | ✅ | ✅ | ✅ | ✅ |
| NAME-07 | release 目录 = `release\<工具名>-<版本>\` | G1 | ✅ | ✅ | ✅ | ✅ |
| NAME-08 | zip 名 = `<工具名>-<版本>-windows-x64.zip` | G3 | ✅ | ✅ | ✅ | ✅ |
| NAME-09 | 菜单动词条对象名 = 被管理服务名，禁"本工具" | E2-02 | ✅ | ✅ | ✅ | ✅ |
| NAME-10 | 环境变量名 = **`APP_ID.upper().replace('-','_') + '_CONFIG'` / `'_DATA_DIR'`**（模板 `paths.py` 的派生式，**连字符转下划线、不是删除**） | B3 | `REME_HELPER_*` ✅ | `LOCAL_SPEAK2TEXT_*` ✅（2026-09-19 改名对齐，见 §4.1.10b） | `DSH_HELPER_*` ✅ | `OPENCODEX_HELPER_*` ✅ |
| NAME-11 | 数据目录 = `%LOCALAPPDATA%\<APP_ID>\` | B3 | ✅ | ✅ | ✅ | ✅ |

> **NAME-10 的落地检查（2026-09-19 最终）**：本行原写"去连字符"，与模板 `paths.py` 的
> `APP_ID.upper().replace('-','_')` **不符**——正确规则是**连字符转下划线**。
> 按此规则四工具统一为 `REME_HELPER_*` / `LOCAL_SPEAK2TEXT_*` / `DSH_HELPER_*` / `OPENCODEX_HELPER_*`，
> **四方全部 ✅，无例外**——l-s2t 已于本轮把历史变量名 `LOCALSPEAK2TEXT_*`（无下划线）改名对齐（§4.1.10b）。
>
> `✶` 这个例外曾存在的原因：`local-speak2text` 的工具名本身用连字符连了三个词，
> "转下划线"与"去连字符"两条读法在此分岔，当年实现按后者写死了变量名。
> **处置选了"改名对齐规则"而不是"给规则加例外"**——环境变量是纯工具链契约（build.bat / tests / CI 用），
> 无外部用户、改名零风险；而留一个例外，后人照 `paths.py` 抄一遍就会静默拿错变量名、**踩中实例隔离（F11）红线**。
>
> `✶` 另一条教训紧随其后：改名后 **`CONFORMANCE` 本表的 NAME-10 行与模板 `modules/paths/README.md:18`
> 都还在写"唯一例外"**——由对抗复核员逐条读文档抓出。**代码改了、测试绿了，文档里的旧结论却没人回头删**。
> 这与 §4.1.10a 是同一类：`文档与现实不符` 不会自己报错，只能靠"改动后反向搜索受影响文档"来兜。

### 3.5 文档规范（DOC）

| # | 检查点 | 规则来源 | reme | l-s2t | dsh | ocx |
|---|---|---|---|---|---|---|
| DOC-01 | `README.md` 英文 canonical + `README.zh-CN.md` 中文 | A1-08 | ✅ | ✅ | ✅ | ✅ |
| DOC-02 | 切换行**精确格式**：英文 `**English** \| [简体中文](README.zh-CN.md)`；中文 `[English](README.md) \| **简体中文**`（当前语言加粗不带链接） | A1-08/G3-04 | ⚠️ 未加粗 | ⚠️ 未加粗 | ✅ | ✅ |
| DOC-03 | 中文版不是机翻腔；代码块/键名/路径两语言一致 | G3-04 | ✅ | ⚠️ `README.zh-CN:37` 残留旧 `models\` | ⚠️ 两份一致地旧 | ⚠️ 同左 |
| DOC-04 | 同信息集八段：安装/交互/资源/配置与数据/更新/排障/开发/许可 | G3-04 | ✅ | ✅ | ⚠️ 缺更新段 | ⚠️ 缺更新段 |
| DOC-05 | **两份 README 都随 release 复制** | G3-04 | ❌ 只拷 `README.md` | ✅ | ✅ | ✅ |
| DOC-06 | README 与本次版本同步（版本号/路径/配置键） | A1-07 | ⚠️ 退出语义过期 | ✅ | ⚠️ 旧包路径、缺 `quit_stop_dsh` | ⚠️ 标题仍 v1.1.0 |
| DOC-07 | README 注明**未触发能力及原因** | I-10 | ⚠️ | ⚠️ | ⚠️ | ❌ |
| DOC-08 | `CHANGELOG.md` 节名与 tag 一一对应，未发版挂 `Unreleased` | A1-02 | ✅ | ✅ | ⚠️ Unreleased 未随 1.8.0 转正 | ✅ |
| DOC-09 | 升级判级在 CHANGELOG/commit 留痕（+0.0.1 / +0.1 依据） | B3-02 | ⚠️ | ⚠️ | ⚠️ | ✅ |
| DOC-10 | 模块 README 四段式；工具 README 有"偏离第 X 条"留痕 | B4/§0.3 | ⚠️ | ⚠️ | ⚠️ | ⚠️ |
| DOC-11 | 脱敏：文档/示例无个人绝对路径、机器名、内网 IP、密钥 | §0 脱敏约定 | ✅ | ⚠️ `run.bat` 硬编码解释器路径 | ❌ `H:\Tools\Python\...` | ❌ `192.168.190.128` + `xzy_admin` |

---

## 4. 规范自身的缺陷登记（文档 ↔ 现实不一致）

> 这一类最危险：**AI 按文档执行，文档本身是错的**。

### 4.1 已确认的规范缺陷

| # | 位置 | 问题 | 处置 |
|---|---|---|---|
| 4.1.1 | `STANDARDS.md` A3-03 | 写"命名互斥量暂缓"，但 `tray_kit` 2.0.1 已把 `CreateMutexW` 作为标准接口，dsh/ocx 字节级一致消费——**规范落后于模板** | 已改为：命名互斥量由 `tray_kit` 提供并采纳；工具侧无需偏离登记 |
| 4.1.2 | `STANDARDS.md` B2 表 | reme-helper 版本列 1.2.4，磁盘 1.2.5 | 发版时同步；建议 B2 版本列由脚本生成 |
| 4.1.3 | `REVIEW.md` T7 行 | 称 local-speak2text 是 「`--quit` 请求文件蓝本」，当时磁盘上 l-s2t **没有** `--quit` | 蓝本标注改为 reme-helper；l-s2t 需补 `--quit` 或明确不做。<br>✅ **2026-09-19 已实现（本条按源码更正，推翻上面那句）**——ls2t-dev 的物证（`tmp.TzZ8BDq8Hk/data/local-speak2text/quit.request` 残留）经**读源码核实**，不是转述：① **生产者**：`src/main.py:1192` `elif "--quit" in sys.argv:` → `:1174` 的 `_request_quit()` 写 `tray_kit.make_quit_request_path(USER_DATA_DIR)`（`= <数据根>/quit.request`，定义在模板 `modules/tray_kit/tray_kit.py:244`）；② **消费者**：`main.py:1041-1046` 起了一个线程，`target=tray_kit.quit_watch_loop`、`args=(quit_stop, <同一路径>, on_quit)`，循环体 `tray_kit.py:253-265`：文件存在 → `unlink()` → 记一行 「quit requested via --quit」 → 调 `on_quit`（**走与托盘退出同一条清理路径**）。⇒ **写与读两端都在役**，不是"只写请求不做 watch"。**读法纪律**：本条此前那句"没有 `--quit`"本身没错（是当时的**时点读数**），错在**没有时点**——现在按源码写成"已实现 + 文件:行号"，任何人可复验。 |
| 4.1.4 | `modules/icons/README.md` | 承诺 `make_image` / `write_app_icons(out_dir=".")`，正本实际是 `base_image()` / `make_icons(base_dir)` | 改 README 对齐正本 |
| 4.1.5 | `modules/paths/README.md` | 承诺 `<APP>_CONFIG` 由本模块支持，正本 `paths.py` 1.1.2 **没有**读该环境变量（`CONFIG_PATH` 直派 `USER_DATA_DIR/config.json`）；而蓝本 l-s2t 的 `paths.py` 里**有** `LOCALSPEAK2TEXT_CONFIG`——**模板相对自家蓝本发生了功能回退** | 已改 README 标注现状。补实现须同批同步 dsh/ocx 副本（否则 sync_check 立刻红灯），**列为待办** |
| 4.1.6 | `blueprints.txt` + `sync_check.py` | **蓝本豁免 = 永久盲区**：l-s2t 被豁免比对，模板已前进（`paths` 1.1.2 加了 `_DATA_DIR`），蓝本却停在原地且无人发现 | 豁免改为**限期**：每次模板升位后，蓝本必须回答"跟 or 不跟"并留痕；见 4.2 |
| 4.1.7 | `STANDARDS.md` J 坑 | "诊断参数冒烟过 ≠ 正常模式可跑"已记录 ef9b381 的教训，但**没有升级为条款**，导致 l-s2t 一个月后踩同款 | 已升级为 D3-01 的硬性要求 + SINGLE-04 检查点 |
| 4.1.8 | `STANDARDS.md` G4.1 条款 3（自启自愈） | 自愈的触发条件只有"注册表指向的 exe **不存在**"。当它指向一个**存在但已损坏/过期的版本目录**（本次：`release\local-speak2text-1.4.0\`，exe 在、但永远打不开）时**不会自愈**——每次开机照旧拉起坏版本 | 待裁定：自愈条件是否放宽为"指向的 exe 不是当前版本 且 当前实例处于稳定位"；或由更新器在替换后主动重写 Run 值。**在裁定前，构建脚本 `norun` 之外的一切换版本动作都要人工确认自启指向** |
| 4.1.9 | `sync_check.py`（**能力边界，比缺陷更严重**） | 它只比对**带 `TEMPLATE-FROM/MODULE` 头**的文件（2026-09-19 由对抗复核员实测反证）。因此三类漂移**完全隐身**：①工具侧无头的文件（`reme/src/modules/i18n/i18n.py` 差 303 行、`l-s2t/src/paths.py`、`src/icons.py`）；②**模板有而工具整模块缺失**（dsh/ocx 无 i18n、l-s2t 无 tray_kit/icons/paths、四工具无 autostart）；③四工具全部 `__init__.py`（模板 `from .x import *` vs 工具 `+ # noqa: F401,F403`，reme 还是具名导出）。**结论：`sync_check` 输出 "0 undeclared drift" 不能当作"一式五份"的绿灯** | 已要求扩展到 `[NOHDR]` / `[MISSING-MODULE]` 两类黄灯并把 `__init__.py` 纳入比对（1.3.0+）。**在此之前，"五份一致"必须用独立的全量哈希比对来断言**（REVIEW R1 的判定口径据此更正） |
| 4.1.10 | `sync_check.py` 第 4 盲区：**只扫 `*.py`，模块 `README.md` 全隐身**（2026-09-19 lead 用独立比对发现） | "整文件夹采纳"按定义是 **README + `__init__.py` + 代码** 三件套（B4 / 各模块 README 的"采纳步骤"都这么写），但扫描用的是 `rglob("*.py")`。实测后果：`modules/appconfig/README.md` 在 dsh/ocx 双 DIFF、reme 有 5 个模块 README DIFF。**`.py` 有哈希闸、`.md` 没有** —— 这正是最容易被漏掉的一类漂移 | 已要求把扫描范围扩到"模块文件夹内全部文件"（排除模板专属 `baseline/`、`build_release/` 与 `__pycache__`），并在 ALIGNMENT 里把"整文件夹采纳"的三件套写成正式定义 |
| 4.1.10a | 归一化规则被误用到文档上（**与 4.1.10 同源，且让"README 不带头"这条规则在实现上不可检测**） | 归一的 `^\s*#\s*TEMPLATE-` 剔除逻辑是为**代码副本**设计的（剔掉出处声明行再比哈希）。但 **markdown 标题也以 `#` 开头**，于是 `# TEMPLATE-FROM: ...` 被当成元信息**静默剔除** → "带了头的 README"与"没带头的 README"**比对结果都是 `[ok]`**，而两者字节并不相同。<br>**机制由合成样本证实**（复核员反向自证：给假工具的 `log_kit/README.md` 加一行 `# TEMPLATE-FROM: …` → 输出 `[ok]`，应为 `[DIFF]`）。<br>⚠️ **本条曾误记一起"实测触发"——写成本家族某工具"给 README 加了头"，那是错的**（该成员全程用 `cp` 逐字节拷贝，从未加头；它当时收到的 `[NOHDR]` 是"内容不同且无头"的提示，被误读成"因为缺头所以不合格"）。**机制成立 ≠ 随手指认的实例成立**——登记缺陷时，实例必须是实测的，不能由机制反推 | **口径**：模块 README 与正本**逐字节一致、不带任何头**（`.py` 靠头表出处，`.md` 的出处由所在目录说明）。**实现**：`.md` 等非代码文件**直接逐字节哈希、不剔任何行**；带头/漏拷/差异一律 `[DIFF]`，不产生 `[NOHDR]`。**交付条件**：必须附"造一个带头的 `.md` 副本 → 报 `[DIFF]`"的反向自证输出（不附即视为未完成——本条第一次交付只扩了扫描范围、没改比对语义，正是漏了这步） |
| 4.1.10b | **改名后文档未反向更新**（2026-09-19，由对抗复核员逐条读文档抓出） | l-s2t 把环境变量 `LOCALSPEAK2TEXT_*` 改名对齐规则后，**两处文档仍在写"这是唯一例外"**：① 模板 `modules/paths/README.md:18`（且被逐字节拷进四个工具，下轮 re-copy 会把旧说法带回来）；② 本文件 NAME-10 行仍标 ⚠️ 例外。**代码改了、测试绿了，旧结论留在文档里没人回头删** | 两处均已修。**纪律**：改名/删除/放宽一类改动完成后，必须**反向搜索受影响文档**（旧名、旧结论、"唯一例外"这类措辞），否则文档会持续说谎；这与 §4.1.10a 同属"文档与现实不符不会自己报错"这一类 |
| 4.1.11 | **规范张力：D1-02 闸门一旦真实生效，就必须先关掉常驻实例才能构建**（2026-09-19 实战暴露，非缺陷） | D1-02 要求"任何版本的实例都不许在构建时运行"（exe 与数据文件会被锁、两个托盘会抢同一份 config）。这条在闸门失效的时期**形同虚设**；修好之后立刻产生真实成本：`reme-dev` 为过 D1-01 删了 `release\reme-helper-1.2.6\`，修好闸门后**因用户实例在跑而再也建不出来** → 出现"`VERSION` 与 CHANGELOG 都写着 1.2.6，本机却没有任何 1.2.6 产物"的状态 | **闸门已精化（2026-09-19 用户裁定后）**：D1-02 改为"**只有当运行实例所在目录 == 本次构建的目标 `release\<工具>-<版本>\` 时才拒绝**"，构建到**新版本目录不再被拦**（依据：构建写新目录、冒烟已用隔离数据区、冒烟不占互斥体）。① 故"本地重建必须先退出常驻实例"的成本**不成立**——那是闸门**拦错对象**造成的，非必然；② **任何删除/覆盖 release 目录的动作（含手工 `rm`、未来 `--clean`）也必须先跑该守卫**——闸门原本管不到"删目录"，这正是本次事故的缺口；③ 仅当确需重建**正在运行的那个版本目录**时，才需先退出实例；④ 更新器链路（退出时替换）不受影响，因为它本就要求用户退出。措辞纪律：此处曾写"闸门正确，不改"，属**把过度保守当作设计使然**——后被用户实测质疑推翻 |
| 4.1.12 | `STANDARDS.md` G3（发版节奏）+ 四工具 `VERSION` | **"版本号"被当成工作进度而非已发布契约**：开发期顺手升号，却不打 tag、不 push、不建 Release——于是"源码写着 X、Release 里没有 X、本机也没有 X 产物"。升级检查（比 `VERSION` 与 Release tag）、`update_repo`、tag 一致性三处随之对不上。规范此前只写了"commit 累计较多才集中发版"（G3 第 6 条），**没写"未发版不得升号"** | 已补 **G3 第 7 条**（升号 + tag + push 三件事同时发生；开发期改动挂 `## Unreleased`）并在 B3 加指针。**整改已闭环（2026-09-19 复核；R-EVID：四工具 `VERSION` 实读，非转述）**：`reme-helper` **1.2.5**、`local-speak2text` **1.4.0**、`dsh-helper` **1.8.1**、`opencodex-helper` **1.2.1** —— 四家**全部回退到位**，`C-04` 由 `WARN` 转绿；本文件 §2.4 B2 登记表的 l-s2t 版本列也已由 `1.4.1` 同步为 `1.4.0`（原先正是这一格让 C-04 报 WARN）。<br>**规则本身不变**：升号而不发 Release，就是"源码写着 X、Release 里没有 X"——台账与产物对不上；开发期一律挂 `## Unreleased`。<br>**留档教训**：这条清单从"当前不符合"变成"已闭环"，靠的是**有人回头改文档**——与 §4.1.10a/§4.1.10b 同类：**整改完成后旧结论不会自己消失**，必须反向搜索受影响文档（旧版本号、旧结论、"当前不符合"这类措辞） |
| 4.1.13 | **"我没搜到" ≠ "它不存在"**：否定判定（X 缺失/未做/不存在）的证据方法（2026-09-19，lead 在本轮反复栽跟头后立） | 本轮 lead 对下级产出下了至少 8 次错误否定判定，两种成因：**① 时间错**——拿几分钟前采集的快照断言"还没做"，而对方在这几分钟里已推进（ocx 门禁、ocx 注册表、`.bak` 目录、release 目录、sync_check 版本、reme 1.2.6 产物）；**② 措辞错**——重采了现场，但 grep 用的是"我以为它会怎么写"而不是"它写了什么"（搜 `无.*1.2.6.*产物`，而对方写的是"**没有** 1.2.6 产物"）。**两者都会得出同一个假结论，且 grep 零命中时无法区分"真的没有"与"我没搜对"** | **操作性纪律（否定判定专用）**：① **不用整句/预设措辞 grep**，改用**语义片段**（`1.2.6 产物`、`frozen build`）或**整段读取**（`git show HEAD:<path>`）；② 结论**带上采集时刻**，或写成"截至 `<时间>` 未发现"；③ 涉及"提交是否落到某个状态"时用**结构命令**而非文本搜索——`git merge-base --is-ancestor <sha> HEAD`、`git reflog`、`git log -- <path>`；④ 并发场景下，"我刚才看到的"默认是过期的，**发含状态的指令前重采一次** |

| 4.1.14 | **两个派发件说不同的话：`update_helper` 的 print 形态 log ↔ `log_kit` 的单参闭包**（2026-09-19，tpl-keeper 认领） | `update_helper` 全文 **7 处**按 print 形态调用（`log("downloading", stem)`、`log("update staged:", staged, "->", target, "(bat %s)" % s)`，最多 5 个位置参数），而 `log_kit.make_logger` 给的是 `def log(message)`。<br>**裂缝长期未暴露，因为三个工具各写了一份互不相同的本地包装把它分别盖住 / 藏住**：dsh `def log(*parts)`（**兜住了**，还在 docstring 里留了"模板 log_kit 待统一"）、ocx `def _log(*parts)`（同）、l-s2t `def log(message)`（**更窄**，却照样 `log=log` 交给模板件）。**工具侧"各自将就"让模板层面的矛盾永远没有机会暴露**——这与 B4 仲裁规则里"多数派是伪裁判"同款：三份本地包装看起来像"共识"，实际是三份将就 | **已修（模板侧）**：① `log_kit` **1.0.3** 的 `log` 改 print 形态（`*parts` + 空格拼接 `str(part)`），与 `update_helper` / `tray_kit` 的调用形态对齐；② `log_kit` / `update_helper` / `tray_kit` 三个 README 的接口表写明该承诺；③ 新增机械判据 **C-29**；④ STANDARDS §J 加"替身比真实实现更宽容会盖住契约冲突——签名宁严勿宽"。<br>**真实树首跑结果**：**l-s2t FAIL**（`src/main.py:80 def log(message)` + `231`/`998`/`1043` 三处 `log=log`），并**实测**该缺陷：把单参 log 传进 `launch_pending_cmd` / `pop_failed_update_note`，模板件 L257/L390 直接 `TypeError`（对照：换 print 形态的 log 正常）——**不是机制反推，是跑出来的**。<br>**待办**：l-s2t 本地包装收窄处随 #36 修；`log_kit` 1.0.3 需级联四工具副本（`update_helper`/`tray_kit` 的 README 同步） |

| 4.1.15 | **判据的覆盖可以被"改成一个变量"悄悄关掉：`mkdtemp` 前缀 + "清一遍就好了"** （2026-09-19，tpl-keeper 认领；lead 裁定"判据可以自己失效比泄漏本身更糟"） | C-30 第一版只做"mkdtemp 根目录的清理必须可验证"（静态、可枚举），**没管前缀从哪来**。复核员的取证脚本把前缀**从源码枚举**（不猜命名：lead 第一轮猜 `opencodex-*` 而实际是 `ocx-*`，42 个一个没命中；改用"目录里只有 `*/log/*.log`"的签名又漏掉约 14 个——同类成员常带 `config.json`，`icon-probe-*` 恰好两个文件，`l-s2t-test-*` 一个 log 都没有）。**枚举口径下暴露的缺口**：`reme-helper/src/main.py:7405` 的 `prefix=f"{APP_ID}-update-"` 是 **f-string**，静态推不出——若只报 WARN，**把 `prefix="reme-x-"` 改成变量就能永久溜出覆盖**。<br>另一条同源错觉是**验收口径**："清一遍就好了"。它是**时点论**：lead 在 16:11 测得 dsh 的 3 个残留目录 mtime 正是 **16:11**（门禁运行当口 ⇒ 当时确实在产生新的）；tpl-keeper 晚些时候用同一批前缀（19 个）复扫得到 **0 命中**——两个时点都成立，**都不能替对方下结论**。只看"现在 %TEMP% 干不干净"既会因历史存量假红、也会因刚清过假绿，所以验收必须是**增量** | **已落**（`conformance_check.py` **1.9.0**，C-30 拆上下两半 + 运行期验收）：<br>① **上半（静态）**：枚举 `mkdtemp` 的 `prefix` 实参——**含包装函数调用点**（`tests/_cleanup.py: scratch_dir(prefix)` 的前缀全在调用点上，dsh/ocx/l-s2t 三家真身）。推不出的站点必须在模块级字面量 **`TMP_PREFIX_REGISTRY = {"<相对路径>:<行号>": "等价前缀"}`** 登记，**不登记即红**；登记值非字面量（判据读不到）= 红；登记了对不上站点（行号漂移）= WARN。判据**同时读这张表**，运行期取证也读它。<br>② **下半（静态）**：扫描范围 `tests/` → **全工具**，真实树立刻多出 **reme `src/main.py:7409` `rmtree(work, ignore_errors=True)`**（`work` = 7405 的 mkdtemp 根，下载/校验失败的早退路径）——同一缺陷的生产代码形态，原来整个溜过去。<br>③ **运行期（R-10，属各工具 `build.bat`）**：`--temp-leak-save` 记基线 → 跑完 `--temp-leak-baseline` **只对新增报红**（残留免疫）；`--temp-leak` 单跑只是取证（列出命中、**永远 exit 0**，因为"历史存量"不该判红，而"清一遍"不是证据）。<br>**真实树首跑**：C-30 **1 FAIL（reme，两处：7405 未登记 + 7409 吞错）**，其余三工具 ok（dsh 6 / l-s2t 9 / ocx 6 个根目录清理可验证）；工具自身的 selftest 临时目录也改成 `_rmtree_strict`（判据作者自己守 C-30）。<br>**归属**：reme 两处属 **#37** 范围；运行期增量断言属 **#34/#36/#37** 的门禁接线 |

| 4.1.16 | **"没人查的一致性一定会漂"：模板派发件的行尾无人检查**（2026-09-19，lead 批准加判据） | `log_kit.py` 被编辑器**整文件重写**成 LF-only：`py_compile` 绿、`sync_check` 两边同为 LF 也 `[ok]`、C-22 只盯 `.bat`/`.cmd`——**四层判据全绿而字节已经变了**，靠"读回字节"才发现（`CRLF=80 / LF-only=0`）。**机制**：拷贝式分发下正本的行尾 = 四份副本的行尾，所以"漂"会被原样放大四倍；而"没人查"的这类一致性**必然漂**（本家族当晚已第二次：C-22 的 bat、本条的 `.py`/`.md`） | **已落** `conformance_check.py` **C-31（WARN）**：派发件（`modules/**` 的 `.py`/`.md`，排除 `build_release/`、`baseline/`）必须全程 CRLF，逐文件报"首个 LF 行号 + LF/CRLF 计数"；样本 4 条（CRLF ok / LF-only / 混合 / 模板专属目录不误伤）。<br>**首跑真实树：4/27 命中**——`modules/autostart/autostart.py`（66 行全 LF）、`modules/icons/icons.py`（63）、`modules/service_link/README.md`（58）、`modules/service_link/service_link.py`（123）；**且工具侧副本同样是 LF**（dsh/ocx/l-s2t 的 `autostart.py`、reme 的 `service_link/*`）。<br>⚠️ **修法约束**：只把正本改成 CRLF 会让 `sync_check` 对这些副本立刻 `[DIFF]`——必须**正本 + 全部受影响副本同批**处理，即一次"可重拷"冻结事件（先改完 → 再冻结 → 最后宣告）。在裁定该波次之前，本条以 WARN 长期可见 |

| 4.1.17 | **泄漏判据的"结构性天花板"：前缀法的覆盖上限 = 源码里出现过的前缀字面量**（2026-09-19，lead 实测后裁定补腿；task #43） | 前缀法（"从源码枚举 `mkdtemp(prefix=...)` → 逐前缀 glob"）被当成"免疫误报"的正解，但实测它**必然假绿**：lead 用 `ocx-*`/`dsh-helper-*`/`local-speak2text-*`/`reme-update-bat-*` 等前缀扫 → **0 命中**，三家据此宣称"泄漏 = 0"；改用**不看名字的结构签名**复扫 → **20 个**。两类盲区：(i) 固定名/自定义名 scratch（`reme-gate-2.2.0`、`icon-probe-*`、`smoke-proof-*`）——四个工具源码里**一个字都搜不到**，它们来自**扫描范围之外**的探针脚本或裸 `mkdtemp()`；(ii) 裸 `mkdtemp()`（系统默认前缀 `tmp`）。⚠️ **2026-09-19 第二次更正（lead 自我更正 + ls2t-dev 判别实验）**：本条原先写的第二类盲区是「未申报前缀的裸 `mkdtemp()` → `tmp*`」——**这个归因被证伪了**：`GNU mktemp -d` 造出 `tmp.gVxHfxTMya`（**带点** + 10 字符），而 Python `tempfile.mkdtemp()` 造出 `tmpigscx7m2`（**无点** + 8 字符）；当时那 8 个残留**全是"带点"形态 ⇒ 出自 shell `mktemp -d`**，且该仓源码里**没有任何裸 `mkdtemp()`**。**正确的表述**：生成器派生腿的天花板**不止**是「源码里出现过的 prefix」，而是 **「它只看我们枚举得到的源码」**——**由 shell 命令（`mktemp -d`）、外部 CLI、探针脚本产生的东西，源码里根本没有可枚举的调用**。所以 **形态腿是唯一能覆盖这一类的那条腿**；并且腿 B 命中必须打印**名字形态直方图**（带点 / 无点 / 其他；实测：shell 3 / Python 1 / 家族前缀 4），否则只知道「有残留」、不知道**该去改谁**（进程规则 vs 仓库代码）。。**"前缀法 0 命中"与"真的没泄漏"在输出上完全同形**——判据可以自己假绿 | **已落**（`conformance_check.py` 1.9.0）：① 运行期取证**两条腿**（腿 A 生成器派生 + 腿 B 形态派生），且**必须打印扫描面**（`%TEMP%` 路径 / 顶层目录数 / 前缀数 / 每腿命中数 / 并集）；② 腿 B 签名经**实物标定**：`<顶层>/<恰好一个子目录>/config.json` 且顶层下**存在** `*.log`。当时实测 **112 个顶层目录**上腿 A = 0、腿 B = **20/20 回归集命中、零误报**；把签名写成"`log/*.log` **非空**"则只覆盖 **11/20**（漏的全是 0 字节 log——空文件/空目录同样是残留，与 C-30 第一版口径一致）；③ 20 个残留已登记为**负样本回归集** `_TEMP_REGRESSION_20260919`，selftest 用其中的真名（`icon-probe-077hxtaw`）作样本证明"不看名字也能命中"；④ 裸 `mkdtemp()` 由 FAIL 改 **WARN**（推得出但很弱，主判据是腿 B）。**清理侧**归 #36/#37/#42：先判活进程占用 → 删 → `try/finally` → 汇报"清理前后列表 + 扫描面"。<br>⚠️ **2026-09-19 腿 B 放宽（lead 报"固定名 scratch 目录漏检"后，用合成形状实测）**：旧签名多写了一条"**恰好一个子目录**"，而那是**形状的偶然特征、不是不变量**——任何多一个子目录（如 `ui-icons/`）的数据根都会隐身。合成形状实测：`log/{config.json,app.log}` HIT；**加一个 `ui-icons/` → MISS**；**`config.json` 摆在顶层 → MISS**（后两者都是真实形态）。新签名 = **`config.json` 在顶层或其一层子目录内 + 顶层下至少一个 `*.log`**。当日 93 个顶层目录实测：旧 4 命中 / 新 7 命中，**新增 3 个全是 `marker-e2e-*`（此前完全不可见的残留，不是误报）**；残余 FP 风险写进注释（外来程序的"config + log"临时目录），弱前缀 WARN 保留。<br>⚠️ **2026-09-19 第二次放宽（复核员实测后，lead 转达）**：上面那条仍要求"`config.json` 在 ≤1 层"，且靠 `rglob("*.log")` 找 `*.log` **文件**——复核员报的真实残留 **`tmp.6FcrxXYxmM\d\local-speak2text`（3 层、只有 `log/`、没有 `config.json`）** 两种写法**全抓不到**。**候选口径在同一次扫描上实测对照**（顶层目录 95 / 条目 647）：V0 旧签名 **7** 命中 / V1「任意深度存在 `*.log` 文件」**13** 命中（多出的 6 个里 5 个是**他程序的日志**：`WinRAR.exe.WebView2/EBWebView/…/000003.log`、`vmware-Administrator`、`virtual_camera`、`kzip_sogou`、`ai/rp/task_outputs/…/output.log` ⇒ **太宽、制造假红**，否掉）/ V2「任意深度存在 `log` **目录**」**8** 命中 ⇒ **采用 V2**：**不再要求 `config.json`、不设深度上限**（B3 规定日志一律落 `<数据根>/log/`，所以"有 log 目录"才是数据根的不变量）。残余 FP = 外来程序自己的 `log/`（现场 1 个，`kzip_sogou`）。<br>⚠️ **同一批更正两处口径**：① **扫描面必须报"目录数"**——lead 曾把顶层**条目数**（目录+文件，634）当成目录数（101）报出，导致两张扫描面不可比；现在两个数**各带标签**一起打印。② **回归集 20 个是"自标定集"**（规则拿它标定、再用规则命中它 = **循环**），**不构成独立验证，不得声称"零误报"**；独立复算由复核员给出 = **14**（16:55，他重实现）。③ `reme-helper-builddata` **已从回归集移除**并移入 **`TMP_DECLARED_PATHS` 白名单**：它是 reme `scripts/build.bat:22` **明写的稳定构建数据位**，不是漏扫残留——复核员的对照实验给了这条硬结论：**形态腿能识别"数据根"，但分不出"该在 %TEMP% 临时"与"该持久/该按声明保留"**，所以**判"是不是泄漏"必须靠位置 + 声明**。<br>⚠️ **第三次更正 + 一条样本口径（2026-09-19，复核员 43 样本定案）**：本条的"盲区清单"被我（lead）前后写过三版：① 只有固定名 → ② 加"无前缀 `mkdtemp()`" → ③ "全是 shell 造的"——**三版各对一半**。复核员扫了 `%TEMP%` 顶层**全部 43 个 `tmp*`**（**样本来源：本机 %TEMP% 顶层；样本量：43**）后定案：**两个种群并存**——`tmp.` + 10 位 `[A-Za-z0-9]`（**带点**，总长 14）= **40 个** ⇒ GNU shell `mktemp -d`；`tmp` + 8 位 `[a-z0-9_]`（**无点**，总长 11）= **3 个** ⇒ Python `tempfile.mkdtemp()`。**关键指纹**：`tmp_8qhz_0a` 里的**下划线**（GNU `mktemp` 的字母表**不含 `_`**，Python 的**含**）。⇒ 三个无点无前缀样本 `tmp0whlwvmi` / `tmpigh0g540` / `tmp_8qhz_0a` 已登记进回归集：它们同时验证**形态腿能抓到 Python 残留**与**生成器腿永远抓不到**，比只放 shell 形态更有区分力。<br>**通用口径（本轮方法论）**：判据文档里凡出现「我们观察到的形态是 X」，**必须同时标注"样本来源"与"样本量"**——否则下一个人拿另一批样本就能把它推翻，而两批样本都可能只覆盖了一个子集（本条连翻三次车就是这么来的）。同族的现成例子：本文件里凡是"实测 N 个""扫描面 M 个"的句子，都应带出处；`--temp-leak` 的**扫描面 + 名字形态直方图**就是这条口径在运行期的落地形态。<br>⚠️ **2026-09-19 第四条边界（复核员定死 3 个无点 tmp 的生产者后）**：`tmpigh0g540` / `tmp_8qhz_0a` 出自**一条 for 循环里的 `python -c`**（两轮各一次 `tempfile.mkdtemp()`，同秒 ctime、都为空）；`tmp0whlwvmi` 出自 `_verify-scratch` 里**一条 heredoc 探针**（设 `REME_HELPER_DATA_DIR=mkdtemp()` 后 `import main`）。**共性：`python -c` / heredoc 从不落盘** ⇒ **任何"扫源码"的原理都不可能覆盖它们**（扫描面里没有对象）。⇒ 生成器腿的天花板**不止**是「扫不到不在源码里的前缀」，而是 **「它只能看见以文件形式存在的生成者」**。<br>**三条腿的分工**：**生成器腿** = 落盘的、可枚举的生成者；**形态腿** = 落盘的残留（不看名字）；**生产者自我标识 = 不落盘的生成者**——靠**产物自带的日志**回指"这一次运行读的是哪个数据根"（见 **C-38**）。**第三条不是补充，是唯一能覆盖这一类的那条路。**<br>⚠️ **2026-09-19 两条口径（复核员实测触发）**：**（A）任何「命中 N 个」的转述都必须自带时点**——**残留集是活的**：lead 广播 reme 残留 **8** 个，**当前是 5**（消失 4：`reme-gate-2.2.0`/`reme-neg-ctl`/`reme-sync-2.2.0-check`/`reme-helper-builddata`；新增 1：`reme-gate-final`；5 = 8−4+1 ✓）。**本轮第二次栽在这上面**（第一次：C-30 的「16:11 三条 vs 稍后 0 条」）。与「0 命中必须打印扫描面」同族：**扫描面说"扫了什么"，时点说"什么时候"**，两者齐了读数才可判。**机械形态**：身份行加 `at:<ISO 时间>`（`conformance_check.py` 1.9.4），任何贴回来的 `--temp-leak` 输出第一行就自带时点。<br>**（B）"删了会自动重建"的那一类不该进清理清单**——`reme-helper-builddata` 是 `reme\scripts\build.bat:22` **明写的固定路径**（lead 先前算成泄漏 = **假阳性**，已更正；它现在从 TEMP 消失，因为下次构建会重建）。**口径**：对**声明过的、且会自动重建**的位置，正确处置是**进白名单**（`TMP_DECLARED_PATHS`），**而不是要求清理**——**"清理"既不持久，又会产生虚假的进展感**（看起来清干净了，下次门禁又长出来）。**"清理清单"只收"不该存在的残留"。** |

| 4.1.18 | **判据存在 ≠ 被检查对象在范围内**（2026-09-19，lead 裁定并留档） | C-28（`.md` 不得含 TAB）只扫四个工具——`main()` 里 `d.name not in {"__pycache__", TEMPLATE_DIR.name}` **把模板仓显式排除**，于是**模板自己的 `.md` 从未被扫过**，而模板正是"四份副本之源"。这与"`sync_check` 只比副本像不像、不查正本自相矛盾"是**同一家族**：**盲区不是缺判据，是判据的适用范围没被检查**。本轮已连续两次撞上它（C-28／C-30 都只覆盖工具侧，模板正本只在 `sync_check` 的比对里出现） | **已落**：给框架加 `TEMPLATE_CHECKS` 注册表——模板判据在 `main()` 里**只跑一次**（`Ctx.dir` = 模板仓根），不跟着四个工具重复刷 N 遍；C-28 按 lead 的"最省事形态"补扫模板仓（不为此给模板开整轮：它没有 `src/` + `build.bat`，整轮会空转甚至误报），C-31（派发件行尾）也走这条通道。**纪律**：新增/改动任何判据时，必须回答"**它的适用范围（roots）是谁定的、正本在不在里面**" |

| 4.1.19 | **不可逆动作排在"调用边界可能失败的语句"之前**（2026-09-19 立；口径由 lead 的宽版收窄为复核员版） | 形态：`detail = marker.read_text(...)` → `marker.unlink()` → `log("previous update failed:", detail)`。**危险不在"log 会不会失败"，而在"调用边界会不会先抛"**：arity/签名不符、属性不存在、名字未定义这类错误在**进入被调方之前**就抛出，**被调方内部的 try/except 保护不了它**——C-29 契约冲突下 l-s2t **真的炸了**（`TypeError` + marker 已删 + 提示消失，实测）。**宽版为什么被否**：lead 原表述"不可逆动作必须排在**所有可能抛异常的语句**之后"会把 `quit_watch_loop` 的 `unlink → log`（模板 + 4 份副本）误报 5 处——`log_kit.log()` 内部 `try/except Exception: pass`，**它本函数不抛**。修完 C-29 后这类危险退化成**潜伏态**，但下次契约冲突会以同样方式炸 | **已落** `conformance_check.py` **C-32（FAIL）**：窄版 D/A/R 三条（见 §5.1 行），样本 7 条覆盖真形态、reme 旧形态、`log` 在删之前、只删不读、读了不 log、接收者不同、幂等删除。**已知站点 5 处（复核员实测 5/5 全真、零假阳性）**：模板 + dsh + ocx `update_helper.pop_failed_update_note()`（三处，**当前仍在役**）；l-s2t `updater.pop_failed_update_note()`、reme `_report_failed_previous_update()`（**历史上真阳性**：l-s2t 那条有实测 TypeError + marker 消失；两处**当前代码已修**为先 log 后删）。**修法约束**：模板整改后必须与 dsh/ocx 副本**同批**（同 C-31 的"可重拷"冻结约束）<br>**两条检测器教训**（lead 批准入本栏）：① **样本必须抄真实现场的形状**——C-32 首版零命中，就是被真实现场的**链式包装**（`marker.read_text(...).strip()`，读与用法不在同一条语句里）挡住的；用**想象出来的形状**写样本，只会得到「全绿但漏掉真案」，与「0 命中 vs 没扫」同族。② **别做全局子串匹配，要认分支**——读与 `log` 之间夹一个 `except OSError: return ""`，文本匹配看不见这个分支，**分支感知**（AST/控制流）能看见：那条 `return` 意味着「读失败时根本走不到 log」，与「读了、删了、才 log」性质完全不同。<br>**C-32 窄版的最后两条限定，各自的论证（lead 补，免得后人以为漏了）**：① **为什么取消幂等豁免**：`detail = read_text(); unlink(missing_ok=True); log(detail)` **仍然是同一缺陷**——危害不是「内容读不到」（内容已在 `detail` 里），而是**「证据在被报告出去之前就被销毁」**：`log(detail)` 一旦抛异常（本家族真发生过：l-s2t 那次 C-29 可变参数 `TypeError` 就是 `log` 自己抛的），栈展开、`detail` 没了、**文件也已被删 ⇒ 下次启动再也报不出来**。而「先 log 后删」之所以是正解，正在于 **log 抛异常时文件还在**、下次还能重报。所以 `missing_ok` 管的是 **删的幂等性**，与这条危害**无关**。② **为什么取消「同一语句块 / 中间无 return」的限制**：A 在函数内**文本更早**且 D 可达 ⇒ **A 在通往 D 的路径上必然已执行**——若 A 与 D 之间存在 `return`，那条路径**根本走不到 D**，而**非 return 路径上 A 照样先于 D 执行**，那正是真阳性。所以放宽不会制造「A 不可达 D」的假阳性；实证也同向（加「同一语句块」限定后命中 0）。<br>**⑦ 的结案（登记为假阳性，别再翻案）**：`reme main.py:7409 rmtree → 7450 log` 经复核员判定为**假阳性**（7409 在嵌套函数 `_fail()` 里，与 7450 是互斥路径），lead 已通知 reme-dev **保持原样别改**；它**不属于 C-32**（7409 是 C-30 下半的真阳性：`rmtree(work, ignore_errors=True)`）。两者别混：**同一条行号在两套判据里结论相反，是因为判据问的问题不同**。 |

| 4.1.20 | **等待/超时的单位假设没人量过：`ping -n 2` 不是「1 秒」**（2026-09-19，ls2t-dev 发现、lead 独立复测） | `_APPLY_BAT` 的等待节拍写成 `ping -n 2 127.0.0.1 >nul`，本意「睡 1 秒」。实测（lead 复测）：`cmd /c 'ping -n 2 127.0.0.1'` = **9.04s / 9.00s / 9.00s**，输出「数据包: 已发送 = 2，已接收 = 0，丢失 = 2 (100% 丢失)」——**loopback ICMP 全丢**，于是每个包等满 4.5s 超时。后果：节拍名义 1s 实际 **9.0s**（差 9 倍）、`UPDATE_WAIT_LIMIT = 120` 的「120 秒」实际 **约 18 分钟**、`:giveup` 打印 `after {limit}s` **与实际相差一个数量级（日志说谎）**。**同一句在模板 + 四份副本**（dsh/ocx 的 `update_helper.py`、l-s2t `updater.py`、reme `main.py`）。**只在 ping 慢/被拦的机器上暴露**，本地实测很容易看不到 | **已修（模板侧，1.9.0 批次）**：① 节拍换成不依赖 ICMP 的 `powershell -NoProfile -Command 'Start-Sleep -Milliseconds 1000'`（DETACHED 无 console，子进程不弹窗；本机实测每拍 1.29s，含 PowerShell 启动费）；② 常量拆成 `UPDATE_WAIT_LIMIT`（**轮询次数**）× `UPDATE_WAIT_TICK_MS`（每拍毫秒）= `UPDATE_WAIT_BUDGET_S`（名义预算，**下界**），注释写明「别把次数当秒」；③ `:giveup` 改成 `after %tries% polls x {tick_ms}ms (nominal budget {budget_s}s, lower bound)`——**不再打印一个没人量过的「秒」**；④ 新增机械判据 **C-33**（禁 `ping` 当节拍，注释/`rem` 不算）；⑤ `sync_check.py` 的 bat 语义断言同步改成 `Start-Sleep -Milliseconds`。**其余四份**由各自仓库随本轮「可重拷」波次同步（reme 还有 `scripts/build.bat` 一处 `ping -n 9`））<br>**⚠️ 后续那批 C-33 红全是假红（必须记在这里，否则后人看到“曾有 6 FAIL”会以为真出过六个违规）**：2026-09-19 晚 C-33 增量一批红，**真因是判据的「豁免边界」画错**——`_code_only_text` 的设计是“不碰 STRING token”（理由正当：渲染 bat 的 python 模板正是字符串），而 **docstring 同样是 STRING** ⇒ **解释这条修复的散文被当成了可执行节拍**；`modules/update_helper/update_helper.py` 那处更是“**越把原因说清楚越违规**”。读数必须带尺子（§4.1.36），两个读数都记上：**lead 转述为“6 FAIL”**；**我用当时的工具实测**——默认调用 **2 FAIL / 2 WARN**，`--only C-33 --roots my-diy-tool-template` 下自命中**5 处（均在 `conformance_check.py` 自身：1 docstring + 1 诊断文案 + 3 自证样本）**。修法见 §4.1.37（挖 AST 裸字符串表达式 + 掩码保行号 + 评据排除仪器自身）。**修后实测（本日）：C-33 全树 0 红**——模板侧渠道 1 行 + 四工具各 1 行均 `[ok]`，连“把模板当工具根”的 `--roots my-diy-tool-template` 也是 0 FAIL。**下一个人看到那批红，请当作“工具缺陷”看——它们一条都不是。**<br>**第二个实例、方向相反（lead 2026-09-19 要求并列）**：`ping` 那次是**等得太久**（9.0s/拍、名义 120s 实际 ~18 分钟）；`>dev/null` 这次是**根本没等**（`rc=0` 但 0.03s、`powershell` 未执行，120 拍几秒烧完）。**两者共同点**：**“等待/超时的单位假设没有被实测过”**，而且**日志都照旧打印一个不成立的“秒数”**（一个是“说 120s 实际 18 分钟”，一个是“说 120s 实际几秒”）。⇒ 斗争结论：**不要只量“等了多久”，还要量“**那条命令到底执行了没有**”**。 |

| 4.1.21 | **清扫器前缀少写一个字符 = 一类产物永久漏扫，而且完全无声**（2026-09-19，helpers-dev 发现；`update_helper.sweep_stale_update_dirs`） | `TEMP_PREFIX = f"{APP_ID}-update-"` 带了**尾随 `-`**，于是 `glob("<APP_ID>-update-*")` **永远匹配不到**替换脚本 `<APP_ID>-update.bat`（固定名，中断的更新留下的就是它）；而清理分支只写 `is_dir()` ⇒ **每中断一次就永久多一个 `*-update.bat`**，且没有任何输出。两类产物的**唯一共同前缀**到 `-update` 为止（暂存目录是 `-update-<随机>`，脚本是 `-update.bat`）| **已修（模板 1.4.3）**：`TEMP_PREFIX` 去掉尾随 `-`，sweeper 同时处理目录与文件（`rmtree` / `unlink`），年龄闸（`st_mtime >= cutoff` 跳过）不变。**实测正/负对照**：`TMPDIR` 重定向后造 3 个过期产物 + 2 个新鲜产物 → `removed = 3`，新鲜的**一个都没动**。教训：**"清扫器跑过了" ≠ "该扫的都扫到了"**——清扫类代码必须配一个"本该被扫到"的正样本，否则漏扫与干净在输出上同形（同 §4.1.17）|
| 4.1.22 | **自愈的两处"不出声"：`except: pass` 让"本来就没这条"与"读失败"同形；`value == wanted` 短路放过死链**（2026-09-19，tpl-keeper 认领；`autostart.migrate_autostart` 模板 1.1.2） | 两个独立缺陷：①条目不存在（用户自己关掉了自启 / 被杀软清掉）时静默返回——**不自动创建是对的**（自动创建等于替用户把他关掉的自启重新打开），但 `except (FileNotFoundError, OSError): pass` 把**读失败**也吞成静默，两种情形在日志里**完全同形**（都是什么都不打印），现场无法区分；②判据 `value != wanted and not os.path.exists(value.strip('"'))` 里 `value == wanted` 会**短路**——注册值恰好等于当前值、文件已被删（旧包目录被整体改名/搬走，路径字符串恰好没变）时**永不修复**；且 `strip('"')` 对**源码态命令行**（`"…\pythonw.exe" "…\main.py"`）得到的是不可能存在的路径 ⇒ 源码态**每次启动都判"已消失"并重写一次** | **已修（模板 1.1.2）**：①条目不存在 → 记一行日志、**不写注册表**；读失败 → 记一行**不同**的日志（两者不再同形）；②新增 `_cmd_exe()` 取命令行**第一个 token**，判据**只看目标文件是否存在**（去掉 `value != wanted`），重写后**复查**新目标、仍不存在就如实报告（不谎报 `migrated`）。三份副本（l-s2t/dsh/ocx）随本波"可重拷"同批 |

| 4.1.23 | **§1（L1）的"版本"列没有判据 ⇒ 9 行里 6 行落后**（2026-09-19，tpl-keeper 复核发现） | §1 是本文件最像"契约"的一张表（模板件 / 能力 / **对外接口稳定承诺** / 版本），但**版本列从来没有被打过**：C-04 只查四工具的 B2 表，模板通道只跑 C-28/C-31/C-32/C-33。实测（逐文件读头部 `TEMPLATE-VER`，非转述）：`appconfig` 1.0.0→**1.0.1**、`paths` 1.1.2→**1.1.3**、`update_helper` **1.0.1→1.4.3**、`i18n` 2.1.0→**2.2.0**、`tray_kit` 2.0.1→**2.2.0**、`log_kit` 1.0.2→**1.0.3**、`sync_check` 1.2.0→**1.8.3**（`autostart`/`icons`/`service_link` 三行本来就是对的）。**危害不是难看**：`update_helper` 那一格写着 1.0.1 而磁盘是 1.4.3，读者会按 1.0.1 的语义去理解接口——而 1.0.1 正是"两处静默失效"的那一版（B4 仲裁规则的反例原型）。这与 §4.1.18 同族：**判据存在 ≠ 被检查对象在范围内**；也与 §4.1.10b 同族：**文档落后于代码不会自己报错** | **已修**：9 行 + `sync_check` 行按磁盘 `TEMPLATE-VER` 逐格同步，补 `conformance_check.py` 一行（原表列了 `sync_check` 却不列它，而它才是跑这张表的人），`paths.process_pending_update()` 标 ⛔ 已弃用（§4.1.5 的处置第二步已落：模板 `paths.py` 1.1.3）。**顺带一处未遂错**：我按"方法调用"的直觉把 `service_link` 的 `.spectators` 写成 `.spectators()`，回读源码发现它是**属性**（`self.spectators = []`，第 50 行）——按 §D7 第 8 条（枚举签名、不猜）已改回并加注。**待办（建议下一轮，不擅自并进本波）**：加 **C-34**（模板通道）：解析 §1 表各行，断言"表内版本 == 该文件头部 `TEMPLATE-VER`"，不匹配即 WARN——否则这一列一定会再漂 |

| 4.1.24 | **口径写成散文 ⇒ 收方各自实现、各自算出假红**（2026-09-19，lead 提议、tpl-keeper 落地） | `.py` 归一化口径在文档里被描述过两次、**两次都不完整**：第一次漏"补不补尾换行"，第二次漏"换行要不要归一"。后果都是同一种：**认真自证的收方报出假红**——复核员自己实现算得 `49b778fc7b26`（先 `decode()` 再 `split("\n")`，CRLF 副本没归一）、`e636cb41bf50`（同因），而 dsh/ocx 明明已经拷对。**根因**：散文与代码是**两份描述**，且散文先漂（设计纪律 ⑦ 的同族） | **已落（两道防线）**：① `ALIGNMENT.md §0` 把口径改为**指向唯一实现**（`sync_check.sha256_text()`），并写明"**收方不要自己重实现这个算子**，跑 `sync_check` 取 `[ok]/[DIFF]` 就是权威判定"；② 新增 **C-36**（模板通道，FAIL）：**性质断言代替散文**——取任一模板 `.py` 正本内容，断言 `sha256_text(LF) == sha256_text(CRLF) == sha256_text(CR)`，**且不等于** naive `split("\n")` 控制值（否则"恒返回常数"的实现也能通过 ⇒ 判据无区分力）；扫描面打印算子名 + 样本文件 + 三种变体哈希 + 控制值。样本 2 条：真算子必须 ok、**变异算子（`splitlines()`→`split("\n")`）必须不 ok**（这一条就是判别力的自证）|

| 4.1.25 | **同一份登记表里两个 `R-07`：ID 不唯一 + 同一判据两份描述（其中一份是旧的）**（2026-09-19，tpl-keeper 在准备"把 R-07 条文粘贴给三家"时发现） | ① **撞号**：§5.2 早有一条 `R-07 = i18n 覆盖（--lang-audit missing == 0）`；我当天又把"`%TEMP%` 残留的**增量**断言"也写成 `R-07`，还把它**塞进了 §5.1（静态表）**——它要跑 `build.bat`，属运行期。于是同一文件里两个 `R-07`，其中一个还进错表。**这条差点被发出去**：若照原样发给三家，三家会拿到一个"在同文档里指向两条规则"的号。与 §4.1.18/§4.1.23 同族——**"索引里缺条目"是盲区，"索引条目本身不唯一/错位"同样是盲区**，而这一格从没被打过。② **同一条判据两份描述**：§5.1 那行仍写着腿 B 的**旧**签名（"恰好一个子目录"），而实现当天已按合成形状实测**放宽**为"`config.json` 在顶层**或其一层子目录内** + 顶层下至少一个 `*.log`"（§4.1.17）——**代码与文档是两份描述，先漂的又是文档**（设计纪律 ⑦ 的同族，与 §4.1.24 同款）。③ **ID 没有分配处**：`C-34` 现被两处独立提议各占一次（§4.1.23 的"§1 版本列"与 lead 的"Node CLI 超时余量"），若两条都实现就是第二个撞号 | **已修**：新条定为 **`R-10`**（`R-07` 归 i18n，不动既有的号），**移入 §5.2 运行期表**并按登记号续在 `R-09` 之后，腿 B 描述同步为实现口径，两处引用（§4.1.15 的 ③、C-30 行）一并改号，行内留"登记沿革"。**待办（不擅自并进本波）**：给判据 ID 一个分配处（或一条唯一性判据）——否则下一对撞号还会在"发条文"这种最不该出错的时刻暴露 |

| 4.1.26 | **"按约定关的"与"误触"在事后单看状态值同形：dsh 的开机自启在目视验证窗口内被关**（2026-09-19，用户裁定） | **事实链**：dsh-helper 的开机自启在 `09:01:41` 被关闭（**它自己的日志有显式记录**），落在此前的 GUI 目视验证窗口内；复核方按"疑似误触"把它恢复为开启，**该归因被用户否掉**——那不是误触，正是**既有约定**要求的动作（debug 前先关掉会引发"启停"的东西，免得软件启停打断正在使用的服务）。<br>**两个洞**：① **约定没有写下来** ⇒ 按约定做的动作，事后从状态值上只能读成"误触"（**"谁关的、什么时候、为什么"没有出现在任何证据里**）；② **协议里没有把自启列为快照项**（只列了 `ui_lang`）⇒ 它被改了**无人发现**，直到 #42 排查才暴露。**"清单漏一项"等于"那一项的状态没有证人"**。<br>**用户给的通用规则**：不能决断 / 不记得原状时，**取"影响最小"的一侧**，判据是**服务优先级最高** → 自启这类开关**默认取"开"**；理由是两侧不对称——**"误开"可由工具在下次启动时自然接入而自愈**（reme-helper 会自动接入 reme），**"误关"会让用户重启后服务起不来且没人知道**。推论：**服务可用性 > 用户界面状态的精确还原**（**排序**，不是并列的价值）。 | **已落**：`STANDARDS.md` **§D3.4**（debug/验证期状态开关纪律：① 测前先关启停动作 ② 恢复规则与"服务优先" ③ 排序 ④ **恢复的前提是先有原值** ⇒ 协议必须带快照清单）；本文件 **§5.3.1 状态快照清单**（S-01 `ui_lang` / S-02 **HKCU Run 键** / S-03 服务与隧道托管如 `quit_stop_tunnels` / S-04 会被点击改动的 config 键）+ **M-05** 行。<br>**家族关系**：与 **§D3.2「守卫失败方向 = 打开」同源**——都是"**不确定时的失败方向**"：守卫朝"能开"，状态恢复朝"服务在"。 |

| 4.1.27 | **"检查异常"与"检出违规"在汇总里只差一个词，处置方向却正好相反**（2026-09-19，lead 批准立档） | 实例：`check_md_tabs(root: Path)` 是**普通助手**，重构后它头上**留着 `@check` 装饰器** ⇒ 注册表把它当判据，四个工具各拿 `Ctx` 调它 → `AttributeError` → 汇总里冒出**四条"检查异常"**，**看起来像四个工具都坏了**，整整一轮的排查方向是错的（真凶是判据自己）。<br>**根因**：注册表是**动态**的（装饰器即注册），"函数存在"与"它是不是一条判据"在源码文本上**看不出区别**；而汇总把"仪器故障"与"被测物违规"印在同一栏、同一个词形（只差几个字）。**同族**：与"0 命中 vs 没扫"、"替身比生产宽"一样——**结果看起来像结论，其实只是仪器坏了**。 | **已落**（`conformance_check.py` **1.9.2**）：新增 **[BROKEN] 档**——判据自身抛异常时独立成档（诊断写"检查异常（仪器故障，非检出违规）"），**进汇总计数**（`summary: N FAIL, M WARN, K BROKEN`）**且独立进退出码**（`if broken: return 1`）。**为什么必须进退出码**：否则它会退化成"一条看着吓人的 WARN"，被调用方咽掉。自检样本：一条故意抛异常的判据必须得到 `(0 FAIL, 0 WARN, 1 BROKEN)`。**同批**：本文件 selftest 收尾**消费 `_rmtree_strict` 的返回值**（原来只调用不看结果——正是 C-30 要治的形状）。**§J 留档**见「幽灵判据」 |

| 4.1.28 | **我自己的读数也有口径错：报"条目数"当"目录数"，以及把自标定集当成独立验证**（2026-09-19，lead 自我纠正后转达复核员取证） | ① **口径错**：lead 报"扫描面 **643** 个顶层目录"，实测是**条目数**（目录+文件；**目录 101 / 条目 634**）；复核员与 tpl-keeper 给的 **112 / 94** 是**目录数**——三个数**看起来同量纲**，实际不是。而扫描面恰恰是"两个人各贴一份、要求**可比**"的东西（详见 §J「报了数，却没报这个数的口径」）。② **循环验证**：回归集那 20 个是**拿它标定规则、再用同一条规则命中它**，**不构成独立验证**，因此**不得声称"零误报"**（独立复算 = 复核员**重实现**得 **14**，16:55）。③ **误判已声明位置**：`reme-helper-builddata` 被算作残留，实为 reme `scripts/build.bat:22` **明写的稳定构建数据位**。 | **已改**（`conformance_check.py` **1.9.2**）：① `--temp-leak` 的 `RESULT` 行两个数**各带标签**一起打印（`扫描顶层目录 N 个（顶层条目 M = 目录+文件）`）；② 回归集注释改为**自标定**措辞，并移出 `reme-helper-builddata`；③ 新增 **`TMP_DECLARED_PATHS` 白名单**（豁免**报告与增量判定**，不改判据——不登记就永远红，登记了就永远有出处）。**纪律**：① 报数必须**带口径标签**；② 凡用于"可比性"的数（扫描面/覆盖率/命中率）必须**同时给出分子与分母的定义**；③ **证据必须自带"怎么读它"**——缺口径的数字，与缺修订号的哈希是同一类东西 |

| 4.1.29 | **「别删正在运行的那个实例」曾只是纪律：内核本来就能替你拒绝**（2026-09-19，lead 批准、helpers-dev 实测） | 事故形态：实例**仍在其中运行时**，`release\<工具>-<版本>\` 被掏空。当时的防护只有**纪律**（「构建前先退出实例」），而纪律管不住手工 `rm -r`、也管不住未来的 `--clean`。**helpers-dev 的实测**（不是推断）给出机制：`CreateFileW(exe, GENERIC_READ, FILE_SHARE_READ|FILE_SHARE_WRITE)`（**不含 `FILE_SHARE_DELETE`**）之后——`os.unlink(exe)` = **winerror 32**、`shutil.rmtree(<release 目录>)` = **winerror 32**、`os.rename(父目录, …)` = **winerror 5**；无句柄的对照组 `unlink` **成功**。<br>**为什么这是「用结构代替纪律」的最好形态**：失败方向是**大声失败**（winerror 32），而不是「静默把目录掏空」；生命周期 = **进程寿命**（句柄随退出释放），**不需要 `finally`**。<br>⚠️ **边界（lead 要求原样写进条款）**：**「在目录里放 in-use 标记」只能当检测、不能当防护**——**标记就在被盲删的那个目录内部，盲删会连它一起删掉**。防护只能来自目录**之外**的东西（本句柄，或一个不看目录内容的删除守卫）。 | **已落**：`modules/paths/paths.py` **1.1.4** 提供 `hold_no_delete(path)`（原语）与 `hold_exe_delete_guard(log=print)`（启动早期调用一次）——**硬要求**：进程启动早期、**托盘/窗口创建之前**；持有到进程结束（故意不 `close`）；**失败必须放行**（D3.2）；**dev 态跳过**（保护 `python.exe` 无意义）。README 加 `<!-- MUST-WIRE: hold_exe_delete_guard -->`（**四家必须接线**，C-27 打红没接的）；新增判据 **C-37**（模板通道，FAIL）= 静态半（原语 + MUST-WIRE）+ **性质半（实测挡得住 + 「释放后成功」这个判别控制）**，自检另有「共享位写错必须被抓住」的样本。**扫描面**：`modules/paths/paths.py` 的真实现（不重写）+ README 的 MUST-WIRE。<br>**C-2 收尾两条（2026-09-19）**：① **命名差异留档**——lead 批准的形态叫 `hold_exe_deny_delete()`，**已落地的实际名字是** `hold_no_delete(path)`（原语）+ `hold_exe_delete_guard(log=)`（启动期调用）；**两者指同一件事**，改名会动派发件、使当前冻结失效 ⇒ **不在本波改名**，下一波可对齐。② **第四条边界（helpers-dev 实测）**：持句柄时 `unlink`=32 / `rmtree`=32 / `rename(父目录)`=5；**`taskkill` 之后文件可删**——但那时进程已死，**不存在"活实例跑在已删镜像上"** ⇒ 这条边界不构成缺口，只是把句柄的语义收窄到"**进程活着的时候**"。 **调用点**：`main()` 里**在运行检测守卫之后立刻**调用（与"早于托盘/窗口"一致）。<br>**📌 C2 落地说明（2026-09-19，helpers-dev 补的两条由 lead 原样采纳；判为 C2 的一部分）**：<br>**要同步改的是 `build.bat` 的**两个守卫**，先把它们的关系写清：**<br>① if exist "%RELEASE_DIR%" → 报错 "already exists. Delete it or bump VERSION"   （G1：一版一目录 / 可复现）<br>② D1-02 运行实例闸（仅当该实例正从**目标目录**运行才拒绝）<br>**① 的实际效果**：**重建同一个版本永远不可能，只能人工删目录**——而「人工 `rm -rf` 一个活实例正在运行的 release 目录」**正是掏空 1.2.2 / 1.4.1 的那个动作**。⇒ **也就是说，这条守卫本身在把用户往那个动作上推**（helpers-dev 原话，lead 原样采纳）。**它把 C2 的动机从「防手滑」升级成「拆掉一个自我矛盾的设计」。**<br>**C2 生效后**（活实例自启动起持有目标 exe 的读句柄、持到进程退出、出错放行；实测 `unlink`→winerror 32 / `rmtree`→32 / 父目录 `rename`→5）⇒ **① 可以安全降级为 ②**：把「目录已存在」从 **ERROR 降为 INFO/WARN**，并入 ② 同一判据（有实例从它运行 → 拒绝；没有 → 由脚本自己清掉重建）。<br>**⚠️ 必须写明的保留语义（helpers-dev 补，lead 原样采纳——这是本次放宽唯一有风险的地方）**：**放宽的是「拒绝条件」，不是「洁净性」。** G1 的「一版一目录、可复现」必须落在「**每次从零重建、不复用旧目录里的任何文件**」，**而不是**落在「存在就拒绝」。<br>**前提（缺一不可）**：C2 的句柄必须由**运行中的实例**持有（早启动、持到进程退出、出错放行）；否则这次放宽会把「安全失败」重新变回「**静默掏空**」。<br>**宣告口径（每次提到这次放宽都要带）**：**放宽了拒绝条件，未放宽洁净性。**<br>**【落点改判】（2026-09-19 lead 收回先前的 `paths`，改为 `modules/tray_kit/tray_kit.py`）**：理由（helpers-dev 给的证据比“语义归属”硬）——① `tray_kit.py` **已有** `import ctypes` + `wintypes` + `CreateMutexW`×12（本文档实测），`paths.py` 则要新增导入；② **C-2 与 `acquire_single_instance` 是同族**：都是**进程寿命的内核对象守卫、都失败放行**；放一起，读者一眼看出“这一族是什么”。⇒ **待落**：现体实现仍在 `paths.py` 1.1.4（`hold_no_delete` / `hold_exe_delete_guard`，C-37 已实测），搬迁至 `tray_kit` 属派发事件（§4.1.39）。<br>**【同族第三例】证据被更早的 `return` 吞掉**（lead 转述 helpers-dev 的自曝）：他的第一版 `delete_protection_selftest` 把 happy path 放在 `try` 里 `return` ⇒ **`finally` 执行完直接返回、跳过后面的清理**⇒ **绿态每跑一次就在 `%TEMP%` 漏一个 `c2-selftest-*`**。修正版：**先算 `result`、清理做完再统一返回**，且**清理失败也进 `problems`**（原版放 `finally` 里，清不掉的证据会被已算好的返回值吞掉）。与 C-32、`marker.unlink` 早于 `log` **同族**。<br>**【重试边界】**：`_rmtree_verified` 的 `delay` 是对付 Defender/索引器的**瞬时锁**（`tests/_cleanup.py` 有先例），**`tries×delay` 耗尽即失败——不是“重试到成功为止”**（否则“重试”会变成“永远等下去”）。<br>✅ **2026-09-19 已落（任务 A3）**：四家 `build.bat` + 模板 `modules/build_release/build.bat` 的 G1 已从 ERROR **降为 INFO**，拒绝条件改由 D1-02 运行实例闸（+ C2 句柄锁）承担；**放宽的是拒绝条件，不是洁净性**——闸后 `rmdir /s /q` 旧目录并**复验**，仍存在即 ERROR 退出（每次从零重建、不复用旧文件）。**判别探针**（守卫段原样抽出，五份各跑两向，GUI 替身 `wscript` 改名）：CellA 无实例→放行且删旧目录；CellB 替身从目标目录内运行→拒绝且不删，`A3 PROBE: ALL PASS`（证据 `H:\Tools\_verify-scratch\A3-g1-probe.txt`）。**同批两条登记（未修，交 lead 裁定）**：① l-s2t `build.bat` 的 D1-02 归一化 `for %%d in ("%RUNNING_DIR%") do set "RUNNING_DIR=%%~fd"` **实测不去尾反斜杠**（与 dsh 注释里"MEASURED 无效"同款）⇒ 其"实例在跑"明确拒绝**不触发**，安全仅由 C2 锁的大声失败兜底（探针 CellB 已实证 rc=1 且不删）；② `build.bat` 里 `if (...)` 块内的 `echo ... (…) …` 会因**裸 `)` 提前闭合块**（§4.1.33 同族，C-22 字节判据看不见）——本批插入文案时被探针当场抓住，已消除。（`modules/build_release/` 属 `sync_check` 的 `TEMPLATE_ONLY_MODULES`，故模板 build.bat 改动**不产生副本漂移**。） |
| 4.1.30 | **「不存在某个机制」不能用一次运行时观察来证明：R1（Job Object）的论证被更正**（2026-09-19，lead 自我更正 + 复核员给事实证据） | 先前的论证是：「父进程退出而子进程存活 ⇒ 子进程没被放进会随父关闭的 job」。**这个推理有洞**：`KILL_ON_JOB_CLOSE` 在**最后一个句柄关闭**时触发，不是创建者退出时——只要还有别人持着那个 job 句柄，创建者死了 job 也不关。所以**单次观察严格只能得出**「那个 job（如果有）没有关闭」，**推不出**「不存在 job」。<br>**真正有效的证据是事实，不是推理**：五个仓全量 grep `CreateJobObject | AssignProcessToJobObject | JOB_OBJECT | CREATE_BREAKAWAY` → **0 命中**（唯一命中在无关 venv 的第三方 `win32\lib\winnt.py` 常量里）⇒ **这套工具根本没有创建 Job Object 的代码，R1 从来不是一个机制**——这个结论**不依赖任何运行时推理**。<br>**附加条款**：将来若有人引入 job，**必须重新论证**（届时「服务被带走」比「隧道被带走」严重得多）。<br>**同源孤儿实际有两处，不止 ocx**（复核员补报，lead 漏了）：`ssh 15044 (-R 10100)` 父 24664 opencodex-helper、**`reme.exe 18512` 父 19084 reme-helper**、**`ssh 2312 (-R 22333)` 父 19084 reme-helper**——三种都是「子活父死」。**reme 那两条更该进结论：服务本身 + 它自己的隧道**。 | **结论（R2 的准确表述，lead 指定统一口径）**：`退出不杀` + `启动先探测、探测失败才杀` 是一套**自洽设计**（健康就认领，坏了才替换）——**所以这不是缺陷，是设计内的一个前提**：它假定 `probe_target()` 在隧道健康时**不会返回假阴性**。而 `probe_target` 是**远端 `curl -sf -m 4 …/healthz` 经 SSH 往返**、还要求响应含 `"service":"opencodex"` ⇒ **它的假阴性可以与「本地这条隧道是否可用」完全无关**（网络抖动 / 远端服务没起 / 远端没 curl / 需要交互式口令）。**这个前提没人验证过**；一旦不成立，**用户正在用的隧道会被工具自己杀掉**。归属 **#45**（helpers-dev 按复核员的源码链做反向复核，重点验「探测的假阳性/假阴性」，别只验「会不会杀」）。**与 C-2 的关系**：C-2 的论证依据是 helpers-dev 实测的 `winerror=32`（内核事实），**不依赖 R1**，因此不受本条更正影响。 |
| 4.1.31 | **判断性探测的失败方向必须与后果的危险性匹配**（2026-09-19，复核员读 ocx `probe_target` 后由 lead 立；判据形态待落地） | **现场三条事实**：① `probe_target()` **吞掉一切异常并无条件 `return False`**；② 它的 `False` 被用来决定 **`kill_target_procs`**（杀掉用户正在使用的隧道）；③ 而它是**远端 `curl -sf -m 4 …/healthz` 经 SSH 往返**、还要求响应含 `"service":"opencodex"` ⇒ **假阴性可与"本地这条隧道是否可用"完全无关**（网络抖动 / 远端服务没起 / 远端没 curl / 需交互式口令）。<br>**与 §D3.2 的关系**：D3.2 说 **守卫自身出错时要放行**（失败方向 = 打开）；这条**更严**——它管的是 **当"动作"那一侧的后果不可逆且伤用户时，失败必须落到"不动"那一侧**。换句话说：**失败方向不能只看"保守/激进"，要看两侧后果谁的不可逆性更大**。这里是"失败即拆用户的东西"，与"失败即少一层保护"不是一个量级。 | **现状**：归 **#45**（helpers-dev 按复核员的源码链做反向复核，重点验探测的**假阴性/假阳性**，别只验"会不会杀"）。**判据形态（我出，待实现）——设计草案 C-38（工具通道，FAIL）**：① 找"**吞异常 + 无条件返回常量**"的函数 P（`except` 兜底分支里 `return False`）；② 找**数据流**：某调用点把 P 的返回值**直接**用作一行动作的守卫（`if not P(...)` / `if P(...) is False`），而该动作属于**破坏性集合**（`kill` / `terminate` / `stop` / `rmtree` / `unlink` / `remove`）；③ 三条同时满足即报，并在诊断里写明**失败方向的后果**。**判别样本**：把 P 的失败返回值改成 `True`（失败即放行）⇒ 必须**不报**；把"破坏性动作"换成"只记一条日志" ⇒ 必须**不报**（避免把"失败只影响提示"的良性形态误报）。**先验扫描面**：四工具 `src/**/*.py` 里"吞异常返回常量"的函数数、其中被用作破坏性守卫的处数——**实跑过再定级**（不许拿想象出来的形状上线）。 |

| 4.1.32 | **"暂时独立形态"的登记：#44-A 弹窗链路不可用时退出被锁死（过渡版）**（2026-09-19，lead 定） | 四工具的 `on_quit` 将各自加**同一个本地小函数**："**弹窗不可用 → 记一行日志 → 按 `quit_stop_tunnels=False` 照常退出**"，并且必须能区分两种情形：**用户明确取消**（照旧**不退出**）与**链路不可用**（**退出**）。<br>**为什么先落过渡版**：用户给的两条前提（业务冲突 / 可验证的更优方案）在本例中是对"暂时独立"的许可，但**附随后续吸收义务**——所以这次**不是把差异留在模板外**，而是**登记 + 限期吸收**。 | **登记口径（四家一致，便于将来一次性 grep 替换）**：① 四家**同一形状**实现（各仓属主做）；② 各仓 `CHANGELOG` + `README` 各写一行**吸收义务**：**"待 `tray_kit` 提供统一形态后改为调用共享件"**；③ **`tray_kit` 侧的统一形态（让调用方能区分"不可用"与"用户取消"）归 tpl-keeper 排期**——**但不在本次波次内**（本轮波次已满，不加行为变更）。**与 §B4 的关系**：这是"允许不一致"两条前提的**带义务留痕**，不是豁免；`sync_check` 不因此放行任何派发件差异（本形态在工具代码里，不在模板件里）。 |

| 4.1.33 | **bat 的"语义"层：三项字节纪律管不到它**（2026-09-19，helpers-dev 实测） | helpers-dev 在新加的交付物断言里写了 `echo [ERROR] Tk runtime missing: _internal\_tkinter.pyd (the extension module itself).` —— **`if (...)` 块内的裸 `)` 会提前闭合块**，整个 bat 在"此时不应有 ."上报语法错。**C-22 三项（CRLF/无 TAB/纯 ASCII）全绿**，因为它是**格式判据**，而这是**语义/解析**问题。他那句总结照抄入库：**"bat 三项字节纪律管不到 bat 的语义"**。 | **已落三件**：① **C-22 docstring 加范围声明**（只管行尾/TAB/ASCII，**不保证 bat 可解析**）——"判据必须自己说清它不覆盖什么"；② **"块内裸 `)`"的启发式——量过之后否掉**：对五仓 8 个 bat 朴素扫描（`^\s*\)` 或行尾 `)`）**命中的全是合法块闭合行**（`build.bat` 单文件十几处 `  )` / `) else (`）⇒ **行级规则没有区分力**，真判它要跟踪块嵌套+引号+`^` 转义；**别用一条会命中正常代码的规则冒充守卫**；③ **真正的守卫写进 C-22 docstring**：新增 bat 块要**从文件原样抽出拼成探针、两个方向各跑一次**（真值 → 通过；不存在路径/缺件注入 → **报错且 `exit /b 1`**）——**只加断言不验"能红"，等于没加**（同 §D3"注入失败前先证明只挡住目标那条路径"）。<br>④ **判据/验证脚本必须带"对照格"**（lead 要求并入本条与 C-22 的说明，2026-09-19）：复核员**只跑「VAR 为空 → 中止」这一格**时，结论是"这个惯用法必炸"；补上**「VAR 有值 → 不该炸」这一格**，才发现**第一次的失败是他自己搬运上下文造成的失真**（整段守卫区段依赖前后行，抽走上下文就换了语义）。⇒ **操作形式：替身/抽取必须是最小对照，且必须有反向格证明它"不该炸（或不该红）"**——**唯一变量法 + 对照格，两者缺一，验证脚本自己就会骗人**（与"负样本要双向：恒红也是没区分力"是同一条）。 |

| 4.1.34 | **"临时升号构建 → 按 G3.7 回滚 → 留下源码里已不存在的版本目录，而自启/部署仍指着它"**（2026-09-19，ls2t-dev 交叉发现两例、复核员补齐第三例） | **本轮已出现三次**：① ocx `1.2.2`（目录被删 ⇒ **死链** + 活实例跑在已删镜像上）；② l-s2t `1.4.1`/`1.4.0`（同上）；③ **dsh `1.8.2`**（目录仍在、**Run 键正指着它**，而源码 `main.py:33 VERSION = "1.8.1"` ⇒ **部署版本 ≠ 源码 VERSION**，暂时无害但状态是错的）。<br>**根因**：升号与发版在 G3.7 里被绑定（"升号 + tag + push 三件事同时发生"），但**构建产物目录**是另一条线——临时升号构建出来的目录不会因为回滚版本号而消失。 | **判定口径（建议，待 lead 定稿）**：① **构建产物目录名必须等于当时的 `VERSION`**（现有 build.bat 已如此）；② 回滚后，**凡不等于当前 `VERSION` 的 `release/<工具>-<版本>/` 一律标记为「孤儿版本」**；③ 对每个孤儿版本**显式判定"是否仍被自启/部署引用"**（`reg query HKCU\...\Run` 对照 + 进程实际路径）：**被引用的孤儿 = 必须处理**（要么把它扶正为当前版本重新构建，要么改引用并删目录），**未被引用的孤儿 = 可留可删，但要在台账里可见**——**"无害残留"不是判定，是漏判**。<br>**为什么值得单列**：这与 §4.1.12（发版节奏）同族，但错在**另一条线**：那条管"版本号不能乱升"，这条管**"升号留下的产物目录会被谁引用"**。<br>**旁证（2026-09-19，lead 从 reme 日志里看到的化石）**：reme 的 `config seeded:` 行指向 **`…\release\reme-helper-1.0.7\config.json`** ⇒ **reme 曾从一个很旧的 release 目录播种过配置**。这不只是一条历史记录，它正是本条第③款存在的理由：**被引用的孤儿版本是"必须处理"的状态**——(a) 它证明"孤儿目录被引用"**不是假想**，而是**已经发生过**（只是当时无害）；(b) 它同时是**归属证据**（那行日志自带路径，正是 C-38 想推广的性质）；(c) 若当时那台机器上 `release\reme-helper-1.0.7\` 被删，下一次启动的配置读取就会指向一个不存在的目录——**"暂时无害"不等于"不会有害"，只等于"还没到那一天"**。 |

| 4.1.35 | **"扫源码"够不着不落盘的生成者 ⇒ 归属只能靠产物自证**（2026-09-19，复核员定死 3 个生产者） | 复核员把 3 个无点 `tmp` 目录的生产者定死了（两例 `python -c`、一例 heredoc），**元凶共性：从不落盘**。这意味着 C-30 的三条腿里，**前两条（生成器腿 = 枚举落盘的生成者 / 形态腿 = 看落盘的残留）对"不以文件形式存在的生成者"原理上无覆盖**；本次能定死归属，靠的是**残留自带的那行日志**（`config seeded: <仓库出厂> → …\<残留>\…`——源是仓库而非用户 AppData，一眼分辨"导入式探针"与"托盘实例"）。<br>**⇒ 立为可判要求（C-38，WARN）**：每个工具启动时必须把**解析出的数据根与配置文件路径**写进自己的日志。**它把"探针自觉带 prefix="这条查不了的纪律，换成了"产物自带归属依据"这条查得了的性质。** | **已落**：C-38（工具通道，WARN；实测 2/4 家已有、dsh/l-s2t 为 0 ⇒ 2 WARN）。**同批记两条边界**：① **"探针必须用带 `prefix=` 的 `mkdtemp`"仍要写，但必须标注它不可机械检查**（探针不落盘，判据无从下手）——**正因为查不了，才有 C-38 兜底**，否则下一个人会以为它已被覆盖；② **会话转录是审计渠道里的最后一条**（lead 裁定）：**只读、只用于归属我们自己的产物、事先声明**；正常路径仍是"仓库/产物自证"。本次是它第一次被动用，也正是它该被动用的场景（生产者不在任何仓里）。<br>**⚠️ 判据形态更正（2026-09-19 晚，复核员实测拦下 lead 的初稿）**：初稿写成"**日志开头若干行必须含数据根路径**"——**按字面会假绿**。实测四家真实日志：reme 6757 行只有 2 行含数据根（**首现在 #770**，09-13）、dsh 92 行 1 行（**#0**，09-18）、ocx 145 行 1 行（**#0**）、**l-s2t 284 行 0 行**；而 **dsh/ocx 的"绿"来自一次性的 `config migrated:` 行**（那 1 行出现在文件第 0 行即最老处）⇒ **绿得不是地方，比红更坏**。<br>**根因**：`config seeded:` / `config migrated:` **只在数据根首次播种/迁移时出现**，也就是说——**能解决归属的那条日志，按构造永远不会在第二次启动时出现**（`tmp0whlwvmi` 能自证，正因它是**全新数据根**）。<br>**⇒ 定形两条**：① 锚在 `startup` 行（该行之后 N 行内必须出现数据根路径），**不看文件前 N 行**——追加/轮转日志的**前 N 行是最老的**；② **一次性行不得计入自证**，并作**反例样本**（"只有一次性 migration 行 ⇒ 判红"）。等级仍 **WARN**（今天四家都红，是**新增缺口**，不是谁写错）。**已实现并实测四家全 WARN**（见 §5.1 的 C-38 行）。 |

| 4.1.36 | **修复会移动落点，从而让旧的扫描面静默失效**（2026-09-19，lead 裁定立档；另附一条"两版工具两套口径"的读法） | 实证：R2 把测试 scratch 从 `%TEMP%` 挪到 `H:\Tools\_verify-scratch`（`tests/_cleanup.py` 的 `_DEFAULT_SCRATCH`）⇒ 那批残留**既不在 `%TEMP%`、也不在任何被枚举的前缀里**，**腿 A（生成器派生）与腿 B（形态派生）同时看不见**——**盲区是被"修复"自己挪出来的**，而不是原来就有的。**根因**：扫描面是从"我们以为的落点"派生的（%TEMP% + 源码里的 prefix 字面量），而 `mkdtemp(..., dir=…)` 的 `dir` 从来没进过枚举。<br>**口径**：① 扫描面必须由**实际有效落点**派生（`mkdtemp(..., dir=…)` 的字面量 / 模块级常量，**含 `_DEFAULT_SCRATCH` 这类默认值**）；② **每个根都要打印扫描目录数**（否则"扫了但没覆盖"与"没扫"同形）；③ **任何"挪动落点"的修复，必须同时检查扫描面是否仍覆盖它**——**"我把它挪走了"不等于"它不在泄漏清单里了"**。<br>**同条目附一条读法（lead 采信后加）**：**同一件事可能有两版工具、两套口径**——本仓 `conformance_check.py` 的 C-30 上半**会解包装函数的调用点**（`scratch_dir("dsh-…-")` 全是字面量 ⇒ 可静态归属 ⇒ `[ok]`），而复核员那版工具不看调用点、会判红。**⇒ 宣告/比对时必须写明工具版本**（本仓现行 `conformance_check.py` TEMPLATE-VER 与身份行 `norm`），否则同一个仓库会给出两个"都对"的结论，下一个人会以为自己漏了什么。这与「证据必须带时点」同族：**读数还必须带"用哪把尺子量的"。** | **归属**：#37 里 reme 的 `src/main.py:7423 rmtree(work, ignore_errors=True)` 属本族（lead 已更正他板上"已完成"的标记并向 reme-dev 重派）；**扫描面按"有效落点"派生**的改动 = 模板专属件（`conformance_check.py`），**不派发到工具 ⇒ 不挡冻结、随时可单独提**，待复核员口径文本到位后落。 |

| 4.1.37 | **"在源码文本上找形态"的判据会读到散文 ⇒ 判据自己判自己红**（2026-09-19，lead 批准 C-33 修法并定为冻结硬前置；tpl-keeper 随后在 C-30 上量到**第二例**） | **C-33 实例**：`check_ping_tick` 把自己的 **docstring 判红**——那段散文正在解释"为什么要禁 `ping -n 2`"，于是**越把原因说清楚越违规**。**复核员最小复现**：`#` 注释绿、`rem` 行绿、**docstring 红**。<br>**C-30 第二例（我按同一条边界自查时量到）**：C-30 下半在**原始文本**上找 `rmtree(..., ignore_errors=True)`，而 `conformance_check.py` 的 `_rmtree_strict` 与 `sync_check.py` 的 `finally` **都在 docstring/注释里引用**了那句被禁的旧写法（"本工具自己先得守 C-30"）⇒ **仪器在自己的合规说明上自证违规**，`--roots my-diy-tool-template` 下 2 处假红。两例**同族同因**：判据按"**token 类型/文本**"划豁免，而它要分的是**语义**——"会被执行的代码文本" vs "关于代码的文本"。<br>**机制边界（lead 裁定，写进条款）**：**"不碰字符串"这条豁免的适用对象是"会被执行的代码文本"**；docstring/注释与 bat 模板**同为 STRING token，语义不同**。**这是豁免边界画错，不是实现 bug**。 | **已落四件（全在模板专属件，零派发件改动）**：① `_strip_docstrings()`——挖 **AST 的裸字符串表达式语句**（含 docstring，含不在首位的说明串；**只挖"裸"的那层**，赋值/传参/拼接的字符串一律保留）；② `_masked_code_text()`——**就地掩成空格、长度与换行不变** ⇒ 给**要报行号**的判据（C-30 的登记键是 `相对路径:行号`）用；③ **C-30 下半改用掩码文本**（C-33 用 ①）；④ **扫描面按绝对路径排除仪器自身**并把**排除项打印进 detail**（否则"排除了"与"没扫"同形，同 C-30 的扫描面纪律）。<br>**自证腿（缺一条腿就是这次假红一路绿灯的原因）**：C-33 加 `ping_in_py_docstring_ok`（**此前 5 条腿恰好缺它**）＋**反向格** `ping_in_py_string_still_flagged`（同样一句话作为真字符串常量**必须照样红**——证明绿来自"豁免了 docstring"而非"豁免了这句话"）＋`own_instrument_excluded_and_announced`；C-30 加 `prose_mention_in_docstring_ok` ＋**反向格** `prose_mention_reverse_cell_flagged`。<br>**⇒ 立为纪律 ⑨：豁免的每一条边界都必须有一条自证腿，且必须带反向格。**<br>**实测（修后）**：C-33 模板侧 21 件 + 工具侧 22 件全绿（排除项已点名）；C-30 模板侧全绿；四工具 C-33 全绿（**l-s2t `src/updater.py` 的真违规已由 ls2t-dev 修掉**：:233 渲染 `powershell Start-Sleep`，:48/:225 是被正确豁免的注释/`rem`）。| 设计纪律 ⑨/§4.1.33/§4.1.24 |

| 4.1.38 | **下一波（#40 之后）：每次启动一行自证——格式先定死，再让四家落地**（2026-09-19，lead 裁定"排期"并要一条可粘贴样例） | **为什么不并进本轮**（lead 三条理由，照实记）：① 它碰**四个 `main.py` 的启动段**，需要四家**同一种行格式**——**格式不先定死，就会像 cmd 守卫那样长出五份变体**（§J 抬头说明那一族）；② 今天四家都红，属**新增缺口**，在正在收敛的重建链上插一条**跨仓格式要求**，会把重建与 #24 继续往后推；③ 它的价值是**回溯性**的（不影响重建、不影响 #24），而它要替代的那条渠道（**会话转录**）**已可用且已裁定**，不是无处兜底。⇒ **本轮只改判据形态与文档**（防假绿），**日志下一波一次同格式落地**。 | **可粘贴样例（各仓 `main.py` 启动段，紧跟自家 `startup` 行之后；这是唯一正本，四家照抄，不自创变体）**：<br>`log("data root: %s" % USER_DATA_DIR)`<br>`log("config   : %s" % CONFIG_PATH)`<br>**形状要求（判据实际会验的就是这三条）**：① **在 `startup` 行之后 20 行内**（不是文件开头）；② 用**解析后的值**（`USER_DATA_DIR` / `CONFIG_PATH` 本身，不是它们的默认字面量、不是局部变量别名——reme `:2897` 的 `config={config}` 就属于读不出的那种）；③ **不是** `config seeded:` / `config migrated:` 这类**一次性**行（那些只在首次播种/迁移出现）。<br>**落点（模板一处，四家重拷即同时具备）**：`modules/paths/paths.py` 的 `seed_config()` **或** `main()` 启动早期；**实现归 tpl-keeper，接线归四家**（与 C-2 同一种分工）。<br>**验收**：C-38 由 4 WARN → 4 ok（detail 里能看到锚与命中行），且**自证腿不变**（6 条全绿）。 | §4.1.35/§5.1 C-38 |

| 4.1.39 | **修判据前必须先回答：这次修复会不会碰到 `modules/**`？**（lead 2026-09-19 定，来自一次之后发现的**他没预见到**） | **发现过程**：lead 被告知“C-33 的 5 处是假红”时，只想到“**判据要改**”，**没想到“改它的过程中可能碰到派发件”**。而 `modules/**` 一旦被改，就是**可重拷事件**：四家副本瞬间漂移、**已宣告的派发件哈希作废**、接收方白拷一遍。<br>**机械形式（两条，都是现成能力）**：① **增量宣告必须列出 `git diff --name-only` 的路径清单，并明写“本批零派发件改动””**（这正是拦住这类事故的那一格；只报 commit 号是不够的）；② **若修判据真的必须改到 `modules/**`，默认处置是重新设计判据**（C-33 就是这个答案：**一行 `modules/` 都不需要改**）；若真无法避免，**必须走派发流程**（改完 → 冻结 → 声告 → 重拷），**不得搭一个已声告的批次**。 | **为什么单列**：它与§4.1.36（修复会移动落点）同族——**一个看似局部的修复，会把影响扩到它看不见的地方**：前者把漏洞挪出扫描面，这条把漂移挪进四家副本。 |

| 4.1.40 | **判据的痕迹留在了产品文案里：为了让 C-33 闭嘴而把散文改写成了“不能被匹配”的形状**（2026-09-19，lead 定性；tpl-keeper 定位到具体提交） | **实例**：`modules/update_helper/update_helper.py` 的模块 docstring 里原本写着自然的一句——`` * **等待节拍不再用 `ping`**：`ping -n 2 127.0.0.1` 看着像“睡 1 秒” ``——它在 **docstring（字符串）** 里，而当时 `_code_only_text` 只过滤 `#` 与 `rem` ⇒ **C-33 把解释自己的散文当成了可执行节拍**。随后的修法不是改判据，而是**把那句话改写成了**“等待节拍不再用 `ping`（那是‘发 ICMP 等回包’，不是睡眠）：`-n 2` + loopback 地址”——**`ping` 与 `-n` 被人为分开**（前面插入一个括号、`-n 2` 单独加反引号）。**定位**：该改写在 commit **`2afebbc`**（#40a 派发件批次，提拉 diff 第 72/77 行），**不是 C-33 修复那一批**（那批只动了 `conformance_check.py` 与三份文档）。<br>**为什么比缺陷本身更重**（lead）：① **判据的痕迹留在了产品文案里**——下一个读者看不出为什么要写成那样；② 改文档的代价每次都要**四家重拷**，而改判据是**一次改动四家同时转绿**。 | **已验证：恢复自然散句现在是安全的**（探针实测：把句子改回原样→ `check_ping_tick` 仍 **GREEN**），因为判据已改为挖 **AST 裸字符串表达式**（§4.1.37）。<br>**处置（不擅自动手）**：该恢复碰 `modules/**` ⇒ **可重拷事件**，按 **§4.1.39** 走派发流程（改完 → 冻结 → 声告 → 重拷），**建议并入下一波的一次重拷**（TEMPLATE-VER 1.4.4 → 1.4.5），不单独发一次通知。 |

| 4.1.41 | **派生值必须取自“本次调用的实参”，不能取自“模块级当前值 / 定义时的快照”**（lead 2026-09-19 立，当天第二次出现） | **一族两例，共同点：用了“另一个时刻 / 另一个来源”的值去代替**本次输入**：<br>① `AsrEngine.__init__(self, model_dir=MODEL_DIR)`——默认参数在**定义时**求值，运行期 `load_config()` 重绑也传不进去（l-s2t #46：**用户改了配置却不生效**）；<br>② `_APPLY_BAT` 的 `budget_s` 曾取模块常量 `UPDATE_WAIT_BUDGET_S`（按 `UPDATE_WAIT_LIMIT=120` 算），调用方 `limit=2` 时渲染出 `2 polls x 1000ms (nominal budget 120s)`——**拼出了一个不可能的组合**（已于 1.4.4 修）。<br>**与“日志里的数必须是被测过的数”同族**：那条管“数没量过”，这条管“数用的是别的输入”——**日志说谎的两种形态都要治**。 | **已立判据 C-39（工具通道 + 模板通道，FAIL）**，只判**可判的那一半**（默认参数），且**三档判别**：① 默认值是**会被重绑的模块级名字**（模块级多次赋值 / 任何 `global` 重绑）⇒ 红；② 默认值是**可变字面量**（`[]`/`{}`/`set()`）⇒ 红；③ **只赋值一次、不可变、无 `global` 重绑**⇒ **放行**（全家族当前 13 处全属此类，已数进 detail 的分母）。**第三档必须放行**，否则就是“看到默认参数就报”的噪音判据——那正是 C-33 那族错误的翻版。<br>**自证腿 4 条（两红两绿）**：`rebound_module_name_flagged` / `mutable_default_flagged` / `immutable_constant_benign_ok`（反向格）/ `none_sentinel_ok`。<br>**残余（未判的那半）**：“模块常量被写进输出文案而函数另有实参”（`budget_s` 那种）**不是**默认参数形态，静态判定需要数据流分析，**本条不担保**；它靠的是 `sync_check --selftest` 的 **E 组行为断言**（已补三条腿，含真变异的反向格）。 |

| 4.1.42 | **版本目录 ↔ 自启目标 必须一致**（ls2t-dev 提议，lead 补两处修正后定；已落为 **C-40**） | **提议原文**：“`release/` 下的版本目录集合 == {`源码 VERSION`}，且自启目标路径 == 该目录下的 exe”。**价值**：把 lead 要的那条**人工前置**（“每个 owner 写明启动哪个 exe、与源码 VERSION 是否一致”）变成**可判的性质**——**与 C-38 同一手法**：纪律 → 可判性质。三条都能从**磁盘 + 注册表**直接读。<br>**⚠️ lead 的修正（按原文字面会产生两处假红，实测）**：`reme-helper/release/` = 1.2.4 + 1.2.5、`dsh-helper/release/` = 1.8.1 + 1.8.2 ⇒“集合相等”会把**正常的历次构建产物**全判红。⇒ **正确形态分两段、两个等级**：<br>**① 强断言（FAIL）**：**自启目标必须存在**，且其所在目录必须是 `release/<源码 VERSION>/` **或稳定安装位**（`%LOCALAPPDATA%\<APP_ID>\app`，若该工具已用稳定位）；<br>**② 登记断言（WARN）**：**不属于当前 VERSION 的版本目录 = 孤儿版本**，必须在 `ORPHAN_VERSIONS` **声明“是否仍被引用”**（条目按**纪律 ⑩ 两栏必填**：`why` + `reverify`）。**被引用的孤儿 = 必须处理；未被引用的 = 可清理**（§4.1.34 第③款）。<br>**内测结果（2026-09-19，实测本机）**：**dsh = FAIL**（现成真反例：源码 `main.py:33 VERSION="1.8.1"`，而 Run 键指着 `release\dsh-helper-1.8.2\dsh-helper.exe`）；ocx（1.2.1⇒`release/opencodex-helper-1.2.1/`）、reme（1.2.5⇒`release/reme-helper-1.2.5/`）**ok**；**l-s2t** 当时被记成「无 Run 项 ⇒ 强断言不适用」——**该结论已证伪（§4.1.53）**：它的 Run 键用的是 `APP_NAME=LocalSpeak2Text`，而判据当时按 `APP_ID` 单查 ⇒ **强断言从未执行**；修后实测其目标 == `release/local-speak2text-1.4.0/`（与源码 VERSION 一致）。<br>**自证腿 6 条**（含**把 dsh 的真实状态逐字搬入**当正例，以及三条反向格：目标==release/<VERSION> ⇒ 绿、稳定安装位 ⇒ 绿、同一孤儿**已登记** ⇒ 绿）；**2026-09-19 增补 4 条键名腿（§4.1.53）⇒ 10 条**。**纯函数 + 可注入 `path_exists`**：否则样本得先在磁盘上造出那些目录，**样本就被活状态污染了**。<br>**措辞纪律（ls2t-dev 主动补的，lead 认为比“答对”更有价值）**：他答完“l-s2t 三者一致、无孤儿版本目录”后**主动补了一句**：“本仓**确实发生过**那个模式（1.4.1 是临时升号构建的产物、最后成了空壳），只是**已被清干净**⇒ 准确表述是‘**出现过该模式，本仓已收敛**’，不是‘从未发生’。” ⇒ **判据/登记的陈述必须区分这两种句式**：**“从未发生”不可验证；“发生过且已收敛”可验证且更诚实**。⇒ 条目一律写成 **“当前态 + 是否曾经出现过 + 如何收敛”**。 |

| 4.1.43 | **退出确认的「链路不可用」分支必须固定为"不停服务"**（lead 2026-09-19 定，源头是他批错过一处；已落为 **C-41**） | **口径**：**那个勾选是用户在"有确认框"的语境下保存的；链路坏掉时用户根本没被问过。** 若沿用，就变成 **"辅助机制坏掉 ⇒ 在无人确认的情况下停掉用户正在用的服务"**——正是本轮的母题。<br>**标准形态 = dsh/ocx 的硬编码 `False`**（`return True, False`，两个分支各一处）；**reme 与 l-s2t 原本按已存配置走**，已被更正，且**在原处留下"曾偏离"的历史**（reme `main.py` 的注释："旧行为沿用已存配置…lead 2026-09-19 撤回旧批准"；l-s2t 的 `_confirm_quit` docstring 记了同一条）。<br>**为什么现在就要写成判据**：将来 `tray_kit` 要做**统一形态**，而**统一之后极容易长回去**——判据立在这里，统一件落地那天它自己就会被验。 | **已落 C-41（工具通道 + 模板通道，FAIL）**：只判**降级分支**（`except` 处理器 + `if <x> is None:` 分支）里喂给退出决策的语句；若它读持久化配置且涉及破坏性开关键 ⇒ 红。<br>**"原生框那一支"不算违规**：那时用户**确实被问到了**（只是没有勾选框）⇒ 按已存配置走合法——**两条分支因此保持可分**（这也是判据必须按分支判、不能按文件判的原因）。<br>**实测（2026-09-19）**：模板 `modules/**`（3 个退出相关函数 / 6 处降级分支）+ 四工具（6/7/6/8 个函数、21/16/21/19 处分支）**全部 `[ok]`**——今天没有违规，判据是**防统一之后长回去**的。<br>**自证 5 条腿**：字面 `False` ⇒ 绿 / `except` 里读 `CFG` ⇒ 红 / `None` 分支字面 `False` ⇒ 绿 / `None` 分支读 `load_config_dict()` ⇒ 红 / **原生框那一支（在 `try` 体内）读配置 ⇒ 绿**（反向格）。 |

| 4.1.44 | **重定向位置上的 `dev/null`：三层判据都看不见的"命令根本没执行"**（lead 2026-09-19 定·**收窄版**；事故由 ls2t-dev 挖到） | **事故链**：他用 **bash heredoc** 打补丁，`nul` 在**到达 Python 之前**被改写成 `/dev/null`、同时 LF→CRLF：<br>`powershell -NoProfile -Command "Start-Sleep -Milliseconds {tick_ms}" >/dev/null 2>nul`<br>**实测影响**：`rc=0` 但 **0.03s**、stderr 报「系统找不到指定的路径」⇒ **`powershell` 根本没执行、睡眠没发生**（对照：正确写法 **0.68s**、stderr 空）。于是等待循环里 `tries` 以 `tasklist` 的极限速度狂涨、**120 拍几秒烧完**，`:giveup` 在旧进程没退时就放弃，**而日志仍打印 `120 polls x 1000ms (nominal budget 120s)`**。<br>**三层判据都看不见**：C-22（仍是 ASCII+CRLF）、C-33（找 `ping`）、`test_update_safety`（走不到那条重定向）。**而他的自证是假绿**——他比对的是**同一个字面量**，被**同一条规则**一起改写、一起错。 | **已落 C-42（工具通道 + 模板通道，FAIL）**：匹配 **`>`（含 `2>`/`>>`）+ 可选空白 + `dev/null`**——**收窄到"重定向位置"**，**不写成"全文不得出现 `dev/`"**（注释里的 `H:/Tools/dev/…` 与 URL 会误报；收窄后零误报，Windows 上没有合法理由在该位置出现它）。<br>**文本口径与 C-33 同一条边界（§4.1.37）**：`.py` 掩掉注释/docstring（**保留其余字符串**——渲染 bat 的模板正是字符串，那才是要查的）；`.bat`/`.cmd` 丢 `rem`/`::` 行。**否则本条判据自己的说明文字会把自己判红。**<br>**实测四家 + 模板 → 全 `[ok]`**（扫描面 24/44/25/33 件 + 模板 23 件）。**自证 5 条腿**：lead 点名的三个样本（重定向命中 → 红 / 注释里 `H:/Tools/dev/x` → 绿 / 模板字符串 `>nul` → 绿）＋ `.bat` 形态 → 红 ＋ **反向格 `devnull_like_name_ok`**（`> dev/nullish` → 绿，证明收窄到了"完整词"）。 |
| 4.1.44-补 | **更一般的规则（lead 判定：这条比判据本身值钱）**：**当"修改路径"与"验证路径"共享同一层转换时，它们会一起错。** | **本例**：改文件用 heredoc、自证用**同一个字面量** ⇒ 同一改写规则作用于两边 ⇒ **比对必然通过**（假绿）。<br>**⇒ 验收要断言"一个改写不可能满足的性质"**（如"重定向位置不得有 `dev/null`"），**而不是断言"等于我以为的那串字符"**；引用具体字面量时，要用**字节/十六进制**（ls2t-dev 的 `nul` 是 `bytes([0x6e,0x75,0x6c])` 拼出来的，尾部 hex `7d2220 3e6e756c 20 323e6e756c`）。<br>**与哪些条目同族**：与「判据的枚举方式决定它的视界」（§4.1.35）、「0 命中必须打印扫描面」（纪律 ⑥）、「读数必须带尺子」（§4.1.36）**同族**——**同源的两层，永远不会互相发现对方的错**。<br>**⇒ 立为纪律 ⑪**（§5 前言）。 |

| 4.1.45 | **`if` **条件**里的 `:~` 子串扩展：会让整个脚本中止（边界由 ls2t-dev 钉准，lead 采纳）** | **危险的只有一种形态**：**同一行条件里**带 `:~` 尾/子串扩展（`:~-1` / `:~0,-1`）——`%` 展开发生在 `if` 求值**之前**，变量未定义时该展开把字面量塞进引号，cmd 报 `The syntax of the command is incorrect.` 并**中止整个脚本**（不是跳过那一行）。<br>**嵌套 `if` 本身无害**：`local-speak2text/build.bat:84` 的 `if defined RUNNING_DIR if /i "%RUNNING_DIR%"=="%TARGET_DIR%" (` **含 `:~` 次数 = 0** ⇒ 普通 `%VAR%` 展开，未定义时得 `""`、语法仍成立 ⇒ **判绿**。**按"打嵌套 `if`"的宽版写，这一行就是现成的假阳性——而它就在我们自己的仓里。**<br>**条件 vs 动作**（我实测补的一条）：`if defined X set "Y=%X:~0,-1%"`（dsh/ocx `build.bat:87`）里 `:~` 落在**动作**一侧且被 `if defined` 守着 ⇒ 未定义时展开为空、无害 ⇒ **判绿**。判据因此以「`:~` 是否出现在**动作关键字之前**」为界。 | **已落 C-43（工具通道 + 模板通道，FAIL）**：`^\s*if\b` 行 + `:~` + 「`:~` 在动作关键字（`set`/`call`/`echo`/`goto`/`exit`/`for`/`rem`）之前」⇒ 红。<br>**实测四家 + 模板 → 全 `[ok]`**（仅 dsh/ocx 的 `:87` 是动作一侧、l-s2t 的 `:84` 是嵌套 `if`，两者都按绿）。<br>**自证 4 条腿**：历史中止形态 ⇒ 红；**逐字搬入本仓真实行 `l-s2t/build.bat:84`** ⇒ 绿；**动作一侧真实形态（dsh/ocx `:87`）** ⇒ 绿；普通 `%A%==%B%` 展开 ⇒ 绿（反向格：不是"见 `%` 就报"）。 |
| 4.1.45-补 | **探针纪律的两条工程边界**（ls2t-dev 的做法，可复用；lead 要求写进条款） | ① **探针只取"守卫段"、以 `cwd=仓库` 运行**——头里"release 目录已存在"那条会先 `exit`，全量 bat 做探针**根本走不到守卫**（他自述第一次就是这么白跑的）。<br>② **判别依据用 `rc` + marker，不要匹配 `Syntax of the command is incorrect.` 那句文案**——cmd 用 **OEM 码页**输出，按 UTF-8 解码匹配不到 ⇒ **两份都会读成 0**（假绿）。<br>⇒ **通则：不要把判据建立在一条可能被错误解码的文本上**（与 §4.1.37「判据读散冒」、纪律 ⑪「同源两层一起错」同族）。 |

| 4.1.46 | **bat 调外部命令必须用绝对路径：PATH 会悄悄换掉程序**（lead 2026-09-19 定；事故由 reme-dev 撞到） | **机制**：本机实测 **`where find` -> `H:\Tools\Git\usr\bin\find.exe`**（排在 System32 前面）。等待循环用 `find /i "{exe}" 文件` 判"旧进程还在不在"，而 **GNU `find` 把 `smss.exe` 当文件名 ⇒ 恒返回非零** ⇒ 循环每次判"旧进程已退出" ⇒ 直接去覆盖**仍在运行的 exe**（文件被锁 ⇒ robocopy 默认百万次重试）。`ping` 同理（GNU 的 `-n` 是 numeric，不是次数）。**与 `dev/null` 同一母题**：**环境悄悄提供一个同名但语义不同的程序，代码走进错分支，而且不报错**。<br>**闭集（8 个）**：`find` / `findstr` / `ping` / `tasklist` / `robocopy` / `where` / `reg` / `timeout`——**只在发现新同名冲突时扩集**，**不写成"所有外部命令"**（会噪声化，且无法判准）。 | **已落 C-44（工具通道 + 模板通道，FAIL）**：**只看命令位置**（行首 / `|`/`&`/`(`/`^` 之后的第一个 token，含 `for /f ('cmd')` 内联形态）；`rem`/`::` 不计；token 内含路径分隔符即算绝对。<br>**实测命中 17 处**：模板 3（`build_release/build.bat:48`、`:171`、`release.bat:10`）、dsh 2、l-s2t 5、ocx 2、reme 5——**全是 `findstr`/`tasklist`/`robocopy` 裸名**。<br>**⚠️ 关键校准（本机实测 `where`）**：**只有 `find` 与 `timeout` 真的被 Git 抢先**（`H:\Tools\Git\usr\bin\`），其余六个当前解析到 System32 ⇒ 今天这 17 处属**潜在**风险而非现役故障；但 **PATH 顺序不是我们能假设的**（正是纪律 ⑫ 的理由），故判据仍按闭集全收。<br>**自证 5 条腿**：裸名 ⇒ 红；绝对路径 ⇒ 绿；`rem` 里提到 ⇒ 绿；`for /f ('findstr …')` ⇒ 红；非闭集命令 ⇒ 绿。 |
| 4.1.46-补 | **\\*\\*与 C-33 的分工（独立，不互相顶替）\\*\\***：**C-33 管"拿 `ping` 当节拍"（语义），C-44 管"裸名 `find`/`ping`"（解析）**——同一行 `ping` 可能同时违反两条，也可能只违反一条。 | **实证**：模板 `update_helper` 的渲染 `apply.bat` **两条都合规**（实测：`%SystemRoot%\System32\tasklist.exe` / `find.exe` / `Robocopy.exe` / `WindowsPowerShell\v1.0\powershell.exe` 全是绝对路径，**裸名命中 0**；`ping` 已无踪）⇒ **不需要为这条改它，也不额外一轮重拷**。<br>**教训**：**两条判据各自独立扫描、各自报红**，不要用一条"认为"覆盖另一条。 |

| 4.1.47 | **假契约比缺契约更危险：`tray_kit` 退出对话框的返回值**（helpers-dev 读实现时发现；lead 定堑） | **现状**：代码永远不返回 `None`（`result` 在函数开头就建成非空 dict、之后只 `.update(...)`），而旧 docstring 写着“**取消返回 None**” ⇒ **那是一份假契约**。**风险不是审美的**：dsh/ocx 刚落的 fail-open 修复**正压在这个值上**（`choice is None` 读作“链路不可用 ⇒ 放行退出”）：**谁哪天照 docstring 去“修好”那个 `or None`，dsh/ocx 就会在用户点“取消”时退出**——**跨文件的静默反转，而现有测试抓不到**。 | **裁定已落在 `tray_kit` 2.2.1**（本文档实测）：① docstring 改成**真契约**（“**取消 = `{"go": False}`；本函数永不返回 `None`**”，并写明“不可用”与“取消”分别由什么返回值表达）；② **删掉不可达的 `or None`**（`return result`，并注明“行为不变，helpers-dev 当场逐路径证过”）——**用结构代替纪律**：去掉“能构造出错误读法”的东西，而不是靠注释提醒。四家副本均已无 `or None`（实测）。<br>**排序说明**：这条**优先于任何“四家同形”的讨论**——**契约不定，同形就没有稳定地基**。 |

| 4.1.48 | **静态检查器的"静默出口"：三处 `continue` 让缺陷输入与合法输入共用一个可观测量**（ls2t-dev 往复产出；判据归模板主。已落 `sync_check` 1.9.0） | **形态**：`scan_tool` 里三处静默出口——① 无任何出处头 ② `TEMPLATE-MODULE` 推导出的目标不存在 ③ 布局兜底不唯一。三者的语义都是"当作这个文件没有出处"，而**"没有出处"正是工具自有文件的正确观测量** ⇒ 头被覆盖 / 模块名写错 / 目标不存在，全部落进"工具自有"这一档，**输出与正常情况逐字相同**。**这不是漏判，是没有判据**：拿一个已知缺陷输入喂进去，**没有任何可观测量会变**。<br>**判准（可执行问法，替换循环问法）**：原问法"这条兜底能不能只在输入正确时生效"**对"兜底自身供给目标"的装置是循环的**（"正确"由兜底自己定义）。改用：**"拿一个已知缺陷输入喂进去，有没有任何一个可观测量会变？"**——不变即盲区，与设计意图无关。补强：`:216` 的"有没有出处"谓词把 `MODULE_RE` 也算合法出处，故裸拷贝在**存在性判据**上也过闸。<br>**已落形态（三档 + 四个出口，各带反向单元 + 控制单元）**：无头（工具自有）／**申报了却解析不出 = `[BAD-HDR]` 红灯**／解析得出。四条腿：`[BAD-HDR]`（红灯，实测四家 0 命中）；`[NO-HDR-COPY]`**（红灯）= 无头但归一化内容等于模板件 ⇒ 拷贝被剥了头**——这条让"缺头⇒报"**可量化且不刷屏**（工具自有件不匹配任何模板件，天然落在判据之外；剥掉任一头立刻变红，实测 0 命中）；`[NO-HDR]`（黄灯）= `src/modules/**` 下无头（该命名空间里"无头"**有歧义**；实测仅 reme `src/modules/__init__.py` 一件，模板无对应件）；**`NOT-WIRED.md` 升格为申报口**——模块目录下有它 = **有意未接入**，该模块缺失项记 `[decl]` 而**不进** missing 计数。**申报件本就存在于野外**（reme `src/modules/service_link/NOT-WIRED.md`）而 sync_check **完全不读它** ⇒ "申报了"与"没人注意"是**同一个可观测量**；今天零行为变化（该模块已完整采纳），它是**出口 + 自证腿**。<br>**退出码口径**：仍只有 `drift`/`missing` 阻断，加两条新红灯；实测默认根与四家各 `exit=0`（dsh/ocx 门禁按路径调用本件、非副本，故即时生效且不破门）。<br>**为什么"缺头⇒报"不能字面执行**：四家共 ~257 个无头 `.py`（main/tests/scripts）**确实**是工具自有件，一律报红等于把判据噪声化。⇒ 把"该不该有头"从**命名空间猜测**改成**可判定的观测**（内容是否等于模板件）。 |

| 4.1.49 | **重建新鲜度判据的分母只有 `src/**`，小于真实打包输入集**（任务 `#62`，2026-09-19，tpl-keeper 落地） | lead 的口径 `exe mtime > max(src/** mtime)` 只覆盖 `src/**`，而四家都有 **out-of-src datas**（l-s2t `*.ico`+`locales/`；dsh `*.ico`+`resources/`+`locales/`；ocx `*.ico`+`bin\plink.exe`+`locales/`；reme `*.ico`+`doc/`+`pairs.json`）⇒ **若只有 datas 变了，判据会说"新鲜"而产物其实是旧的**。与 `#58` 的 R-10 扫描面同族：**判据的分母小于事实的定义域**。本批次实测这些 out-of-src 输入**全部早于** exe ⇒ **缺口真实存在但当时零影响** | **已落 C-46（WARN，工具通道）**：分母 = `src/**`（剔 `__pycache__`/`*.pyc`）∪ `build.bat|scripts/build.bat` 的 `--add-data "SRC;DEST"` 源（展开 `%~dp0` / `%CD%` / `%APPNAME%`，展不开的源跳过）。**必须打印扫描面（输入件数 + `--add-data` 源数）与取到最大值的那条路径**——只给布尔是"无法复核的结论"（`receipt_check.py` 的教训）。**实测（2026-09-19）**：分母 29/28/28/34 件（dsh/ocx/l-s2t/reme）；**dsh 的 max 输入正是 out-of-src 的 `dsh-helper-taskbar.ico`（20:38:02 < exe 20:38:33）⇒ 补上的那一项就是承重项**；l-s2t / reme 因本波并发编辑 `src/**` 而**如实转 WARN（过期）**——⚠ **这是预期读数**：本轮明确**不重建**，如实留着，**不要为消 WARN 去构建**（否则违反用户范围约束）。**自证 4 条腿**（out-of-src 项变新 ⇒ 翻红 / 严格 `>`（等值即过期）/ 全旧 ⇒ 新鲜 / 空分母 ⇒ **不可判**）。  **另见 §4.1.65**（同一判据的**参照系**与**排除项**两个维度）。|
| 4.1.50 | **bat 绝对路径化与判据锚点：模板侧已落地，工具侧归各仓**（任务 `#49/#50`，2026-09-19 tpl-keeper 核验） | `#49` 四项：① 模板 `modules/update_helper/update_helper.py` 渲染的 apply.bat **早已全绝对路径**（`%SystemRoot%\System32\{tasklist,find,Robocopy}.exe` + `…\WindowsPowerShell\v1.0\powershell.exe`，裸名 0；见 §4.1.46-补）；② 判据分类器已改为"首 token → 剥引号 → 取末段路径 → 去 `.exe` → 小写比命令名"（`sync_check._split_cmd`），裸名与绝对路径都识别、顺手消掉 `findstr` 误配；③ `idx()` 未命中**返回 `None` 不返回 `-1`**（`-1` 会流进 `>` 比较成**空真**）；④ 双向自证在 `sync_check --selftest` 的 **E-mut 组**。`#50`：删**真正执行安装的那一行**（`robocopy STAGE→TARGET`）**必须变红**——实测**死 3 条**（`检查 rc` / `替换前先快照` / `start 前有存在性守卫`），且"**空真集合为空**（没有判据停止工作）= 0 处"。**本轮补的模板侧缺口**：模板自己的 `modules/build_release/{build,release}.bat` 仍有 3 处裸名（`findstr`×2 / `robocopy`×1）⇒ **已按字节绝对路径化**，C-44 模板通道由 FAIL → `[ok]`（扫描面 2 个 bat）。**同批一次自伤留档**：用 heredoc→Python 写这批 bat 时，`\f` 落成了真 `0x0c`（正文成了 `System32<FF>indstr.exe`），而 **C-44 仍判绿**（只看 token 是否含分隔符）、**C-22 三项（CRLF/无 TAB/ASCII）也都不覆盖控制字符**——是**字节回读**当场抓住并按字节还原。⇒ 又一条"既有字节判据不看控制字符"的实证（与 §4.1.36 的 0x0c 家族同源）。 |
| 4.1.51 | **自启自愈谓词是"存在性"，不能代理"当前性"**（任务 `#63`，2026-09-19；**登记，不写派发件**） | `modules/autostart/autostart.py` 的 `_cmd_alive(value)`（:86-93）判据 = "命令行里路径 token **全部存在**"。`release/` 保留历史版本目录的布局使该谓词**对废弃版本恒真** ⇒ `migrate_autostart`（:121-122）直接 `return`。历史实例：dsh 的 `dsh-helper` + `DSH-Helper`（**大小写不同的孤儿条目**）两条 Run 值都指着被废弃的 `release\dsh-helper-1.8.2\`；而 `migrate_autostart` 只读 `APP_NAME` ⇒ **大小写变体永不在其视野内**。**已消除的部分**：Run 键本轮已改指 1.8.1（HANDOFF §1.5）；`DSH-Helper` 孤儿条目已不存在（本日 22:12 **只读回读** Run 表，只剩一条 `dsh-helper`）。**判据侧已满足"漂移变红"**：C-40 强断言（Run 目标目录必须 == `release/<源码 VERSION>/`）的负控格 `live_dsh_case_flagged` 就是"1.8.2 vs VERSION 1.8.1 ⇒ FAIL"（逐字搬入真实反例，§4.1.42）。**未落地部分（推翻开关交 lead）**：把谓词改成"等于源码 VERSION 对应的目录"**必须改 `modules/autostart/autostart.py`**——那是**派发件**，改它会让 dsh/ocx/l-s2t 三份副本立刻 `[DIFF]`、`sync_check` 红灯、连带各自 `build.bat` 门禁 1.2 失败（与并发的 W5/W7/W8 直接冲突）。按"**影响最小的一侧**"本轮**不写派发件**。**✅ lead 2026-09-19 裁定（明确结论，勿当"没做"）**：本轮不写派发件，**谓词改造并入下一波可重拷波次（与 T4 `update_helper` 接口扩展 / 四家重拷同一批）**；理由 = ① 改它是**派发事件**，会让 dsh/ocx/l-s2t 三份副本 `[DIFF]`、`sync_check` 红、各自门禁 1.2 失败，且与并发 W5/W7/W8 冲突；② **C-40 已能兜住漂移**（强断言 + `<VERSION>` 目录比对 + 真实反例自证格），"**存在性谓词 + 当前性判据并存**"是可接受的稳态——漂移由**判据**抓住，不必由**谓词**阻止；③ 用户本轮约束是避免重构与范围膨胀。**附带登记**：大小写变体 Run 条目曾是 C-40 与 `migrate_autostart` 的**共同盲区**（两者都只读精确键名）。**2026-09-19 更新**：C-40 修复后（§4.1.53）取**全表**并把大小写变体键打进 detail 的 `[注]` ⇒ **判据侧已可见化**；但 `migrate_autostart` 的视野仍未变（它只读 `APP_NAME`），故本条谓词部分仍待可重拷波次（见任务 #9）。 |


| 4.1.52 | **横幅「自报即自证」不成立：`conformance_check` 的横幅曾把 ref（`head:`）与内容 id 印在同一行**（任务 `#58`，2026-09-19 落地） | 工具**自印自己的 HEAD** = 被测对象供给判它的可观测量，属「**无判据**」而非「漏判」（与 `sync_check` 三处静默出口 `#57` 同构）。而自报的 `sha256` / `norm` 是**内容派生**、`head` 是 **ref** —— ref 必须由**读的人在外面配**（`git rev-parse HEAD` 的 blob id），两类证据**分开记、不互替**；`head(at pin)=X head(now)=Y` 仍把 ref 印进自报，不够。 | **已落**：`identity_line()` 的横幅改为 `# conformance_check <VER>  sha256:<raw>  norm:<norm>  at:<ISO>` —— 去掉 `head:`，保留内容 id 与**时点** `at:`（§4.1.28）。**被检仓库**的 `repo=<name> rev=<short> dirty=<yes|no>` 行**保留**：那是关于**对象**的外部证据，不是仪器自报。**同批条文**（路径解析两子句 + `FROM` 分支禁 `continue`）见 `STANDARDS.md §D8 附则 附 2/附 3`。 |

| 4.1.53 | **C-40 的 Run 键名口径假绿：按 `APP_ID` 单查，而 autostart 契约用 `APP_NAME`**（lead 2026-09-19 实测发现；tpl-keeper 同批修） | `_run_value(app_id)` → `QueryValueEx(k, app_id)`，但模板契约写的是 **`APP_NAME`**（`modules/autostart/autostart.py:44/53/113`）。四家里 dsh/ocx/reme 的 `APP_ID == APP_NAME`（恰好相同，判据看起来是对的），**只有 l-s2t 不同**（`APP_ID=local-speak2text` vs `APP_NAME=LocalSpeak2Text`）⇒ **C-40 对 l-s2t 的强断言从未执行**（输出 `Run[local-speak2text]=（无）`）。**更贵之处**：它让 §4.1.42 的内测结论「l-s2t 无 Run 项 ⇒ 强断言不适用」**一起错了**——判据与文档互相佐证一个假结论，正是 §4.1.10b（文档不反向更新）+ §4.1.24（散文与代码两份描述、先漂散文）的同族。**对照**：`HANDOFF §1.5` 反而是对的，未改。**旁证（为什么不能只换成 APP_NAME）**：reme 的 `APP_NAME="ReMe 助手"` 而 Run 键是 `reme-helper`（其内联自启用 APP_ID）⇒ 必须**双候选**。 | **已修（`conformance_check.py` 1.9.16；lead 二次更正「不能只改用 APP_NAME」后定稿）**：`_run_values()` 取**全表** → `select_run_entry()` **路径优先、键名兜底**（机制见 §4.1.54）：① **路径腿**（主）枚举全表，值里的路径落在**本工具仓库根或稳定安装位**之下即命中——**不依赖键名**，两种形态都覆盖，且能排除外来串台项（`OpenCodexTray-…vbs`）；② **键名腿**（兜底）= `APP_NAME`→`APP_ID`，覆盖 dev 态等路径异常。detail **打印实际走的哪条腿**（`选键腿=path/name/none`）与两个候选值；`key=None` 与「命中但值坏」可区分（§D8 第 6 条）。附带提示：多个 Run 项指向本工具、命中键不是候选（大小写变体/第三形态，§4.1.51）、两候选同时存在。**自证 5 条腿（§4.1.37；含 lead 要的两条正样本）**：① 模板形态（键=`APP_NAME`，l-s2t 真值）**旧单选必漏、新路径腿必中**；② 内联形态（键=`APP_ID`，reme 真值）必中；③ **外来项反向格**（值不落在本工具目录 ⇒ 不得命中）；④ 两候选皆无 ⇒ None；⑤ 大小写变体/重复项进 notes。**修后实测**：l-s2t 输出 `Run[LocalSpeak2Text]="…release\local-speak2text-1.4.0\local-speak2text.exe"`，强断言**真的执行**（目标目录 == `release/local-speak2text-1.4.0/` ⇒ 无 FAIL）；它现在转 WARN 是**另一件事**——孤儿目录 `_stale_local-speak2text-1.4.0-20260919-204004` 未登记（可清理、未获授权）。 |

| 4.1.54 | **Run 键名没有单一契约：模板 autostart 用 `APP_NAME`，reme 内联用 `APP_ID`**（lead 2026-09-19 定；与 §4.1.53 同批） | 两个实现**各自都是对的**，合起来没有共同键名：模板 `modules/autostart/autostart.py:44/53/113` 全用 `APP_NAME`（l-s2t 的键 = `LocalSpeak2Text`，`appconfig.py:13` 注释明写「历史注册表自启键名，改名 = 断链（NAME-05），不得擅动」）；reme `src/main.py:3577/3589/3592/3630/3634` 全用 `APP_ID`（键 = `reme-helper`，其 `APP_NAME` 是中文展示名 `ReMe 助手`）。⇒ **任何「只认某一个键名」的判据都必漏一半**（这正是 §4.1.53 假绿的根因）。**注意**：l-s2t 的历史键名属**允许的差异**（NAME-05：改名 = 断链），**不是缺陷，不得为过判据去改键名常量**。 | **处置**：C-40 选键改为**不依赖键名**的路径优先（§4.1.53）；本条登记为「两实现各自正确、合起来矛盾」的**允许差异**，**不要求统一键名**。**同族**：`sync_check` 覆盖不到的那类家族不一致——共享件之外 / 各仓自有实现，没有正本可比。 |

| 4.1.55 | **R-10 加宽的前置条件：key 必须换全路径（三处）+ 仓内落点无人兜底**（任务 `#64`，2026-09-19；**本轮只登记、不实现**） | **① 无人兜底的缺口**：R-10 运行期腿的根只有 `%TEMP%`；**仓内三处落点**（l-s2t `build\test-data`、`build\selftest-data`、`%RELEASE_DIR%\smoke-data`）既不在扫描面内（`:2172` 枚举 `%TEMP%` 子项名；`:2300` 集合运算），也不在 git 可见面内（`local-speak2text/.gitignore:3 build/`、`:4 release/`）⇒ **git status 同样看不见**。⇒ 不是"R-10 窄但别人兜得住"，是**无人兜底**。<br>**② 加宽的第一步不是扩列表，是换 key：裸名 → 全路径**：`:2300 union = sorted((set(names_a) \| set(names_b)) - set(TMP_DECLARED_PATHS))` 是对**裸名**做集合运算 ⇒ 多根下同名目录的去重会变成**误伤**；且 `:2172 d.name in TMP_DECLARED_PATHS` 的过滤在**判定阶段**，裸名 `reme-helper-builddata` 会吃掉**任何根下**同名目录。<br>⇒ **换 key 必须同时覆盖三处**（`names_a` / `names_b` / `TMP_DECLARED_PATHS`），否则扩根会扩出一个"**看着能扫、实则被白名单吃掉**"的判据。<br>**③ reme 侧现场读数**（只读枚举，未创建/删除）：`$TEMP/reme-helper-builddata/` 在盘上、被白名单在 `:2172`/`:2300` 两处减掉 ⇒ **腿 A 与腿 B 都看不见**（机制与 l-s2t 不同：它被**白名单**关掉，l-s2t 三处被**扫描面**排除）。<br>**④ 白名单这一格：查后判为非缺陷**（`§4.1.15` 的设计）：`:2323-2340` 全条打印白名单（含不在盘上的），每条带 `[为什么不算残留]` + `[重验触发条件]`，并有 `_declared_problems()` 查两栏缺失 ⇒ 是**带 datum 的已批准豁免**，非隐藏静默出口。**唯一可挑且其自陈**：`reverify` 为**人工触发**（"该行被改动时"），**无机械复验腿**——与 `#57` 同族，已知且已书面化。 | **本轮只登记不实现**（台账原裁定"交 tpl-keeper，**本轮不动手**"）。**实现属独立改进**：需扩根 + 三处换 key + 为**每个新根**实测判定逻辑（避免假红），且 R-10 是**取证工具**（`--temp-leak` 永远 `exit 0`）⇒ **无即时危害**。<br>**下一轮若做，验收口径**：扩根后必须给出"**每个根各自的扫描面 + 命中数**"，且用**合成样本**证明"两处同名目录不会被去重吃掉"。<br>**配套纪律（阴性结论必须与阳性对照同句，§4.1.13 同族）**：verifier 靠 `git check-ignore -v` 才纠回自己"`.gitignore` 无"的误判；四仓 `grep "^# TEMPLATE-MODULE"` → 0 时**必须附模板正本 18 当对照**——没有那个 18，"真的全 0"与"正则写错"读数**完全相同**。<br>✅ **2026-09-19 已落（任务 A2，`conformance_check.py` 1.9.24）**：① **换 key = 全路径**（`_leak_key`），同时覆盖 `names_a` / `names_b` / `TMP_DECLARED_PATHS` 三处；② **扩根** = `%TEMP%` + l-s2t 三处落点（`build/test-data`、`build/selftest-data`、`release/<ver>/smoke-data`），逐根打**候选数 + 双腿命中数**；③ 白名单 key 与基线文件同步换全路径。**自证**：`R-10/dedup` 格 PASS（两处同名 `dup` 并集=2，裸名 key 会=1；全路径豁免反向格）；`--temp-leak-save` / `-baseline` 全路径往返实测 0 新增。证据：`H:\Tools\_verify-scratch\A2-r10-temp-leak.txt`。 |

| 4.1.56 | **C-44 的段首盲区：`if exist X findstr …` 这类裸名漏判**（verifier 2026-09-19 复核发现；**本轮只登记、不改**） | C-44 的 `_BAT_CMD_SPLIT`（`\|`/`&`/`(`/`^`）**不切空白**、只取**段首 token** ⇒ 形如 `if exist foo findstr /i …` 的行，段首是 `if`，其后的裸名 `findstr` **不会被判**。<br>**verifier 明说"当前四家 + 模板仓内无此形态，故不翻案"** ⇒ 是**潜伏**缺口，非现役缺陷。 | **登记，不改**。**为什么不改**：修法是"把空白也纳入切分"，但那会**改变现有 token 切分语义** ⇒ 有引入假红的风险（本仓 bat 里有大量 `if … (` 结构），而**收益为零**（无真实案例）。与 §4.1.33「**别用一条会命中正常代码的规则冒充守卫**」同族。<br>**下一轮若改，验收口径**：先在本仓 `.bat` 上跑"**改前/改后命中数对照**"，证明**只多抓潜伏形态、不误伤现有合法行**（对照格，§4.1.33）。<br>✅ **2026-09-19 已落（任务 A1，1.9.23）**：先做对照再改——全家族 6 根 11 个 `.bat` 改前/改后 **added=0 / removed=0**（不误伤现有合法行）；合成电池里 **naive 全空白切分 5/5 正样本命中但误伤 6/9 条合法行**（`echo find`、`call :x find` 等）⇒ 否掉，改用**窄版** `_bat_cmd_tokens`（仅当段首为 `if` 时按 cmd 条件语法推进到命令 token）：**5/5 潜伏形态命中、9/9 合法负样本不命中**。自证增 2 格（判别力格 `if_exist_bare_cmd_flagged` + 反向格 `if_exist_echo_find_ok`）。证据：`H:\Tools\_verify-scratch\A1-c44-blindspot-eval.txt`。 |
| 4.1.57 | **verifier 的 F-5 登记「横幅丢了 `head:` 字段」应被驳回 —— 那是 `#58` 的有意设计**（lead 2026-09-19 裁定） | verifier 复核时看到 `1.9.13` 的横幅曾印 `head:3ed3e12`、而 `1.9.18` 去掉了它，据此建议"恢复"。**但 `conformance_check.py:326-328` 的注释明写**：**横幅不印 ref**（任务 `#58`）—— 工具自印自己的 HEAD = **被测对象供给判它自己的可观测量**，属"**无判据**"而非"漏判"；ref 由读的人在外面配（`git rev-parse HEAD` 的 blob id），与自报的 `sha256`/`norm` **两类证据分开记、不互替**（§D8 附则 附 2）。<br>⇒ 被检仓的 `repo=… rev=… dirty=…` 行**仍然保留**（那是**对象证据**，不是自报）。 | **驳回**，不改。**教训**：复核者读到的是**两个时点的差异**，但**差异 ≠ 回退** —— 判"是不是缺陷"必须读**当时的裁定理由**（`#58` 的条文），否则会把**设计**当成**损失**（§4.1.48「拿已知缺陷输入喂进去，有没有可观测量会变」的反向：**这里可观测量变了，但那是设计要它变的**）。 |

| 4.1.58 | **「未勾选」分支仍执行清理：把条款 3 的*作用域规则*当成了*触发条件***（**用户报告** 2026-09-20；已修 + 已立判据 C-50） | **现象**：ocx 关闭后**即使没勾选"同时关闭隧道"，隧道服务也被关了**。<br>**现场**：`on_quit` 把清理拆成两半 —— `if stop_tunnels: kill_target_procs(...)` / **`else: 无差别 `terminate()` 所有 OWNED 句柄**。⇒ 没勾选也清。<br>**规范**：`STANDARDS §G4.2 **条款 5**` 是**明文** —— *"退出确认弹窗提供'顺便关闭服务/隧道'勾选项，**默认不勾**；**不勾 = 服务与隧道越过托盘生命周期继续运行**"*。<br>**根因（值钱的部分）**：旧注释写的是「有界清理（G4.2 **条款 3**）：只停自己启动的（OWNED）」—— 它把 **条款 3 的「作用域规则」**（*清理谁*：只清接入实例、禁全量签名击杀）**误当成了「触发条件」**（*要不要清*）。**两条款分工：条款 5 管要不要，条款 3 管清理谁，不可互推。**<br>**为什么只有 ocx 犯**：dsh / reme 把两者**压在同一条 `if <勾选>:` 里**（`else` 只记日志 —— dsh `log("dsh service left running…")` / reme `notify("…保持运行")`），结构上就没有这个缺口；**ocx 拆成 `if/else` 并在 `else` 补了"有界清理"**，于是踏空。 | **已修**（ocx `64f8fa8`）：`else` 分支只记日志。OWNED 隧道与外部隧道同属"越过托盘继续运行"（条款 4：放行是合法状态），下次启动由探测自动重新接入。**依据**：本家族**零 Job Object**（R1 §4.1.30 全仓 grep 实测）+ "子活父死"实测 ⇒ 子进程不随父退出而死。<br>**已立判据 C-50**（1.9.25，FAIL）= 退出路径（`on_quit`/`quit_app`/`_decide_quit`）的 **`else` 分支**不得出现破坏性调用；自证 3 腿（红格 = 本缺陷真身 / 反向格 = 勾选分支里 kill **合法** / else 只记日志放行）。四家实测 `[ok]`。<br>⚠ **产物未更新**（`release\opencodex-helper-1.2.1\` 有活实例在跑 ⇒ 构建**正确地**干净拒绝）；**须由用户退出托盘后重建**。 |

| 4.1.59 | **无 UI 的退出入口（`--quit`）沿用了"用户在*有确认框*时保存的勾选"**（2026-09-20 排查用户报告时发现；已修 + 已立判据 C-51） | **现象**：`--quit`（外部工具/脚本用的**无 UI** 入口）会让**没有任何人被问过**的一次退出，执行"停服务/停隧道"。<br>**现场**：reme `quit_watch_loop` → `shutdown_tray(TRAY_ICON)` **不传 kwargs** ⇒ `stop_reme/stop_tunnels` 落 `None` ⇒ 函数内回读 `CFG["quit_stop_*"]`。⇒ **勾过一次"退出时停服务"的用户，会被一次外部 `--quit` 静默停掉服务**。<br>**同族**：`§4.1.43`（C-41）的母题原话 —— *"那个勾选是用户在**有确认框**的语境下保存的；链路坏掉时用户根本没被问过"*。**C-41 只查降级分支**（`except` / `if x is None:`），**不覆盖 `--quit` 这条独立路径** ⇒ 本条是 C-41 的**覆盖面补充**。<br>**排查结论（三家对照）**：`dsh`/`ocx` **无 `--quit`** ⇒ 不适用；`l-s2t` 的 `--quit` 走 `exit` 分支、触发的是"**应用用户自己下载的更新**"（非破坏性、且是用户意图的延续）⇒ 不构成缺陷；**只有 reme 中招**。 | **已修**（reme `fcb8fcf`）：`shutdown_tray(TRAY_ICON, stop_reme=False, stop_tunnels=False)`。托盘菜单路径不受影响（走 `quit_app`，用户**确实被问到了**）。<br>**已立判据 C-51**（1.9.26，FAIL）= `quit_watch_loop` 内对 `shutdown_tray`/`on_quit`/`quit_app` 的调用必须**显式**传 `stop_reme=False, stop_tunnels=False`。<br>⚠ **覆盖面教训（本判据首跑翻的车）**：首版**没排除 `src/modules/**`** ⇒ 把模板 `tray_kit.quit_watch_loop`（**机制件**：只回调、不读配置）报成 4 条 FAIL（**假红**）。已加**豁免腿**（同一段"有罪代码"放进 `src/modules/**` ⇒ 必须不报）—— **判据的适用范围必须自己先想清楚**（§4.1.18 同族）。 |

| 4.1.60 | **C-38 的锚只认一种日志包装名：`log(` / `print(`，不认 `_log(`**（2026-09-20，修 C-38 时发现） | **现象**：ocx 的 C-38 恒报「**锚 0 处（无）**」，即使它**确实**有启动日志。<br>**旧归因（R1 §3 T6）**："ocx 用 `_log(` 不是 `log(`、词是 `starting` 不是 `startup`" —— **对了一半**：措辞改了之后锚**仍不命中**，真因是判据的正则 `(?:^|\W)(?:log\|print)\s*\(` —— **`_` 属 `\w`，前面的 `(?:^\|\W)` 不成立** ⇒ `_log(` 永不匹配。<br>**为什么值钱**：这类缺陷的形状是「**判据说'没有'，而事实是'有'**」——它会让下一个人去改**本来是对的东西**（去改 ocx 的措辞），而真凶在判据自己身上（与 `§4.1.37` 判据读散文同族）。 | **已修**：正则改为 `(?:_?log\|print)\s*\(` —— 接受可选下划线前缀（本家族现役两种形态 `log` / `_log`）。**不用 `\w*log`**：那会把 `catalog(` 也当成日志调用。<br>**同批的连带修复**：统一四家措辞时把 ocx 的 `starting` 改成 `startup` ⇒ **ocx 的 `tests/test_startup_path.py:152` 断言 `any("starting" in line …)` 失配** ⇒ 构建被门禁拦下。已把断言改成 `"startup"`（**码是为了四家措辞一致才改的，测试应跟随**）。<br>**教训**：**改文案会打断依赖该文案的测试** —— 而那个测试守的是"启动序列走到了"，与措辞无关；**断言应该锚在语义上（走到启动），不该锚在具体词上**（与 §4.1.36「读数必须带尺子」同族：**换把尺子，读数就变了**）。 |

| 4.1.61 | **判据的"豁免分支"是盲区：C-20 对"未启用 i18n"直接放行，无人核对豁免前提**（用户 2026-09-20 报告时暴露；已补判据 C-52 + 已补条文） | **用户报告**："dsh-helper 没有中英" —— 并给出**正确的流程判断**：*"4 个原有工具之间的对齐是最简单的，结果这个都漏掉了 ⇒ 说明验收标准有问题 / 公共模板规范没对齐 / 检查流程有纰漏"*。<br>**实测真相**：dsh **有** i18n（`src/modules/i18n/` 三件与模板一致、菜单第 24 项即 `English / 中文`、`init('en')` 后 `退出`→`Quit` 实测有效）。用户看到的是**旧产物**：`release\dsh-helper-1.8.2\`（exe **09-19 13:37**），而 i18n 是 **`477bc7c`（09-19 15:05:03）** 才引入的 —— **早 1.5 小时**；Run 键直到本波 21:16 才从它改指 1.8.1。<br>**但流程判断成立**：`C-20` 的实现是<br>`if not c.has_i18n(): return True, "未启用 i18n（T1 未触发或待办）"`<br>—— **直接放行，且没有任何判据核对那个理由是否成立**（这个工具是否真的还没开源？）。⇒ "**该启用却没启用**"是一个**不红不黄、连"跳过了什么"都不打印**的状态。 | **判定**：**规范存在**（`§A2 T1` 触发条件①"交付他人/开源发布"），**缺的是检验**。<br>**已补判据 C-52**（1.9.27，FAIL）= `git remote` 非空（= 已开源）⇒ 必须有 `src/modules/i18n/` 或 `pairs.json`（§E4 许可）；判不了（非 git 仓库）按未触发放行但**打印扫描面**（纪律 ⑥）。自证 4 腿（红格 / 未触发 / 重形态 / 有目录）。<br>**已补条文**：`§A2 T1` 行下加「**触发的可判形态**」，写明"未启用 i18n **不是**合法默认态，必须与触发条件对得上"，并立纪律：**判据的每一条豁免，都必须有一格能核对"豁免前提是否成立"**（§4.1.18 同族）。<br>**顺带纠正一条归因**：这条第一次被记成"dsh 缺 i18n"，**实测是"用户看到了 i18n 引入之前的产物"** —— 与 §4.1.13「"我没搜到" ≠ "它不存在"」同族，只是方向相反：**"我看到了"也可以是"我看到了旧的"**。 ⚠ **已被取代（2026-09-20）**：§A2 已按用户裁定把双语改为「默认要求、不再是触发式」，C-52 → 1.9.28；本条所述「触发的可判形态」已不适用（保留在案）。 |
| 4.1.62 | **门禁把"异步副作用"当判据 + "脚本没跑完"没有独立判据 ⇒ 失败被记到别的断言头上**（2026-09-20；l-s2t 已修，**真实机制未定**） | **现象**：l-s2t `GATE 2d` 在 CI 上红、本机同一份字节 5/5 全绿。两次发版 CI 都停在同一步（run `35488810525`／v1.4.1 与 run `35490593435`／v1.4.2 的错误注解都指向 `#step:7` = **Build release**，即 `build.bat`），⇒ **不是偶发，是环境相关的确定性失败**；而 CI 步骤日志**需登录才能读**（匿名只看到 "Sign in to view logs"）。<br>**现场（从日志末行反推，三重核对）**：`log_text[-100:]` 的**末行是一条 `start` 行**。三个场景的日志末行分别是 `done`／`restored - starting previous version`／`RESTORE FAILED` ⇒ 只有"报了 start 却没有后续"的场景能留下这种尾巴 ⇒ **脚本写了 `:182` 的 start 行之后、在 `:stage_invalid` 的 `echo` 之前就没了**，且 `_check_no_hang` 通过（不是挂死）。<br>**根因（值钱的部分，两半）**：**① 判据把异步副作用当结论** —— "旧版被拉回""新版被启动"是用"等 `.vbs` 写出的 marker"来判的。而 ①`start ""` 拉起的进程**可能被拒绝创建**（桌面堆压力），②**robocopy 在"大小 + 时间戳都相同"时把目标当成同一个文件直接跳过**——本仓两份替身脚本只差 `started-old.txt`/`started-new.txt`（**等长**）且同一时钟 tick 内写下。**这两条 reme-helper 都已实测（各约三次一次）、都已裁定、都已修掉**，是 l-s2t 的 B5 新测试**重新引入**的。<br>**② "harness 有没有把脚本跑完"不是一条判据** —— 于是它附身到**碰巧先执行的那条断言**上，报出来的名字是"日志没记拒绝"，与真实成因无关。当晚据此排查，四条候选（`rem` 里的 `\|`、`rem` 里的 `>`、重定向失败中止批处理、LF-only 批处理）**逐条被独立探针证伪**，全部探针留在 `H:\Tools\_verify-scratch\`。 | **已修**（l-s2t `01d3887` + `061126d`）：判定改用**确定性**证据（日志分支行 + 安装目录内容），marker 降级为**观察**（照 reme 的 `_observe_started` 口径）；新增 `_reached_terminal()`（模板 bat 每条收尾路径都会且只会写一行终态：`done`／`STAGE INVALID`／`restored…`／`RESTORE FAILED`／`aborted:`）作为独立的 ok/FAIL，失败即重跑一次 + 打印全取证（stdout/stderr/日志/marker/`@echo on` 逐行 trace）；`_stage()` 按场景清 `update.failed`/`update.log`（消掉两处**跨场景假绿**）。**无谓的重试删掉了**（`_bat_success` 那次重试原本就是在盖 robocopy 跳过）。<br>**取证通道**：把 GATE 2d 加进 `tests.yml`（每次 push 都跑，不再只在发版时暴露），并让失败路径发 `::error::` **注解**——**注解是公开可读文本，日志不是**（本人已实测匿名可读注解、不可读日志）。`_gha_annotate()` 的转义（`%`→`%25`、换行→`%0A`，顺序不可反）有自证探针。<br>⚠ **未结项**：真实机制**仍未定**（本机 5/5 复现不出，CI 日志读不到）。v1.4.2 的 release 仍红在同一格。<br>**纪律（两条，供全家族）**：① **判据不得依赖"被拉起的进程真的跑起来了"这类异步副作用**——它换来的是假红，而假红会训练人忽略红灯；② **"脚本/子进程有没有跑完"必须是**一条有名字的判据**，否则它会附身到别的断言上，把排查引向错误的方向。<br>✅ **2026-09-20 结项（真因已定位，本条上面那半段归因是错的，保留在案）**：**真因 = 测试替身 bat 的行尾与产品不一致**。产品 `update_helper.download_and_prepare()` 用 `script.write_text(text, encoding="mbcs")`（**不传 `newline`**）⇒ Windows 文本模式把 `\n` 翻成 `\r\n`（实测：114 CRLF / 0 裸 LF、6523 字节）；而测试写的是 `newline=""`（**关掉**那次翻译）⇒ 6409 字节、**全裸 LF**。**cmd.exe 对 LF-only 批处理文件的 `goto` 标签查找与字节相位有关**：同一渲染器下逐长度扫描 47 个根路径长度，**root 长度 79..85 时 `goto stage_invalid` 报 `The system cannot find the batch label specified`，78 与 86+ 正常**；CI 的 scratch 根 `C:\Users\RUNNER~1\AppData\Local\Temp\l-s2t-upd-temp-XXXX\l-s2t-bat-YYYY` **正好 79 字节**，本机 `H:\Tools\_verify-scratch\l-s2t-bat-XXXX` 约 45 ⇒ **"CI 红、本机 5/5 绿"的全部原因**。改成 CRLF 后 **47 个长度 0 失败**（对照：LF 下 7 个失败）。⇒ 这是**测试保真度缺陷**（"内容一致"不等于"落盘字节一致"），**不是产品缺陷，也不是 CI 抖动**。<br>**四条教训（比结论值钱）**：① **测试必须与产品落盘的字节一致**——行尾也是内容，而且它能在**另一个层面**（cmd 的解析器）决定成败；② **"LF 已被证伪"那一次是错的，因为量错了层**：量的是模块文件在盘上的字节（CRLF），而代码真正交给 cmd 的是 Python 字符串（LF —— Python 读源码时做 universal-newline 转换，再被 `newline=""` 原样落盘）⇒ **判据必须量"被测对象真正使用的那一层"**；③ **第一手证据一直就在手边**：bat 自己的 stderr 写着 `cannot find the batch label specified - stage_invalid`，而当时那行被 `stderr=DEVNULL` 吞了 ⇒ **先开取证通道，再谈归因**；④ **降级/重试不能替代定位**：中途把失败归因为"环境扰动"并加 retry、把 marker 改观察，**是在没定位前就收口** —— 方向错了（那两条改动本身是真缺陷，留着，但它们不是原因）。<br>**已落**：l-s2t `da6dbbe`（替身 bat 写 CRLF）+ `d798e26`（GATE 2e-2i 也进每次 push 的 `tests.yml`；`release.yml` 把 build 失败尾部发成 `::error::` 注解）。<br>⚠ **同类潜伏缺陷（已定位并已修）**：`reme-helper/tests/test_update_bat.py:217` 也用 `newline=""` 写**真渲染的** update bat ⇒ 同一颗雷，它今天只是**恰好**没撞上坏相位（其 scratch 根 `…\Temp\reme-update-bat-XXXXXXXX` 长 62 字节，不在 79..85）。**已修**（reme `fc6206a`，改成 `newline="\r\n"`，测试仍全绿）。**另两处 `newline=""` 经核实无须改**：l-s2t `tests/test_startup_path.py:128` 与 `test_update_safety.py:601` 写的是**字面量里自带 `\r\n`** 的两行假 bat（`newline=""` 在这里恰恰是**保留** CRLF 的正确写法），且**不含 `goto`**，无标签查找可失败。⇒ **同一行代码在同一仓里既可能是缺陷也可能是正确写法，判据必须看"这段文本的行尾从哪来"**。 |
| 4.1.63 | **判据的期望值取自"仓库没钉住的输入" ⇒ CI 必红、本机必绿，且与被测代码无关**（2026-09-20；l-s2t `b1b491c` 已修，**未修的是它的根**） | **现象**：l-s2t `GATE 3`（`python src\pipeline.py`，真 ASR 往返）在 CI 上连红 **四轮**（v1.4.1/.2/.3/.4），本机每次都绿。CI 注解（1.4.4 新加的 `::error::` 通道）一次就给出了现场：`RuntimeError: 自检失败：定稿文本与预期相差过大`；`定稿文本: 开饭时间早上9点至下午5点。`；`候选 ['欢迎','达摩院','语音']`。<br>**根因**：断言写的是"命中 `("欢迎","达摩院","语音")` ≥2 个"，那是 **paraformer** 测试 wav 的句子（本机 `asr-modules/` 里那份）；而 CI 的 `release.yml` 下载的是 **sensevoice** 那个 release，并拷它自带的 `test_wavs/zh.wav` —— **两句不同的话**。⇒ 门禁的期望值**取决于一份仓库没有钉住的输入**。它 2026-09-19 才加（`1618b3c`），**v1.4.0 发版时还不存在**，这正是"以前是绿的"的原因。<br>**为什么值钱**：① 这条**永远不会在开发机上红**（本机 wav 正好是期望的那句）⇒ 只能靠 CI 暴露，而 CI 又是最后一个环节；② 它**与被测代码完全无关** —— 期间任何一次"改代码→CI 红"的归因都会被它带偏（本轮就白跑了三轮 tag）；③ 它的形状是"**判据的输入没被钉住**"，与 §4.1.61「判据的豁免分支是盲区」同族：**都在说"判据的成立条件自己没有判据"**。 | **已修**（l-s2t `b1b491c`）：改成"与一组**已知参照文本**做**字符级重合率**，取最高者 ≥0.6"（`difflib`，只归一化标点/空白）。实测判别力：本机句 1.00／CI 句 1.00／ASR 小波动 0.95／乱码 0.00／空 0.00 ⇒ **"乱码必红"的能力保住了，而判据跟着输入走**。每次运行都打印两个重合率；失败信息里写明"换过 wav 就把正确文本加进 `_REFS`"。<br>⚠ **根未除（已登记，下一轮）**：真正的解法是**把测试 wav 变成仓库资产**（或把参照文本与 wav 一起 vendor 进来），让期望值有唯一确定的依据；本轮只做到"对已知两份输入都正确 + 对第三份可自述"。<br>**纪律（供全家族）**：**门禁的期望值必须来自仓库内的、可核对的依据**；期望值若依赖外部下载物或本机既有文件，就不是"门禁"，而是"**取决于环境的巧合**"。可机械核对的一条：**每条断言都要能回答"它比的这个值，是从哪来的？"**（与 §D8"锚必须是可核对的对象"同族）。 |
| 4.1.64 | **门禁只在"tag 触发"的发版流水线里跑 ⇒ 修门禁本身必须打 tag，而打 tag = 发版**（2026-09-20；**四家全部命中，已全部修复**） | **发现路径**：修 l-s2t 门禁时，改完**没有任何办法验证**——`tests.yml` 只跑 compile/i18n，真正的门禁都在 `build.bat` 里，而 `build.bat` 只被 tag 触发的 `release.yml` 调用。于是"修门禁"被迫变成"打 tag"（v1.4.2/.3/.4 三个 tag 都是这么来的），**把一次门禁修复伪装成三次发版**，正是 §G3.7 要防的形态。<br>**四家实测覆盖面**（按"push 触发的 `tests.yml` 是否覆盖 `tests/*.py`"）：<br>· **l-s2t**：`tests.yml` **一个 `tests/*.py` 都不跑**（只 compile+i18n+icon）；`build.bat` 有 12 道门禁（2b..2i、GATE 3、smoke）⇒ 全在发版时才跑。<br>· **reme**：`tests.yml` 跑 9 个套件，但 `test_update_bat.py`（更新链真跑 bat）**不在其中**，只在 `scripts\build.bat`（根 `build.bat` 是转发壳）。<br>· **dsh**：`tests.yml` **一个 `tests/*.py` 都不跑**（只 compile+import+一条内联版本比较）；`tests\test_*.py` **7 个套件**只在 `build.bat` 的 `for %%t in (tests\test_*.py)` 里跑。<br>· **ocx**：同上，**9 个套件**只在 `build.bat` 里跑。<br>⇒ **"每次 push 都绿"在这些仓里几乎不构成证据**：`tests.yml` 覆盖的只是"能不能编译/能不能 import"。 | **已修**（四家，均不打 tag、不发版——**因为门禁修复不产生新产物**）：把门禁搬进 push 触发的 `tests.yml`。<br>· l-s2t `061126d`＋`d798e26`：GATE 2d 单独一步 + 2e..2i 各一步（一格一 gate，失败时 UI 里直接点名）。<br>· reme `9680683`：加 `test_update_bat.py` 一步。<br>· dsh `4282d65` / ocx `25db66f`：**整段套件**一步（`tests/test_*.py` 全跑）。<br>**三处共同的实现要点（值得照抄）**：<br>① **必须复刻 `build.bat` 的套件级 data-dir 固定**（dsh `DSH_HELPER_DATA_DIR`／ocx `OPENCODEX_HELPER_DATA_DIR`／l-s2t `LOCAL_SPEAK2TEXT_DATA_DIR`）——build.bat 原注释称之为 **F11/D12 "belt and braces"**：某个测试文件忘了自己钉数据根时，仍然不能写到机器真实的 `%LOCALAPPDATA%`；<br>② **失败必须能点名到文件**：步骤日志需登录、注解不需要 ⇒ 用 `::error title=tests failed::<文件名>`（换行 `%0A`、`%` `%25`，顺序不可反）；<br>③ **失败必须真的非零退出**——只打注解而 exit 0 就是**假绿**（自证两条腿实测：全过 exit 0 / 注入一个失败 exit 1 且注解点名 `test_zzz_bad.py`，见 `_verify-scratch/pwsh-suite-loop-selftest.ps1`）。<br>**四家 CI 实测**：l-s2t tests #15/#16、reme tests #42、dsh tests #9、ocx tests #10 全 **Success**，且无 `tests failed` 注解。<br>**纪律（供全家族）**：**"能修"与"能验证修复"是两件事**；一条判据若只在发版流水线里执行，那么它同时**把门禁修复的成本抬高到一次发版**，结果是**没人愿意修门禁**（本轮四家都带着这个缺口跑了很久）。⇒ **凡门禁，必须有一条 push 触发的执行路径**（可机械核对：把 `tests/*.py` 的集合与 push 触发工作流实际执行的集合做差，**差集必须为空或每条都有书面理由**）。 |
| 4.1.65 | **"时新性 / 新鲜度"判据的参照系必须稳定，且被测集合必须排除机器生成物**（2026-09-20；**[单家强证据]**：仅 l-s2t 1 家） | **两个反例都已被实测钉死**：① **不能拿 HEAD 的时钟当基准** —— dirty 仓上恒真（实测判"新鲜"而 `src/` 里 **6 个文件更新**）；② **必须排除 `__pycache__` / `*.pyc`** —— `src/` 下最新的是**门禁自己刚生成的 `.pyc`**，比最新真实源文件还**新 17 秒**。⇒ 两者都让判据在**无人察觉时恒为"新鲜"**。<br>**与 §4.1.49 的分工**：那条管**分母（范围）**（分母小于真实打包输入集）；本条管**参照系（HEAD 时钟）**与**排除项（机器生成物）** —— 同一判据上的**两个独立维度**，**修好任一个都不会让另一个失效**。<br>**与常识的区别**：常识是"拿最新时间戳跟一个时间点比"；本条要求**基准本身在 dirty 状态下也必须可判**，且被测集合要**区分"人写的"与"机器生成的"**。 | **处置：登记**（本轮 l-s2t 已在其门禁落地这半条：`分母剔 __pycache__/*.pyc` —— 该半**与 C-46 同源、已落**）。**未落的是参照系那半**：`不得用 HEAD 的时钟` **无机械判据可写**（参照系是设计选择，只能在评审时核对）⇒ **只登记、不新立 C-xx**。<br>**证据等级：[单家强证据]** —— **不作为"≥2 家"通用条**，仅供后续出现第二家时升级。<br>**来源锚点**：l-s2t `CHANGELOG §1.4.1`「新鲜度判据不能用 HEAD 的时钟」「新鲜度判据必须排除 `__pycache__`」。 |


### 4.2 蓝本豁免的收紧（建议，待用户裁定）

现状：`blueprints.txt` 里的工具被 `sync_check` 完全跳过。
问题：模板升级后蓝本可以无限期落后，而**唯一能发现落后的机制被关掉了**。

建议改为三档：
1. `[ok]` 归一化一致；
2. `[decl]` 已申报 OVERRIDE；
3. `[lag]` **蓝本落后**——蓝本工具不再整体跳过，而是比对其"已采用模块"是否落后于模板版本号，落后即黄灯（不阻断构建，但计入交付自查）。

### 4.3 首版审计中被推翻的误判（记录口径，防后人重犯）

| 误判 | 真相 |
|---|---|
| reme-helper A1-10"文案散落违规" | 重形态（中文即键 + 外置 `pairs.json`）**被 STANDARDS 明示许可**，且覆盖扫描已进门禁 |
| reme-helper A3-01"主题持久化违规" | A3 结论是"暂缓"不是"禁止"；F2 反而要求语言/主题只存 config |
| reme-helper E2-07 / E5-02 | E2-07 该工具无面板 token 概念（不适用）；E5-02 实际**有** tooltip/toast 浮窗（`main.py:4348/5211`）只是无边界约束 |
| dsh E1-01/E1-02"多解释器违规" | 纯托盘工具无"常驻根窗口"，**模板 `tray_kit` 明示**临时 Tk 根形态；真正要防的跨线程访问不成立 |
| dsh E2-06 / dsh G5-01 / dsh I-02 / ocx B3-02 | 均为**审计员自造要求**或把模板标准接口当工具偏离 |
| l-s2t T8/G3-01"CI 从不跑真实 ASR" | `release.yml` 会下载模型真跑门禁 3 |

**口径**：判定必须"证据 + 规范原文"双落地。规范没写的要求不得加码；
规范明示许可的形态不得判违规。

### 4.4 差异的允许条件（2026-09-19 用户定）

> **允许不一致的前提只有两条**：
> 1. **业务冲突**——前提是**双方都有该功能**。**"没有功能"不构成冲突，那是缺失**，必须补齐，不得以"允许不一致"论处。
> 2. **有更好的方案**——允许暂时独立，但必须给出**可验证的**更优理由。
>
> **两条的共同后续义务**：事后**必须评估"能否优化模板以吸收该差异"**。
>
> **推论**：`TEMPLATE-LOCAL-OVERRIDE` 是**留痕**，**不是豁免理由**。差异只有两种归宿——**消灭它**，或**说明理由并持续承担"回头改模板"的义务**。

**措辞纪律**：**"波次/排期"是时间安排，不是许可**。把差异写成"有意保留的独立波次"是误导性表述
（本轮 lead 自己犯过）。除上列两条前提外，**一切差异都是"未获允许的缺口"**。

**逐条判定（本轮重判；判定对象 = ALIGNMENT §3"不应对齐"清单）**：

| 差异 | 判定 | 依据 |
|---|---|---|
| `dsh-helper` 的 `ICON_ASSET` | **移出清单（差异已消灭）** | 模板 `icons` 2.0.0 **已原生支持** `ICON_ASSET`（`appconfig.ICON_ASSET` → `base_image()`），工具侧只是填参数 → 根本不构成差异，更谈不上"不应对齐" |
| `appconfig.py` 参数文件 | **保留**（非"业务冲突"） | 依据是**模板机制本身允许**：T1 就是为"每工具一份参数"设计的（D6/D15），`sync_check` 记 `[param]`；不属于"允许不一致"的两条前提，而是**设计上的一致形态** |
| `reme-helper` 重形态 `i18n` | **保留，但归入前提 2（更好方案）** | 双方**都有** i18n 功能 → 不是"没有功能"。属**方案差异**：reme 需 `pairs.json`（中文即键）+ 整句最长片段替换，量级百条。**模板吸收评估结论**：吸收需在模板内并存两套查表引擎，成本大于收益 → **暂不吸收**；义务保留（reme owner 需持续给出可验证的更优理由，模板侧继续评估） |
| `local-speak2text` 的 `updater` | **移出"不应对齐"清单，改记"未采纳的缺口"** | 实测**不构成业务冲突**：`src/updater.py` 与模板 `update_helper` 同为目标 `INSTALL_DIR` 的"查→下→校验→换"三段式（含 sha256）。差异只在**签名**（`check_update(config_path,…)` vs `current_version`）与 **repo 来源**（运行时 `config.update_repo` vs appconfig 固定）。前者是接口形态、后者是**模板可吸收**的一点（让 REPO 可被 config 覆盖）→ 按原则③**应收敛**，当前状态记 `[MISSING-MODULE]` 缺口 |

---

## 5. 机械化检查清单（能脚本化的条目）

> 目标：把"靠 AI 记得住"变成"不绿就构建失败"。
> **§5.1 已落地为 [`conformance_check.py`](conformance_check.py)**（2026-09-19 建立），与 `sync_check.py` 并列：
>
> ```bat
> python my-diy-tool-template\conformance_check.py                    :: 全家族
> python my-diy-tool-template\conformance_check.py --only C-08 C-09   :: 只跑守卫类
> python my-diy-tool-template\conformance_check.py --strict           :: WARN 也计入退出码
> ```
>
> 分工：`sync_check.py` 管"拷贝件与模板正本是否一致"（哈希级）；本脚本管"条款是否落地"（语义级）。
> **设计纪律 ①–⑧（⑤⑥⑦⑧ 于 2026-09-19 补，前四条同日由 lead 合并定稿）**：
> ① **只写能给出证据的检查**，判不了的宁可 WARN、不硬判 FAIL——误判一次，人就再也不信这个工具了（首版即修掉 6 处误判，见 §4.3）；
> ② **每条检查的输出必须带 `文件:行号` 或实际值**，否则等于没说；
> ③ **FAIL = 硬违规**（默认让退出码非 0）；**WARN = 需要人判断**，只提示；
> ④ **"不认识形态"与"检出违规"必须分开**（展开见下）；
> ⑤ **判据的每条限定，都必须用"已知正例"回验过才算数**（展开见下）；
> ⑥ **"0 命中"与"确实没有"必须分开：报 ok / 不适用时必须同时给出扫描面**（展开见下）；
> ⑦ **同一件事只允许一份判据：禁止自造第二套"加强版"**（展开见下）。
> ⑧ **承重前提必须"打印取值与来源"，不许只断言它为真**（展开见下）。
> 前四条管"**判据的输出要诚实**"，⑤管"**判据的构造过程要回验**"，⑥管"**判据的覆盖必须自证**"，⑦管"**判据的唯一性**"。
> **④ "不认识形态"与"检出违规"必须分开**（2026-09-19 补；同日由 lead 升级并合并两条口径）：
> **(a) 不通过消息必须与它实际检出的东西一致**——检不出就只能说检不出，**不许用不相干的模式
> 去解释失败**。反例：C-10 把"探针的消费形态不认识"说成"smoke 里跑了真守卫"，让人差点往
> `smoke()` 里塞一个会挂死构建的真守卫。**错误诊断比漏报更贵**——它会把人引向错误的修复对象。
> **(b) 判据遇到自己不认识的形态时，一律 `WARN + "形态不认识，需人工确认"`**，并在消息里写明
> "期望什么形态 / 实际看到什么"。**FAIL 只能用在确实检出违规证据的时候**（AST 调用节点、
> `文件:行号` + 实际值）。**不认识 ≠ 违规。**
> **(c) 判准（lead 2026-09-19 定，并入本条）：分支级别取决于「它检出的东西」，不取决于「它期望的形态」。**
> **确证违规 → FAIL**（"我确实检出了违规证据"）；**检不出 / 形态不认识 / 证据不足 → WARN**
> （附「期望什么形态、实际看到什么」）。对照：C-10 命中 `smoke()` 体内的 `acquire_single_instance`
> **AST 调用节点** = 确证 → FAIL ✔；C-11 取到字面量后**与 exe 名对不上** = 确证 → FAIL ✔；
> C-11 **看不到** `tasklist|findstr` 字样 = 证据不足 → WARN ✔。
> **降错方向的代价**：真缺陷从红灯变黄灯、GATE 不再拦（D1-02 就是这样被抓出来的，也是它差点被放过的原因）。
> **为什么升级**：同一元缺陷一天内出现**三次**——C-10 的 `check()` 带参形态、C-10 的正则读注释、
> C-11 的 PowerShell 形态；每次都是"判据只认自己那一款，别款一律报违规"。详见 STANDARDS §D7。
> **落地**：`conformance_check.py` 1.7.1 起支持按分支返回级别 `(ok, detail, "WARN")`；
> C-10 的两处兜底与 C-11 的"取不出字面量"改走 WARN，**能确证的仍报 FAIL**（C-10 的 AST 真跑
> 守卫节点、C-11 的错误字面量——后者正是 D1-02 的真实缺陷，不许放过）。
>
> **设计纪律 ⑤（2026-09-19 加）：判据的每条限定，都必须用"已知正例"回验过才算数。**
> 前四条管"**判据的输出要诚实**"，这一条管"**判据的构造过程要回验**"。实证（复核员做 C-32 时
> 逐条回验）：加"同一语句块"（本意防误报）→ **漏掉正典，命中 0**；加"最近一条赋值"（本意简化）
> → 落在 `except` 分支的 `detail = ""` 上（同一变量两条赋值），命中 4、**漏了 reme**；
> 改成"遍历函数内**所有**先前赋值"才得到 5 处命中、5 处全真、零假阳性。
> **"收紧条件"不能靠加限定词的直觉，得靠逐条看命中、反推缺了哪一条。**
> 推论：**样本必须抄真实现场的形状**——C-32 首版就是被 `read_text(...).strip()` 的链式包装
> 与 `except: return ""` 挡住而零命中，是真实树首跑（模板 `update_helper` 竟然 `[ok]`）把漏报
> 打出来的；用想象中的形状写样本，会得到"全绿但漏掉真案"。
> **本纪律最硬的证据（判据作者自曝，lead 指定入档）**：判据第一版只扫"赋值右值的**子孙节点**"里
> 有没有 `read_text/read_bytes` 调用——而真实写法是 `detail = marker.read_text()`，**调用本身就是
> 右值的根节点**，根本不在"子孙"里 ⇒ **整个函数被漏掉，命中 0**。改法是"遍历右值**自身及其全部
> 子孙**"。**这条漏报不是靠再读一遍代码发现的，是样本当场打出来的**：换一个"想象出来的形状"
> （把调用包在链式里）会全绿，而真案隐身。⇒ **判据的每条限定词都是一个待验证的断言，
> 验证手段只有一个：拿已知正例去跑它。**

> **设计纪律 ⑥（2026-09-19 加，lead 依 tpl-keeper 的实证升级）：判据报"ok / 不适用 / 0 命中"时，
> 必须同时给出它的扫描面**（扫了哪些路径、候选站点几个、命中几个）。
> **"只报 0 命中"与"确实没有"在输出上不可区分**——那正是本族反复栽的形状。同族三条：
> ④"不认识 ≠ 违规"（管**输入形态**）、§4.1.18"判据存在 ≠ 被检查对象在范围内"（管**适用范围**）、
> 本条"没命中 ≠ 没问题"（管**覆盖**）——三条合起来才把"判据的输出"这一面补齐。
> **实证（C-30 首版，tpl-keeper 自犯）**：第一版只认**裸调用** `X = mkdtemp(...)`，于是 reme 那行
> `root = Path(tempfile.mkdtemp(...))` **被静默跳过**——**最该被检的那个文件被判成"本条不适用"**。
> 改按"赋值右侧含 `mkdtemp(`"+ 认包装函数调用点后，真实树立刻变成 **reme 1 / l-s2t 9 / dsh 6 / ocx 6**。
> **落地要求**：① 每条判据的 ok / 不适用分支必须打印扫描面（`--temp-leak` 已是范例：`%TEMP%` 路径 /
> 顶层目录数 / 前缀数 / 每腿命中数 / 并集）；② **样本测试要断言这个数字**，否则"扫了 0 个文件"
> 会伪装成绿；③ **判据首跑报"不适用 / 0 命中"时，当作可疑信号，而不是绿灯。**
> 一句话：**"我没命中"与"我没有检查"必须在输出上长得不一样。**

> **设计纪律 ⑦（2026-09-19 加，lead 裁定后立）：同一件事只允许一份判据——禁止自造第二套"加强版"。**
> 两份判据会**各自漂移、各自误报**，最后由"**没人知道该信哪个**"——这正是本族今晚在消灭的那种
> 漂移，只是换了个载体（从"文件副本""文档结论"换成了"判据本身"）。与同一族的
> "**索引里缺条目本身就是盲区**"（本文件 §4.1.18 与 checker 头部那句自我要求）并列。
> **实证（tpl-keeper，2026-09-19）**：复核员的 C-30 增强草案未到时，我**拒绝**自造一版"加强版前缀判据"
> ——理由不是省事，而是**同一条规则有两个实现，等于给契约换了两把尺**；后到的草案与既有实现必须**合并进
> 同一个检查**，而不是并存。
> **同族的第二个形态（lead 当日更正）**：把"**判据的机制**"与"**取证的方法**"混成一句话——C-30
> 从第一版起就是**读源码判定**（看赋值右侧是否含 `mkdtemp(`），而"枚举前缀再回查 `%TEMP%`"是
> **一次性的泄漏取证方法**；两者分属两个文档位置，**不该在同一句里以第二份判据的口吻出现**。
> **落地**：新增任何检查前先问"**这条是否已有实现/草案**"；有则**扩展那一个**（或等它），不并存第二份。
> 与 ④⑤⑥ 的分工：④ 管**输入形态**、⑥ 管**覆盖**、⑦ 管**唯一性**——三条一起才堵住"判据自己成为新的漂移源"。

> **设计纪律 ⑧（2026-09-19 加，ls2t-dev 提出、lead 认可填了空白）：承重前提（load-bearing premise）既不是 bug 也不是配置错，没法用"通过/失败"判——只能靠"输出它的取值与来源"来暴露。**
> 实例三条：① R2 的 「`probe_target` 在健康时不返回假阴性」（**没人验证过**，一旦不成立就是"杀掉用户正在用的隧道"）；② l-s2t 的 「配置里的 `model_dir` 是有效的」（已落成 GATE 3 **打印解析结果 + 来源**、陈旧时 `[WARN]`）；③ l-s2t 的 「`AsrEngine()` 会用解析出的 `model_dir`」（**实为导入期快照**，#46 —— 这条前提当时是**假的**）。
> **判据形态**：对每条承重前提，**要求把它打印出来（取值 + 来源）**，而不是断言它为真——**前提为假时，"断言为真"只会静默地绿；打印取值则当场露馅**。
> **与 ⑥ 的分工**：⑥ 管"读数必须自带分母（扫描面）"，⑧ 管"**被当成前提的那个值必须可见**"——两者同属主线：**把沉默的假设变成打印出来的事实**（同族还有：身份行、`[BROKEN]` 档、C-38 启动自证、R-EVID 的时点）。
> **落地要求**：承重前提的打印落在**门禁/自检**里（不是注释、不是文档），陈旧即 WARN、不可判也必须打印"判不了 + 为什么"。

> **设计纪律 ⑨（2026-09-19 加，lead 批准 C-33 修法后由 tpl-keeper 立）：判据的每一条豁免边界，都必须有一条自证腿，且必须带反向格。**
> 触发实证：C-33 的 `check_ping_tick` 会读 **docstring**，于是它自己那段"为什么要禁 `ping -n 2`"的散文被当成可执行节拍 ⇒ **越把原因说清楚越违规**；而自证集**当时恰好 5 条腿、独缺 docstring 那一条**，所以假红一路绿灯、直到真树上的散文踩响它。**假红的代价不只是烦**：它会让 `ALL PASS` 变成自相矛盾的读数（判据在自己的自证上全绿、在真树上因读散文而红），最终**教人习惯性忽略红**。
> **修法边界（写进条款，别只写实现）**：**"不碰字符串"这条豁免的适用对象是"会被执行的代码文本"**；**docstring / 注释 / 判据自己的诊断文案与正样本，是"关于代码的文本"**——同为 STRING token、语义不同。**这是豁免边界画错，不是实现 bug**，所以修在判据侧（挖 AST 裸字符串表达式 + 掩码保行号 + 排除仪器自身并**打印**排除项），**不是**去改写注释绕开它。
> **通用形态（与今天多条同族，lead 点名）**：**豁免范围一旦按"token 类型 / 文本特征"划，就会把"语义不同的同类型对象"一起放过、或一起误伤**——裸 `mkdtemp()` 按"prefix 有无"划、C-22 按"扩展名"划、本条按"STRING token"划，都出过同类问题。**机械判据只能按可判定的性质划界；凡按语法分类，都得配一条反向格证明它没有伤到该管的那一侧。**

> **设计纪律 ⑩（2026-09-19 加，复核员先提醒"它是**关掉覆盖**的开关"，lead 补成规则）：白名单 / 登记表的每一条，都必须写明「为什么它不算残留」与「什么情况下必须重验它」——两栏必填。**
> **为什么必须写成规则**：`TMP_DECLARED_PATHS` / `TMP_PREFIX_REGISTRY` 的条目是**唯一能让形态腿停止报警的东西**。⇒ **一条过期条目会静默地关掉一处覆盖，而且关掉之后没有任何症状**——这与"0 命中"和"没扫"不可区分是**同一个病**（⑥ 管"读数要带分母"，⑩ 管"**分母本身是被谁关掉的也要可见**"）。
> **实例**：`reme-helper-builddata` 进白名单的正当理由是"`scripts/build.bat:22` 明写的固定路径 + 删了会自动重建"；它的**重验触发条件**因此就是"**该行被改动时**"（路径变了 / 不再自动重建 / 加了清理 ⇒ 条目过期，而那处覆盖其实**已经被关掉且无人察觉**）。
> **机械形态**：① 条目是**结构体**而非裸值（`{why, reverify}` / `{prefix, why, reverify}`），**缺栏即红**（旧裸形态同样不合规）；② `--temp-leak` **打印生效条目的总数 + 每条的来源行与重验条件**，且**不只打印"现场命中"的那几条**（条目在不在盘上都照样生效）；③ 校验器自己有**反向格**——真表必须 0 问题，坏样本必须被抓住。

> **设计纪律 ⑪（2026-09-19 加，lead 定，来自 ls2t-dev 挖到的 `dev/null` 事故）：**当「修改路径」与「验证路径」共享同一层转换时，它们会一起错。**
> 改文件用 heredoc、自证用**同一个字面量** ⇒ 同一改写规则作用于两边 ⇒ **比对必然通过**（假绿）。
> ⇒ **验收要断言「一个改写不可能满足的性质」**（如「重定向位置不得有 `dev/null`」），**而不是断言「等于我以为的那串字符」**；引用具体字面量时，**一律用字节/十六进制**。
> 与「判据的枚举方式决定它的视界」、「0 命中必须打印扇描面」、「读数必须带尺子」同族——**同源的两层，永远不会互相发现对方的错**。

> **设计纪律 ⑫（2026-09-19 加，lead 定）：判据/程序所依赖的「外部名字」，其解析结果会随环境变化（PATH 顺序、同名工具）。
> **凡依赖外部名字的地方，要么钉死绝对路径，否则就是「把分支走向交给了环境」。**
> 实例：`where find` 在本机指向 Git 的 `usr/bin/find.exe`（排在 System32 前），而 GNU `find` 语义不同 ⇒ 命令**不报错**地走进错分支；同族：`dev/null`（shell 与 cmd 对同一串字符的解释不同）、`ping -n`（GNU 的 `-n` 是 numeric）。
> **与其它条目的关系**：与纪律 ⑪（修改路径与验证路径同源）**并列**——那条说「同源的两层一起错」，这条说「**启动环境会把你的分支换掉**」；两者都属「代码之外的因素暗中改变了执行路径」。

> **设计纪律 ⑬（2026-09-19 加，helpers-dev 提出、lead 采纳并一般化）：同形判据要锚在「语义的可观测产物」（日志/输出）上，不能锚在「实现形状」上。**
> **理由一句话**：**语义必须相同，形状可以允许不同。** 锚在形状上，就会把"语义达标但形状不同"判成未达标。
> **实例（他给的原话）**：reme 的退出结构**完全不同**（自带对话框、三元组返回），用函数名 `_decide_quit` 去抓，会把 reme **误标成未达标**；
> 改用语义相同的那行日志——**`quit confirm unavailable; quitting without stopping the service`**——才是稳定的锚点。
> **与本条同族**：纪律 ⑥（读数要带分母/扫描面）、⑪（同源两层一起错）、⑫（外部名字的解析随环境变化）——**都在讲"判据的立足点必须选在语义层，而不是实现层"**。
> **落地形态**：跨仓"同形"检查优先匹配**日志行/用户可见输出**；确需匹配代码时，必须同时接受多种等价形状（或按分支/性质判，见 C-41）。

### 5.1 立即可脚本化（无需运行程序）

| # | 检查 | 命令/断言 | 覆盖条款 |
|---|---|---|---|
| C-01 | 一级目录无 `.py` | `find <tool> -maxdepth 1 -name '*.py'` 为空 | B1-02 |
| C-02 | 无 `src/tests` | 目录不存在 | B1-01 |
| C-03 | 版本单源 | `grep -rn '^VERSION = ' src/ \| wc -l` == 1 | A1-03 |
| C-04 | B2 表版本 == 磁盘 VERSION | 解析 STANDARDS B2 表 + `src` | B2-01 |
| C-05 | README 切换行格式 | `line3` 正则 `^\*\*English\*\* \| \[简体中文\]` | A1-08/DOC-02 |
| C-06 | 两份 README 都进 release | build.bat 有两条 copy + 交付断言 | DOC-05 |
| C-07 | 生成物 ico 不在 git | `git ls-files '*.ico'` 为空 | A1-01/G2-01/G5-01 |
| C-08 | 互斥体名不含第二个反斜杠 | 正则 `Local\\[^\\]+\\` 命中即红 | SINGLE-01 |
| C-09 | 守卫失败方向 | 源码含 `not handle` 与 `return False` 同行/近邻即红 | SINGLE-02 |
| C-10 | `--smoke` 不绕过启动路径 | `--smoke` 分派点必须在 `acquire_single_instance` **之后** | SINGLE-04/D3-01 |
| C-11 | 运行检测匹配串与 exe 名一致 | 从 appconfig 取 `EXE_NAME`，与 build.bat 的 `findstr /c:` 比对 | SINGLE-05/D1-02 |
| C-12 | `MenuSignature` 被消费 | `grep -c 'MenuSignature' src/main.py` ≥ 1 | E2-09 |
| C-13 | `ui_q`/`ui_post` 存在（托盘类） | grep 非空 | E1-03/I-03 |
| C-14 | 日志轮转参数 | `grep 'maxBytes\|LOG_MAX_BYTES' src/log_kit.py` | D4-02 |
| C-15 | 托盘有"打开日志目录" | 词表/菜单 grep | D4-02 |
| C-16 | 环境变量名格式 | 存在 `<APP_ID 大写去连字符>_CONFIG` 与 `_DATA_DIR` 两个读取点 | B3-04/NAME-10 |
| C-17 | 测试不写用户真实数据区 | `grep -rn 'HKCU\|winreg' tests/` 须为 0，或有 DATA_DIR 重定向 | B4-04/D3-03 |
| C-18 | `sync_check` 在 build.bat 门禁中 | grep 非空 | B4-03 |
| C-19 | `TEMPLATE-FROM` 头齐全 | 凡与模板同名的文件都有头 | B4-01/B4-03 |
| C-20 | 中文残留（启用 T1 的工具） | 词表外的中文字面量 == 0 | A1-10/E4-02 |
| C-21 | 包 `import *` 不得复制可变状态 | 包用 `import *` 且子模块有 `global` 重绑 → 红 | §D6 |
| C-22 | bat/cmd 字节卫生（CRLF + 无 0x09 + 纯 ASCII） | 逐文件逐行报位置；构建产物与脚手架目录跳过 | B3/J 坑 |
| C-23 | 模块级状态不得被 `global` 重绑 | 状态须"容器就地改"或经访问器读 | §D6 |
| C-24 | 菜单读的容器状态须进签名 | 有菜单无签名机制 → 红 | E2-09/§D6 |
| **GATE-01** | **门禁步骤必须既存在又能被执行**：调用路径不在磁盘上即红；落在**顶层** `exit /b` / `goto :eof` 之后的调用＝死代码（`if (...)` 里的 `exit /b` 是条件式，**不算**死代码） | 覆盖 C-25；实例：reme `build.bat:201` 被 TAB 写坏，整行测试门禁**从未执行**且无症状 | B4-03/D1-05 |
| **GATE-02** | **`start` 前必须有存在性守卫**：`robocopy` 返回 0~7 表示"**没复制也没出错**"，只看"排除 ≥8"会把空 stage 当成功，随后 `start` 指向不存在的 exe → GUI 子系统的**模态框**，`DETACHED_PROCESS` 也压不住 | 覆盖 C-26；扫 `.bat` **与渲染 bat 的 `.py` 模板**（只扫 `.bat` 会一条都找不到）。见 §J「无人值守路径上弹模态对话框」 | D1-09/J 坑 |
| **GATE-03** | **模块采纳 = 拷贝 + 接线**：`sync_check` 的 `[ok]` 只证明"拷全了"，不证明"接上了"。模块 README 用 `<!-- MUST-WIRE: symbol -->` 声明"启动/退出时必须调用"的入口，判据在**工具代码**里找引用（排除被拷模块本体与 `__init__.py` 转发），找不到即红 | 覆盖 C-27；实例：dsh/ocx 拷全了 `update_helper` 但 `sweep_stale_update_dirs` / `pop_failed_update_note` **代码零引用**——README 承诺的两件事一件都没发生 | B4/D14 |
> **索引口径（2026-09-19）**：本表逐条列出**实现里存在的每个判据 ID**——`C-25` / `C-26` / `C-27` 的判据行就是上面的
> `GATE-01` / `GATE-02` / `GATE-03`（同一实现的两种叫法，不再重复建行）。**"索引里缺条目"本身就是盲区**：
> 一个跑得到、却在表里没有行的判据，等于没人知道它存在。核对办法：`conformance_check.py` 的 `CHECKS` +
> `TEMPLATE_CHECKS` 里的 ID 集合，与本表逐一对齐（本次实测 46 个 ID（C-46 计入），仅 C-25/26/27 走 GATE 别名）。

| C-28 | **`.md` 不得含 0x09 TAB**（**WARN**，只扫手写中文文档；`.py` 缩进、`.json` 转义是合法用途）。**模板仓也扫一遍、只报一次** | 逐文件报 TAB 行号。**留档**：C-28 的规则文本**自己那条 CHANGELOG 里就落进两个真 TAB**（想写两字符 `` `\t` ``，写进去的是真 TAB，且 `HEAD 188bbcc` 上已存在）——**"描述这个坑的文档，本身踩了这个坑"**。模板侧此前被 `main()` 的排除名单挡在扫描范围外（见 §4.1.18），现按"最省事形态"补扫：只让 C-28 额外扫模板仓，不给模板开整轮 | J 坑/§4.1.18 |
| C-29 | 交给模板件的 `log` 必须接受可变参数（print 形态） | 工具代码里 `log=<name>` 且该 `<name>` 的定义是单参无 `*args` → 红；`log=` 后不是工具内函数定义（如 reme 的**日志路径**常量）→ 判不了，不下判 | D4-04/§4.1.14 |
| C-30 | **mkdtemp 临时目录：前缀必须可静态归属，清理必须可验证**（禁 `ignore_errors` 吞掉）。**运行期取证另有两条腿（R-10）**；另有**已声明位置白名单 `TMP_DECLARED_PATHS`**（构建脚本明写的固定数据位，如 reme `scripts/build.bat:22` 的 `%TEMP%\reme-helper-builddata`，**不算泄漏**——判"是不是泄漏"必须靠位置 + 声明，形态腿自己分不出"该临时"与"该持久"） | **上半**：从源码**枚举** `mkdtemp` 的 `prefix` 实参（含包装函数**调用点**上的字面量，如 `scratch_dir("x-")`）；**第二路径：可折叠模块常量**（`APP_ID = "reme-helper"` + `prefix=f"{APP_ID}-update-"` ⇒ 折出 `reme-helper-update-`，**能折就不必登记**；只认模块级字面量、同名冲突或非字面量赋值一律判"折不出"，**宁缺勿猜**）；折不出的必须在模块级字面量 `TMP_PREFIX_REGISTRY = {"<相对路径>:<行号>": "等价前缀"}` 登记——**两态**：**未登记 = FAIL / 已登记 = OK**（lead 2026-09-19 把原来的"WARN"升级为两态：留 WARN 等于给"把字面量改成变量"留了降级逃逸口）；登记值非字面量 = 红；登记了却对不上站点（行号漂移）= WARN；**裸 `mkdtemp()`** 推得出系统默认前缀 `tmp` 但**很弱**（会撞无关目录）⇒ **WARN** 并交给腿 B。**真实树效果**：reme `main.py` 的 `f"{APP_ID}-update-"` 靠折叠转 `[ok]`，C-30 只剩它的 `rmtree(work, ignore_errors=True)`（#37）**下半**：赋值右侧含 `mkdtemp(` 的变量即"根目录"，被 `rmtree(..., ignore_errors=True)` 删 → 红；**扫全工具**（reme `src/main.py` 就是生产代码形态），删子目录 / 固定路径 / 有返回值的助手一律放行。**白名单/登记表条目两栏必填**（lead 2026-09-19，见设计纪律 ⑩）：`TMP_DECLARED_PATHS` 用 `{why, reverify}`，`TMP_PREFIX_REGISTRY` 用 `{prefix, why, reverify}`；**缺一栏就是合规性红**（旧的裸字符串形态也算不合规）。`--temp-leak` 必须打印**生效白名单条目数 + 每条的两栏**（不只打印“现场命中”的那几条）。**为什么**：白名单是**关掉覆盖**的开关，一条过期条目会静默地关掉一处覆盖且**没有任何症状**。 | D4-01/§J「导入即副作用 + 句柄未释放」/§D7 硬要求 8/§4.1.17 |
| C-33 | **禁拿 `ping` 当等待节拍**（**FAIL**）：它依赖网络配置——丢弃 loopback ICMP 的机器上 `ping -n 2` **实测 9.0s/拍**，名义 120s 变 ~18 分钟，而超时日志仍写"120s" | `.py`/`.bat`/`.cmd` 里出现 `ping` 且带 `-n`/`-w` 即**确证违规**；**注释/`rem` 行不算**（要抓的是会被执行的节拍），但渲染 bat 的 `.py` 模板里那句节拍是**字符串**、必须抓住。工具侧扫全仓，模板侧扫 `modules/**`、只跑一次。正确形态：`powershell -NoProfile -Command "Start-Sleep -Milliseconds 1000"`（DETACHED 无 console，不会弹窗）。样本 5 条（py 模板里的节拍 / bat 真节拍 / Start-Sleep / py 注释 / bat rem） | §4.1.20/J 坑 |
| C-32 | **禁「读证据 → 删证据 → 报告」的危险顺序**：不可逆动作不得排在**调用边界可能失败的语句**之前（**FAIL**） | **窄版判据**（复核员定稿、lead 裁定"不上通用版"），三条同时满足：**D** = `unlink/remove/rmtree/rmdir`（记接收者 `rcv`）；**A** = 函数内**任意一条**早于 D 的赋值，右值**含** `read_text/read_bytes` 且接收者与 `rcv` **AST 相同**（`ast.dump` 相等）；**R** = 晚于 D 的 `log` 调用，参数引用了 A 的名字。**为什么不禁通用版**：`log_kit.log()` 内部 `try/except` **本函数不抛**，宽版会把 `quit_watch_loop` 的 `unlink → log` 误报 5 处（假阳性比漏报更伤信任）。**为什么限定词要逐条回验**：见设计纪律 ⑤。**真实树**：模板 + **dsh + ocx** 的 `update_helper.pop_failed_update_note()` 三处 FAIL（源头在模板）；l-s2t / reme 已修（先 log 后删）→ ok | J 坑/§4.1.19 |
| C-31 | **模板派发件（`.py`/`.md`）必须全程 CRLF**（**WARN**；**模板正本专属**，`main()` 里只跑一次，不跟着工具重复 N 遍） | 对象 = `modules/**` 的 `.py`/`.md`，排除模板专属的 `build_release/`、`baseline/`（它们不进工具）。**C-22 只管 `.bat`/`.cmd`**，而正本的行尾会被原样拷进四个工具：LF-only 不报错、不触发任何现有判据（`py_compile` 绿、`sync_check` 两边同为 LF 也绿）——`log_kit.py` 被整文件重写那次是**读回字节**才发现的。首跑 **4/27 命中**（`autostart.py`/`icons.py`/`service_link/*`），工具侧副本同为 LF | J 坑/§4.1.16 |
| C-36 | **归一化算子必须行尾不敏感**（**FAIL**，模板通道）。**性质断言代替散文**：`sha256_text(LF) == sha256_text(CRLF) == sha256_text(CR)`，**且**不等于 naive `split("\n")` 控制值（否则「恒返回常数」的实现也能通过 ⇒ 无区分力）。扫描面打印算子名 + 样本 + 三变体哈希 + 控制值 | §4.1.24 |
| C-37 | **C-2 拒绝删除句柄**：模板 `paths.py` 必须提供 `hold_no_delete` / `hold_exe_delete_guard`，README 必须有对应 **MUST-WIRE**；**且性质实测**——持句柄时 `unlink` / `rmtree(父目录)` **必须失败**，释放后 `unlink` **必须成功**（判别控制）。自检另证「共享位写错（带上 `FILE_SHARE_DELETE`）必须被抓住」 | §4.1.29/D3.2 |
| C-38 | **启动自证：`startup` 行之后必须能看到解析后的数据根 / 配置文件路径**（**WARN**）。把"探针必须用带 `prefix=` 的 `mkdtemp`"这条**无法机械检查**的纪律，换成一条**可判的性质** | 判据（**2026-09-19 改形态**，原"文件前 N 行含数据根"按字面会假绿）：① 锚 = **第一个字符串实参以 `startup` 开头的 `log(`/`print(` 行**，数据根/配置路径必须出现在**其后 20 行内**——**不看文件前 N 行**（追加/轮转日志的**前 N 行是最老的**）；② **`config seeded:` / `config migrated:` 这类一次性行不得计入**；③ 文本先经 `_masked_code_text`（散文不算，§4.1.37）；④ **锚也要打印进 detail**（锚认错必须看得见）。**实测（2026-09-19，改形态后）＝ 四家全 WARN**：dsh 锚 `main.py:1763`、l-s2t 锚 `main.py:1030`（都是真启动行，窗口内无自证）；**reme 锚是 `main.py:7433 log(f"startup update check: …")`——一条周期性检查行，不是启动标记**（它真正的启动行是 `:2897 log(f"ReMe started … config={config}")`，但那里是局部变量 `config` 而非 `CONFIG_PATH`，读不出解析结果，**不算自证**）；**ocx 锚 0 处 ⇒ 不可判**（源码里根本没有启动标记）——**不可判也按 WARN 报，不报 ok**（"绿得不是地方，比红更坏"）。修复路径是**模板一处**（`paths.seed_config()` 加一行 ⇒ 四家重拷后同时具备）——**属下一波，不并入当前冻结**；格式样例见 §4.1.38。 | §4.1.17/§4.1.35/§4.1.37/§4.1.38 |
| C-39 | **默认参数不得取「会被重绑的模块级名字」/ 可变字面量（定义时快照）**（**FAIL**；模板侧扫 `modules/**`、工具侧扫 `src/**`）| 判据：① 默认值是**会被重绑的模块级名字**（模块级多次赋值 / `global` 重绑）⇒ 红；② 默认值是**可变字面量** ⇒ 红；③ 只赋值一次、不可变、无重绑 ⇒ **放行**。**实测（2026-09-19）**：模板 `modules/**` 19 件 + 四工具 `src/**` 16/18/16/16 件全 `[ok]`，良性默认参数计入 detail 分母。残余：“模块常量写进输出文案而函数另有实参”那种形态非默认参数，本条**不担保**，靠 `sync_check --selftest` E 组行为断言。 | §4.1.41/§4.1.20
| C-40 | **版本目录 ↔ 自启目标必须一致；孤儿版本目录必须登记「是否仍被引用」**（**FAIL**；读**磁盘 + 注册表**）| 强断言：自启目标必须存在，且其目录 == `release/<源码 VERSION>/` 或 `%LOCALAPPDATA%\<APP_ID>\app`（稳定安装位）。登记断言（WARN）：非当前 VERSION 的目录（孤儿版本）必须在 `ORPHAN_VERSIONS` 两栏登记。**实测（2026-09-19）**：**dsh = FAIL**（VERSION 1.8.1 vs Run → `release\dsh-helper-1.8.2\`，真反例）；ocx / reme 与源码 VERSION 一致 ⇒ ok；**l-s2t 的「无 Run 项」是假绿（§4.1.53）**——它的 Run 键是 `APP_NAME=LocalSpeak2Text`，判据当时按 `APP_ID` 单查 ⇒ 强断言从未执行；修后实测 `Run[LocalSpeak2Text]` 指向 `release/local-speak2text-1.4.0/`（与 VERSION 一致），且四家 `选键腿=path`。**自证 11 条**（6 + 选键口径 5 条；含两条正样本与外来项反向格）；**选键路径优先、不依赖键名**（§4.1.54）。 | §4.1.34/§4.1.42/纪律 ⑩
| C-41 | **退出确认的「链路不可用」分支必须固定为不停服务**（不得沿用已存勾选）**（**FAIL**）| 只判降级分支（`except` + `if x is None`）里喂给退出决策的语句；读持久化配置且涉及破坏性开关键 ⇒ 红。**原生框那一支不算**（用户确实被问到了）。**实测四家 + 模板 → 全 `[ok]`**（今天无违规，判据防的是`tray_kit` 统一之后长回去）。**自证 5 条腿**（含反向格）。 | §4.1.43
| C-42 | **重定向位置不得出现 `dev/null`**（**FAIL**）| 匹配 `>`（含 `2>`/`>>`）+ 可选空白 + `dev/null`；`.py` 掩掉注释/docstring（保留其余字符串），`.bat`/`.cmd` 丢 `rem`/`::` 行。Windows 上该位置出现它会让命令**根本不执行**。**实测四家 + 模板 → 全 `[ok]`**（扫描面 24/44/25/33 + 23 件）；**自证 5 条腿**。 | §4.1.44
| C-43 | **`if` 条件里不得用 `:~` 子串扩展**（**FAIL**）| `^\s*if\b` 行 + `:~` + 「`:~` 在动作关键字之前」⇒ 红；**嵌套 `if`（无 `:~`）与动作一侧的 `:~` 均判绿**。**实测四家 + 模板 → 全 `[ok]`**；**自证 4 条腿**（含逐字搬入的 `l-s2t/build.bat:84` 与 dsh/ocx `:87` 两个真实样本）。 | §4.1.45
| C-44 | **bat 里闭集命令必须用绝对路径**（不得裸名）**（**FAIL**）| 只看命令位置（行首 / `|`&`(`^` 之后的第一个 token，含 `for /f ('cmd')` 内联形态）；`rem`/`::` 不计。闭集 8 个：find/findstr/ping/tasklist/robocopy/where/reg/timeout。**实测命中 17 处**（模板 3 / dsh 2 / l-s2t 5 / ocx 2 / reme 5），**本机只有 `find` 与 `timeout` 真被抢先**（其余属潜在）；**自证 5 条腿**。 | §4.1.46
| C-45 | **工具侧副本（`src/modules/**` 的 .py/.md）必须全程 CRLF**（**WARN**）| **按字节判**（读 `bytes`，数 `
| C-34 | **§1 登记表版本列 == 文件头 `TEMPLATE-VER`**（**WARN**，模板通道）| 逐行 regex 取 §1 行的模块路径与版本列，与**文件头**比；不符 ⇒ WARN。**为何值得单列**：§1 的列头是“对外接口（稳定承诺）”，而这一列**此前没有任何判据打过它**（C-04 只查四工具 B2 表）——读表的人会按**错误的语义**理解接口。**实测修正前 3 行落后**（paths 1.1.3→1.1.4 / update_helper 1.4.3→1.4.4 / tray_kit 2.2.0→2.2.1）；修后 9 行全一致。**实测方向句**：**文件已自带的事实，不要再手抄一份**（同族第五次）。**自证 2 条腿**。 | §4.1.23/§4.1.18
| C-35 | **实例隔离两条腿：测试文件自钉 + `build.bat` 整体外套**（**WARN**）| **leg_a（文件级）**：凡 import src 的测试文件必須自钉数据根（判 import 与 env 赋值/`scratch_dir(` 的**行号先后**）；**leg_b（harness 级）**：`build.bat` 在测试段整体外套一次钉。<br>**两腿是并集不是合取**：**leg_b 在场 ⇒ 整体盖住**，单文件不必再自钉；leg_b 缺席 ⇒ 每个 import src 的测试文件都必須自钉。**判别力实测**：关掉 harness 腿 ⇒ **reme 11 个全红**；打开 ⇒ **四仓 0 FAIL / 0 WARN**（测得：dsh leg_a 6 + leg_b :120、l-s2t 12 + :125、ocx 7 + :119、reme 靠 leg_b）。<br>**覆盖面会扩——必须带时点**：**2026-09-19 当日只有 reme 有 leg_b**（`scripts/build.bat:22` pin）；**l-s2t 已批准补、dsh/ocx 已路由** ⇒ 落地后覆盖 **1 家 → 4 家**。**它同时把一条口径钉成断言**：“补丁是 no-op”**不该是会过期的陈述**——两腿同时在场才使 no-op 成为**可机械验证的性质**。**自证 3 条腿**。 | §4.1.35/F11-D12
` 与 `
`）。**为什么必须单独存在**：`sync_check` 按 `read_text()` 比内容、**行尾被归一化** ⇒ 只改行尾的重拷在它眼里**零效果、照旧 `[ok]`**——**“CRLF 波完成”可以与“零效果 + 全绿”同时成立**。扫描面排除非派发件（`src/*.py`/`tests/`/`tools/`/CHANGELOG）——那是各仓自有风格。**实测**：dsh/ocx/l-s2t 全 `[ok]`（21/21/18 件）；**reme = WARN**：**4/20** 非 CRLF（`src/modules/i18n/__init__.py`、`i18n.py`（205 处）、`i18n/README.md`、`service_link/NOT-WIRED.md`）。**自证 3 条腿**（LF 副本红 / CRLF 副本绿 / 无 modules 不适用）。 | §4.1.47/§4.1.36

| C-46 | **重建新鲜度：exe 必须比全部构建输入新**（**WARN**）；分母 = `src/**`（剔 `__pycache__`/`*.pyc`）∪ `build.bat`/`scripts/build.bat` 的 `--add-data` 源 | **分母补全**（任务 `#62`）：只扫 `src/**` 时，out-of-src datas（`*.ico` / `resources/` / `locales/` / `bin\plink.exe` / `doc/`）变了也会判"新鲜"。判据必须打印**扫描面（输入件数 + `--add-data` 源数）**与**取到最大值的那条路径**（只给布尔 = 无法复核的结论）；**空分母 ⇒ 不可判**（不报绿，§D8 第 6 条）。**实测（2026-09-19）**：dsh 29 件 / 4 源、ocx 28 / 4、l-s2t 28 / 3、reme 34 / 4；**dsh 的 max 输入 = `dsh-helper-taskbar.ico`（out-of-src）⇒ 补的那一项就是承重项**；l-s2t / reme 因并发编辑 `src/**` 如实 WARN。**自证 4 条腿**。⚠ **该 WARN 是预期读数**：本轮明确**不重建**（用户约束避免范围膨胀）⇒ **如实留着，不要为消它去构建**。 | §4.1.49 |

### 5.2 需要运行才能检查

| # | 检查 | 方法 | 覆盖条款 |
|---|---|---|---|
| R-01 | 单实例守卫真值 | 单测：建→再建须 False；失败注入须 True | SINGLE-07 |
| R-02 | 正常启动路径存活（非 `--smoke`） | 重定向数据区启动，N 秒内日志出现 `startup` 且进程存活 → 再 `--quit` | SINGLE-04/T12 |
| R-03 | 冻结自检有断言 | `--smoke` 退出码可判 + 人为破坏配置时非 0 | A1-06/D3-01 |
| R-04 | 两种布局路径解析 | 发布包放仓库内 / 临时目录各跑一次 | D2-01/D5-04 |
| R-05 | 交付物完整性 | 删 `_internal/base_library.zip` 后构建须非 0 | D1-08 |
| R-06 | 退出确认降级链 | 模拟富对话框失败，须落原生框且清理按持久化配置 | EXIT-06 |
| R-07 | i18n 覆盖 | `--lang-audit` missing == 0 | T5/E4-03 |
| R-08 | 主题可读性 | 正文 ≥8:1 / 次要 ≥4:1 / 禁用 ≥6:1 | E3-02 |
| R-09 | 测试隔离覆盖内核对象 | **在用户实例正在运行的前提下**跑单实例测试，断言仍应全绿（若红了，说明测试用了生产互斥体名） | SINGLE-08 |
| R-10 | `%TEMP%` 残留的**增量**断言（C-30 的运行期一半，**属于各工具 `build.bat`**）。**两条腿 + 必须打印扫描面**。<br>**登记沿革**：本条曾被我误编为 `R-07`，与 §5.2 既有的「R-07 i18n 覆盖」**撞号**（同日发现）——`R-07` 归 i18n，本条定为 `R-10` | 腿 A **生成器派生**（源码枚举前缀 + `TMP_PREFIX_REGISTRY`；裸 `mkdtemp()` → 弱前缀 `tmp`），腿 B **形态派生**（**任意深度存在名为 `log` 的目录**：不要求 `config.json`、不设深度上限、log 里 0 文件也算；**不看名字**——两次放宽都是先实测再改签名：先去掉「恰好一个子目录」，再去掉「必须有 config.json + 只扫两层」，后者是复核员的真实残留 `tmp.6FcrxXYxmM\d\local-speak2text`（3 层、只有 `log/`）。候选口径实测对照：V1「任意深度存在 `*.log` 文件」13 命中但多出 5 个他程序日志 ⇒ 否掉，采用 V2 的 8 命中）。**已声明位置**（`TMP_DECLARED_PATHS`）不计入并集与增量。跑测试前 `--temp-leak-save <基线>`，跑完 `--temp-leak-baseline <基线>`：**只对"新增"报红**（历史存量不计）。`--temp-leak` 单跑只是**取证**（列出命中与**扫描面**，永远 exit 0）——**"0 命中"必须与"没扫"可区分**（实测腿 A 得 0、腿 B 得 20）。**"清一遍"不是证据**：它只是一个时点 | D4-01/§4.1.15/§4.1.17 |
| R-11 | **冻结产物必须携带 Tk 运行时资产（"目录在 ≠ 文件在"）**。**适用面实测**：四家 release 目录**全部**带 `_tkinter.pyd`（dsh 1.8.1/1.8.2、l-s2t 1.4.0、ocx 1.2.1、reme 1.2.5），⇒ **对四家都成立**，可作家族通用门禁 | **第四条断言必须打在文件上**（不是目录）：`<release>\_internal\_tkinter.pyd` **且** `<release>\_internal\_tcl_data\init.tcl` 都**是文件**——本次炸的正是 `init.tcl` 这个**文件缺失**，而"目录存在"检查挡不住它。**放在 PyInstaller 之后、release 目录已生成之后**。可粘贴片段（ASCII-only）：<br>```bat
if not exist "%RELEASE_DIR%\_internal\_tkinter.pyd" goto :tk_missing
if not exist "%RELEASE_DIR%\_internal\_tcl_data\init.tcl" goto :tk_missing
echo [GATE] Tk runtime assets present (_tkinter.pyd + _tcl_data\init.tcl)
goto :tk_done
:tk_missing
echo [ERROR] Tk runtime asset missing under %RELEASE_DIR%\_internal\ (the DIRECTORY may exist while the FILE does not).
if not defined NOPAUSE pause
exit /b 1
:tk_done<br>**分工（三条互不替代）**：**C-22 管格式**（CRLF/无 TAB/纯 ASCII）、**R-11 管资产存在性**（文件在不在）、**两条都不管"bat 能不能被解析"**——那是 §4.1.33 的**探针纪律**（原样抽出、两方向各跑一次）。 | D1-08/§4.1.33 |


### 5.3 需要人工目视（**不由 AI 代跑**）

| # | 检查 | 原因 |
|---|---|---|
| M-01 | 托盘图标在溢出区可见（dev + frozen 各一次） | 日志 `NIM_ADD` 与进程存活都不算数，必须肉眼确认 |
| M-02 | 退出确认弹窗按钮布局/焦点/模态行为 | 需要真实鼠标键盘 |
| M-03 | 浮窗生长/滚动/不越屏 | 视觉判断 |
| M-04 | 发版前整轮人工功能回归（D16 闸） | 规范明确"自动化不可替代" |
| M-05 | **状态开关的测前快照 + 测后回读**（自启 / `ui_lang` / 服务托管 / 被点击改动的 config 键） | 2026-09-19 事故：dsh 的开机自启在目视验证窗口内被关、**无人发现**。清单见 §5.3.1，恢复口径见 `STANDARDS §D3.4` |

### 5.3.1 GUI / 目视验证的**状态快照清单**（2026-09-19 事故后补，配合 `STANDARDS §D3.4`）

**由来**：先前的协议只要求"记录 `ui_lang`、结束后还原"，**没把「开机自启开关」列为要快照的状态**——于是
dsh-helper 的自启在 `09:01:41`（它自己的日志有显式记录）被关闭后**无人发现**，直到 #42 排查才暴露。
**清单漏一项 = 那一项被改了也没人知道**；而且**事后单看状态值区分不了"按约定关的"与"误触关的"**（§D3.4 第 1 条）。

**每条三拍**：**测前读值（连时刻一起写进证据）→ 测后回读比对 → 不符则按 `§D3.4` 第 2 条恢复**
（拿不准原状时取"影响最小"侧 = **服务优先** = 这类开关默认取"**开**"），并在留痕里写明"原值=X / 原状未知，按 D3.4-2 取开"。

| # | 状态项 | 读值方式（测前、测后**用同一条命令**） | 归属 |
|---|---|---|---|
| S-01 | `ui_lang`（界面语言） | `<APP>_CONFIG` 指向的那份 `config.json` 里的键；或 `--status` | 四工具 |
| S-02 | **开机自启（HKCU `...\Run` 键）** | `reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v <APP_NAME>`——**本次事故就是漏了它** | 四工具（`autostart`） |
| S-03 | **服务/隧道托管开关**（如 ocx 的 `quit_stop_tunnels`） | `config.json` 键。实测：ocx 的隧道是 ocx-helper 的**直属子进程**（`PID 24664 opencodex-helper.exe` → `PID 15044 ParentProcessId=24664 ssh -N -R 10100:…`），用户真实配置 `quit_stop_tunnels = False` ⇒ **点错一下就是用户正在使用的隧道闪断** | ocx（reme 同类：服务托管） |
| S-04 | 其它**会被点击改动**的 `config.json` 键（主题、热键、模型、阈值、开机最小化…） | 测前整份备份 `config.json` 到 scratch，测后 `diff` 回读 | 四工具 |

**范围判据**：快照清单 = 本次**点击清单**的镜像——"**会点到**"的每个开关都必须在清单里有一行；两份对不上就是缺口。
**证据形态**：读值必须连**时刻**一起记（§4.1.13：不带时刻的读数不是证据）；只写"我看过了"不算快照。

### 5.4 首轮机械检查结果（2026-09-19，`conformance_check.py`）

| 检查 | reme | l-s2t | dsh | ocx | 说明 |
|---|---|---|---|---|---|
| C-01 一级无 .py | ✅ | ✅ | ✅ | ✅ | |
| C-02 无 src/tests | ✅ | ✅ | ✅ | ✅ | |
| C-03 版本单源 | ✅ | ✅ | ✅ | ✅ | |
| C-04 登记表版本一致 | ✅ | ✅**（修）** | ✅ | ✅ | |
| C-05 README 切换行加粗 | ❌ | ✅**（修）** | ✅ | ✅ | reme 两份仍未加粗 |
| C-06 两份 README 随包 | ⚠️ 只拷英文 | ✅ | ✅ | ✅ | |
| C-07 生成 ico 不入库 | ❌ | ✅ | ✅ | ✅ | reme 双 ico 被跟踪 |
| C-08 互斥体名合法 | ✅ | ✅**（修）** | ✅ | ✅ | 修前 ❌——正是 l-s2t 打不开的根因 |
| C-09 守卫失败放行 | ✅ | ✅**（修）** | ✅ | ✅ | 修前 ❌ |
| C-10 `--smoke` 覆盖守卫 | ❌ | ✅**（修）** | ❌ | ❌ | reme/dsh/ocx 仍绕过守卫 |
| C-11 运行检测匹配串 | ❌ | ✅ | ✅ | ✅ | reme 的 `reme-helper-` 命不中当前 exe |
| C-12 菜单签名重画接线 | ✅ | ❌ | ❌ | ❌ | 仅 reme 有内联等构 |
| C-13 队列封送骨架 | ✅ | ✅ | ⚠️ | ⚠️ | |
| C-14 日志轮转 1MB×3 | ✅ | ✅ | ✅ | ✅ | |
| C-15 托盘「打开日志目录」 | ⚠️ | ✅ | ✅ | ✅ | reme 缺 |
| C-16 `_CONFIG`+`_DATA_DIR` 双 env | ❌ 缺 DATA_DIR | ✅**（修）** | ❌ 两个都缺 | ❌ 两个都缺 | 模板 `paths` 也只有 `_DATA_DIR` 一半 |
| C-17 测试不碰用户注册表 | ✅ | ✅**（修）** | ✅ | ✅ | 修前 ❌：跑测试会改坏用户自启项 |
| C-18 门禁含 sync_check + 测试 | ✅ | ✅ | ❌ 无 tests/ | ❌ 无 tests/ | |
| C-19 模板件头部齐 | ⚠️ | ✅ | ✅ | ✅ | reme 的重形态 i18n 无头 |
| C-20 无词表外中文 | ✅ 重形态豁免 | ⚠️ 2 处 | ✅ 未启用 | ✅ 未启用 | l-s2t 剩余 2 处是 `smoke()` 诊断文案（写 smoke.log，非用户界面） |

**合计（2026-09-19 修复后）**：reme 6 FAIL / 4 WARN；**l-s2t 1 FAIL / 2 WARN**（修复前 5 FAIL / 1 WARN）；
dsh 3 FAIL / 1 WARN；ocx 3 FAIL / 1 WARN。

l-s2t 剩余 1 FAIL = C-12（菜单签名重画未接线），属**行为改动**，需 GUI 目视回归，已列为待办。
`✶` C-12 是唯一被有意推迟的一条：它改的是右键菜单的重画时机，**没有目视回归就不该动**——
这正是 §0.3 纪律 2「验证优先于修复」的边界：能自动化的先修，要眼睛看的排队。

> `✶` **C-05 / C-10 / C-12 / C-16 / C-18 是四工具同时或多数命中的家族级缺口**——
> 这五条改模板/改一次脚本就能全家族受益，优先级高于任何单工具的业务改动。

---

### 5.5 增量宣告模板（固定格式，**每次照抄**）

> **为什么要有模板**（lead 2026-09-19）：宣告里有一句解释**每次都会被需要**——只要宣告时不巧还有
> 别的在途改动，读者就会遇到同一个疑问。**要解释的东西，就该长在格式里**，不该每次手写。

**四行固定格式**（缺一不可）：

1. **本批 commit**（含上一批 commit，便于对方算增量）；
2. **`git diff --stat <上一批> <本批>`** 的逐路径数字；
3. **`git diff --name-only` 的路径清单，并明写"本批零派发件改动"**——只报 commit 号不足以让人
   判断**要不要重拷**（§4.1.39）。若**确有**派发件改动，则改为写出「哪些路径 + 新哈希 + 谁要重拷」，
   并走派发流程（改完 → 冻结 → 宣告 → 重拷）；
4. **家族读数**：`X FAIL / Y WARN / Z BROKEN`，并列出各条归谁。

**常驻说明（每份宣告都要带，不得省略）**：

> **关于 `dirty=yes`**：`dirty` 是**整体工作区**的状态，不是"被宣告的文件"的状态。
> 它必须与**逐路径自证**一起读——"被宣告的这几个文件自其冻结提交起一个字节都没动"。
> ⇒ **`dirty=yes` 本身不表示宣告失效**；它表示**当时工作区里还有别的在途改动**，
> 而那些改动**不在本批的路径清单里**（第 3 行已经把清单给出来了）。
> **判据**：拿第 3 行的路径清单去核；清单里每个文件干净 ⇒ 本批仍然成立。

> **两句制（ls2t-dev 提的精确区分，2026-09-19 入档）：内容标识 与 绑定断言 分开写。**
> **内容标识**（如 `f81a5922e2d8`）**没有错**：它精确标识了当时那份内容，**作为名字它永不过期**；
> **绑定断言**（「**= 磁盘现在这一份**」）是**时点性的**，改动一落它就假。
> ⇒ 宣告写成两句：「相较 `<旧 rev>`，只动了 `X` 一个文件，**新值 N**」（**标识**）＋「**以 N 为准**（此后未再变动）」（**断言**）。
> ⇒ 好处：**「旧值作废」有了明确对象——作废的是断言，不是标识**；也免得后人以为「哈希作废」意味着那个哈希**算错了**。

**身份行（一并贴）**：`# conformance_check <VER>  sha256:<raw12>  norm:<norm12>  head:<sha>  at:<ISO>`。
两种哈希口径都要的原因见下（§5.6），`head` + `at` 回答"这份输出属于哪个提交、什么时候"。

### 5.6 身份行为什么要印两种哈希（实测判别实例）

同一条内容在家族里有两把尺子：**`.py` 比对用 `norm`**（剔 `# TEMPLATE-*` 行）、**`.md` 用逐字节**。
只印一种，就会有人拿另一种去对，然后得出"对不上"的假结论。

**实测的判别实例**（可复算，2026-09-19）：在本文件末尾**只追加一行 `# TEMPLATE-TEST: …`**
⇒ `raw 8213f62be793 → f6b5d7711a26`（**变**），`norm 0179f3bfda82 → 0179f3bfda82`（**不变**）。
⇒ **只印 norm 看不见"抬头/版本动了"；只印 sha256 又与 `.py` 的比对口径对不齐。**

⚠️ 另有一条需更正的说法：lead 转述的"`sync_check` 1.8.2→1.8.3 时 sha256 变而 norm 没变"**实测不成立**
（那两个修订两侧都变了：raw `230c5c4deb5f→7b104dc70994`、norm `0d2335462db4→1eccbbf2b908`；且两件工具
**全部相邻修订里都没有"一个变一个不变"**的实例）。**机制为真，那个具体例子为假**——故此处只收实测的合成对照。

## 6. 首版审计结论摘要（2026-09-19）

### 6.1 按工具统计（⚠️/❌ 计数，仅统计适用条款）

| 工具 | ✅ | ⚠️ | ❌ | 最严重的三项 |
|---|---|---|---|---|
| reme-helper | 48 | 24 | 4 | 无稳定安装位（G4.1-01/02）；测试共享用户数据区（B4-04）；双 ico 入库（G2-01） |
| local-speak2text | 41 | 26 | 13 | **单实例守卫导致完全无法启动（T12）**；测试改写用户真实注册表（B4-04/D3-03）；测试非门禁（D3-02） |
| dsh-helper | 51 | 19 | 10 | 无 tests/（B1-01/D3-02）；无稳定安装位 + 无自启自愈（G4.1-01/02/03/05）；无 i18n 且文案全内联（T1/A1-10） |
| opencodex-helper | 44 | 22 | 15 | 无稳定安装位 + 注册表死链实证（G4.1-02）；无 tests/ 且 `import main` 有落盘副作用（B4-04/I-04）；commit 前未验证（B3-03） |

### 6.2 家族共性缺口（四工具同时命中的）

| 缺口 | 命中 | 说明 |
|---|---|---|
| **实例隔离**：`_CONFIG` + `_DATA_DIR` 两个 env 没一个工具齐全 | 4/4 | 模板已实现 `_DATA_DIR`，四工具都没同步——**这是"模板领先使用者"的唯一一条，也是 4.1.6 蓝本盲区的直接证据** |
| 稳定安装位 + 自启自愈 | 3/4（l-s2t 已做） | reme/dsh/ocx 升级必留自启死链 |
| `tests/` 未进门禁 / 无 tests/ | 3/4（reme 最好也缺 DATA_DIR） | 测试是"死代码"，且 l-s2t 的测试还会改写用户真实注册表 |
| README 未注明"未触发能力及原因" | 4/4 | I-10 自查项形同虚设 |
| 缺 `release.bat` 或 release.bat 不可用 | 3/4 | dsh/ocx 缺件，l-s2t 路径写错 |
| `--smoke` 绕过正常启动路径 | 4/4 | 规范只在 J 坑里记了教训，未升级为条款（本次已升级） |

### 6.3 下一步优先级建议

1. **P0**：l-s2t 单实例修复（用户当前痛点）；
2. **P0**：把 §5.1 的 C-01..C-20 落成 `conformance_check.py` 并接入四工具 build.bat；
3. **P1**：四工具同步 `paths.py` 1.1.2（补 `_DATA_DIR` / `_CONFIG`）+ 修 l-s2t 的测试隔离；
4. **P1**：dsh/ocx 补 `tests/` 骨架与 `release.bat`；
5. **P2**：文档类（README 切换行加粗、未触发项注明、脱敏）；
6. **P2**：dsh/ocx 接入 i18n（触发条件早已满足）。

---

## 7. GUI 目视回归结果（2026-09-19，frozen 态真 exe）

只读的自动化检查覆盖不到"眼睛看得见"的东西。以下用 computer use 实操 `release\local-speak2text-1.4.1\` 的真 exe 得到：

| 项 | 结果 | 证据 |
|---|---|---|
| M-01 托盘图标可见 | ✅ | 展开任务栏溢出区，悬停 tooltip 显示 `LocalSpeak2Text`（不是看日志推断的） |
| E2-01 八段式菜单 | ✅ | 实测菜单：信息(版本+状态) → 更新(检查/立即) → 默认入口(使用指引…) → 业务(自动增益/选择模型目录…/检测模型性能/复制添加模型方式) → 打开(打开日志目录) → 偏好(开机自启/Language) → 退出(恒最后)；`default=True` 唯一 |
| E2-02/03/04/05 命名五规则 | ✅ | 只读信息行仅第一段；开关用 ☑ 状态短语；"…"只出现在开窗项 |
| G4.1-04 退出确认形态 | ✅ | 红底「退出」在左、「取消」在右且带焦点框、模态、关窗=取消 |
| EXIT-06 取消不退出 | ✅ | 点「取消」后进程存活、日志无 `exit` |
| E1-04 退出路径 | ✅ | 确认后进程退出，日志出现 `exit`，无 `crash.log` |
| T12 真实双开 | ✅ | 第二实例被拒 + 弹窗「LocalSpeak2Text 已在运行：请使用托盘里的那个实例。」+ 新日志行 `another instance holds Local\local-speak2text-single-instance; this launch cancels` |
| **EXIT-02 Esc = 取消** | ❌ | 按 Esc 弹窗**不关**。代码坐实：`main.py:918-947` 有 `no.focus_set()`/`protocol(WM_DELETE_WINDOW)`/`grab_set()`，**独缺 `top.bind("<Escape>", ...)`**；模板 `tray_kit.confirm_quit_dialog` 有这一行 |
| E2-09 菜单重画时机 | ⚠️ 偶发 | 首次打开菜单时信息行仍显示「正在加载模型…」（模型已就绪 5 分钟）；再次打开显示正确的「就绪 [sense_voice]」。**观察到一次、未复现**，按纪律记为"疑似重画时机竞态"而非确定缺陷 |

`✶ Insight ─────────────────────────────────────`
**EXIT-02 这一条只有目视能抓住**：代码里 `no.focus_set()`、`WM_DELETE_WINDOW`、`grab_set()` 一应俱全，静态审查看起来"完全符合"，但"按 Esc 能不能关"这件事**没有任何自动化断言**——除非有人真的按一下。这正是 §5.3 把四条列为"必须人工目视、不由 AI 代跑"的原因。
`─────────────────────────────────────────────────`

---

## 8. local-speak2text 首轮整改记录（2026-09-19）

对照表建成后，**立刻拿它审 l-s2t 作为"颗粒度是否够细"的实测**——这就是本表存在的意义。

| 条款 | 问题（修前） | 处置 | 验证方式 |
|---|---|---|---|
| SINGLE-01 | `MUTEX_NAME = r"Local\%s\SingleInstance"` 含第二个反斜杠 → `CreateMutexW` 恒失败 err=3 | 改为模板同款 `Local\<APP_ID>-single-instance` | `tests/test_single_instance.py` 断言"内核接受新名 + 旧名仍失败" |
| SINGLE-02 | `if not handle … return False` —— 守卫自身失败被当成"已有实例" | 改为失败放行；仅 `ERROR_ALREADY_EXISTS` 才拒绝 | 同测试注入 `WinDLL` 抛异常，断言放行 |
| SINGLE-04 | `--smoke` 在 `main()` 之前 `sys.exit(smoke())`，完全绕过守卫 | `smoke()` 增 `mutex_name_is_valid()` 探测（不占锁） | build.bat 冻结冒烟即验证 |
| SINGLE-07 | 守卫零断言，坏了 3 个月无人知 | 新增 `tests/test_single_instance.py`（8 断言） | 已进门禁 GATE 2b |
| D3-01 | 无任何测试覆盖真实 `main()` 启动路径 | 新增 `tests/test_startup_path.py`：替身换掉 Tk/托盘/模型/钩子，跑真 `main()` | 已进门禁 GATE 2b |
| B3-04 / B4-04 | 全仓无 `<APP>_DATA_DIR`，测试/构建与常驻实例共享 config/log | `paths.py` 加 `LOCALSPEAK2TEXT_DATA_DIR`；build.bat 冒烟同时钉 `_CONFIG` 与 `_DATA_DIR` | 实测冒烟前后用户日志 mtime 不变 |
| D3-03 | `test_autostart_migrate.py` 改写用户真实 HKCU Run 且不还原 | 备份原值 + `finally` 还原 + 还原后断言 | 实测跑完注册表回到原值 |
| A1-10 / E4-02 | 3 处用户可见中文散落在调用点 | 2 处进词表（`dup_running` / `notify_lang_switched`，74→76 键）；`i18n.init` 提前到守卫之前 | 冒烟 + `--lang-audit`（待补）|
| A1-08 | 两份 README 语言切换行未加粗 | 按精确格式修正（保 CRLF） | `conformance_check.py` C-05 |
| B2-01 | 登记表版本 1.4.0 / 磁盘 1.4.1 | 升版 `1.4.0 → 1.4.1`（+0.0.1，bug 修复档）+ CHANGELOG + 登记表同步 | 构建 [DONE] |

**实机验证（frozen 态，隔离数据区）**：
```
2026-09-19 12:07:44 INFO startup LocalSpeak2Text v1.4.1 (pid 1872)
2026-09-19 12:07:46 INFO model ready: sense_voice      ← 进程存活 = 守卫放行
```
修前同一位置的表现是：弹"已在运行"→ 进程立即退出，**工具完全打不开**。

**未做（有意推迟，见 §5.4）**：C-12 菜单签名重画（行为改动，需 GUI）；T4/T5 自检命令；
T7 guide；E2-06 `--quit`；其余 5 个测试套件入门禁（现只接了 2 个 → D3-02 仍为 ⚠️）。

---

## 9. 通用经验的内化来源（2026-09-20）

> **引用**：本表基线形态**按 `STANDARDS §L L6①` 的阶梯**（**定义唯一、提及从属**，此处**不重述**其内容）。
> **标识**：`§9.1` 的 `P` 编号是 **`proposals.md` 的提案行标识**（每行**自带内容标签**）；**跨文件引用须写作 `proposals.md P<n>`**（**裸写 `P4` 不可解析**）；实质锚为**四家工具的 `文件:行号`**。
> **✅ 定稿（2026-09-20）**：基线 `HEAD` = 本行所在提交（`git rev-parse HEAD`；`git status --porcelain` 为空）；所依据 `STANDARDS.md` 版本 = **与本行同一提交的 `STANDARDS.md`**（现场 `git rev-parse HEAD:STANDARDS.md` **派生**，**不在正文抄写**）；`CONFORMANCE.md` blob 见 `git rev-parse HEAD:CONFORMANCE.md`（**自指哈希无法内嵌**，故给指针）。（按"**pin 用 blob、不用时效词**"的口径书写。）19:56 之后 STANDARDS 的两处增量（`§D8 附则 附 1 ④`、`§L L5②`）**已并入 §9.3 反查表**。
> 本轮并入：**Δ1** → `STANDARDS §D3.5`（3 家）、**过程稿 §1.6 的 2 条** → `STANDARDS §D9`（2 家）、**Δ2** → `CONFORMANCE §4.1.65`（[单家强证据]，只登记）、**§L（L1–L9）** → `STANDARDS §L`。
> **自扫词表**（逐句对当前事实，非仅统计）：`尚未|未改|未提交|未建|待落`（**本行只是词表列示，非状态断言**）⇒ **排除本行**后逐句核：本表与过程稿均 **0 处**（命令与输出见 §9.5）。

> **用途**：让"删除四个工具的开发文档"成为**有据可查**的动作 —— 每条通用经验在此指得出**落点**与**四家源锚点**。
> **判据**：任何一条源信息，要么有落点、要么有丢弃理由；**两者皆无 = 删了就真丢了**（自检见 §9.5）。
> 过程稿与逐条细节留 `_verify-scratch/internalize/retire-list.md`（临时取证区，会被清理）；**本表是正本**。
> 归属口径（本轮立）：**锚点必须属于被引的那一方**，引用方自查不算确认；"X 报告里已提过 Y"必须 grep 到锚点才可写。

### 9.1 提案 → 落点 + 四家源锚点（提案稿 21 条 + 补录 3 条；裁决依据见过程稿）

| 提案 | 决定 | 落点 | 四家源锚点 |
|---|---|---|---|
| P1 状态经访问器 / 禁 `import *` | 已存在 | STANDARDS §D6 | dsh `CHANGELOG.md:237-246`；ocx `CHANGELOG §1.2.2`／`update_helper/README.md:33-42`；reme `UCR §8.1`；l-s2t `CHANGELOG §1.4.1` |
| P2 清理不许假成功（删后回读） | 已存在 | §D3 + §J | dsh `CHANGELOG.md:105-114`；ocx `CHANGELOG §1.2.2`(R2)／`tests/README.md:44-47`；reme `CHANGELOG §1.2.6`「C-30」；l-s2t `CHANGELOG §1.4.1` |
| P3 无 console 下 `start` 缺失目标弹模态框 | 已存在 | §J + §5.3.1 | dsh `CHANGELOG.md:102-120`；ocx `CHANGELOG §1.2.2`(R1+R4)；reme `CHANGELOG §1.2.6`「自更新链加固」；l-s2t `CHANGELOG §1.4.1` |
| P4 退出降级链三态 | **合并** | **STANDARDS §K1**（收编条：G4.2 条款 5 + §4.1.58/59 + C-41/C-49~51） | dsh `CHANGELOG.md:41-53`；ocx `CHANGELOG §1.2.2`；reme `CHANGELOG §1.2.6`／`tests/test_quit_failopen.py` |
| P5 探测失败不得触发破坏性动作 | 已存在 | §G4.2 条款 4–5 + C-49/C-51 + §4.1.58 | ocx `CHANGELOG §1.2.2`(probe_target)；reme `CHANGELOG §1.2.6`首条(C-51)；l-s2t `CHANGELOG §1.4.1`「#45 同族审计」 |
| P6 守则运行时 fail-open + 构建期 fail-closed | 已存在 | §D3.2 | dsh `tray_kit/README.md:18-19`；ocx `CHANGELOG §1.2.2`(D3.1/C-10)；reme `CHANGELOG §1.2.6`「tray_kit 追平 2.2.0」 |
| P7 实例隔离早于首次 import | 已存在 | §D3 + F11/D12 | dsh `tests/README.md:38-41`；ocx `tests/README.md:39-42`；l-s2t `CHANGELOG §1.4.1` |
| P8 无 console 管道阻塞 / `ping` 非时钟 | 已存在 | §J + C-33 | dsh `update_helper/README.md:52-54`、`:57-62`；reme `CHANGELOG §v1.0.9`/`§1.2.6`；l-s2t `CHANGELOG §1.4.1` |
| P9 robocopy 空源落在"成功"码区间 | 已存在 | **§5.1 GATE-02** + §J | dsh `update_helper/README.md:70-77`；reme `CHANGELOG §1.2.6`；l-s2t `CHANGELOG §1.4.1` |
| P10 robocopy 只比 size+mtime | 已存在 | §4.1.62 | reme `CHANGELOG §1.2.6`（三对照表）；l-s2t `CHANGELOG §1.4.2` |
| P11 断言须带对照/负控 | **判据在条文缺** | **STANDARDS §K2** | dsh `tests/README.md:25-28`、`:31-36`；ocx `tests/README.md:24-28`、`:31-36` |
| P12 i18n 缺键返回键名 + 默认文案泄漏 | 已存在 | §E4 + C-20/C-52 | dsh `CHANGELOG.md:14-28`、`:29-33`；ocx `CHANGELOG §1.2.2`(E4-02) |
| P13 桩须照抄生产签名 | **合并** | **§K2**（并入 P11） | dsh `CHANGELOG.md:132-138`；ocx `tests/README.md:14-22` |
| P14 菜单签名须对照 `build_menu()` | 已存在 | §E2 第二条（"状态签名比较"） | dsh `CHANGELOG.md:69-80`；ocx `CHANGELOG §1.2.2`(E2-09) |
| P15 绝对路径 / bat CRLF / 门禁可达 | 已存在 | C-22/C-44 + §4.1.62/63 | reme `CHANGELOG §1.2.6`(PATH)；l-s2t `CHANGELOG §1.4.1`、`§1.4.3` |
| P16 判据扫描面须声明并论证 | 已存在 | §D8 + §4.1.55 | l-s2t `CHANGELOG §1.4.1`「扫描面…」；ocx 判据自检（扫描面非空） |
| P17 仪器先自证 / 锚取 commit·blob | 已存在 | §D7 + §D8 | l-s2t `CHANGELOG §1.4.1`「首次运行纪律」「锚点教训」「哈希必须带配方」；HANDOFF R1 §4.5/§6 |
| P18 改名保留 / 自愈须"当前性" | 已存在 | D11 + §4.1.51 | dsh、ocx `autostart/README.md:18`；l-s2t `CHANGELOG §1.4.1`「重建纪律」 |
| P19 拷贝到位 ≠ 接线（MUST-WIRE） | **判据在条文缺** | **STANDARDS §K3** | dsh、ocx `update_helper/README.md:88-93`；l-s2t `CHANGELOG §1.4.1`「重拷验收口径升级」 |
| P20 改模板优先 / 吸收义务 | **判据在条文缺** | **STANDARDS §K4** | dsh `CHANGELOG.md:51-68`；HANDOFF TL 三/D3/D13。**§K4 = 单家强证据（dsh + HANDOFF），不计入门槛** |
| P21 打包断言"冒烟看不见的东西" | **合并** | **§K2**（并入 P11）；3 家（dsh `build.bat:276-288`／ocx `build.bat:275-287`／reme `scripts/build.bat:437-444`） | reme `CHANGELOG §1.2.6` B 项 |

> **计数（逐条）**：已存在 **15**（P1/2/3/5/6/7/8/9/10/12/14/15/16/17/18）、合并 **3**（P4/P13/P21）、判据在条文缺 **3**（P11/P19/P20）⇒ **真正新写条文 = §K 的 K1–K4**。**§K 已提交 `5fee7a6`**；其"是否与 §D/§E/§G 重复"的核重归终检重跑（见 §9.5）。
> 补录（提案后按裁决指示）：**P22**→§4.1.62、**P23**→§4.1.63、**P24**→§4.1.64（均 ≥2 家）。

### 9.2 每份源文档 → 内化 / 丢弃

| 处置 | 内容 | 理由 |
|---|---|---|
| **内化** | 四份报告 §1 通用候选（经 P1–P24 合并） | 已在 §9.1 指得出落点 |
| **丢弃·本工具特有** | dsh 10 / ocx 8 / reme 9 / l-s2t 9 条（报告 §2） | 绑定各工具业务（dsh web／opencodex 隧道／ReMe 上游／ASR 识别），第五个工具无对应物 ⇒ **随文档消失可接受** |
| **丢弃·冗余** | 四份 §3 共 40 段 | 同一事实已有更规范的正本（模板 README/CHANGELOG 或本表），删除不丢信息 |
| **丢弃·因 ≤25 上限被裁** | 36 条（报告 §4）；Δ 增补扫描结论：收 **2 条 Δ**（**已落**：Δ1→`§D3.5`、Δ2→`§4.1.65`；吸收 3 源条目）、**33 条逐条给理由**（27 条"模板已有"／5 条"已被 P1/P2/P3/P7/P12 覆盖"／1 条"单家且原文自判为可用性改进"） | 逐条理由见过程稿 §2，无一条以"未收"结案 |
| **不采信** | 下层自曝"仅来自工作记忆、不可验证"的自述 | 按 `[待核实]`／A4/D5 处理，不作落点依据 |

> **§4 取数（前缀匹配，非精确串）**：`^## 4\.` 命中 **4/4**；精确串 `^## 4\. 因 ≤25 条上限被裁掉的条目` 对 l-s2t 命中 **0**（其标题少一"条"字）⇒ 必须**前缀取数**，否则静默漏掉 l-s2t 全部。命中标题原文：dsh `## 4. 因 ≤25 条上限被裁掉的条目（清单，不占 §1 配额）`；ocx / reme `## 4. 因 ≤25 条上限被裁掉的条目`；l-s2t `## 4. 因 ≤25 上限被裁掉的条目（清单，不计入 §1 配额）`。

> **粒度声明（2026-09-20）**：本表为**候选池级**，**池外项按类别豁免** —— dsh §4 自述「**非穷举**，其余在初筛即判为业务耦合或纯通用常识、从未进入候选池」。**不得读成"全量逐条"**（那是超出实际证据的主张）。

> **§9.2a 不收但留痕（检测启发式）**（不另立条文，保留为"嗅觉"）
> - **"降级比正常更完整"本身就是检出信号**：ocx 案例里 native fallback 用了翻译文案、而**正常路径没翻译** ⇒ 说明**本地化的覆盖顺序反了**（根因同 P12，故不新增）。
> - `import *` 的第二个实例 **`LANG` 成静态副本**（切语言后通知英文、菜单中文）⇒ 根因同 P1/§D6，不重复立条。

### 9.3 反查：模板新增/改动 → 来源锚点（防"凭空出现的规范"）

| 模板位置 | 源锚点 |
|---|---|
| STANDARDS **§K1** | P4 四家锚点（§9.1）+ G4.2 条款 5 + §4.1.58/59 + C-41/C-49~51 |
| STANDARDS **§K2** | P11/P13/P21（dsh/ocx `tests/README.md`；reme `CHANGELOG §1.2.6`；dsh/ocx/reme `build.bat`） |
| STANDARDS **§K3** | P19（dsh/ocx `update_helper/README.md:88-93`；l-s2t `CHANGELOG §1.4.1`） |
| STANDARDS **§K4** | P20（dsh `CHANGELOG.md:51-68`；HANDOFF TL 三/D3/D13）（**单家强证据，不计入门槛**） |
| STANDARDS **§A2 T1**（口径变更） | 用户 2026-09-20 裁定"双语是默认要求"；C-52 |
| CONFORMANCE **§4.1.58 ~ §4.1.64** | 用户报告 + **裁决时的四仓差集实测**（**§4.1.64 的锚点 = 四仓差集实测，非 l-s2t 报告**） |
| CONFORMANCE **§9**（本节） | 提案稿 + 裁决记录（均为过程稿） |
| STANDARDS **§L**（L1–L9） | **第三个团队的协作过程本身**（这一轮内化作业），**非**四工具的开发经验 ⇒ 锚点是**事件性锚点**（事件 + 时刻 + 当事人），**不指向过程文件**（见 §L 抬头） |
| STANDARDS **§D3.5**（Δ1：等待/轮询） | dsh `CHANGELOG.md:86-101`；ocx `CHANGELOG §1.2.2`／`tests/README.md:55-57`／`tests/test_ui_marshal.py`；reme `CHANGELOG §1.2.6` |
| STANDARDS **§D9**（跨编码/stdio 边界） | l-s2t `CHANGELOG.md:43`、`:1478-1482`；reme `CHANGELOG.md:593`、`:603`、`:611` |
| CONFORMANCE **§4.1.65**（时新性的参照系） | l-s2t `CHANGELOG §1.4.1`「不能用 HEAD 的时钟」「必须排除 `__pycache__`」 |
| STANDARDS **§D8 附则 附 1 ④**（行尾判据扩三维 + "扫描面缺口族"问法） | 终检自测复现行内裸 CR ＋ 写入方提交缺陷 ＋ 整文件重写归一化（落笔方自查） |
| STANDARDS **§L L1 边界**（任务定义里的时间/前置条件也是权限边界） | 只读旁观者 观-6（名册外派发 #16 的时序事故） |
| STANDARDS **§L L3 实例五 第二信号**（"不可能值"报警 ＋ 整文件重写吃掉裸 CR） | 过程管控方两次自曝仪器失真 ＋ 落笔方自报 |
| STANDARDS **§L L5①-补 取证注**（0 命中不得单因归因） | 只读旁观者 判-6 |
| STANDARDS **§L L5② 分界＋机制化**（传播只作用于当前值陈述；计数由脚本产生） | 只读旁观者 判-4 ＋ 过程管控方自报 |
| STANDARDS **§L L6① 示例＋来源等级** | 只读旁观者 判-15（同一形态三次，缺示例）＋ 过程管控方自曝 |
| STANDARDS **§L L9 款③④**（核验期静止 / 三步协议 / 作废≠有错） | 只读旁观者 判-7/判-9/判-12 ＋ 过程管控方（不收敛观察） |
| STANDARDS **§D8 附则 附 1 ④-补**（通道声明 / 三形态失真 / 非白名单控制字符扫描并锚） | 过程管控方 5 例失真 ＋ 只读旁观者 判-17 ＋ 落笔方自报（heredoc 折叠） |
| STANDARDS **§L L1 边界之二**（在途作业清单 = 冻结声明第四要素） | 只读旁观者 判-18（名册外派发在冻结期启动的实例） |
| STANDARDS **§L L3 实例五 第三形态**（量级正常的假值 ＋ 写含反斜杠内容用文件方式） | 只读旁观者追补 22 ＋ 落笔方自报 |
| STANDARDS **§L L5①-补**（可 grep 性须实测标注，不按形态推断） | 过程管控方（TSV 逐行实测，发现两处不可取） |
| STANDARDS **§L L5② 分类计数按值域** | 只读旁观者 观-7 |
| STANDARDS **§L L6① 款③④**（反例声明 / 消息也要带基线） | 过程管控方自曝（公式反例）＋ 只读旁观者（消息交叉 4 次） |
| STANDARDS **§L L9 款⑤–⑧**（冻结四要素 / 基线传播分类 / 结果优于预期须说明 / 引用须带载体） | 只读旁观者 判-9 与判-18 ＋ 过程管控方 ＋ 落笔方自检 |
| STANDARDS **§K1 收编源指针** ＋ **§D8 附 1 ④ 输入集须随结论发布** ＋ **§L L5①-补 两端取词** | 过程管控方（观-8 第三类定性：收编源缺指针）＋ 只读旁观者第 7 项候选（计数类结论须携带输入集） |
| STANDARDS **§L L1 默认值按后果分类** ＋ **§D8 附 1 ④ 选型通则与"反例的必要性"** ＋ **§L L9 款⑨（状态看对象）** | 只读旁观者（判-18 过宽条款自曝）＋ 过程管控方（选型通则 / 正例集不能区分两式）＋ 过程管控方（状态判据精化） |
| `STANDARDS §D8 附则 附 1 ④`（行尾口径：**同文件内不得混用**；跨文件允许不同） | 本轮裁定 15a（口径：单文件内不得混用行尾；**不得扩大到全仓级统一**） |
| `STANDARDS §L L5②`（**计数必须由脚本产生，不得手数**） | 本轮裁定 15b；与 `§9.5` 的「计数由脚本算并回读」**同一口径，不另立条** |

> **裁决自更正实例（对应 §L L5）**：裁决时曾把 P6/P14 判"条文缺"，核对后发现 §D3.2／§E2 已有 —— 原因是**关键词只试了一种说法**。⇒ 判"已存在/新增"必须至少换两种说法检索（单关键词 0 命中不构成"不存在"的证据）。

### 9.4 边界与残留（已落项 + 待确认项）

- **✅ 2 条（已落）**：reme `os._exit` 不刷缓冲 / locale 编码、l-s2t 编码边界两侧 ⇒ **已落 `STANDARDS §D9`「跨编码 / stdio 边界」**（2026-09-20 落笔；2 家实证 ⇒ 够通用；逐家锚点 = l-s2t `CHANGELOG.md:43`／`:1478-1482`；reme `CHANGELOG.md:593`／`:603`／`:611`）⇒ **对应源段落自此可删**。
- **5 条落点精度待确认**：dsh 跑真实执行 / reme 备份回滚源 / reme 校验缺失=失败 / reme 无头孪生 / l-s2t 派生量两段合取。
- **✅ Δ1/Δ2 与 STANDARDS §L 已落**（2026-09-20）：**§L = L1–L9**；**Δ1** → `STANDARDS §D3.5`（等待 / 轮询，**3 家**）；**Δ2** → `CONFORMANCE §4.1.65`（时新性判据，**[单家强证据]**）⇒ **对应源文档段落自此可删**。

### 9.5 判据自检

源条目 **72**（逐条；**计数由脚本算并回读**）：**已定位 61** ＋ **§1.1 的 6 条**（落点 `§K`，**已提交 `5fee7a6`**；其"是否与 §D/§E/§G 重复"的核重归终检重跑，故**单列、不计入已定位**）＋ **待精度确认 5** ＋ **无落点 0** = 72。
⇒ **留空 = 0**（无落点 0 + 无理由 0；另 5 条落点精度待确认）。
**与 §L L5② 同源**（"计数须脚本产生"）：本行即其 §9 侧落点，**不另立条**。
**自扫（复制即跑）**：`for w in 尚未 未改 未提交 未建 待落; do echo "$w=$(grep -o "$w" <file> | wc -l)"; done` ⇒ 过程稿 `retire-list.md` 全 **0**；本节（`CONFORMANCE §9`）**排除两处词表列示行后**亦 **0 处**。
**M3 待复核（不单方裁）**：过程稿 §1.6 的 2 条孤儿项是否计入"已定位"（本表取 **61**；旧口径 65/67 差 **2**）⇒ **登记 T11 只读复核**。

---

*本文件与 `STANDARDS.md` 冲突时以 STANDARDS 为准；本文件的状态列随每次审计更新，
更新即记入 `REVIEW.md` 的记录表。*
