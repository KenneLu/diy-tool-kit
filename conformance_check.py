# -*- coding: utf-8 -*-
# TEMPLATE-MODULE: conformance_check | TEMPLATE-VER: 1.9.4
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
#      `STANDARDS.md:492` 的 `System32<0x0c>ind.exe`（应为 `System32\find.exe`）、
#      `CONFORMANCE.md` 的 `%TEMP%<0x0d>eme-helper-builddata`（应为 `%TEMP%\reme-helper-builddata`）。
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
    # HEAD 一并打印（lead 指定）：它是"这份输出属于哪个提交"的最短答案。
    # 取不到就印 `?`——不在 git 仓 / 无 git / 超时都不该让判据崩（**不许因此报错**）。
    head = "?"
    try:
        r = subprocess.run(["git", "-C", str(TEMPLATE_DIR), "rev-parse", "--short", "HEAD"],
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0 and r.stdout.strip():
            head = r.stdout.strip()
    except Exception:
        pass
    # `at:`（lead 2026-09-19 加，"计数必须带时点"）：**任何"命中 N 个"的转述都需要时点**——
    # 残留集是活的（本轮 reme 从 8 变 5：消失 4、新增 1），缺时点的数字会让接收方去找
    # 已不存在的东西。**扫描面说"扫了什么"，时点说"什么时候"**，两者齐了读数才可判。
    import time as _time
    at = _time.strftime("%Y-%m-%dT%H:%M:%S")
    return ("# conformance_check %s  sha256:%s  norm:%s  head:%s  at:%s"
            % (ver, hashlib.sha256(raw).hexdigest()[:12],
               hashlib.sha256(norm.encode("utf-8")).hexdigest()[:12], head, at))

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
            guess = self._find("src/modules/tray_kit/tray_kit.py")
            if guess is None:
                for p in self.py_files():
                    if re.search(r"^\s*def\s+acquire_single_instance\b",
                                 self.read(p), re.M):
                        guess = p
                        break
            self._cache["guard"] = guess
        return self._cache["guard"]

    def has_i18n(self) -> bool:
        return bool(self._find("src/modules/i18n/i18n.py", "src/i18n.py")
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
    std = TEMPLATE_DIR / "STANDARDS.md"
    if not std.exists():
        return True, "无 STANDARDS.md"
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


@check("C-06", "WARN", "两份 README 都随 release 复制（DOC-05）")
def c06(c: Ctx):
    text = c.build_blob
    if not text:
        return False, "找不到 build.bat"
    has_zh = "README.zh-CN.md" in text
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
    lk = c._find("src/modules/log_kit/log_kit.py", "src/log_kit.py", "log_kit.py")
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
    mods = c.src / "modules"
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
    mods = c.src / "modules" / "i18n"
    if (mods / "pairs.json").exists():
        return True, "重形态（pairs.json 中文即键，STANDARDS §E4 明示许可），跳过"
    if not c.has_i18n():
        return True, "未启用 i18n（T1 未触发或待办）"
    if c.entry is None:
        return True, "无入口文件"
    try:
        tree = ast.parse(c.read(c.entry))
    except SyntaxError as exc:
        return False, "入口文件语法错误: %s" % exc
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
                        and CJK.search(sub.value):
                    bad.append("%s:%d %s" % (c.entry.relative_to(c.dir).as_posix(),
                                             sub.lineno, sub.value[:60]))
    return (not bad), ("词表外中文 %d 处: %s" % (len(bad), " | ".join(bad[:4]))
                       if bad else "未发现词表外中文（AST 级）")


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
    mods = c.src / "modules"
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
    mods = c.src / "modules"
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
    mods = c.src / "modules"
    if not mods.is_dir():
        return True, "无 src/modules/"
    code = [p for p in c.py_files()
            if "modules" not in p.relative_to(c.src).parts[:1]
            and p.name != "__init__.py"]
    bad, declared = [], 0
    for d in sorted(x for x in mods.iterdir() if x.is_dir()):
        # 声明取**模板正本**（`TEMPLATE_DIR/modules/<m>/README.md`）优先：要求是模块的属性，
        # 不该等工具把带锚点的 README 拷过去之后才生效——否则锚点加上当天所有工具都"无声明"，
        # 检查空转（首版实测）。工具侧 README 也读，兼容工具自己追加的声明。
        readmes = [p for p in (TEMPLATE_DIR / "modules" / d.name / "README.md",
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


def _self_identifying(root: Path):
    """工具 `src/**/*.py` 里是否存在"把数据根/配置路径打进日志"的那一行。

    返回 `(ok_or_None, [(相对路径, 行号, 行内容)])`；`None` = 无 `src/`（判据不适用）。
    模板 `paths.py` 的**副本**也在 `src/modules/paths/` 下，所以"在模板里加一行"对四家同时生效。
    """
    src = root / "src"
    if not src.is_dir():
        return None, []
    hits = []
    for f in sorted(src.rglob("*.py")):
        try:
            for i, line in enumerate(f.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
                if "log(" not in line and "print(" not in line:
                    continue
                if any(n in line for n in _SELF_ID_NAMES):
                    hits.append((f.relative_to(root).as_posix(), i, line.strip()))
        except OSError:
            continue
    return bool(hits), hits


@check("C-38", "WARN", "启动自证：日志里必须能看到解析后的数据根 / 配置文件路径")
def c38(c: Ctx):
    """**为什么是 WARN 而不是 FAIL**：缺它不会让用户看到任何异常，只会让**下一次残留归属
    无据可依**——而那正是本次三个 `tmp*` 目录耗掉一整轮取证的原因（它们出自 `python -c` /
    heredoc，**不落盘**，外部扫描原理上够不着）。等级由 lead 定（他倾向 WARN；我实测 3/4 家未做，
    且修复路径是**模板一处**：`paths.seed_config()` 加一行 ⇒ 四家重拷后同时具备）。

    **为什么"扫源码里有没有那一行"就够**：我们不需要判它的格式好不好看，只需要保证
    **那次解析的结果会落进日志**——这正是"把不可查的纪律换成可查的性质"。
    """
    ok, hits = _self_identifying(c.dir)
    if ok is None:
        return True, "扫描面：无 src/（判据不适用）"
    if ok:
        return True, ("扫描面：src/**/*.py 全部；启动自证行 %d 处（%s）"
                      % (len(hits), ", ".join("%s:%d" % (h[0], h[1]) for h in hits[:3])))
    return False, ("扫描面：src/**/*.py 全部；**0 处**把数据根/配置路径写进日志的行。"
                   "【为什么值得做】`python -c`/heredoc 探针**不落盘**，源码扫描原理上覆盖不到它们；"
                   "能定死归属的只有**产物自带的那行日志**（如 `config seeded: <源> -> <目标>`）。"
                   "【正确形态】在 `seed_config()` 或启动早期 `log()` 一行，写出 `USER_DATA_DIR` 与 "
                   "`CONFIG_PATH` 的**解析结果**（不是常量、不是假设值）")


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
            if "modules" not in p.relative_to(c.src).parts[:1] and p.name != "__init__.py"]
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
                items = val.elts if isinstance(val, (ast.List, ast.Tuple)) else [val]
                got = []
                for item in items:
                    if isinstance(item, ast.Constant) and isinstance(item.value, str) and item.value:
                        got.append(item.value)
                    else:
                        problems.append((rel_file, "登记 `%s` 的值不是非空字符串字面量（是%s）——"
                                         "判据与 %%TEMP%% 取证都读不到，等于没登记"
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
    files = _py_files_under(c.dir)
    texts = [(p, c.read(p)) for p in files]
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
                         "确实推不出的（如 f-string 拼 APP_ID）在 %s 登记等价前缀，例如\n"
                         "    %s = {\"src/main.py:7405\": \"reme-update-\"}   "
                         "# 键 = 站点「相对路径:行号」，值 = 该处前缀的等价字面量（可为列表）\n"
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
TMP_DECLARED_PATHS = {
    "reme-helper-builddata":
        "reme-helper/scripts/build.bat:22 set \"REME_HELPER_DATA_DIR=%TEMP%\\reme-helper-builddata\""
        "（固定名、全文无清理）",
}


def _shape_hits(T: Path):
    """腿 B：按**结构签名**找残留（不看目录名，免疫命名猜测）。返回 `[(名字, 触发路径)]`。

    签名 = "**隔离数据根**"的不变量 = **有一个 `log` 目录**（B3：日志一律落
    `<数据根>/log/<工具名>.log`）。返回触发路径供人工判读——"命中了"与"命中了什么"必须同时可见。

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
         `kzip_sogou`、`ai/rp/task_outputs/.../output.log` ⇒ **太宽，制造假红**，否掉
      V2 「存在 `log` **目录**（任意深度）」              8 命中 —— 7 个是自家数据根 + 1 个外来程序（`kzip_sogou`）
     ⇒ 采用 V2。**残余假阳性风险在案**：外来程序自己的 `log/` 目录会被算作命中。
    """
    hits = []
    for d in sorted(T.iterdir()):
        if not d.is_dir() or d.name in TMP_DECLARED_PATHS:
            continue
        try:
            for root, dirs, _files in os.walk(d, onerror=lambda _e: None):
                if "log" in dirs:
                    rel = Path(root, "log").relative_to(d).as_posix()
                    hits.append((d.name, rel))
                    break
        except OSError:
            continue
    return hits


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


def _declared_present(T: Path):
    """白名单里**确实存在于 %TEMP%** 的那些（只报出来，不计入并集/增量）。"""
    out = []
    for name, why in sorted(TMP_DECLARED_PATHS.items()):
        try:
            if (T / name).is_dir():
                out.append((name, why))
        except OSError:
            pass
    return out


def _temp_hits(prefixes, T):
    """腿 A：按**从源码枚举/登记**的前缀找残留。返回 [(前缀, 目录名, mtime, 文件数)]。"""
    import time
    hits = []
    for d in sorted(T.iterdir()):
        if not d.is_dir():
            continue
        for pref in prefixes:
            if pref and d.name.startswith(pref):
                try:
                    nfiles = len([f for f in d.rglob("*") if f.is_file()])
                    mtime = time.strftime("%m-%d %H:%M", time.localtime(d.stat().st_mtime))
                except OSError:
                    nfiles, mtime = 0, "(不可读)"
                hits.append((pref, d.name, mtime, nfiles))
                break
    return hits


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

    print(identity_line())   # 取证输出也要自证身份
    print("== 扫描面 ==")
    # 扫描面必须**可比对**：`%TEMP%` 经环境变量常是 8.3 短名（`ADMINI~1`），
    # 两个人各贴一份输出会对不上"是不是同一个根"。故同时打印解析后的规范长路径。
    print("  目录: %s   （解析后: %s）" % (T, Path(T).resolve()))
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

    hits_a = _temp_hits(all_prefs, T)
    names_a = sorted({d for _, d, _, _ in hits_a})
    hits_b = _shape_hits(T)
    why_b = dict(hits_b)
    names_b = sorted(why_b)
    union = sorted((set(names_a) | set(names_b)) - set(TMP_DECLARED_PATHS))
    print("== 腿 A：生成器派生（前缀）命中 %d ==" % len(names_a))
    by_pref = {}
    for pref, dname, ts, nfiles in hits_a:
        by_pref.setdefault(pref, []).append((dname, ts, nfiles))
    for pref, items in sorted(by_pref.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        print("  %-26s %2d 个" % (pref, len(items)))
        for dname, ts, nfiles in items[:3]:
            print("        %-30s %s 文件%2d%s" % (dname, ts, nfiles, "" if nfiles else " (空目录)"))
        if len(items) > 3:
            print("        ... 还有 %d 个" % (len(items) - 3))
    print("== 腿 B：形态派生（不看名字）命中 %d ==" % len(names_b))
    only_b = [d for d in names_b if d not in names_a]
    for d in names_b[:12]:
        print("        %-30s %-26s%s" % (d, why_b[d], "" if d in names_a else "  <- 腿 A 的盲区"))
    if len(names_b) > 12:
        print("        ... 还有 %d 个" % (len(names_b) - 12))
    # 名字形态直方图：**把"有残留"变成"该去改谁"**——带点 ⇒ shell `mktemp -d`
    # （进程规则/外部 CLI 造的，源码里没有可枚举的调用点）；无点 ⇒ Python `mkdtemp()`。
    print("  名字形态直方图：%s" % _shape_histogram(names_b))
    print("     ↑ 带点（`tmp.<10>`）= GNU `mktemp -d`（shell/外部 CLI）；无点（`tmp<8>`）= Python `mkdtemp()`。"
          "前者**源码里没有调用点**，只能靠形态腿，且要改的是**进程规则**而不是代码")
    declared = _declared_present(T)
    if TMP_DECLARED_PATHS:
        print("== 已声明位置（**不算泄漏**，不计入并集与增量）现场命中 %d / 登记 %d =="
              % (len(declared), len(TMP_DECLARED_PATHS)))
        for n, why in declared:
            print("        %-30s %s" % (n, why))
    reg = {n for v in _TEMP_REGRESSION_20260919.values() for n in v}
    print("== 并集 %d 个；其中 %d 个在腿 A 命中之外（腿 B 独有）；"
          "命中已登记回归集 %d/%d =="
          % (len(union), len(only_b), len(set(union) & reg), len(reg)))
    # 扫描面报**目录数**：lead 那次把"条目数"（目录+文件）当成了目录数（634 vs 101），
    # 于是两个人贴出来的扫描面根本不可比。两个数**显式带标签**一起报。
    n_dirs = len([d for d in T.iterdir() if d.is_dir()])
    n_entries = len(list(T.iterdir()))
    print("RESULT: 扫描顶层**目录** %d 个（顶层条目 %d = 目录+文件）"
          " / 腿 A 前缀 %d 个 / 命中 A=%d B=%d 并集=%d / 已声明 %d"
          % (n_dirs, n_entries, len(all_prefs), len(names_a), len(names_b), len(union),
             len(TMP_DECLARED_PATHS)))
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
_PING_TICK = re.compile(r"\bping(?:\.exe)?\b[^\n]*?\s-(?:n|w)\b", re.I)


def _code_only_text(p: Path, text: str) -> str:
    """**注释不算违规**（纪律 ④(c)：这里要抓的是会被执行的节拍）。

    `.py`：用 `tokenize` 把 `COMMENT` 词法单元挖掉（不碰字符串——渲染 bat 的 `.py` 模板
    正是**字符串**，那才是要查的东西）；`.bat`/`.cmd`：逐行丢掉 `rem` / `::`。
    **两件都做**：渲染出来的 bat 会以 `rem` 行形式存在字符串里。
    """
    if p.suffix.lower() == ".py":
        import io
        import tokenize
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
    """`root` 下的 `.py`/`.bat`/`.cmd` 不得用 `ping -n/-w` 当节拍。返回 `(ok, detail)`。"""
    hits = []
    files = [p for p in root.rglob("*")
             if p.is_file() and p.suffix.lower() in (".py", ".bat", ".cmd")
             and not any(part in _PY_SKIP_DIRS for part in p.parts)]
    for p in sorted(files):
        text = _code_only_text(p, p.read_text(encoding="utf-8", errors="replace"))
        rel = p.relative_to(root).as_posix()
        for n, m in enumerate(_PING_TICK.finditer(text), 1):
            hits.append("%s(命中%d) `%s`" % (rel, n, m.group(0).strip()[:40]))
    if hits:
        return False, ("%d 处用 ping 当等待节拍：%s。【为什么是硬违规】`ping -n 2` 的\"1 秒\""
                       "只在 loopback ICMP 有响应时成立；丢弃 ICMP 的机器上实测 **9.0s/拍**"
                       "（两次 4.5s 超时），名义 120s→实际 ~18 分钟，而超时日志仍写\"120s\""
                       "（**日志说谎**）。改用不依赖网络的睡眠："
                       "`powershell -NoProfile -Command \"Start-Sleep -Milliseconds 1000\"`"
                       "（DETACHED 进程无 console，子进程不会弹窗）"
                       % (len(hits), ", ".join(hits[:8])))
    return True, "没有把 ping 当等待节拍"


@check("C-33", "FAIL", "禁拿 `ping` 当等待节拍（依赖网络配置，实测差 9 倍）")
def c33(c: Ctx):
    """见 `check_ping_tick` 上方注释。工具侧扫全仓 `.py`/`.bat`/`.cmd`。"""
    return check_ping_tick(c.dir)


@template_check("C-33", "FAIL", "模板派发件里的同一形态（模板正本只跑一次）")
def c33_template(c: Ctx):
    """模板侧只扫 `modules/**`——那是会被拷进工具的正本代码（含渲染 bat 的 `.py` 模板）。"""
    return check_ping_tick(c.dir / "modules")


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
    mods = c.dir / "modules"
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
    py = c.dir / "modules" / "paths" / "paths.py"
    rd = c.dir / "modules" / "paths" / "README.md"
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
        paths = importlib.import_module("modules.paths.paths")
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
    mods = root / "modules"
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
    return check_evidence_order(c.dir / "modules")


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
            d = base / name / "src" / "modules" / "demo"
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
            d = base / ("c23_" + name) / "src" / "modules" / "demo"
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
            d = base / ("c27_" + name) / "src" / "modules" / "demo"
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
            ("fstring_prefix_registered_ok",
             "import tempfile\n"
             "TMP = tempfile.mkdtemp(prefix=f'{APP_ID}-update-')\n"
             "\n"
             "TMP_PREFIX_REGISTRY = {\n"
             "    'src/main.py:2': 'app-update-',\n"
             "}\n", True, None),
            ("registry_value_not_literal_flagged",
             "import tempfile\n\n"
             "TMP_PREFIX_REGISTRY = {'src/main.py:4': PREFIX}\n\n"
             "TMP = tempfile.mkdtemp(prefix=f'{APP_ID}-update-')\n", False, None),
            ("registry_stale_entry_warn",
             "import tempfile\n\n"
             "TMP_PREFIX_REGISTRY = {'src/main.py:99': 'app-old-'}\n\n"
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
        c30_cases = (
            ("verified_cleanup_ok", _cleanup_ok, True),
            ("ignore_errors_on_mkdtemp_root_flagged", _cleanup_bad, False),
            ("ignore_errors_through_wrapper_flagged", _cleanup_wrapper, False),
            ("ignore_errors_on_scratch_subdir_ok", _cleanup_subdir, True),
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
        # 白名单判别样本：名字与内容都命中形态，但**已声明** ⇒ 不得进命中集。
        _mk_shape("reme-helper-builddata", ["log/x.log"])
        (fake_tmp / "just-a-file.txt").write_bytes(b"x")   # 顶层文件不是目录 → 不命中
        got_shape = {n for n, _why in _shape_hits(fake_tmp)}
        want_shape = {"icon-probe-077hxtaw", "smoke-proof-nl6gj9kf",
                      "two-subs", "config-at-top", "nested-no-config"}
        good = got_shape == want_shape
        failed += 0 if good else 1
        print("[selftest] %s  C-30/shape %s: got=%s want=%s"
              % ("PASS" if good else "FAIL", "name_agnostic_shape", sorted(got_shape),
                 sorted(want_shape)))

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
             {"modules/demo/a.py": b"x = 1\r\ny = 2\r\n",
              "modules/demo/README.md": b"# demo\r\n"}, True),
            ("lf_only_dispatched_flagged",
             {"modules/demo/a.py": b"x = 1\ny = 2\n"}, False),
            ("mixed_eol_flagged",
             {"modules/demo/a.py": b"x = 1\r\ny = 2\n"}, False),
            ("template_only_dir_ignored",
             {"modules/build_release/tool.py": b"x = 1\n"}, True),
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
        print("fix: 逐条见 my-diy-tool-template/CONFORMANCE.md 对应 ID。")
        return 1
    if warns and args.strict:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
