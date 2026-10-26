# ota_test —— 本地 OTA 验收测试（模板自带）

**无网络、无真应用、无可见窗口**地跑完整个更新接缝：

```
下载(本地 fixture) -> sha256 -> 解压 -> 选包根 -> 生成替换 bat
  -> 等旧进程退出 -> 快照 -> robocopy /e /purge -> 启动新 exe -> 备份轮转 -> 收尾
```

用 `probe.vbs`（wscript，无控制台窗口）当替身 exe；断言新包落地、旧载荷被清理、旧版进
`_backup`、暂存被清理、`update.log` 出现 done。

## 为什么在模板仓

更新链是 4 个工具共用的公共模块；接缝测试必须只有一份，否则各工具各写一套、各自漂移。
工具仓只负责**调用**它。

## 运行

在借用模板的工具仓根目录（模板落在 `src/template/`）：

```bat
python src\template\ota_test\run_local_ota_test.py
python src\template\ota_test\run_local_ota_test.py --app-id reme-helper
```

`--app-id` 只影响合成包的目录名，让测试贴近该工具的真实发布布局。**完整替换链固定用
`probe.vbs` 当替身**：不能用真实 exe 名——真机可能正跑着同名进程，替换 bat 的“等旧进程
退出”会一直等它（产品行为正确，测试里是死等）。构建脚本与 CI 应跑同一条命令。

## 覆盖

1. 包根解析：稳定 `<APP_ID>/`、任意单一目录名、扁平 zip、歧义（两个目录都含 exe）、
   缺 exe —— 后两者必须 fail-closed；
2. 完整替换链（真 `download_and_prepare()` + 真渲染 bat）；
3. 缺 exe 的包在生成替换脚本之前就中止（绝不进“退出后才失败”的路径）。

## 不覆盖（由发布侧门禁负责）

- 真实 GitHub 下载/网络错误——由发布工作流 + 实际 Release 验收；
- 发布 zip 的顶层目录契约与 exe PE 版本元数据——由 release workflow 的 **OTA 布局门禁**
  在发布前对真实产物断言；
- “旧版更新器装新版”的跨版本行为：修复版无法修运行中的旧更新器，旧版必须手动换一次；
  之后用修复版自身做下一次发布的跨版本验收。
