# ALIGNMENT.md —— 一式五份收敛表（副本 ↔ 模板正本）

> 建立：2026-09-19。对应 `sync_check.py` **1.4.0**（双通道 + `.py`/`.md` 全件比对）。
> 本文只回答一个问题：**每个工具里的每个拷贝件，与模板正本像不像？不像则怎么收敛？**
> **不做**条款符合度裁定——"能力/条款做没做到"看 [CONFORMANCE.md](CONFORMANCE.md)（76 条 × 四工具矩阵），
> "本轮改了什么"看 [REVIEW.md](REVIEW.md)。三者边界：
>
> | 文档 | 管什么 | 判据 |
> |---|---|---|
> | **ALIGNMENT.md**（本文） | 副本与正本的**形状**是否一致 | 归一化哈希 + `TEMPLATE-VER` + 头部申报 |
> | CONFORMANCE.md | 规范条款是否**落地** | 语义级 76 条，人工 + `conformance_check.py` |
> | REVIEW.md | 复审**过程与记录** | R1/R2/R3 三轮留痕 |
>
> 交叉警示：**SAME ≠ 在役**。反例见 §T-service_link——reme 的副本字节一致却从未被 import。

## 0. 判定口径与图例

`sync_check.py` **1.4.0** 是**双通道**扫描 + 整模块缺失检测，均做归一化哈希（剔除 `# TEMPLATE-*` 元信息行）：
① 头部通道（工具自报 `TEMPLATE-FROM`）；② 布局通道（`src/modules/<模块>/` 下与模板同名者一律比对，
**不要求工具侧有头**）；③ 模板 `modules/<模块>/` 有代码而工具既无目录又无申报 → 整模块缺失。
扫描范围 **.py + .md**，排除模板专属目录 `baseline/` `build_release/` 与 `__pycache__` 等生成目录。
CONFORMANCE §4.1.9 的三类盲区（无头文件 / 整模块缺失 / `__init__.py`）与 §4.1.10 的第 4 盲区
（模块 README 隐身）均已闭环。

> **「整文件夹采纳」的正式定义（1.4.0 固化）**：一个模块被采纳 =
> **`README.md` + `__init__.py` + 代码文件**，三者都要与模板一致。
> `.py` 按**归一化哈希**（剔 `TEMPLATE-*` 行）；**`.md` 按逐字节哈希**。
> 只给 `.py` 装闸而让 `README.md` 无闸，等于"模块文档可以无限漂移"——这正是第 4 盲区。
> 模板专属目录（`baseline/`、`build_release/`）**不适用**本定义：它们不拷贝进 `src/modules/`。
>
> **`.md` 口径（CONFORMANCE §4.1.10a）**：模块 README **不带任何 TEMPLATE 头，与正本逐字节一致**。
> 头机制是为代码副本设计的（剔掉出处行再比哈希），而 markdown 标题也以 `#` 开头，沿用会把
> `# TEMPLATE-FROM:` 静默吞掉，使"带头/不带头"都判相等。故 `.md`：要么 `[ok]`，要么 `[DIFF]`，
> **绝不产生 `[NOHDR]`**，也不参与头/VER 判定。
> **唯一例外（模块级 OVERRIDE）**：同模块任一 `.py` 已申报 `TEMPLATE-LOCAL-OVERRIDE` 时，
> 整模块已申报差异，其 README 不可能一致 → 记 `[decl]`（已申报），不记 `[DIFF]`
> （实例：reme 重形态 `i18n/`）。**注意：`[decl]` 只表示"差异已留痕"，不表示"差异获准"**
> （获准只有两条前提，见 §3 首段）；输出带**申报来源**（如 `(declared via __init__.py)`），
> 让"已申报差异"与"漏拷"一眼可分。`[NOHDR]` **仅保留给 `.py`**。
>
> **反向自证（已固化为可重复执行的回归样本）**：`python my-diy-tool-template/sync_check.py --selftest`
> —— A 带头 `.md` → `[DIFF]`；B 逐字节相同 → `[ok]`；C 模块 `.py` 带 OVERRIDE 且 README 不同
> → `[decl]`。三条全 PASS 则退出码 0，任一条不符则 1。**不写成一次性命令**：判据若被改坏，
> 回归样本要能自动喊出来。

| 状态 | 含义 | sync_check 标签 | 阻断退出码 |
|---|---|---|---|
| `SAME` | 归一化一致且 VER 相同 | `[ok]` | 否 |
| `LAG(x→y)` | 内容/VER 落后模板；**蓝本**报黄灯，普通工具报红灯 | `[lag]` / `[DRIFT]` | 蓝本否 / 普通是 |
| `PARAM` | `appconfig.py`，参数文件按设计豁免（F2/D6/D15） | `[param]` | 否 |
| `OVERRIDE` | 有差异且已申报 `# TEMPLATE-LOCAL-OVERRIDE:` | `[decl]` | 否 |
| `NOHDR` | 落在 `src/modules/<模块>/`、模板有同名件、不一致且**工具侧无头** | `[NOHDR]` | 否（黄灯） |
| `INLINE` | 工具内联实现，不在 `src/modules/<模块>/` 也无头 | 由 `[MISSING-MODULE]` 间接暴露 | 否 |
| `MISSING-MODULE` | 模板 `modules/<模块>/` 有代码，工具无目录且无申报 | `[MISSING-MODULE]` | 否（黄灯） |
| `MISSING-FILE` | 模块已被采纳（目录在/有文件申报来自它），但模板里的某个件工具侧没有 | `[MISSING-FILE]` | 否（黄灯） |
| `DIFF(.md)` | 非代码件（模块 README）与正本**逐字节不一致**；无头、不参与头/VER 判定。**例外**：同模块任一 `.py` 已申报 OVERRIDE → 记 `[decl]` | `[DIFF]` / `[decl]` | 否（黄灯） |
| `MISSING` | 头部申报的模板路径不存在 | `[MISS]` | **是**（红灯） |
| `N/A` | 设计上本就不该拷贝 | — | — |

### 0.1 快照与并发声明（重要）

> **「可重拷」宣告纪律（规范正文见 STANDARDS B4）**：**宣告 = 一次冻结承诺；宣告之后模板侧任何编辑都会立即作废它。**
> 顺序必须是 **先改完 → 再冻结 → 最后宣告**；若宣告后仍有改动，**必须重新宣告并写明"变了哪几个文件"**。
> 宣告要**到文件级**（例："`modules/i18n/` 以 `f1547d0` 为准；`i18n.py`/`__init__.py` 未变，仅 `README.md` 需补拷"）。
> 机械佐证：`git diff --stat <宣告sha> HEAD -- <模块>/`。
> 实例见 §2 T5：i18n 2.1.1 先宣告、后改 README 三行，使两工具的 `[ok]` 退回 `[DIFF]`（根因是指令顺序）。

下表是 **2026-09-19 的一次磁盘快照**，而队友 #2（reme-helper 收敛）、#3（l-s2t 收敛）、
#4（dsh/ocx 补 autostart）**正在并发改动四个工具**，矩阵是移动靶。使用规则：

1. **以实时 `sync_check` 输出为准**，本文只提供"目标态 + 改动清单 + 风险"；
2. 行号引用可能随队友改动漂移，**优先按函数名定位**，行号仅作辅助；
3. 复现本文数据：

```bat
python my-diy-tool-template\sync_check.py
python my-diy-tool-template\sync_check.py --roots reme-helper local-speak2text
python my-diy-tool-template\conformance_check.py --roots reme-helper
```

本次快照的 `sync_check` 摘要（**退出码 0**，1.4.0：`.py + .md`、`.md` 逐字节；以实时输出为准）：
`0 undeclared drift, 0 blueprint lag(s), 3 declared override(s), 4 param file(s),`
`0 doc byte-diff(s), 0 no-header mismatch(es), 9 missing module(s), 6 missing file(s)`。
3 条 `[decl]` = reme `i18n/` 整模块（`i18n.py`、`__init__.py`、`README.md`）
——reme 重形态 `i18n`（**方案差异，依据见 §3.2**），README 随模块一并 `[decl]`；
6 条 `MISSING-FILE` = dsh/l-s2t/ocx
各缺 `icons/README.md` 与 `icons/__init__.py`（icons 包化波次的已知缺口，保持黄灯）。
`[DIFF]`、`[NOHDR]` 均归零。
模板升位瞬间曾出现 **4 条红灯**（dsh/ocx 各 2 条：`paths` 1.1.2→**1.1.3**、`tray_kit`
2.0.1→**2.0.2**），属 §0.2 级联清单的预期中间态；**dsh/ocx 已在同步波次中重拷，红灯自消**。
数字随队友收敛持续下降——**以实时命令输出为准**。

**模板侧本轮新增变更（影响所有副本）**：`modules/*/__init__.py` 统一为
`# TEMPLATE-MODULE: <模块> | TEMPLATE-VER: <版本>` + `from .<模块> import *  # noqa: F401,F403`
（CRLF、纯 ASCII，与 dsh/ocx 多数派一致），并给 `modules/icons/` 补了 `__init__.py`；
**`__init__.py` 的 VER 必须镜像同模块正本 VER**（本轮已同步 appconfig/paths/tray_kit 三处）。
各工具 `src/modules/*/__init__.py` 需按此回基（见 §4 序 1a）。

### 0.2 上一轮模板升位与级联清单（**已下发**）

"模板先冻结、工具再收敛"的最后一轮，模板侧 4 处改动 + 版本号：

| # | 模板文件 | 旧 → 新 VER | 性质 | 必须重拷的副本 |
|---|---|---|---|---|
| 1 | `modules/appconfig/appconfig.py` | 1.0.0 → **1.0.1** | 修 `ICON_DRAW` 签名矛盾 + 补 `ICON_ASSET = None` | **无**（`[param]` 豁免比对；但 `appconfig/__init__.py` VER 随之升，见 #2 行注） |
| 2 | `modules/appconfig/__init__.py` | 1.0.0 → **1.0.1** | VER 镜像模块正本 | 带 VER 头的副本（l-s2t `[lag]` 黄灯）；无头副本内容不变仍 `[ok]` |
| 3 | `modules/paths/paths.py` + `__init__.py` | 1.1.2 → **1.1.3** | 补 `<APP_ID 派生>_CONFIG`（兑现 README 承诺，§4.1.5） | **dsh-helper、opencodex-helper（红灯必改）**；l-s2t/reme 蓝本黄灯 |
| 4 | `modules/tray_kit/tray_kit.py` + `__init__.py` | 2.0.1 → **2.0.2** | 退出确认/重复启动文案参数化（E4-02）+ 无勾选项形态 | **dsh-helper、opencodex-helper（红灯必改）**；l-s2t/reme 蓝本黄灯 |

`modules/icons/__init__.py`（2.0.0，上一轮已加）**四工具中 reme 外三家仍缺** → `[MISSING-FILE]` 黄灯：
dsh-helper、local-speak2text、opencodex-helper 各补一份（`from .icons import *  # noqa: F401,F403`）。
reme 因 `icons` 整模块未采纳，记 `[MISSING-MODULE]`。

### 0.3 本轮模板升位与级联清单（**下发用**，2026-09-19 第二轮）

本轮按**用户仲裁规则**（STANDARDS §B4：公共件冲突以 reme-helper 的**已验证实现**为基准，
不看"用的人多"）重写 `modules/update_helper/`，并给 `sync_check.py` 加 E 组回归。

| # | 模板文件 | 旧 → 新 VER | 性质 | 必须重拷的副本 |
|---|---|---|---|---|
| 1 | `modules/update_helper/update_helper.py` | 1.1.0 → **1.3.0** | 照 reme 已验证链路补齐**失败回退**：替换前快照且成功才轮转、检查 robocopy rc、失败回铺、失败 marker、sha256 缺失即中止（fail-closed） | **dsh-helper、opencodex-helper（红灯必改）** |
| 2 | `modules/update_helper/__init__.py` | 1.1.0 → **1.3.0** | 新增导出 `verify_zip_sha256` / `pop_failed_update_note` / `failed_marker_path` | 同上（整夹重拷） |
| 3 | `modules/update_helper/README.md` | — （逐字节） | 接口表补 3 行；替换脚本语义要点从 2 条扩到 6 条；采纳步骤加"启动 sweep + 读失败 marker" | 同上（整夹重拷） |
| 4 | `sync_check.py` | 1.4.0 → **1.5.0** | `--selftest` 新增 E 组（替换脚本语义正向 17 项 + 旧形态反向） | **无**（设计不拷贝：门禁按路径调用模板正本） |

**新增采纳动作（不只是重拷）**：dsh/ocx 在启动流程里加两行——
`sweep_stale_update_dirs()`（清残留）与 `note = pop_failed_update_note(update_dir)`（非空则 notify）。
不加这两行不会报错，但"上次更新失败"就又变成无声消失（这正是 1.3.0 要消灭的形态）。

**`.sha256` 前置条件**：1.3.0 起缺 `.sha256` 即中止更新。dsh/ocx 的 `release.yml` 均已于
`gh release create` 时上传 `.zip.sha256`（已核对两仓库 workflow），故不会断更新。

## 1. 主矩阵（模板件 × 四工具）

行首 VER = 模板正本当前 VER；"收敛中" = 队友当轮正在改、尚未落定。

| 模板件 (VER) | reme-helper | local-speak2text | dsh-helper | opencodex-helper |
|---|---|---|---|---|
| **appconfig.py** (1.0.1) | `PARAM` 参数不同；另申报 VERSION 不入此文件、ICON_DRAW 不启用 | `PARAM` 已建 `src/modules/appconfig/appconfig.py` | `PARAM` 参数不同；ICON_ASSET 手工 png，VERSION 在 `main.py` | `PARAM` 参数不同；ICON_DRAW 自绘，VERSION 在 `main.py` |
| **paths.py** (1.1.3) | `SAME` 1.1.3（**已跟进**，队友 #2；dev `RUN_DIR` 分叉随 OVERRIDE 保留） | `SAME` 1.1.3（**已跟进**）；模板补 `_CONFIG` 后原 OVERRIDE 已撤 | `SAME` 1.1.3（**已重拷**，红灯自消） | `SAME` 1.1.3（**已重拷**，红灯自消） |
| **autostart.py** (1.1.1) | `MISSING-MODULE` 内联在 `main.py`（含模板没有的 `sync_autostart_path` 自愈；倾向反向沉淀） | `SAME` 1.1.1（**已抽件**，队友 #3） | `SAME` 1.1.1（**已抽件**，队友 #4） | `SAME` 1.1.1（**已抽件**，队友 #4） |
| **update_helper.py** (1.3.0) | `MISSING-MODULE` **内联且已验证**（main.py 7098-7345）——模板 1.3.0 的基准就是它，见 §7.1 | `MISSING-MODULE` 变体 `src/updater.py`（稳定位 + `update.pending.json`），**无头** | `[DIFF]` 停在 1.1.0：缺快照/rc/回铺/marker/fail-closed（**红灯**，本轮重拷） | `[DIFF]` 同左 |
| **i18n.py** (2.1.1) | `NOHDR` 重形态 `modules/i18n/i18n.py`(204 行，差 303 行) + `pairs.json`；缺模板头 | `SAME` 2.1.1 | `MISSING-MODULE` | `MISSING-MODULE` |
| **icons.py** (2.0.0) | `MISSING-MODULE` 内联 `make_icon`/`make_taskbar_icon`/`icon_font`（运行态着色不同构） | `SAME` 2.0.0（`src/icons.py` 已消费模板）；缺 `icons/__init__.py` → `MISSING-FILE` | `SAME` 2.0.0（`ICON_ASSET`，头部申报）；缺 `icons/__init__.py` → `MISSING-FILE` | `SAME` 2.0.0（`ICON_DRAW`）；缺 `icons/__init__.py` → `MISSING-FILE` |
| **tray_kit.py** (2.0.2) | `SAME` 2.0.2（**已跟进**，队友 #2） | `SAME` 2.0.2（**已跟进**，队友 #3） | `SAME` 2.0.2（**已重拷**，红灯自消） | `SAME` 2.0.2（**已重拷**，红灯自消） |
| **log_kit.py** (1.0.2) | `SAME` 1.0.2（**已回基**，队友 #2，root-logger 分叉已并入正文或撤销） | `SAME` 1.0.2（**已收敛**，队友 #3） | `SAME` 1.0.2 | `SAME` 1.0.2 |
| **service_link.py** (0.1.0) | `SAME`（**已文件夹化**，队友 #2）但**未接线**（`main.py` 无 import） | `MISSING-MODULE` | `MISSING-MODULE` | `MISSING-MODULE` |
| **`__init__.py`**（各模块） | `i18n/__init__.py` 已申报 OVERRIDE（`[decl]`，重形态）；其余 `SAME` | 全部 `SAME`（已跟进 1.0.1） | `SAME` | `SAME` |
| **`README.md`**（各模块，1.4.0 起纳入） | `[decl]` ×1（`i18n/README.md`，随重形态模块整包申报）；其余 4 个 `[ok]` | 全部 `[ok]`（已重拷修正后的 paths README） | `update_helper/README.md` `[DIFF]`（本轮重拷后回 `[ok]`）；其余 `[ok]` | 同左 |
| **`icons/` 整夹**（README + `__init__.py`） | `MISSING-MODULE`（整模块未采纳） | `MISSING-FILE` ×2（README + `__init__.py` 未拷） | `MISSING-FILE` ×2 | `MISSING-FILE` ×2 |
| **sync_check.py** (1.5.0) | `N/A` 设计不拷贝：门禁按路径调用模板正本 | `N/A` 同左 | `N/A` 同左 | `N/A` 同左 |

> 矩阵外的 `baseline` / `build_release` 非 `.py` 模板件（README/bat/workflows），不属本文范围，
> 见 REVIEW.md 对应关系矩阵与 CONFORMANCE §B 基线条款。

## 2. 非 SAME 格子逐项展开

字段：**目标态** / **精确位置** / **改动清单** / **风险** / **负责人**。
风险分级：低 = 纯拷贝；中 = 要改调用点/import；高 = 行为变更需人工回归。
`收敛中` 的格子只给"剩余动作"，避免与队友重复劳动。

---

### T1 · appconfig.py（模板 1.0.1）

**目标态**：四工具各持一份，参数按工具填；差异**只允许**存在于本文件（D6/D15）。

- **local-speak2text `PARAM`（已抽件，队友 #3；收尾中）**
  - 现状：`src/modules/appconfig/appconfig.py` 已有 `TEMPLATE-FROM` 头，sync_check 记 `[param]`；
    `APP_ID/APP_NAME/VERSION` 已入此文件（`VERSION = "1.4.1"`），`src/paths.py` 已删除。
  - 剩余动作：① 确认 `src/paths.py` 旧常量无残留、`main.py`/`updater.py` 的 `from paths import VERSION`
    改指 appconfig；② build.bat GATE 1 的 `src/paths.py` 编译项已随文件迁移调整；③ 确认
    `VERSION` 全仓唯一（D15/C-03），`findstr` 目标同步。
  - 风险：**中**（迁移已完成大半，剩单一事实源核验）。负责人：lead 决定；执行 l-s2t owner。
- **reme-helper `PARAM`**
  - 精确位置：`reme-helper/src/modules/appconfig/appconfig.py:1-12`（已申报 OVERRIDE）。
  - 改动清单：无。**不应改**，见 §3.1。风险：低。负责人：lead 决定（维持）。
- **dsh-helper / opencodex-helper `PARAM`**
  - 精确位置：两工具 `src/modules/appconfig/appconfig.py`；`VERSION` 各在 `main.py`（符合 D15）。
  - 改动清单：无。风险：低。负责人：lead 决定（维持）。

---

### T2 · paths.py（模板 1.1.3）

模板 1.1.2 的两个新点：dev 态锚定改"向上找 `main.py` 所在 src 的上一级"（不依赖自身深度）；
数据根整体可被 `<APP_ID 大写>` + `_DATA_DIR` env 重定向（F11）。
**1.1.3 新增**：`CONFIG_PATH` 可被 `<APP_ID 派生>_CONFIG` 钉死（兑现 README 承诺，
CONFORMANCE §4.1.5 的"模板回退"已闭环）——l-s2t 的 `_CONFIG` OVERRIDE 理由随之消失。

- **reme-helper `SAME` 1.1.2（已回基，队友 #2）**
  - 现状：`src/modules/paths/paths.py` 头部 VER 已改 1.1.2、归一化一致；dev `RUN_DIR`=仓库根与
    `REME_HELPER_CONFIG` 以 `TEMPLATE-LOCAL-OVERRIDE` 保留（设计分叉）。
  - 剩余：跑 reme `--smoke` + 8 套件做 R3 回归（路径根行为变更）。风险：**中**。负责人：lead 决定。
- **local-speak2text `SAME` 1.1.3（已跟进）**
  - 现状：已迁 `src/modules/paths/paths.py` 并重拷到 1.1.3；模板补上 `<APP>_CONFIG` 后
    （CONFORMANCE §4.1.5"模板回退"闭环），原 `_CONFIG` OVERRIDE 已撤销。
  - 遗留（不阻断）：env 前缀 `LOCALSPEAK2TEXT_*`（无下划线）与模板派生式 `LOCAL_SPEAK2TEXT_*`
    不同（NAME-10 已知唯一例外）。要么改名对齐（测试/CI 同步改），要么保留一条只针对前缀的 OVERRIDE。
  - 风险：低（文件已一致；前缀是独立小项）。负责人：lead 决定。
- **dsh-helper / opencodex-helper `SAME` 1.1.3（已重拷）**
  - 改动清单：无。注意其 `_DATA_DIR` 键是**f-string 动态拼**（`f"{APP_ID.upper().replace('-','_')}_DATA_DIR"`），
    故 `conformance_check.py` C-16 按字面量 grep 会误报缺失——**这是 C-16 的实现盲区，不是工具缺陷**
    （证据：两文件与正本 1.1.2 归一化一致）。负责人：lead 决定（C-16 修法另议）。

---

### T3 · autostart.py（模板 1.1.1）

**目标态**：四工具都抽件为 `src/modules/autostart/autostart.py`，调用点改为 import。
模板默认 `target="stable"`，但在 `INSTALL_EXE` 不存在时自动退回 `sys.executable`，
故无稳定位的 dsh/ocx 可**零改动正文**采纳（`target="runtime"` 只是省一次存在性判断）。

- **dsh-helper `SAME`（队友 #4 已完成，2026-09-19 快照）**
  - 现状：`src/modules/autostart/autostart.py` 与正本 1.1.1 归一化一致；`main.py:27` 已 import，
    `toggle_autostart` 已改调 `autostart.*`。注意 dsh 原 `_fold_command` 严口径是否随抽件丢失——
    若丢失，属"形状收敛、语义变松"，应反向沉淀回模板或申报（**归 CONFORMANCE，本文只提示**）。
  - **剩余**：`src/modules/autostart/__init__.py` 缺 `# noqa: F401,F403` → 现为 `[NOHDR]`，补一行即 `[ok]`。
  - 风险：低（文件已一致）；语义复核中。负责人：lead 决定。
- **opencodex-helper `MISSING-MODULE`（内联，队友 #4 进行中）**
  - 精确位置：`main.py:833`（`RUN_KEY`）、`:834`（`RUN_NAME`）、`:836`（`autostart_enabled`）、
    `:840`（`set_autostart`）、`:608`（`on_toggle_autostart`）；菜单 `:815`。
  - 改动清单：① 抽件为 `src/modules/autostart/`，删内联段（现用 `reg.exe` 子进程，模板用 `winreg`，
    功能等价但实现不同）；② `RUN_NAME` == `APP_ID` == `APP_NAME`，换名无迁移风险；
    ③ 注意 ocx 现无"启动自愈"（模板 `migrate_autostart`），抽件后获得该能力——顺带收益，需回归。
  - 风险：**中**（改调用点；`reg`→`winreg` 等价性需冒烟）。负责人：lead 决定。
- **local-speak2text `SAME`（已抽件，队友 #3）**
  - 现状：`src/modules/autostart/` 与正本 1.1.1 归一化一致（`autostart.py` + `__init__.py` 均 `[ok]`）；
    旧 `main.py` 内联的 `RUN_KEY`/`get_autostart_cmd`/`is_autostart_enabled`/`migrate_autostart`/
    `set_autostart` 已迁出；并新增回归测试 `tests/test_autostart_migrate.py`（含注册表备份还原）。
  - 改动清单：无。风险：低。负责人：lead 决定。
- **reme-helper `MISSING-MODULE`（内联）**
  - 精确位置：`main.py` 的 `autostart_enabled` / `set_autostart` / `toggle_autostart` /
    `sync_autostart_path`（模板**无**的自愈语义）；`:49-50` 已申报该分叉。
  - 改动清单：① 键名差异：reme 用 `APP_ID`，模板用 `APP_NAME`；reme `APP_NAME="ReMe 助手"`，
    **换名=断链**，必须写一次性迁移或在 OVERRIDE 保留 APP_ID；② `sync_autostart_path` 建议反向
    沉淀进模板（新 VER），而非丢弃；③ `main.py` 菜单调用点改 import。
  - 风险：**高**（注册表键名 + 自愈语义，需人工回归开关自启）。负责人：lead 决定。

---

### T4 · update_helper.py（模板 1.0.1）

**目标态**：dsh/ocx 的旗舰形态——正文零差异，差异全进 appconfig。l-s2t 的稳定位变体与 reme 的
备份/自愈更新链是**真实业务分叉**，不改正文，走 OVERRIDE。

- **reme-helper `MISSING-MODULE`（内联）**
  - 精确位置：`main.py` 的 `HELPER_RELEASES_API`、`check_helper_update`、`startup_helper_update_check`、
    `download_and_apply_helper_update`、`sweep_stale_update_dirs`、`run_helper_update`；
    脚本段含备份目录 + `robocopy "%INSTALL%" "%BACKUP%"` / `robocopy "%STAGE%" "%INSTALL%" /e /purge`。
  - 改动清单：**不建议**强行抽件（模板无"备份目录 + 残留清理 + 匿名 API 60 次/IP 节流"语义，
    见 `main.py` 相关注释）。选项：保持内联 + 在 `:48-50` 申报段补 `update_helper` 的 OVERRIDE 说明；
    或先反向沉淀"备份/清理"进模板 1.1.0 再统一。
  - 风险：**高**（更新链是发版命脉，误改=用户升级失败）。负责人：lead 决定（倾向"不跟，留 OVERRIDE"）。
- **local-speak2text `MISSING-MODULE` + `OVERRIDE`(未申报)**
  - 目标态：保留 `src/updater.py` 稳定位变体（现被 `[MISSING-MODULE]` 抓到：模板有模块、工具无目录、
    文件也无头），**补头申报**后由布局通道接管（届时若落在 `src/modules/update_helper/` 则归 `[decl]`）。
  - 精确位置：`local-speak2text/src/updater.py` 的 `check_update(config_path, force)`、
    `download_update`、`prepare_update_cmd`；消费点 `main.py`。
  - 改动清单：① 头部加 `# TEMPLATE-FROM: my-diy-tool-template/modules/update_helper/update_helper.py |
    TEMPLATE-VER: 1.0.1` + `# TEMPLATE-LOCAL-OVERRIDE: 稳定安装位形态（update.pending.json 延迟换目录，
    与模板 apply.cmd 立即换不同）`；② 或反向沉淀进模板（1.1.0）再统一。
  - 风险：**中**（签名不同：`check_update(config_path,...)` vs 模板 `check_update(current_version,...)`，
    直接对齐要改全部调用点）。负责人：lead 决定。
- **dsh-helper / opencodex-helper `SAME` 1.0.1**：无改动。负责人：lead 决定（维持）。

---

### T5 · i18n.py（模板 2.1.0）

- **reme-helper `OVERRIDE`（重形态，唯一）**
  - 目标态：**保持重形态**（`pairs.json` 中文即键，STANDARDS §E4 明示许可），但补模板头，
    使 sync_check 能把它记成 `[decl]` 而不是"看不见"。
  - 精确位置：`reme-helper/src/modules/i18n/i18n.py`（现为 docstring，**无** `TEMPLATE-FROM`）、
    `pairs.json`；`main.py` 的 `t()` 为唯一出口。
  - 改动清单：仅加两行头：`# TEMPLATE-FROM: my-diy-tool-template/modules/i18n/i18n.py |
    TEMPLATE-VER: 2.1.0` + `# TEMPLATE-LOCAL-OVERRIDE: 重形态（词表 = pairs.json 中文即键，
    §E4 许可；模板轻量双表形态不适用）`。**不改正文**。
  - 风险：**低**（纯加注释行，不触逻辑）。负责人：lead 决定。
- **local-speak2text `SAME` 2.1.0**：无改动（含 `locales/*.json`）。
- **dsh-helper / opencodex-helper `MISSING-MODULE`**
  - 目标态：**待定**——是否启用 i18n 取决于 CONFORMANCE §A2-T1 分级裁决（当前两工具 UI 中文硬编码）。
  - 改动清单：若"触发"→ 拷贝 `modules/i18n/` + 建 `locales/zh.json`+`en.json` + 逐条替换 UI 文案；
    若"不触发"→ 在 CONFORMANCE 记 N/A，本文标 `N/A`。
  - 风险：**高**（全 UI 文案替换 + 需目视回归）。负责人：lead 决定（先裁 T1 是否触发）。

---

### T6 · icons.py（模板 2.0.0）

2.0.0 的关键：**生成流程全在模板**，工具只经 `appconfig` 提供 `ICON_DRAW` 或 `ICON_ASSET`。

- **local-speak2text `SAME` 2.0.0（队友 #3 已完成）**
  - 现状：`src/icons.py` 已带头消费模板；`draw_mic` 图形来源经 appconfig。
  - 复核点：运行态托盘绘制 `main.py` 的 `make_icon_image` 与构建期是否仍同设计语言（模板不要求同构，
    仅需一致）。风险：低。负责人：lead 决定。
- **reme-helper `MISSING-MODULE`（内联）**
  - 精确位置：`main.py` 的 `icon_font`、`make_icon`、`make_taskbar_icon`；运行态着色另有若干处。
  - 改动清单：抽件需把绘制函数搬进 `appconfig.ICON_DRAW`，但 reme 的 `make_icon` 要同时喂
    运行态三色与构建期 ico，与模板"单一静态 `ICON_DRAW(256)`"不同构。
    选项：保持内联 + 在 `:49` 申报段补 icons；或模板扩展支持运行态参数（新 VER）。
  - 风险：**高**（图标外观 + 运行态着色需目视）。负责人：lead 决定（倾向"不跟，留 OVERRIDE"）。
- **dsh-helper `SAME` 2.0.0**：`src/icons.py` 已申报 `ICON_ASSET` 指
  `resources/img/dsh-helper-icon.png`。**不应改**，见 §3.4。
- **opencodex-helper `SAME` 2.0.0**：`appconfig._draw_icon` 自绘；无改动。

---

### T7 · tray_kit.py（模板 2.0.2）

2.0.1 相对 1.0.1 是**大版本**：2.0.0 加入 `confirm_quit_dialog`、`MenuSignature`、`quit_watch_loop`、
`mask_token`。落后工具会缺"菜单签名重画"（右键菜单开着失焦，CONFORMANCE C-12）。
**2.0.2**：`confirm_quit_dialog` / `warn_duplicate_instance` 的用户可见文案改为**可传参、中文为默认**
（`title/body_text/confirm_text/cancel_text/message`），满足 E4-02；`checkbox_text` 为空/None 时
不再渲染空勾选框。**向后兼容**：老调用点不传参照旧。

- **reme-helper `LAG(1.0.1→2.0.1)+OVERRIDE`**
  - 精确位置：`reme-helper/src/modules/tray_kit/tray_kit.py:1-4`（VER 1.0.1 + OVERRIDE：互斥体名
    由调用方显式传入）；消费点 `main.py` import 行。
  - 改动清单：① 靠到 2.0.1 正文；② 复核"互斥体名显式传入"分叉——模板
    `acquire_single_instance(app_id, mutex_name=None,...)` 已支持该参数，OVERRIDE 可能**可以撤销**，
    先验证再决定；③ 新增的 `confirm_quit_dialog` / `MenuSignature` 是否落地归 CONFORMANCE（E2-09/C-12），
    本文只管文件对齐。
  - 风险：**高**（退出确认框/菜单重画是交互，需目视回归）。负责人：lead 决定。
- **local-speak2text `MISSING-MODULE`（内联）**
  - 精确位置：`main.py` 的 `MUTEX_NAME`、`acquire_single_instance`（含 `--smoke` 绕过守卫的历史
    教训注释）；退出路径与菜单散在托盘构建段。
  - 改动清单：抽件为 `src/modules/tray_kit/tray_kit.py`，删内联守卫段；引入 `MenuSignature`
    替换全量重建；`make_quit_request_path` 接 `--quit`。**注意** l-s2t 的 `MUTEX_NAME` 已经是合法命名
    （单反斜杠），迁移不得回退（曾经的单实例血案）。
  - 风险：**高**（菜单重画 + 退出守卫，C-12 需 GUI 目视）。负责人：lead 决定。
- **dsh-helper / opencodex-helper `SAME` 2.0.2（已重拷，红灯自消）**
  - 现状：模板升到 2.0.2 时曾报红灯（预期级联），同步波次已重拷 `tray_kit.py` + `tray_kit/__init__.py`。
  - 后续可选：退出确认框若启用 i18n，把文案接到 `t()`（不接则中文默认值照旧可用）。
  - 风险：无（已一致）。负责人：lead 决定。
- **local-speak2text `SAME` 2.0.2（已跟进，队友 #3）**：文件已一致。后续可选：把退出确认框
  文案接到 `t()`（E4-02），不接则中文默认值照旧可用。风险：低。负责人：lead 决定。

---

### T12 · log_kit.py（模板 1.0.2）

- **local-speak2text `SAME` 1.0.2（队友 #3 已完成）**
  - 现状：`src/modules/log_kit/log_kit.py` 与正本 1.0.2 归一化一致；旧散文件 `src/log_kit.py` 已退役。
  - 改动清单：无。风险：低。
- **reme-helper `SAME` 1.0.2（已回基，队友 #2）**
  - 现状：`reme-helper/src/modules/log_kit/log_kit.py` 与正本归一化一致（原 root-logger 分叉
    已并入正文或撤销 OVERRIDE）；`log_kit/__init__.py` 亦 `[ok]`。改动清单：无。
- **dsh-helper / opencodex-helper `SAME` 1.0.2**：无改动。

---

### 横切件 · `__init__.py` / `README.md`（模板 1.3.0 / 1.4.0 起先后纳入比对）

**模板侧已统一**（本轮变更）：每个 `modules/<模块>/__init__.py` = 两行
`# TEMPLATE-MODULE: <模块> | TEMPLATE-VER: <版本>` + `from .<模块> import *  # noqa: F401,F403`
（CRLF、纯 ASCII；与 dsh/ocx 多数派一致，仅加注释不动导入语义）；`modules/icons/` 补了 `__init__.py`。
归一化哈希剔除 `# TEMPLATE-*` 行，故**多数派的单行 noqa 形态直接 `[ok]`**，无需改工具文件。

- `dsh-helper`：**全部 `[ok]`**（队友 #4 已给 autostart `__init__.py` 补 noqa）。
- `opencodex-helper`：**全部 `[ok]`**（队友 #4 直接带头拷贝模板形态）。
- `local-speak2text`：**全部 `[ok]`**（队友 #3 已给 log_kit/paths 的 `__init__.py` 补头 + noqa）。
- `reme-helper`：appconfig/paths/log_kit `[ok]`；`i18n/__init__.py`、`tray_kit/__init__.py`
  是**具名导出**（模板为 `import *`）→ `[NOHDR]`。若具名导出确有必要，建议反向沉淀成模板的
  "具名导出"变体或加 `TEMPLATE-LOCAL-OVERRIDE` 申报；否则回基多数派形态。
- 风险：**低**（纯注释/导出形态，不改运行时行为——`import *` 与具名导出对调用方均可得名）。
  负责人：lead 决定；reme owner 执行。

---

### T-service_link · service_link.py（模板 0.1.0）

- **reme-helper `SAME` 但散文件 + 未接线（典型"SAME ≠ 在役"）**
  - 精确位置：`reme-helper/src/modules/service_link.py`（散文件，正确布局应为
    `src/modules/service_link/service_link.py` + `__init__.py`）；`main.py` 全文**无** `import service_link`、
    无 `ServiceLink` / `can_start` / `spectators` 引用（仅有一处注释提到它）。
  - 改动清单：① 低风险部分——文件夹化（移文件 + 加 `__init__.py`），sync_check 仍 `[ok]`；
    ② 高风险部分——是否把 reme 的进程管理接到 `ServiceLink` 状态机，属 CONFORMANCE
    §G4.2 能力落地，**不在本文范围**，需 lead 单独排期。
  - 风险：① 低 / ② 高。负责人：lead 决定。
- **local-speak2text / dsh-helper / opencodex-helper `MISSING`**
  - 目标态：dsh 有"dsh 服务托管"业务（现内联在 `main.py` 的 start/stop 菜单），
    opencodex 曾因退出签名击杀被 §G4.2 列为反例；l-s2t 无服务托管业务。
  - 改动清单：**待 lead 裁定**各工具是否接 `ServiceLink`；若接，属新能力开发，另立任务。
  - 风险：**高**（进程生命周期）。负责人：lead 决定。

## 3. "不应对齐"清单（**必须逐条给依据**，2026-09-19 用户裁定后重判）

> **允许不一致的前提只有两条**（STANDARDS B4 / CONFORMANCE §4.4）：
> ① **业务冲突**（前提是**双方都有该功能**；"没有功能"是缺失、必须补齐）；
> ② **有更好的方案**（须给**可验证的**更优理由）。
> 两条的共同义务：**事后必须评估"能否优化模板以吸收该差异"**。
> `TEMPLATE-LOCAL-OVERRIDE` 是**留痕**、**不是豁免理由**；**排期（波次）不是许可**。
> **没有依据的条目必须移出本清单**——清单外的差异一律记"未获允许的缺口"。

| 条目 | 判定 | 依据 |
|---|---|---|
| `appconfig.py` 参数文件 | 保留 | **设计上的一致形态**（模板机制本身允许：T1 就为每工具一份参数而设，D6/D15）——**不是**"允许不一致" |
| reme 重形态 `i18n` | 保留（前提 ②） | 双方**都有** i18n 功能 → 属**方案差异**；reme 需 `pairs.json`（中文即键）+ 整句最长片段替换（百条级）。**吸收评估：暂不吸收**（模板内并存两套查表引擎，成本>收益）；义务保留 |
| ~~dsh `ICON_ASSET`~~ | **移出清单** | 模板 `icons` 2.0.0 **已原生支持** `ICON_ASSET` → **差异已被模板吸收**，不存在"不对齐" |
| ~~l-s2t `updater` 稳定位变体~~ | **移出清单，改记"未采纳缺口"** | 实测**不构成业务冲突**：同为 `INSTALL_DIR` 目标的"查→下→校验→换"三段式（含 sha256），差异仅签名与 repo 来源（后者**模板可吸收**）→ 按原则③应收敛，当前记 `[MISSING-MODULE]` |

### 3.1 appconfig.py —— 参数文件（**设计豁免**，非"业务冲突"）
`appconfig.py` 是 D6/D15 唯一的"可改文件"，四份取值本就不同。`sync_check` 对 `appconfig.py`
命中 `[param]`（先于 `[decl]` 判定），**无需**写 OVERRIDE。依据是**模板机制本身允许**
（T1 即为"每工具一份参数"而设计），**不是**"业务冲突/更好方案"这两条前提。
唯一要求：差异**只**是参数，不得塞逻辑（reme 的 `ICON_DRAW 不启用` 已用 OVERRIDE 说明，属边界情况）。
l-s2t 新增的 appconfig 需补 `TEMPLATE-FROM` 头才能进 `[param]` 统计。

### 3.2 reme-helper i18n —— 重形态（**前提 ②：更好的方案**，附吸收评估）
- 判定依据：**双方都有 i18n 功能**，故**不是**"业务冲突"；属**方案差异**，走前提 ②。
- 分叉性质：词表 = `pairs.json`（中文即键）+ 整句最长片段替换；模板为轻量 `zh/en` 双表。
  量级差异是硬事实（reme 百条级文案），STANDARDS §E4 亦明示许可两种形态。
- **模板能否吸收（必答项）**：**暂不吸收**——吸收需在模板内并存两套查表引擎（键查 + 片段替换），
  复杂度与维护成本大于收益；**义务保留**：reme owner 持续提供可验证的更优理由，模板侧持续评估。
- 所需 OVERRIDE 文案（加到 `src/modules/i18n/i18n.py` 头部）：
  ```
  # TEMPLATE-LOCAL-OVERRIDE: 重形态（词表 = pairs.json 中文即键 + 整句最长片段替换，
  #   STANDARDS §E4 许可）；属方案差异（前提②），模板吸收评估=暂不吸收，义务保留
  ```

### 3.3 ~~local-speak2text updater —— 稳定位变体~~ → **已移出：这是未采纳的缺口**
- 实测证据（`local-speak2text/src/updater.py`）：目标同为 **`INSTALL_DIR`**（稳定安装位），
  流程同为"查 GitHub Releases → 下载 zip + sha256 校验 → 暂存 → 退出后整目录替换"，
  **与模板 `update_helper` 不构成业务冲突**。
- 真实差异只有两点：① 签名 `check_update(config_path, force)` vs `check_update(current_version, force)`；
  ② repo 来源 = 运行时 `config.update_repo` vs appconfig 固定 `REPO_OWNER/REPO_NAME`。
  其中 ② **是模板可吸收的一条**（让 `REPO` 可被 config 覆盖）→ 按原则③应**收敛**。
- 当前状态：`sync_check` 记 `[MISSING-MODULE]`（黄灯缺口），**不是**"不应对齐"。
- 若 l-s2t owner 仍主张"更好方案"，须给出**可验证**理由（如"运行时换源是交付需求"），否则应采纳模板件。

### 3.4 ~~dsh-helper ICON_ASSET~~ → **已移出：差异已被模板吸收**
- 事实：模板 `icons` 2.0.0 **已原生支持** `ICON_ASSET`（`appconfig.ICON_ASSET` → `base_image()`
  统一缩放 256 基图），dsh 只是把参数指向手工 png——**这正是模板设计的两种图形来源之一**。
- 结论：不存在"不对齐"，**移出清单**；`dsh/src/icons.py` 与模板 `[ok]`，`ICON_ASSET` 属 `appconfig` 参数。

### 3.5 reme-helper paths / tray_kit 现有 OVERRIDE（**逐条给依据**）
- `log_kit.py`：已回基为 `SAME` 1.0.2，**不再有 OVERRIDE**（§T12）——差异已消灭。
- `paths.py`（dev `RUN_DIR`=仓库根）：已回基 1.1.3。**判定**：前提 ②（更好方案）**待举证**——
  reme 的诊断输出/图标需跟随"这次跑的那个包"，故 dev 态 `RUN_DIR` 与 `APP_DIR` 分离；
  owner 须给出可验证理由，并回答"模板能否吸收（如把 dev `RUN_DIR` 变成可配置项）"。
- `tray_kit.py`（互斥体名显式传入）：2.0.2 正文已内置 `mutex_name` 参数 → **差异已被模板吸收**，
  **应撤销 OVERRIDE 直接对齐**（收敛收益）；当前因 VER 落后报 `[lag]`。

## 4. 执行顺序建议（低风险先做，力求一次编译通过）

排序原则：① 只加注释/头、不动逻辑的排最前；② 纯搬文件 + 改 import 次之；
③ 牵动 VERSION/路径根的合并批次；④ 交互/更新链/服务生命周期最后，必须人工回归。

| 序 | 动作 | 涉及文件 | 风险 | 状态（快照时） |
|---|---|---|---|---|
| **0a** | **dsh/ocx 重拷 `paths` 1.1.3 + `tray_kit` 2.0.2（消 4 条红灯）** | 4 个 .py（+2 个 `__init__.py`） | 低 | **完成**（同步波次已重拷，红灯自消） |
| **0b** | dsh/l-s2t/ocx 补 `src/modules/icons/__init__.py` | 3 个文件 | 低 | 待做（`[MISSING-FILE]`） |
| **0c** | l-s2t/reme 跟进 paths 1.1.3 / tray_kit 2.0.2 / appconfig `__init__` 1.0.1（消黄灯） | 蓝本各 2-3 文件 | 低 | **基本完成**（仅剩 l-s2t `appconfig/__init__` 1 条 lag） |
| 1 | reme i18n 补 OVERRIDE 头；l-s2t updater 补 OVERRIDE 头 | 2 个文件的头部注释 | 低 | 待做 |
| 1a | 各工具 `src/modules/*/__init__.py` 形态回基（模板已统一） | 见 0b/0c | 低 | 部分完成 |
| 2 | reme `service_link.py` 文件夹化（+`__init__.py`） | 1 移 + 1 新 | 低 | **完成**（队友 #2） |
| 3 | l-s2t `log_kit` 1.0.0→1.0.2 + 迁 modules 布局 | `src/modules/log_kit/` | 中 | **完成**（队友 #3） |
| 4 | dsh `autostart` 抽件 | `src/modules/autostart/` | 中 | **完成**（队友 #4） |
| 5 | ocx `autostart` 抽件（`reg`→`winreg`） | `main.py` 自启段 | 中 | **完成**（队友 #4） |
| 6 | l-s2t `autostart` 抽件（蓝本搬家） | `main.py` 自启段 | 中 | **完成**（队友 #3，含回归测试） |
| 7 | reme `paths` 回基（1.1.1→1.1.3）+ 重写 OVERRIDE | `modules/paths/paths.py` | 中 | **完成**（队友 #2） |
| 8 | ~~模板是否回填 `<APP>_CONFIG`~~ → **已回填（1.1.3）** | 模板正本 + 3 副本 | — | **完成**（本轮） |
| 9 | l-s2t `appconfig`+`paths` 合并收尾（VERSION 单一事实源核验） | appconfig / main / updater / build | 中 | 进行中（队友 #3） |
| 10 | ~~reme `tray_kit` 靠 2.0.1~~ → **已跟 2.0.2** | `modules/tray_kit/tray_kit.py` | 中 | **完成**（队友 #2） |
| 11 | l-s2t `tray_kit` 2.0.2 抽件跟进（签名重画/退出框 + i18n 文案） | `main.py` 托盘段 | 高 | 待做，GUI 目视 |
| 12 | reme `autostart` / `icons` / `update_helper`：**倾向不跟**，反向沉淀或留 OVERRIDE | `main.py` 三大段 | 高 | 待 lead 决策 |
| 13 | dsh/ocx `i18n`：先裁 T1 是否触发 | — | 高 | 待 lead 决策 |
| 14 | `ServiceLink` 是否接线（reme/dsh/ocx） | 各 `main.py` | 高 | 待 lead 决策，另立任务 |

**一次编译通过的批次建议**：#1+#1a+#2 都是注释/文件级操作，可合成一个"黄灯清零"commit（不动逻辑）；
#3–#6 是"抽件/搬家 + 改 import"批；#8 是模板变更，须先于任何副本同步；#10–#14 逐个单独 commit + 人工回归。

## 5. 与 sync_check 1.4.0 的配合

1.3.0 做三件事（对应 CONFORMANCE §4.1.9 三类盲区）：蓝本逐文件比对、布局通道（无头也扫）、
整模块缺失检测；1.4.0 把扫描范围从 `*.py` 扩到 `.py + .md`，模块 README 不再隐身
（对应 CONFORMANCE §4.1.10 第 4 盲区）。

- 蓝本副本内容/VER 落后 → `[lag]`（黄灯，**不阻断**），打印 `副本VER -> 模板VER`；
- 蓝本副本 VER 相同却仍内容不同 → 未申报分叉，仍 `[DRIFT]` 红灯；
- `src/modules/<模块>/` 下无头且不一致 → `[NOHDR]`（黄灯，提示补头）；
- 模板有模块、工具无目录无申报 → `[MISSING-MODULE]`（黄灯）；
- 模块已采纳但缺其中某件 → `[MISSING-FILE]`（黄灯，本轮新增，复核员实测漏检）；
- 默认只扫**家族工具**（有 `src/` 且有门禁 `build.bat`），避免把同目录无关项目刷成缺失。

**R1 基线（1.4.0 扫描扩展后）**：`0 undeclared drift`、`0 blueprint lag`、
`9 nohdr`（5 个 reme 模块 README + dsh/ocx 的 appconfig README + reme i18n×2）、
`9 missing-module`、`6 missing-file`（dsh/l-s2t/ocx 各缺 `icons/README.md` + `icons/__init__.py`）。
此前 l-s2t `log_kit 1.0.0→1.0.2`、reme `paths 1.1.1→1.1.2`、四工具 `autostart` 缺失、
`__init__.py` 形态不一、`service_link` 散文件、模板 `_CONFIG` 回退、模块 README 隐身
均被同一机制暴露并已收敛——**这正是逐轮补盲区的收益证明**。

**自证（本轮新增）**：临时目录造样本，验证 `__init__.py` 带 `TEMPLATE-MODULE` 头时判 `[ok]`
（不再假红灯）、无头正文走布局通道判 `[ok]`、缺件判 `[MISSING-FILE]`，退出码 0——见 task#5 命令。
此后模板每次升位，蓝本必须回答"跟 / 不跟"并留痕。

## 6. 已知盲区（本文自曝，避免"表绿=万事大吉"）

1. **模板头仍是"版本/申报"的载体**：布局通道能发现"不一致"，但只有补了头才能在
   `[decl]`/`[VER 落后]` 层面被追踪。因此本表所有 `NOHDR`/`MISSING-MODULE` 的首选动作都是补头（序 #1/#1a）。
2. **不在 `src/modules/<模块>/` 且无头的文件仍不可见**：如 l-s2t 的 `src/updater.py`、
   `src/pipeline.py`。前者被 `[MISSING-MODULE]` 间接抓到（因为模板有 update_helper 模块），
   纯工具私有文件（pipeline 等）**本就不该纳入比对**，属正常。
3. **散文件不改状态**：reme `service_link.py` 与正本哈希一致故 `[ok]`，但**未接线**
   （`main.py` 无 import）——`SAME ≠ 在役`（布局已由队友 #2 文件夹化）。
3b. **`__init__.py` 的 VER 会跟着模块 VER 走**：本轮 appconfig 1.0.1 / paths 1.1.3 /
   tray_kit 2.0.2 升位时，对应 `__init__.py` 必须同步升 VER，否则带头的副本会被判 VER 落后。
   这是"模板内部一致性"问题，已在模板侧修正；各工具带头副本需按 §0.2 重拷。
4. **`conformance_check.py` C-16 的字面量 grep** 对 f-string 动态 env 键失效，
   会把已实现 `_DATA_DIR` 的 dsh/ocx 误报为缺失（证据：两副本与正本 1.1.2 归一化一致）。
   修法另议，**不属本文改动范围**。
5. **本文只判形状，不判能力**：例如 dsh autostart 抽件后 `_fold_command` 严口径若丢失，
   文件仍 `[ok]` 但语义变松——那要查 CONFORMANCE §G4.1。
6. **行号会漂移**：队友并发改工具时 `文件:行号` 证据会失效，定位以函数名为准。
7. **第 4 盲区：模块 README 曾长期隐身（1.4.0 已补，CONFORMANCE §4.1.10）**。
   此前 `sync_check` 用 `rglob("*.py")` 扫描，模块文件夹里的 `README.md` **从未进入比对**——
   于是"代码一致"被误当成"整文件夹一致"，而模块文档可以无限漂移。实测（lead 独立全量哈希）：
   `modules/appconfig/README.md` 在 dsh/ocx 双 DIFF、reme 有 5 个模块 README DIFF。
   **`.py` 有哈希闸、`.md` 没有**，是最容易被漏掉的一类漂移。1.4.0 起扫描范围含 `.py + .md`，
   模板专属目录与 `__pycache__` 排除；这解释了为何本表新增 `README.md` 行与 `icons/` 整夹行。
   实测快照（lead 独立比对，1.4.0 上线前）：

   | 模板文件 | reme | l-s2t | dsh | ocx |
   |---|---|---|---|---|
   | `modules/appconfig/README.md` | DIFF | SAME | DIFF | DIFF |
   | `modules/log_kit/README.md` | DIFF | SAME | SAME | SAME |
   | `modules/paths/README.md` | DIFF | SAME | SAME | SAME |
   | `modules/tray_kit/README.md` | DIFF | SAME | SAME | SAME |
   | `modules/i18n/README.md` | DIFF | SAME | — | — |

   汇总：**l-s2t 0 DIFF（17 SAME）**；dsh/ocx 各 1 DIFF（appconfig README）；reme 7 DIFF
   （5 个 README + i18n×2 未申报）。1.4.0 上线后 `sync_check` 的输出与上表逐格吻合。
8. **README 不带头是硬口径（§4.1.10a），差异记 `[DIFF]` 而非 `[NOHDR]`**：模块 README
   与正本逐字节一致、不带任何 TEMPLATE 头。**不能给 `.md` 补头**——markdown 标题也以 `#`
   开头，归一化的剔行逻辑会把 `# TEMPLATE-FROM:` 当元信息静默剔除，于是"带头副本"与
   "不带头副本"比对结果都是 `[ok]`，而字节并不相同（合成样本可复现）。故 `.md`
   一律走逐字节哈希：`[ok]` / `[DIFF]` / `[decl]`（模块级 OVERRIDE 时）。
   提示语本身也要对：`[NOHDR]` 的"补头"建议**只对 `.py` 成立**，绝不能出现在 `.md` 上
   ——否则会把人教去给 README 加头，而那条路恰好是被禁止的。

## 7. 模块来源清单 vs reme-helper（仲裁规则落地，2026-09-19）

用户仲裁规则（STANDARDS §B4）：**公共模块版本冲突时，以 reme-helper 的已验证实现为准，
不看"哪个版本用的人多"**。本节是它的执行结果——先回答"reme 到底有没有做过"，再回答
"是否更可靠"，最后给裁定。**"reme 有"不等于"模板必须换成 reme 的形状"**：前提②（可验证的
更优方案）仍然有效；但举证责任在偏离方。

| 模板模块 (VER) | reme 是否有对应实现 | 形态 | 模板来源 | 裁定与依据 |
|---|---|---|---|---|
| `paths` (1.1.3) | **有**，`src/modules/paths/`，与正本同 VER | 模板件（reme 已拷贝） | reme 运行验证（数据区重定向/稳定位） | **一致**，无需裁定 |
| `log_kit` (1.0.2) | **有**，`src/modules/log_kit/` | 模板件 | reme 抽件来源 | **一致**（只确认，不重构） |
| `tray_kit` (2.0.2) | **有**，`src/modules/tray_kit/` | 模板件 | reme 抽件来源（reme 托盘长期在役） | **一致**（只确认，不重构） |
| `service_link` (0.1.0) | **有**，`src/modules/service_link/` | 模板件 | reme 抽件来源 | **一致**；但 reme **未接线**（`main.py` 无 import）→ `SAME ≠ 在役`，属另一类缺口 |
| `appconfig` (1.0.1) | **有**，`src/modules/appconfig/appconfig.py` | 参数文件 | 双方 | **设计豁免**（§3.1），非冲突 |
| `i18n` (2.1.1) | **有**，但是**重形态**（中文即键 + `pairs.json` 片段替换） | reme 自研重形态 | 模板为轻量 T5；reme 已申报 OVERRIDE | 差异获准（前提②，STANDARDS §E4 明示）。**但**"包门面不得复制可变全局"这条**是 reme 的正确形态**，模板 2.1.1 已吸收（i18n 的 LANG 曾是静态副本） |
| `autostart` (1.1.1) | **有，内联**（`main.py:3501-3570`：`autostart_enabled` / `set_autostart` / `toggle_autostart` / `sync_autostart_path`） | reme 内联 + 自报留痕 | 蓝本 local-speak2text（稳定安装位） | **保留模板形态**（前提②）：模板指向稳定安装位 + `migrate_autostart` 自愈，比 reme 的 `sys.executable` 形态更能扛"版本目录被换掉"；reme 自己的 `sync_autostart_path` 正是为这个坑打的补丁。**理由可验证**，故属获准差异 |
| `icons` (2.0.0) | **有，内联**（`make_icon` / `make_taskbar_icon` / `icon_font`，含运行态着色） | reme 内联 | 模板 2.0.0 为抽件形态 | **未裁定 / 记缺口**：抽件形态与 reme 内联不同构，尚未做"是否更优"的举证。列入待评估（不阻塞本轮） |
| `update_helper` (1.3.0) | **有，内联且已验证**（`main.py` 7098-7345） | reme 内联 | 模板 1.0.x 是**合成件** | **按 reme 重写**（接口不变），见 §7.1 |
| `baseline` / `build_release` | 无（模板专属） | — | 模板 | 不适用 |

> 读法：`MISSING-MODULE`（reme 无目录）**不等于 reme 没做过**——reme 有三件是**内联**在
> `main.py` 里的（`autostart` / `update_helper` / `icons`，reme 自己在 `main.py:61-63` 申报留痕）。
> 仲裁规则要求逐件去看**内联实现**，而不是看到"没有目录"就判"reme 没做过"。

### 7.1 `update_helper` 专项审计（1.0.1 → 1.2.0 → 1.3.0）

**审计对象**：模板 `modules/update_helper/`（1.0.1）vs reme `src/main.py` 的更新链。

**结论（先给）**：**rewrite，按 reme 语义重写，接口保持**——不是补丁式修补。理由：

1. 模板 1.0.x 是**合成件**：没有一次端到端跑通的记录，而 reme 的链路**发过版、跑过真实替换**。
   两处静默失效（`PENDING_CMD` 被 `import *` 复制、`UPDATE_READY` 从不赋值）就出在这个合成件上；
2. 缺的不是一行两行，而是**整条失败路径**（回退/可见性）。补丁式修补会把"失败时无路可退"
   这种结构缺陷留成补丁堆；
3. 重写**不需要改接口**：`check_update(current_version, force=False)` /
   `download_and_prepare(latest, target_dir, update_dir, log=…)` 签名与语义保持，
   dsh/ocx 调用点零改动（实测其调用为 `check_update(VERSION, force=True)`、`update_ready()`、
   `pending_cmd()`、`download_and_prepare(latest, APP_DIR, UPDATE_DIR, log=log)`）。

**反方论据（"模板已被 dsh/ocx 采纳，动它代价大"）为什么不成立**：那是"多数派"思维——
采纳面是**错误的传播范围**，不是正确性证据（STANDARDS §B4 仲裁规则第 1 条）。
dsh/ocx 之所以采纳 1.0.x，是因为模板当时只有 1.0.x。

#### 7.1.1 reme 语义要点 → 模板落地状态

| reme 语义要点（`main.py`） | 1.0.1 | 1.2.0 | 1.3.0 |
|---|---|---|---|
| `tasklist` 写文件 + `find` 读文件（**不用管道**：DETACHED 下 `tasklist \| find` 永不返回，实测 0.13s vs 挂起） | ✗ | ✓ | ✓ |
| 等旧进程退出**有上限**（120 ≈ 1 次/秒）→ `:giveup` 记日志 | ✗ | ✓ | ✓ |
| 备份目录在**目标目录之外**（否则 `/purge` 会连备份一起删，且 `robocopy target target\_backup /e` 会扫到自己） | ✗ | ✓ | ✓ |
| `robocopy /e /purge` 清上一版残留 + 全流程写 `update.log` | ✗ | ✓ | ✓ |
| 收尾删暂存（实测每次 ~50MB）+ 脚本自删 | ✗ | ✓ | ✓ |
| `sweep_stale_update_dirs()`：只清**一小时前**的 %TEMP% 暂存（保护进行中的更新） | ✗ | ✓ | ✓ |
| `http_error_hint()`：403/429 = GitHub 匿名配额，翻成人话 | ✗ | ✓ | ✓ |
| **替换前先快照，且只在替换成功后才轮转为 BACKUP**（旧备份是回退源，不得提前删） | ✗ | ✗ | ✓ |
| **检查 robocopy rc（>=8 失败）→ 绝不启动新 exe，从快照回铺并启动旧版** | ✗ | ✗ | ✓ |
| **回铺也失败 → 不启动任何 exe，保留快照供人工恢复** | ✗ | ✗ | ✓ |
| **失败 marker（`update.failed`）+ 下次启动读一次并通知**（托盘已退出，只能下次说） | ✗ | ✗ | ✓ |
| **sha256 缺失也算失败**（fail-closed，绝不静默放行） | ✗ | ✗（"没 sha 就跳过"=静默放行） | ✓ |
| 检查与"下载并安装"的**状态与自身版本状态分离**（两个 `UPDATE_STATE` 互相覆盖的教训） | — | ✓（`_STATE` 只服务查） | ✓ |

#### 7.1.2 剩余差异（**明记，不作"已对齐"**）

1. **资产定位方式**：reme 从 Releases API 的 `assets[]` 里按后缀找 zip / `.sha256`；
   模板按命名约定拼 URL（`<APP_ID>-<版本>-windows-x64.zip`）。约定写法**更简单但更脆**——
   资产改名即 404。约定已写进 README「打包约定」，四工具 release.yml 均遵守。
2. **zip 内层结构**：模板期望一层 `<APP_ID>-<版本>/`（release.yml 约定），reme 直接解到
   `work/stage`。属打包约定差异，不构成语义分歧。
3. **接口形状**：reme 是 `tuple(bool, str)` + 状态字典；模板是 `dict(latest/current/newer/error)`
   + 访问器。工具已依赖模板形状，**保持**。
4. **"启动时 sweep + 读失败 marker"是采纳方义务**：模板只提供函数，工具需在启动流程调用
   （README 采纳步骤已写）。未接线 = 失败可见性白做——已写入 §0.3 级联清单。
5. **模板内还有第二条更新路径**：`modules/paths/paths.py: process_pending_update()`
   （`UPDATE_PENDING = RUN_DIR / "update.pending.json"`，`robocopy /MIR`）。
   它**无 rc 检查、无回退、/MIR 会删目标多余文件**，与 `update_helper` 的 bat 是两套机制。
   reme 无对应物 → 按仲裁规则**不是基准**；是否收敛（并入 update_helper 或删除）**待裁定**，
   本轮不动（改动面大且 l-s2t 可能在用）。
