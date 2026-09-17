# _template：拷贝式公共模板库（my_diy_tools）

工具无关的基础设施模板。**拷贝式，不是共享包**（决策 D1，2026-09-17 确认）：
新工具直接把需要的文件拷过去、只改 `appconfig.py`，即可获得与 reme-helper 同级的
基线能力；模板修了 bug，由 `sync_check.py` 点名各工具同步。

## 模板清单（T 编号见执行文档 §四 Wave 1）

| 文件 | 能力 | 蓝本 |
|---|---|---|
| `appconfig.py` (T1) | 参数区：拷贝后唯一要改的文件 | — |
| `paths.py` (T2) | 数据区/播种/稳定安装位/**数据根 env 重定向**（F11） | local-speak2text |
| `autostart.py` (T3) | 自启三件套：优先稳定位 / 设置 / 启动自愈 | local-speak2text |
| `update_helper.py` (T4) | 在线更新：查→下（sha256）→换（退出后 robocopy + 重启） | dsh/opencodex + local-speak2text |
| `i18n.py` (T5) | 轻量中英双表（重 i18n 见 reme-helper，二期） | local-speak2text |
| `icons.py` (T6) | 代码生成双 ico（不进二进制资源） | local-speak2text |
| `tray_kit.py` (T7) | 单实例 / --quit 请求文件+监视循环 / token 掩码 / 菜单签名重画 | reme-helper + local-speak2text |
| `build.bat` (T8) | 门禁构建骨架：编译检查 → 测试 → PyInstaller → 冒烟 | local-speak2text + dsh |
| `release.bat` (T9) | 打 tag 触发发版（版本读自 appconfig/paths，单一事实源） | local-speak2text |
| `workflows/` (T9) | tests.yml（push 全分支）+ release.yml（tag v* 发版） | local-speak2text |
| `sync_check.py` (T10) | 模板漂移检查（四件套之二） | — |
| `log_kit.py` (T12) | 滚动日志 1MB×3 + 打开日志目录 | reme-helper |

二期件（触发才抽，D3）：设置窗口、主题、harness 测试缝、重 i18n、guide——蓝本 reme-helper。

## 新工具接入步骤

1. 拷所需模板件到工具目录（`appconfig.py` 必拷）；
2. 改 `appconfig.py` 六个键 + `ICON_DRAW`；
3. 每个拷贝文件**保留头两行 TEMPLATE 标记**；
4. 有意定制时在文件头加一行 `# TEMPLATE-LOCAL-OVERRIDE: <原因>`；
5. build.bat 门禁加一步 `python ..\_template\sync_check.py --roots <工具名>`（有模板件的工具）；
6. README/CHANGELOG 按工具实际能力写，双语按发布面判断。

## 同步纪律（D8）

模板修复 → `TEMPLATE-VER` 升位（patch 起步）→ 各工具跑 sync_check 红灯点名 →
逐工具**独立 commit + 门禁绿 + semver 判级（一般 patch，先报后动）**，才算同步完成。
push 与发版是用户决定权。

## 实例隔离纪律（F11/D12，硬性）

测试、构建脚本、CI 里跑的实例**必须**用独立数据区（`paths.py` 的
`<APP_ID>_DATA_DIR` 环境变量整体重定向），严禁与用户常驻实例共享
config / log / quit.request 等任何落盘文件——否则工具链的一次清理会杀掉用户的托盘。
