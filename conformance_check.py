# -*- coding: utf-8 -*-
# TEMPLATE-MODULE: conformance_check | TEMPLATE-VER: 2.0.2
# 2.0.2（W3 后段收尾）：**C-52 收窄**——pairs.json 重形态 grandfather 终结（reme 已迁
#   轻形态 locales/*.json，执行文档 W3 后段）。合法 i18n 形态只剩 src/template/i18n/
#   目录一种：i18n_gap 删 has_pairs 形参；C-20 删重形态跳过腿（词表外中文检查全家族生效）；
#   自测腿 neg_pairs_form_ok → pos_pairs_no_dir_is_gap 守卫格（豁免若回潮当场红）。
#   C-52 扫描面文案残留的 src/modules/ 同步改 src/template/。
# 2.0.1（W1 收尾步）：四仓已全部迁到 src/template/——**拆除 2.0.0 的全部过渡垫片**
#   （_find 双前缀展开、mod_root 回落、排除过滤器双名、C-34 双前缀与归一、
#   appconfig 双路径、C-35 加 modules、C-45 base 回落），一律只认 template/。
# 2.0.0（W1 改名，D8）：模板仓 modules/ → template/ 双布局过渡（垫片已在 2.0.1 拆除）。
# 1.9.29：**C-40 孤儿口径修正（2026-09-20 发版暴露）**：`release/` 下必然有三类目录 ——
#   ① 当前版本（跳过）/ ② **上一版**（历次构建的自然产物，§4.1.42 原话，**不登记**）/
#   ③ **改名保留镜像** `_stale_*` / `*.pre-rebuild-*`（**有意动作，必须登记**）。
#   旧实现把 ② 也算"待登记孤儿" ⇒ 登记量随发版次数**线性增长**、漏登是必然的
#   （本次发版一次就新增 4 条）。ORPHAN_VERSIONS 同步重写为只收 ③（4 条，措辞按新 Run 键更新）。
# 1.9.28：**C-52 口径变更（用户 2026-09-20 裁定）**：*"默认所有工具都应该支持双语"* ——
#   不再把"是否已开源"当开关。理由：四家全是公开仓库 ⇒ 开关恒开；而它作为开关的**副作用**
#   是给判据留了一条**豁免分支**（C-20 遇"未启用"直接放行、没人核对前提）。
#   ⇒ `i18n_gap` 删掉 `if not has_remote: return False`，只看"有没有 i18n"。
#   自证腿加一格 **`pos_no_remote_still_gap`**（传 has_remote=False 也必须报）——
#   这一格是"开关语义已移除"的守卫：哪天回退成 False，就说明有人把开关加回来了。
# 1.9.27：**新增 C-52（FAIL）**= T1 触发（有远端仓库 = 已开源）的工具**必须启用 i18n**。
#   补 **C-20 的豁免盲区**：C-20 遇到"未启用 i18n"直接 `return True, "T1 未触发或待办"`
#   —— **放行**，而**没有任何判据核对那个理由是否成立**。于是"该启用却没启用"是一个
#   不红不黄、连跳过了什么都不打印的状态（§4.1.18 同族：判据的**豁免分支**就是盲区）。
#   触发做成可判：`git remote` 非空 ⇒ 必须有 `src/modules/i18n/` 或 `pairs.json`（§E4 许可）。
#   判不了（非 git 仓库）按未触发放行，但**打印扫描面**（纪律 ⑥）。
#   自证 4 腿：红格（有远端+无 i18n）/ 未触发（无远端）/ 重形态 pairs / 有目录。
# 1.9.26：**新增 C-51（FAIL）**= 无 UI 的退出入口（`--quit`）不得沿用持久化清理勾选
#   （§4.1.43 / C-41 同族）。C-41 只查**降级分支**（except / `if x is None:`），
#   **不覆盖 `--quit` 这条无 UI 路径**（本判据补上）。
#   实测缺陷（2026-09-20 排查用户报告时发现）：reme `quit_watch_loop` 调
#   `shutdown_tray(TRAY_ICON)` 不传 kwargs ⇒ stop_* 落 None ⇒ 回读 CFG[quit_stop_*]
#   ⇒ **勾过一次"退出时停服务"的用户，会被一次外部 `--quit` 静默停掉服务**。
#   自证 2 腿（红格 = reme 修前真身；反向格 = 显式 stop_*=False 必须放行）。
# 1.9.25：**新增 C-50（FAIL）**= 退出路径的「未勾选」分支不得执行破坏性动作
#   （G4.2 **条款 5** 明文："不勾 = 服务与隧道越过托盘生命周期继续运行"）。
#   由来：**用户报告 2026-09-20** —— ocx 关闭后即使没勾选也把隧道关了。
#   实测根因：`on_quit` 把清理拆成 `if stop_tunnels: kill…` / **`else: terminate 所有
#   OWNED 句柄`** ⇒ 没勾选也清。**把条款 3 的「作用域规则」当成了「触发条件」**：
#   条款 5 管**要不要清**、条款 3 管**清理谁**，分工不可互推。
#   dsh/reme 无此病（两者压在同一条 `if <勾选>:` 里，`else` 只记日志）。
#   自证 3 腿（红格 = ocx 修前真身；反向格 = 勾选分支里 kill 合法 / else 只记日志放行）。
# 1.9.24：**R-10 加宽**（任务 A2 / §4.1.55）= ① **换 key：裸名 → 全路径**（`_leak_key`），
#   覆盖 `names_a`/`names_b`/`TMP_DECLARED_PATHS` 三处——否则多根下同名目录会被集合并集
#   去重吃掉、白名单也会暗吃掉别根的同名目录；② **扩根**：`%TEMP%` 之外纳入 l-s2t 仓内
#   三处落点（`build/test-data`、`build/selftest-data`、`release/<ver>/smoke-data`，它们既不在
#   `%TEMP%`、又被 `.gitignore` 的 `build/`+`release/` 遮住 ⇒ 无人兜底）；③ 每个根各自打印
#   **扫描面（候选数）+ 双腿命中数**。自证增 1 格（同名两根不去重 + 全路径豁免反向格）。
# 1.9.23：**补 C-44 段首盲区**（任务 A1 / §4.1.56）= `_bat_cmd_tokens` 在段首为 `if` 时
#   按 cmd 条件语法（`[not] [/i] errorlevel|exist|defined|cmdextversion <arg>` / `str1==str2`）
#   推进到**命令 token**，使 `if exist X findstr …` 这类裸名可判。
#   **只对 `if` 段推进，不做全空白切分**——后经合成电池实测：全空白切分会把 `echo find`、
#   `call :x find` 等 6/9 条合法行判红（§4.1.33）。
#   **改前/改后对照（在本家族 6 个根的全部 11 个 .bat 上）**：新增命中 **0**、消失 **0**
#   （即不误伤现有任何合法行）；潜伏形态由合成电池证明（5/5 正样本命中、9/9 合法负样本不命中）。
#   自证增 2 格（判别力格 + 反向格），合计 7 格。
# 1.9.22：**修 C-27 假红**（P5 批次暴露）：C-27 遍历 `src/modules/**` 时不认
#   `NOT-WIRED.md`（sync_check 的"有意不接入"申报口，§4.1.48）⇒ 把**如实申报**的
#   模块按"已采纳"查 MUST-WIRE，报成 FAIL（l-s2t/reme 的 `update_helper` 各一条）。
#   修法：该目录下有 `NOT-WIRED.md` ⇒ **跳过**（"不采纳"当然不接线）。
#   自证 2 腿（红格 = 有声明零引用必报；反向格 = 同一份 + NOT-WIRED 必不报）。
# 1.9.21：**新增 C-49（FAIL）**= 破坏性动作的守卫探测，**探测自身失败不得判为「不健康」**
#   （任务 #45 / §D3.2；§4.1.31 立的通用纪律的机械形态）。形态：**四条件同时满足才报** ——
#   ① 函数有 `except` 且不重新抛出；② 该分支的失败结果是 `False`（分支内 `return False`，
#   或分支不 return 而函数末尾是 `return False`）；③ 函数名出现在 `if not f(` 守卫里，
#   且守卫体内含破坏性动词；④ **函数本身必须是纯探测** —— 体内不得直接执行破坏性动作
#   （否则就是"动作本身"，`False` 是它的**正确语义**，如 reme `_rmtree_verified`）。
#   **ocx `probe_target` 修前正是这个形态**（返回值决定 `kill_target_procs` = 杀用户隧道）。
#   自证 4 腿（红格 + 三条反向格：失败放行 / 良性动作 / **动作执行者**）。
# 1.9.20：**新增 C-48（FAIL）**= 自建 Tk 控件不得用**中文字面量**做文案（R1 §3 T3 的守卫）。
#   由来：reme 的退出确认框 6 处硬编码中文，**英文模式下整框中文**，而当时三层判据全绿 ——
#   C-20（"词表外中文"）对**重形态** i18n 直接跳过（rem 是「中文即键」，中文不算"词表外"）。
#   判据形态：**只看函数体**（剔签名默认值 —— 模板 `confirm_text="退出"` 是向后兼容默认，
#   其 docstring 明说"不传则用中文默认值"，调用方经 `t()` 传词条 ⇒ 不是缺陷）、
#   只看**控件构造处的 `text=` 中文字面量**。两条合法通道都放行：
#   ① `translate_tree(w)` 事后递归替换（reme 修后用这条）；② **参数注入** `text=body_text`
#   （模板 `tray_kit.confirm_quit_dialog` 走这条）。另附：`.title(` 不得传裸 `APP_NAME`。
#   自证 3 腿（红格 = reme 修前真身；两条反向格 = translate_tree / 参数注入都必须放行）。
# 1.9.19：**W6 独立复核后的三处判据修正**（登记见 CONFORMANCE §4.1 F）：
#   ① **新增 C-47（FAIL）**= 派发件头不得用被禁形态 `TEMPLATE-MODULE` —— C-19 的 `and` 链
#      反把它列为合法形态 ⇒ R1 §2.1 那 13 处 `MODULE→FROM` 修复**没有任何守卫**（回归不会红）。
#      自证 3 腿（判别力格 = 旧谓词必漏 / 两条反向格 = 别误伤 FROM 与 LOCAL-OVERRIDE）。
#   ② **修 C-06 空真**（§4.1 F-2）= 只看**命令位置**：新增 `_strip_bat_prose` 剔 `rem`/`::`/`echo` ——
#      旧实现是纯 token 存在性，**reme 被自己的注释与错误提示骗绿**（删掉真拷贝行仍报"均随包"）。
#      自证 2 腿（红格 = 只有散文时必须红）。
#   ③ **修 C-46 分母**（§4.1 F-4）= `src/modules/**/*.md` **不计入构建输入**（是给人读的派发件，
#      不是 PyInstaller 打包输入）⇒ **只改文档不再误报"过期"**；自证 1 腿（含同目录 `.py` 反向格）。
#   ④ **登记但明确不改**：C-44 段首盲区（§4.1.56 —— 无真实案例 + 改动有假红风险）；
#      **驳回**"恢复横幅 `head:`"（§4.1.57 —— 那是任务 #58 的有意设计，差异 ≠ 回退）。
# 1.9.18：l-s2t 孤儿登记补「键名口径 = APP_NAME 非 APP_ID」+ 采集时点（§4.1.53）；纯登记文案，无判据行为变更。
# 1.9.17：C-46 的「过期」WARN 消息内联声明**本轮不重建 ⇒ 预期读数**（防下一个人去追它 / 去构建）；纯文案，无行为变更。
# 1.9.16：**C-40 选键改为「路径优先、键名兜底」**（§4.1.53/§4.1.54）= 家族 Run 键名无单一契约（模板 autostart 用 APP_NAME / reme 内联用 APP_ID），只认键名必漏一半；路径腿枚举全表、命中「值路径落在本工具仓库根或稳定安装位之下」，键名腿兜底 dev 态，且**打印实际走的哪条腿**。自证 5 条腿（两条正样本 + 外来项反向格）。
# 1.9.15：**修 C-40 键名假绿**（§4.1.53）= Run 键名从「按 `APP_ID` 单查」改为「取全表 + 按 `APP_NAME`→`APP_ID` 双候选选键并打印命中」——l-s2t 的 `APP_ID=local-speak2text` ≠ `APP_NAME=LocalSpeak2Text`，旧实现读不到 ⇒ 强断言从未执行；附大小写变体键提示（§4.1.51）。自证 4 条腿。
# 1.9.14：**新增 C-46**（WARN）= **重建新鲜度分母补全为构建输入集**（`src/**` ∪ `--add-data` 源，四家皆有 out-of-src datas）；自证 4 条腿（含「同一 exe 因 out-of-src 项变新而翻红」的承重格）。
# 1.9.13：**新增 C-35**（WARN）= **实例隔离两条腿**（测试文件自钉 + build.bat 整体外套），判别力已实测（关腿⇒ reme 11 红）。
# 1.9.12：**新增 C-34**（WARN，模板通道）= **§1 登记表版本列 == 文件头 TEMPLATE-VER**（手抄副本必然滞后）；自证 2 条腿。
# 1.9.11：**新增 C-45**（WARN）= **工具侧副本（`src/modules/**` 的 .py/.md）必须全程 CRLF**（`sync_check` 按 read_text 比、行尾被归一化），按字节判；自证 3 条腿。
# 1.9.10：**新增 C-44**（FAIL）= **bat 里闭集命令（find/findstr/ping/tasklist/robocopy/where/reg/timeout）必须用绝对路径**，与 C-33（ping 当节拍）**独立**；只看命令位置，自证 5 条腿。
# 1.9.9：**新增 C-43**（FAIL）= **`if` 条件里的 `:~` 子串扩展**（未定义时会中止整个脚本）——**窄版**：嵌套 `if`（无 `:~`）与动作一侧的 `:~` 均判绿，自证 4 条腿。
# 1.9.8：**新增 C-42**（FAIL）= **重定向位置不得出现 `dev/null`**（收窄版：不写成“全文不得出现 dev/”，否则注释里的路径与 URL 会误报）；文本口径与 C-33 同一条边界（正文保留、散文不算），自证 5 条腿。
# 1.9.7：**新增 C-41**（FAIL）= 退出确认的「链路不可用」分支必须固定为**不停服务**（不得沿用已存勾选）——判据只看降级分支，**原生框那一支不算**；
#   实测模板 + 四家全绿（今天无违规，立判据是为了防 `tray_kit` 统一之后长回去），自证 5 条腿。
# 1.9.6：**新增 C-40**（FAIL）= 版本目录 ↔ 自启目标必须一致（强断言）+ 孤儿版本目录必须两栏登记（WARN）；读**磁盘 + 注册表**，纯函数 + 可注入 `path_exists` （样本不受活状态污染），自证 6 条。
#   **实测：dsh = FAIL**（源码 VERSION=1.8.1 而 Run 键指着 `release\dsh-helper-1.8.2\`）。
# 1.9.5 三条：
#   ① **新增 C-39**（工具通道 + 模板通道，FAIL）=**派生值必须取自本次调用的实参**：默认参数不得取“会被重绑的模块级名字”或可变字面量，**良性常量必须放行**（三档判别，否则就是噪音判据）。
#   ② **判据读散文两例已修**（§4.1.37）：`_strip_docstrings` 挖 AST 裸字符串表达式、`_masked_code_text` 就地掩码保行号、扫描面排除仪器自身并打印排除项（C-33 / C-30）。
#   ③ **C-38 改形态**：锚在 `startup` 行之后 20 行内 + 一次性行不计入
#      （原“文件前 N 行”按字面会假绿）；“判不了”按 WARN 报。
# 1.9.4 两条（都来自复核员的实测）：
#   ① **身份行加 `at:` 时点**——"任何「命中 N 个」的转述都必须自带时点"（同一族：扫描面说「扫了什么」、时点说「什么时候」）。实证：reme 残留我广播成 8、**当前是 5**（消失 4、新增 1）——**残留集是活的**，本轮第二次栽在这上面。
#   ② **`TMP_DECLARED_PATHS` 的口径写清**：**声明过的、且会随下次构建自动重建的位置**，正确处置是**进白名单**，**不是要求清理**——清理既不持久，又会产生**虚假的进展感**（看起来清干净了，下次门禁又长出来）。# 1.9.3：① **新增 C-37（模板通道，FAIL）= C-2 拒绝删除句柄**：静态半（`paths.py` 提供
#   `hold_no_delete` / `hold_exe_delete_guard` + README 的 `<!-- MUST-WIRE -->`，否则四家
#   拷走了也**没人调用**）+ **性质半**（用临时文件实测：持句柄时 `unlink` / `rmtree(父目录)`
#   **必须失败**，释放后 `unlink` **必须成功**这个判别控制）。自检另加**判别力样本**：
#   把共享位写成 `…|FILE_SHARE_DELETE`（允许别人删）的原语**必须被抓住**——共享位写错在
#   源码上完全看不出来，只能实测。
#   ② **C-29 补两条"不下判"样本**：`log=` 后面给的是**日志路径**（`log_path` 变量 /
#   `HELPER_UPDATE_LOG` 常量）时必须 `[ok]`（不下判）——l-s2t/reme 的真实形态，报红就是假红。
#   ③ **顺手补两条已漏登记的索引行**：C-36 自 1.9.1 起实现，却一直没进 CONFORMANCE §5.1 表
#   （"索引里缺条目本身就是盲区"——这次是**我自己**犯的）。
#   ④ **另修两处转义损坏**（本轮实测发现，都是"描述这个坑的文本自己踩坑"）：
#      `家族规范.md:492` 的 `System32<0x0c>ind.exe`（应为 `System32\find.exe`）、
#      `合规对照表.md` 的 `%TEMP%<0x0d>eme-helper-builddata`（应为 `%TEMP%\reme-helper-builddata`）。
#      **第 ④ 条还暴露了我的字节检查不完整**：只数了 `CRLF` 与"孤立 LF"，**从没数过孤立 CR**
#      ——"混合行尾"可以整整齐齐地藏在那个盲区里（本轮就是这么藏的）。
# 1.9.2：**腿 B 按复核员的实测再放宽一次 + 扫描面口径修正**（lead 转达复核员取证后裁定）：
#   ① **不再要求 `config.json`、不设深度上限**：旧签名（config 在 ≤1 层 + 顶层下存在 `*.log`）
#      抓不到 `tmp.6FcrxXYxmM\d\local-speak2text`（3 层、只有 `log/`）这类真实残留。
#      新签名 = **任意深度存在名为 `log` 的目录**（B3 规定日志落 `<数据根>/log/`）。
#      **候选口径实测后才选**（同一次扫描，顶层目录 95 / 条目 647）：
#        V0 旧签名 7 命中 / V1「任意深度存在 `*.log` 文件」13 命中（多出的 5 个是他程序日志：
#        WebView 缓存、vmware、virtual_camera、kzip_sogou… ⇒ **太宽、制造假红**，否掉）/
#        V2「任意深度存在 `log` 目录」8 命中 ⇒ **采用 V2**；残余 FP 风险（外来程序的 `log/`）在案。
#   ② **已声明位置白名单** `TMP_DECLARED_PATHS`：`reme-helper-builddata` 是 reme
#      `scripts/build.bat:22` **明写的稳定构建数据位**，不是漏扫残留——它此前**永久红**，
#      且"形态能认出数据根"≠"它是泄漏"（复核员对照实验：同规则扫 %LOCALAPPDATA% 命中的
#      恰好是那 4 个真实数据根）⇒ **判"是不是泄漏"必须靠位置 + 声明**。白名单只豁免报告
#      与增量判定，不改判据。
#   ③ **扫描面报"目录数"**：lead 曾把顶层**条目数**（目录+文件，634）当成目录数（101）报出，
#      两张扫描面因此不可比。现在两个数**各带标签**一起打印。
#   ④ **回归集措辞更正**：那 20 个是**自标定集**（规则拿它标定、再用规则命中它 = 循环），
#      **不构成独立验证**，不得声称"零误报"；独立复算由复核员给出 = **14**（16:55，他重实现）。
#      `reme-helper-builddata` 已从回归集移除（它不是残留）。
#   ⑤ **[BROKEN] 档**（lead 批准）：判据**自身抛异常**不再混进"检出违规"——独立成档、
#      进汇总计数、**独立进退出码**（不计 FAIL、也不被 WARN 咽掉）。由来：`check_md_tabs`
#      是收 `Path` 的助手却在重构后**留着 `@check` 装饰器**，四个工具各报一条"检查异常"，
#      **看起来像工具坏了**，整整一轮排查方向是错的（STANDARDS §J"幽灵判据"）。
#      自检样本：一条故意抛异常的判据必须得到 `(0 FAIL, 0 WARN, 1 BROKEN)`。
#      **同批还补**：本文件自己的 selftest 收尾**必须消费 `_rmtree_strict` 的返回值**
#      （原来只调用不看返回，等于"加了重试但不看结果"——正是 C-30 要治的形状）。
# 1.9.1：**身份行**（lead 批准）：每次运行的第一行打印
#   `# conformance_check <VER>  sha256:<raw>  norm:<归一化>`
#   —— `raw` = 文件逐字节 sha256，`norm` = sync_check 口径（剔 `# TEMPLATE-*` 行后哈希）。
#   **两种都印**，因为本家族同时用两套口径发哈希（ALIGNMENT §0 专门钉过这件事）；
#   只印一种，迟早有人拿另一套去对，得出"对不上"的假结论。
#   动机：同一类分歧（tray_kit 版本 / 183 行 / C-11）今晚发生了**三次**，每次都靠人工
#   对齐修订号，成本极高。**一行身份行让任何贴回来的输出自证身份**——是旧快照还是磁盘
#   这份，看第一行就知道。它同时是 R-EVID 的**自动化形式**：让工具自己打印时点，
#   比要求每个人记得贴时点可靠（"用结构代替纪律"）。
# 1.9.0：① **C-30 补上"覆盖缺口必须自己报出来"**（lead 裁定：判据可以自己失效比泄漏更糟）。
#   ① 新增上半：**mkdtemp 前缀必须可静态归属**——从源码枚举 `mkdtemp(...)` 的 `prefix` 实参
#      （含**包装函数的调用点**，如 `scratch_dir(prefix)`：dsh/ocx/l-s2t 三家真实前缀都在
#      调用点上）；f-string / 变量 / 无 prefix 等推不出的站点，必须在模块级字面量
#      `TMP_PREFIX_REGISTRY`（键 `"相对路径:行号"` → 等价前缀）登记，**不登记即红**。
#      登记表的值非字面量 = 判据读不到 = 等于没登记，也红；登记了却对不上站点 = 过期 WARN。
#   ② 下半扫描范围 **tests/ → 全工具**：真实树立刻多出一处 **reme `src/main.py:7409`
#      `rmtree(work, ignore_errors=True)`**（`work` = 7405 的 mkdtemp 根），是同一缺陷的
#      生产代码形态；只看 tests/ 会整个溜过去。首跑真实树：**C-30 1 FAIL（reme，
#      `src/main.py:7405` 的 `prefix=f"{APP_ID}-update-"` 未登记）**，其余三工具 ok。
#   ③ 运行期取证改成**两条腿**（task #43，lead 裁定）：腿 A 生成器派生（前缀枚举 + 登记表；
#      裸 `mkdtemp()` → 系统默认前缀 `tmp`，列为**弱前缀**并单独 WARN，因为它会撞上无关目录）、
#      ⚠️ **归因更正（2026-09-19，lead 自我更正 + ls2t-dev 判别实验）**：腿 A 的天花板**不止**是
#      "源码里出现过的 prefix"，而是 **"它只看我们枚举得到的源码"**——由 **shell `mktemp -d`**、
#      外部 CLI、探针脚本造的目录**源码里没有调用点**，腿 A 结构上抓不到。判别形态（`_name_shape`）：
#      `tmp.gVxHfxTMya`（带点+10）= GNU `mktemp -d`；`tmpigscx7m2`（无点+8）= Python `mkdtemp()`。
#      所以腿 B 必须打印**名字形态直方图**——它把"有残留"变成"该去改谁"（进程规则 vs 仓库代码）。
#      腿 B **形态派生**（`_SHAPE_RULE`：**任意深度存在名为 `log` 的目录**——B3 规定日志一律落
#      `<数据根>/log/`，故"有 log 目录"就是数据根的不变量；**不看名字、不要求 config.json、
#      不设深度上限、log 里的文件是 0 字节甚至没有文件都算**）。**必须打印扫描面**——
#      实测：112 个顶层目录上腿 A = **0**、腿 B = **20**，20 个全在腿 A 命中之外；若把签名
#      写成"log 非空"则只覆盖 11/20。那 20 个的名字（`icon-probe-*`/`smoke-proof-*`/
#      `reme-gate-2.2.0`/`tmp*`）**在四个工具源码里一个字都搜不到**（裸 mkdtemp 的默认前缀、
#      或扫描范围之外的探针脚本）——"前缀法 0 命中"与"真没泄漏"在输出上完全同形，这就是
#      "判据可以自己假绿"。20 个已登记为负样本回归集 `_TEMP_REGRESSION_20260919`，
#      ⚠️ 但它是**自标定集**（规则拿它标定，再用规则命中它 = 循环），**不构成独立验证**，
#      不得据此声称"零误报"；独立复算由复核员给出 = **14**（16:55，他重实现）。
#      ⚠️ **2026-09-19 两次放宽，两次都是先实测再改签名**：
#      ① 旧签名多写了一条"**恰好一个子目录**"，那是**形状的偶然特征、不是不变量**——任何多一个
#      子目录（如 `ui-icons/`）的数据根都会隐身。合成形状实测：`log/{config.json,app.log}` HIT、
#      **加一个 `ui-icons/` → MISS**、**config 摆在顶层 → MISS**（后两者都是真实形态）。
#      放宽后当日 93 个顶层目录实测：旧 4 命中 / 新 7 命中，**新增的 3 个是 `marker-e2e-*`**。
#      ② 再放宽（复核员报真实残留 `tmp.6FcrxXYxmM\d\local-speak2text`：**3 层、只有 `log/`、
#      没有 config.json`**）：旧签名两种写法全抓不到。候选口径在同一次扫描上实测对照——
#      「任意深度存在 `*.log` **文件**」= 13 命中，**多出的 6 个里 5 个是他程序日志**
#      （WebView 缓存、vmware、virtual_camera、kzip_sogou…）⇒ **太宽，制造假红**，否掉；
#      采用「任意深度存在 `log` **目录**」= 8 命中（7 个自家数据根 + 1 个外来程序的 log/）。
#      FP 残余风险在案；另有**已声明位置白名单** `TMP_DECLARED_PATHS`（构建脚本明写的固定数据位，
#      不算泄漏）。
#   ④ 新增运行期取证/验收（只读）：`--temp-leak`（列出 %TEMP% 命中，**永远 exit 0**——
#      历史存量会让它恒红，那是取证不是判据）、`--temp-leak-save` / `--temp-leak-baseline`
#      （**增量断言**：只对"跑测试期间新增"报红，残留免疫）。这才是 lead 定的验收口径
#      "跑完门禁后实测 = 0"的可执行形态。**"0"要按时点读**：lead 16:11 那次测得 dsh 3 个
#      残留目录的 mtime 就是 16:11（门禁运行当口 ⇒ 当时在产生新的），而 tpl-keeper 稍后
#      复扫同一批 19 个前缀得 **0 命中**——两次测量各自成立，谁也不能替对方下结论；
#      "清一遍就好了"同样只是一个时点，只有增量断言不依赖历史存量。
#   ⑤ 本工具自守 C-30：selftest 收尾从 `rmtree(..., ignore_errors=True)` 改成
#      `_rmtree_strict`（删后回读、失败抛错）——同一个 %TEMP% 泄漏形态，判据作者自己也会犯。
#   样本 11 条（前缀 7 + 清理 4），含 dsh/ocx/l-s2t 的 `param_prefix_literal_calls_ok`。
#   · 新增 **C-31（WARN，模板正本专属）**：派发件（`modules/**` 的 `.py`/`.md`，排除模板
#   专属的 `build_release/` `baseline/`）必须全程 CRLF。由来：C-22 只管 `.bat`/`.cmd`，
#   **模板里的 `.py`/`.md` 被写成 LF 没有任何一层会报**（`py_compile` 绿、`sync_check` 两边
#   同为 LF 也绿）——`log_kit.py` 被整文件重写那次就是"读回字节"才发现的。lead 批准为
#   **WARN**（不误伤将来有意为之的文件，但让不一致可见）。为此新开 `TEMPLATE_CHECKS` 注册表：
#   模板判据**只跑一次**（`Ctx.dir` = 模板仓根），不跟着四个工具重复输出 N 遍。
#   **首跑真实树：4/27 个派发件是 LF-only**（`autostart.py` / `icons.py` /
#   `service_link/README.md` / `service_link/service_link.py`），且**工具侧副本同样是 LF**
#   （dsh/ocx/l-s2t 的 `autostart.py`、reme 的 `service_link/*`）——要改成 CRLF 必须
#   **正本 + 全部副本同批**（只改正本会让 `sync_check` 立刻 `[DIFF]`），属一次"可重拷"冻结事件。
#   · **C-30 第二路径：可折叠模块常量**（lead 2026-09-19 裁定"低成本做法"）：模块级
#   `APP_ID = "reme-helper"` + `prefix=f"{APP_ID}-update-"` 其实**推得出**（折成
#   `reme-helper-update-`），不该逼作者写登记表。只认模块级字面量；同名再赋不同值或赋非
#   字面量 → 该名字不可折叠（**宁缺勿猜**）。登记口径同步升级为**两态**：未登记 → FAIL /
#   已登记 → OK（原 WARN 留了"把字面量改成变量即可降级"的逃逸口）。样本 +3（折叠常量 / 折叠
#   拼接 / 同名冲突仍红）。**真实树**：reme 靠折叠转 `[ok]`，C-30 只剩 `rmtree(work, ignore_errors=True)`。
#   · **C-28 补扫模板正本 + §4.1.18**（lead 批准"最省事形态"）：此前 `main()` 用
#   `d.name not in {..., TEMPLATE_DIR.name}` 把模板仓**显式排除**，于是模板自己的 `.md`
#   从未被扫过，而模板是四份副本之源——**"判据存在 ≠ 被检查对象在范围内"**。只让 C-28
#   额外扫一遍模板仓、只报一次（不给模板开整轮：它没有 `src/` + `build.bat`，会空转甚至误报）。
#   **留档**：C-28 的规则文本自己那条 CHANGELOG 里就落进两个真 TAB（想写两字符 `` `\t` ``，
#   写进去的是真 TAB，`HEAD 188bbcc` 上已存在）——**描述这个坑的文档，本身踩了这个坑**。
# 1.8.0：新增 **C-30**：测试里对 **mkdtemp 根目录**的清理必须可验证——禁 `ignore_errors` 吞掉。
#   根因（实测）：四工具在 %TEMP% 积了 **133~138 个**自家前缀目录，每个里恰好一个文件
#   `<app>/log/<app>.log`——**`log_kit` 的 FileHandler 句柄还开着**（Windows 拒删在用文件），
#   而 `rmtree(..., ignore_errors=True)` 把失败静默吞掉 → 每跑一次泄漏一个，**门禁全绿**。
#   **判据刻意收窄**防误伤 best-effort 清理：只报"**mkdtemp 根目录**"被 ignore_errors 删；
#   删子目录 / 固定路径 / 用有返回值的助手一律放行。四条样本，含 `neg_ignore_errors_on_scratch_subdir`。
#   **首跑真实树即发现自身**一处**漏报**并修掉：reme 写的是 `root = Path(tempfile.mkdtemp(...))`，
#   只认裸调用会让最该检查的文件报"本条不适用"——现在按"赋值右侧含 mkdtemp"判定（l-s2t 的
#   `scratch_dir(...)` 包装形态也一并认了，根目录计数由 4→9）。真实树现值：四工具 0 FAIL。
# 1.7.2：C-11 补收 **`.Path` + 目录精确比较**这一族（不带 `-Name` 的写法，如
#   `Get-Process | Where-Object {$_.Path -eq ...}`）——它比 `tasklist | findstr` 的**子串匹配
#   更强**（无子串歧义，直接比"运行实例所在目录 == 本次构建目标"），此前会掉进"认不出形态"
#   的 WARN 里，等于**对着更强的实现报"判不了"**。样本按 lead 点名的名字对齐：
#   `pos_ps_getprocess` / `pos_tasklist_findstr` / `neg_no_detection`(WARN)，
#   另加 `pos_ps_path_compare`、`neg_substring_only`(FAIL)、`neg_no_c_literal`(WARN)。
# 1.7.1：设计纪律 ④ 升级——**"不认识形态" ≠ "检出违规"**（lead 裁定，本轮最强的一条判据要求）。
#   ① C-10 的两处兜底（既无探针也无守卫调用节点 / 有 --smoke 但无 `def smoke`）改报 **WARN**：
#     判据看不出"绕过"（那取决于 `--smoke` 与守卫在 main() 里的先后），只能说"不认识这个形态"。
#   ② C-11 拆成三档：`tasklist|findstr` 取得出字面量且对得上 → ok；**对不上 → FAIL（确证）**；
#     看得到 `tasklist|findstr` 但取不出 `/c:"字面量"` → **WARN（形态不认识）**。
#   ③ 保留 FAIL 的两处（C-10 的 AST 真跑守卫节点、C-11 的错误字面量）**其余措辞改成"确证"**，
#     让消息与检出物一致（纪律 ④a）。
#   ④ C-11 补三条样本：`pos_tasklist_findstr`（此前**正中靶心的分支反而没有样本**）、
#     `neg_substring_only`（带版本号字面量 = D1-02 真实违规 ⇒ FAIL）、`neg_no_c_literal`（⇒ WARN）。
#     C-10 的两条 WARN 样本也补上 sev 断言（原先只断言 ok，severity 变了没人知道）。
# 1.7.0：新增 **C-29**：交给模板件的日志函数必须接受可变参数（print 形态）。
#   根因是 `update_helper`（7 处多参调用）与 `log_kit` 1.0.2（单参闭包）**说不同的话**，
#   而 dsh/ocx/l-s2t 各写了一份互不相同的本地 log 包装把冲突分别盖住/藏住。
#   首跑真实树即报出 **l-s2t**（`src/main.py:80 def log(message)` + 231/998/1043 三处
#   `log=log`），并附实测证据：模板件 L257/L390 的两个位置参数直接 TypeError。
#   三条样本：varargs_log_ok / single_arg_wired_flagged / single_arg_unused_ok。
#   同时 **log_kit 1.0.3 把 log 统一为 print 形态**（这是判据能成立的前提）。
# 1.6.0：① **修 C-11 假红灯**（dsh/ocx）：它们用 PowerShell `Get-Process -Name <APPNAME>`
#   做运行检测，旧实现只认 `tasklist | findstr` → 报"未找到运行检测"（一句与事实相反的诊断）。
#   现在两种形态都认；**两者都没有时按 WARN 报**——框架支持检查按分支返回级别（3 元组）。
# 1.5.0：① **修 C-10 假红灯**（reme）："结果被消费"≠"必须写成 if"——探针**作为参数交给
#   check() 助手**也算消费；兜底分支改按 **AST 调用节点**找真跑守卫（原来对函数体做文本匹配，
#   把注释里的 single_instance_free() 当成了真调用 → 打印与事实相反的诊断）。新增两条样本：
#   pos_probe_passed_to_check_helper / pos_guard_name_in_comment_only。
#   ② 新增 **C-28（WARN）**：本仓 `.md` 不得含 0x09 TAB（lead 裁定：不扩到所有文本文件，
#   只挑手写中文文档这一类，误报成本低）。
# 1.4.0：新增三条「当天缺陷没有现役条款能拦」的机械判据（各带正负样本）：
#   C-25 门禁步骤必须**既存在又能被执行**（reme build.bat:201 被 TAB 写坏 ⇒ 该步从未执行）
#   C-26 `start` 前必须存在性守卫——外部程序"成功"不能只靠排除失败码（robocopy rc=0 ≠ 成功）
#   C-27 模块采纳 = 拷贝 + 接线（README `<!-- MUST-WIRE: sym -->` 声明的符号须在**工具代码**里被引用）
# 1.3.0：新增 **C-22 bat/cmd 字节卫生**（CRLF + 无 0x09 + 纯 ASCII，逐文件逐行报位置）。
#   把"bat 必须 CRLF + 纯 ASCII"从口头纪律升级成可执行判据；五条 selftest 样本（TAB / LF-only /
#   非 ASCII / 混合 / 合规）。构建产物与脚手架目录（release/out/dist/_internal/.cache/.verify-scratch）
#   跳过——它们不是作者手写、也不入库。
# 1.2.0：C-10 判据重写——旧判据只要 smoke() 里出现 `mutex|single_instance` **任意子串**就算过，
#   太松（"把 --smoke 提前分派 + 留一句注释"就能骗过），**区分不了"覆盖了"与"绕过了"**。
#   现判据（D3.3）：smoke() 内必须有**探针** `mutex_name_is_valid(...)` 且**判了结果**；
#   真跑守卫（acquire_single_instance）判 FAIL 并说明会弹模态框挂死构建；
#   `single_instance_free` 不算探针（用户实例在跑时返回 False → 假红）。四种形态各一条 selftest。
# 1.1.0：新增 C-23（模块级状态被 global 重绑 = 脆形态）与 C-24（菜单读的容器状态未进签名 /
#   有菜单无签名机制），补 STANDARDS §D6 的机械阶梯 C-21 → C-23 → C-24；两条都有 --selftest
#   正反样本。C-22 号被"bat/cmd 字节卫生"占用，故本组从 C-23 起编号。
"""CONFORMANCE §5.1 的机械化落地：把"靠 AI 记得住"变成"不绿就报"。

与 sync_check.py 的分工：
  sync_check.py        只管「拷贝件与模板正本是否一致」（哈希级）
  conformance_check.py 管「条款是否落地」（语义级，但仍要求可机械判定）

设计纪律 ①–⑦（来自 2026-09-19 首轮审计的教训；**索引与正文必须一致**——索引缺条目本身
就是"文档说谎"）：
  ① 只写**能给出证据**的检查；判不了的宁可 WARN，不硬判 FAIL——误判会让人不再信任工具；
  ② 每条检查的输出必须带 `文件:行号` 或实际值，否则等于没说；
  ③ FAIL = 硬违规（默认让退出码非 0）；WARN = 需要人判断，只提示；
  ④ **"不认识形态"与"检出违规"必须分开**（2026-09-19 由 lead 升级，合并原有两条口径）：
     (a) 判据的"不通过消息"**必须与它实际检出的东西一致**——检不出就说检不出，不许拿不相干
         的模式去解释失败（C-10 曾把"消费形态不认识"说成"真跑守卫"，误导出错误修法）；
     (b) 遇到**判据自己不认识的形态**时，一律 **WARN + "形态不认识，需人工确认"**，并在消息里
         写明"期望什么形态 / 实际看到什么"。**不认识 ≠ 违规**；**FAIL 只能用在确实检出违规
         证据的时候**（AST 调用节点、行号 + 实际值这类）。
     (c) **判准：分支级别取决于「它检出的东西」，不取决于「它期望的形态」**——确证违规 → FAIL；
         检不出/形态不认识/证据不足 → WARN。降错方向的代价是**真缺陷从红灯变黄灯、GATE 不再拦**。
     * 为什么升级：同一元缺陷一天内出现**三次**——C-10 的 `check()` 形态、C-10 的正则读注释、
       C-11 的 PowerShell 形态；每次都是"判据只认自己那一款，别款一律报违规"。误判一次，
       人就再也不信这个工具（纪律 ①）。
  ⑤ **判据的每条限定，都必须用"已知正例"回验过才算数**（2026-09-19 加）：前四条管
     "判据的**输出**要诚实"，⑤ 管"判据的**构造过程**要回验"。实证（复核员做 C-32 时逐条回验）：
     加"同一语句块"→ 漏掉正典、命中 0；加"最近一条赋值"→ 落在 `except` 里的 `detail = ""`
     上，命中 4、**漏了 reme**；改成"遍历所有先前赋值"才 5/5 全真。**"收紧条件"不能靠加限定词
     的直觉**。推论：**样本必须抄真实现场的形状**——用想象的形状写样本，会得到"全绿但漏真案"。
  ⑥ **判据报"ok / 不适用 / 0 命中"时，必须同时给出它的扫描面**（2026-09-19 加，lead 依
     tpl-keeper 的实证升级）：**"只报 0 命中"与"确实没有"在输出上不可区分**——本族反复栽
     的形状。**"没命中 ≠ 没问题"**。实证（C-30 首版自犯）：只认裸调用 `X = mkdtemp(...)`，
     于是 reme 的 `root = Path(tempfile.mkdtemp(...))` **被静默跳过**——**最该被检的文件被判成
     "本条不适用"**；改按"赋值右侧含 `mkdtemp(`"+认包装调用点后 → reme 1 / l-s2t 9 / dsh 6 /
     ocx 6。落地：ok/不适用分支必须打印"扫了哪些路径、候选几个、命中几个"（`--temp-leak` 是
     范例），**样本要断言这个数字**，否则"扫了 0 个文件"会伪装成绿。
     同族三条各管一面：④ 管**输入形态**（不认识 ≠ 违规）、§4.1.18 管**适用范围**（判据存在 ≠
     在范围内）、⑥ 管**覆盖**（没命中 ≠ 没问题）。
  ⑦ **同一件事只允许一份判据：禁止自造第二套"加强版"**（2026-09-19 加，lead 裁定后立）：
     两份判据会各自漂移、各自误报，最后由"**没人知道该信哪个**"——**判据自己成为新的漂移源**，
     与 §4.1.18"索引缺条目本身就是盲区"并列。实证：复核员的 C-30 增强草案未到时，本文件作者
     **拒绝**并行自造一版"加强版前缀判据"；后到的草案必须**合并进同一个检查**，不并存。
     同族第二形态（lead 当日更正）：**"判据的机制"与"取证的方法"不能混成一句话**——C-30 从
     第一版起就是**读源码判定**，而"枚举前缀再回查 `%TEMP%`"是**一次性的取证方法**。
     落地：新增检查前先问"这条是否已有实现/草案"；有则扩展那一个（或等它）。
     与 ④⑥ 的分工：④ 输入形态、⑥ 覆盖、⑦ 唯一性——三条一起堵住"判据自己变成漂移源"。

用法：
  python my-diy-tool-template/conformance_check.py                  # my_diy_tools 下全部工具
  python my-diy-tool-template/conformance_check.py --roots dsh-helper local-speak2text
  python my-diy-tool-template/conformance_check.py --strict         # WARN 也计入退出码
  python my-diy-tool-template/conformance_check.py --only C-08 C-09
  python my-diy-tool-template/conformance_check.py --selftest       # 合成样本反向自证各判据

C-30 的运行期验收（**增量断言**，残留免疫；"清一遍"不算证据）：
  跑测试前：… --roots <工具> --temp-leak-save build\\_tmpbase.txt
  跑完门禁：… --roots <工具> --temp-leak-baseline build\\_tmpbase.txt   # 新增非空 = 泄漏复现
"""
import argparse
import ast
import itertools
import os
import re
import subprocess
import sys
from pathlib import Path

try:  # Windows 控制台默认 GBK，中文检查标题会变乱码
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

def repo_identity(path) -> str:
    """`repo=<name> rev=<short sha> dirty=<yes|no>` —— **被检仓库**的修订与脏净。

    为什么必须逐仓库打一行（lead 2026-09-19，采用 ls2t-dev 的形态）：只印 checker 自身
    身份，仍看不出"这条结论建立在哪个修订、是否建立在**未提交**改动上"——有人贴过工作区态
    的 `[ok]` 却没声明，复核者无从判断。`dirty=yes` 一栏**一行暴露**"结论建立在未提交改动上"。
    取不到 git 就印 `?`（非 git 目录 / 无 git / 超时都不许让判据崩）。
    """
    import subprocess as _sp
    path = Path(path)
    rev, dirty = "?", "?"
    try:
        r = _sp.run(["git", "-C", str(path), "rev-parse", "--short", "HEAD"],
                    capture_output=True, text=True, timeout=5)
        if r.returncode == 0 and r.stdout.strip():
            rev = r.stdout.strip()
            s = _sp.run(["git", "-C", str(path), "status", "--porcelain"],
                        capture_output=True, text=True, timeout=5)
            if s.returncode == 0:
                dirty = "yes" if s.stdout.strip() else "no"
    except Exception:
        pass
    return "repo=%s rev=%s dirty=%s" % (path.name, rev, dirty)


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_DIR = Path(__file__).resolve().parent


def identity_line() -> str:
    """**本工具自己的身份**（lead 2026-09-19 批准）：版本 + 两种哈希口径。

    为什么是运行时自算、而不是写死一串：写死的哈希**自己就会过期**——那正是"贴回来的
    输出说不清是哪个时点"的成因。自算保证"这一行永远描述**正在跑的这个文件**"。
    两种口径都给：`sha256`（逐字节）与 `norm`（sync_check 归一化：剔 `# TEMPLATE-*` 行）。
    本家族两套都在用（`.py` 比对用 norm、`.md` 用逐字节，ALIGNMENT §0 专门钉过），
    **只印一种就会有人拿另一种去对**，然后得出"对不上"的假结论。
    **实测的判别实例**（可复算，2026-09-19 实测）：在本文件末尾只追加一行 `# TEMPLATE-TEST: …`
    ⇒ `raw 8213f62be793 → f6b5d7711a26`（**变**）而 `norm 0179f3bfda82 → 0179f3bfda82`（**不变**）。
    ⇒ **只印 norm 会看不见"抬头/版本动了"；只印 sha256 又会与 `.py` 的比对口径（norm）对不齐。**
    ⚠️ 这条实例是**我实测的合成对照**，不是历史读数——lead 转述的那个"`sync_check` 1.8.2→1.8.3
    时 sha256 变而 norm 没变"**实测不成立**：那两个修订两侧都变了
    （raw `230c5c4deb5f→7b104dc70994`、norm `0d2335462db4→1eccbbf2b908`），且两件工具的
    **全部相邻修订里都没有"一个变一个不变"**的实例。**机制为真，那个具体例子为假。**
    """
    import hashlib
    import re as _re
    import subprocess
    raw = Path(__file__).read_bytes()
    text = raw.decode("utf-8", "replace")
    norm = "\n".join(ln for ln in text.splitlines()
                     if not _re.match(r"^\s*#\s*TEMPLATE-", ln))
    m = _re.search(r"TEMPLATE-VER:\s*([\d.]+)", text[:2000])
    ver = m.group(1) if m else "?"
    # **横幅不印 ref**（任务 #58，2026-09-19）：工具自印自己的 HEAD = 被测对象供给判它的
    # 可观测量，属"无判据"而非"漏判"。ref 由读的人在外面配（`git rev-parse HEAD` 的 blob id），
    # 与自报的 sha256/norm **两类证据分开记、不互替**（§D8 附则 附 2）。
    # `at:`（lead 2026-09-19 加，"计数必须带时点"）：**任何"命中 N 个"的转述都需要时点**——
    # 残留集是活的（本轮 reme 从 8 变 5：消失 4、新增 1），缺时点的数字会让接收方去找
    # 已不存在的东西。**扫描面说"扫了什么"，时点说"什么时候"**，两者齐了读数才可判。
    import time as _time
    at = _time.strftime("%Y-%m-%dT%H:%M:%S")
    return ("# conformance_check %s  sha256:%s  norm:%s  at:%s"
            % (ver, hashlib.sha256(raw).hexdigest()[:12],
               hashlib.sha256(norm.encode("utf-8")).hexdigest()[:12], at))

# 蓝本工具（内容以模板正本为准，不按"消费方"判定）
def load_blueprints() -> set:
    cfg = TEMPLATE_DIR / "blueprints.txt"
    if not cfg.exists():
        return set()
    return {ln.strip() for ln in cfg.read_text(encoding="utf-8").splitlines()
            if ln.strip() and not ln.lstrip().startswith("#")}


class Ctx:
    """一个工具的检查上下文（惰性探测，避免检查项各自重复读盘）。"""

    def __init__(self, name: str, tool_dir: Path):
        self.name = name
        self.dir = tool_dir
        self._cache = {}

    def _find(self, *cands):
        for c in cands:
            p = self.dir / c
            if p.exists():
                return p
        return None

    @property
    def src(self) -> Path:
        return self.dir / "src"

    @property
    def mod_root(self) -> Path:
        """工具侧模块目录根（W1 改名后为 src/template）。"""
        return self.src / "template"

    @property
    def entry(self):
        if "entry" not in self._cache:
            self._cache["entry"] = self._find("src/main.py", "main.py")
        return self._cache["entry"]

    @property
    def build_bat(self):
        """只认真正含门禁的那个 bat（有些工具根 build.bat 只是转发壳）。"""
        if "build" not in self._cache:
            cands = [p for p in (self.dir / "build.bat",
                                 self.dir / "scripts" / "build.bat",
                                 self.dir / "build_release" / "build.bat")
                     if p.exists()]
            real = [p for p in cands if "PyInstaller" in self.read(p)
                    or "pyinstaller" in self.read(p)]
            self._cache["build"] = (real or cands or [None])[0]
        return self._cache["build"]

    @property
    def build_blob(self) -> str:
        """全部门禁 bat 的合并文本（有的工具把步骤拆在多个 bat 里）。"""
        if "bblob" not in self._cache:
            parts = []
            for p in (self.dir / "build.bat", self.dir / "scripts" / "build.bat",
                      self.dir / "build_release" / "build.bat",
                      self.dir / "release.bat"):
                if p.exists():
                    parts.append(self.read(p))
            self._cache["bblob"] = "\n".join(parts)
        return self._cache["bblob"]

    def py_files(self):
        if "py" not in self._cache:
            out = []
            for p in self.src.rglob("*.py"):
                if any(part in {".git", "__pycache__", "build", "out", "dist"}
                       for part in p.parts):
                    continue
                out.append(p)
            self._cache["py"] = sorted(out)
        return self._cache["py"]

    def read(self, path) -> str:
        try:
            return Path(path).read_text(encoding="utf-8", errors="replace")
        except OSError:
            return ""

    @property
    def app_id(self) -> str:
        """先从 appconfig 找 APP_ID，退回 paths.py。"""
        if "app_id" not in self._cache:
            found = ""
            for p in self.py_files():
                m = re.search(r'^\s*APP_ID\s*=\s*["\']([^"\']+)["\']', self.read(p), re.M)
                if m:
                    found = m.group(1)
                    break
            self._cache["app_id"] = found or self.name
        return self._cache["app_id"]

    def find_line(self, path, pattern):
        """返回 (行号, 行内容) 或 None —— 证据必须是行号。"""
        for i, line in enumerate(self.read(path).splitlines(), 1):
            if re.search(pattern, line):
                return i, line.strip()
        return None

    @property
    def guard_file(self):
        """单实例守卫的实现文件：先看模板件副本，再看内联定义。"""
        if "guard" not in self._cache:
            guess = self._find("src/template/tray_kit/tray_kit.py")
            if guess is None:
                for p in self.py_files():
                    if re.search(r"^\s*def\s+acquire_single_instance\b",
                                 self.read(p), re.M):
                        guess = p
                        break
            self._cache["guard"] = guess
        return self._cache["guard"]

    def has_i18n(self) -> bool:
        return bool(self._find("src/template/i18n/i18n.py", "src/i18n.py")
                    or self._find("locales", "src/locales"))

    def git_files(self, *patterns):
        try:
            r = subprocess.run(["git", "-C", str(self.dir), "ls-files", *patterns],
                               capture_output=True, timeout=30)
        except (OSError, subprocess.SubprocessError):
            return None
        if r.returncode != 0:
            return None
        return [ln for ln in r.stdout.decode("utf-8", "replace").splitlines() if ln.strip()]


CHECKS = []


def check(cid, severity, title):
    def deco(fn):
        CHECKS.append((cid, severity, title, fn))
        return fn
    return deco


# **模板正本专属**判据：`main()` 里只跑一次（`Ctx.dir` = 模板仓根），不跟着工具跑 N 遍。
# 为什么单开一张表：这类判据的对象是**正本自己**（拷出去之前的样子），按工具重复执行既
# 不增加信息、又把同样的行刷 N 遍淹没真信号。首个成员是 C-31（派发件行尾）。
TEMPLATE_CHECKS = []


def template_check(cid, severity, title):
    def deco(fn):
        TEMPLATE_CHECKS.append((cid, severity, title, fn))
        return fn
    return deco


# ---------------------------------------------------------------- C-01 / C-02
@check("C-01", "FAIL", "一级目录不出现 .py（B1-02）")
def c01(c: Ctx):
    hits = sorted(p.name for p in c.dir.glob("*.py"))
    return (not hits), ("根目录 .py: " + ", ".join(hits)) if hits else "一级无 .py"


@check("C-02", "FAIL", "不存在 src/tests（B1-01）")
def c02(c: Ctx):
    p = c.src / "tests"
    return (not p.exists()), str(p) if p.exists() else "无 src/tests"


# ---------------------------------------------------------------- C-03 / C-04
@check("C-03", "FAIL", "版本单一事实源，只写一处（A1-03）")
def c03(c: Ctx):
    hits = []
    for p in c.py_files():
        for i, line in enumerate(c.read(p).splitlines(), 1):
            if re.match(r'^\s*VERSION\s*=\s*["\']', line):
                hits.append("%s:%d" % (p.relative_to(c.dir).as_posix(), i))
    return (len(hits) == 1), ("VERSION 定义: " + ", ".join(hits)) if hits else "未找到 VERSION"


@check("C-04", "WARN", "登记表版本 == 磁盘版本（B2-01）")
def c04(c: Ctx):
    std = TEMPLATE_DIR / "家族规范.md"
    if not std.exists():
        return True, "无 家族规范.md"
    text = std.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"\|\s*%s\s*\|[^|]*\|[^|]*\|\s*`([\d.]+)`" % re.escape(c.name), text)
    if not m:
        return False, "B2 登记表无 %s 行" % c.name
    table_ver = m.group(1)
    disk = ""
    for p in c.py_files():
        mm = re.search(r'^\s*VERSION\s*=\s*["\']([^"\']+)["\']', c.read(p), re.M)
        if mm:
            disk = mm.group(1)
            break
    if not disk:
        return False, "无法读到磁盘 VERSION"
    return (table_ver == disk), "表 %s / 磁盘 %s" % (table_ver, disk)


# ---------------------------------------------------------------- C-05..C-07
@check("C-05", "FAIL", "README 语言切换行精确格式（A1-08/DOC-02）")
def c05(c: Ctx):
    en, zh = c.dir / "README.md", c.dir / "README.zh-CN.md"
    if not (en.exists() and zh.exists()):
        return False, "缺 README.md 或 README.zh-CN.md"
    problems = []
    if not re.search(r"^\*\*English\*\*\s*\|\s*\[简体中文\]\(README\.zh-CN\.md\)",
                     c.read(en), re.M):
        problems.append("README.md 第 3 行未写成 **English** | [简体中文](...)")
    if not re.search(r"^\[English\]\(README\.md\)\s*\|\s*\*\*简体中文\*\*",
                     c.read(zh), re.M):
        problems.append("README.zh-CN.md 未写成 [English](...) | **简体中文**")
    return (not problems), "; ".join(problems) if problems else "两份切换行格式正确"


def _strip_bat_prose(text: str) -> str:
    """丢掉 bat 里**不执行**的行：`rem`/`::` 注释与 `echo` 输出。

    **为什么需要**：判据若在全文找 token，就会被"说明这件事"的散文骗绿 ——
    `rem`/`echo` 行含同样的字面量，但它们**不执行任何动作**。与 §4.1.37
    （判据读散文 ⇒ 判据自己判自己红）同族，方向相反：这里散文让判据**假绿**。
    **"提到"与"执行"必须分开。**
    ⚠ 边界：`echo … >> file` 会真写文件，但那是**输出文本**而非**复制动作**，
    本判据问的是"有没有把 README 拷进 release"，故一并排除（保守侧：宁可在
    `echo` 里漏判，也不要被注释骗绿——漏判可由门禁输出行兜住，假绿不能）。
    """
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        low = s.lower()
        if not s or low == "rem" or low.startswith("rem ") or low.startswith("rem\t") \
                or s.startswith("::") or low.startswith("echo"):
            continue
        out.append(ln)
    return "\n".join(out)


@check("C-06", "WARN", "两份 README 都随 release 复制（DOC-05）")
def c06(c: Ctx):
    """只看**命令位置**：排除 `rem`/`::` 注释行与 `echo` 行。

    旧实现是 `"README.zh-CN.md" in text`（纯 token 存在性）⇒ **reme 被自己的注释与
    错误提示骗绿**：删掉 `scripts/build.bat:370-371` 的真拷贝行后，`:366` 的
    `rem Both READMEs ship: … README.zh-CN.md …` 与 `:371` 的
    `echo [ERROR] README.zh-CN.md was not copied…` 仍含该字面量 ⇒ 判据照旧报"均随包"
    （verifier 2026-09-19 用纯字符串变异实测，dsh/ocx/l-s2t 同变异**转红**=负控通过，
    只有 reme 空真）。与 C-44「只看命令位置」同一手法：**提到 ≠ 执行**。
    """
    text = c.build_blob
    if not text:
        return False, "找不到 build.bat"
    body = _strip_bat_prose(text)
    has_zh = "README.zh-CN.md" in body
    return has_zh, ("build.bat 未复制 README.zh-CN.md" if not has_zh else "两份 README 均随包")


@check("C-07", "FAIL", "代码生成的 ico 不入库（A1-01/G2-01/G5-01）")
def c07(c: Ctx):
    files = c.git_files("*.ico", "*.png")
    if files is None:
        return True, "无 git 或非仓库，跳过"
    ico = [f for f in files if f.lower().endswith(".ico")]
    if ico:
        return False, "生成物入库: " + ", ".join(ico[:6])
    return True, "无 ico 入库（png 手工资产按 B1 允许）"


# ---------------------------------------------------------------- C-08..C-11
def _literal_value(raw: bool, text: str) -> str:
    """把源码里的字符串字面量还原成"值"：普通字符串 `\\\\` 是**一个**反斜杠。"""
    if raw:
        return text
    return re.sub(r"\\\\", lambda _m: "\\", text)


def _indent_block(lines, idx):
    """取 lines[idx] 所属 if 语句的块体（缩进更深的那些行）。"""
    head = lines[idx]
    indent = len(head) - len(head.lstrip())
    out = []
    for j in range(idx + 1, len(lines)):
        ln = lines[j]
        if not ln.strip():
            continue
        if (len(ln) - len(ln.lstrip())) <= indent:
            break
        out.append((j, ln))
    return out


@check("C-08", "FAIL", "互斥体名合法：Local\\ 前缀后不得再有反斜杠（SINGLE-01）")
def c08(c: Ctx):
    """用 AST 取字面量的**值**——注释里引用的反例（如本模块头部的说明）不算违规。"""
    gf = c.guard_file
    if gf is None:
        return True, "未发现自建守卫（可能未启用 T12）"
    rel = gf.relative_to(c.dir).as_posix()
    try:
        tree = ast.parse(c.read(gf))
    except SyntaxError as exc:
        return False, "%s 语法错误: %s" % (rel, exc)
    bad = []
    for node in ast.walk(tree):
        value = None
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value
        elif isinstance(node, ast.JoinedStr):     # f-string：把字面片段拼起来看整体
            value = "".join(p.value for p in node.values
                            if isinstance(p, ast.Constant) and isinstance(p.value, str))
        if value and "Local\\" in value and value.count("\\") >= 2:
            bad.append("%s:%d %s" % (rel, node.lineno, value))
    return (not bad), ("非法互斥体名（含第二个反斜杠）: " + "; ".join(bad)) if bad else "命名合法"


@check("C-09", "FAIL", "守卫自身失败必须放行（SINGLE-02/D3.2）")
def c09(c: Ctx):
    gf = c.guard_file
    if gf is None:
        return True, "未发现自建守卫"
    text = c.read(gf)
    m = re.search(r"def\s+acquire_single_instance\b[\s\S]*?(?=\ndef |\Z)", text)
    if not m:
        return True, "无 acquire_single_instance 定义"
    body = m.group(0)
    lines = body.splitlines()
    fail_open = re.search(r"except[^\n]*:[\s\S]{0,300}?return\s+True", body) is not None
    for idx, ln in enumerate(lines):
        if re.match(r"\s*if\s+not\s+handle\b", ln):
            block = [b for _j, b in _indent_block(lines, idx)]
            if any(re.search(r"return\s+False", b) for b in block):
                return False, ("`if not handle` 的块体直接 return False = 失败即拒绝"
                               "（守卫自身失败必须放行）")
            if any(re.search(r"return\s+True", b) for b in block):
                fail_open = True
    if not fail_open:
        return False, "守卫失败时没有显式放行路径（既无 try/except→True，也无 not handle→True）"
    return True, "失败方向为打开"


# 探针 = "验名字合法性，不占锁不弹窗"。**不能**认 single_instance_free：用户常驻实例
# 在跑时它返回 False，拿它当冒烟断言会假红（D3.3 的禁忌之一）。
_PROBE_NAMES = {"mutex_name_is_valid"}
# 真跑守卫：命中即说明冒烟可能弹模态框把构建挂死（**只在探针缺失时**拿来作提示）。
_GUARD_NAMES = {"acquire_single_instance", "single_instance_free", "warn_duplicate_instance"}


def _callee_name(node) -> str:
    """调用表达式取被调名：`f()` / `mod.f()` / `self.f()` 都归一到 `f`。"""
    if not isinstance(node, ast.Call):
        return ""
    fn = node.func
    if isinstance(fn, ast.Name):
        return fn.id
    if isinstance(fn, ast.Attribute):
        return fn.attr
    return ""


def _calls(fn, names) -> bool:
    """AST 级：函数体里是否存在对 `names` 之一**真正的调用节点**（注释/字符串不算）。"""
    return any(isinstance(n, ast.Call) and _callee_name(n) in names for n in ast.walk(fn))


def _guarded_probe_calls(fn) -> tuple:
    """在函数体里找**结果被消费**的探针调用，返回 (已消费数, 只调未判数)。

    **判据是"返回值有没有被用"，不是"必须写成 `if`"**（2026-09-19 修，reme 假红灯）：
      * **裸表达式语句** `mutex_name_is_valid(...)` → 值被丢弃 → `plain`（覆盖 ≠ 调用）；
      * **其余一切**都算已消费 → `guarded`：条件里、`assert`、布尔组合、**作为参数交给
        `check()`/断言助手**（reme 的形态）、赋给变量……。

    旧判据只认 `if`/`while`/`assert` 的 test，于是 reme
    `check("single-instance name valid", mutex_name_is_valid(...))` 落在两种之间 →
    `guarded=0, plain=0` → **假红灯**。这正是"假红灯比漏报更伤信任"那一条。
    """
    dropped = {id(n.value) for n in ast.walk(fn)
               if isinstance(n, ast.Expr) and _callee_name(n.value) in _PROBE_NAMES}
    guarded = plain = 0
    for n in ast.walk(fn):
        if isinstance(n, ast.Call) and _callee_name(n) in _PROBE_NAMES:
            if id(n) in dropped:
                plain += 1
            else:
                guarded += 1
    return guarded, plain


@check("C-10", "FAIL", "诊断参数不绕过正常启动路径：smoke 须有守卫**探针**并判结果（D3.1/D3.3）")
def c10(c: Ctx):
    """判据要能区分"**覆盖了**"和"**绕过了**"——这是本条两轮修正的核心。

    * 旧判据（2.0.x）：`smoke()` 里出现 `mutex|single_instance` **任意子串**就算过。
      太松：把 `--smoke` 提前分派、函数体里留一句注释提到 mutex 都能骗过它。
    * 现判据（D3.3）：**AST 取 `def smoke` 的 body 范围**，要求其中有**探针调用**
      `mutex_name_is_valid(...)`，且该调用**被条件/断言消费**（`if not …` / `assert`）。
      只调用不判断 = 没有覆盖；写在注释里 = 更不算（子串判据会误收，AST 不会）。
    * 反例（不许当解）：`acquire_single_instance()` **真跑** —— 用户常驻实例在跑时会弹
      **模态**重复启动框，把无人值守的构建挂死（本家族已踩两次）。
    """
    if c.entry is None:
        return True, "无入口文件"
    text = c.read(c.entry)
    if "--smoke" not in text:
        return True, "无 --smoke"
    try:
        tree = ast.parse(text)
    except SyntaxError as exc:
        return False, "入口文件语法错误，无法判定：%s" % exc
    smokes = [n for n in ast.walk(tree)
              if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "smoke"]
    if not smokes:
        return False, ("**判不了（形态不认识）**：入口里有 `--smoke`，但没有名为 `smoke` 的函数可查"
                       "——本判据要求冒烟逻辑落在具名函数里，才判得了'覆盖'与'绕过'。"
                       "这**可能**是形态不认识（冒烟代码写在别处），而非没有覆盖。"
                       "期望形态：`def smoke(): ...`；实际看到：入口文件里没有该函数定义。"), "WARN"
    guarded = plain = 0
    for fn in smokes:
        g, p = _guarded_probe_calls(fn)
        guarded += g
        plain += p
    if guarded:
        return True, "smoke 用探针覆盖了守卫名字合法性，且结果被条件/断言消费"
    if plain:
        return False, ("smoke 调了 mutex_name_is_valid 但**没判结果**（覆盖 ≠ 调用："
                       "要么 if not … 中止，要么 assert）")
    # 只能按 **AST 调用节点**判定守卫——**绝不能对函数体做文本匹配**：守卫名出现在
    # 注释里（如"别用它 single_instance_free()"这种说明）会把诊断带偏，报出一句与事实
    # 相反的话（reme 2026-09-19 实例：它既有注释又有正确的探针，却被报成"真跑守卫"）。
    hit = sorted({n for fn in smokes for n in _GUARD_NAMES if _calls(fn, {n})})
    if hit:
        return False, ("**确证**（AST 直接调用节点，不是文本猜测）：smoke() 里调用了 %s —— 真跑守卫。"
                       "用户常驻实例在跑时会弹模态重复启动框，把构建挂死。"
                       "改用探针 tray_kit.mutex_name_is_valid()" % "/".join(hit))
    # 既没检出探针、也没检出真跑守卫 —— 这是**未检出**，不是**确证违规**（设计纪律 ④）。
    # 判据只认识"已知形态"；工具完全可能把覆盖包在别的助手函数里。所以报 WARN 并写明
    # 期望形态与实际所见，把判断交回人——**不认识 ≠ 违规**。
    return False, ("**判不了（形态不认识）**：smoke() 里既没有探针 `mutex_name_is_valid(...)` 的"
                   "调用节点，也没有真跑守卫的调用节点。**若你确实绕过了守卫，那才是 SINGLE-04/"
                   "D3.1 违规**——但本判据看不出'绕过'（那取决于 `--smoke` 与守卫在 main() 里的"
                   "先后），所以只报 WARN，请人工确认。期望形态：`if not "
                   "tray_kit.mutex_name_is_valid(APP_ID): raise RuntimeError(...)`；"
                   "实际看到：smoke() 里没有任何已知守卫符号的调用节点。"), "WARN"


@check("C-11", "FAIL", "运行检测匹配串能命中当前 exe 名（SINGLE-05/D1-02）")
def c11(c: Ctx):
    """三种形态，**认不出时只报 WARN**（2026-09-19 修假红灯，与 C-10 同类）。

    dsh/ocx 用 **PowerShell `Get-Process -Name <APPNAME>`** 做运行检测，旧实现只认
    `tasklist | findstr`，于是对它们报"未找到运行检测"——**假红灯 + 误导诊断**（人家明明有）。
    现在：① `tasklist | findstr /c:"..."`；② `Get-Process ... -Name <名>`；③ 两者都没有 ⇒
    **WARN**（判不了就不硬判，见设计纪律 ①）。
    """
    text = c.build_blob
    if not text:
        return True, "无 build.bat"
    appname = re.search(r'set\s+APPNAME=(\S+)', text)
    app = appname.group(1) if appname else c.app_id
    exe = app + ".exe"
    saw_tasklist_without_literal = False
    for line in text.splitlines():
        if "tasklist" in line and "findstr" in line:
            mm = re.search(r'/c:"([^"]+)"', line)
            if mm:
                probe = mm.group(1).replace("%APPNAME%", app)
                if probe and probe in exe:
                    return True, "tasklist 匹配串 %r 能命中 %s" % (probe, exe)
                return False, ("**确证**：`%s` 的匹配串 %r 与当前 exe 名 %s 对照不上——只有旧版"
                               "带版本号的 exe 会被命中，当前实例在跑也拦不住构建"
                               % (line.strip()[:70], probe, exe))
            saw_tasklist_without_literal = True
        if "Get-Process" in line:
            mm = re.search(r"-Name\s+'?\"?([\w.%\[\]]+)", line)
            if mm:
                probe = mm.group(1).replace("%APPNAME%", app)
                if probe and probe in exe:
                    return True, "PowerShell 匹配名 %r 能命中 %s" % (probe, exe)
                return False, ("**确证**：PowerShell 匹配名 %r 与当前 exe 名 %s 对照不上"
                               % (probe, exe))
        # **`.Path` + 目录精确比较**这一族（dsh/ocx 的形态）：它比 `tasklist | findstr`
        # 的**子串匹配更强**——没有子串歧义，且直接比"运行实例所在目录是不是本次构建目标"。
        # 不带 `-Name` 时（如 `Get-Process | Where-Object {$_.Path -eq ...}`）此前会掉进
        # "认不出形态"的 WARN 里，那是对着更强的实现报"判不了"。认得就明确放行。
        if "Get-Process" in line and ".Path" in line:
            return True, ("PowerShell `Get-Process` 取 `.Path` 做**目录精确比较**（SINGLE-05 的"
                          "强化形态：无子串歧义）")
    if saw_tasklist_without_literal:
        return False, ("**判不了（形态不认识）**：看到 `tasklist | findstr`，但取不出 `/c:\"...\"` "
                       "字面量来与 exe 名对照——它可能用别的方式写匹配串。期望形态："
                       "`tasklist ... | findstr /i /c:\"%APPNAME%.exe\"`；"
                       "实际看到：该行没有 `/c:\"...\"`。"), "WARN"
    # 判不了就不硬判（设计纪律 ①④）：认不出形态 ⇒ **WARN**，并给出补形态的指引。
    return False, ("**判不了（形态不认识）**：既无 `tasklist | findstr` 也无 `Get-Process`，"
                   "本判据不认识该工具的运行检测形态——**不认识 ≠ 违规**，请人工确认。"
                   "若该工具确有自有实现，请把它的形态补进本检查"), "WARN"


# ---------------------------------------------------------------- C-12..C-15
@check("C-12", "FAIL", "菜单签名重画被消费（E2-09）")
def c12(c: Ctx):
    if c.entry is None:
        return True, "无入口文件"
    text = c.read(c.entry)
    # 两种合法形态：直接用模板类，或内联等构（模板类名 / 自带签名+菜单占用探测）
    if "MenuSignature" in text:
        return True, "使用模板 MenuSignature"
    inline = ("menu_is_open" in text and
              ("tray_signature" in text or "MENU_DIRTY" in text
               or "GUI_INMENUMODE" in text))
    if inline:
        return True, "内联等构（签名比较 + 菜单占用探测）"
    return False, "既无 MenuSignature 也无内联签名/占用探测（菜单每拍全量重建，开着会被打断）"


@check("C-13", "WARN", "存在队列封送骨架（E1-03/I-03）")
def c13(c: Ctx):
    hits = [p.relative_to(c.dir).as_posix() for p in c.py_files()
            if re.search(r"\bui_q\b|\bui_post\b|\bui_call\b", c.read(p))]
    return bool(hits), ("队列封送在: " + ", ".join(hits)) if hits else "未发现 ui_q/ui_post"


@check("C-14", "FAIL", "日志轮转 1MB x 3（D4-02）")
def c14(c: Ctx):
    lk = c._find("src/template/log_kit/log_kit.py", "src/log_kit.py", "log_kit.py")
    if lk is None:
        return False, "未找到 log_kit"
    text = c.read(lk)
    ok = ("maxBytes" in text or "LOG_MAX_BYTES" in text) and \
         ("backupCount" in text or "LOG_BACKUPS" in text)
    rel = lk.relative_to(c.dir).as_posix()
    return ok, ("%s 缺 maxBytes/backupCount" % rel) if not ok else "%s 轮转参数在位" % rel


@check("C-15", "WARN", "托盘有「打开日志目录」（D4-02/A3-02）")
def c15(c: Ctx):
    pats = ("打开日志目录", "open_log_dir", "Open log folder", "open_logs")
    hits = [p.relative_to(c.dir).as_posix() for p in c.py_files()
            if any(k in c.read(p) for k in pats)]
    locale = c.dir / "locales"
    if not hits and locale.is_dir():
        hits = [p.name for p in locale.glob("*.json")
                if any(k in c.read(p) for k in pats)]
    return bool(hits), ("日志目录入口在: " + ", ".join(hits)) if hits else "未发现「打开日志目录」入口"


# ---------------------------------------------------------------- C-16..C-20
@check("C-16", "FAIL", "实例隔离：_CONFIG 与 _DATA_DIR 两个 env 都要有（B3-04/B4-04）")
def c16(c: Ctx):
    """找**实际读取点**，两种写法都要认：
        os.environ.get("LOCALSPEAK2TEXT_DATA_DIR")          # 字面量
        os.environ.get(_ENV_PREFIX + "_DATA_DIR")           # 常量拼接（l-s2t 收敛后用这种）
    2026-09-19 修：原实现只认字面量，l-s2t 改成拼接式后被误报成"两个 env 都没有"。
    """
    # 判据：同一行里既有 `environ` 又有该后缀。三种写法都能覆盖：
    #   environ.get("APP_DATA_DIR") / environ.get(_PREFIX + "_DATA_DIR") / environ.get(f"{X}_DATA_DIR")
    # （2026-09-19 修：先前用"紧贴引号的完整键名"正则，把 f-string / 拼接式全判成缺失，
    #   造成 dsh/ocx 的 `_DATA_DIR` 与 l-s2t 的两个 env 都被误报。）
    # 只认 environ 的**取参表达式**，避免把 `DEFAULT_CONFIG` 这类含 `_CONFIG` 的标识符误判
    # （2026-09-19 第二轮修正：先用"整键名"，漏了拼接/f-string；改用"同行含子串"，又误收 DEFAULT_CONFIG）。
    env_arg = re.compile(r"environ(?:\.get\(\s*|\[\s*)([^)\]\n]{0,160})")
    want, missing = {}, []
    for suffix in ("_CONFIG", "_DATA_DIR"):
        hits = []
        for p in c.py_files():
            rel = p.relative_to(c.dir).as_posix()
            for i, line in enumerate(c.read(p).splitlines(), 1):
                for arg in env_arg.findall(line):
                    # 后缀之后不能紧跟标识符字符，否则 NPM_CONFIG_PREFIX 会被当成 `_CONFIG`
                    # （2026-09-19 第三轮修正：dsh/ocx 的 NPM_CONFIG_PREFIX 曾骗过本检查）
                    if re.search(re.escape(suffix) + r"(?![A-Za-z0-9_])", arg):
                        hits.append("%s:%d" % (rel, i))
                        break
        want[suffix] = hits
        if not hits:
            missing.append(suffix)
    if missing:
        return False, ("缺 %s 环境变量读取点（测试/自检无法钉住配置或隔离数据根）"
                       % "、".join(missing))
    return True, "; ".join("%s@%s" % (s, ",".join(h[:2])) for s, h in want.items())


@check("C-17", "FAIL", "测试不触碰用户真实注册表/数据区（B4-04/D3-03）")
def c17(c: Ctx):
    tdir = c.dir / "tests"
    if not tdir.is_dir():
        return True, "无 tests/（已在 B1-01 单列）"
    bad = []
    for p in tdir.rglob("*.py"):
        text = c.read(p)
        if not re.search(r"HKEY_CURRENT_USER|HKCU", text):
            continue
        # 允许"写注册表"的用例，但必须备份+还原（finally/restore），否则跑测试会改坏用户配置
        if re.search(r"finally|restore|backup", text, re.I):
            continue
        bad.append(p.relative_to(c.dir).as_posix())
    return (not bad), ("测试写用户注册表且无还原: " + ", ".join(bad)) if bad else "测试未触碰用户注册表（或已备份还原）"


@check("C-18", "FAIL", "build.bat 门禁含 sync_check 与测试（B4-03/D1-05/D3-02）")
def c18(c: Ctx):
    text = c.build_blob
    if not text:
        return False, "找不到 build.bat"
    problems = []
    if "sync_check" not in text and c.name not in load_blueprints():
        problems.append("门禁无 sync_check 步")
    if not c.dir.joinpath("tests").is_dir():
        problems.append("无 tests/ 目录（D1 门禁 3 / 故障回归无载体）")
    elif "tests\\" not in text and "tests/" not in text:
        problems.append("门禁不跑 tests/")
    return (not problems), "; ".join(problems) if problems else "门禁含 sync_check 与测试"


@check("C-19", "WARN", "模板件头部 TEMPLATE-FROM/TEMPLATE-VER 齐（B4-01/B4-03）")
def c19(c: Ctx):
    mods = c.mod_root
    if not mods.is_dir():
        return True, "无 src/modules/"
    missing = []
    for p in sorted(mods.rglob("*.py")):
        if p.name == "__init__.py":
            continue
        head = c.read(p)[:4096]
        if "TEMPLATE-FROM" not in head and "TEMPLATE-MODULE" not in head \
                and "TEMPLATE-LOCAL-OVERRIDE" not in head:
            missing.append(p.relative_to(c.dir).as_posix())
    return (not missing), ("无模板头: " + ", ".join(missing)) if missing else "模板件头部齐全"


@check("C-47", "FAIL", "派发件头不得用被禁形态 `TEMPLATE-MODULE`（已被 `TEMPLATE-FROM` 取代）")
def c47(c: Ctx):
    """R1 §2.1 那 13 处 `# TEMPLATE-MODULE:` → `# TEMPLATE-FROM:` 的修复，**当时没有守卫**：
    C-19 的判定串反而把 `TEMPLATE-MODULE` 列为合法形态（`"TEMPLATE-MODULE" not in head`
    是它 `and` 链里的一项）⇒ **回归不会被任何判据抓住**（verifier 2026-09-19 复核发现，
    §4.1 F-1）。本条把唯一被禁的形态独立成判据 —— 与 C-19 分工：C-19 管**有没有头**，
    本条管**是不是被禁的那一种**（一条判据一个职责，改 C-19 的语义会混淆两件事）。
    """
    mods = c.mod_root
    if not mods.is_dir():
        return True, "无 src/modules/"
    hits = []
    for p in sorted(mods.rglob("*.py")):
        if "TEMPLATE-MODULE" in c.read(p)[:4096]:
            hits.append(p.relative_to(c.dir).as_posix())
    if hits:
        return False, ("仍用被禁形态 `TEMPLATE-MODULE`（应改为 `TEMPLATE-FROM`，§2.1）: "
                       + ", ".join(hits))
    return True, "无被禁头形态"


_TK_TEXT_CN = re.compile(r"text\s*=\s*[\"']([^\"']*[\u4e00-\u9fff][^\"']*)[\"']")


@check("C-48", "FAIL", "自建 Tk 控件不得用**中文字面量**做文案（须走 t()/translate_tree）")
def c48(c: Ctx):
    """R1 §3 T3：reme 的退出确认框有 6 处硬编码中文，**英文模式下整个框仍是中文**，
    而当时**三层判据全绿** —— C-20（"词表外中文"）对**重形态** i18n 直接跳过
    （rem 是「中文即键」，中文本身不算"词表外"）。⇒ 重形态工具缺的正是这条腿。

    **判据只看"控件构造处的 `text=` 是不是中文字面量"**（不是"有没有 translate_tree"）：
    合法通道有两条 —— ① `translate_tree(w)` 事后递归替换（reme 修后用的就是它）；
    ② **参数注入**（`text=body_text`，词条在调用点经 `t()` 传入；模板
    `tray_kit.confirm_quit_dialog` 走这条，见 R1 §2.1 第 2 项）。两条都放行，
    只有"中文字面量写死在控件构造处"才报。
    另附一条：`.title(` 不得传裸 `APP_NAME`（常量，不随语言走）。
    """
    problems = []
    for p in c.py_files():
        src = c.read(p)
        if "tk.Toplevel" not in src:
            continue
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        rel = p.relative_to(c.dir).as_posix()
        lines = src.splitlines()
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not node.body:
                continue
            # ⚠ **只取函数体，不含签名默认值**：模板 `tray_kit.confirm_quit_dialog` 的
            # `confirm_text="退出"` 是**向后兼容的默认值**（其 docstring 2.0.2 明说
            # "不传则用中文默认值，老调用点行为不变"），调用方经 `t()` 传词条 ⇒ **不是缺陷**。
            # 用 body 首末语句的行号切出（`get_source_segment(node)` 会把签名一起带上）。
            first = min(getattr(s, "lineno", 1) for s in node.body)
            lasts = [getattr(s, "end_lineno", None) or getattr(s, "lineno", None)
                     for s in node.body]
            last = max(x for x in lasts if x) if any(lasts) else first
            body = "\n".join(lines[first - 1:last])
            if "tk.Toplevel" not in body:
                continue
            hit = _TK_TEXT_CN.search(body)
            if hit and "translate_tree(" not in body:
                problems.append("%s:%d %s() 控件文案写死中文字面量且无 translate_tree()（例：%s）"
                                % (rel, node.lineno, node.name, hit.group(1)[:24]))
            if re.search(r"\.title\(\s*APP_NAME\s*\)", body):
                problems.append("%s:%d %s() 的 title() 用裸 APP_NAME（不随语言变）"
                                % (rel, node.lineno, node.name))
    return (not problems), ("；".join(problems) if problems else "自建 Tk 框的中文字面量均有本地化通道")


_DESTRUCTIVE_KW = ("kill", "terminate", "stop_", "stop(", "rmtree", "unlink", "remove", "delete")


@check("C-49", "FAIL", "破坏性动作的守卫探测：探测自身失败不得判为「不健康」（#45/§D3.2）")
def c49(c: Ctx):
    """#45：ocx `probe_target` 的 `except Exception: pass` + 末尾无条件 `return False`，
    而它的返回值被用来决定 `kill_target_procs`（**杀用户正在用的那条隧道**）。
    ⇒ 探测**自身**出毛病（ssh 缺失 / 超时）＝"拆用户的东西"，与 §D3.2
    （守卫自身失败要**放行**）正好相反。§4.1.31 立的通用纪律，本条是它的机械形态。

    **三条件同时满足才报**（缺一条都会噪声化）：
      ① 函数里有 `except` 分支，且该分支**不重新抛出**；
      ② 该分支的"失败结果"是 `False` —— 分支内直接 `return False`，或分支不 return
         而函数**末尾**是 `return False`（失败被折叠成"假"）；
      ③ 函数名出现在 `if not <name>(` / `if <name>(…) is False` 的**守卫位置**，
         且该守卫体内含**破坏性动词**（kill/terminate/rmtree/unlink/remove/delete…）。

    ⇒ 修法只有两种：**失败侧返回 True（放行）**，或**失败侧不触发该动作**。
    判别样本见自证腿：`except: return True` ⇒ 不报；动作改成只记一行日志 ⇒ 不报。
    """
    problems = []
    for p in c.py_files():
        src = c.read(p)
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        rel = p.relative_to(c.dir).as_posix()
        lines = src.splitlines()
        guarded = set()
        for node in ast.walk(tree):
            if not isinstance(node, ast.If):
                continue
            seg = (ast.get_source_segment(src, node) or "").lower()
            if not any(k in seg for k in _DESTRUCTIVE_KW):
                continue
            test = node.test
            call = None
            if isinstance(test, ast.UnaryOp) and isinstance(test.op, ast.Not):
                if isinstance(test.operand, ast.Call):
                    call = test.operand
            elif isinstance(test, ast.Compare) and isinstance(test.left, ast.Call):
                call = test.left
            if call is not None and isinstance(call.func, ast.Name):
                guarded.add(call.func.id)
        if not guarded:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if node.name not in guarded:
                continue
            handlers = [h for h in ast.walk(node) if isinstance(h, ast.ExceptHandler)]
            if not handlers:
                continue
            # ④ 函数本身必须是**纯探测**：体内不得直接执行破坏性动作。
            #    反例（假阳性来源）：reme `_rmtree_verified` —— 它**就是那个动作**，
            #    返回值是"删除成功了吗"，`False` 是正确语义，不是"探测失败被折叠"。
            #    与 §4.1.33「别用一条会命中正常代码的规则冒充守卫」同族。
            body_seg = "\n".join(
                lines[node.lineno - 1:(getattr(node, "end_lineno", None) or node.lineno)]).lower()
            if any(k in body_seg for k in ("rmtree", "unlink", "os.remove", "shutil.move",
                                           "terminate(", "kill(")):
                continue
            tail_start = max((getattr(h, "end_lineno", 0) or 0) for h in handlers)
            tail = "\n".join(lines[tail_start:])
            tail_false = bool(re.search(r"^\s*return False\s*$", tail, re.M))
            folded = False
            for h in handlers:
                if any(isinstance(x, ast.Raise) for x in ast.walk(h)):
                    continue                       # 重新抛出 ⇒ 失败没被折叠
                rets = [x for x in ast.walk(h) if isinstance(x, ast.Return)]
                if rets:
                    if any(isinstance(x.value, ast.Constant) and x.value.value is False for x in rets):
                        folded = True              # 分支内直接 return False
                elif tail_false:
                    folded = True                  # 分支不 return，落到末尾的 return False
            if folded:
                problems.append("%s:%d %s() 被用作破坏性动作的守卫，但探测自身失败被折叠成 False"
                                % (rel, node.lineno, node.name))
    return (not problems), ("；".join(problems) if problems else "破坏性守卫的探测失败方向均为放行")


_QUIT_FUNC_NAMES = ("on_quit", "quit_app", "_decide_quit")
_DESTRUCTIVE_CALLS = ("terminate", "kill", "stop_service", "stop_process_group",
                      "force_terminate_process_tree", "terminate_process_tree",
                      "rmtree", "unlink", "remove")


@check("C-50", "FAIL", "退出路径的「未勾选」分支不得执行破坏性动作（G4.2 条款 5）")
def c50(c: Ctx):
    """G4.2 **条款 5 明文**：*退出确认弹窗提供"顺便关闭服务/隧道"勾选项，默认不勾；
    **不勾 = 服务与隧道越过托盘生命周期继续运行***。

    实测缺陷（用户报告 2026-09-20）：ocx 1.2.1 的 `on_quit` 把清理拆成
    `if stop_tunnels: kill…` **`else: 无差别 terminate 所有 OWNED 句柄`** ⇒
    **没勾选也把（自己起的）隧道关了**。
    **根因**：把条款 3 的「**作用域规则**（清理谁：只清接入实例、禁全量签名击杀）」
    当成了「**触发条件**（要不要清）」——条款 5 管要不要、条款 3 管清理谁，**分工不可互推**。
    dsh/reme 无此病：它们把两者压在同一条 `if <勾选>:` 里，`else` 只记日志。

    形态：`on_quit` / `quit_app` / `_decide_quit` 内，任一 `if` 的 **`else` 分支**
    出现破坏性调用 ⇒ 报。**判别样本**见自证腿：`else: log(...)` 放行、
    `else: proc.terminate()` 报红、`if <勾选>: kill` 本身**不报**（那是条款 5 允许的路径）。
    """
    problems = []
    for p in c.py_files():
        src = c.read(p)
        if "quit_stop" not in src:
            continue
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        rel = p.relative_to(c.dir).as_posix()
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if node.name not in _QUIT_FUNC_NAMES:
                continue
            for sub in ast.walk(node):
                if not isinstance(sub, ast.If):
                    continue
                for blk, tag in ((sub.body, "body"), (sub.orelse, "else")):
                    if tag != "else":
                        continue
                    for call in (n for stmt in blk for n in ast.walk(stmt)
                                 if isinstance(n, ast.Call)):
                        name = ""
                        if isinstance(call.func, ast.Attribute):
                            name = call.func.attr
                        elif isinstance(call.func, ast.Name):
                            name = call.func.id
                        if name in _DESTRUCTIVE_CALLS:
                            problems.append(
                                "%s:%d %s() 的 else 分支调用 %s() —— 未勾选时不得清理（G4.2-5）"
                                % (rel, getattr(sub, "lineno", 0), node.name, name))
    return (not problems), ("；".join(problems) if problems else "退出路径的未勾选分支均无破坏性动作")


@check("C-51", "FAIL", "无 UI 的退出入口（--quit）不得沿用持久化清理勾选（§4.1.43/C-41 同族）")
def c51(c: Ctx):
    """`--quit` 是**无 UI 的外部入口**（外部工具/脚本在用）：**没有任何人**被问过。

    若它沿用 `CFG["quit_stop_*"]`（那是用户在**有确认框**的语境下保存的偏好），就变成
    "**辅助机制在无人确认的情况下停掉用户正在用的服务**" —— `§4.1.43` / C-41 的母题。
    C-41 只查**降级分支**（`except` / `if x is None:`），**不覆盖这条路径**（本判据补上）。

    实测缺陷（2026-09-20 排查用户报告时发现）：reme `quit_watch_loop` 调
    `shutdown_tray(TRAY_ICON)` **不传 kwargs** ⇒ `stop_reme/stop_tunnels` 落 `None`
    ⇒ 函数内回读 `CFG["quit_stop_*"]` ⇒ **勾过一次"退出时停服务"的用户，会被一次
    外部 `--quit` 静默停掉服务**。

    形态：`quit_watch_loop` 内对 `shutdown_tray` / `on_quit` / `quit_app` 的调用，
    必须**显式**传 `stop_reme=False` 与 `stop_tunnels=False`。
    （托盘菜单那条路径不受影响：它走 `quit_app`，用户**确实被问到了**。）
    """
    problems = []
    # ⚠ **只查工具侧**（排除 `src/modules/**`）：模板 `tray_kit.quit_watch_loop` 是
    # **机制件** —— 它只 `on_quit()` 回调，**自己不读任何配置**；"要不要清"由**调用方
    # 传进来的回调**决定。把它也算进来是**假红**（判据把"回调调用点"误当成"退出入口"）。
    # 与 C-27 的 `code` 过滤同一条边界：**判据的适用范围必须自己先想清楚**（§4.1.18）。
    code = [p for p in c.py_files()
            if "template" not in p.relative_to(c.src).parts[:1]]
    for p in code:
        src = c.read(p)
        if "quit_watch_loop" not in src:
            continue
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        rel = p.relative_to(c.dir).as_posix()
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) \
                    or node.name != "quit_watch_loop":
                continue
            for call in (n for n in ast.walk(node) if isinstance(n, ast.Call)):
                if isinstance(call.func, ast.Attribute):
                    fname = call.func.attr
                elif isinstance(call.func, ast.Name):
                    fname = call.func.id
                else:
                    continue
                if fname not in ("shutdown_tray", "on_quit", "quit_app"):
                    continue
                kw = {k.arg: k.value for k in call.keywords if k.arg}
                ok = all(isinstance(kw.get(n), ast.Constant) and kw[n].value is False
                         for n in ("stop_reme", "stop_tunnels"))
                if not ok:
                    problems.append(
                        "%s:%d quit_watch_loop() 调 %s() 未显式传 stop_reme=False/"
                        "stop_tunnels=False ⇒ 会沿用持久化勾选（无人确认却停服务）"
                        % (rel, call.lineno, fname))
    return (not problems), ("；".join(problems) if problems else "无 UI 退出入口未沿用持久化勾选")


def _git_has_remote(path):
    """工具是否**有远端仓库**（= A2 T1 的触发条件"已开源发布"的可判形态）。
    返回 True / False / **None（判不了）**—— 三态，因为"非 git 仓库"不能当成"未触发"。"""
    import subprocess
    try:
        r = subprocess.run(["git", "-C", str(path), "remote"],
                           capture_output=True, text=True, timeout=15)
        if r.returncode != 0:
            return None
        return bool(r.stdout.strip())
    except Exception:
        return None


def i18n_gap(has_remote, has_i18n_dir):
    """**纯函数**（供判据与自证腿共用）：**本家族任何工具都不得缺 i18n** ⇒ True。

    **2026-09-20 口径变更（用户裁定）**：*"**默认所有工具都应该支持双语**"* ——
    不再把"是否已开源"当作开关。理由两条：
      * 四家**全部**是公开仓库 ⇒ 该触发条件对**每一家**都成立，开关实际上**恒开**；
      * 更糟的是它的**副作用**：作为开关，它给判据留了一条**豁免分支** —— C-20 遇到
        "未启用"直接放行，**没人核对那个前提**，"该有却没有"于是不红不黄（§4.1.18 同族）。
      * 本家族是**拷贝式模板**：新工具一定从模板拷出 ⇒ **默认就该带双语**，
        "没有"才是需要解释的例外。
    ⇒ 保留 `has_remote` 形参，只为让**自证腿能验证"开关语义已移除"**
      （传 False 也必须报）——它**不再参与判定**。

    **2026-09-27 W3 后段收窄**：pairs.json 重形态 grandfather 终结（reme 已迁
    轻形态 locales）⇒ 合法形态只剩 `src/template/i18n/` 目录一种。
    `has_pairs` 形参删除——它曾是"收窄前合法"的守卫，收窄后保留只会再开豁免口。
    """
    return not has_i18n_dir


@check("C-52", "FAIL", "所有工具默认必须支持双语 i18n（用户 2026-09-20 裁定：默认，不设开关）")
def c52(c: Ctx):
    """**默认要求**（用户裁定）：本家族每个工具都必须有 i18n —— 不依赖任何触发条件。

    由来（两层，都要记住）：
      1. **C-20 的豁免分支是盲区**：它遇到"未启用 i18n"直接
         `return True, "未启用 i18n（T1 未触发**或待办**）"` ⇒ **放行**，
         而**没有任何判据核对那个理由**（这个工具是否真没开源？）。
      2. **用户 2026-09-20 的裁定**：*"默认所有工具都应该支持双语"* ——
         四家全是公开仓库，"是否开源"这个开关**恒开**，留着它只会继续制造豁免角落。

    合法形态**一种**（W3 后段收窄，2026-09-27）：`src/template/i18n/` 目录（轻形态，
    词表 locales/*.json）。pairs.json 重形态 grandfather 已终结（reme 迁轻形态完成）。
    **扫描面照打**（纪律 ⑥）：没命中与没扫必须可区分。
    """
    src_i18n = c.mod_root / "i18n"
    has_dir = src_i18n.is_dir()
    remote = _git_has_remote(c.dir)      # 只为打印现场，**不参与判定**
    if i18n_gap(remote, has_dir):
        return False, ("**本家族默认要求双语，但本工具没有 i18n** —— "
                       "合法形态：`src/template/i18n/` 目录（轻形态，词表 locales/*.json）。"
                       "这不是'待办'：新工具从模板拷出即应自带。"
                       "扫描面：%s 存在=%s（有远端=%s，仅作现场信息）"
                       % (src_i18n.as_posix(), has_dir, remote))
    return True, ("i18n 在位（目录=%s）；扫描面：%s"
                  % (has_dir, src_i18n.as_posix()))


CJK = re.compile(r"[\u4e00-\u9fff]")


def _call_name(node) -> str:
    f = getattr(node, "func", None)
    if isinstance(f, ast.Attribute):
        return f.attr
    if isinstance(f, ast.Name):
        return f.id
    return ""


@check("C-20", "WARN", "启用 i18n 的工具无词表外中文（A1-10/E4-02）")
def c20(c: Ctx):
    """**2026-09-27 W3 后段口径升级**：词表 = `locales/*.json` 的 zh 值集 + t() 调用。

    旧口径"t() 调用点外不得有中文"对**数据驱动文案**（词表值存进数据表、显示时
    `t(item[...])` 统一翻译——reme 模式）全部误报：中文在数据源而非调用点。
    重形态跳过腿删除后这一口径缺陷立即显形（reme 763 处误报）。⇒ 判据精神不变
    （中文必须**可翻**），口径改为：t() 调用内的中文豁免；其余中文字面量必须
    出现在 locales zh 值集（静态可判，与运行时反查同一张表）。
    """
    if not c.has_i18n():
        return True, "未启用 i18n（T1 未触发或待办）"
    if c.entry is None:
        return True, "无入口文件"
    try:
        tree = ast.parse(c.read(c.entry))
    except SyntaxError as exc:
        return False, "入口文件语法错误: %s" % exc
    zh_values = set()
    for loc in (c.dir / "locales", c.mod_root / "i18n" / "locales"):
        zh = loc / "zh.json"
        if zh.exists():
            try:
                import json as _json
                zh_values.update(str(v) for v in _json.loads(zh.read_text(encoding="utf-8")).values())
            except Exception:
                pass
    bad = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if _call_name(node) == "t":        # i18n.t(...) / t(...) —— 正当出口
            continue
        args = list(node.args) + [k.value for k in node.keywords]
        for a in args:
            # 递归展开 BinOp("..." % x) / IfExp / f-string，否则拼出来的文案会被漏掉
            for sub in ast.walk(a):
                if isinstance(sub, ast.Constant) and isinstance(sub.value, str) \
                        and CJK.search(sub.value) and sub.value not in zh_values:
                    bad.append("%s:%d %s" % (c.entry.relative_to(c.dir).as_posix(),
                                             sub.lineno, sub.value[:60]))
    return (not bad), ("词表外中文 %d 处（词表=t() 调用 + locales zh 值集 %d 条）: %s"
                       % (len(bad), len(zh_values), " | ".join(bad[:4]))
                       if bad else "未发现词表外中文（词表=t() 调用 + locales zh 值集 %d 条）"
                       % len(zh_values))


# ---------------------------------------------------------------- C-21
def _star_copied_state(mod_dir: Path, read) -> tuple:
    """返回 (module_name, [被静态拷贝的状态名])；无风险时 module_name 为空。

    形状（已出现两例：`i18n.LANG`、`update_helper.PENDING_CMD`，**两次都静默失效**）：
      ① `__init__.py` 用 `from .<m> import *` → 包命名空间拿到一份**值拷贝**；
      ② 子模块里存在**模块级公有名**且被函数内 `global` **重绑** → 真值只改子模块那份；
      ③ 外部读 `包.名字` → 永远是导入时定格的旧值。
    """
    init = mod_dir / "__init__.py"
    py = mod_dir / f"{mod_dir.name}.py"
    if not (init.exists() and py.exists()):
        return "", []
    m = re.search(r"^\s*from\s+\.(\w+)\s+import\s+\*", read(init), re.M)
    if not m:
        return "", []
    try:
        tree = ast.parse(read(py))
    except SyntaxError:
        return "", []
    top = set()
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for tg in node.targets:
                if isinstance(tg, ast.Name) and not tg.id.startswith("_"):
                    top.add(tg.id)
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
                and not node.target.id.startswith("_"):
            top.add(node.target.id)
    rebound = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Global):
            rebound.update(n for n in node.names if not n.startswith("_"))
    return m.group(1), sorted(top & rebound)


@check("C-21", "FAIL", "包 import * 不得复制可变状态（外部读会拿到过期值）")
def c21(c: Ctx):
    """机械化"状态副本"这一形状——它已静默失效两次（i18n.LANG / update_helper.PENDING_CMD）。

    命中即说明：包门面用 `import *` 拷了状态，而子模块会用 `global` 重绑它 →
    外部读包拿到永久旧值（i18n 表现为菜单不刷新；update_helper 表现为 apply.cmd 永不拉起）。
    修法：门面只绑函数 + PEP 562 `__getattr__` 委派子模块（见两模块 2.1.1 / 1.1.0）。
    """
    mods = c.mod_root
    if not mods.is_dir():
        return True, "无 src/modules/"
    bad = []
    for d in sorted(p for p in mods.iterdir() if p.is_dir()):
        mod, names = _star_copied_state(d, c.read)
        if names:
            bad.append("%s: %s" % ((d / "__init__.py").relative_to(c.dir).as_posix(),
                                   ",".join(names)))
    return (not bad), ("会被 import * 静态拷贝的状态（外部读恒旧值）: " + "; ".join(bad)
                       if bad else "无 import * 状态复制")


# ---------------------------------------------------------------- C-22..C-24
_CONTAINERS = (ast.Dict, ast.List, ast.Set, ast.ListComp, ast.DictComp, ast.SetComp)

# --- C-22：bat/cmd 字节卫生 -------------------------------------------------
# 只扫**源**：构建产物（release/out/dist/_internal）与脚手架/缓存目录（.cache/.verify-scratch，
# 两者都在 .gitignore 里）跳过——它们不是作者手写的、也不入库，报出来只会淹没真问题。
# ⚠️ 但"生成的 bat 是 LF"这件事本身仍要记在案：恰恰是脚本写文件把 CRLF 写丢了的现场（见 J 坑）。
_BAT_SKIP_DIRS = {".git", "__pycache__", "build", "dist", "release", "out", "_internal",
                  "node_modules", ".verify-scratch", ".cache"}


def _bat_files(root: Path):
    out = []
    for p in root.rglob("*"):
        if p.suffix.lower() not in (".bat", ".cmd") or not p.is_file():
            continue
        if any(part in _BAT_SKIP_DIRS for part in p.parts):
            continue
        out.append(p)
    return sorted(out)


def _bat_hygiene(path: Path) -> list:
    """返回 [`第N行:原因`]；空列表 = 合规。判据：**CRLF / 无 0x09 / 纯 ASCII**。

    为什么是字节级而不是"看着没问题"：`write_text("...\\t...")` 会把 `\\t` 当**转义**解释，
    写进 .bat 就成了真 TAB——`"%PY%" tests<TAB>est_update_bat.py` 这种行**永远跑不起来**；
    若它前面还有别的门禁先把构建拦下，这条坏行就**永远不会暴露**（2026-09-19 reme 实例）。
    LF-only 更隐蔽：cmd 对 `for`/`goto` 行的解析在 LF 下会异常。中文则按 OEM 码页撕碎后续行。
    """
    data = path.read_bytes()
    lf_only, tabs, nonascii = [], [], []
    line = 1
    for i, b in enumerate(data):
        if b == 0x0A:
            if i == 0 or data[i - 1] != 0x0D:
                lf_only.append(line)
            line += 1
        elif b == 0x09:
            tabs.append(line)
        elif b > 0x7F and (not nonascii or nonascii[-1] != line):
            nonascii.append(line)
    bad = []
    if lf_only:
        bad.append("LF-only 行 %d 处（首见 第%d 行；必须 CRLF）" % (len(lf_only), lf_only[0]))
    if tabs:
        bad.append("含 0x09 TAB %d 处（第 %s 行）"
                   % (len(tabs), ",".join(str(n) for n in tabs[:6])))
    if nonascii:
        bad.append("非 ASCII %d 行（第 %s 行；cmd 按 OEM 码页解析）"
                   % (len(nonascii), ",".join(str(n) for n in nonascii[:6])))
    return bad


@check("C-22", "FAIL", "bat/cmd 字节卫生：CRLF + 无 TAB + 纯 ASCII（B3/J 坑）")
def c22(c: Ctx):
    """把"bat 必须 CRLF + 纯 ASCII"从口头纪律升级成**可执行判据**（逐文件逐行报位置）。

    三个判据各对应一次真实事故：TAB（转义写坏行 ⇒ 门禁从未执行）、LF-only（cmd 解析异常）、
    非 ASCII（OEM 码页撕碎后续行）。**每次新增/修改 bat 行后必须跑一次本检查自证**——
    这类损坏不会报错，只会让某行静默失效。

    ⚠️ **范围声明（2026-09-19 补，必须写在这里）**：**本条只管行尾 / TAB / ASCII 三项字节形态，
    不保证 bat 能被 cmd 解析。** 实证：helpers-dev 在 `if (...)` 块里写了一行
    `echo [ERROR] Tk runtime missing: _internal\\_tkinter.pyd (the extension module itself).`
    —— **块内的裸 `)` 会提前闭合块**，整个 bat 在"此时不应有 ."上报语法错，而本条三项全绿。
    他那句总结请照抄：**"bat 三项字节纪律管不到 bat 的语义"**。

    **为什么本检查不顺手加一条"块内裸 `)`"的启发式**（不是没想到，是**量过之后否掉**）：
    对五仓 8 个 bat 做了一次朴素扫描（`^\\s*\\)` 或行尾 `)`），命中的**全是合法的块闭合行**
    （`build.bat` 一个文件就有十几处 `  )` / `) else (`）——**行级规则没有区分力**，
    要判"这个 `)` 是不是提前闭合"必须跟踪**块嵌套 + 引号 + `^` 转义**，那是另一件事的规模。
    在它做出来之前，**别用一条会命中正常代码的规则冒充守卫**。

    **真正的守卫（正确做法，替代启发式）**：新增的 bat 块要**从文件里原样抽出、拼成探针文件、两个方向各跑一次**
    ——① 真值路径 → 应当通过；② 不存在的路径/缺件注入 → 应当**报错且 `exit /b 1`**。
    helpers-dev 这次就是靠"反向也跑一遍"把坑抓出来的：**只加断言不验"能红"，等于没加**
    （与 §D3/§J 那条"注入一个失败，必须先把'只挡住目标那一条路径'证明出来"同族）。

    ⚠️ **验证脚本必须带"对照格"（复核员自曝，lead 要求并入本条与 C-33 的说明）**：
    他只跑"**VAR 为空 → 中止**"这一格时，结论是"这个惯用法必炸"；补上"**VAR 有值 → 不该炸**"这一格，
    才发现**第一次的失败是他自己搬运上下文造成的失真**（整段守卫区段依赖前后行，抽走上下文就换了语义）。
    ⇒ **操作形式：替身/抽取必须是最小对照，且必须有反向格证明它"不该炸（或不该红）"**——
    **唯一变量法 + 对照格，两者缺一，验证脚本自己就会骗人**（与"负样本要双向：恒红也是没区分力"同一条）。
    """
    files = _bat_files(c.dir)
    if not files:
        return True, "无 .bat/.cmd（本工具用别的方式构建）"
    bad = []
    for p in files:
        for item in _bat_hygiene(p):
            bad.append("%s: %s" % (p.relative_to(c.dir).as_posix(), item))
    return (not bad), ("；".join(bad) if bad
                       else "%d 个 bat/cmd 全部 CRLF+ASCII 且无 TAB" % len(files))




def _is_container(node) -> bool:
    if isinstance(node, _CONTAINERS):
        return True
    if isinstance(node, ast.Call):
        fn = node.func
        name = fn.id if isinstance(fn, ast.Name) else (
            fn.attr if isinstance(fn, ast.Attribute) else "")
        return name in {"dict", "list", "set", "defaultdict", "OrderedDict", "deque"}
    return False


def _rebound_state(py_path: Path, read) -> list:
    """返回 [`名字:行号(形态)`]：模块级公有名被函数内 `global` **重绑**。

    这正是两次静默失效的形状（`i18n.LANG`、`update_helper.PENDING_CMD`）：
    `global` 重绑 = 换了一个对象/值，而**导入方手里的引用不会跟着变**
    （`import *` 拷的是对象引用，标量更是直接拷值）⇒ 外部读到的是死副本。
    **就地修改**（`d.update(...)` / `d["k"]=v`）不受影响——那两条路是 STANDARDS §D6 认可的：
    容器就地改，或经访问器暴露。容器**重绑**同样在禁列（与标量同理），故两类都报、分别标注。
    """
    try:
        tree = ast.parse(read(py_path))
    except SyntaxError:
        return []
    kinds = {}
    for node in tree.body:
        targets = []
        if isinstance(node, ast.Assign):
            targets = [t for t in node.targets if isinstance(t, ast.Name)]
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            targets = [node.target]
        for tg in targets:
            if not tg.id.startswith("_"):
                kinds[tg.id] = ("容器重绑" if _is_container(node.value) else "标量", node.lineno)
    rebound = {n for node in ast.walk(tree) if isinstance(node, ast.Global)
               for n in node.names}
    return ["%s:%d(%s)" % (n, kinds[n][1], kinds[n][0]) for n in sorted(rebound & set(kinds))]


@check("C-23", "WARN", "模块级状态不得被 global 重绑（外部读会拿到死副本，STANDARDS §D6）")
def c23(c: Ctx):
    """C-21 的**前一层**：C-21 查"已经坏了"（`import *` 真的拷了状态），本条查**脆形态**——
    状态写成模块级名字、由函数 `global` 重绑。这样写今天可能没事（门面若用 `__getattr__`
    委派就挡住了），但任何人把 `import *` 加回来就静默复发。

    正路只有两条（§D6）：**可变容器就地改**（`d.update()` / `d[k]=v`），或**经访问器暴露**。
    """
    mods = c.mod_root
    if not mods.is_dir():
        return True, "无 src/modules/"
    bad = []
    for p in sorted(mods.rglob("*.py")):
        if p.name == "__init__.py":
            continue
        for hit in _rebound_state(p, c.read):
            bad.append("%s: %s" % (p.relative_to(c.dir).as_posix(), hit))
    return (not bad), ("模块级状态被 global 重绑（改为容器就地改/访问器）: " + "; ".join(bad)
                       if bad else "无 global 重绑的模块级状态")


# ⚠️ 参数表用 `[^)]*`，**不能**用 `.*?\):`：带返回注解的签名（`def f() -> tuple:`）里没有
# 紧跟的 `):`，非贪婪展开会一路吞到别处的 `):`，于是"签名体"取到的是**另一个函数**——
# 实测把 reme 的 `tray_signature` 误判成不含 HELPER_UPDATE_STATE（假红灯）。
_SIG_DEF = re.compile(r"^def (\w*signature\w*)\s*\([^)]*\)[^:\n]*:(.*?)(?=^\S|\Z)", re.M | re.S)
_MENU_KW = re.compile(r"(?:enabled|checked|visible|default)\s*=\s*(.+)")


def _menu_state_tokens(text: str, read) -> list:
    """菜单动态项里引用的**模块级容器**名（如 `CFG` / `HELPER_UPDATE_STATE`）。

    刻意**只认容器**：函数式读取（`service_is_healthy()`）与类属性状态由各自的重画路径负责，
    本检查看不到，也就不硬判（宁可窄、不可误报——误报会让人不再信任工具，见文件头纪律①）。
    """
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    containers = set()
    for node in tree.body:
        if isinstance(node, ast.Assign) and _is_container(node.value):
            containers.update(t.id for t in node.targets if isinstance(t, ast.Name))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) \
                and node.value is not None and _is_container(node.value):
            containers.add(node.target.id)
    if not containers:
        return []
    used = set()
    for line in text.splitlines():
        m = _MENU_KW.search(line)
        if not m:
            continue
        used.update(n for n in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", m.group(1)) if n in containers)
    return sorted(used)


@check("C-24", "WARN", "驱动托盘菜单的状态必须进入菜单签名（E2-09/§D6）")
def c24(c: Ctx):
    """菜单只在**签名变化**时重画；签名漏掉某个状态 ⇒ 该状态变了菜单也不刷新。

    reme 已实测踩过（`tray_signature()` 原先不含更新状态 ⇒ 后台查到新版后「下载并更新」
    不亮，2026-09-19 修）。本条只管**模块级容器**这一种载体（高置信）：容器在菜单项里被读、
    却不进签名 → 报。函数式读取与类属性状态不在范围内（见 `_menu_state_tokens` 的说明）。
    """
    menu_files = [p for p in c.py_files() if "MenuItem(" in c.read(p)]
    if not menu_files:
        return True, "未见托盘菜单（无 MenuItem(）"
    problems, checked = [], 0
    for p in menu_files:
        text = c.read(p)
        m = _SIG_DEF.search(text)
        has_sigobj = "MenuSignature(" in text
        tokens = _menu_state_tokens(text, c.read)
        if not m and not has_sigobj:
            problems.append("%s 有菜单但无签名函数/MenuSignature（状态变了不会重画）"
                            % p.relative_to(c.dir).as_posix())
            continue
        if not tokens:
            checked += 1
            continue
        body = (m.group(2) if m else text)
        missing = [t for t in tokens if t not in body]
        if missing:
            problems.append("%s: 菜单读了 %s 但签名不含它"
                            % (p.relative_to(c.dir).as_posix(), ",".join(missing)))
        checked += 1
    return (not problems), ("；".join(problems) if problems
                            else "签名覆盖菜单容器状态（受检文件 %d）" % checked)


# ---------------------------------------------------------------- C-25..C-27
# 三条都来自 2026-09-19 当天暴露的缺陷，**现役 76 条款一条都拦不住**：
#   C-25 门禁步骤"可执行 + 可被执行"   （reme build.bat:201 被 TAB 写坏 ⇒ 该步从未执行）
#   C-26 外部程序"成功"必须含正向要求   （robocopy rc=0 = 没复制也没出错 ⇒ 空 STAGE 被判成功）
#   C-27 采纳 = 拷贝 + 接线             （dsh/ocx 拷了 update_helper，README 承诺的调用零引用）
_PATHISH = re.compile(r"[A-Za-z0-9_%~.\\/-]+\.(?:py|bat|cmd)\b")


def _bat_invocations(path: Path):
    """返回 [(行号, 相对路径)]：bat 里**以脚本文件为参数**的调用（注释行不算）。

    只认不含 `%` 的路径字面量——带变量的（例如以 `%RELEASE_DIR%` 开头的）解析不了，不硬判。
    """
    out = []
    for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        s = line.strip()
        if not s or s.lower().startswith(("rem ", "rem\t", "::")):
            continue
        for tok in _PATHISH.findall(s):
            if "%" in tok or "~" in tok or tok.startswith(("-", "/", "\\")):
                continue
            # 只认**看起来是路径**的（带分隔符）：`dsh.cmd` / `appconfig.py` 这类裸文件名
            # 是当参数或当命令用的，是否存在由 PATH/调用方决定，不硬判（首版实测的误报）。
            if "\\" not in tok and "/" not in tok:
                continue
            out.append((i, tok.strip('"\'')))
    return out


@check("C-25", "FAIL", "门禁步骤必须既存在又能被执行（D1-05/J 坑）")
def c25(c: Ctx):
    """两步都要过：**(a) 被调用的路径在磁盘存在**；**(b) 该步不在死代码里**。

    反面教材（2026-09-19）：`reme/scripts/build.bat:201` 被写成
    `"%PY%" tests<TAB>est_update_bat.py` —— 转义把文件名撕开，**整行测试门禁从未执行过**；
    又因 D1-01 排在它前面，即使不修也永远不暴露。**"写了"不等于"跑了"**。
    """
    files = [p for p in _bat_files(c.dir)
             if p.name.lower() in ("build.bat", "release.bat", "run.bat", "clean.bat")]
    if not files:
        return True, "无 build/release bat"
    missing, dead = [], []
    for p in files:
        lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        # 死代码判定：**顶层无条件**的 `exit /b` / `goto :eof` 之后、下一个标签之前的调用。
        # ⚠️ 括号块内（`if errorlevel 1 ( ... exit /b 1 )`）与 `if ... exit /b` 都是**条件**出口，
        # 成功路径根本不走——把它们当无条件会把每个工具的正常门禁全误报成"死代码"（首版实测）。
        terminated, depth = False, 0
        for i, line in enumerate(lines, 1):
            s = line.strip()
            if s.startswith(":"):
                terminated = False
            elif depth == 0 and not s.lower().startswith("if ") \
                    and re.match(r"^(exit\s+/b|goto\s+:eof)", s, re.I):
                terminated = True
            elif terminated and s and not s.lower().startswith(("rem", "::", ")")):
                for tok in _PATHISH.findall(s):
                    if "%" not in tok:
                        dead.append("%s:%d %s（前有顶层 exit/goto :eof，永不执行）"
                                    % (p.relative_to(c.dir).as_posix(), i, tok))
            depth = max(0, depth + s.count("(") - s.count(")"))
        for lineno, rel in _bat_invocations(p):
            if Path(rel).is_absolute():
                continue
            # 家族约定：模板库与工具**同级**，跨仓引用（`..\my-diy-tool-template\x.py`）
            # 要按"工具的父目录"再找一遍——首版只找工具内，把正常的 sync 门禁误报成缺失。
            cands = [p.parent / rel, c.dir / rel, c.dir.parent / rel]
            if not any(x.exists() for x in cands):
                missing.append("%s:%d %s" % (p.relative_to(c.dir).as_posix(), lineno, rel))
    bad = missing + dead
    return (not bad), ("；".join(bad[:6]) if bad
                       else "%d 个 bat 的步骤调用都在磁盘上且不在死代码里" % len(files))


_START_WITH_PATH = re.compile(r'^\s*start\s+"[^"]*"\s+"(?P<path>[^"]+)"', re.I | re.M)


@check("C-26", "FAIL", "start 前必须存在性守卫：外部程序的\"成功\"不能只靠排除失败码（J 坑）")
def c26(c: Ctx):
    """`robocopy` 的 `rc=0` 意为**没有任何文件被复制、也没出错**——所以"只排除 >=8"会把
    **空/损坏的暂存包判成成功**，随后 `start` 指向不存在的 exe ⇒ Windows"找不到文件"
    **模态框**（`DETACHED_PROCESS` 挡不住，GUI 子系统）⇒ 脚本永久阻塞。

    判据：每一条 `start "" "<路径>"` 都必须有存在性守卫——同行 `if exist "<路径>"`
    或更早的 `if not exist "<路径>" goto …`。**负向排除 ≠ 成功，必须额外校验目标产物存在。**

    ⚠️ **同时扫 `.py`**：更新链的 bat 是**渲染生成**的，模板本体是 Python 里的字符串
    （模板 `update_helper._APPLY_BAT`、l-s2t `updater.py` 的 apply 模板）——只扫 `.bat`
    等于把真正的现场漏掉（首版实测：四个工具全报"无 start 调用"）。
    """
    bad, checked = [], 0
    sources = list(_bat_files(c.dir)) + [p for p in c.py_files()]
    for p in sources:
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in _START_WITH_PATH.finditer(text):
            target = m.group("path")
            if "%" in target:
                continue
            checked += 1
            lineno = text[:m.start()].count("\n") + 1
            line = text.splitlines()[lineno - 1]
            earlier = "\n".join(text.splitlines()[:lineno - 1])
            inline = re.search(r'if\s+exist\s+"%s"' % re.escape(target), line, re.I)
            before = re.search(r'if\s+not\s+exist\s+"%s"' % re.escape(target), earlier, re.I)
            if not (inline or before):
                bad.append("%s:%d start 指向 %s，但**没有任何存在性守卫**"
                           % (p.relative_to(c.dir).as_posix(), lineno, target))
    return (not bad), ("；".join(bad) if bad
                       else "%d 处 start 都有存在性守卫" % checked if checked
                       else "无 start 调用")


_MUST_WIRE = re.compile(r"<!--\s*MUST-WIRE:\s*([A-Za-z_][A-Za-z0-9_]*)\s*-->")


@check("C-27", "FAIL", "模块采纳 = 拷贝 + 接线：README 声明的必接符号须在代码里被引用（B4/D14）")
def c27(c: Ctx):
    """**`sync_check` 的模块 `[ok]` 只证明"拷全了"，不证明"接上了"**。

    反面教材（2026-09-19）：dsh/ocx 把 `update_helper` 三件拷到位（哈希全绿），但
    `sweep_stale_update_dirs` / `pop_failed_update_note` 在 `src/` 下**只出现在被拷进去的
    README 里，代码零引用** —— README 承诺的两件事一件都没发生（失败通知永不触发、%TEMP%
    残留越积越多），而所有机械检查都是绿的。**SAME ≠ 在役。**

    机制：模块 README 用 `<!-- MUST-WIRE: symbol -->` 声明"启动/退出时必须调用"的入口；
    检查器在**工具代码**（`src/**/*.py`，排除 `src/modules/**` 的拷贝本体与 `__init__.py`
    的转发导出）里找引用；找不到即报。
    """
    mods = c.mod_root
    if not mods.is_dir():
        return True, "无 src/modules/"
    code = [p for p in c.py_files()
            if "template" not in p.relative_to(c.src).parts[:1]
            and p.name != "__init__.py"]
    bad, declared = [], 0
    for d in sorted(x for x in mods.iterdir() if x.is_dir()):
        # **已申报"有意不接入"的模块不查**（2026-09-19 P5 批次）：`NOT-WIRED.md` 是
        # sync_check 的申报口（§4.1.48），语义就是"本工具**不采纳**这个模块"——那它的
        # README 承诺的接线当然不成立。旧实现不认它 ⇒ 把"如实申报"报成 FAIL（假红）：
        # l-s2t/reme 各报一条 `update_helper 声明必接 … 零引用`，而它们恰恰是**刚申报完**的。
        if (d / "NOT-WIRED.md").exists():
            continue
        # 声明取**模板正本**（`TEMPLATE_DIR/modules/<m>/README.md`）优先：要求是模块的属性，
        # 不该等工具把带锚点的 README 拷过去之后才生效——否则锚点加上当天所有工具都"无声明"，
        # 检查空转（首版实测）。工具侧 README 也读，兼容工具自己追加的声明。
        readmes = [p for p in (TEMPLATE_DIR / "template" / d.name / "README.md",
                               d / "README.md") if p.exists()]
        syms = sorted({s for r in readmes for s in _MUST_WIRE.findall(c.read(r))})
        for sym in syms:
            declared += 1
            if not any(re.search(r"\b%s\b" % re.escape(sym), c.read(p)) for p in code):
                bad.append("%s 声明必接 %s，但工具代码里零引用" % (d.name, sym))
    if not declared:
        return True, "无 MUST-WIRE 声明"
    return (not bad), ("；".join(bad) if bad else "%d 个必接符号都已接线" % declared)


# ---------------------------------------------------------------- C-28
def check_md_tabs(root: Path):
    """`root` 下所有手写 `.md` 不得含 0x09 TAB。返回 `(ok, detail)`。

    **普通助手函数，不要加 `@check`**——它收的是 `Path`，不是 `Ctx`（我先前的重构
    把装饰器留在了它头上，于是每个工具都收到 `Ctx` → `AttributeError`，四条 WARN
    全是"检查异常"）。注册点只有下面 `c28` 与模板侧的 `c28_template` 两处。
    """
    bad = []
    for p in sorted(root.rglob("*.md")):
        if any(part in _BAT_SKIP_DIRS for part in p.parts):
            continue
        data = p.read_bytes()
        if b"\x09" not in data:
            continue
        lines = [i for i, ln in enumerate(data.split(b"\n"), 1) if b"\x09" in ln]
        bad.append("%s: TAB 行 %d 处（第 %s 行）"
                   % (p.relative_to(root).as_posix(), len(lines),
                      ",".join(str(n) for n in lines[:5])))
    return (not bad), ("；".join(bad) if bad else "手写文档无 TAB")


# ---------------------------------------------------------------- C-38
# "生产者自我标识"：把一条**无法机械检查的纪律**换成一条**可判的性质**。
# 由来（2026-09-19，复核员定死 3 个无点 tmp 目录的生产者）：那些残留出自 `python -c` /
# heredoc 探针——**从不落盘**，所以任何"扫源码"的原理都覆盖不到。最后能定死归属，靠的是
# **残留自带的那行日志**（`config seeded: <仓库出厂> -> …\<残留>\…`）：源是仓库而不是
# 用户 AppData，一眼就能分辨"导入式探针"与"托盘实例"。
# ⇒ **把归属依据写进产物自己**，比任何外部扫描都强。
_SELF_ID_NAMES = ("USER_DATA_DIR", "CONFIG_PATH")
# **一次性行不得计入自证**（2026-09-19，lead 依复核员的实测裁定）：
# `config seeded:` / `config migrated:` 只在**数据根首次播种/迁移**时出现——也就是说，
# **能解决归属的那条日志，按构造永远不会在第二次启动时出现**。复核员的实测（读真实日志）：
# reme 6757 行里只有 2 行含数据根（首现在 **#770**，09-13）；dsh 92 行 1 行（**#0**，09-18）；
# ocx 145 行 1 行（**#0**）；**l-s2t 284 行 0 行**。dsh/ocx 的"绿"正来自那次一次性
# `config migrated:` ⇒ **绿得不是地方，比红更坏**（它会让人以为这条性质已经被满足）。
_SELF_ID_ONESHOT = ("config seeded", "config migrated")
# 锚 = **启动那一条日志**：`log(...)`/`print(...)` 的**第一个字符串实参以 `startup` 开头**
# （家族现行写法 `log("startup %s v%s (pid %s)" % ...)`）。**不能**用"行里含 startup"——
# 那样 `log("dsh process exited during startup: …")` 这种**错误提示**也会变成锚（实测踩到）。
# 2026-09-20 修盲区（§4.1.60）：锚原来只认 `log(` / `print(`，而 **ocx 的本地日志包装叫
# `_log(`** ⇒ `_` 属 `\w`、前面的 `(?:^|\W)` 不成立 ⇒ **`_log` 永不命中**，ocx 恒报
# 「锚 0 处」。R1 §3 T6 曾把这条归因成"ocx 措辞不对（用了 starting 不是 startup）"——
# **归因错了一半**：措辞改了之后锚仍不命中，真因是**判据只认一种包装名**。
# 修法：接受可选下划线前缀（本家族现役两种形态 `log` / `_log`）；
# **不用 `\w*log`**——那会把 `catalog(` 也当成日志调用。
_SELF_ID_ANCHOR = re.compile(r"""(?i)(?:^|\W)(?:_?log|print)\s*\(\s*f?["']\s*startup\b""")
_SELF_ID_WINDOW = 20


def _self_id_window(source_text: str):
    """在**已掩码**的源码文本上判"启动自证"。

    规则（lead 2026-09-19 定的形态，替代原来的"文件前 N 行 / 全文任意处"）：
      ① **锚在 `startup` 那条日志行**，数据根/配置路径必须出现在**它之后 `_SELF_ID_WINDOW` 行内**
         ——**不看文件前 N 行**：追加/轮转日志的**前 N 行是最老的**，看它等于回看历史；
      ② **一次性行（`config seeded:` / `config migrated:`）不计入**。
    返回 `(ok_or_None, detail, hits)`；`None` = 判不了（没有锚行）。
    """
    lines = source_text.splitlines()
    anchors = [i for i, ln in enumerate(lines) if _SELF_ID_ANCHOR.search(ln)]
    if not anchors:
        return None, "**判不了**：找不到 `startup` 日志行（本条判据锚在它上面）", [], []
    hits = []
    for a in anchors:
        for j in range(a + 1, min(a + 1 + _SELF_ID_WINDOW, len(lines))):
            ln = lines[j]
            if "log(" not in ln and "print(" not in ln:
                continue
            if any(n in ln for n in _SELF_ID_NAMES):
                if any(one in ln for one in _SELF_ID_ONESHOT):
                    continue          # 一次性行：不算自证
                hits.append((a + 1, j + 1, ln.strip()))
    # **锚也要交出来**（纪律 ⑥：读数自带分母）：锚认错了（例如把 `startup update check:`
    # 这种周期性检查行当成启动标记）必须**看得见**，否则"判红的理由"本身无法被复核。
    anchor_list = [(i + 1, lines[i].strip()[:60]) for i in anchors]
    return bool(hits), "", hits, anchor_list


def _self_identifying(root: Path):
    """工具 `src/**/*.py` 里是否**在 `startup` 行之后**把数据根/配置路径打进日志。

    返回 `(ok_or_None, detail, [(相对路径, 锚行, 命中行, 行内容)])`；`None` = 判不了。
    模板 `paths.py` 的**副本**也在 `src/modules/paths/` 下，所以"在模板里加一行"对四家同时生效。
    ⚠️ 文本先经 `_masked_code_text`：**散文不算**（§4.1.37 / 设计纪律 ⑨）——工具源码里
    docstring 引用 `USER_DATA_DIR` 是很自然的写法，不掩码就会假绿。
    """
    src = root / "src"
    if not src.is_dir():
        return None, "无 src/（判据不适用）", [], []
    if not (src / "main.py").exists() and not list(src.glob("*.py")):
        return None, "src/ 下没有 .py（判据不适用）", [], []
    hits = []
    anchors = []
    judged = 0
    for f in sorted(src.rglob("*.py")):
        try:
            text = _masked_code_text(f.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
        ok, why, found, found_anchors = _self_id_window(text)
        if ok is None:
            continue
        judged += 1
        rel = f.relative_to(root).as_posix()
        for a, j, line in found:
            hits.append((rel, a, j, line))
        for ln_no, ln_txt in found_anchors:
            anchors.append((rel, ln_no, ln_txt))
    if not judged:
        return None, "扫描面内没有可判的 `startup` 锚行", [], []
    return bool(hits), "", hits, anchors


@check("C-38", "WARN", "启动自证：`startup` 行之后必须能看到解析后的数据根 / 配置文件路径")
def c38(c: Ctx):
    """**为什么是 WARN 而不是 FAIL**：缺它不会让用户看到任何异常，只会让**下一次残留归属
    无据可依**——而那正是本次三个 `tmp*` 目录耗掉一整轮取证的原因（它们出自 `python -c` /
    heredoc，**不落盘**，外部扫描原理上够不着）。等级由 lead 定，**2026-09-19 复核员实测后
    定为 WARN（今天四家都红，是新增缺口，不是谁写错）**。

    **形态为什么改**（lead 裁定，原形态"文件前 N 行含数据根"**按字面会假绿**）：
    ① 锚在 `startup` 行之后 N 行——**追加/轮转日志的前 N 行是最老的**；
    ② **一次性行（`config seeded:` / `config migrated:`）不计入**，并作反例样本
       ——"只有一次性 migration 行 ⇒ 判红"。
    """
    ok, why, hits, anchors = _self_identifying(c.dir)
    _span = ("扫描面：src/**/*.py；锚 = 第一个字符串实参以 `startup` 开头的 `log(`/`print(` 行，"
             "窗口 = 其后 %d 行；锚 %d 处（%s）"
             % (_SELF_ID_WINDOW, len(anchors),
                ", ".join("%s:%d" % (a[0], a[1]) for a in anchors[:3]) or "无"))
    if ok is None:
        # **判不了也要 WARN，不能报 ok**（lead："绿得不是地方，比红更坏"；设计纪律 ⑧ 要求
        # 不可判必须打印"判不了 + 为什么"）。这一格今天真实发生：ocx 源码里**根本没有**
        # `log("startup …")` 这条启动标记 ⇒ 既无法定锚，也说明它**没有任何启动自证**。
        return False, (_span + "；%s。⇒ 这一格**不可判**，但按 WARN 报（不是通过）："
                       "判据锚在 `startup` 启动标记上，没有标记就既定不了锚、也谈不上自证——"
                       "**缺启动日志本身就是缺口**（第一次启动/第二次启动都无法归属）。"
                       "【正确形态】启动早期 `log(\"startup <名字> v<版本> (pid <pid>)\")`，"
                       "**紧跟着**一行写出解析后的 `USER_DATA_DIR` 与 `CONFIG_PATH`" % why)
    if ok:
        return True, (_span + "；命中 %d 处（%s）"
                      % (len(hits),
                         ", ".join("%s:%d→:%d" % (h[0], h[1], h[2]) for h in hits[:3])))
    return False, (_span + "；**该窗口内 0 处**把数据根/配置路径写进日志的行。"
                   "【为什么锚在 startup 而不看文件前 N 行】追加/轮转日志的**前 N 行是最老的**；"
                   "且 `config seeded:` / `config migrated:` 这类**一次性行不得计入**——"
                   "复核员实测：dsh/ocx 今天的\"有\"正来自一次性的 `config migrated:`，**绿得不是地方**。"
                   "【为什么值得做】`python -c`/heredoc 探针**不落盘**，源码扫描原理上覆盖不到它们；"
                   "能定死归属的只有**产物自带的那行日志**。"
                   "【正确形态】`startup` 那一行之后紧跟一行，写出 `USER_DATA_DIR` 与 `CONFIG_PATH` 的"
                   "**解析结果**（不是常量、不是假设值）")


@check("C-28", "WARN", "本仓 .md 不得含 0x09 TAB（只扫手写中文文档）")
def c28(c: Ctx):
    """**只扫 `.md`，WARN 级**——误报成本低，但能覆盖一类真实事故。

    背景：写 CHANGELOG 时用 Python 字符串拼内容，`"\\t"` 被当成**转义**，于是文件里落进一个
    **真 TAB**（2026-09-19 本人实例）。bat 有 C-22 管，`.py` 的 TAB 是缩进（合法）、`.json`
    里也可能是合法转义——所以**只挑 `.md`**：本仓的 `.md` 全是手写中文文档，TAB 没有任何
    正当用途。lead 裁定：不扩到所有文本文件，但这一条值得有。

    **最刺眼的一次**（lead 原话留档）：C-28 的规则文本自己那条 CHANGELOG 里就落进了**两个真
    TAB**——作者想写两字符的 `` `\\t` ``，写进去的是真 TAB，**且 `HEAD`（`188bbcc`）上就已存在**。
    **"描述这个坑的文档，本身踩了这个坑"**。已用显式字节值改回两字符（非转义写法），并回读确认。
    """
    return check_md_tabs(c.dir)


@template_check("C-28", "WARN", "模板仓 .md 不得含 0x09 TAB（同一判据；模板只跑一次）")
def c28_template(c: Ctx):
    """模板正本也扫一遍——修 §4.1.18 的盲区（**判据存在 ≠ 被检查对象在范围内**）。

    此前模板仓被 `main()` 的 `d.name not in {..., TEMPLATE_DIR.name}` **显式排除**，于是
    **模板自己的 `.md` 从未被 C-28 扫过**，而模板正是四份副本之源。lead 裁定用"最省事形态"：
    只让 C-28 额外扫模板仓、只报一次（不为此给模板开整轮——它没有 `src/` + `build.bat`，
    整轮会在它身上空转甚至误报）。
    """
    return check_md_tabs(c.dir)


# ---------------------------------------------------------------- C-29
_LOG_DEF = re.compile(r"^[ \t]*def\s+(log|_log)\s*\(([^)]*)\)", re.M)
_LOG_WIRED = re.compile(r"\blog\s*=\s*([A-Za-z_]\w*)")


@check("C-29", "FAIL", "交给模板件的日志函数必须接受可变参数（print 形态）")
def c29(c: Ctx):
    """**"替身比真实实现更宽容"会盖住契约冲突**——本条是它的机械落地。

    根因（2026-09-19 定）：`update_helper` 全文 7 处按 print 形态调用
    （`log("downloading", stem)`、`log("update staged:", staged, "->", target, "(bat %s)" % s)`），
    而 `log_kit.make_logger` 1.0.2 给的是**单参闭包** `log(message)`。

    **为什么一直没炸**：dsh / ocx 各自在工具侧写了 `def log(*parts)` 把它兜住（两处都留了
    "模板 log_kit 待统一"的注释），l-s2t 写了单参包装却照样 `log=log` 传给
    `tray_kit` / `update_helper` —— **冲突被三份互不相同的本地包装分别盖住或藏住**，
    模板层面于是长期保持"两个派发件说不同的话"。

    判据：工具代码里出现 `log=<name>`（把函数交给模板件），而该 `<name>` 在**工具代码内**
    的定义是单参、没有 `*args`/`*parts` → 报，并点名定义处与第一处传参点。

    **✅ 合规正例（写在最前，防后人误伤）**：**工具侧自建 `def log(*parts)` 包装是正确做法，
    不是要消灭的偏差**——dsh `src/main.py:120` 与 ocx `src/main.py:80`（`def _log(*parts)`）
    就是这么写的，C-29 对它们判 `[ok]`（首跑只报 l-s2t 是对的）。判据说要消灭的是
    **"只收一个参数"**的包装，不是"自己写包装"这件事本身。
    `✶` 为什么要把这句写进判据说明：**判据的措辞会塑造后人的行为**——若这里只写"传给模板件的
    log 必须收可变参数"，读者很容易把它读成"凡自建包装皆偏差"，从而去"统一"掉 dsh/ocx 那种
    **本来就正确**的写法。样本 `pos_tool_side_vararg_wrapper` 专门钉住这一形态。

    不做的事（避免假红灯）：`log=` 后面的名字**不是工具内的函数定义**时**不下判**——
    例如 reme 的 `log=HELPER_UPDATE_LOG` 是**日志文件路径**（交给 bat 模板的），
    不是日志函数；拿它开火就是一句与事实相反的诊断（本文件的设计纪律 ④）。
    """
    code = [p for p in c.py_files()
            if "template" not in p.relative_to(c.src).parts[:1] and p.name != "__init__.py"]
    if not code:
        return True, "无工具代码"
    wired = {}
    for p in code:
        rel = p.relative_to(c.dir).as_posix()
        for i, line in enumerate(c.read(p).splitlines(), 1):
            for m in _LOG_WIRED.finditer(line):
                wired.setdefault(m.group(1), []).append("%s:%d" % (rel, i))
    if not wired:
        return True, "没有把日志函数交给模板件（log= 零命中）"
    defs = {}
    for p in code:
        text = c.read(p)
        for m in _LOG_DEF.finditer(text):
            name = m.group(1)
            if name in wired and name not in defs:
                defs[name] = (p.relative_to(c.dir).as_posix(),
                              text[:m.start()].count("\n") + 1, m.group(2).strip())
    if not defs:
        return True, ("log= 命中的 %d 处都不是工具内的函数定义（如日志路径常量），本条判不了"
                      % sum(len(v) for v in wired.values()))
    bad = []
    for name, (rel, lineno, params) in sorted(defs.items()):
        if "*" in params:
            continue
        bad.append("%s:%d `def %s(%s)` 只收一个参数，却由 %s 交给模板件——"
                   "模板件按 print 形态调用时（如 `log(\"downloading\", stem)`）直接 TypeError"
                   % (rel, lineno, name, params, wired[name][0]))
    if bad:
        return False, "；".join(bad)
    return True, "%d 个交给模板件的日志函数都是 print 形态（%s）" % (
        len(defs), ", ".join(sorted(defs)))


# ---------------------------------------------------------------- C-30
_RMTREE_CALL = re.compile(r"(?:shutil\.)?rmtree\s*\(\s*([A-Za-z_]\w*)")
_ASSIGN_LINE = re.compile(r"^\s*([A-Za-z_]\w*)\s*=")
_DEF_HEAD = re.compile(r"^\s*def\s+([A-Za-z_]\w*)\s*\([^)]*\)\s*:", re.M)
# 只排除**非作者手写**的目录（构建产物 / 依赖 / 缓存）。`.verify-scratch` 与
# `_verify-scratch` 都排除——探针脚本自己不该被当成工具代码。
_PY_SKIP_DIRS = {".git", "__pycache__", "build", "dist", "release", "out", "_internal",
                 "node_modules", ".verify-scratch", "_verify-scratch", ".venv", "venv",
                 "site-packages", ".cache"}

# 不可静态枚举的 mkdtemp 前缀的**登记锚点**：工具仓任意 `.py` 的模块级字面量字典，
# 键 `"<相对路径>:<行号>"`（posix 分隔符）→ 该处前缀的**等价字面量**（str 或 str 列表）。
# 判据（本条）与运行期取证（--temp-leak）**都读这张表**——否则把 prefix 改成变量
# 就能悄悄从覆盖里溜出去，那是"判据可以自己失效"的形态，比泄漏本身更糟。
_REGISTRY_NAME = "TMP_PREFIX_REGISTRY"


def _mkdtemp_producers(texts) -> set:
    """哪些**函数名**会产生 mkdtemp 根目录：`mkdtemp` 本身 + 工具自己的包装。

    l-s2t 的测试写的是 `_TMP = scratch_dir("l-s2t-startup-")`，而 `scratch_dir` 是
    `tests/_cleanup.py` 里包了 `mkdtemp` 的助手。只认 `mkdtemp` 字面量会**漏掉真实形态**
    （判据会对着真正泄漏的地方报绿灯），所以把"函数体里出现 `mkdtemp(`"的本地函数也算生产者。
    """
    producers = {"mkdtemp"}
    for text in texts:
        for m in _DEF_HEAD.finditer(text):
            if "mkdtemp(" in text[m.end():m.end() + 800]:
                producers.add(m.group(1))
    return producers


def _mkdtemp_roots(text, producers) -> set:
    """本文件里哪些**变量**是 mkdtemp 根目录。

    必须按"赋值语句右侧含不含 mkdtemp"判定，而不是只认 `X = mkdtemp(...)` 这一种写法：
    reme 的测试是 `root = Path(tempfile.mkdtemp(prefix="reme-update-bat-"))`——
    外面套了 `Path(...)`。**只认裸调用会让最需要检查的文件报"本条不适用"**
    （2026-09-19 真实树首跑实测：reme 就是这样被漏掉的）。
    """
    lines = text.splitlines()
    roots = set()
    for i, line in enumerate(lines):
        m = _ASSIGN_LINE.match(line)
        if not m:
            continue
        # 右侧可能续行：把本行 + 后两行拼起来看
        rhs = " ".join(lines[i:i + 3])
        if "mkdtemp(" in rhs or any(p + "(" in rhs for p in producers if p != "mkdtemp"):
            roots.add(m.group(1))
    return roots


def _is_mkdtemp_call(node) -> bool:
    if not isinstance(node, ast.Call):
        return False
    f = node.func
    return getattr(f, "attr", "") == "mkdtemp" or getattr(f, "id", "") == "mkdtemp"


def _module_constants(trees) -> dict:
    """模块级**字面量字符串常量**表 `{名字: 值}`（同名冲突则丢弃，宁缺勿猜）。

    这是"低成本第二路径"（lead 2026-09-19 裁定）：`APP_ID = "reme-helper"` 之后
    `mkdtemp(prefix=f"{APP_ID}-update-")` 其实**推得出**，不必逼作者去写登记表。
    只认模块级 `NAME = "字面量"`（含带注释的类型注解形态），不做任何运行期求值。
    """
    vals, unstable = {}, set()
    for tree in trees.values():
        for n in tree.body:
            if isinstance(n, ast.Assign):
                targets = [t for t in n.targets if isinstance(t, ast.Name)]
                value = n.value
            elif isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
                targets = [n.target]
                value = n.value
            else:
                continue
            literal = value if isinstance(value, ast.Constant) and isinstance(value.value, str) else None
            for t in targets:
                # 任何"非字面量赋值"或"同名再赋不同值"都让该名字**不可折叠**（宁缺勿猜）：
                # 运行期可能被改写的值，拿来当常量就是拿假设当事实。
                if literal is None or (t.id in vals and vals[t.id] != literal.value):
                    unstable.add(t.id)
                    vals.pop(t.id, None)
                    continue
                if t.id not in unstable:
                    vals[t.id] = literal.value
    return vals


def _fold_str(node, consts):
    """把**可折叠**的表达式折成字符串字面量；折不出返回 None（不猜）。"""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        return consts.get(node.id)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = _fold_str(node.left, consts), _fold_str(node.right, consts)
        return left + right if left is not None and right is not None else None
    if isinstance(node, ast.JoinedStr):   # f-string：只折叠"常量 + 可折叠常量"两种片段
        parts = []
        for piece in node.values:
            if isinstance(piece, ast.Constant) and isinstance(piece.value, str):
                parts.append(piece.value)
            elif isinstance(piece, ast.FormattedValue):
                if piece.format_spec is not None or piece.conversion not in (-1, 115):
                    return None
                v = _fold_str(piece.value, consts)
                if v is None:
                    return None
                parts.append(v)
            else:
                return None
        return "".join(parts)
    return None


def _expr_kind(node) -> str:
    """给"推不出来的 prefix"一个人能读的原因（而不是把 AST 类名甩给人）。"""
    if isinstance(node, ast.JoinedStr):
        return "f-string 拼接"
    if isinstance(node, ast.Name):
        return "变量 `%s`" % node.id
    if isinstance(node, ast.Call):
        return "函数调用结果"
    if isinstance(node, ast.Attribute):
        return "属性取值"
    if isinstance(node, ast.BinOp):
        return "字符串运算结果"
    return type(node).__name__


def _py_files_under(root: Path):
    return sorted(p for p in root.rglob("*.py")
                  if p.is_file() and not any(part in _PY_SKIP_DIRS for part in p.parts))


def _enclosing_map(tree):
    """节点 → 最近的**外层函数**（名, 形参表, 是否方法）。

    必须按"最近外层"而不是 `ast.walk(fn)`：后者会把**内层函数**的 mkdtemp 算到外层
    的形参头上，于是"prefix 是形参"的判断会张冠李戴。
    """
    enc = {}

    def walk(node, fname, params, method):
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                ps = [a.arg for a in list(child.args.args) + list(child.args.kwonlyargs)]
                walk(child, child.name, ps, bool(ps) and ps[0] in ("self", "cls"))
            else:
                enc[id(child)] = (fname, params, method)
                walk(child, fname, params, method)

    walk(tree, None, [], False)
    return enc


def enumerate_mkdtemp_prefixes(root: Path):
    """从源码**枚举** mkdtemp 前缀（不猜命名，STANDARDS §D7 硬要求 8）+ 读登记表。

    返回 `(prefixes, opaque, registry, problems)`：
      * `prefixes` 可静态归属的前缀（字面量实参 + 包装函数调用点传的全是字面量）；
      * `opaque`   `[(站点 rel, 原因)]`——静态推不出、**必须**在登记表里登记的站点；
      * `registry` `{站点 rel: [等价前缀]}`（登记表读到的内容）；
      * `problems` 登记表自身的形态问题（非字面量 / 值读不出来 = 登记了等于没登记）。

    为什么必须从**调用点**解形参：`tests/_cleanup.py` 的 `scratch_dir(prefix)` 内部是
    `mkdtemp(prefix=prefix)`——只看这一行会报"不可枚举"，而 dsh/ocx/l-s2t **三个工具**
    的真实前缀全在调用点上写着字面量。**只看被调方，会把三家本来合格的地方全判红。**
    """
    trees, sites, calls, defs = {}, [], [], {}
    for p in _py_files_under(root):
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except (SyntaxError, OSError):
            continue
        trees[p] = tree
        enc = _enclosing_map(tree)
        for n in ast.walk(tree):
            if _is_mkdtemp_call(n):
                rel = "%s:%d" % (p.relative_to(root).as_posix(), n.lineno)
                sites.append((rel, n, enc.get(id(n), (None, [], False))))
            elif isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
                calls.append((n.func.id, n.args, {k.arg: k.value for k in n.keywords}))
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                defs[n.name] = defs.get(n.name, 0) + 1

    consts = _module_constants(trees)
    prefixes, opaque, weak, folded = set(), [], [], []
    for rel, node, (fname, params, method) in sites:
        kw = next((k for k in node.keywords if k.arg == "prefix"), None)
        if kw is None:
            # 裸 `mkdtemp()`：前缀是**系统默认值**（`tempfile.gettempprefix()`，通常 "tmp"）。
            # 它不是"推不出"，而是**推得出但很弱**——`tmp*` 会撞上大量无关临时目录，
            # 所以腿 A 里单独记，且**腿 B（形态派生）才是它的主判据**（task #43）。
            import tempfile as _tf
            pfx = _tf.gettempprefix() or "tmp"
            prefixes.add(pfx)
            weak.append((rel, pfx))
            continue
        v = kw.value
        if isinstance(v, ast.Constant) and isinstance(v.value, str) and v.value:
            prefixes.add(v.value)
            continue
        # 第二路径：**可折叠模块常量**（`f"{APP_ID}-update-"` 这类）——能折就不必登记。
        fold = _fold_str(v, consts)
        if fold:
            prefixes.add(fold)
            folded.append((rel, fold))
            continue
        resolvable = (isinstance(v, ast.Name) and fname and not method and v.id in params
                      and defs.get(fname) == 1)
        if resolvable:
            idx = params.index(v.id)
            vals, bad = [], 0
            for cname, args, kws in calls:
                if cname != fname:
                    continue
                if v.id in kws:
                    a = kws[v.id]
                elif len(args) > idx:
                    a = args[idx]
                else:
                    bad += 1
                    continue
                if isinstance(a, ast.Constant) and isinstance(a.value, str) and a.value:
                    vals.append(a.value)
                else:
                    bad += 1
            if vals and not bad:
                prefixes.update(vals)
                continue
            if not vals:
                opaque.append((rel, "`prefix` 取自 `%s()` 的形参，但全工具找不到传字面量的调用点"
                               % fname))
            else:
                opaque.append((rel, "`prefix` 取自 `%s()` 的形参，而调用点有 %d 处不是字面量"
                               % (fname, bad)))
            continue
        why = "`prefix` 无法静态归属（%s）" % _expr_kind(v)
        if method:
            why += "，且是方法形参（调用点解析不可靠）"
        opaque.append((rel, why))

    registry, problems = {}, []
    for p, tree in trees.items():
        rel_file = p.relative_to(root).as_posix()
        for n in tree.body:   # 只认**模块级**赋值
            if not (isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == _REGISTRY_NAME
                            for t in n.targets)):
                continue
            if not isinstance(n.value, ast.Dict):
                problems.append((rel_file, "`%s` 必须是**字面量字典**（键 \"相对路径:行号\" → "
                                 "等价前缀字面量），当前是%s——判据读不到它"
                                 % (_REGISTRY_NAME, _expr_kind(n.value))))
                continue
            for k, val in zip(n.value.keys, n.value.values):
                if not (isinstance(k, ast.Constant) and isinstance(k.value, str)):
                    problems.append((rel_file, "登记键不是字符串字面量"))
                    continue
                key = k.value.strip().replace("\\", "/")
                # **三栏结构是必填**（lead 2026-09-19）：白名单/登记表是**关掉覆盖**的开关，
                # 只写"等价前缀"等于只写结果、不写**它为什么可以豁免**与**什么时候过期**——
                # 一条过期登记会**静默关掉一处覆盖且没有任何症状**（同"0 命中"与"没扫"不可区分）。
                if not isinstance(val, ast.Dict):
                    problems.append((rel_file,
                                     "登记 `%s` 必须是三栏结构 "
                                     "`{\"prefix\": \"…\", \"why\": \"…\", \"reverify\": \"…\"}`"
                                     "（当前是%s）——`why` 与 `reverify` 是**必填**："
                                     "登记表是**关掉覆盖**的开关，没有这两栏就无法判断它何时过期"
                                     % (key, _expr_kind(val))))
                    continue
                fields = {}
                for fk, fv in zip(val.keys, val.values):
                    if isinstance(fk, ast.Constant) and isinstance(fk.value, str):
                        fields[fk.value] = fv
                for field in ("prefix", "why", "reverify"):
                    fv = fields.get(field)
                    if not (isinstance(fv, ast.Constant) and isinstance(fv.value, str)
                            and fv.value.strip()):
                        problems.append((rel_file, "登记 `%s` 的必填栏 `%s` 缺失或不是"
                                                   "非空字符串字面量（是%s）"
                                         % (key, field, _expr_kind(fv) if fv is not None else "缺失")))
                pv = fields.get("prefix")
                items = (pv.elts if isinstance(pv, (ast.List, ast.Tuple))
                         else ([pv] if pv is not None else []))
                got = []
                for item in items:
                    if isinstance(item, ast.Constant) and isinstance(item.value, str) and item.value:
                        got.append(item.value)
                    else:
                        problems.append((rel_file, "登记 `%s` 的 `prefix` 不是非空字符串字面量（是%s）"
                                         "——判据与 %%TEMP%% 取证都读不到，等于没登记"
                                         % (key, _expr_kind(item))))
                if got:
                    registry.setdefault(key, [])
                    registry[key] += [g for g in got if g not in registry[key]]
    return sorted(prefixes), opaque, registry, problems, weak, folded


@check("C-30", "FAIL", "mkdtemp 临时目录：前缀必须可静态归属，清理必须可验证（禁 ignore_errors 吞掉）")
def c30(c: Ctx):
    """**"删不掉"必须变成红，而不是被 `ignore_errors=True` 吞掉**（2026-09-19 实测）。

    背景：四个工具在 `%TEMP%` 积了 **133~138 个**自家前缀目录，每个里面**恰好一个文件**
    `<app>/log/<app>.log`。根因不是窗口 cwd，而是 **`log_kit` 的 FileHandler 句柄还开着**
    （Windows 拒绝删除在用文件），而 `rmtree(..., ignore_errors=True)` 把失败**静默吞掉** →
    每跑一次泄漏一个目录，**而所有门禁照旧全绿**。

    **判据刻意收窄**（避免误伤真正的 best-effort 清理——那是本条最容易做错的地方）：
      * 只盯**由 `mkdtemp` 产生的根目录**（含工具自己的包装函数，如 `scratch_dir`）；
      * 只有那个**根目录**被 `rmtree(..., ignore_errors=True)` 删时才报；
      * 删**子目录**、删固定路径、用 `_rmtree_retry` 之类**有返回值**的助手 → **不报**。

    正确形态：删前释放日志句柄（`logging.shutdown()` / 关 FileHandler）→ 删 → **回读确认不存在**
    → 不存在才算成功，失败即红。本条只否掉"吞掉失败"这一种写法，不规定必须用哪个助手。

    **本条不猜命名**（STANDARDS §D7 硬要求 8）：mkdtemp 根目录与 mkdtemp 前缀都是**从源码
    枚举**出来的（mkdtemp 调用节点 + 包装函数的**调用点**实参），**不做** `prefix="xxx"` 的
    字符串匹配——前缀怎么改、新增几个，判据自动跟着变。

    **覆盖缺口必须自己报出来**（review 2026-09-19 裁定）：源码里推不出的 prefix
    （f-string / 变量 / 无 prefix）**不许静默放过**——否则把 `prefix="reme-x-"` 改成变量
    就能从判据的覆盖里溜出去，那是"判据可以自己失效"的形态，**比泄漏本身更糟**。
    这类站点必须在 `TMP_PREFIX_REGISTRY` 登记**等价前缀**，判据与运行期取证都读它。

    **验收口径**（lead 裁定）：不是"现在 %TEMP% 是干净的"，而是**跑完门禁后实测 = 0**。
    ⚠️ 但"0"必须按时点读，不许当成永恒事实（R-EVID）：lead 在 **16:11** 那一次测量里，
    dsh 的 3 个残留目录 mtime 正是 **16:11**（门禁运行的当口）→ 当时它们是**跑门禁时产生的**，
    不是历史存量；而 tpl-keeper 在**晚些时候**用同一批前缀（19 个）复扫 `%TEMP%` 得到
    **0 命中**——**两次测量各自成立，谁都不能替对方下结论**。"清一遍就好了"之所以不成立，
    是因为它同样只是一个时点；正确的运行期断言是**增量**（跑测试前记基线 → 跑完比对新增，
    命令见 `--temp-leak-baseline`），它不依赖任何历史存量。
    """
    if not c.dir.is_dir():
        return True, "工具目录不存在"
    prefixes, opaque, registry, problems, weak, folded = enumerate_mkdtemp_prefixes(c.dir)
    bad = ["登记表 %s：%s" % (rel, why) for rel, why in problems]
    for rel, why in opaque:
        if rel not in registry:
            bad.append("%s mkdtemp %s，且未在 %s 登记等价前缀" % (rel, why, _REGISTRY_NAME))

    # 第二半：mkdtemp 根目录的删除必须可验证。**扫全工具，不只 tests/**——
    # reme `src/main.py:7405` 的 `work = Path(mkdtemp(prefix=f"..."))` 在 7409 被
    # `rmtree(work, ignore_errors=True)` 删（下载/校验失败的早退路径），是同一个缺陷的
    # 生产代码形态；只看 tests/ 会让它整个溜过去。
    # ⚠️ 文本先**掩码**（注释/docstring → 空格，长度与换行不变）：本条要报 `相对路径:行号`，
    # 所以不能用会拼掉换行的 `_code_only_text`。不掩码的代价是实测过的假红——本文件
    # `_rmtree_strict` 的 docstring **引用**了被禁写法（"本工具自己先得守 C-30"），
    # 于是**仪器在自己的合规说明上自证违规**（与 C-33 读 docstring 同族同因）。
    files = _py_files_under(c.dir)
    texts = [(p, _masked_code_text(c.read(p))) for p in files]
    producers = _mkdtemp_producers([t for _, t in texts])
    roots_total = 0
    for p, text in texts:
        roots = _mkdtemp_roots(text, producers)
        roots_total += len(roots)
        if not roots:
            continue
        rel = p.relative_to(c.dir).as_posix()
        for m in _RMTREE_CALL.finditer(text):
            if m.group(1) not in roots:
                continue
            # ignore_errors 可能写在续行上——看调用点之后 160 字符，而不是只看同一行
            if "ignore_errors" not in text[m.end():m.end() + 160]:
                continue
            bad.append("%s:%d `rmtree(%s, ignore_errors=True)` —— `%s` 是 mkdtemp 根目录"
                       % (rel, text[:m.start()].count("\n") + 1, m.group(1), m.group(1)))
    if bad:
        return False, ("；".join(bad)
                       + "。【正确形态①】前缀写字面量，或让包装函数的**每个调用点**都传字面量；"
                         "确实推不出的（如 f-string 拼 APP_ID）在 %s 登记等价前缀。"
                         "**登记值是三栏结构，`why` 与 `reverify` 是必填**（登记表是"
                         "**关掉覆盖**的开关：没写\"为什么可豁免\"与\"什么时候重验\"的条目，"
                         "过期后不会被任何人发现）——贴下面这段，别自创变体：\n"
                         "    %s = {\n"
                         "        \"src/main.py:7405\": {\n"
                         "            \"prefix\": \"reme-update-\",   # 该处前缀的等价字面量（可为列表）\n"
                         "            \"why\": \"prefix 由 f-string 拼成，APP_ID 在本文件有唯一字面量定义\",\n"
                         "            \"reverify\": \"APP_ID 改名/改成变量，或该站点行号位移时\",\n"
                         "        },\n"
                         "    }   # 键 = 站点「相对路径:行号」\n"
                         "【正确形态②】删 mkdtemp 根目录前先释放日志句柄（logging.shutdown() / "
                         "关 FileHandler），删后**回读确认目录已不存在**，失败即红"
                       % (_REGISTRY_NAME, _REGISTRY_NAME))
    if weak and not bad:
        return False, ("%d 处裸 `mkdtemp()`（前缀是系统默认 %r）——它**推得出但很弱**："
                       "按前缀取证会撞上大量无关临时目录，主判据是运行期的**形态派生腿**"
                       "（`--temp-leak` 的腿 B）。建议加家族前缀，或在 %s 登记弱前缀。位置：%s"
                       % (len(weak), weak[0][1], _REGISTRY_NAME,
                          ", ".join(r for r, _ in weak))), "WARN"
    stale = sorted(k for k in registry if k not in {r for r, _ in opaque})
    if stale:
        return False, ("前缀与清理都 ok，但 %s 里 %d 条登记**对不上任何不可枚举站点**"
                       "（行号漂移/已改回字面量？）：%s——登记表必须跟着代码走，"
                       "过期的登记等于没有覆盖" % (_REGISTRY_NAME, len(stale), ", ".join(stale))), "WARN"
    if not prefixes and not opaque:
        return True, "没有 mkdtemp 调用（本条不适用）"
    return True, ("%d 个前缀可静态归属（登记表 %d 条 / 常量折叠 %d 处），"
                  "%d 个 mkdtemp 根目录的清理可验证"
                  % (len(prefixes), len(registry), len(folded), roots_total))


# ---------------- 运行期取证 / 验收：%TEMP% 残留（**只读，两条腿**） ----------------
# 这是 C-30 的**运行期**一半：C-30 本体只做静态的"前缀可归属 + 清理可验证"，
# "%TEMP% 里还剩几个"必须现场量。
#
# **为什么必须两条腿**（2026-09-19 实测，task #43）：光靠"从源码枚举前缀"有**结构性天花板**
# ——它的覆盖上限 = 源码里出现过的 prefix 字面量。当时标定的 20 个残留里（自标定集），`icon-probe-*`、
# `smoke-proof-*`、`reme-gate-2.2.0`、`tmp0whlwvmi` 这些名字**在四个工具的源码里一个字都
# 搜不到**（有的来自裸 `mkdtemp()` 的系统默认前缀 `tmp`，有的来自**扫描范围之外**的探针脚本），
# 于是"前缀法 0 命中"与"真的没有泄漏"在输出上**完全同形**——这正是"判据可以自己假绿"。
#   腿 A（生成器派生）：源码枚举前缀 + 登记表；裸 `mkdtemp()` → 系统默认前缀（**弱前缀**）。
#   腿 B（形态派生）：**不看名字**，只看结构签名（下方 `_SHAPE_RULE`）。
# 口径要求（lead 裁定）：**必须打印扫描面**（扫描目录数 / 前缀数 / 每腿命中数）——
# "0 命中"与"没扫"必须可区分。
_TEMP_REGRESSION_20260919 = {
    "reme-helper": ["tmp.pFZVIqwEaS", "tmp.sugjQLprlQ",
                    "tmp.18X8SOMwNn", "tmp0whlwvmi", "reme-sync-2.2.0-check",
                    "reme-gate-2.2.0", "reme-neg-ctl"],
    "dsh-helper": ["icon-probe-077hxtaw", "icon-probe-hjbanmd1", "icon-probe-tlqg0adv",
                   "smoke-proof-iv0gm2p4", "smoke-proof-nl6gj9kf", "tmp2k2z1nt2"],
    "opencodex-helper": ["icon-probe-f6pwh8sm", "icon-probe-r28q2h6d",
                         "smoke-proof-4ibz3s31", "smoke-proof-a15nu1_k", "tmpq_u7g0sl"],
    "local-speak2text": ["tmp.kFj54SLt7t"],
    # 复核员对 %TEMP% 顶层**全部 43 个 `tmp*`** 做的形态普查（2026-09-19，样本量 43）：
    #   `tmp.` + 10 位 `[A-Za-z0-9]`（**带点**，总长 14）= **40 个** ⇒ GNU shell `mktemp -d`；
    #   `tmp` + 8 位 `[a-z0-9_]`（**无点**，总长 11）= **3 个** ⇒ Python `tempfile.mkdtemp()`。
    #   **关键指纹**：`tmp_8qhz_0a` 里的**下划线**——GNU `mktemp` 的字母表**不含 `_`**，Python 的**含**。
    #   ⇒ **两个种群并存**（lead 先前"只有固定名"→"加上无前缀 mkdtemp"→"全是 shell"三次表述各对一半）。
    # 下面三个**无点无前缀**样本专为这件事登记：它们同时验证**形态腿能抓到 Python 残留**、
    # **生成器腿永远抓不到**（无前缀可枚举）——比只放 shell 形态的样本更有区分力。
    "_shape_census_20260919": ["tmp0whlwvmi", "tmpigh0g540", "tmp_8qhz_0a"],
}
# 负样本回归集（2026-09-19 实测；**它证明的是"不看名字也能命中"，不是"零误报"**）：
#   * ⚠️ **这是自标定集**：规则就是拿这批名字标定出来的，再用同一条规则命中它们
#     ⇒ **循环**，不构成独立验证。独立复算由复核员给出：他**重实现**后得 **14**（16:55），
#     比当初的 20 少——差额来自时点不同（部分目录已被清掉）+ 他的日志腿口径。
#     所以此处**不得**再写"20/20 零误报"，只写"与手工标定集一致（自标定，非同源独立验证）"。
#   * `reme-helper-builddata` **已从本集移除**：它是 reme `scripts/build.bat:22` 明写的稳定
#     构建数据位（见 `TMP_DECLARED_PATHS`），**不是泄漏**——把声明过的位置算进"残留"是我
#     当时的误判（lead 转达复核员的取证后更正）。
#   * 宽松口径（`*.log` **存在**而非非空）覆盖 **20/20**；若写成"`log/*.log` **非空**"则只覆盖
#     **11/20**——漏掉的全是 log 为 0 字节的那一批（dsh 3 + ocx 5 + tmp2k2z1nt2）。**空文件/空目录
#     同样是残留**，这正是 C-30 从第一版起就坚持的口径（"清理跑过了 ≠ 清理成功了"）。
_SHAPE_RULE = ("**任意深度**存在名为 `log` 的**目录**（里面的 `*.log` 是 0 字节、甚至一个文件都没有，"
               "同样算——空目录也是残留）。**不看名字、不要求 `config.json`、不设深度上限**")

# 已声明的**稳定构建数据位**：构建脚本明写该路径、且明写不清理 ⇒ **不是漏扫残留**。
# 判"是不是泄漏"必须**靠位置 + 声明**：形态腿能认出"数据根"，但分不出"该在 %TEMP% 临时"
# 与"该按声明长期保留"（复核员对照实验：同规则扫 %LOCALAPPDATA% 命中的恰好是那 4 个**真实
# 数据根**——所以形态本身不构成"泄漏"判定，位置与声明才构成）。
# 白名单只豁免**报告与增量判定**，不改判据：这里不登记就永远红，登记了就永远有出处可查。
# ⚠️ **为什么"自动重建类"必须走白名单、而不是要求清理**（lead 2026-09-19 定）：声明过、且**下次构建会自动重建**的位置（如 reme `scripts/build.bat:22` 明写的固定路径），对它做"清理"**既不持久、又制造虚假的进展感**——看起来清干净了，下次门禁它又长出来。**正确处置是承认它是设计的一部分并登记出处**；"清理清单"只收**不该存在的残留**。
#
# ⚠️ **两条必填字段（lead 2026-09-19 定，复核员先提醒"它是**关掉覆盖**的开关"）**：
#   ① `why`     = **为什么它不算残留**（谁声明的、在哪一行）；
#   ② `reverify`= **什么情况下必须重验它**（触发条件）。
# **为什么必须两栏**：白名单条目是**唯一能让"形态腿"停止报警**的东西 ⇒
# **一条过期条目会静默地关掉一处覆盖，而且关掉之后没有任何症状**
# （与"0 命中"和"没扫"不可区分是同一个病）。所以每条都必须写出**它的失效条件**。
# **缺任一栏 = 仪器自身的表坏了** ⇒ 按 `[BROKEN]` 语义报（见 `_declared_problems`）。
def _leak_key(p) -> str:
    """跨根唯一 key = **规范化绝对路径**（任务 #64 / §4.1.55：裸名 ⇒ 多根下同名目录
    会被集合运算去重吃掉，还会让白名单"吃掉任何根下的同名目录"）。"""
    return os.path.normcase(str(Path(p).resolve()))


def _tmp_declared(name: str) -> str:
    import tempfile
    return _leak_key(Path(tempfile.gettempdir()) / name)


TMP_DECLARED_PATHS = {
    # key 从裸名 `reme-helper-builddata` 换成**全路径**（§4.1.55 的换 key 三处之一）。
    _tmp_declared("reme-helper-builddata"): {
        "why": "reme-helper/scripts/build.bat:22 "
               "`set \"REME_HELPER_DATA_DIR=%TEMP%\\reme-helper-builddata\"`"
               "（固定名、该 bat 全文无清理）⇒ 是**构建数据位**，不是残留",
        "reverify": "**该行被改动时**——路径变了、或它不再自动重建、或加了清理语句，"
                    "此条即过期（届时它退化成一处被静默关掉的覆盖）",
    },
}

# 两栏缺一即"仪器的表坏了"。返回 `[(名字, 问题描述)]`；空列表 = 表是完整的。
_REQUIRED_DECL_FIELDS = ("why", "reverify")


def _declared_problems():
    out = []
    for name, entry in sorted(TMP_DECLARED_PATHS.items()):
        if not isinstance(entry, dict):
            out.append((name, "条目不是 `{why, reverify}` 两栏结构（当前是 %s）" % type(entry).__name__))
            continue
        for field in _REQUIRED_DECL_FIELDS:
            if not str(entry.get(field, "")).strip():
                out.append((name, "缺必填栏 `%s`——白名单是**关掉覆盖**的开关，"
                                  "没有它就没法判断这条什么时候过期" % field))
        extra = set(entry) - set(_REQUIRED_DECL_FIELDS)
        if extra:
            out.append((name, "有未使用的栏：%s（要么用起来，要么删掉）" % ", ".join(sorted(extra))))
    return out


def _shape_rel(d: Path):
    """腿 B 签名 = "**隔离数据根**"的不变量 = **有一个 `log` 目录**（B3：日志一律落
    `<数据根>/log/<工具名>.log`）。返回触发路径（相对 `d`）或 `None`。

    2026-09-19 两次放宽，两次都是**先实测、再改签名**：
      ① 旧签名要求"**恰好一个子目录**"——那是标定样本的**偶然特征，不是不变量**。合成形状实测：
         `log/{config.json,app.log}` HIT；**加一个 `ui-icons/` → MISS**；**`config.json` 摆顶层 → MISS**。
      ② 旧签名还要求"`config.json` 在顶层或一层内"，且靠 `rglob("*.log")` 找 `*.log` **文件**。
         复核员报的真实残留 **`tmp.6FcrxXYxmM\\d\\local-speak2text`（3 层）只有 `log/`、没有
         `config.json`**——两种旧写法全抓不到。于是改成"**`log` 目录，任意深度**"。
    **候选口径实测（本次扫描面：顶层目录 95 个 / 条目 647）**：
      V0 现行（config(≤1层) 且 存在 `*.log`）          7 命中
      V1 「存在 `*.log` 文件（任意深度，不要 config）」  13 命中 —— 多出的 6 个里 5 个是**他程序的日志**：
         `WinRAR.exe.WebView2/EBWebView/.../000003.log`、`vmware-Administrator`、`virtual_camera`、
         `kzip_sogou`、`ai/rp/task_outputs/.../output.log` ⇒ **太宽、制造假红**，否掉
      V2 「存在 `log` **目录**（任意深度）」              8 命中 —— 7 个是自家数据根 + 1 个外来程序（`kzip_sogou`）
     ⇒ 采用 V2。**残余假阳性风险在案**：外来程序自己的 `log/` 目录会被算作命中。
    """
    try:
        for root, dirs, _files in os.walk(d, onerror=lambda _e: None):
            if "log" in dirs:
                return Path(root, "log").relative_to(d).as_posix()
    except OSError:
        return None
    return None


def _shape_hits(T: Path):
    """`T` 的**直接子目录**里命中腿 B 的，返回 `[(名字, 触发路径)]`（自检用包装）。"""
    hits = []
    for d in sorted(T.iterdir()):
        if not d.is_dir() or _leak_key(d) in TMP_DECLARED_PATHS:
            continue
        rel = _shape_rel(d)
        if rel is not None:
            hits.append((d.name, rel))
    return hits


def _prefix_of(d: Path, prefixes):
    """腿 A：返回第一个命中的前缀（无则 None）。"""
    for pref in prefixes:
        if pref and d.name.startswith(pref):
            return pref
    return None


# ---------------------------------------------------------------- R-10 扫描根（§4.1.55 / 任务 #64）
# 加宽的两步：① **换 key：裸名 → 全路径**（`_leak_key`）——否则多根下同名目录会被集合运算
#   去重吃掉，白名单也会"吃掉任何根下的同名目录"；② **扩根**：除 `%TEMP%` 外，把 l-s2t
#   仓内三处落点纳入（它们既不在 `%TEMP%`、也被 `.gitignore` 的 `build/`+`release/` 遮住 ⇒
#   **无人兜底**）。落点自身就是候选（`mode="self"`），`%TEMP%` 枚举子项（`mode="children"`）。
def _leak_root_specs():
    """返回 `[(label, path, mode)]`；`mode ∈ {"children","self"}`。"""
    import tempfile
    specs = [("<TEMP>", Path(tempfile.gettempdir()), "children")]
    ls = ROOT / "local-speak2text"
    if ls.is_dir():
        for rel in ("build/test-data", "build/selftest-data"):
            specs.append(("<l-s2t>/" + rel, ls / rel, "self"))
        rel_dir = ls / "release"
        if rel_dir.is_dir():
            try:
                versions = sorted(p for p in rel_dir.iterdir() if p.is_dir())
            except OSError:
                versions = []
            for vd in versions:
                specs.append(("<l-s2t>/%s/smoke-data" % vd.name, vd / "smoke-data", "self"))
    return specs


def _iter_candidates(spec):
    """按 `mode` 产出**候选残留目录**。只 listdir、不递归、绝不删。"""
    _label, path, mode = spec
    try:
        if mode == "children":
            if not path.is_dir():
                return
            for d in sorted(path.iterdir()):
                if d.is_dir():
                    yield d
        else:
            if path.is_dir():
                yield path
    except OSError:
        return


def _scan_leak_roots(specs, prefixes):
    """扫描 `specs` 的候选集。

    返回 `(hits_a, hits_b, stats)`：
      `hits_a = [(key, label, path, pref, mtime, nfiles)]`
      `hits_b = [(key, label, path, rel)]`
      `stats  = [(label, path, mode, n_candidates, n_a, n_b)]`
    `key` = `_leak_key(path)`（**全路径**，跨根唯一）。
    """
    import time
    hits_a, hits_b, stats = [], [], []
    for spec in specs:
        label, path, mode = spec
        cands = list(_iter_candidates(spec))
        na = nb = 0
        for d in cands:
            key = _leak_key(d)
            pref = _prefix_of(d, prefixes)
            if pref is not None:
                try:
                    nfiles = len([f for f in d.rglob("*") if f.is_file()])
                    mtime = time.strftime("%m-%d %H:%M", time.localtime(d.stat().st_mtime))
                except OSError:
                    nfiles, mtime = 0, "(不可读)"
                hits_a.append((key, label, d, pref, mtime, nfiles))
                na += 1
            rel = _shape_rel(d)
            if rel is not None:
                hits_b.append((key, label, d, rel))
                nb += 1
        stats.append((label, path, mode, len(cands), na, nb))
    return hits_a, hits_b, stats


def _name_shape(name: str) -> str:
    """按**名字形态**反推"这是谁造的"——把"有残留"变成"该去改谁"的那一步。

    ls2t-dev 的判别实验（各造一个目录，形态固定可辨）：
      GNU `mktemp -d`            → `tmp.gVxHfxTMya`（**带点** + 10 字符）
      Python `tempfile.mkdtemp()` → `tmpigscx7m2`  （**无点** + 8 字符）
    为什么重要：l-s2t 那 8 个残留**全是"带点"形态 ⇒ 出自 shell `mktemp -d`**，
    而该仓源码里**没有任何裸 `mkdtemp()`** ⇒ **要改的是进程规则/脚本，不是仓库代码**；
    只看"有残留"会把修复方向指错（去 grep 一个根本不存在的调用点）。
    """
    if re.match(r"^tmp\.[A-Za-z0-9]{10}$", name):
        return "shell mktemp -d"
    if re.match(r"^tmp[A-Za-z0-9_]{8}$", name):
        return "Python mkdtemp"
    return "其他/家族前缀"


def _shape_histogram(names) -> str:
    """腿 B 命中集的**名字形态直方图**（lead 采纳 ls2t-dev 的口径）。"""
    from collections import Counter
    c = Counter(_name_shape(n) for n in names)
    return "，".join("%s %d" % (k, v) for k, v in sorted(c.items())) or "（空）"


def _declared_present():
    """白名单里**确实存在于盘上**的那些（只报出来，不计入并集/增量）。

    返回 `[(key, entry)]`；`key` 是**全路径**，`entry` 是 `{why, reverify}` 两栏。
    **打印由调用方负责把两栏都说全**（"为什么不算残留" + "什么时候重验"）——只打印名字/路径
    等于把开关藏起来。
    """
    out = []
    for key, entry in sorted(TMP_DECLARED_PATHS.items()):
        try:
            if Path(key).is_dir():
                out.append((key, entry))
        except OSError:
            pass
    return out


def temp_leak_main(names, save=None, baseline=None) -> int:
    """列出/比对 `%TEMP%` 里的残留目录，**两条腿**。只 listdir + stat，**绝不删任何东西**。

    `--temp-leak`          列出当前命中（永远 exit 0）：这是**取证**，不是判据——
                           历史存量会让它恒红，而"清一遍"在清理代码修好前不可能成立。
    `--temp-leak-save F`   把当前命中目录名写进 F（作为基线）。
    `--temp-leak-baseline F` 与基线比对，**只对"新增"报红**（残留免疫）。这就是
                           lead 定的验收口径"跑完门禁后实测 = 0"的可执行形态：
                           跑门禁前 save，跑完 baseline，新增必须为空。

    **两条腿都要，且必须打印扫描面**（task #43）：腿 A 的覆盖上限 = 源码里出现过的 prefix
    字面量；标定的 20 个残留里有一大半**在四个工具源码里一个字都搜不到**（裸 `mkdtemp()`
    的默认前缀 `tmp`、以及扫描范围之外的探针脚本），此时"腿 A 0 命中"与"真的没泄漏"
    在输出上完全同形。腿 B 看结构不看名字，是那些情况的唯一判据。
    **扫描面必须报"目录数"**：lead 那次把"顶层条目数"（目录+文件，634）当成了目录数
    （101）报出来，两张扫描面因此不可比——所以本函数把两个数**各带标签**一起打印。
    """
    import tempfile
    per_tool, all_prefs, all_weak = [], [], []
    for name in names:
        root = ROOT / name
        if not root.is_dir():
            print("[skip] %s: no such dir" % name)
            continue
        prefixes, opaque, registry, problems, weak, folded = enumerate_mkdtemp_prefixes(root)
        for vals in registry.values():
            prefixes = sorted(set(prefixes) | set(vals))
        uncovered = [r for r, _ in opaque if r not in registry]
        per_tool.append((name, prefixes, uncovered, problems, weak, folded))
        all_prefs += prefixes
        all_weak += weak
    all_prefs = sorted(set(all_prefs))
    T = Path(tempfile.gettempdir())
    specs = _leak_root_specs()

    print(identity_line())   # 取证输出也要自证身份
    print("== 扫描面 ==")
    # 扫描面必须**可比对**：`%TEMP%` 经环境变量常是 8.3 短名（`ADMINI~1`），
    # 两个人各贴一份输出会对不上"是不是同一个根"。故同时打印解析后的规范长路径。
    print("  %%TEMP%%: %s   （解析后: %s）" % (T, Path(T).resolve()))
    print("  根 %d 个（%d 个枚举子项 + %d 个落点自身）——§4.1.55 加宽后："
          % (len(specs), sum(1 for _l, _p, m in specs if m == "children"),
             sum(1 for _l, _p, m in specs if m == "self")))
    for label, path, mode in specs:
        print("    %-38s %-52s [%s]" % (label, path,
              "枚举子项" if mode == "children" else "落点自身"))
    print("  腿 A 前缀 %d 个（从源码枚举 + 登记表；其中弱前缀 %d 处来自裸 mkdtemp）"
          % (len(all_prefs), len(all_weak)))
    print("  腿 B 规则: %s" % _SHAPE_RULE)
    for name, prefixes, uncovered, problems, weak, folded in per_tool:
        print("    %-22s 前缀 %2d 个%s%s" % (name, len(prefixes),
              ("，弱前缀: " + ", ".join(p for _, p in weak)) if weak else "",
              ("，常量折叠 %d 处" % len(folded)) if folded else ""))
        for rel, why in problems:
            print("        [登记表形态问题] %s %s" % (rel, why))
        for rel in uncovered:
            print("        [不可枚举且未登记] %s" % rel)

    hits_a, hits_b, stats = _scan_leak_roots(specs, all_prefs)
    declared_set = set(TMP_DECLARED_PATHS)
    names_a = sorted({k for k, *_ in hits_a} - declared_set)
    names_b = sorted({k for k, *_ in hits_b} - declared_set)
    union = sorted(set(names_a) | set(names_b))
    print("== 每个根的扫描面 + 命中数（§4.1.55 验收：每个根各自打印）==")
    for label, path, mode, nc, na, nb in stats:
        print("  %-38s 候选 %3d  腿A %3d  腿B %3d  [%s]"
              % (label, nc, na, nb, "枚举子项" if mode == "children" else "落点自身"))
    print("== 腿 A：生成器派生（前缀）命中 %d ==" % len(names_a))
    by_pref = {}
    for key, label, d, pref, ts, nfiles in hits_a:
        if key in declared_set:
            continue
        by_pref.setdefault(pref, []).append((d.name, label, ts, nfiles))
    for pref, items in sorted(by_pref.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        print("  %-26s %2d 个" % (pref, len(items)))
        for dname, label, ts, nfiles in items[:3]:
            print("        %-30s %-18s %s 文件%2d%s"
                  % (dname, label, ts, nfiles, "" if nfiles else " (空目录)"))
        if len(items) > 3:
            print("        ... 还有 %d 个" % (len(items) - 3))
    key2b = {k: (d, label, rel) for k, label, d, rel in hits_b}
    set_a = set(names_a)
    only_b = [k for k in names_b if k not in set_a]
    print("== 腿 B：形态派生（不看名字）命中 %d ==" % len(names_b))
    for k in names_b[:12]:
        d, label, rel = key2b[k]
        print("        %-30s %-18s %-24s%s"
              % (d.name, label, rel, "" if k in set_a else "  <- 腿 A 的盲区"))
    if len(names_b) > 12:
        print("        ... 还有 %d 个" % (len(names_b) - 12))
    # 名字形态直方图：**把"有残留"变成"该去改谁"**——带点 ⇒ shell `mktemp -d`
    # （进程规则/外部 CLI 造的，源码里没有可枚举的调用点）；无点 ⇒ Python `mkdtemp()`。
    print("  名字形态直方图：%s" % _shape_histogram([Path(k).name for k in names_b]))
    print("     ↑ 带点（`tmp.<10>`）= GNU `mktemp -d`（shell/外部 CLI）；无点（`tmp<8>`）= Python `mkdtemp()`。"
          "前者**源码里没有调用点**，只能靠形态腿，且要改的是**进程规则**而不是代码")
    declared = _declared_present()
    if TMP_DECLARED_PATHS:
        print("== 已声明位置白名单：**生效 %d 条**（全部参与过滤）/ 其中现场命中 %d 条 =="
              % (len(TMP_DECLARED_PATHS), len(declared)))
        # **全部条目都打印，不只打印"现场命中"的那些**（lead 2026-09-19）：白名单是
        # **关掉覆盖**的开关——开关藏起来，就没人能发现它过期了；而且**不在盘上时它照样生效**
        # （过滤发生在判定阶段，与当前有没有残留无关）。key 已换成**全路径** ⇒ 同名目录在
        # 其它根下不会被这条暗吃掉（§4.1.55）。
        present = {k for k, _ in declared}
        for k, entry in sorted(TMP_DECLARED_PATHS.items()):
            print("        %s  %s" % (k, "现场命中" if k in present else "（当前不在盘上，条目仍生效）"))
            print("        %-30s [为什么不算残留] %s" % ("", entry.get("why", "?")))
            print("        %-30s [重验触发条件]   %s" % ("", entry.get("reverify", "?")))
        for name, why in _declared_problems():
            print("        [BROKEN] 白名单条目本身不合规：%s —— %s" % (name, why))
    reg = {n for v in _TEMP_REGRESSION_20260919.values() for n in v}
    hit_basenames = {Path(k).name for k in union}
    print("== 并集 %d 个；其中 %d 个在腿 A 命中之外（腿 B 独有）；"
          "命中已登记回归集 %d/%d（按**目录名**比对）=="
          % (len(union), len(only_b), len(hit_basenames & reg), len(reg)))
    # 扫描面报**目录数**：lead 那次把"条目数"（目录+文件）当成了目录数（634 vs 101），
    # 于是两个人贴出来的扫描面根本不可比。两个数**显式带标签**一起报。
    n_dirs = len([d for d in T.iterdir() if d.is_dir()])
    n_entries = len(list(T.iterdir()))
    print("RESULT: 扫描**根** %d 个（%%TEMP%% 顶层目录 %d 个 / 顶层条目 %d = 目录+文件）"
          " / 腿 A 前缀 %d 个 / 命中 A=%d B=%d 并集=%d / 已声明 %d"
          % (len(specs), n_dirs, n_entries, len(all_prefs), len(names_a), len(names_b),
             len(union), len(TMP_DECLARED_PATHS)))
    if save:
        Path(save).write_text("\n".join(union) + "\n", encoding="utf-8")
        print("已写基线: %s（%d 条，并集）" % (save, len(union)))
    if baseline:
        bp = Path(baseline)
        if not bp.exists():
            print("[判不了] 基线文件不存在: %s——先在跑测试前 --temp-leak-save" % bp)
            return 2
        old = {ln.strip() for ln in bp.read_text(encoding="utf-8").splitlines() if ln.strip()}
        cur = set(union)
        new = sorted(cur - old)
        gone = sorted(old - cur)
        print("基线 %d 条；本次新增 %d 条；基线里已消失 %d 条" % (len(old), len(new), len(gone)))
        for d in new:
            print("  [泄漏复现] %s" % d)
        if new:
            return 1
        print("增量 = 0：本轮没有新增残留（**这才是验收判据**；历史存量不计）")
    return 0


# ---------------------------------------------------------------- C-32
# 窄版（复核员定稿、lead 裁定）：**读同一对象 → 删它 → 再 log 用那个值**，三条同时满足：
#   D：`unlink/remove/rmtree/rmdir`，接收者记 `rcv`；
#   A：函数内**任意一条**早于 D 的赋值，右值**含** `read_text/read_bytes` 且接收者与 `rcv`
#      **AST 相同**（`ast.dump` 相等）；
#   R：晚于 D 的 log 调用，参数引用了 A 的名字。
# 为什么不是"同一语句块"：加了它 → **漏掉正典**（命中 0）；为什么不是"最近一条赋值"：
# 加了它 → 落在 `except` 分支的 `detail = ""` 上（同一变量两条赋值），命中 4、**漏了 reme**。
# 改"遍历所有先前赋值"才得到 5 处全真、零假阳性（复核员逐条回验）。见设计纪律第 5 条。
_READ_CALLS = ("read_text", "read_bytes")
_DELETE_NAMES = ("unlink", "remove", "rmtree", "rmdir")
_LOG_NAMES = ("log", "_log")


def _call_name(call):
    """`marker.unlink()` → `(接收者表达式, 'unlink')`；`os.remove(x)` → `(None, 'remove')`。"""
    f = call.func
    if isinstance(f, ast.Attribute):
        return f.value, f.attr
    if isinstance(f, ast.Name):
        return None, f.id
    return None, None


def _iter_no_defs(node):
    """遍历子树但**不进嵌套函数/类/lambda**：否则内层函数的读写会被算到外层头上。"""
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            continue
        yield child
        yield from _iter_no_defs(child)


def _evidence_order_hits(fn):
    """窄版 D/A/R 的三元组命中：`[(读行, 变量, 删行, log行)]`。"""
    reads, dels, logs_ = [], [], []
    for node in _iter_no_defs(fn):
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)):
            # 右值本身也要看（`detail = marker.read_text()` 的读调用就是右值根节点，
            # 只看子孙会整个漏掉——首跑样本当场打出来的漏报）。
            for c in itertools.chain([node.value], _iter_no_defs(node.value)):
                if isinstance(c, ast.Call):
                    rcv, name = _call_name(c)
                    if rcv is not None and name in _READ_CALLS:
                        reads.append((node.lineno, node.targets[0].id, ast.dump(rcv)))
                        break
        if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
            rcv, name = _call_name(node.value)
            if name in _DELETE_NAMES:
                subj = rcv if rcv is not None else (
                    node.value.args[0] if node.value.args else None)
                if subj is not None:
                    dels.append((node.lineno, ast.dump(subj)))
        if isinstance(node, ast.Call):
            _rcv, name = _call_name(node)
            if name in _LOG_NAMES:
                names = {n.id for n in _iter_no_defs(node) if isinstance(n, ast.Name)}
                logs_.append((node.lineno, names))
    hits = []
    for d_line, d_rcv in dels:
        for a_line, var, a_rcv in reads:
            if a_line >= d_line or a_rcv != d_rcv:
                continue
            for r_line, names in logs_:
                if r_line > d_line and var in names:
                    hits.append((a_line, var, d_line, r_line))
                    break
    return hits


def check_evidence_order(root: Path):
    """按窄版 D/A/R 找"读证据 → 删证据 → 报告"。返回 `(ok, detail)`。"""
    bad = []
    for p in _py_files_under(root):
        try:
            tree = ast.parse(p.read_text(encoding="utf-8", errors="replace"))
        except (SyntaxError, OSError):
            continue
        base_rel = p.relative_to(root).as_posix()
        for fn in [n for n in ast.walk(tree)
                   if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
            for a_line, var, d_line, r_line in _evidence_order_hits(fn):
                bad.append("%s: %s():%d 读 `%s` → :%d 删同一接收者 → :%d 才 log 它"
                           % (base_rel, fn.name, a_line, var, d_line, r_line))
    if bad:
        return False, ("；".join(bad) + "。【为什么是硬违规】不可逆动作（删证据）排在"
                       "**调用边界可能失败的语句**之前：arity/签名不符、属性不存在这类错误"
                       "在**进入被调方之前**就抛出，**被调方内部的 try/except 保护不了它**"
                       "——l-s2t 就是这么真炸的（TypeError + marker 已删 + 提示消失）。"
                       "【正确形态】先算文案 → 先报告 → **最后**删证据（删不掉就留给下次再报）")
    return True, "没有「读证据→删证据→报告」的危险顺序"


# ---------------------------------------------------------------- C-33
# **禁止拿 `ping` 当等待节拍**。它不是"睡 1 秒"，而是"发 N 个 ICMP 等回包"——
# 在**丢弃 loopback ICMP** 的机器上每个包要等满超时：`ping -n 2 127.0.0.1` 实测 **9.0s**
# （两次 4.5s），于是名义 120s 的等待变成 ~18 分钟，而 `:giveup` 还打印 "after 120s"
# ——**日志说谎**。这是"以未验证的单位假设写等待/超时"的一族（同类：robocopy rc=0 其实是
# "没拷文件"）。判据口径：`.py`/`.bat` 里出现 `ping` 且带 `-n`/`-w` 参数即**确证违规**
# （本家族没有任何"真的需要 ping 网络"的用途；有求真的用法再给它开单独形态）。
#
# ⚠️ **假红与修法（2026-09-19，lead 批准，且是本波冻结的硬前置）**：本判据曾把自己的
# **docstring 判红**——那段散文正是在解释"为什么禁 `ping -n 2`"，于是**越说清原因越违规**；
# 把模板仓当工具根跑（`--roots my-diy-tool-template`）时更明显：自身 5 处命中全在
# `conformance_check.py` 里（1 处 docstring + 1 处诊断文案 + 3 处自证样本）。修法三条
# （**不是**删掉解释文字——那等于让判据在最该说清原因的文字上被绕开）：
#   ① `_code_only_text` 挖掉 **AST docstring 节点**（豁免对象 = "关于代码的文本"）；
#   ② 扫描面**按绝对路径排除仪器自身**（它的诊断文案与自证样本**必然**含被禁形态），
#      排除项打印进 detail（否则"排除了"与"没扫"同形，同 C-30 的扫描面纪律）；
#   ③ 自证集补上缺的那条腿 `ping_in_py_docstring_ok`——**原来 5 条腿恰好缺它**，所以假红
#      一路绿灯。⇒ **豁免的每一条边界都必须有一条腿**，否则那条边界没人守着。
_PING_TICK = re.compile(r"\bping(?:\.exe)?\b[^\n]*?\s-(?:n|w)\b", re.I)


def _strip_docstrings(text: str) -> str:
    """挖掉 **AST 里的 docstring 节点**（保留行号与偏移，位置不失真）。

    挖的是**裸字符串表达式语句**（`ast.Expr` 且值是**字符串常量**）：包含语言定义的 docstring
    （`Module`/`ClassDef`/`FunctionDef`/`AsyncFunctionDef` 的 `body[0]`），也包含**位置不在
    首位**的说明性字符串——两者**运行时都是零效果**，语义上都是"关于代码的文本"。
    ⚠️ 只挖到"裸"这一层：**参与运算/赋值/传参的字符串一律保留**——渲染 bat 的 python 模板、
    判据自己的正样本，都是这种普通字符串，那才是要查的东西。
    解析失败（语法错）时**原样返回**：宁可按文本查，也不静默放过。
    """
    import ast
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return text
    rows = text.splitlines(keepends=True)
    offset = []
    acc = 0
    for line in rows:
        offset.append(acc)
        acc += len(line)
    for node in ast.walk(tree):
        if (not isinstance(node, ast.Expr)
                or not isinstance(node.value, ast.Constant)
                or not isinstance(node.value.value, str)):
            continue
        lo = node.lineno
        hi = node.end_lineno or node.lineno
        for r in range(lo, min(hi, len(rows)) + 1):
            # 逐字符掩成空格：**换行原样保留** ⇒ 行号与偏移量都不失真
            line = rows[r - 1]
            body_end = len(line.rstrip("\r\n"))
            text = (text[:offset[r - 1]]
                    + " " * body_end + line[body_end:]
                        + text[offset[r - 1] + len(line):])
    return text


def _masked_code_text(text: str) -> str:
    """把**注释与 docstring 就地掩成空格**：长度与换行**完全不变** ⇒ 偏移量与行号仍可靠。

    与 `_code_only_text` 的分工：那个拼成"逻辑行"给**跨行形态正则**用（行号会失真）；
    这个留在原位置给**要报行号的判据**用（C-30 的登记键就是 `相对路径:行号`）。
    **为什么必须有它（2026-09-19，同一条豁免边界、同一成因）**：C-30 下半曾在**原始文本**
    上找 `rmtree(..., ignore_errors=True)`，而 `_rmtree_strict` 的 docstring **引用**了那句
    旧写法（"本工具自己先得守 C-30"）⇒ **仪器在自己的合规说明上自证违规**，和 C-33 读
    docstring 假红一模一样。⇒ **凡"在源码文本上找形态"的判据，都必须在掩码后的文本上找**。
    """
    import io
    import tokenize
    out = _strip_docstrings(text)
    try:
        toks = list(tokenize.generate_tokens(io.StringIO(out).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return out
    rows = out.splitlines(keepends=True)
    offset = []
    acc = 0
    for line in rows:
        offset.append(acc)
        acc += len(line)
    buf = list(out)
    for t in toks:
        if t.type != tokenize.COMMENT or t.start[0] - 1 >= len(rows):
            continue
        r, col = t.start                      # COMMENT 词法单元**从不跨行**
        line = rows[r - 1]
        end = len(line.rstrip("\r\n"))
        for i in range(offset[r - 1] + col, offset[r - 1] + end):
            if buf[i] not in "\r\n":
                buf[i] = " "
    return "".join(buf)


def _code_only_text(p: Path, text: str) -> str:
    """**注释与 docstring 不算违规**（纪律 ④(c)：这里要抓的是会被执行的节拍）。

    `.py`：① 用 `ast` 挖掉 **docstring 节点**；② 用 `tokenize` 把 `COMMENT` 词法单元挖掉。
    其余字符串**不碰**——渲染 bat 的 `.py` 模板正是**字符串**，那才是要查的东西。
    `.bat`/`.cmd`：逐行丢掉 `rem` / `::`。**两件都做**：渲染出来的 bat 会以 `rem` 行形式
    存在字符串里。

    ⚠️ **豁免边界（2026-09-19，lead 裁定，写进条款）**：**"不碰字符串"这条豁免的适用对象是
    "会被执行的代码文本"**；**docstring / 注释是"关于代码的文本"**——它与 bat 模板**同为
    STRING token，语义不同**。**这是豁免边界画错，不是实现 bug**。
    ⇒ 通用形态（与今天多条同族）：**判据的豁免范围一旦按"token 类型"划，就会把"语义不同的
    同类型对象"一起放过、或一起误伤**（裸 `mkdtemp()` 按"prefix 有无"划、C-22 按"扩展名"划，
    都出过同类问题）。**按 token 类型划 = 按语法分类；而这里要分的是语义**。
    ⇒ 代价曾经是**假红**：本判据自己的 docstring 解释了"为什么要禁 `ping -n 2`"，于是
    **解释得越清楚越会被判红**。**改写注释来绕开是错的**——那等于让判据在最该说清原因的文字上
    被绕开；只能从判据侧修（本函数）＋补上缺的那条自证腿（`ping_in_py_docstring_ok`）。
    自证集此前 **5 条腿恰好缺这一条**，所以假红一路绿灯、直到被真树上的散文触发。
    """
    if p.suffix.lower() == ".py":
        import io
        import tokenize
        text = _strip_docstrings(text)
        try:
            out = []
            for tok in tokenize.generate_tokens(io.StringIO(text).readline):
                if tok.type == tokenize.COMMENT:
                    out.append("\n" * tok.string.count("\n") + " " * (len(tok.string) - tok.string.count("\n")))
                else:
                    out.append(tok.string)
            text = " ".join(out)   # 行号不再对应原文，故下面按"逻辑行"报
        except (tokenize.TokenError, IndentationError, SyntaxError):
            pass
    kept = []
    for line in text.splitlines():
        s = line.strip().lower()
        if s.startswith("rem ") or s == "rem" or s.startswith("::"):
            continue
        kept.append(line)
    return "\n".join(kept)


def check_ping_tick(root: Path):
    """`root` 下的 `.py`/`.bat`/`.cmd` 不得用 `ping -n/-w` 当节拍。返回 `(ok, detail)`。

    ⚠️ **扫描面排除仪器自身**（2026-09-19，同一条豁免边界的机械形态）：本判据所在文件的
    **诊断文案**（解释"为什么要禁 `ping -n 2`"）与**自证样本**（`ping_tick_in_py_flagged`
    等把被禁形态当**数据**）**必然**包含被禁字符串——它们都是"关于代码的文本"。判据对自己
    无法做可靠证人：**它引用的正是它要禁的东西**。⇒ 自身文件按**绝对路径**排除（不按文件名，
    否则改个名字就能豁免），且**排除数量必须打印出来**——否则"排除了"与"没扫"同形
    （同 C-30"每个根都要打印扫描目录数"）。
    """
    self_path = Path(__file__).resolve()
    hits = []
    files = [p for p in root.rglob("*")
             if p.is_file() and p.suffix.lower() in (".py", ".bat", ".cmd")
             and not any(part in _PY_SKIP_DIRS for part in p.parts)]
    excluded = []
    for p in sorted(files):
        if p.resolve() == self_path:
            excluded.append(p.relative_to(root).as_posix())
            continue
        text = _code_only_text(p, p.read_text(encoding="utf-8", errors="replace"))
        rel = p.relative_to(root).as_posix()
        for n, m in enumerate(_PING_TICK.finditer(text), 1):
            hits.append("%s(命中%d) `%s`" % (rel, n, m.group(0).strip()[:40]))
    span = "扫描面：%d 个 .py/.bat/.cmd" % (len(files) - len(excluded))
    if excluded:
        span += "；排除仪器自身 %s（诊断文案与自证样本必然含被禁形态）" % ", ".join(excluded)
    if hits:
        return False, ("%d 处用 ping 当等待节拍：%s。【为什么是硬违规】`ping -n 2` 的\"1 秒\""
                       "只在 loopback ICMP 有响应时成立；丢弃 ICMP 的机器上实测 **9.0s/拍**"
                       "（两次 4.5s 超时），名义 120s→实际 ~18 分钟，而超时日志仍写\"120s\""
                       "（**日志说谎**）。改用不依赖网络的睡眠："
                       "`powershell -NoProfile -Command \"Start-Sleep -Milliseconds 1000\"`"
                       "（DETACHED 进程无 console，子进程不会弹窗）。%s"
                       % (len(hits), ", ".join(hits[:8]), span))
    return True, "没有把 ping 当等待节拍。%s" % span


# ---------------------------------------------------------------- C-39
# **派生值必须取自"本次调用的实参"，不能取自"模块级当前值 / 定义时的快照"**（lead 2026-09-19 立）。
# 一族两例，都是"用了另一个时刻/另一个来源的值去代替本次输入"：
#   ① `AsrEngine.__init__(self, model_dir=MODEL_DIR)`——默认参数在**定义时**求值，
#      运行期 `load_config()` 重绑 `MODEL_DIR` 也传不进去（l-s2t #46，用户改了配置却不生效）；
#   ② `_APPLY_BAT` 的 `budget_s` 曾取模块常量 `UPDATE_WAIT_BUDGET_S`（按 `UPDATE_WAIT_LIMIT=120`
#      算），调用方 `limit=2` 时渲染出 `2 polls x 1000ms (nominal budget 120s)`——
#      **拼出了一个不可能的组合**（1.4.4 已修）。
# **可判的那一半**（本条）：**函数默认值是模块级名字**。危险与否**有判别准则**，不是"看到就报"：
#   * 该名字在模块里**被重绑过**（模块级多次赋值 / 任何 `global` 重绑）⇒ **快照必然失真** ⇒ 红；
#   * 默认值是**可变字面量**（`[]`/`{}`/`set()`）⇒ 跨调用共享同一对象 ⇒ 红（经典坑）；
#   * 只赋值一次、且是不可变字面量、无 `global` 重绑 ⇒ **良性**（今天全家族 13 处全属此类）。
#   ⚠️ 第三档**必须放行**，否则就是"看到默认参数就报"的噪音判据——那正是 C-33 那族错误的翻版。
_DEFAULT_SNAPSHOT_OK_NOTE = ("良性：模块级常量只赋值一次、不可变、无 global 重绑 ⇒ "
                             "默认值 == 当前值，不会失真")


def _module_bindings(tree):
    """模块级名字的**赋值次数** + 被 `global` 重绑的名字集合。"""
    counts = {}
    globals_rebound = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Global):
            globals_rebound.update(node.names)
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    counts[t.id] = counts.get(t.id, 0) + 1
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
            t = node.target
            if isinstance(t, ast.Name):
                counts[t.id] = counts.get(t.id, 0) + 1
    return counts, globals_rebound


def _mutable_default(node) -> bool:
    return (isinstance(node, (ast.List, ast.Dict, ast.Set))
            or (isinstance(node, ast.Call) and getattr(node.func, "id", "") in ("list", "dict", "set")))


def check_default_snapshot(root: Path, sub: str = "src"):
    """`root/<sub>/**/*.py`：默认参数不得取"会被重绑的模块级名字"或可变字面量。

    `sub` 默认 `src`（工具侧）；**模板侧传 `modules`**——模板根下没有 `src/`，不传就恒
    "判据不适用"，而这一类缺陷的活样本（`update_helper.py` 的 `budget_s`）恰恰住在 `modules/` 里。
    """
    src = root / sub
    if not src.is_dir():
        return True, "扫描面：无 %s/（判据不适用）" % sub
    bad, benign, scanned = [], 0, 0
    for f in sorted(src.rglob("*.py")):
        if any(part in _PY_SKIP_DIRS for part in f.parts):
            continue
        try:
            text = _masked_code_text(f.read_text(encoding="utf-8", errors="replace"))
            tree = ast.parse(text)
        except (OSError, SyntaxError):
            continue
        scanned += 1
        rel = f.relative_to(root).as_posix()
        counts, reb = _module_bindings(tree)
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for d in list(node.args.defaults) + [x for x in node.args.kw_defaults if x]:
                if _mutable_default(d):
                    bad.append("%s:%d `%s()` 的默认值是**可变字面量**（跨调用共享同一对象）"
                               % (rel, d.lineno, node.name))
                    continue
                if not isinstance(d, ast.Name):
                    continue
                name = d.id
                if name in reb or counts.get(name, 0) > 1:
                    bad.append("%s:%d `%s(...=%s)` 的默认值是**会被重绑的模块级名字**"
                               "（%s）——默认值在**定义时**求值，之后的每次重绑都传不进去"
                               % (rel, d.lineno, node.name, name,
                                  "有 global 重绑" if name in reb else "模块级赋值 %d 次"
                                  % counts.get(name, 0)))
                elif name.isupper():
                    benign += 1
    if bad:
        return False, ("%d 处默认参数取了\"另一个时刻的值\"：%s。【为什么是硬违规】默认参数在"
                       "**函数定义时**求值一次，之后模块级名字怎么变都传不进去——用户改了配置"
                       "却不生效（l-s2t #46 就是这个形态）。【正确形态】用 `None` 哨兵 + "
                       "函数体内解析（`if x is None: x = MODULE_NAME`），把取值推迟到**本次调用**。"
                       "【说明】模块级常量只赋值一次且不可变时**不算违规**（本扫描面里良性 %d 处）"
                       % (len(bad), "；".join(bad[:6]), benign))
    return True, ("扫描面：%s/**/*.py 共 %d 个文件；%s；良性默认参数 %d 处（只赋值一次、不可变）"
                  % (sub, scanned, _DEFAULT_SNAPSHOT_OK_NOTE, benign))


@check("C-39", "FAIL", "默认参数不得取「会被重绑的模块级名字」/ 可变字面量（定义时快照）")
def c39(c: Ctx):
    """见上方注释。与 §4.1.41 同条：**派生值必须取自本次调用的实参**。

    两例：`AsrEngine(model_dir=MODEL_DIR)`（#46，导入期快照）、`budget_s` 取模块常量
    （更新链文案与实参不符，1.4.4 修）。**第三档（良性常量）必须放行**——否则就是噪音判据。
    """
    return check_default_snapshot(c.dir)


@template_check("C-39", "FAIL", "模板派发件里的同一形态（模板正本只跑一次）")
def c39_template(c: Ctx):
    return check_default_snapshot(c.dir, "template")


# ---------------------------------------------------------------- C-40
# **版本目录 ↔ 自启目标 必须一致**（ls2t-dev 提议，lead 补两处修正后定）。
# 它把一条**靠人自觉的纪律**（"每个 owner 写明启动哪个 exe、版本号与源码 VERSION 是否一致"）
# 换成**可判的性质**——与 C-38「生产者自我标识」同一手法：**纪律 → 可判性质**。
# 三条都能从**磁盘 + 注册表**直接读，不需要任何人记忆。
#
# ⚠️ **不能写成"release/ 的版本目录集合 == {VERSION}"**（lead 的修正，实测两处假红）：
#   `reme-helper/release/` = 1.2.4 + 1.2.5、`dsh-helper/release/` = 1.8.1 + 1.8.2
#   ⇒「集合相等」会把**正常的历次构建产物**全判红。⇒ 拆两段、两个等级：
#   **① 强断言（FAIL）**：**自启目标必须存在**，且其所在目录必须是 `release/<源码 VERSION>/`
#      **或稳定安装位**（`%LOCALAPPDATA%\<APP_ID>\app`，若该工具已用稳定位）；
#   **② 登记断言（WARN）**：**不属于当前 VERSION 的版本目录 = 孤儿版本**，必须**声明"是否仍被引用"**。
#      **被引用的孤儿 = 必须处理；未被引用的 = 可清理**（§4.1.34 第③款）。
#      **声明条目按纪律 ⑩ 两栏必填**（`why` + `reverify`）——它是**关掉覆盖**的开关。
#
# **措辞纪律（ls2t-dev 主动补的，lead 认为比答对更有价值）**：陈述必须区分
# **"从未发生"（不可验证）** 与 **"发生过且已收敛"（可验证且更诚实）**——
# 条目一律写成 **"当前态 + 是否曾经出现过 + 如何收敛"**。
_STABLE_INSTALL_SUBDIR = "app"          # %LOCALAPPDATA%\<APP_ID>\app
ORPHAN_VERSIONS = {
    # 目录名 -> {why: 为什么可留 / 被谁引用 / 如何收敛, reverify: 什么情况下必须重验}
    #
    # ⚠ **只登记"改名保留的镜像"**（`_stale_*` / `*.pre-rebuild-*`）—— 那是有意动作，必须留痕。
    # **普通 `<tool>-<semver>` 目录（含"上一版"）不登记**：它们是历次构建的自然产物
    # （§4.1.42 原话），逐条登记会随发版次数线性增长、必然漏登（2026-09-20 发版暴露）。
    # 条目按**纪律 ⑩ 两栏必填**（`why` + `reverify`）——它是**关掉覆盖**的开关。
    "_stale_dsh-helper-1.8.2_20260920-120657": {
        "why": "未被引用的**改名保留镜像**（2026-09-20 发版前归档）。它曾是 dsh 的临时升号产物、"
               "后被 Run 键引用（部署版本 != 源码 VERSION 的那个状态）；2026-09-19 21:16 Run 键先改指 1.8.1，"
               "2026-09-20 发版升到 **1.8.2** 时把该目录归档为本名（D11 rename-preserve，不删）。"
               "当前态：存在、**未被引用**——Run[dsh-helper] 实测指向 "
               "`release\dsh-helper-1.8.2\dsh-helper.exe`（== 当前源码 VERSION）。"
               "曾出现过：是。如何收敛：**未收敛**——它现在只是回滚路径；删除未获授权。",
        "reverify": "dsh 的 Run 键值或 `release/` 目录集合变化时；或用户授权清理该镜像时。",
    },
    "_stale_local-speak2text-1.4.0-20260919-204004": {
        "why": "未被引用的**改名保留镜像**（2026-09-19 20:40:04 一次重建时保留）。"
               "当前态：存在、**未被引用**——Run[LocalSpeak2Text] 实测指向 "
               "`release\local-speak2text-1.4.1\local-speak2text.exe`（== 当前源码 VERSION 1.4.1）。"
               "内含旧 exe（6296010 B / mtime 2026-09-19 17:25）+ `_internal/` + README* + config.json"
               "（smoke.log 是 22:15 取证时新写的，非原目录内容）。曾出现过：是。"
               "如何收敛：**未收敛**——未被引用，但按红线不得删 `release/`，它是回滚路径之一。",
        "reverify": "l-s2t 的 Run 键值或 `release/` 目录集合变化时；或用户授权清理该镜像时。",
    },
    "opencodex-helper-1.2.1.pre-rebuild-20260919-203905": {
        "why": "未被引用的**改名保留镜像**（2026-09-19 20:39:05 ocx 重建时保留——为避免 "
               "`robocopy /E` 在目标目录留下陈旧 `_internal`）。当前态：存在、**未被引用**——"
               "Run[opencodex-helper] 实测指向 "
               "`release\opencodex-helper-1.2.2\opencodex-helper.exe`（== 当前源码 VERSION 1.2.2）。"
               "曾出现过：是。如何收敛：**未收敛**——未被引用，删除未获授权。",
        "reverify": "ocx 的 Run 键值或 `release/` 目录集合变化时；或用户授权清理该镜像时。",
    },
    "_stale_reme-helper-1.2.5_20260919-204442": {
        "why": "未被引用的**改名保留镜像**（2026-09-19 20:44:42 一次重建时保留）。"
               "当前态：存在、**未被引用**——Run[reme-helper] 实测指向 "
               "`release\reme-helper-1.2.6\reme-helper.exe`（== 当前源码 VERSION 1.2.6）。"
               "含旧 exe（4192589 B / mtime 2026-09-19 18:51:06）+ `_internal/`。曾出现过：是。"
               "如何收敛：**未收敛**——未被引用，删除未获授权。",
        "reverify": "reme 的 Run 键值或 `release/` 目录集合变化时；或用户授权清理该镜像时。",
    },
}
_REQUIRED_ORPHAN_FIELDS = ("why", "reverify")


def orphan_entry_problems():
    """孤儿版本登记表的**两栏必填**校验（纪律 ⑩，与 `TMP_DECLARED_PATHS` 同一形态）。"""
    out = []
    for name, entry in sorted(ORPHAN_VERSIONS.items()):
        if not isinstance(entry, dict):
            out.append((name, "条目不是 `{why, reverify}` 两栏结构"))
            continue
        for field in _REQUIRED_ORPHAN_FIELDS:
            if not str(entry.get(field, "")).strip():
                out.append((name, "缺必填栏 `%s`——它是**关掉覆盖**的开关，没写就没人知道何时过期"
                            % field))
    return out


def tool_version(root: Path):
    """源码 VERSION（单一事实源）：`src/main.py` 优先，其次 appconfig 的两个落点。"""
    import ast as _ast
    for rel in ("src/main.py", "src/appconfig.py",
                "src/template/appconfig/appconfig.py"):
        f = root / rel
        if not f.exists():
            continue
        try:
            tree = _ast.parse(f.read_text(encoding="utf-8", errors="replace"))
        except (OSError, SyntaxError):
            continue
        for node in tree.body:
            if isinstance(node, _ast.Assign):
                for t in node.targets:
                    if (isinstance(t, _ast.Name) and t.id == "VERSION"
                            and isinstance(node.value, _ast.Constant)
                            and isinstance(node.value.value, str)):
                        return node.value.value, rel
    return None, None


def _run_values():
    """HKCU\\...\\Run 的**全部键值**（`{键名: 值}`）；读不到（非 Windows / 无权限）返回 `{}`。

    为什么取全表（CONFORMANCE §4.1.53）：Run 键名**没有单一契约**（§4.1.54）——模板 autostart 用
    `APP_NAME`（l-s2t 的键是 `LocalSpeak2Text`），reme 内联用 `APP_ID`（键是 `reme-helper`）。
    旧实现按 `APP_ID` 单查 ⇒ 对 `APP_ID != APP_NAME` 的工具**永远读不到** ⇒ 强断言静默不执行 = 假绿。
    """
    out = {}
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                            r"Software\Microsoft\Windows\CurrentVersion\Run",
                            0, winreg.KEY_READ) as k:
            i = 0
            while True:
                try:
                    name, val, _ = winreg.EnumValue(k, i)
                except OSError:
                    break
                out[name] = val
                i += 1
    except Exception:
        return {}
    return out


def _first_path(cmd):
    """从 Run 值（整条命令行）取第一个路径 token：优先第一个引号段，否则首个空白分隔 token。"""
    if not cmd:
        return None
    m = re.search(r'"([^"]+)"', str(cmd))
    if m:
        return m.group(1)
    parts = str(cmd).strip().split()
    return parts[0] if parts else None


def _is_under(child, parent):
    """`child` 是否等于 `parent` 或在其下（`normcase`+`normpath`，**不要求路径存在**，便于自证）。"""
    if not child or not parent:
        return False
    c = os.path.normcase(os.path.normpath(str(child)))
    p = os.path.normcase(os.path.normpath(str(parent)))
    return c == p or c.startswith(p + os.sep)


def select_run_entry(run_values, root=None, app_id=None, app_name=None, local_appdata=None):
    """选**本工具**的 Run 项：**先按路径、再按键名**（不依赖键名，CONFORMANCE §4.1.53/§4.1.54）。

    为什么不能只认键名：家族里 Run 键名**无单一契约**——模板 autostart 用 `APP_NAME`、reme 内联用
    `APP_ID` ⇒ 任选其一都会漏掉另一半。故两条腿：
      ① **路径腿**（主）：枚举全表，值里的路径落在**本工具仓库根**或**稳定安装位**之下即命中；
      ② **键名腿**（兜底）：无路径命中时退回 `APP_NAME` → `APP_ID` 候选（覆盖 dev 态等路径异常的形态）。
    返回 `(key, value, how, notes)`；`how ∈ {"path","name","none"}`——**打印实际走的哪条路**。
    `notes` 记需人看的形态：多个项指向本工具 / 命中键名不是候选（大小写变体或第三形态，§4.1.51）/
    两候选键同时存在。
    """
    rv = run_values or {}
    root_p = Path(root) if root else None
    stable = (Path(local_appdata) / app_id / _STABLE_INSTALL_SUBDIR
              if (local_appdata and app_id) else None)
    hits = []
    for k, v in rv.items():
        p = _first_path(v)
        if p and ((root_p and _is_under(p, root_p)) or (stable and _is_under(p, stable))):
            hits.append(k)
    order = [k for k in (app_name, app_id) if k]
    notes = []
    if hits:
        key, how = hits[0], "path"
        if len(hits) > 1:
            notes.append("**多个** Run 项指向本工具：%s（取第一个，需人看）"
                         % ",".join(sorted(hits)))
        if key not in order:
            notes.append("命中键 `%s` **不是** APP_NAME/APP_ID 候选（大小写变体或第三形态；"
                         "`migrate_autostart` 只读 APP_NAME，看不见它，§4.1.51）" % key)
    else:
        key = next((k for k in order if k in rv), None)
        how = "name" if key else "none"
    if key is not None:
        others = [k for k in order if k != key and k in rv]
        if others:
            diff = any(rv[k] != rv[key] for k in others)
            notes.append("候选键 `%s` 同时存在（值%s）" % (",".join(others), "不同" if diff else "相同"))
    return key, (rv.get(key) if key is not None else None), how, notes


def _read_app_name(root):
    """从 `src/modules/appconfig/appconfig.py` 读 **`APP_NAME`**（模板 autostart 契约的键名）。"""
    ap = root / "src" / "template" / "appconfig" / "appconfig.py"
    if not ap.exists():
        return None
    m = re.search(r'APP_NAME\s*=\s*["\']([^"\']+)',
                  _masked_code_text(ap.read_text(encoding="utf-8", errors="replace")))
    return m.group(1) if m else None

def judge_version_targets(version, app_id, release_names, run_target, declared,
                           local_appdata, path_exists=None):
    """**纯函数**（便于自证）：判"版本目录 ↔ 自启目标"。返回 `(ok, detail, sev_or_None)`。

    `run_target` 为 None = 该工具没有自启项（强断言不适用）；`declared` = 孤儿登记表。
    两段分开：强断言失败 ⇒ FAIL；仅孤儿未登记 ⇒ WARN。
    """
    want_dir = "%s-%s" % (app_id, version) if (app_id and version) else None
    # `path_exists` 可注入：**纯函数才好自证**——真调用用 `Path.exists`，
    # 自证用替身（否则样本得先在磁盘上造出那些目录，样本就被活状态污染了）。
    exists = path_exists or (lambda p: Path(p).exists())
    fails, warns = [], []
    if run_target:
        tgt = Path(run_target.strip().strip('"'))
        if not exists(str(tgt)):
            fails.append("自启目标**不存在**：%s" % tgt)
        else:
            parent = tgt.parent
            ok_release = bool(want_dir) and parent.name.lower() == want_dir.lower() \
                and parent.parent.name.lower() == "release"
            ok_stable = bool(local_appdata) and \
                parent == Path(local_appdata) / app_id / _STABLE_INSTALL_SUBDIR
            if not (ok_release or ok_stable):
                fails.append("自启目标在 `%s`，而当前源码 VERSION=%s ⇒ 既不是 `release/%s/`，"
                             "也不是稳定安装位 `%%LOCALAPPDATA%%\\%s\\%s`"
                             % (parent.name, version, want_dir, app_id, _STABLE_INSTALL_SUBDIR))
    for name in sorted(release_names):
        if want_dir and name.lower() == want_dir.lower():
            continue
        # **只要求登记"改名保留的镜像"**（2026-09-20 发版暴露的口径修正）。
        # `release/` 下必然出现三类目录，别压成一类：
        #   ① 当前版本 `<tool>-<VERSION>`       —— 跳过；
        #   ② **上一版** `<tool>-<某 semver>`   —— **历次构建的自然产物**，
        #      §4.1.42 原话就是"正常的历次构建产物" ⇒ **不要求逐条登记**。
        #      把它算作"待登记孤儿"，登记量会**随发版次数线性增长**、漏登是必然的
        #      （本次发版一次就新增 4 条，正是这个缺口暴露）；
        #   ③ **改名保留的镜像** `_stale_*` / `*.pre-rebuild-*` —— **有意的动作**
        #      （rename-preserve，D11），必须留痕 ⇒ **要求登记**。
        if not (name.startswith("_stale_") or ".pre-rebuild-" in name):
            continue
        entry = declared.get(name)
        if not isinstance(entry, dict) or not str(entry.get("why", "")).strip():
            warns.append("孤儿镜像目录 `%s` **未登记**（须在 ORPHAN_VERSIONS 写明："
                         "当前态 / 是否曾出现 / 如何收敛 / 是否仍被引用）" % name)
    if fails:
        return False, ("；".join(fails) + "。【为什么是硬违规】自启键存的是**全路径**，"
                        "指到哪个目录就永远启动哪一份；源码已经往前走了而自启没跟，"
                        "用户重启后跑的是旧镜像（§4.1.34）。"), "FAIL"
    if warns:
        return False, ("；".join(warns) + "。【等级 WARN】孤儿目录本身不是缺陷，"
                       "**被引用而无人认领**才是。"), "WARN"
    return True, ("自启目标与源码 VERSION 一致（或该工具无自启项）；"
                  "release/ 目录 %d 个，无未登记孤儿" % len(release_names)), None


@check("C-40", "FAIL", "版本目录 ↔ 自启目标必须一致；孤儿版本目录必须登记「是否仍被引用」")
def c40(c: Ctx):
    """见上方注释。读**磁盘 + 注册表**（无需任何人记忆）。

    **措辞纪律**：登记条目一律写 **"当前态 + 是否曾经出现过 + 如何收敛"**——
    "从未发生"不可验证，"发生过且已收敛"可验证且更诚实（ls2t-dev 自曝 l-s2t 正是后者）。
    """
    root = c.dir
    rel_dir = root / "release"
    rels = [p.name for p in sorted(rel_dir.iterdir()) if p.is_dir()] if rel_dir.is_dir() else []
    app_id = None
    ap = root / "src" / "template" / "appconfig" / "appconfig.py"
    if ap.exists():
        m = re.search(r'APP_ID\s*=\s*["\']([^"\']+)',
                      _masked_code_text(ap.read_text(encoding="utf-8", errors="replace")))
        app_id = m.group(1) if m else None
    if not app_id:
        app_id = root.name if rels else None
    version, where = tool_version(root)
    run_values = _run_values()
    app_name = _read_app_name(root)
    local_appdata = os.environ.get("LOCALAPPDATA", "")
    run_key, run_target, run_how, run_notes = select_run_entry(
        run_values, root=root, app_id=app_id, app_name=app_name, local_appdata=local_appdata)
    if not rels and run_key is None:
        return True, "扫描面：release/ 与候选 Run 项都不存在（判据不适用）"
    ok, detail, sev = judge_version_targets(version, app_id, rels, run_target,
                                            ORPHAN_VERSIONS, local_appdata)
    detail = ("扫描面：release/ %d 个目录 / 源码 VERSION=%s（%s）/ "
              "Run[%s]=%s（选键腿=%s；候选 APP_NAME=%r, APP_ID=%r）；%s"
              % (len(rels), version, where or "未找到",
                 run_key or "无命中", run_target or "（无）", run_how, app_name, app_id, detail))
    if run_notes:
        detail += "；[注] " + "；".join(run_notes)
    for name, why in orphan_entry_problems():
        detail += "；[BROKEN] 孤儿登记条目不合规：%s —— %s" % (name, why)
        sev = "FAIL"
    return (ok, detail) if sev is None else (ok, detail, sev)


# ---------------------------------------------------------------- C-41
# **退出确认的"链路不可用"分支，必须固定为"不停服务"**（lead 2026-09-19 定，源头是他批错过一处）。
# 理由一句话：**那个勾选是用户在"有确认框"的语境下保存的；链路坏掉时用户根本没被问过**。
# 若沿用，就变成 **"辅助机制坏掉 ⇒ 在无人确认的情况下停掉用户正在用的服务"**——正是本轮的母题。
# 标准形态 = dsh/ocx 的**硬编码 `False`**；reme 与 l-s2t 原本按已存配置走，已改（并在原地留下"曾偏离"）。
# **为什么现在就要写成判据**：将来 `tray_kit` 要做统一形态，**统一之后极容易长回去**——
#   判据立在这里，统一件落地那天它自己就会被验。
#
# **可判性**：只看**降级分支**（`except` 处理器 + `if <x> is None:` 分支）里那段"喂给退出决策"
#   的语句；若它**读持久化配置**（`CFG`/`cfg`/`load_config_dict`/`config` 任一）**并且**涉及
#   破坏性开关键（`quit_stop*`/`quit_apply*`/`stop_tunnels`/`stop_reme`/`stop_service`）⇒ 红。
#   **原生框那一支不算**：那时用户**确实被问到了**（只是没有勾选框）⇒ 按已存配置走是合法的，
#   两条分支因此保持可分（与 reme 代码里的注释同一条口径）。
_QUIT_FUNC_RE = re.compile(r"quit", re.I)
_DESTRUCTIVE_QUIT_KEYS = ("quit_stop", "quit_apply", "stop_tunnels", "stop_reme",
                          "stop_service", "stop_dsh")
_CONFIG_READ_TOKENS = ("CFG", "cfg", "load_config_dict", "config")
_QUIT_BRANCH_NOTE = ("降级分支不得沿用已存勾选：**用户这次没被问过** —— "
                     "\"没问到\"与\"用户选了\"必须分开")


def _quit_stmt_feeds_decision(node) -> bool:
    """这条语句是否在决定"退出时动不动服务/应用更新"。"""
    if isinstance(node, ast.Return):
        return True
    if isinstance(node, ast.Assign):
        for t in node.targets:
            for n in ast.walk(t):
                if isinstance(n, ast.Name) and re.search(r"stop|quit", n.id, re.I):
                    return True
    return False


def _reads_destructive_config(node) -> bool:
    seg = ast.unparse(node)
    return (any(k in seg for k in _DESTRUCTIVE_QUIT_KEYS)
            and any(c in seg for c in _CONFIG_READ_TOKENS))


def check_quit_fallback(root: Path, sub: str = "src"):
    """见上方注释。返回 `(ok, detail)`；扫描面 = `<sub>/**/*.py`。"""
    base = root / sub
    if not base.is_dir():
        return True, "扫描面：无 %s/（判据不适用）" % sub
    bad, funcs, branches = [], 0, 0
    for f in sorted(base.rglob("*.py")):
        if any(part in _PY_SKIP_DIRS for part in f.parts):
            continue
        try:
            tree = ast.parse(_masked_code_text(f.read_text(encoding="utf-8", errors="replace")))
        except (OSError, SyntaxError):
            continue
        rel = f.relative_to(root).as_posix()
        for fn in ast.walk(tree):
            if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not _QUIT_FUNC_RE.search(fn.name):
                continue
            funcs += 1
            # ① 降级链里的 except 处理器
            for h in [n for n in ast.walk(fn) if isinstance(n, ast.ExceptHandler)]:
                for st in h.body:
                    branches += 1
                    if _quit_stmt_feeds_decision(st) and _reads_destructive_config(st):
                        bad.append("%s:%d `%s()` 的 `except` 分支用**已存配置**决定是否停服务/应用更新"
                                   "（`%s`）" % (rel, st.lineno, fn.name,
                                                 ast.unparse(st).strip()[:60]))
            # ② `if <x> is None:` 这一支（"链路不可用"的显式写法）
            for node in ast.walk(fn):
                if not isinstance(node, ast.If) or "None" not in ast.unparse(node.test):
                    continue
                for st in node.body:
                    branches += 1
                    if _quit_stmt_feeds_decision(st) and _reads_destructive_config(st):
                        bad.append("%s:%d `%s()` 的 `if %s` 分支用**已存配置**决定是否停服务/应用更新"
                                   "（`%s`）" % (rel, st.lineno, fn.name,
                                                 ast.unparse(node.test).strip()[:30],
                                                 ast.unparse(st).strip()[:60]))
    if bad:
        return False, ("%d 处：%s。【为什么是硬违规】%s。辅助机制坏掉**不得**触发破坏性动作"
                       "——`False` 是**硬编码**的那一侧，与 dsh/ocx 的 `return True, False` 同形"
                       % (len(bad), "；".join(bad[:4]), _QUIT_BRANCH_NOTE))
    return True, ("扫描面：%s/**/*.py；退出相关函数 %d 个、降级分支 %d 处，**无一处沿用已存勾选**"
                  "（%s）" % (sub, funcs, branches, _QUIT_BRANCH_NOTE))


@check("C-41", "FAIL", "退出确认的「链路不可用」分支必须固定为不停服务（不得沿用已存勾选）")
def c41(c: Ctx):
    """见上方注释。**原生框那一支不算违规**（那时用户确实被问到了）。"""
    return check_quit_fallback(c.dir)


@template_check("C-41", "FAIL", "模板派发件里的同一形态（模板正本只跑一次）")
def c41_template(c: Ctx):
    return check_quit_fallback(c.dir, "template")


# ---------------------------------------------------------------- C-42
# **重定向位置上的 `dev/null`**（lead 2026-09-19 定，收窄版；来自 ls2t-dev 挖到的一个很深的事故）。
# **事故链**：他用 **bash heredoc** 打补丁，`nul` 在**到达 Python 之前**被改写成 `/dev/null`
#   （同时 LF→CRLF）：
#       powershell -NoProfile -Command "Start-Sleep -Milliseconds {tick_ms}" >/dev/null 2>nul
#   **实测影响**：`rc=0` 但 **0.03s**、stderr 报"系统找不到指定的路径" ⇒ **`powershell` 根本没执行、
#   睡眠没发生**（对照：正确写法 **0.68s**、stderr 空）。于是等待循环里 `tries` 以 `tasklist` 的
#   极限速度狂涨、**120 拍几秒烧完**，`:giveup` 在旧进程没退时就放弃，
#   **而日志仍打印 `120 polls x 1000ms (nominal budget 120s)`**。
# **三层判据都看不见**：C-22（仍是 ASCII + CRLF）、C-33（找 `ping`）、`test_update_safety`
#   （根本走不到那条重定向）。**而他的自证是假绿**——他比对的是**同一个字面量**，
#   被**同一条规则**一起改写、一起错。
#
# **为什么写成"重定向位置"而不是"全文不得出现 `dev/`"**（lead 明确要求收窄）：
#   注释里的路径（`H:/Tools/dev/…`）与 URL（`/dev/`）会**误报**；收窄到重定向位置后**零误报**
#   —— Windows 上**没有任何合法理由**在重定向位置出现 `dev/null`。
# **等级 FAIL**：一旦出现，那条命令**根本没执行**，而外围全是绿的。
_DEVNULL_REDIRECT = re.compile(">" + chr(92) + "s*/?dev/null" + chr(92) + "b", re.I)   # chr(92) 构造反斜杠：绝不过转义层（今天已被它坑三次）


def _redirect_text(p: Path, text: str) -> str:
    """取"会被执行的那部分文本"：`.py` 掩掉注释/docstring（**保留其余字符串**——渲染 bat 的
    模板正是字符串，那才是要查的）；`.bat`/`.cmd` 逐行丢掉 `rem` / `::`。

    ⚠️ 与 C-33 同一条豁免边界（§4.1.37）：**散文不算**。否则**本条判据自己的说明文字**
    （里面就写着那行错误写法）会把自己判红——那是今天已经犯过两次的错误。
    """
    if p.suffix.lower() == ".py":
        return _masked_code_text(text)
    kept = []
    for line in text.splitlines():
        s = line.strip().lower()
        if s.startswith("rem ") or s == "rem" or s.startswith("::"):
            continue
        kept.append(line)
    return "\n".join(kept)


def check_devnull_redirect(root: Path):
    """`root` 下的 `.py`/`.bat`/`.cmd`：**重定向位置不得出现 `dev/null`**。

    ⚠️ **扫描面按绝对路径排除仪器自身**（与 C-33 同一条，§4.1.37）：
    本判据的**正样本**里就必然写着那个被禁形态（否则它没有区分力）——
    不排除就是“**判据把自己的自证样本当成违规**”。这一次它真的发生了：
    实现当天就在 `conformance_check.py:4087` 报了两处（都是自己的样本）。
    """
    self_path = Path(__file__).resolve()
    hits, scanned, excluded = [], 0, []
    files = [p for p in root.rglob("*")
             if p.is_file() and p.suffix.lower() in (".py", ".bat", ".cmd")
             and not any(part in _PY_SKIP_DIRS for part in p.parts)]
    for p in sorted(files):
        if p.resolve() == self_path:
            excluded.append(p.relative_to(root).as_posix())
            continue
        scanned += 1
        try:
            text = _redirect_text(p, p.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
        rel = p.relative_to(root).as_posix()
        for n, m in enumerate(_DEVNULL_REDIRECT.finditer(text), 1):
            line = text[:m.start()].count("\n") + 1
            frag = text[m.start():m.start() + 40].splitlines()[0]
            hits.append("%s:%d(命中%d) `%s`" % (rel, line, n, frag))
    if hits:
        return False, ("%d 处在**重定向位置**出现 `dev/null`：%s。【为什么是硬违规】"
                       "Windows 上 `>` 后面跟 `/dev/null` 会让该命令**根本不执行**"
                       "（实测 `rc=0` 但 0.03s、stderr 报「系统找不到指定的路径」；正确写法 0.68s）"
                       "——而外围判据全是绿的：字节卫生看不见、C-33 找的是 `ping`、"
                       "运行期测试走不到那条重定向。【正确形态】Windows 上一律 `>nul 2>nul`。"
                       "【扫描面】%d 个 .py/.bat/.cmd%s" % (len(hits), "；".join(hits[:6]), scanned,
                        ("；排除仪器自身 " + ", ".join(excluded)) if excluded else ""))
    return True, ("重定向位置无 `dev/null`。扫描面：%d 个 .py/.bat/.cmd%s（`.py` 掩掉注释/docstring、"
                  "保留其余字符串——渲染 bat 的模板正是字符串）"
                  % (scanned, ("；排除仪器自身 " + ", ".join(excluded)) if excluded else ""))


@check("C-42", "FAIL", "重定向位置不得出现 `dev/null`（Windows 上该命令根本不执行）")
def c42(c: Ctx):
    """见上方注释。**收窄到"重定向位置"**：注释里的 `H:/Tools/dev/…` 与 URL 不算。"""
    return check_devnull_redirect(c.dir)


@template_check("C-42", "FAIL", "模板派发件里的同一形态（模板正本只跑一次）")
def c42_template(c: Ctx):
    return check_devnull_redirect(c.dir)


# ---------------------------------------------------------------- C-43
# **`if` **条件**里的 `:~` 子串扩展**（lead 2026-09-19 定；边界由 ls2t-dev 钉准）。
# **危险的只有一种形态**：**同一行条件里**带 `:~` 尾/子串扩展（`:~-1` / `:~0,-1`）——
#   它在变量未定义时把字面量塞进引号，cmd 报语法错并**中止整个脚本**。
# **嵌套 `if` 本身无害**：`local-speak2text/build.bat:84`
#       if defined RUNNING_DIR if /i "%RUNNING_DIR%"=="%TARGET_DIR%" (
#   **含 `:~` 次数 = 0** ⇒ 只是普通 `%VAR%` 展开，未定义时得 `""`、语法仍成立 ⇒ **判绿**。
#   （按"打嵌套 `if`"的宽版写，这一行就是**现成的假阳性**——而它就在我们自己的仓里。）
#
# **条件 vs 动作**：`if defined X set "Y=%X:~0,-1%"`（dsh/ocx `build.bat:87`）里，
#   `:~` 落在**动作**（`set`）一侧、且被 `if defined` 守着 ⇒ 未定义时展开为空、无害 ⇒ **判绿**。
#   判据因此必须把"同一行里 `:~` 出现在**动作关键字之前**"当作"在条件里"。
#   **动作关键字集合**：`set` / `call` / `echo` / `goto` / `exit` / `for` / `rem`。
_IF_COND_TILDE = re.compile(r"^\s*if\b", re.I)
_ACTION_KW = re.compile(r"(?i)(?:^|\s)(set|call|echo|goto|exit|for|rem)\s")
_ACTION_KW_STRICT = re.compile(r"(?i)(?:^|\s)set\s")


def check_if_substr_expansion(root: Path):
    """`root` 下的 `.bat`/`.cmd`：**同一行 `if` 条件里不得出现 `:~` 子串扩展**。"""
    hits, scanned = [], 0
    files = [p for p in root.rglob("*")
             if p.is_file() and p.suffix.lower() in (".bat", ".cmd")
             and not any(part in _PY_SKIP_DIRS for part in p.parts)]
    for p in sorted(files):
        scanned += 1
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = p.relative_to(root).as_posix()
        for n, line in enumerate(text.splitlines(), 1):
            s = line.strip()
            if s.lower().startswith("rem ") or s.startswith("::"):
                continue
            if not _IF_COND_TILDE.match(line) or ":~" not in line:
                continue
            # 动作关键字之前的 `:~` 才算"在条件里"（之后的属动作一侧，见上方注释）
            act = _ACTION_KW_STRICT.search(line)
            cond_part = line[:act.start()] if act else line
            if ":~" in cond_part:
                hits.append("%s:%d `%s`" % (rel, n, line.strip()[:70]))
    if hits:
        return False, ("%d 处在 **`if` 条件里**使用 `:~` 子串扩展：%s。【为什么是硬违规】"
                       "`%%` 展开发生在 `if` 求值**之前**，变量未定义时该展开会把字面量塞进引号，"
                       "cmd 报 `The syntax of the command is incorrect.` 并**中止整个脚本**"
                       "（不是跳过那一行）。【正确形态】用 `for %%%%d in (\"%%VAR%%\") do set \"VAR=%%%%~fd\"`"
                       "——`%%%%~f` 在解析期不做子串扩展，未定义时也不会拼出坏引号。"
                       "【边界】**嵌套 `if` 本身无害**（`if defined X if /i \"%%X%%\"==\"%%Y%%\" (` 判绿）；"
                       "`:~` 落在**动作**一侧（`if defined X set \"Y=%%X:~0,-1%%\"`）同样判绿。"
                       "【扫描面】%d 个 .bat/.cmd" % (len(hits), "；".join(hits[:5]), scanned))
    return True, ("`if` 条件里无 `:~` 子串扩展。扫描面：%d 个 .bat/.cmd"
                  "（嵌套 if 与「动作一侧的 :~」都按绿处理——后者被 `if defined` 守着且展开为空）"
                  % scanned)


@check("C-43", "FAIL", "`if` 条件里不得用 `:~` 子串扩展（未定义时会中止整个脚本）")
def c43(c: Ctx):
    """见上方注释。**宽版（凡嵌套 `if` 就报）会在我们自己的仓里立刻假阳性**，故按窄版写。"""
    return check_if_substr_expansion(c.dir)


@template_check("C-43", "FAIL", "模板派发件里的同一形态（模板正本只跑一次）")
def c43_template(c: Ctx):
    return check_if_substr_expansion(c.dir)


# ---------------------------------------------------------------- C-44
# **bat 里的外部命令必须用绝对路径**（lead 2026-09-19 定；事故由 reme-dev 撞到）。
# **机制**：`where find` -> **`<third-party>\Git\usr\bin\find.exe`**（排在 System32 前面）。
#   等待循环用 `find /i "{exe}" 文件` 判"旧进程还在不在"，而 **GNU `find` 把 `smss.exe`
#   当文件名 ⇒ 恒返回 1** ⇒ 循环每次判"旧进程已退出" ⇒ 直接去覆盖**仍在运行的 exe**
#   （文件被锁 ⇒ robocopy 默认百万次重试）。`ping` 同理（GNU 的 `-n` 是 numeric，不是次数）。
# **与 `dev/null` 同一母题**：**环境悄悄提供一个同名但语义不同的程序，代码走进错分支，
#   而且不报错**。
#
# **闭集**（只收这 8 个）：`find` / `findstr` / `ping` / `tasklist` / `robocopy` / `where` /
#   `reg` / `timeout`——**只在发现新的同名冲突时才扩集**，**不写成"所有外部命令"**
#   （那会噪声化，且"所有命令"无法用一条正则判准）。理由：这 8 个都有（或有）GNU/第三方同名物。
# **只判"命令位置"**：行首、或 `|`/`&`/`(`/`^` 之后的第一个 token；`rem`/`::` 行不算。
#   ⇒ 这样不会误伤散文（`update_helper` 的 `rem` 里成篇讨论 `find`/`ping`）。
# **合规形态**：token 里含路径分隔符（`%SystemRoot%\System32\find.exe`、`C:\...\x.exe`、
#   `\\srv\share\x.exe`）即算绝对。
_BARE_NAME_CLOSED_SET = ("find", "findstr", "ping", "tasklist", "robocopy", "where", "reg",
                         "timeout")
_BAT_CMD_SPLIT = re.compile(r"[|&(^]")
_BAT_TOKEN = re.compile(r"\s*([^\s]+)")
# §4.1.56 段首盲区：`if exist X findstr …` 的段首是 `if`，命令 token 在其后。
_IF_COND_KW = ("errorlevel", "exist", "defined", "cmdextversion")


def _bat_cmd_tokens(seg):
    """段内**命令位置**的候选 token。

    基础形态 = 段首 token（行首 / `|`/`&`/`(`/`^` 之后）——C-44 1.9.10 的原有语义。
    补腿（§4.1.56）：段首是 `if` 时，`if [not] [/i] <条件> <命令>` 的命令 token 也是命令位置。
    **只对 `if` 段做条件推进，不做全空白切分** —— 后者会把 `echo find`、`call :x find`
    这类合法行判红（合成电池实测 6/9 误伤），违反 §4.1.33。
    """
    toks = seg.split()
    if not toks:
        return
    yield toks[0]
    if toks[0].lower() != "if":
        return
    i = 1
    while i < len(toks) and toks[i].lower() == "not":
        i += 1
    if i < len(toks) and toks[i].lower() == "/i":
        i += 1
        while i < len(toks) and toks[i].lower() == "not":
            i += 1
    if i >= len(toks):
        return
    kw = toks[i].lower()
    if kw in _IF_COND_KW:
        i += 2                      # 关键字 + 1 个实参（errorlevel N / exist F / defined V）
    elif "==" in toks[i]:
        i += 1                      # if [not] str1==str2
    else:
        return                      # 未知条件形态 ⇒ 保守不动，宁漏不误
    if i < len(toks):
        yield toks[i]


def check_bat_absolute_cmds(root: Path):
    """`root` 下的 `.bat`/`.cmd`：闭集里的命令必须用绝对路径（**只看命令位置**）。"""
    hits, scanned = [], 0
    files = [p for p in root.rglob("*")
             if p.is_file() and p.suffix.lower() in (".bat", ".cmd")
             and not any(part in _PY_SKIP_DIRS for part in p.parts)]
    for p in sorted(files):
        scanned += 1
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        rel = p.relative_to(root).as_posix()
        for n, line in enumerate(text.splitlines(), 1):
            s = line.strip()
            if not s or s.lower().startswith("rem ") or s.lower() == "rem" or s.startswith("::"):
                continue
            for seg in _BAT_CMD_SPLIT.split(s):
                for raw in _bat_cmd_tokens(seg):
                    tok = raw.strip('"').strip().lstrip("'").rstrip("'")
                    base = tok.split("\\")[-1].split("/")[-1].lower()
                    base = base[:-4] if base.endswith(".exe") else base
                    if base in _BARE_NAME_CLOSED_SET and "\\" not in tok and "/" not in tok:
                        hits.append("%s:%d `%s`" % (rel, n, tok[:40]))
    if hits:
        return False, ("%d 处以**裸名**调用闭集命令：%s。【为什么是硬违规】PATH 的顺序不是我们"
                       "能假设的（实测 `where find` -> `<third-party>\\Git\\usr\\bin\\find.exe`，"
                       "排在 System32 之前）：GNU `find` 语义不同、**恒返回非零**，于是"
                       "\u201c旧进程还在不在\u201d这条判断**静默走错分支**，代码去覆盖仍在运行的 exe。"
                       "**同一个母题**：环境提供同名异物 ⇒ 走进错分支且不报错。"
                       "【正确形态】`%%SystemRoot%%\\System32\\find.exe`（或 `C:\\...` 绝对路径）。"
                       "【闭集】find/findstr/ping/tasklist/robocopy/where/reg/timeout——"
                       "只收这 8 个，只在发现新同名冲突时扩集。【扫描面】%d 个 .bat/.cmd"
                       % (len(hits), "；".join(hits[:6]), scanned))
    return True, ("闭集命令均为绝对路径（只看命令位置；`rem`/`::` 不计）。扫描面：%d 个 .bat/.cmd"
                  % scanned)


@check("C-44", "FAIL", "bat 里的外部命令（闭集 8 个）必须用绝对路径，不得裸名")
def c44(c: Ctx):
    """见上方注释。**C-33 管"ping 当节拍"、本条管"裸名 ping"——两者独立，不互相顶替。**"""
    return check_bat_absolute_cmds(c.dir)


@template_check("C-44", "FAIL", "模板派发件里的同一形态（模板正本只跑一次）")
def c44_template(c: Ctx):
    return check_bat_absolute_cmds(c.dir / "template")


@check("C-33", "FAIL", "禁拿 `ping` 当等待节拍（依赖网络配置，实测差 9 倍）")
def c33(c: Ctx):
    """见 `check_ping_tick` 上方注释。工具侧扫全仓 `.py`/`.bat`/`.cmd`。"""
    return check_ping_tick(c.dir)


@template_check("C-33", "FAIL", "模板派发件里的同一形态（模板正本只跑一次）")
def c33_template(c: Ctx):
    """模板侧只扫 `modules/**`——那是会被拷进工具的正本代码（含渲染 bat 的 `.py` 模板）。"""
    return check_ping_tick(c.dir / "template")


# ---------------------------------------------------------------- C-36
# 归一化算子的**性质断言**（lead 提议，2026-09-19）。为什么用性质、不用冻结哈希：
# 冻结某个文件的哈希，会在那个文件正常演进时误报；而**"行尾不敏感"是算子的定义性质**，
# 与样本文件无关。另外必须有**判别控制**——否则"恒返回常数"的实现也能通过。
#
# 背景（复核员用自己的实现算出假红 `e636cb41bf50`）：同一份内容的三种行尾（LF/CRLF/CR）
# 必须得到**同一个**哈希；而 naive 的 `split("\n")` 会给出不同的值（CRLF 的行尾会带 `\r`）。
# ⚠️ 下面那个 `_naive_split_hash` 是**判别控制**，不是"第二套判据"（设计纪律 ⑦）：
#    它的职责是**必须算出不同的值**，用来证明本条判据有区分力。
_NAIVE_META = re.compile(r"^\s*#\s*TEMPLATE-")


def _naive_split_hash(text):
    """判别控制：与 `sha256_text` 只差一个算子（`split("\\n")` 而非 `splitlines()`）。"""
    import hashlib
    return hashlib.sha256("\n".join(
        l for l in text.split("\n") if not _NAIVE_META.match(l)).encode("utf-8")).hexdigest()


def eol_insensitive_ok(fn, text):
    """性质：`fn` 对同内容的 LF/CRLF/CR 三种行尾给出**同一个**哈希，且**不等于** naive 控制值。"""
    base = text.replace("\r\n", "\n").replace("\r", "\n")
    got = {"LF": fn(base),
           "CRLF": fn(base.replace("\n", "\r\n")),
           "CR": fn(base.replace("\n", "\r"))}
    naive = _naive_split_hash(base.replace("\n", "\r\n"))
    uniq = set(got.values())
    ok = len(uniq) == 1 and list(uniq)[0] != naive
    detail = "三种行尾 %s | 判别控制(naive split) %s -> %s" % (
        "/".join("%s=%s" % (k, v[:12]) for k, v in got.items()), naive[:12],
        "行尾不敏感且有区分力" if ok else "**不满足**（或与 naive 同值 ⇒ 无区分力）")
    return ok, detail


@template_check("C-36", "FAIL", "归一化算子必须行尾不敏感（性质断言 + 判别控制）")
def c36_template(c: Ctx):
    """模板侧性质判据：**断言性质，不描述算子**——这样收方不必读懂散文，改坏了会先响。

    扫描面（设计纪律 ⑥）：算子名 + 样本文件 + 三种变体的哈希 + 控制值，全部打印。
    """
    import importlib.util
    mods = c.dir / "template"
    samples = sorted(p for p in mods.rglob("*.py") if p.is_file()) if mods.exists() else []
    if not samples:
        return False, "扫描面：模板 modules/ 下 0 个 .py，取不到样本（判据不适用）"
    sc_path = Path(__file__).resolve().parent / "sync_check.py"
    try:
        spec = importlib.util.spec_from_file_location("_tpl_sync_check_c36", sc_path)
        sc = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(sc)
    except Exception as exc:                       # noqa: BLE001
        return False, "扫描面：import sync_check 失败：%r" % (exc,)
    text = samples[0].read_text(encoding="utf-8", errors="replace")
    ok, detail = eol_insensitive_ok(sc.sha256_text, text)
    return ok, ("扫描面：算子=sync_check.sha256_text（%d 个候选 .py 取第 1 个）样本=%s | %s"
                % (len(samples), samples[0].relative_to(c.dir).as_posix(), detail))


# ---------------------------------------------------------------- C-2 / C-37
# C-2 = **活实例对自己的 exe 持一个"拒绝删除"句柄**（lead 2026-09-19 批准，helpers-dev 实测）。
# 它把"别删正在运行的实例目录"从**纪律**升级成**内核强制**：持句柄时 `unlink` /
# `rmtree(父目录)` / `rename(父目录)` 全部失败（winerror 32 / 32 / 5），失败方向是
# **大声失败**而不是静默掏空目录——后者正是 2026-09-19 那次事故的形态。
# 判据分两半，缺一不可：
#   **静态半**：模板 `paths.py` 必须提供原语，且 README 必须有 MUST-WIRE 声明
#              （否则四家拷走了也**没人调用**——那正是 C-27 存在的理由）；
#   **性质半**：**实测**原语真的挡得住（不是"注释里说它能挡"）。用临时文件，不碰真 exe。
def c2_property(hold_no_delete):
    """性质断言（返回 `(ok, detail)`）：持句柄时 `unlink` 与 `rmtree(父目录)` **必须失败**。

    **判别控制**：还断言"释放句柄后同一个 `unlink` **必须成功**"——没有这一半，
    一个"永远打不开任何文件"的实现也能通过前一半（判据就没有区分力）。
    """
    import ctypes
    import shutil
    import tempfile

    d = Path(tempfile.mkdtemp(prefix="c37_c2_"))
    try:
        f = d / "victim.exe"
        f.write_bytes(b"MZ")
        h = hold_no_delete(f)
        if not h:
            return False, "原语返回空句柄——拿不到句柄就无从验证性质"
        blocked = []
        for label, fn in (("unlink", f.unlink), ("rmtree(父目录)", lambda: shutil.rmtree(d))):
            try:
                fn()
                blocked.append("%s=**未被挡住**" % label)
            except OSError as exc:
                blocked.append("%s=winerror %s" % (label, getattr(exc, "winerror", None)))
        ctypes.WinDLL("kernel32", use_last_error=True).CloseHandle(ctypes.c_void_p(h))
        try:
            f.unlink()
            after, released_ok = "释放后 unlink 成功（控制组）", True
        except OSError as exc:
            after = "释放后 unlink **仍失败** winerror %s（控制组不成立）" % getattr(exc, "winerror", None)
            released_ok = False
        ok = released_ok and all("winerror" in b for b in blocked)
        return ok, "持句柄时 %s；%s" % ("，".join(blocked), after)
    finally:
        if not _rmtree_strict(d):        # C-30：删完回读，判据自己不许留残留
            return False, "临时目录未清掉（判据自己泄漏）：%s" % d


@template_check("C-37", "FAIL", "C-2 拒绝删除句柄：原语在位 + 删除必须被内核挡住（性质实测）")
def c37_template(c: Ctx):
    """静态半（原语 + MUST-WIRE）+ 性质半（真的挡得住）——两半都过才算过。

    **为什么性质半不能省**：`hold_no_delete` 的全部价值在于"内核会不会拒绝"，
    而那是**运行时事实**；共享位写错（比如顺手带上 `FILE_SHARE_DELETE`）在源码上
    完全看不出来，只有真的去 `unlink` 一次才知道。这正是"能实测的就别推断"。
    """
    py = c.dir / "template" / "paths" / "paths.py"
    rd = c.dir / "template" / "paths" / "README.md"
    missing = []
    if not py.is_file():
        return False, "扫描面：%s 不存在" % py
    src = py.read_text(encoding="utf-8", errors="replace")
    for name in ("def hold_no_delete", "def hold_exe_delete_guard"):
        if name not in src:
            missing.append("paths.py 缺 %s" % name)
    if not rd.is_file() or "<!-- MUST-WIRE: hold_exe_delete_guard -->" not in rd.read_text(
            encoding="utf-8", errors="replace"):
        missing.append("README 缺 `<!-- MUST-WIRE: hold_exe_delete_guard -->`（没有它，四家拷走了也没人调用）")
    if missing:
        return False, "扫描面：%s / %s | %s" % (py.name, rd.name, "；".join(missing))
    import importlib
    import sys as _sys
    _sys.path.insert(0, str(c.dir))
    try:
        paths = importlib.import_module("template.paths.paths")
    except Exception as exc:                        # noqa: BLE001
        return False, "import 模板 paths.py 失败（判不了，不猜）：%r" % (exc,)
    ok, detail = c2_property(paths.hold_no_delete)
    ctx = ("扫描面：%s 的 hold_no_delete（真实现，不重写）+ README 的 MUST-WIRE | 性质实测：%s"
           % (py.relative_to(c.dir).as_posix(), detail))
    if ok:
        dev_ok = paths.hold_exe_delete_guard(log=lambda _m: None) is False
        if not dev_ok:
            return False, ctx + " | dev 态（未冻结）本应**跳过并放行**，实测却没有"
        ctx += " | dev 态跳过并放行（D3.2 失败方向）"
    return ok, ctx


# ---------------------------------------------------------------- C-31
# 派发件 = 会被"整文件夹"拷进四个工具的模块内容（`modules/<模块>/` 下的 .py/.md）。
# 模板专属件不在其列：`build_release/`（模板自己的构建工具）与 `baseline/`（历史件）。
_DISPATCH_SKIP_DIRS = {"__pycache__", "build_release", "baseline"}
_DISPATCH_EXTS = (".py", ".md")


def _dispatched_files(root: Path):
    mods = root / "template"
    if not mods.is_dir():
        return []
    return [p for p in sorted(mods.rglob("*"))
            if p.is_file() and p.suffix.lower() in _DISPATCH_EXTS
            and not any(part in _DISPATCH_SKIP_DIRS for part in p.parts)]


def _first_lone_lf(blob: bytes) -> int:
    """第一个"前一字节不是 \\r 的 \\n"所在行号（1 基）；没有则返回 0。"""
    line, i = 1, 0
    while i < len(blob):
        if blob[i:i + 1] == b"\n":
            if i == 0 or blob[i - 1:i] != b"\r":
                return line
            line += 1
        i += 1
    return 0


def check_dispatched_eol(root: Path):
    """派发件（`.py`/`.md`）必须全程 CRLF。返回 `(ok, detail)`。

    为什么要有这条：模板是**拷贝式分发**（B4）——**正本的行尾就是四份副本的行尾**。
    正本被某个编辑器整文件写成 LF-only 时：`py_compile` 照旧绿、`sync_check` 照旧
    `[ok]`（两边同为 LF，归一化哈希一致）、C-22 只管 `.bat`/`.cmd`——**没有任何一层
    会报**。实测现场（2026-09-19）：`modules/log_kit/log_kit.py` 被整文件重写成 LF，
    是**读回字节**才发现的。**没人查的一致性问题一定会漂**，所以给它一条可见的 WARN。
    """
    files = _dispatched_files(root)
    if not files:
        return True, "模板 modules/ 下没有 .py/.md（判据不适用）"
    bad = []
    for p in files:
        blob = p.read_bytes()
        crlf = blob.count(b"\r\n")
        lone = blob.count(b"\n") - crlf
        if lone:
            bad.append("%s:%d 行尾是 LF（共 %d 处；CRLF %d 处）"
                       % (p.relative_to(root).as_posix(), _first_lone_lf(blob), lone, crlf))
    if bad:
        return False, ("%d/%d 个派发件不是全程 CRLF：%s。【正确形态】统一 CRLF——"
                       "正本的行尾会被原样拷进四个工具，而 LF-only 不报错、不触发任何"
                       "现有判据（C-22 只管 .bat/.cmd），只能靠本条可见"
                       % (len(bad), len(files), "；".join(bad)))
    return True, "%d 个派发件（.py/.md）全部 CRLF" % len(files)


@template_check("C-31", "WARN", "模板派发件（.py/.md）必须全程 CRLF（C-22 只管 bat/cmd）")
def c31(c: Ctx):
    return check_dispatched_eol(c.dir)


# ---------------------------------------------------------------- C-45
# **工具侧副本的行尾也必须是 CRLF**（lead 2026-09-19 升为本波必办）。
# **为什么必须补这条**：`sync_check` 按 `read_text()` 比内容 ⇒ **CRLF/LF 被归一化**，
#   于是"模板侧把 4 份派发件从 LF 改成 CRLF"**在 `sync_check` 眼里是零效果、照旧 `[ok]`**
#   ——**"CRLF 波完成" 可以与 "零效果 + 全绿" 同时成立**（本轮实测：`icons.py`×3、
#   `service_link.py`×1 属此类）。这与"`sync_check` 剔掉 `# TEMPLATE-*` 行、而缺陷恰好
#   住在那一行里"是**同一族**：**判据看不见的那一层，等于没改**。
# **扫描面**：工具侧 `src/modules/**` 的 `.py`/`.md`（= 模板派发件的副本）。
#   **不扫** `src/*.py`、`tests/`、`tools/`、`CHANGELOG.md` 等**非派发件**——l-s2t 有 24 个
#   非派发 `.py`/`.md` 是 LF-only，那是**各仓自有风格**，不在本条范围（避免误伤）。
# **按字节判**：读 `bytes`，数 `\n` 与 `\r\n`，不看归一化后的文本。
_TOOL_COPY_SKIP = {"__pycache__"}


def check_tool_copy_eol(root: Path, sub: str = "src"):
    """工具侧副本（`<sub>/modules/**` 的 `.py`/`.md`）必须全程 CRLF。"""
    base = root / sub / "template"
    if not base.is_dir():
        return True, "扫描面：无 %s/modules/（该工具不消费模板模块，判据不适用）" % sub
    files = [p for p in sorted(base.rglob("*"))
             if p.is_file() and p.suffix.lower() in _DISPATCH_EXTS
             and not any(part in _TOOL_COPY_SKIP for part in p.parts)]
    if not files:
        return True, "扫描面：%s/modules/ 下没有 .py/.md（判据不适用）" % sub
    bad = []
    for p in files:
        blob = p.read_bytes()
        crlf = blob.count(b"\r\n")
        lone = blob.count(b"\n") - crlf
        if lone:
            bad.append("%s:%d 行尾是 LF（共 %d 处；CRLF %d 处）"
                       % (p.relative_to(root).as_posix(), _first_lone_lf(blob), lone, crlf))
    if bad:
        return False, ("%d/%d 个工具侧副本不是全程 CRLF：%s。【为什么这条必须单独存在】"
                       "`sync_check` 按 `read_text()` 比内容、**行尾被归一化** ⇒ 只改行尾的"
                       "重拷在它眼里是**零效果、照旧 `[ok]`**（实测：icons.py×3 + service_link.py×1）。"
                       "【正确形态】按**字节**统一 CRLF（**不要用 `read_text`/`write_text`**"
                       "——那一对会改掉你要对比的字节）"
                       % (len(bad), len(files), "；".join(bad)))
    return True, "%d 个工具侧副本（%s/modules/** 的 .py/.md）全部 CRLF" % (len(files), sub)


@check("C-45", "WARN", "工具侧副本（src/modules/** 的 .py/.md）必须全程 CRLF（sync_check 看不见行尾）")
def c45(c: Ctx):
    """见上方注释。**按字节判**：`sync_check` 的归一化会吃掉行尾，故这条必须独立存在。"""
    return check_tool_copy_eol(c.dir)


# ---------------------------------------------------------------- C-34
# **§1 登记表「版本」列 == 文件头 `TEMPLATE-VER`**（lead 2026-09-19 批准，本波并入）。
# **为什么**：§1 的列头写着"对外接口（稳定承诺）"，而版本列**从来没有任何东西打过它**
#   ——C-04 只查四工具的 B2 表、模板通道只跑 C-28/31/32/33（§4.1.18 同族：判据存在 ≠
#   被检查对象在范围内）。实测：9 行里 **3 行落后**（`paths` 1.1.3→1.1.4、
#   `update_helper` 1.4.3→1.4.4、`tray_kit` 2.2.0→2.2.1）。**读表的人会按错误的语义
#   理解接口**——不是排版问题。
# **同族第五次**：口径文档 / `:giveup` 日志 / `tray_kit` docstring / §1 版本列 / 今天的登记表
#   ——**文件已自带的事实，不要再手抄一份**。本判据的方向是「**让判据去读产物**」。
# **形态（最简，按 lead 的许可）**：逐行 regex 取 §1 行里的模块路径与"版本列"，
#   与**文件头**的 `TEMPLATE-VER` 比；不符 ⇒ WARN。**表格解析脆就退化**——不追求覆盖别的表。
_C34_ROW = re.compile(r"^\| `(template/[^`]+)` \|")
_C34_VER = re.compile(r"\|\s*([\d]+\.[\d.]+)\s*\|\s*$")


def check_registry_versions(root: Path):
    """§1 登记表的版本列 vs 文件头 `TEMPLATE-VER`。返回 `(ok, detail)`。"""
    doc = root / "合规对照表.md"
    if not doc.exists():
        return True, "扫描面：无 合规对照表.md（判据不适用）"
    bad, checked = [], 0
    for n, line in enumerate(doc.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        m = _C34_ROW.match(line)
        if not m:
            continue
        rel = m.group(1)
        v = _C34_VER.search(line.rstrip())
        if not v:
            continue
        f = root / rel
        if not f.exists():
            continue
        hm = re.search(r"TEMPLATE-VER:\s*([\d.]+)",
                       f.read_text(encoding="utf-8", errors="replace")[:600])
        if not hm:
            continue
        checked += 1
        if hm.group(1) != v.group(1):
            bad.append("合规对照表.md:%d `%s` 表内=%s 文件头=%s"
                       % (n, rel, v.group(1), hm.group(1)))
    if bad:
        return False, ("%d/%d 行登记表版本与文件头不一致：%s。【为什么值得单列】§1 的列头是"
                       "\"对外接口（稳定承诺）\"，**读表的人会按错误的语义理解接口**；"
                       "而这一列此前**没有任何判据打过它**（§4.1.18 同族）。"
                       "【正确形态】以**文件头**为准——**文件已自带的事实不要再手抄一份**"
                       % (len(bad), checked, "；".join(bad)))
    return True, "§1 登记表 %d 行的版本列与文件头 `TEMPLATE-VER` 一致" % checked


@template_check("C-34", "WARN", "§1 登记表版本列 == 文件头 TEMPLATE-VER（手抄副本必然滞后）")
def c34(c: Ctx):
    """见上方注释。**只查 §1 主表**；扩到别的表 = 下轮项（lead 许可的最简形态）。"""
    return check_registry_versions(c.dir)


# ---------------------------------------------------------------- C-35
# **实例隔离的两条腿：文件级 + harness 级**（ls2t-dev 提规格 + 判别力实测，lead 批准）。
# **leg_a（文件级）**：**凡 import src 的测试文件必须自钉数据根**——判
#   `import main|modules|pipeline` 与 env 赋值 / `scratch_dir(` 的**行号先后**。
# **leg_b（harness 级）**：**`build.bat` 必须在测试段整体外套一次数据根钉**
#   （pin 在**测试之前**、清在**测试之后**）。
#
# **判别力（实测，不是"应绿"）**：**关掉 harness 腿 ⇒ reme 11 个全红；打开 ⇒ 四仓 0 FAIL / 0 WARN**。
#   ⇒ **它是有区分力的判据，不是恒绿**（这正是本条敢立的前提）。
# **覆盖面会扩——必须写时点**（否则后人拿旧读数当现状）：**今天只有 reme 有 leg_b**
#   （`scripts/build.bat:22` pin、全程不清、测试 140–244 全在其后）；**l-s2t 已批准补 leg_b、
#   dsh/ocx 已路由** ⇒ 三家落地后 leg_b 覆盖**从 1 家变 4 家**。
# **它同时把一条口径钉成断言**：ls2t-dev 的补丁"今天是 no-op"**不该是一句会过期的陈述**——
#   **两条腿同时在场**，才使 "no-op" 成为**可机械验证的性质**（同族：把靠陈述的换成靠性质的）。
_C35_IMPORT = re.compile(r"^\s*(?:import|from)\s+(main|template|pipeline)\b")
_C35_PIN = re.compile(r"""(os\.environ\[|scratch_dir\s*\(|setdefault\s*\()""")
_C35_PIN_KEY = re.compile(r"DATA_DIR|_CONFIG")
_C35_BAT_PIN = re.compile(r"""(?i)^\s*set\s+"?[A-Z0-9_]*DATA_DIR=""")
_C35_BAT_CLEAR = re.compile(r"""(?i)^\s*set\s+"?[A-Z0-9_]*DATA_DIR=""")
_C35_BAT_TEST = re.compile(r"""(?i)(tests\\|tests/|_test\.py|test_[a-z_]*\.py)""")


def check_instance_isolation(root: Path):
    """两腿：测试文件自钉（leg_a）+ build.bat 整体外套（leg_b）。"""
    a_bad, a_ok = [], 0
    tests_dir = root / "tests"
    if tests_dir.is_dir():
        for p in sorted(tests_dir.rglob("*.py")):
            if "__pycache__" in p.parts:
                continue
            try:
                lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            imp = next((i for i, l in enumerate(lines) if _C35_IMPORT.match(l)), None)
            if imp is None:
                continue
            pin = next((i for i, l in enumerate(lines)
                        if _C35_PIN.search(l) and _C35_PIN_KEY.search(l)), None)
            if pin is not None and pin < imp:
                a_ok += 1
            else:
                a_bad.append("%s:%d import 在 %d 行，而钉数据根在 %s"
                             % (p.relative_to(root).as_posix(), imp + 1, imp + 1,
                                ("%d 行" % (pin + 1)) if pin is not None else "**没有**"))
    b_note, b_ok = "", False
    bats = [p for p in list(root.rglob("build.bat")) + list(root.rglob("build.cmd"))
            if p.is_file() and "__pycache__" not in p.parts]
    # **任一候选满足即可**：只取第一个会漏——实测 reme 根级另有一个 build.bat（无 pin），
    # 判据于是看错了对象。
    for bat in bats:
        if b_ok:
            break
        lines = bat.read_text(encoding="utf-8", errors="replace").splitlines()
        pin = next((i for i, l in enumerate(lines) if _C35_BAT_PIN.match(l)), None)
        first_test = next((i for i, l in enumerate(lines) if _C35_BAT_TEST.search(l)), None)
        last_test = max((i for i, l in enumerate(lines) if _C35_BAT_TEST.search(l)), default=None)
        cleared = (last_test is not None and any(
            _C35_BAT_CLEAR.match(l) and "=%" not in l and l.rstrip().endswith('=""')
            for l in lines[last_test + 1:]))
        if pin is not None and first_test is not None and pin < first_test:
            b_ok = True
            b_note = ("%s 第 %d 行钉、首个测试在第 %d 行%s"
                      % (bat.relative_to(root).as_posix(), pin + 1, first_test + 1,
                         "，其后已清" if cleared else "，**未见清除**（清在末测试之后才算）"))
        else:
            b_note = ("%s 未在测试段整体外套数据根钉（pin 行=%s 首测试行=%s）"
                      % (bat.relative_to(root).as_posix(),
                         (pin + 1) if pin is not None else "无",
                         (first_test + 1) if first_test is not None else "无"))
    # 两腿是**并集**：leg_b 在场即整体盖住（"关掉 harness 腿 ⇒ reme 11 红、打开 ⇒ 4 仓全绿"
    # 只在并集语义下成立）；leg_b 缺席才要求每个 import src 的测试文件自钉。
    if a_bad and not b_ok:
        return False, ("leg_a：%d 个测试文件未自钉（%s）；leg_b：%s。【为什么两条腿都要】"
                       "文件级钉只保证**那一个文件**；harness 级外套保证**整体**，"
                       "**新加一个忘记自钉的测试**只有 leg_b 挡得住。"
                       "【判别力实测】关掉 leg_b ⇒ reme 11 个全红；打开 ⇒ 四仓 0 FAIL / 0 WARN"
                       "（不是恒绿）。【覆盖面时点 2026-09-19】leg_b 目前只有 reme；"
                       "l-s2t 已批准补、dsh/ocx 已路由 ⇒ 落地后覆盖 1 家 → 4 家"
                       % (len(a_bad), "；".join(a_bad[:4]) or "无", b_note))
    return True, ("leg_a %d 个测试文件自钉、leg_b %s" % (a_ok, b_note))


@check("C-35", "WARN", "实例隔离两条腿：测试文件自钉数据根 + build.bat 整体外套一次")
def c35(c: Ctx):
    """见上方注释。**leg_b 的覆盖面会从 1 家扩到 4 家**（时点写在 detail 里）。"""
    return check_instance_isolation(c.dir)


@check("C-32", "FAIL", "禁「读证据 → 删证据 → 报告」的危险顺序（调用边界一失败就先删了证据）")
def c32(c: Ctx):
    """**不可逆动作不得排在"调用边界可能失败的语句"之前**（复核员精确化 + lead 裁定）。

    为什么**不上通用版**："不可逆动作必须排在所有可能抛异常的语句之后"太宽——`log_kit.log()`
    内部是 `try/except Exception: pass`，**本函数不抛**，于是 `quit_watch_loop` 的
    `unlink → log`（模板 + 4 份副本）会被误报 5 处。**假阳性比漏报更伤信任**（纪律 ①）。

    为什么**仍要立**：arity/签名不符、属性不存在、名字未定义这类错误在**进入被调方之前**
    就抛出，被调方内部的 try/except 保护不了它——C-29 的契约冲突下 l-s2t **真的炸了**
    （`TypeError` + marker 已被删 + 提示消失）。修完 C-29 后这类危险退化成潜伏态，
    但下次契约冲突还会以同样方式炸。

    **窄版判据**（复核员定稿）：D（删除，记接收者）+ A（函数内**任意**更早的赋值，右值含
    `read_text`/`read_bytes` 且接收者与 D **AST 相同**）+ R（更晚的 `log` 引用 A 的名字），
    三条同时满足才报。**限定词必须逐条用已知正例回验**（设计纪律 ⑤）："同一语句块"会漏掉正典
    （命中 0）、"最近一条赋值"会落在 `except` 里的 `detail = ""` 上（命中 4、漏 reme）。
    样本 7 条，含 `quit_watch_loop` 那种"删除后写日志但**没有读证据**"的形态（必须放行）。
    """
    return check_evidence_order(c.dir)


@template_check("C-32", "FAIL", "模板派发件（modules/**）里的同一形态（模板正本只跑一次）")
def c32_template(c: Ctx):
    """模板侧只扫 `modules/**`——那才是会被拷进工具的正本代码。

    教训见 §4.1.18：判据存在 ≠ 被检查对象在范围内。模板 `update_helper` 正是这条判据的
    活样本（`pop_failed_update_note` 的"读 → 删 → log"顺序），不扫模板就等于不扫源头。
    """
    return check_evidence_order(c.dir / "template")


def _rmtree_strict(path, tries=10):
    """删 + 回读确认；删不掉就重试，仍删不掉**抛错**（绝不 `ignore_errors` 吞掉）。

    本工具是 C-30 的作者，**自己先得守 C-30**：selftest 的临时目录以前用
    `rmtree(base, ignore_errors=True)` 收尾——那正是本条判红的那种写法（"清理跑过了"
    被当成"清理成功了"）。同一个 `%TEMP%` 前缀泄漏形态，工具自己也会犯。
    """
    import shutil
    import time
    last = ""
    for _ in range(max(1, tries)):
        try:
            shutil.rmtree(path)
        except OSError as exc:
            last = repr(exc)
            time.sleep(0.2)
        if not Path(path).exists():
            return True
    raise OSError("临时目录删不掉（%s）：%s" % (path, last or "still exists"))


def selftest() -> int:
    """C-21..C-33 反向自证：合成样本，正例须点名，反例须放行。"""
    import shutil
    import tempfile
    print(identity_line())   # 自证输出也自证身份：贴出来的 selftest 结果不能是无主的
    base = Path(tempfile.mkdtemp(prefix="conf_selftest_"))
    try:
        cases = []
        for name, init_src, want in (
            ("pos", "from .demo import *  # noqa: F401,F403\n", False),   # 复制 → 应报
            ("neg", "from .demo import set_state\n", True),               # 显式导入 → 放行
        ):
            d = base / name / "src" / "template" / "demo"
            d.mkdir(parents=True)
            (d / "demo.py").write_text(
                "STATE = None\n\n\ndef set_state():\n    global STATE\n    STATE = 1\n",
                encoding="utf-8")
            (d / "__init__.py").write_text(init_src, encoding="utf-8")
            cases.append((name, base / name, want))
        failed = 0
        for name, tool_dir, want in cases:
            ok, detail = c21(Ctx(name, tool_dir))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-21 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail))

        # C-23：标量/容器被 global 重绑 → 报；就地改容器 → 放行
        c23_cases = (
            ("pos_scalar", "STATE = None\n\n\ndef f():\n    global STATE\n    STATE = 1\n", False),
            ("pos_container_rebind", "STATE = {}\n\n\ndef f():\n    global STATE\n    STATE = {\"a\": 1}\n", False),
            ("neg_inplace", "STATE = {}\n\n\ndef f():\n    STATE[\"a\"] = 1\n", True),
        )
        for name, body, want in c23_cases:
            d = base / ("c23_" + name) / "src" / "template" / "demo"
            d.mkdir(parents=True)
            (d / "demo.py").write_text(body, encoding="utf-8")
            (d / "__init__.py").write_text("from .demo import f\n", encoding="utf-8")
            ok, detail = c23(Ctx(name, base / ("c23_" + name)))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-23 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail))

        # C-24：菜单读容器却不在签名里 → 报；进了签名 → 放行；无菜单 → 放行
        menu_pos = ("import pystray\nCFG = {}\n\n\ndef _menu_signature():\n    return (1,)\n\n\n"
                    "def build():\n    return pystray.MenuItem('x', None, enabled=lambda i: CFG.get('a'))\n")
        menu_neg = menu_pos.replace("return (1,)", "return (CFG.get('a'),)")
        c24_cases = (("pos_missing", menu_pos, False), ("neg_covered", menu_neg, True),
                     ("neg_no_menu", "CFG = {}\n", True))
        for name, body, want in c24_cases:
            d = base / ("c24_" + name) / "src"
            d.mkdir(parents=True)
            (d / "main.py").write_text(body, encoding="utf-8")
            ok, detail = c24(Ctx(name, base / ("c24_" + name)))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-24 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail))

        # C-10：判据要能区分"覆盖了"与"绕过了"——四种形态各一个样本
        c10_head = "import sys\nif '--smoke' in sys.argv:\n    pass\n\n\n"
        c10_cases = (
            ("pos_probe_guarded",
             "def smoke():\n"
             "    if not tray_kit.mutex_name_is_valid(APP_ID):\n"
             "        raise RuntimeError('bad mutex name')\n"
             "    return 0\n", True),
            # 未检出（不是确证违规）⇒ WARN
            ("neg_no_guard",
             "def smoke():\n    return 0\n", False, "WARN"),
            ("neg_real_guard_modalfree",
             "def smoke():\n    if not tray_kit.acquire_single_instance(APP_ID):\n"
             "        return 1\n", False),
            ("neg_probe_unchecked",
             "def smoke():\n    tray_kit.mutex_name_is_valid(APP_ID)\n    return 0\n", False),
            # 子串判据会**误收**这一条（名字只出现在注释里）；AST 不会。这就是升级判据的理由。
            ("neg_comment_only",
             "def smoke():\n    # TODO: should call mutex_name_is_valid(APP_ID) here\n"
             "    return 0\n", False, "WARN"),
            # reme 的真实形态：探针**作为参数交给 check() 助手**——值被消费了，必须放行。
            # 旧判据只认 if/while/assert 的 test，这里 guarded=0/plain=0 → 假红灯。
            ("pos_probe_passed_to_check_helper",
             "def smoke():\n"
             "    check('single-instance name valid',\n"
             "          mutex_name_is_valid(APP_ID, mutex_name=SINGLE_INSTANCE_NAME))\n", True),
            # 守卫名**只出现在注释里** + 有正确探针 → 必须放行（reme 那条假红灯的根因）
            ("pos_guard_name_in_comment_only",
             "def smoke():\n"
             "    # 不许用 single_instance_free()：用户实例在跑时它为真\n"
             "    check('ok', mutex_name_is_valid(APP_ID))\n", True),
            # 真跑守卫（AST 调用节点）才 FAIL
            ("neg_real_guard_ast",
             "def smoke():\n    tray_kit.acquire_single_instance(APP_ID)\n", False),
        )
        for case in c10_cases:
            name, body, want = case[:3]
            want_sev = case[3] if len(case) > 3 else None
            d = base / ("c10_" + name) / "src"
            d.mkdir(parents=True)
            (d / "main.py").write_text(c10_head + body, encoding="utf-8")
            res = c10(Ctx(name, base / ("c10_" + name)))
            ok, detail = res[0], res[1]
            sev = res[2] if len(res) == 3 else "FAIL"
            # 设计纪律 ④：**未检出 ≠ 确证违规**。这两种形态（既无探针也无守卫调用节点）
            # 必须是 **WARN**——判据说不出"绕过了"，只能说"不认识这个形态"。
            good = (ok == want) and (want_sev is None or sev == want_sev)
            failed += 0 if good else 1
            print("[selftest] %s  C-10 %s: ok=%s want=%s sev=%s want_sev=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, sev, want_sev, detail[:80]))

        # C-22：字节卫生——三种损坏各一条样本（都会让**某一行**静默失效），合规的必须放行
        c22_cases = (
            ("pos_tab", b"@echo off\r\necho a\tb\r\n", False),
            ("pos_lf_only", b"@echo off\necho ok\n", False),
            ("pos_nonascii", b"@echo off\r\nrem \xd6\xd0\xce\xc4\r\n", False),
            ("pos_mixed_tab_lf", b"@echo off\nset x=1\r\n\tbad\n", False),
            ("neg_clean", b"@echo off\r\necho ok\r\nif errorlevel 1 exit /b 1\r\n", True),
        )
        for name, blob, want in c22_cases:
            d = base / ("c22_" + name)
            d.mkdir(parents=True)
            (d / "build.bat").write_bytes(blob)
            ok, detail = c22(Ctx(name, d))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-22 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail))

        # C-25：路径不存在 → 报；顶层 exit 之后的调用（死代码）→ 报；合规 → 放行
        def _mk_tool(name, bat, extra=()):
            d = base / name
            (d / "tests").mkdir(parents=True, exist_ok=True)
            for rel in extra:
                (d / rel).write_text("x = 1\n", encoding="utf-8")
            (d / "build.bat").write_bytes(bat)
            return d

        c25_cases = (
            ("pos_missing_path", b'@echo off\r\n"%PY%" tests\\gone.py\r\n', (), False),
            ("pos_dead_code", b'@echo off\r\n"%PY%" tests\\t.py\r\nexit /b 1\r\n"%PY%" tests\\t.py\r\n',
             ("tests/t.py",), False),
            ("neg_conditional_exit", b'@echo off\r\nif errorlevel 1 (\r\n  exit /b 1\r\n)\r\n'
                                     b'"%PY%" tests\\t.py\r\n', ("tests/t.py",), True),
        )
        for name, blob, extra, want in c25_cases:
            ok, detail = c25(Ctx(name, _mk_tool("c25_" + name, blob, extra)))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-25 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:90]))

        # C-26：无守卫 start → 报；同行 if exist → 放行；前置 if not exist → 放行
        c26_cases = (
            ("pos_unguarded", b'@echo off\r\nstart "" "C:\\t\\a.exe"\r\n', False),
            ("neg_inline_guard", b'@echo off\r\nif exist "C:\\t\\a.exe" start "" "C:\\t\\a.exe"\r\n', True),
            ("neg_prior_guard", b'@echo off\r\nif not exist "C:\\t\\a.exe" goto dead\r\n'
                                b'start "" "C:\\t\\a.exe"\r\n:dead\r\n', True),
        )
        for name, blob, want in c26_cases:
            ok, detail = c26(Ctx(name, _mk_tool("c26_" + name, blob)))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-26 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:90]))

        # C-27：README 的 MUST-WIRE 符号在工具代码里查引用
        for name, main_src, want in (("pos_unwired", "x = 1\n", False),
                                     ("neg_wired", "def f():\n    sweep_stale()\n", True)):
            d = base / ("c27_" + name) / "src" / "template" / "demo"
            d.mkdir(parents=True)
            (d / "README.md").write_text("<!-- MUST-WIRE: sweep_stale -->\n", encoding="utf-8")
            (base / ("c27_" + name) / "src" / "main.py").write_text(main_src, encoding="utf-8")
            ok, detail = c27(Ctx(name, base / ("c27_" + name)))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-27 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:90]))

        # C-28：.md 里的真 TAB 必须被点名（这是本人踩过的形态）。
        # ⚠️ 用**显式字节值**构造，不写 b"...TAB..."——写下这段样本时，正是 `TAB` 被当转义
        # 解释、把真 TAB 落进了源文件（本 J 坑同一天第三次出现，且出现在"检测 TAB"的检查里）。
        _tab, _crlf = bytes([9]), bytes([13, 10])
        d = base / "c28_pos"
        d.mkdir(parents=True)
        (d / "CHANGELOG.md").write_bytes(b"# x" + _crlf + b"line" + _tab + b"with tab" + _crlf)
        ok, detail = c28(Ctx("c28_pos", d))
        good = ok is False
        failed += 0 if good else 1
        print("[selftest] %s  C-28 pos_md_tab: ok=%s want=False | %s"
              % ("PASS" if good else "FAIL", ok, detail[:70]))
        d = base / "c28_neg"
        d.mkdir(parents=True)
        (d / "CHANGELOG.md").write_bytes(b"# x" + _crlf + b"clean line" + _crlf)
        ok, detail = c28(Ctx("c28_neg", d))
        good = ok is True
        failed += 0 if good else 1
        print("[selftest] %s  C-28 neg_clean_md: ok=%s want=True | %s"
              % ("PASS" if good else "FAIL", ok, detail[:70]))

        # C-11：认形状（tasklist / PowerShell 两种），认不出只 WARN。
        # 用显式字节值构造样本（CRLF 转义在多个 heredoc 里被解释成真字节——本日第 4 次）。

        _crlf = bytes([13, 10])
        _e = base / "c11_none"
        _e.mkdir(parents=True)
        (_e / "build.bat").write_bytes(b"@echo off" + _crlf + b"set APPNAME=my-helper" + _crlf)
        ok, detail, sev = c11(Ctx("c11_none", _e))
        good = (ok is False and sev == "WARN")
        failed += 0 if good else 1
        print("[selftest] %s  C-11 neg_no_detection: ok=%s sev=%s | %s"
              % ("PASS" if good else "FAIL", ok, sev, detail[:60]))
        _p = base / "c11_ps"
        _p.mkdir(parents=True)
        (_p / "build.bat").write_bytes(
            b"@echo off" + _crlf + b"set APPNAME=my-helper" + _crlf
            + b"powershell -NoProfile -Command \"(Get-Process -Name %APPNAME%"
            + b" -ErrorAction SilentlyContinue).Path\"" + _crlf)
        ok, detail = c11(Ctx("c11_ps", _p))
        good = ok is True
        failed += 0 if good else 1
        print("[selftest] %s  C-11 pos_ps_getprocess: ok=%s | %s"
              % ("PASS" if good else "FAIL", ok, detail[:70]))

        # C-11 补齐三条（2026-09-19 lead 点名）：此前**只有** PowerShell 形态与"认不出"两条样本，
        # `tasklist | findstr` 这条**正中靶心**的分支反而没有任何样本兜着——判据改了没人知道。
        _c11 = (
            # ① tasklist 形态的**合规**样本（l-s2t build.bat:86 的真实写法）
            ("pos_tasklist_findstr", b"tasklist /fo csv 2>nul | findstr /i /c:\"%APPNAME%.exe\" >nul",
             True, None),
            # ② **确证违规**：匹配串写成**带版本号**的字面量——只有旧版 exe 会被命中，
            #    当前（无版本号）实例在跑也拦不住构建（D1-02 的真实形态）⇒ FAIL
            ("neg_substring_only", b"tasklist | findstr /i /c:\"%APPNAME%-1.0.exe\"", False, "FAIL"),
            # ③ 看到 tasklist|findstr 但取不出 `/c:"字面量"` ⇒ **形态不认识**，不是违规 ⇒ WARN
            ("neg_no_c_literal", b"tasklist /fo csv | findstr /i \"%APPNAME%\"", False, "WARN"),
            # ④ `.Path` + 目录精确比较（**不带 `-Name`** 的那一族）：比子串匹配更强，
            #    必须放行而不是掉进"认不出形态"的 WARN（对着更强的实现报"判不了"）
            ("pos_ps_path_compare",
             b"powershell -NoProfile -Command \"(Get-Process | Where-Object "
             b"{$_.Path -eq '%CD%\\release\\x\\my-helper.exe'}).Count\"", True, None),
        )
        for name, cmdline, want, want_sev in _c11:
            _d = base / ("c11_" + name)
            _d.mkdir(parents=True)
            (_d / "build.bat").write_bytes(
                b"@echo off" + _crlf + b"set APPNAME=my-helper" + _crlf + cmdline + _crlf)
            res = c11(Ctx(name, _d))
            ok, detail = res[0], res[1]
            sev = res[2] if len(res) == 3 else "FAIL"
            good = (ok == want) and (want_sev is None or sev == want_sev)
            failed += 0 if good else 1
            print("[selftest] %s  C-11 %s: ok=%s want=%s sev=%s want_sev=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, sev, want_sev, detail[:80]))

        # C-29：交给模板件的 log 必须是 print 形态。
        # 命名按"该不该报"写清楚：本文件的样本命名在两代检查里刚好相反
        # （C-25/26 的 pos = 该报、C-11 的 pos = 合规），所以这里不用 pos/neg，
        # 直接用 `_ok` / `_flagged` / `_unused` 三个词，读的人不必猜。
        c29_cases = (
            ("varargs_log_ok",
             "def log(*parts):\n    pass\n\n\nupdate_helper.download_and_prepare(log=log)\n", True),
            # dsh `main.py:120` / ocx `main.py:80` 的**真实形态**：工具侧自建包装，把
            # 任意个位置参数拼成一行再转交 log_kit。**这是正解，不是偏差**——判据的措辞
            # 若让人以为"自建包装"该被消灭，这份样本就是挡它的那道闸。
            ("pos_tool_side_vararg_wrapper",
             "from modules import log_kit\n\n"
             "_LOG_HANDLE = log_kit.make_logger(LOG_DIR)\n\n\n"
             "def log(*parts):\n"
             '    """模板件的日志契约是 print 形态（log("a", b)），这里按契约收参再拼接。"""\n'
             '    _LOG_HANDLE[0](" ".join(str(p) for p in parts))\n'
             "\n\n"
             "def check_update_menu(_icon=None, _item=None):\n"
             "    update_helper.download_and_prepare(latest, APP_DIR, UPDATE_DIR, log=log)\n", True),
            ("single_arg_wired_flagged",
             "def log(message):\n    pass\n\n\ntray_kit.acquire_single_instance(log=log)\n", False),
            ("single_arg_unused_ok",
             "def log(message):\n    pass\n\n\nx = 1\n", True),
            # **值不是函数**这一类必须**不下判**（而非报红）：l-s2t `updater.py:277` 与
            # reme 的真实形态是 `log=` 后面给**日志文件路径**（`log_path` / 常量
            # `HELPER_UPDATE_LOG`）。把它们当"单参 log"报红就是假红——判据只能判
            # "工具内自己定义的那个函数"，别的一律不下判（宁可漏，不造假红）。
            ("path_value_not_a_function_ok",
             "HELPER_UPDATE_LOG = UPDATE_DIR / 'update.log'\n\n\n"
             "update_helper.download_and_prepare(latest, APP_DIR, UPDATE_DIR,\n"
             "                                   log=HELPER_UPDATE_LOG)\n", True),
            ("local_path_var_as_log_ok",
             "log_path = UPDATE_DIR / 'helper.log'\n\n\n"
             "update_helper.pop_failed_update_note(UPDATE_DIR, log=log_path)\n", True),
        )
        for name, main_src, want in c29_cases:
            d = base / ("c29_" + name) / "src"
            d.mkdir(parents=True)
            (d / "main.py").write_text(main_src, encoding="utf-8")
            ok, detail = c29(Ctx(name, base / ("c29_" + name)))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-29 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:100]))

        # C-30 上半：mkdtemp 前缀必须可静态归属，推不出的必须在 TMP_PREFIX_REGISTRY 登记。
        # 命名按该不该报写清楚（与 C-29 同一约定），不靠 pos/neg 猜。
        # `param_prefix_literal_calls_ok` 钉的是 **dsh/ocx/l-s2t 三个工具的真实形态**
        # （`tests/_cleanup.py: scratch_dir(prefix)` 内部 mkdtemp，前缀全在调用点上是字面量）：
        # 少了它，判据的下一版很容易改成"形参=不可枚举"，**一次把三家全判红**。
        _prefix_cases = (
            ("literal_ok",
             "import tempfile\nTMP = tempfile.mkdtemp(prefix='app-test-')\n", True, None),
            ("param_prefix_literal_calls_ok",
             "import tempfile\n\n\n"
             "def scratch_dir(prefix):\n"
             "    return tempfile.mkdtemp(prefix=prefix)\n"
             "\n\n"
             "TMP = scratch_dir('app-test-')\n", True, None),
            ("param_prefix_nonliteral_call_flagged",
             "import tempfile\n\n\n"
             "def scratch_dir(prefix):\n"
             "    return tempfile.mkdtemp(prefix=prefix)\n"
             "\n\n"
             "TMP = scratch_dir(APP_ID + '-test-')\n", False, None),
            # 第二路径（lead 2026-09-19 裁定的"低成本做法"）：**可折叠模块常量**。
            # reme `src/main.py:6 APP_ID = "reme-helper"` + 前缀 `f"{APP_ID}-update-"` 就是这一形态
            # ——能折出来就不该逼作者写登记表。
            ("foldable_module_constant_ok",
             "import tempfile\n"
             "APP_ID = 'app'\n"
             "TMP = tempfile.mkdtemp(prefix=f'{APP_ID}-update-')\n", True, None),
            ("foldable_concat_ok",
             "import tempfile\n"
             "BASE = 'app-'\n"
             "TMP = tempfile.mkdtemp(prefix=BASE + 'test-')\n", True, None),
            # 同名不同值 → 折不出来（宁缺勿猜）⇒ 仍要登记
            ("conflicting_constants_flagged",
             "import tempfile\n"
             "APP_ID = 'one'\n"
             "APP_ID = 'two'\n"
             "TMP = tempfile.mkdtemp(prefix=f'{APP_ID}-update-')\n", False, None),
            ("fstring_prefix_unregistered_flagged",
             "import tempfile\nTMP = tempfile.mkdtemp(prefix=f'{APP_ID}-update-')\n", False, None),
            # 登记表放**文件后半段**也能被认（判据按模块级常量找，不按位置猜）；
            # 键必须与站点 `相对路径:行号` **逐字对上**——对不上就是过期 WARN。
            # 2026-09-19 起值是**三栏结构**：`why` / `reverify` 是必填（白名单 = 关掉覆盖的开关）。
            ("fstring_prefix_registered_ok",
             "import tempfile\n"
             "TMP = tempfile.mkdtemp(prefix=f'{APP_ID}-update-')\n"
             "\n"
             "TMP_PREFIX_REGISTRY = {\n"
             "    'src/main.py:2': {'prefix': 'app-update-',\n"
             "                      'why': 'APP_ID 在本文件有唯一字面量定义',\n"
             "                      'reverify': 'APP_ID 被改名或改成变量时'},\n"
             "}\n", True, None),
            # 旧形态（裸字符串/变量）= **不合规**：只写结果不写"为什么"与"何时过期"。
            ("registry_bare_string_form_flagged",
             "import tempfile\n"
             "TMP = tempfile.mkdtemp(prefix=f'{APP_ID}-update-')\n"
             "TMP_PREFIX_REGISTRY = {'src/main.py:2': 'app-update-'}\n", False, None),
            ("registry_missing_reverify_flagged",
             "import tempfile\n"
             "TMP = tempfile.mkdtemp(prefix=f'{APP_ID}-update-')\n"
             "TMP_PREFIX_REGISTRY = {'src/main.py:2': {'prefix': 'app-update-',\n"
             "                                         'why': 'APP_ID 有唯一字面量'}}\n", False, None),
            ("registry_value_not_literal_flagged",
             "import tempfile\n\n"
             "TMP_PREFIX_REGISTRY = {'src/main.py:4': {'prefix': PREFIX,\n"
             "                                         'why': 'x', 'reverify': 'y'}}\n\n"
             "TMP = tempfile.mkdtemp(prefix=f'{APP_ID}-update-')\n", False, None),
            ("registry_stale_entry_warn",
             "import tempfile\n\n"
             "TMP_PREFIX_REGISTRY = {'src/main.py:99': {'prefix': 'app-old-',\n"
             "                                          'why': '历史站点', 'reverify': '站点位移时'}}\n\n"
             "TMP = tempfile.mkdtemp(prefix='app-test-')\n", False, "WARN"),
        )
        for name, body, want, want_sev in _prefix_cases:
            d = base / ("c30p_" + name) / "src"
            d.mkdir(parents=True)
            (d / "main.py").write_text(body, encoding="utf-8")
            res = c30(Ctx(name, base / ("c30p_" + name)))
            ok, detail = res[0], res[1]
            sev = res[2] if len(res) == 3 else "FAIL"
            good = (ok == want) and (want_sev is None or sev == want_sev)
            failed += 0 if good else 1
            print("[selftest] %s  C-30/prefix %s: ok=%s want=%s sev=%s want_sev=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, sev, want_sev, detail[:100]))

        # 白名单**两栏必填**的自证（2026-09-19，lead 定；复核员先提醒"它是关掉覆盖的开关"）。
        # 判别力靠**两格对照**：真表必须 0 问题（否则校验器在乱咬），坏样本必须被抓住。
        _real_problems = _declared_problems()
        _saved = dict(TMP_DECLARED_PATHS)
        try:
            TMP_DECLARED_PATHS.clear()
            TMP_DECLARED_PATHS["bad-missing-reverify"] = {"why": "只有为什么"}
            _bad1 = _declared_problems()
            TMP_DECLARED_PATHS.clear()
            TMP_DECLARED_PATHS["bad-bare-string"] = "旧的裸字符串形态"
            _bad2 = _declared_problems()
        finally:
            TMP_DECLARED_PATHS.clear()
            TMP_DECLARED_PATHS.update(_saved)
        for label, got, want_empty in (("real_table_clean", _real_problems, True),
                                       ("missing_reverify_caught", _bad1, False),
                                       ("bare_string_form_caught", _bad2, False)):
            good = (not got) if want_empty else bool(got)
            if want_empty:
                good = good and not TMP_DECLARED_PATHS.get("bad-missing-reverify")
            failed += 0 if good else 1
            print("[selftest] %s  C-30/declared %s: problems=%d want_%s | %s"
                  % ("PASS" if good else "FAIL", label, len(got),
                     "0" if want_empty else ">0",
                     (got[0][1][:90] if got else "（无）")))

        # C-30 下半：只有"mkdtemp 根目录被 ignore_errors 吞掉"才报；子目录/固定路径要放行。
        _cleanup_ok = ("import shutil, logging, tempfile\n"
                       "TMP = tempfile.mkdtemp(prefix='t-')\n"
                       "logging.shutdown()\n"
                       "shutil.rmtree(TMP)\n"
                       "assert not TMP.exists()\n")
        _cleanup_bad = ("import shutil, tempfile\n"
                        "TMP = tempfile.mkdtemp(prefix='t-')\n"
                        "shutil.rmtree(TMP, ignore_errors=True)\n")
        # 包装函数（l-s2t 真实形态）：scratch_dir 内部调 mkdtemp
        _cleanup_wrapper = ("import shutil, tempfile\n"
                            "def scratch_dir(prefix):\n"
                            "    return tempfile.mkdtemp(prefix=prefix)\n"
                            "TMP = scratch_dir('t-')\n"
                            "shutil.rmtree(TMP, ignore_errors=True)\n")
        # 非 mkdtemp 根：目录是 mkdir 出来的，删它吞错不算泄漏
        _cleanup_subdir = ("import shutil, tempfile\n"
                           "TMP = tempfile.mkdtemp(prefix='t-')\n"
                           "sub = TMP / 'sub'\n"
                           "shutil.rmtree(sub, ignore_errors=True)\n"
                           "shutil.rmtree(TMP)\n")
        # 2026-09-19 补：**散文不算**（豁免边界必须有腿守着，同 C-33）。同一条被禁写法写在
        # docstring / 注释里，只是"关于代码的文本"⇒ 必须 ok；反向格：同样的字符串是**真调用**
        # ⇒ 必须红（证明绿来自"豁免了散文"，不是"豁免了这句话"）。
        _cleanup_prose = ("import shutil, tempfile\n"
                          '"""\u672c\u5de5\u5177\u81ea\u5df1\u5148\u5f97\u5b88\uff1a\u4ee5\u524d\u7528 '
                          "rmtree(TMP, ignore_errors=True) \u6536\u5c3e\u3002\"\"\"\n"
                          "TMP = tempfile.mkdtemp(prefix='t-')\n"
                          "# \u65e7\u5199\u6cd5\uff1ashutil.rmtree(TMP, ignore_errors=True)\n"
                          "shutil.rmtree(TMP)\n")
        _cleanup_prose_reverse = _cleanup_prose.replace("shutil.rmtree(TMP)\n",
                                                        "shutil.rmtree(TMP, ignore_errors=True)\n")
        c30_cases = (
            ("verified_cleanup_ok", _cleanup_ok, True),
            ("ignore_errors_on_mkdtemp_root_flagged", _cleanup_bad, False),
            ("ignore_errors_through_wrapper_flagged", _cleanup_wrapper, False),
            ("ignore_errors_on_scratch_subdir_ok", _cleanup_subdir, True),
            ("prose_mention_in_docstring_ok", _cleanup_prose, True),
            ("prose_mention_reverse_cell_flagged", _cleanup_prose_reverse, False),
        )
        for name, body, want in c30_cases:
            d = base / ("c30_" + name) / "src"
            d.mkdir(parents=True)
            (d / "test_x.py").write_text(body, encoding="utf-8")
            ok, detail = c30(Ctx(name, base / ("c30_" + name)))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-30/cleanup %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:100]))

        # C-30/腿 B：形态派生签名（不看名字）。样本**故意用回归集里的真实名字**
        # （`icon-probe-*` 在四个工具源码里搜不到）——它必须被找到，才证明"不看名字"成立。
        # 每个样本都对应一次**真实的**误判历史，注释里写清"旧签名为什么会漏/会误"。
        fake_tmp = base / "c30_shape_tmp"

        def _mk_shape(rel, files=()):
            d = fake_tmp / rel
            d.mkdir(parents=True, exist_ok=True)
            for f in files:
                p = d / f
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(b"")          # 0 字节：按宽松口径**仍算残留**
            return d

        _mk_shape("icon-probe-077hxtaw", ["log/config.json", "log/app.log"])   # 回归集真名 → 命中
        _mk_shape("smoke-proof-nl6gj9kf", ["log/config.json", "log/app.log"])  # 同上（0 字节）
        # 两个子目录（多一个 `ui-icons/`）——旧签名要求"恰好一个子目录"时**漏掉**。
        _mk_shape("two-subs", ["log/config.json", "log/app.log", "ui-icons/a.png"])
        # `config.json` 摆在顶层——旧签名（config 必须在**子目录**里）时**漏掉**。
        _mk_shape("config-at-top", ["config.json", "log/app.log"])
        # 复核员报的真实形态：**3 层**、**只有 `log/`、没有 config.json`**。
        # 旧签名（config 在 ≤1 层 且 顶层下存在 `*.log`）**两种写法都抓不到** ⇒ 这是本次放宽的判别样本。
        _mk_shape("nested-no-config", ["dsh-helper/log/dsh-helper.log"])
        # 反向样本：有 config.json 但**没有 log 目录** → 不是数据根，必须不命中。
        _mk_shape("no-log-dir", ["config.json", "x.txt"])
        # 白名单判别样本：名字与内容都命中形态，但**已声明（按全路径）** ⇒ 不得进命中集。
        _decl_dir = _mk_shape("reme-helper-builddata", ["log/x.log"])
        (fake_tmp / "just-a-file.txt").write_bytes(b"x")   # 顶层文件不是目录 → 不命中
        # key 已换全路径（§4.1.55）⇒ 自检必须声明**这个合成路径**，而不是靠裸名。
        _saved_decl = dict(TMP_DECLARED_PATHS)
        try:
            TMP_DECLARED_PATHS[_leak_key(_decl_dir)] = {"why": "自检样本", "reverify": "自检样本"}
            got_shape = {n for n, _why in _shape_hits(fake_tmp)}
        finally:
            TMP_DECLARED_PATHS.clear()
            TMP_DECLARED_PATHS.update(_saved_decl)
        want_shape = {"icon-probe-077hxtaw", "smoke-proof-nl6gj9kf",
                      "two-subs", "config-at-top", "nested-no-config"}
        good = got_shape == want_shape
        failed += 0 if good else 1
        print("[selftest] %s  C-30/shape %s: got=%s want=%s"
              % ("PASS" if good else "FAIL", "name_agnostic_shape", sorted(got_shape),
                 sorted(want_shape)))

        # R-10 加宽自证（§4.1.55 / 任务 #64）：**两处同名目录不得被去重吃掉**。
        # 判别力格 = 两个根各含同名 `dup` ⇒ 并集必须 2 条（裸名 key 会并成 1 条）；
        # 反向格   = 白名单**按全路径**只豁免其中一条 ⇒ 另一条仍在命中集。
        _dedup_base = base / "r10_dedup"
        _r1, _r2 = _dedup_base / "r1", _dedup_base / "r2"
        for _r, _f in ((_r1, "a.log"), (_r2, "b.log")):
            (_r / "dup" / "log").mkdir(parents=True)
            (_r / "dup" / "log" / _f).write_bytes(b"")
        _specs = [("r1", _r1, "children"), ("r2", _r2, "children")]
        _ha, _hb, _st = _scan_leak_roots(_specs, [])
        _keys = sorted({k for k, *_ in _hb})
        _dedup_good = (len(_keys) == 2 and {Path(k).name for k in _keys} == {"dup"})
        _saved2 = dict(TMP_DECLARED_PATHS)
        try:
            TMP_DECLARED_PATHS[_leak_key(_r1 / "dup")] = {"why": "自检", "reverify": "自检"}
            _k2 = sorted({k for k, *_ in _hb} - set(TMP_DECLARED_PATHS))
        finally:
            TMP_DECLARED_PATHS.clear()
            TMP_DECLARED_PATHS.update(_saved2)
        _decl_good = (len(_k2) == 1 and _k2[0] == _leak_key(_r2 / "dup"))
        good = _dedup_good and _decl_good
        failed += 0 if good else 1
        print("[selftest] %s  R-10/dedup %s: 并集=%d（裸名会=1） 全路径豁免后=%d want=1 | keys=%s"
              % ("PASS" if good else "FAIL", "same_name_two_roots_not_deduped",
                 len(_keys), len(_k2), [Path(k).name for k in _keys]))

        # C-32：读证据 → 删证据 → 报告。样本必须用**真实现场的形状**——首版就是被
        # `marker.read_text(...).strip()` 的链式包装 + `except: return` 挡住而**零命中**，
        # 是真实树首跑（模板 update_helper 竟然 [ok]）把这个漏报打出来的。
        c32_cases = (
            ('template_shape_flagged',
             chr(10).join(["def f(marker, log):", "    try:", "        detail = marker.read_text(encoding='utf-8').strip()", "        marker.unlink()", "    except OSError as exc:", "        log('read error:', exc)", "        return ''", "    log('previous update failed:', detail)", "    return detail"]) + chr(10),
             False),
            ('reme_old_shape_flagged',
             chr(10).join(["def f(marker, log):", "    try:", "        detail = marker.read_text().strip()", "    except OSError:", "        detail = ''", "    marker.unlink()", "    log('previous update failed:', detail)"]) + chr(10),
             False),
            ('log_before_delete_ok',
             chr(10).join(["def f(marker, log):", "    detail = marker.read_text()", "    log('previous update failed:', detail)", "    marker.unlink()"]) + chr(10),
             True),
            ('delete_without_read_ok',
             chr(10).join(["def f(marker, log):", "    marker.unlink()", "    log('watch loop stopped')"]) + chr(10),
             True),
            ('read_then_delete_no_log_ok',
             chr(10).join(["def f(marker, log):", "    detail = marker.read_text()", "    marker.unlink()", "    return detail"]) + chr(10),
             True),
            ('different_receiver_ok',
             chr(10).join(["def f(a, b, log):", "    detail = a.read_text()", "    b.unlink()", "    log(detail)"]) + chr(10),
             True),
            ('idempotent_delete_still_flagged',
             chr(10).join(["def f(marker, log):", "    detail = marker.read_text()", "    marker.unlink(missing_ok=True)", "    log(detail)"]) + chr(10),
             False),
        )
        for name, body, want in c32_cases:
            d = base / ("c32_" + name) / "src"
            d.mkdir(parents=True)
            (d / "main.py").write_text(body, encoding="utf-8")
            ok, detail = check_evidence_order(base / ("c32_" + name))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-32 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:100]))

        # C-33：禁拿 ping 当节拍。**注释/rem 行不算**（要抓的是会被执行的节拍），
        # 而渲染 bat 的 .py 模板里那句真节拍是**字符串**，必须抓住。
        c33_cases = (
            ("ping_tick_in_py_flagged",
             {"src/main.py": "BAT = '''ping -n 2 127.0.0.1 >nul'''\n"}, False),
            ("ping_tick_in_bat_flagged",
             {"scripts/apply.bat": "@echo off\r\nping -n 2 127.0.0.1 >nul\r\n"}, False),
            ("start_sleep_ok",
             {"src/main.py": "BAT = '''powershell -NoProfile -Command "
                             "\"Start-Sleep -Milliseconds 1000\" >nul'''\n"}, True),
            ("ping_in_py_comment_ok",
             {"src/main.py": "# 旧写法是 ping -n 2 127.0.0.1，实测 9 秒\nX = 1\n"}, True),
            ("ping_in_bat_rem_ok",
             {"scripts/apply.bat": "@echo off\r\nrem ping -n 2 127.0.0.1 was wrong\r\n"}, True),
            # 2026-09-19 补：**这条腿此前缺失，正是假红一路绿灯的原因**（豁免边界必须有腿守着）。
            # docstring = "关于代码的文本"，与下面那条 bat 模板**同为 STRING token、语义不同**。
            ("ping_in_py_docstring_ok",
             {"src/main.py": '"""说明：禁拿 `ping -n 2 127.0.0.1` 当节拍，实测 9 秒。"""\nX = 1\n'},
             True),
            # 反向对照（唯一变量法）：同样一句话**不在 docstring 里**而是一个真正的字符串常量
            # ⇒ 必须**照样红**，证明上面那条绿是"豁免了 docstring"，不是"豁免了这句话"。
            ("ping_in_py_string_still_flagged",
             {"src/main.py": 'HELP = "禁拿 `ping -n 2 127.0.0.1` 当节拍"\n'}, False),
        )
        for name, files, want in c33_cases:
            d = base / ("c33_" + name)
            for rel, body in files.items():
                fp = d / rel
                fp.parent.mkdir(parents=True, exist_ok=True)
                fp.write_text(body, encoding="utf-8", newline="")
            ok, detail = check_ping_tick(d)
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-33 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:100]))

        # C-33 自证腿（2026-09-19 补）：**扫描面必须排除仪器自身，且必须把排除项说出来**。
        # 这条腿扫的是**真目录**（本文件所在目录），不是合成样本——因为要证的正是"仪器对
        # 自己不做证人"这条性质。判别力：去掉 check_ping_tick 里的排除分支，本腿立刻红。
        # 同时钉住"排除 ≠ 静默"：detail 里必须出现被排除的文件名，否则"排除了"与"没扫"同形。
        _own_root = Path(__file__).resolve().parent
        ok, detail = check_ping_tick(_own_root)
        good = ok and ("conformance_check.py" in detail)
        failed += 0 if good else 1
        print("[selftest] %s  C-33 own_instrument_excluded_and_announced: ok=%s want=True "
              "(且 detail 必须点名被排除的文件) | %s"
              % ("PASS" if good else "FAIL", ok, detail[:160]))

        # C-38（2026-09-19 改形态后补）：**锚在 `startup` 行之后**，且**一次性行不计入**。
        # 五条腿 = 1 正 + 4 反，每条都对着新形态的一条限定（设计纪律 ⑨：豁免的每一条边界
        # 都必须有一条腿，且必须带反向格）。
        _sid_wrap = ("def main():\n"
                     "    log('startup vVERSION')\n"
                     "    log('data root:', USER_DATA_DIR, 'config:', CONFIG_PATH)\n")
        _sid_ok = _sid_wrap
        _sid_no_id = "def main():\n    log('startup vVERSION')\n    log('ready')\n"
        # 反例①：只有**一次性** migration 行 ⇒ 必须红（dsh/ocx 今天的"绿"就来自这里）
        _sid_oneshot = ("def seed_config():\n"
                        "    log('config migrated:', LEGACY_CONFIG_PATH, '->', CONFIG_PATH)\n"
                        "def main():\n    log('startup vVERSION')\n")
        # 反例②：数据根写在**文件开头 / startup 之前** ⇒ 必须红（"前 N 行是最老的"）
        _sid_before = ("log('data root:', USER_DATA_DIR)\n"
                       "def main():\n    log('startup vVERSION')\n    log('ready')\n")
        # 反例③：写在窗口之外（21 行之后）⇒ 必须红
        _sid_far = ("def main():\n    log('startup vVERSION')\n"
                    + "    log('tick')\n" * 21
                    + "    log('data root:', USER_DATA_DIR)\n")
        # 反例④：**只在 docstring 里提到** USER_DATA_DIR ⇒ 必须红（散文不算，§4.1.37）
        _sid_prose = ('def main():\n'
                      '    """\u542f\u52a8\u65f6\u4f1a\u5427 USER_DATA_DIR \u6253\u8fdb\u65e5\u5fd7\u3002"""\n'
                      "    log('startup vVERSION')\n    log('ready')\n")
        c38_cases = (
            ("startup_then_data_root_ok", _sid_ok, True),
            ("startup_without_data_root_flagged", _sid_no_id, False),
            ("oneshot_migration_line_flagged", _sid_oneshot, False),
            ("data_root_before_startup_flagged", _sid_before, False),
            ("data_root_outside_window_flagged", _sid_far, False),
            ("prose_mention_only_flagged", _sid_prose, False),
        )
        for name, body, want in c38_cases:
            ok, why, _hits, _anch = _self_id_window(body)
            got = (ok is True) if want else (ok is False)
            good = got and ok is not None
            failed += 0 if good else 1
            print("[selftest] %s  C-38 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want,
                     why or ("命中 %d 处" % len(_hits))))

        # C-39（2026-09-19，lead 立）：**派生值必须取自本次调用的实参**。
        # 四格两红两绿——只报"会被重绑"与"可变字面量"，**良性常量必须放行**
        # （否则就是"看到默认参数就报"的噪音判据，正是 C-33 那族错误的翻版）。
        c39_cases = (
            ("rebound_module_name_flagged",
             "MODEL_DIR = 'old'\n"
             "def load():\n"
             "    global MODEL_DIR\n"
             "    MODEL_DIR = 'new'\n"
             "def use(d=MODEL_DIR):\n"
             "    return d\n", False),
            ("mutable_default_flagged",
             "def collect(items=[]):\n    return items\n", False),
            ("immutable_constant_benign_ok",
             "SAMPLE_RATE = 16000\n"
             "def open_mic(sample_rate=SAMPLE_RATE):\n"
             "    return sample_rate\n", True),
            ("none_sentinel_ok",
             "MODEL_DIR = 'm'\n"
             "def use(d=None):\n"
             "    return d if d is not None else MODEL_DIR\n", True),
        )
        for name, body, want in c39_cases:
            d = base / ("c39_" + name) / "src"
            d.mkdir(parents=True)
            (d / "main.py").write_text(body, encoding="utf-8")
            ok, detail = check_default_snapshot(base / ("c39_" + name))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-39 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:110]))

        # C-40（2026-09-19，ls2t-dev 提议 + lead 两处修正）：**纯函数**判"版本目录 ↔ 自启目标"。
        # 六格 = 1 个**真实反例**（dsh 当时的状态）+ 5 格对照；**机器前缀已换成占位**（`H:\x\`，与同组其它样本一致），**判别结构逐字保留**。
        # 用纯函数是为了**能拿确定输入自证**：注册表与磁盘是活状态，不能当固定样本。
        _la = r"C:\Users\x\AppData\Local"
        _dsh = r'"H:\x\dsh-helper\release\dsh-helper-1.8.2\dsh-helper.exe"'
        c40_cases = (
            # 真实反例：**自启目标 1.8.2 ≠ VERSION 1.8.1**（当时实测状态；**仅替换机器前缀**）
            ("live_dsh_case_flagged",
             ("1.8.1", "dsh-helper", ["dsh-helper-1.8.1", "dsh-helper-1.8.2"], _dsh, {}, _la),
             False, "FAIL"),
            # 反向格①：目标目录 == release/<VERSION> ⇒ 绿（否则成了"凡有自启就报"）
            ("target_matches_version_ok",
             ("1.2.1", "opencodex-helper", ["opencodex-helper-1.2.1"],
              r'"H:\x\opencodex-helper\release\opencodex-helper-1.2.1\opencodex-helper.exe"',
              {}, _la), True, None),
            # 反向格②：稳定安装位 ⇒ 绿（更新链的目标形态）
            ("stable_install_ok",
             ("1.2.1", "opencodex-helper", ["opencodex-helper-1.2.1"],
              r'"%s\opencodex-helper\app\opencodex-helper.exe"' % _la, {}, _la), True, None),
            # 反例③：目标**不存在** ⇒ 红（死链）
            ("missing_target_flagged",
             ("1.2.1", "opencodex-helper", [], r'"H:\nope\nope-1.2.1\nope.exe"', {}, _la),
             False, "FAIL"),
            # 反例④：**改名保留镜像**未登记 ⇒ WARN（不是 FAIL：镜像本身不是缺陷）
            # 1.9.29 改：样本从普通版本目录名换成 `_stale_*` 形态 —— 新口径只对
            # **改名保留的镜像**要求登记（普通 `<tool>-<semver>` 是历次构建的自然产物）。
            ("undeclared_orphan_warn",
             ("1.8.1", "dsh-helper",
              ["dsh-helper-1.8.1", "_stale_dsh-helper-1.8.0_20260101-000000"],
              r'"H:\x\dsh-helper\release\dsh-helper-1.8.1\dsh-helper.exe"', {}, _la),
             False, "WARN"),
            # 反向格③：同一镜像**已登记**（两栏齐全）⇒ 绿
            ("declared_orphan_ok",
             ("1.8.1", "dsh-helper",
              ["dsh-helper-1.8.1", "_stale_dsh-helper-1.8.0_20260101-000000"],
              r'"H:\x\dsh-helper\release\dsh-helper-1.8.1\dsh-helper.exe"',
              {"_stale_dsh-helper-1.8.0_20260101-000000":
                   {"why": "改名保留镜像；当前态：存在但未被引用",
                    "reverify": "Run 键再次指向它，或 release/ 集合变化时"}},
              _la), True, None),
            # **新口径的守卫格**（1.9.29）：**上一版目录**（普通 `<tool>-<semver>`，未登记）
            # ⇒ 必须**放行**。这一格是"只收改名保留镜像"这条边界的探针 ——
            # 哪天它回退成 WARN，就说明"上一版"又被当成待登记孤儿了（登记量会随发版线性膨胀）。
            ("prev_version_dir_not_an_orphan",
             ("1.8.1", "dsh-helper", ["dsh-helper-1.8.1", "dsh-helper-1.8.0"],
              r'"H:\x\dsh-helper\release\dsh-helper-1.8.1\dsh-helper.exe"', {}, _la),
             True, None),
        )
        for name, args, want, want_sev in c40_cases:
            # 目标存在性用替身：只按"路径里是否含 nope"决定 False——**唯一变量**。
            ok, _detail, sev = judge_version_targets(*args, path_exists=lambda p: "nope" not in p)
            good = (ok == want) and (want_sev is None or sev == want_sev)
            failed += 0 if good else 1
            print("[selftest] %s  C-40 %s: ok=%s want=%s sev=%s want_sev=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, sev, want_sev, _detail[:90]))

        # C-40 选键口径（§4.1.53/§4.1.54 假绿修法；§4.1.37 判别力自证）：
        # 必须**两条正样本**——① 模板 autostart 形态（键 = APP_NAME，l-s2t 真值）；
        # ② reme 内联形态（键 = APP_ID，且 APP_NAME 是中文展示名、不在 Run 表里）。
        # 旧谓词（按 APP_ID 单查）必须在①上**漏**（红），新"路径优先"两条都**抓**。
        _rv_ls = {"LocalSpeak2Text":
                  '"C:\\x\\local-speak2text\\release\\local-speak2text-1.4.0\\local-speak2text.exe"'}
        _old_miss = _rv_ls.get("local-speak2text")            # 旧实现：按 APP_ID 单查
        _k1, _v1, _how1, _ = select_run_entry(_rv_ls, root=r"C:\x\local-speak2text",
                                              app_id="local-speak2text",
                                              app_name="LocalSpeak2Text")
        good = (_old_miss is None) and (_k1 == "LocalSpeak2Text") and (_how1 == "path")
        failed += 0 if good else 1
        print("[selftest] %s  C-40 run-key APP_NAME-form: old_miss=%s new=(%s,%s)"
              " want (None,('LocalSpeak2Text','path'))"
              % ("PASS" if good else "FAIL", _old_miss, _k1, _how1))
        # ② reme 内联：键 = APP_ID，APP_NAME 是中文展示名（不在 Run 表里）⇒ 仍必须命中
        _rv_reme = {"reme-helper":
                    '"C:\\x\\reme-helper\\release\\reme-helper-1.2.5\\reme-helper.exe"'}
        _k2, _v2, _how2, _ = select_run_entry(_rv_reme, root=r"C:\x\reme-helper",
                                              app_id="reme-helper", app_name="ReMe 助手")
        good = (_k2 == "reme-helper" and _how2 == "path")
        failed += 0 if good else 1
        print("[selftest] %s  C-40 run-key APP_ID-form: hit=%s how=%s want (reme-helper,path)"
              % ("PASS" if good else "FAIL", _k2, _how2))
        # 反向格：外来项（如 `OpenCodexTray-…vbs`，值指向别处）**不得**被算成本工具的自启项
        _rv_foreign = {"OpenCodexTray-abc":
                       '"C:\\Windows\\System32\\wscript.exe" //B "C:\\Users\\x\\.opencodex\\opencodex-tray.vbs"'}
        _k3, _v3, _how3, _ = select_run_entry(_rv_foreign, root=r"C:\x\\opencodex-helper",
                                              app_id="opencodex-helper", app_name="opencodex-helper")
        good = (_k3 is None and _how3 == "none")
        failed += 0 if good else 1
        print("[selftest] %s  C-40 foreign Run item not matched: hit=%s how=%s want (None,none)"
              % ("PASS" if good else "FAIL", _k3, _how3))
        # 控制格：两候选皆无 ⇒ None（"没命中"与"命中但值坏"必须可区分，§D8 第 6 条）
        _k4, _v4, _how4, _ = select_run_entry({}, root=r"C:\x\a", app_id="a", app_name="B")
        good = (_k4 is None and _how4 == "none")
        failed += 0 if good else 1
        print("[selftest] %s  C-40 run-key none-present: hit=%s want None"
              % ("PASS" if good else "FAIL", _k4))
        # 附带盲区可见化：大小写变体键（§4.1.51）路径腿也能抓到，并把"多个/非候选"记进 notes
        _rv_var = {"dsh-helper": '"C:\\x\\dsh-helper\\release\\dsh-helper-1.8.1\\dsh-helper.exe"',
                   "DSH-Helper": '"C:\\x\\dsh-helper\\release\\dsh-helper-1.8.2\\dsh-helper.exe"'}
        _k5, _v5, _how5, _n5 = select_run_entry(_rv_var, root=r"C:\x\dsh-helper",
                                               app_id="dsh-helper", app_name="dsh-helper")
        good = (_how5 == "path") and any(("多个" in n) or ("不是" in n) for n in _n5)
        failed += 0 if good else 1
        print("[selftest] %s  C-40 case/duplicate Run keys noted: hit=%s notes=%s"
              % ("PASS" if good else "FAIL", _k5, _n5))

        # C-41（2026-09-19，lead 立）：**降级分支不得沿用已存勾选**。
        # 四格两红两绿，另加一格"**合法的原生框那一支**"必须放行（否则就成了"凡读配置就报"）。
        c41_cases = (
            ("fallback_literal_false_ok",
             "def on_quit():\n"
             "    try:\n"
             "        choice = confirm()\n"
             "    except Exception:\n"
             "        return True, False\n", True),
            ("fallback_reuses_saved_checkbox_flagged",
             "def on_quit():\n"
             "    try:\n"
             "        choice = confirm()\n"
             "    except Exception:\n"
             "        return True, bool(CFG.get('quit_stop_tunnels', False))\n", False),
            ("none_branch_literal_false_ok",
             "def on_quit():\n"
             "    choice = decide()\n"
             "    if choice is None:\n"
             "        stop_tunnels = False\n"
             "        return True, stop_tunnels\n", True),
            ("none_branch_reuses_config_flagged",
             "def on_quit():\n"
             "    choice = decide()\n"
             "    if choice is None:\n"
             "        stop_tunnels = bool(load_config_dict().get('quit_stop_tunnels', False))\n"
             "        return True, stop_tunnels\n", False),
            # 反向格：**原生框那一支**（在 try 体内）按已存配置走是合法的
            # ——那时用户**确实被问到了**，只是没有勾选框（与 reme 代码里的注释同一条口径）。
            ("native_fallback_in_try_body_ok",
             "def on_quit():\n"
             "    try:\n"
             "        choice = confirm()\n"
             "    except Exception:\n"
             "        choice = {'go': True, 'stop': bool(CFG.get('quit_stop_tunnels', False))}\n"
             "    return choice\n", True),
        )
        for name, body, want in c41_cases:
            d = base / ("c41_" + name) / "src"
            d.mkdir(parents=True)
            (d / "main.py").write_text(body, encoding="utf-8")
            ok, detail = check_quit_fallback(base / ("c41_" + name))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-41 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:110]))

        # C-42（2026-09-19，lead 定·收窄版）：**重定向位置不得出现 `dev/null`**。
        # 五格：lead 点名的三个样本（红 / 绿 / 绿）+ 一个 .bat 形态 + 一个"名字像但不同"的反向格。
        c42_cases = (
            ("redirect_devnull_flagged",
             {"src/main.py": 'BAT = "x >/dev/null 2>nul\n"\n'}, False),
            ("comment_dev_path_ok",
             {"src/main.py": "# see H:/Tools/dev/notes\nX = 1\n"}, True),
            ("template_string_nul_ok",
             {"src/main.py": 'BAT = "powershell -NoProfile -Command \\"Start-Sleep -Milliseconds 1000\\" >nul 2>nul"\n'},
             True),
            ("bat_file_redirect_flagged",
             {"scripts/a.bat": "@echo off\r\nfoo.exe > /dev/null\r\n"}, False),
            # 反向格：**名字像但不是它** ⇒ 必须放行（证明判据收窄到了"重定向位置 + 完整词"）
            ("devnull_like_name_ok",
             {"src/main.py": 'X = "a > dev/nullish thing"\n'}, True),
        )
        for name, files, want in c42_cases:
            d = base / ("c42_" + name)
            for rel, body in files.items():
                fp = d / rel
                fp.parent.mkdir(parents=True, exist_ok=True)
                fp.write_text(body, encoding="utf-8", newline="")
            ok, detail = check_devnull_redirect(d)
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-42 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:110]))

        # C-43（2026-09-19，lead 定 / 边界由 ls2t-dev 钉准）：**`if` 条件里的 `:~`**。
        # 四格：真危险形态（红）+ **我们仓里那行现成的假阳性**（绿，逐字搬入）+ 动作一侧（绿）
        # + 普通 `%VAR%` 展开（绿）。
        c43_cases = (
            # 1) 历史中止形态：`:~-1` 在**条件**里，且后面跟着坏引号
            ("if_cond_substr_flagged",
             {"build.bat": '@echo off\r\nif defined X if "%X:~-1%"=="\\" set "X=bad"\r\n'}, False),
            # 2) **逐字搬入本仓真实行**（l-s2t build.bat:84）：嵌套 if、零个 `:~` ⇒ 必须绿
            ("nested_if_without_substr_ok",
             {"build.bat": '@echo off\r\n'
                          'if defined RUNNING_DIR if /i "%RUNNING_DIR%"=="%TARGET_DIR%" (\r\n'
                          '  echo refuse\r\n'
                          ')\r\n'}, True),
            # 3) `:~` 在**动作**一侧、被 `if defined` 守着（dsh/ocx build.bat:87 的真实形态）
            ("substr_in_action_ok",
             {"build.bat": '@echo off\r\n'
                          'if defined RUNNING_DIR set "RUNNING_DIR=%RUNNING_DIR:~0,-1%"\r\n'}, True),
            # 4) 与本判据无关的普通展开（反向格：证明不是"见 % 就报"）
            ("plain_expansion_ok",
             {"build.bat": '@echo off\r\nif /i "%A%"=="%B%" echo same\r\n'}, True),
        )
        for name, files, want in c43_cases:
            d = base / ("c43_" + name)
            for rel, body in files.items():
                fp = d / rel
                fp.parent.mkdir(parents=True, exist_ok=True)
                fp.write_text(body, encoding="utf-8", newline="")
            ok, detail = check_if_substr_expansion(d)
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-43 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:110]))

        # C-44（2026-09-19，lead 定）：**bat 里闭集命令必须绝对路径**。
        # 原五格：裸名（红）/ 绝对路径（绿）/ rem 里提到（绿）/ for /f ('cmd') 形态（红）
        # / 非闭集命令（绿）。
        # 1.9.23 增两格（§4.1.56 段首盲区）：
        #   判别力格 = `if exist X findstr …` 必须红（旧实现漏）；
        #   反向格   = `if exist X echo find` 必须绿（证明红来自"命令位置"而非"行里出现 find"）。
        c44_cases = (
            ("bare_name_flagged",
             {"build.bat": "@echo off\r\nfindstr /b /c:\"VERSION = \" src\\main.py\r\n"}, False),
            ("absolute_path_ok",
             {"build.bat": "@echo off\r\n%SystemRoot%\\System32\\findstr.exe /b /c:\"V\" x\r\n"},
             True),
            ("rem_mention_ok",
             {"build.bat": "@echo off\r\nrem never use bare find or ping here\r\n"}, True),
            ("for_f_inline_bare_flagged",
             {"build.bat": "@echo off\r\nfor /f \"tokens=2\" %%a in ('findstr /b x y') do set V=%%a\r\n"},
             False),
            ("non_closed_set_ok",
             {"build.bat": "@echo off\r\npython -c \"print(1)\"\r\n"}, True),
            ("if_exist_bare_cmd_flagged",
             {"build.bat": "@echo off\r\nif exist \"%EXE%\" findstr /i \"x\" y\r\n"}, False),
            ("if_exist_echo_find_ok",
             {"build.bat": "@echo off\r\nif exist foo echo find\r\n"}, True),
        )
        for name, files, want in c44_cases:
            d = base / ("c44_" + name)
            for rel, body in files.items():
                fp = d / rel
                fp.parent.mkdir(parents=True, exist_ok=True)
                fp.write_text(body, encoding="utf-8", newline="")
            ok, detail = check_bat_absolute_cmds(d)
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-44 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:110]))

        # C-45（2026-09-19，lead 升为本波必办）：**工具侧副本的行尾**。
        # 三格：LF 副本（红）/ CRLF 副本（绿）/ 无 modules 目录（不适用=绿）。
        c45_cases = (
            ("lf_copy_flagged", "template/mod1/a.py", b"x = 1\ny = 2\n", False),
            ("crlf_copy_ok", "template/mod1/a.py", b"x = 1\r\ny = 2\r\n", True),
            ("no_modules_dir_ok", None, None, True),
        )
        for name, rel, blob, want in c45_cases:
            d = base / ("c45_" + name)
            if rel:
                fp = d / "src" / rel
                fp.parent.mkdir(parents=True, exist_ok=True)
                fp.write_bytes(blob)
            else:
                (d / "src").mkdir(parents=True, exist_ok=True)
            ok, detail = check_tool_copy_eol(d)
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-45 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:100]))

        # C-47（2026-09-19，verifier 复核发现）：**被禁头形态 `TEMPLATE-MODULE`**。
        # 红格 = 判别力自证：旧 C-19 的 `and` 链把 MODULE 列为合法 ⇒ 回归抓不到；
        # 两条反向格 = 别误伤合法形态（`TEMPLATE-FROM` / `TEMPLATE-LOCAL-OVERRIDE`）。
        c47_cases = (
            ("pos_banned_module_head", "TEMPLATE-MODULE", False),
            ("neg_from_head_ok", "TEMPLATE-FROM", True),
            ("neg_local_override_ok", "TEMPLATE-LOCAL-OVERRIDE", True),
        )
        for name, marker, want in c47_cases:
            d = base / ("c47_" + name)
            (d / "src" / "template" / "m").mkdir(parents=True, exist_ok=True)
            (d / "src" / "template" / "m" / "m.py").write_text(
                "# %s: x\nX = 1\n" % marker, encoding="utf-8")
            ok, detail = c47(Ctx(name, d))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-47 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:100]))

        # C-06（2026-09-19，verifier 发现空真）：**只有 rem/echo 提到 ⇒ 必须红**。
        # 红格 = 判别力自证（旧实现在这一格**假绿**，reme 真身就是这形态）；
        # 反向格 = 有真拷贝行 ⇒ 必须放行（别把 dsh/ocx/l-s2t 误伤）。
        c06_cases = (
            ("pos_prose_only",
             "rem Both READMEs ship: README.zh-CN.md\necho [ERROR] README.zh-CN.md was not copied\n",
             False),
            ("neg_real_copy",
             "copy README.md \"%RELEASE_DIR%\\\"\ncopy README.zh-CN.md \"%RELEASE_DIR%\\\"\n",
             True),
        )
        for name, body, want in c06_cases:
            d = base / ("c06_" + name)
            d.mkdir(parents=True, exist_ok=True)
            (d / "build.bat").write_text(body, encoding="utf-8")
            ok, detail = c06(Ctx(name, d))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-06 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:100]))

        # C-48（R1 §3 T3 的守卫）：自建 Tk 框没有本地化通道 ⇒ 必须红。
        # 红格 = 判别力自证（= reme 修前的真身：Toplevel + 裸 APP_NAME、无 translate_tree）；
        # 反向格 = 同一个框补上两条通道 ⇒ 必须放行。
        _cn = "\u786e\u5b9a\u9000\u51fa\uff1f"
        c48_cases = (
            # 红格（= reme 修前的真身）：中文字面量写死在控件构造处、又无 translate_tree。
            ("pos_cn_literal_without_translate",
             "import tkinter as tk\n\n\ndef dlg():\n    w = tk.Toplevel(None)\n"
             "    tk.Label(w, text=\"%s\").pack()\n    return w\n" % _cn, False),
            # 反向格 1：同一段文本 + translate_tree ⇒ 放行（reme 修后就是这形态）。
            ("neg_translate_tree_ok",
             "import tkinter as tk\n\n\ndef dlg():\n    w = tk.Toplevel(None)\n"
             "    tk.Label(w, text=\"%s\").pack()\n    translate_tree(w)\n"
             "    return w\n" % _cn, True),
            # 反向格 2：**参数注入** ⇒ 放行（模板 tray_kit 走这条，别误伤）。
            ("neg_injected_text_ok",
             "import tkinter as tk\n\n\ndef dlg(body_text):\n    w = tk.Toplevel(None)\n"
             "    tk.Label(w, text=body_text).pack()\n    return w\n", True),
        )
        for name, body, want in c48_cases:
            d = base / ("c48_" + name)
            (d / "src").mkdir(parents=True, exist_ok=True)
            (d / "src" / "main.py").write_text(body, encoding="utf-8")
            ok, detail = c48(Ctx(name, d))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-48 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:100]))

        # C-49（#45 的机械形态）：破坏性守卫的探测失败被折叠成 False ⇒ 必须红。
        # 红格 = 判别力自证（= ocx 修前的真身：except 吞掉 + 末尾 return False + kill 守卫）；
        # 反向格 1 = 失败侧 return True（放行）⇒ 不报；反向格 2 = 动作只记日志 ⇒ 不报。
        c49_cases = (
            ("pos_folded_to_false",
             "import os\n\n\ndef probe(p):\n    try:\n        os.path.exists(p)\n"
             "    except Exception:\n        pass\n    return False\n\n\n"
             "def go(p):\n    if not probe(p):\n        os.remove(p)\n", False),
            ("neg_fail_open_true",
             "import os\n\n\ndef probe(p):\n    try:\n        os.path.exists(p)\n"
             "    except Exception:\n        return True\n    return False\n\n\n"
             "def go(p):\n    if not probe(p):\n        os.remove(p)\n", True),
            ("neg_benign_action",
             "import os\n\n\ndef probe(p):\n    try:\n        os.path.exists(p)\n"
             "    except Exception:\n        pass\n    return False\n\n\n"
             "def go(p):\n    if not probe(p):\n        print(\"offline\")\n", True),
            # 反向格 3：**函数本身是动作执行者**（= reme `_rmtree_verified` 的真身）⇒ 不报。
            # 它的返回值是"删除成功了吗"，False 是正确语义，不是"探测失败被折叠"。
            ("neg_actor_not_a_probe",
             "import os\nimport shutil\n\n\ndef do_rm(p):\n    try:\n        shutil.rmtree(p)\n"
             "    except Exception:\n        pass\n    return False\n\n\n"
             "def go(p):\n    if not do_rm(p):\n        os.remove(p)\n", True),
        )
        for name, body, want in c49_cases:
            d = base / ("c49_" + name)
            (d / "src").mkdir(parents=True, exist_ok=True)
            (d / "src" / "main.py").write_text(body, encoding="utf-8")
            ok, detail = c49(Ctx(name, d))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-49 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:100]))

        # C-27 豁免腿（§4.1.37）：**已申报 NOT-WIRED 的模块不查**。
        # 红格 = 有声明但零引用 ⇒ 必报；反向格 = 同一份 + `NOT-WIRED.md` ⇒ 不报。
        # （模板 README 的 MUST-WIRE 来自真身，故这里只造工具侧 + synth 模板名对不上，
        #  改用「工具侧 README 也读」那条路径：把声明写在工具侧 README 上。）
        for name, not_wired, want in (("pos_declared_but_not_wired", False, False),
                                      ("neg_not_wired_exempts", True, True)):
            d = base / ("c27_" + name)
            (d / "src" / "template" / "m").mkdir(parents=True, exist_ok=True)
            (d / "src" / "main.py").write_text("x = 1\n", encoding="utf-8")
            (d / "src" / "template" / "m" / "README.md").write_text(
                "<!-- MUST-WIRE: some_symbol_xyz -->\n", encoding="utf-8")
            if not_wired:
                (d / "src" / "template" / "m" / "NOT-WIRED.md").write_text(
                    "有意不接入\n", encoding="utf-8")
            ok, detail = c27(Ctx(name, d))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-27 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:100]))

        # C-50（G4.2 条款 5）：退出路径的「未勾选」分支不得清理。
        # 红格 = 判别力自证（= ocx 1.2.1 修前的真身）；两条反向格：
        # 「勾选分支里 kill」是**合法**的（条款 5 允许）、「else 只记日志」必须放行。
        c50_cases = (
            ("pos_else_terminates",
             "def on_quit(icon, item):\n    if CFG.get('quit_stop_tunnels'):\n"
             "        kill_tunnels()\n    else:\n        proc.terminate()\n", False),
            ("neg_checked_branch_kills_ok",
             "def on_quit(icon, item):\n    if CFG.get('quit_stop_tunnels'):\n"
             "        proc.terminate()\n    else:\n        log('keep running')\n", True),
            ("neg_else_logs_only",
             "def quit_app(icon, item):\n    stop = CFG.get('quit_stop_reme')\n"
             "    if stop:\n        stop_service()\n    else:\n        notify('stays up')\n", True),
        )
        for name, body, want in c50_cases:
            d = base / ("c50_" + name)
            (d / "src").mkdir(parents=True, exist_ok=True)
            (d / "src" / "main.py").write_text(
                "CFG = {}\n\n\n" + body, encoding="utf-8")
            ok, detail = c50(Ctx(name, d))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-50 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:90]))

        # C-51（§4.1.43/C-41 同族）：无 UI 退出入口不得沿用持久化勾选。
        # 红格 = 判别力自证（= reme 修前的真身：不传 kwargs）；反向格 = 显式全 False。
        # 第 3 格是**豁免腿**（§4.1.37）：同一段"有罪代码"放进 `src/modules/**`
        # （机制件路径）⇒ **必须不报**。模板 `tray_kit.quit_watch_loop` 只回调、
        # 不读配置，不该被本判据管 —— 没有这一格，判据会把机制件报成假红（首跑就是这样）。
        _c51_body = ("def quit_watch_loop():\n    if ICON is not None:\n"
                     "        shutdown_tray(ICON)\n    return\n")
        c51_cases = (
            ("pos_no_kwargs_uses_cfg", "src", _c51_body, False),
            ("neg_explicit_false_ok", "src",
             "def quit_watch_loop():\n    if ICON is not None:\n"
             "        shutdown_tray(ICON, stop_reme=False, stop_tunnels=False)\n", True),
            ("neg_template_module_exempt", "src/template/tray_kit", _c51_body, True),
        )
        for name, sub, body, want in c51_cases:
            d = base / ("c51_" + name)
            (d / sub).mkdir(parents=True, exist_ok=True)
            (d / sub / "mod.py").write_text("ICON = None\n\n\n" + body, encoding="utf-8")
            ok, detail = c51(Ctx(name, d))
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-51 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:90]))

        # C-52（补 C-20 的豁免盲区）：T1 触发却没启用 i18n ⇒ 必须红。
        # 红格 = 判别力自证（有远端 + 无 i18n）；未触发（无远端）也必须报
        # （开关语义已移除的自证格）。
        # **W3 后段收窄（2026-09-27）**：pairs.json 重形态 grandfather 终结 ⇒
        # 原 neg_pairs_form_ok 反向格删除，换 pos_pairs_no_dir_is_gap 守卫格——
        # 只有目录（没有 pairs.json 也算合法）的时代结束了；这一格若哪天回退，
        # 说明有人把重形态豁免又加回来了。
        c52_cases = (
            ("pos_remote_no_i18n_is_gap", (True, False), True),
            # ⚠ **开关语义已移除的自证格**（2026-09-20 用户裁定"默认所有工具都支持双语"）：
            # 传 has_remote=False 也**必须报** —— 它证明"是否开源"不再是豁免条件。
            # 这一格若哪天回退成 False，说明有人把开关又加回来了。
            ("pos_no_remote_still_gap", (False, False), True),
            # ⚠ **重形态豁免已移除的守卫格**（W3 后段收窄）：pairs.json 不再是合法形态，
            # 无目录必须报（reme 已迁轻形态 locales）。
            ("pos_pairs_no_dir_is_gap", (True, False), True),
            ("neg_has_dir_ok", (True, True), False),
            ("neg_no_remote_with_dir_ok", (False, True), False),
        )
        for name, args, want in c52_cases:
            got = i18n_gap(*args)
            good = got == want
            failed += 0 if good else 1
            print("[selftest] %s  C-52 %s: got=%s want=%s | args=%s"
                  % ("PASS" if good else "FAIL", name, got, want, args))

        # C-34（2026-09-19，lead 批准）：**§1 登记表版本列 vs 文件头**。
        # 两格：表格版本与文件头不符（红）/ 一致（绿）。
        c34_cases = (
            ("registry_version_mismatch_flagged", "1.2.3", False),
            ("registry_version_match_ok", "9.9.9", True),
        )
        for name, table_v, want in c34_cases:
            d = base / ("c34_" + name)
            (d / "template" / "m").mkdir(parents=True)
            (d / "template" / "m" / "m.py").write_text(
                "# TEMPLATE-VER: 9.9.9\nX = 1\n", encoding="utf-8")
            (d / "合规对照表.md").write_text(
                "| \u6a21\u5757 | \u63cf\u8ff0 | \u63a5\u53e3 | \u7248\u672c |\n"
                "|---|---|---|---|\n"
                "| `template/m/m.py` | x | y | %s |\n" % table_v, encoding="utf-8")
            ok, detail = check_registry_versions(d)
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-34 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:100]))

        # C-35（2026-09-19，ls2t-dev 规格 + lead 批准）：**实例隔离两条腿**。
        # 三格 = 并集语义的三条边：无 leg_b 且未自钉（红）/ 无 leg_b 但自钉了（绿）/
        # **有 leg_b 且未自钉（绿——这一格就是"关掉 harness 腿 ⇒ 11 红、打开 ⇒ 全绿"的判别力来源）**。
        c35_cases = (
            ("no_pin_at_all_flagged",
             "import main\nX = 1\n", "@echo off\r\n\"%PY%\" tests\\t.py\r\n", False),
            ("file_level_pin_ok",
             "import os\nos.environ['APP_DATA_DIR'] = 'x'\nimport main\nX = 1\n",
             "@echo off\r\n\"%PY%\" tests\\t.py\r\n", True),
            ("harness_pin_covers_ok",
             "import main\nX = 1\n",
             "@echo off\r\nset \"APP_DATA_DIR=%TEMP%\\d\"\r\n\"%PY%\" tests\\t.py\r\n", True),
        )
        for name, test_src, bat_src, want in c35_cases:
            d = base / ("c35_" + name)
            (d / "tests").mkdir(parents=True)
            (d / "tests" / "t.py").write_text(test_src, encoding="utf-8")
            (d / "build.bat").write_text(bat_src, encoding="utf-8", newline="")
            ok, detail = check_instance_isolation(d)
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-35 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:100]))

        # C-36：归一化算子的性质断言。样本 2 条——
        #   ① 真算子（sync_check.sha256_text）→ 必须 ok；
        #   ② **变异算子**（把 `splitlines()` 换成 `split("\n")`）→ 必须**不 ok**。
        # 第 ② 条就是"判别力"的自证：少了它，一个恒返回常数的实现也能让 ① 通过。
        import hashlib as _hl
        import importlib.util as _ilu
        _sc_path = Path(__file__).resolve().parent / "sync_check.py"
        _spec = _ilu.spec_from_file_location("_tpl_sc_c36_selftest", _sc_path)
        _sc = _ilu.module_from_spec(_spec)
        _spec.loader.exec_module(_sc)
        _c36_text = "# TEMPLATE-MODULE: demo | TEMPLATE-VER: 1.0.0\nalpha = 1\nbeta = 2\n"

        def _mutated_split(text):        # 只改算子：splitlines() -> split("\n")
            return _hl.sha256("\n".join(
                l for l in text.split("\n") if not _NAIVE_META.match(l)).encode("utf-8")).hexdigest()

        for name, fn, want in (("real_operator_eol_insensitive", _sc.sha256_text, True),
                               ("mutated_split_lacks_power", _mutated_split, False)):
            ok, detail = eol_insensitive_ok(fn, _c36_text)
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-36 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:110]))

        # C-31：派发件行尾。正 / 负样本各一，另加一条"范围"样本——
        # 模板专属目录（build_release/）里的 LF 不算，防止判据扩成"模板全仓"后误伤。
        c31_cases = (
            ("crlf_dispatched_ok",
             {"template/demo/a.py": b"x = 1\r\ny = 2\r\n",
              "template/demo/README.md": b"# demo\r\n"}, True),
            ("lf_only_dispatched_flagged",
             {"template/demo/a.py": b"x = 1\ny = 2\n"}, False),
            ("mixed_eol_flagged",
             {"template/demo/a.py": b"x = 1\r\ny = 2\n"}, False),
            ("template_only_dir_ignored",
             {"template/build_release/tool.py": b"x = 1\n"}, True),
        )
        for name, files, want in c31_cases:
            d = base / ("c31_" + name)
            for rel, blob in files.items():
                fp = d / rel
                fp.parent.mkdir(parents=True, exist_ok=True)
                fp.write_bytes(blob)   # 显式字节：行尾样本绝不能经字符串转义构造
            ok, detail = check_dispatched_eol(d)
            good = ok == want
            failed += 0 if good else 1
            print("[selftest] %s  C-31 %s: ok=%s want=%s | %s"
                  % ("PASS" if good else "FAIL", name, ok, want, detail[:100]))

        # C-37（C-2）：性质判据的**判别力**自证——一个"共享位写错"的原语必须**不通过**。
        # 真原语用 `FILE_SHARE_READ|WRITE`（不给 DELETE）；下面这条**故意**带上
        # `FILE_SHARE_DELETE`（= 允许别人删），于是 unlink 会成功 ⇒ 性质断言必须失败。
        # 这正是"能实测的就别推断"：共享位写错在源码上完全看不出来。
        def _permissive_hold(path):
            import ctypes
            k32 = ctypes.WinDLL("kernel32", use_last_error=True)
            k32.CreateFileW.restype = ctypes.c_void_p
            h = k32.CreateFileW(str(path), 0x80000000, 0x1 | 0x2 | 0x4, None, 3, 0, None)
            return None if not h or h == ctypes.c_void_p(-1).value else h

        _c37_real = c2_property(_permissive_hold)
        good = _c37_real[0] is False
        failed += 0 if good else 1
        print("[selftest] %s  C-37 判别力 %s: ok=%s（want False）| %s"
              % ("PASS" if good else "FAIL", "permissive_share_is_caught",
                 _c37_real[0], _c37_real[1][:110]))



        # C-46：新鲜度的**分母**必须含 out-of-src datas——纯函数四格。
        # 关键不是"能判新鲜"，而是"**补上的那一项能改变结论**"：
        # 同一 exe 在 src-only 视图下判新鲜、在含 out-of-src 的构建输入集下判过期。
        _c46_exe = 1000.0
        _c46_src = ("src/main.py", 900.0)
        _c46_data = ("locales/en.json", 1200.0)   # out-of-src 打包输入，比 exe 新
        c46_cases = (
            ("neg_all_older_is_fresh", [_c46_src], True),
            ("pos_out_of_src_data_newer_is_stale", [_c46_src, _c46_data], False),
            ("pos_equal_mtime_is_stale_strict_gt", [("src/main.py", 1000.0)], False),
        )
        for name, items, want in c46_cases:
            ok, newest, _mt, n = judge_freshness(_c46_exe, items)
            good = (ok == want)
            failed += 0 if good else 1
            print("[selftest] %s  C-46 %s: ok=%s want=%s | n=%d max=%s"
                  % ("PASS" if good else "FAIL", name, ok, want, n, newest))
        _c46_empty = judge_freshness(_c46_exe, [])
        good = _c46_empty[0] is None
        failed += 0 if good else 1
        print("[selftest] %s  C-46 empty_denominator_is_undecidable: ok=%s want=None"
              % ("PASS" if good else "FAIL", _c46_empty[0]))

        # C-46 豁免腿（§4.1.37：**豁免的每条边界都要有自证腿 + 反向格**）：
        # `src/modules/**/*.md` **不计入分母**（是给人读的派发件，不是构建输入）；
        # 但同目录的 `*.py` **必须仍计入**（反向格 —— 证明豁免只针对文档，
        # 不是把 `src/modules/` 整目录跳过）。
        _c46d = base / "c46_doc_exempt"
        (_c46d / "src" / "template" / "m").mkdir(parents=True, exist_ok=True)
        (_c46d / "src" / "main.py").write_text("x = 1\n", encoding="utf-8")
        (_c46d / "src" / "template" / "m" / "m.py").write_text("y = 1\n", encoding="utf-8")
        (_c46d / "src" / "template" / "m" / "README.md").write_text("# doc\n", encoding="utf-8")
        _c46_names = {n for n, _ in _freshness_inputs(_c46d, "demo")[0]}
        good = ("src/template/m/README.md" not in _c46_names
                and "src/template/m/m.py" in _c46_names
                and "src/main.py" in _c46_names)
        failed += 0 if good else 1
        print("[selftest] %s  C-46 module_doc_exempt_but_code_included: names=%s"
              % ("PASS" if good else "FAIL", sorted(_c46_names)))

        # [BROKEN]：**检查自身出错**必须独立成一档——不计 FAIL、不被 WARN 咽掉、并进退出码。
        # 用一条**故意抛异常**的判据作样本（历史实例：`check_md_tabs` 头上留着 `@check`，
        # 四个工具各报一条"检查异常"，看起来像工具坏了 ⇒ 一整轮排查方向是错的）。
        def _boom(_c):
            raise RuntimeError("simulated instrument failure")

        _brows = _run_checks(Ctx("broken-demo", base),
                             [("X-99", "FAIL", "整条判据抛异常（仪器故障样本）", _boom)])
        _bf, _bw, _bb = _print_rows(_brows, 0, 0, 0)
        good = (_bf, _bw, _bb) == (0, 0, 1)
        failed += 0 if good else 1
        print("[selftest] %s  BROKEN 档 %s: (fails,warns,broken)=%s want=(0,0,1)"
              % ("PASS" if good else "FAIL", "instrument_failure_is_its_own_tier",
                 (_bf, _bw, _bb)))

        print("[selftest] " + ("ALL PASS" if not failed else "%d FAILED" % failed))
        rc = 1 if failed else 0
    finally:
        # C-30 的作者自己也得守 C-30，且**必须消费返回值**（"我加了重试 ≠ 失败可见"）：
        # 删不掉就让退出码变红，而不是只在屏幕上飘一行 [FAIL]。
        if not _rmtree_strict(base):
            rc = 1
    return rc



# ---------------------------------------------------------------- C-46
# **重建新鲜度：分母必须是"构建输入集"，不能只有 `src/**`**（任务 #62，2026-09-19）。
# 口径（交接 §1.4）：`exe mtime > max(构建输入 mtime)`，排除 `__pycache__/` 与 `*.pyc`。
# **分母 = `src/**` ∪ `--add-data "SRC;DEST"` 的 SRC 清单**（= PyInstaller datas 的并集）。
# 为什么不能只有 src：四家都有 out-of-src 打包输入（`*.ico` / `resources/` / `locales/` /
#   `bin\plink.exe` / `doc/`）——只扫 src 时，"只有 datas 变了"的重建会被判成**新鲜**，
#   而真实产物是旧的（判据的分母小于事实的定义域，与 `#58` 的 R-10 扫描面同族）。
# 等级 WARN：它不是规范违规，而是"这批产物能不能作数"的信号；红 ⇒ 该产物不可作为回执。
# **必须报告取到最大值的那条路径**：只给一个布尔是"无法复核的结论"（receipt_check 的教训）。
_ADD_DATA_RE = re.compile(r'--add-data\s+"([^";]+);', re.I)
_FRESH_SKIP_DIRS = {"__pycache__"}
_FRESH_SKIP_SUFFIX = {".pyc"}


def _freshness_inputs(root: Path, app_id):
    """构建输入集：`src/**`（剔 pycache/pyc）∪ `build.bat|scripts/build.bat` 的 `--add-data` 源。

    返回 `(items, datas)`：`items=[(相对路径, mtime)]`；`datas` = 成功解析的 `--add-data` 源
    清单（扫描面声明用）。解析不出的源（仍含未展开 `%VAR%`）跳过——**扫描面必须自报缺口**。
    """
    items, datas = [], []

    def add_file(p: Path):
        try:
            items.append((p.relative_to(root).as_posix(), p.stat().st_mtime))
        except (OSError, ValueError):
            pass

    src = root / "src"
    if src.is_dir():
        for p in src.rglob("*"):
            if not p.is_file() or any(x in _FRESH_SKIP_DIRS for x in p.parts) \
                    or p.suffix.lower() in _FRESH_SKIP_SUFFIX:
                continue
            # **模块文档不计入分母**：`src/modules/**/*.md` 是派发件的 README（给人读的），
            # **不是构建输入** —— PyInstaller 只收 `--add-data` 显式列出的东西。旧口径全收
            # `src/**` ⇒ **只改 README 也会报"产物过期"**（噪音，且会诱导人去重建）。
            # （verifier 2026-09-19 复核提出；本轮两处 WARN 都有真代码支撑，故当时结论未受影响。）
            if p.suffix.lower() == ".md" and "template" in p.parts:
                continue
            add_file(p)
    for rel in ("build.bat", "scripts/build.bat"):
        bp = root / rel
        if not bp.exists():
            continue
        try:
            text = bp.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in _ADD_DATA_RE.finditer(text):
            raw = m.group(1).strip()
            s = raw.replace("%~dp0", str(root) + os.sep).replace("%CD%", str(root))
            if app_id:
                s = s.replace("%APPNAME%", app_id)
            if "%" in s:            # 还有未展开的变量 ⇒ 本判据读不出这个源，跳过并计入缺口
                continue
            sp = Path(s)
            if sp.is_file():
                add_file(sp)
                datas.append(raw)
            elif sp.is_dir():
                for p in sp.rglob("*"):
                    if p.is_file() and not any(x in _FRESH_SKIP_DIRS for x in p.parts) \
                            and p.suffix.lower() not in _FRESH_SKIP_SUFFIX:
                        add_file(p)
                datas.append(raw)
    return items, datas


def judge_freshness(exe_mtime, items):
    """**纯函数**（便于自证）：每个输入都早于 exe ⇒ 新鲜。

    返回 `(ok, newest_path, newest_mtime, n)`；`items` 为空 ⇒ `ok=None`（**不可判**，
    与"新鲜"必须可区分——§D8 第 6 条"0 命中与没东西可命中"）。
    """
    if not items:
        return None, None, None, 0
    newest = max(items, key=lambda it: it[1])
    return exe_mtime > newest[1], newest[0], newest[1], len(items)


@check("C-46", "WARN", "重建新鲜度：exe 必须比**全部构建输入**（src/** ∪ --add-data 源）新")
def c46(c: Ctx):
    """见上方注释。**分母补全**是任务 #62 的落地；缺 exe / 无输入 ⇒ 记"不可判"，不报绿。

    **本条不覆盖**（§4.1.33：判据必须自报边界）：`_internal/` 内容是否正确、生成物
    （`*.ico` / config 由脚本生成）的生成顺序、构建是否完整——那些由 build 门禁输出行回答
    （交接 §1.4：「FRESH 只证 exe 比源新，不证构建完整」）。
    """
    import time
    root = c.dir
    version, _where = tool_version(root)
    app_id = c.app_id or root.name
    exe = (root / "release" / ("%s-%s" % (app_id, version)) / ("%s.exe" % app_id)
           if version else None)
    if exe is None or not exe.is_file():
        return True, ("扫描面：无 `release/%s-<VERSION>/%s.exe`（判据不适用）"
                      % (app_id, app_id))
    items, datas = _freshness_inputs(root, app_id)
    ok, newest, mt, n = judge_freshness(exe.stat().st_mtime, items)
    if ok is None:
        return True, "扫描面：构建输入 0 件（不可判；空分母不等于新鲜）"

    def stamp(t):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))

    return ok, ("扫描面：构建输入 %d 件（其中 --add-data 源 %d 个）；exe=%s；"
                "max 输入=%s @ %s；%s"
                % (n, len(datas), stamp(exe.stat().st_mtime), newest, stamp(mt),
                   "全部输入早于 exe ⇒ 新鲜"
                   if ok else "**过期**：有构建输入比 exe 新 ⇒ 该产物不是这批输入的构建结果"
                   "（⚠ 本轮明确**不重建** ⇒ 该 WARN 是**预期读数**，如实留着、别为消它去构建；见 CONFORMANCE §5.1 C-46）"))
# ---------------------------------------------------------------- 主流程
def _run_checks(c: Ctx, checks, only=None):
    rows = []
    for cid, severity, title, fn in checks:
        if only and cid not in only:
            continue
        try:
            res = fn(c)
            # 允许检查**按分支**返回级别：`(ok, detail, "WARN")`——"判不了"不该按 FAIL 算
            # （设计纪律 ①：判不了的宁可 WARN；C-11 的"认不出形态"就是这一档）。
            if isinstance(res, tuple) and len(res) == 3:
                ok, detail, severity = res
            else:
                ok, detail = res
        except Exception as exc:
            # **[BROKEN]：检查自身出错 ≠ 检出违规**（lead 2026-09-19 批准立档）。
            # 两者在汇总里只差一个词（"检查异常" vs 一条违规），但处置方向**相反**：
            # 一个要改被检对象，一个要改判据自己。历史实例：`check_md_tabs` 头上留着
            # `@check` 装饰器（它是收 `Path` 的助手），于是四个工具各报一条"检查异常"，
            # 看起来像工具坏了——整整一轮的排查方向是错的（见 STANDARDS §J）。
            # 所以它必须**独立成档、进计数、进退出码**，否则会被当 WARN 咽掉。
            rows.append((cid, "BROKEN", title, False, "检查异常（仪器故障，非检出违规）: %r" % (exc,)))
            continue
        rows.append((cid, severity, title, ok, detail))
    return rows


def run_tool(name: str, only=None) -> tuple:
    c = Ctx(name, ROOT / name)
    return c, _run_checks(c, CHECKS, only)


def _print_rows(rows, fails, warns, broken=0):
    for cid, severity, title, ok, detail in rows:
        if ok:
            tag = "ok  "
        elif severity == "FAIL":
            tag = "FAIL"
        elif severity == "BROKEN":
            tag = "BROKEN"
        else:
            tag = "WARN"
        if not ok:
            if severity == "FAIL":
                fails += 1
            elif severity == "BROKEN":
                broken += 1
            else:
                warns += 1
        print("  [%s] %-5s %-46s %s" % (tag, cid, title, detail))
    return fails, warns, broken


def main() -> int:
    ap = argparse.ArgumentParser(description="family conformance check")
    ap.add_argument("--roots", nargs="*", default=None)
    ap.add_argument("--strict", action="store_true", help="WARN 也计入退出码")
    ap.add_argument("--only", nargs="*", default=None, help="只跑指定检查 ID")
    ap.add_argument("--selftest", action="store_true",
                    help="用合成样本反向自证 C-21..C-30（各检查的正反例）后退出")
    ap.add_argument("--temp-leak", action="store_true",
                    help="只读列出 %%TEMP%% 里命中家族 mkdtemp 前缀的目录（取证，永远 exit 0）")
    ap.add_argument("--temp-leak-save", default=None,
                    help="把当前命中目录名写入该文件，作为增量验收的基线")
    ap.add_argument("--temp-leak-baseline", default=None,
                    help="与基线文件比对，**只对新增残留**报红（残留免疫，历史存量不计）")
    args = ap.parse_args()
    if args.selftest:
        return selftest()

    def is_family_tool(d: Path) -> bool:
        """家族工具 = src\\ + 构建脚本（避免把同目录下的无关项目也拉进来）。"""
        return (d / "src").is_dir() and (
            (d / "build.bat").exists() or (d / "scripts" / "build.bat").exists())

    names = args.roots or sorted(
        d.name for d in ROOT.iterdir()
        if d.is_dir() and not d.name.startswith(("_", "."))
        and d.name not in {"__pycache__", TEMPLATE_DIR.name}
        and is_family_tool(d)
    )

    if args.temp_leak or args.temp_leak_save or args.temp_leak_baseline:
        return temp_leak_main(names, args.temp_leak_save, args.temp_leak_baseline)

    print(identity_line())   # 身份行：任何贴回来的输出自证"这是哪一版、哪个文件的产物"

    fails = warns = broken = 0
    only = set(args.only) if args.only else None

    # 模板正本跑一次（不按工具跑 N 次——它检查的东西与具体工具无关，重复输出只会淹信号）。
    trows = _run_checks(Ctx(TEMPLATE_DIR.name, TEMPLATE_DIR), TEMPLATE_CHECKS, only)
    if trows:
        print("=" * 78)
        print("%s  (模板正本, 只跑 TEMPLATE_CHECKS)" % TEMPLATE_DIR.name)
        print("  " + repo_identity(TEMPLATE_DIR))   # 被检仓库的修订与脏净（dirty=yes 一行暴露）
        print("=" * 78)
        fails, warns, broken = _print_rows(trows, fails, warns, broken)
        print()

    for name in names:
        tool_dir = ROOT / name
        if not tool_dir.is_dir():
            print("[skip] %s: no such dir" % name)
            continue
        c, rows = run_tool(name, only)
        print("=" * 78)
        print("%s  (APP_ID=%s)" % (name, c.app_id))
        print("  " + repo_identity(tool_dir))   # 每个 --roots 仓库各一行：rev + dirty
        print("=" * 78)
        fails, warns, broken = _print_rows(rows, fails, warns, broken)
        print()

    print("summary: %d FAIL, %d WARN, %d BROKEN（检查自身出错——该改的是判据，不是被检对象）"
          % (fails, warns, broken))
    if broken:
        print("fix: [BROKEN] 是**判据自己**出错（仪器故障），先修 conformance_check.py；"
              "它不计入 FAIL、也不被 WARN 咽掉，独立进退出码。")
        return 1
    if fails:
        print("fix: 逐条见 my-diy-tool-template/合规对照表.md 对应 ID。")
        return 1
    if warns and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
