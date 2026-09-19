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
| `modules/appconfig/appconfig.py` | 参数区：**唯一要改的文件** | `APP_ID` / `APP_NAME` / `REPO_OWNER` / `REPO_NAME` / `EXE_NAME` / `VERSION` / `ICON_DRAW(d, size)` | 1.0.0 |
| `modules/paths/paths.py` | 数据区/播种/稳定位/**数据根重定向** | `APP_DIR` `RUN_DIR` `USER_DATA_DIR` `CONFIG_PATH` `LEGACY_CONFIG_PATH` `LOG_DIR` `LOG_PATH` `UPDATE_DIR` `INSTALL_DIR` `INSTALL_EXE` `is_stable_install()` `ensure_user_dirs()` `seed_config()` `process_pending_update()` | 1.1.2 |
| `modules/autostart/autostart.py` | 自启三件套 | `get_autostart_cmd(target="stable")` `is_autostart_enabled()` `set_autostart(bool)` `migrate_autostart(log=…)` | 1.1.1 |
| `modules/update_helper/update_helper.py` | 更新三段式（查/下/换） | `check_update(cur, force=False)` `download_and_prepare(...)` `UPDATE_READY` `PENDING_CMD` | 1.0.1 |
| `modules/i18n/i18n.py` | 轻量中英双表（机制词表分离） | `init(lang)` `t(key,*args)` `load_language_from_config` `save_language_to_config` `detect_system_lang()` `load_tables()` `available_langs()` | 2.1.0 |
| `modules/icons/icons.py` | 代码生成双 ico | `make_image(size)` `write_app_icons(out_dir)` / CLI | 2.0.0 |
| `modules/tray_kit/tray_kit.py` | 单实例 / 退出请求 / token 掩码 / 签名重画 / **退出确认框** | `acquire_single_instance(app_id, mutex_name=None, log=…)` `single_instance_free(name)` `warn_duplicate_instance` `confirm_quit_dialog(app, text, init, parent=None, on_change=None)` `make_quit_request_path(dir)` `quit_watch_loop(stop, path, on_quit, beat)` `mask_token(url)` `MenuSignature(rebuild, menu_is_open, log)` | 2.0.1 |
| `modules/log_kit/log_kit.py` | 滚动日志 1MB×3 + 打开日志目录 | `make_logger(log_dir)` `get_logger(log_dir)` `LOG_MAX_BYTES` `LOG_BACKUPS` | 1.0.2 |
| `modules/service_link/service_link.py` | 服务唯一性/接入/有界清理状态机 | `ServiceLink(probe, launch, terminate, graceful=None, adopt_pid=None, log)` `.refresh()` `.can_start()` `.start()` `.stop()` `.state` `.spectators` `.note_spectators()` | 0.1.0 |
| `sync_check.py` | 防漂移哈希比对 | `python my-diy-tool-template/sync_check.py [--roots …]` | 1.2.0 |

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
| EXIT-02 | 人工路径必经二次确认（红底确认钮在左 + 取消持默认焦点 + `grab_set` 模态防叠加 + `WM_DELETE_WINDOW`/Esc = 取消） | `tray_kit.confirm_quit_dialog` | ✅ | ✅ `main.py:878-907` | ✅ | ✅ |
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
| SINGLE-07 | 守卫有断言覆盖（建互斥体→第二次调用须 False；失败注入须 True） | D3-02 | ⚠️ | ❌ **零断言**（这是 bug 存活 3 个月的根本原因） | ⚠️ | ⚠️ |

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
| NAME-10 | 环境变量名 = `<大写APP_ID去连字符>_CONFIG` / `_DATA_DIR`，四工具**格式统一** | B3 | `REME_HELPER_*` | `LOCALSPEAK2TEXT_*` | `DSH_HELPER_*` | `OPENCODEX_HELPER_*` |
| NAME-11 | 数据目录 = `%LOCALAPPDATA%\<APP_ID>\` | B3 | ✅ | ✅ | ✅ | ✅ |

> **NAME-10 的落地检查**：目前只有 `LOCALSPEAK2TEXT_*`（无 `_DATA_DIR`）、`DSH_HELPER_*`（无 `_CONFIG`）、
> `OPENCODEX_HELPER_*`（无 `_CONFIG`）、`REME_HELPER_*`（无 `_DATA_DIR`）。
> 模板 `paths.py` 1.1.2 **已含 `_DATA_DIR`**——四个工具都该同步，这是"模板领先于所有使用者"的唯一一条。

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
| 4.1.3 | `REVIEW.md` T7 行 | 称 local-speak2text 是"`--quit` 请求文件蓝本"，磁盘上 l-s2t **没有** `--quit` | 蓝本标注改为 reme-helper；l-s2t 需补 `--quit` 或明确不做 |
| 4.1.4 | `modules/icons/README.md` | 承诺 `make_image` / `write_app_icons(out_dir=".")`，正本实际是 `base_image()` / `make_icons(base_dir)` | 改 README 对齐正本 |
| 4.1.5 | `modules/paths/README.md` | 承诺 `<APP>_CONFIG` 由本模块支持，正本 `paths.py` 1.1.2 **没有**读该环境变量（`CONFIG_PATH` 直派 `USER_DATA_DIR/config.json`）；而蓝本 l-s2t 的 `paths.py` 里**有** `LOCALSPEAK2TEXT_CONFIG`——**模板相对自家蓝本发生了功能回退** | 已改 README 标注现状。补实现须同批同步 dsh/ocx 副本（否则 sync_check 立刻红灯），**列为待办** |
| 4.1.6 | `blueprints.txt` + `sync_check.py` | **蓝本豁免 = 永久盲区**：l-s2t 被豁免比对，模板已前进（`paths` 1.1.2 加了 `_DATA_DIR`），蓝本却停在原地且无人发现 | 豁免改为**限期**：每次模板升位后，蓝本必须回答"跟 or 不跟"并留痕；见 4.2 |
| 4.1.7 | `STANDARDS.md` J 坑 | "诊断参数冒烟过 ≠ 正常模式可跑"已记录 ef9b381 的教训，但**没有升级为条款**，导致 l-s2t 一个月后踩同款 | 已升级为 D3-01 的硬性要求 + SINGLE-04 检查点 |
| 4.1.8 | `STANDARDS.md` G4.1 条款 3（自启自愈） | 自愈的触发条件只有"注册表指向的 exe **不存在**"。当它指向一个**存在但已损坏/过期的版本目录**（本次：`release\local-speak2text-1.4.0\`，exe 在、但永远打不开）时**不会自愈**——每次开机照旧拉起坏版本 | 待裁定：自愈条件是否放宽为"指向的 exe 不是当前版本 且 当前实例处于稳定位"；或由更新器在替换后主动重写 Run 值。**在裁定前，构建脚本 `norun` 之外的一切换版本动作都要人工确认自启指向** |

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
> **设计纪律**：只写能给出证据的检查；判不了的宁可 WARN，不硬判 FAIL——
> 误判一次，人就再也不信这个工具了（首版即修掉 6 处误判，见 §4.3）。

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

### 5.3 需要人工目视（**不由 AI 代跑**）

| # | 检查 | 原因 |
|---|---|---|
| M-01 | 托盘图标在溢出区可见（dev + frozen 各一次） | 日志 `NIM_ADD` 与进程存活都不算数，必须肉眼确认 |
| M-02 | 退出确认弹窗按钮布局/焦点/模态行为 | 需要真实鼠标键盘 |
| M-03 | 浮窗生长/滚动/不越屏 | 视觉判断 |
| M-04 | 发版前整轮人工功能回归（D16 闸） | 规范明确"自动化不可替代" |

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

## 7. local-speak2text 首轮整改记录（2026-09-19）

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

*本文件与 `STANDARDS.md` 冲突时以 STANDARDS 为准；本文件的状态列随每次审计更新，
更新即记入 `REVIEW.md` 的记录表。*
