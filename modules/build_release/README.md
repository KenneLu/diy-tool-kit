# T8+T9 · build_release —— 门禁构建 + tag 发版链

> 规范出处：STANDARDS.md §D1（构建即门禁）、§G1/G3/G4、§H 发布链规范 1–6。
> 蓝本：local-speak2text 的 build.bat/release.bat/workflows（reme-helper 的 ASCII 教训已吸收）。

## 定位

两件事，各一份骨架：

1. **build.bat（T8）**：门禁顺序 = 编译检查 → 单元测试（有则跑）→ PyInstaller
   onedir/noconsole → 冻结冒烟。**便宜在前、昂贵在后**，每步失败判定 + 非零退出，
   禁止人眼判断成功。
2. **release.bat + workflows（T9）**：`release.bat` 打 `v<semver>` tag 并推送 →
   `release.yml` 在 CI 干净检出上构建、出 zip+sha256、发布 GitHub Release；
   `tests.yml` 对所有分支的 push/PR 跑编译与测试。手动 `workflow_dispatch` 只出
   工件不发布。

## 采纳步骤

1. 拷 `build.bat` / `release.bat` 到工具根；`workflows\` 拷到 `.github\workflows\`；
2. 把 `<APP_ID>` 占位替换；确认版本读取源（`appconfig.py` 或 `main.py`，全链路一处）；
3. build.bat 的冒烟步按工具实况裁剪（如 dsh 的 `--smoke` 依赖本机装有 dsh.cmd，CI 跳过）；
4. CI 依赖清单（requirements.txt）必须入库，pyinstaller 也要列——`cache: pip` 没清单直接报错。
4. **冒烟/自检服务无扰**：门禁只拦构建，**不得顺手停服务**——冒烟与自检是只读动作，
   禁止启停真实的常驻服务（规范 §D3，2026-09-18 补）。

## 边界与坑（全部实测翻过车）

- **bat 保持纯 ASCII**：cmd 按 OEM/GBK 码页解析，UTF-8 中文注释会撕碎后续行；
- **`--specpath build` 时相对 `--add-data` 按 spec 目录解析**：workflow 里用 `$pwd\dir` 绝对路径；
- **onedir 产物 exe 自带版本名**：发布前改名成裸 `EXE_NAME`（B3：exe 永不带版本号）；
- robocopy 退出码 0–7 都是成功，`errorlevel 8` 才算失败；
- runner stdout 是管道，`PYTHONUTF8=1` 否则中文即死；
- 大资源 CI 拿不到：workflow 里显式下载，或无资源时明确跳过。
