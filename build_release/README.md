# build_release —— 门禁构建 + tag 发版链

> 蓝本：local-speak2text 的 build.bat/release.bat/workflows（reme-helper 的 ASCII 教训已吸收）。

## 定位

两件事，各一份骨架：

1. **build.bat**：门禁顺序 = 编译检查 → 单元测试（有则跑）→ PyInstaller
   onedir/noconsole → 冻结冒烟。**便宜在前、昂贵在后**，每步失败判定 + 非零退出，
   禁止人眼判断成功。
2. **release.bat + workflows**：`release.bat` 打 `v<semver>` tag 并推送 →
   `release.yml` 在 CI 干净检出上构建、出 zip+sha256、发布 GitHub Release；
   `tests.yml` 对所有分支的 push/PR 跑编译与测试。手动 `workflow_dispatch` 只出
   工件不发布。

## 版本解析（阶段 0.1，**两步式**，改这里之前先看）

```bat
for /f "tokens=2 delims==" %%a in ('findstr /b /c:"VERSION = " <源文件>') do set VERSION=%%a
if defined VERSION for /f "tokens=1" %%a in ("%VERSION:"=%") do set VERSION=%%a
```

- **禁用 `"tokens=2,*"`**：它把**行尾剩余全部**交给变量，于是
  `VERSION = "1.4.0"  # 发版时才改` 会把注释一起吞进版本号（再经 cmd 代码页变乱码），
  令 `RELEASE_DIR` 变垃圾路径、构建坏掉。两步式：先按 `=` 切，再去引号取首个空白分隔 token。
- **端到端回归**：`python verify_build_bat.py`（模板专属，不派发）。它把本目录 `build.bat`
  按文档填好占位符、放进临时工具骨架，用 cmd.exe **真实执行整个脚本**，四个样本断言：
  两步式 + 行尾注释 → `1.4.0`；预置 `release\<APP>-1.4.0` → 按**这个解析出来的名字**拒绝；
  换回旧写法 → 版本号里带上注释、且预置目录认不出（反向，防断言空转）。
  为什么不做片段级测试：cmd 行为依赖上下文（setlocal/变量/代码页），抠两行单独跑通
  **不能**证明它在脚本里也对。

## 命名规则与版本元数据（2026-10-26，用户定）

**安装目录、exe 文件名、发布 zip 的内层目录都不携带版本号**（路径稳定，快捷方式/自启/更新
链不会随版本反复变更）。版本只出现在两处：

1. **exe 的 PE 文件属性**：`version_file.py` 生成 PyInstaller `--version-file`，
   构建时写 FileVersion / ProductVersion；release workflow 发布前断言
   `(Get-Item app.exe).VersionInfo.FileVersion` 与版本号一致；
2. **发布资产文件名**：`<app>-<version>-windows-x64.zip`（下载 URL 需要；它是文件，不是
   任何运行期依赖的路径）。

发布 zip 的内层固定为**稳定 `<APP_ID>/`**；`update_helper 1.5.1` 按**内容**解析包根
（扁平 exe 或"恰好一个直接含 exe 的顶层目录"），不把目录名/版本号当判据。发布前有
**OTA 布局门禁**：zip 顶层必须唯一等于 `<APP_ID>` 且含 exe，否则不发版。

本地 OTA 验收由模板自带的 [`ota_test/`](../ota_test/README.md) 提供，工具仓构建/CI 直接
调用（无网络、无真应用）。

## 采纳步骤

1. 拷 `build.bat` / `release.bat` 到工具根；`workflows\` 拷到 `.github\workflows\`；
2. 把 `<APP_ID>` / `<COMPANY>` 占位替换；确认版本读取源（`appconfig.py` 或 `main.py`，全链路一处）；
3. build.bat 的冒烟步按工具实况裁剪（如 dsh 的 `--smoke` 依赖本机装有 dsh.cmd，CI 跳过）；
4. CI 依赖清单（requirements.txt）必须入库，pyinstaller 也要列——`cache: pip` 没清单直接报错；
5. 构建/CI 加一条本地 OTA 验收：`python src\template\ota_test\run_local_ota_test.py --app-id <APP_ID>`；
6. **冒烟/自检服务无扰**：门禁只拦构建，**不得顺手停服务**——冒烟与自检是只读动作，
   禁止启停真实的常驻服务（规范 §自检与测试，2026-09-18 补）。

## 边界与坑（全部实测翻过车）

- **bat 保持纯 ASCII**：cmd 按 OEM/GBK 码页解析，UTF-8 中文注释会撕碎后续行；
- **`--specpath build` 时相对 `--add-data` 按 spec 目录解析**：workflow 里用 `$pwd\dir` 绝对路径；
- **onedir 产物 exe 必须保持裸 `EXE_NAME`**：版本进 PE 元数据（`version_file.py` +
  `--version-file`），**不**改 exe 文件名；发布 zip 内层用稳定 `<APP_ID>/`；
- **OTA 本地验收**：工具仓的构建/CI 调 `python src\template\ota_test\run_local_ota_test.py
  --app-id <APP_ID>`；它用 `probe.vbs` 当替身，不能用真实 exe 名（真机可能正跑着同名进程，
  bat 的"等旧进程退出"会死等）；
- robocopy 退出码 0–7 都是成功，`errorlevel 8` 才算失败；
- runner stdout 是管道，`PYTHONUTF8=1` 否则中文即死；
- 大资源 CI 拿不到：workflow 里显式下载，或无资源时明确跳过。
