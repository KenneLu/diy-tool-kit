# baseline —— 仓库基线件规范（README 双语 / CHANGELOG / LICENSE / .gitignore）

> 蓝本：reme-helper / local-speak2text 的仓库形态。

## 定位

本目录不放代码，只承载**每个新仓库必配的文件清单与规范**：

| 文件 | 规范 |
|---|---|
| `README.md` + `README.zh-CN.md` | **基线 8，触发条件 = 开源/交付他人**（⚠️ 与中英双语 i18n 触发无关，2026-09-18 勘误）。英文 canonical + 中文版；顶部语言切换行（英文版 `**English** \| [简体中文](README.zh-CN.md)`，中文版 `[English](README.md) \| **简体中文**`，当前语言加粗不带链接）；不是机翻直译，同信息各自地道；两份都随 release zip |
| `CHANGELOG.md` | 每版本一节，与 tag 对应；未发版改动挂 `## Unreleased` |
| `LICENSE` | MIT（版权行占位，采纳后自填） |
| `.gitignore` | build/dist/out/release/__pycache__/*.pyc/log/config.json（数据区已在 LOCALAPPDATA，exe 旁只允许出厂模板） |

## 自查清单

- [ ] 基线 8 判定过了吗？（公开仓库 = 必做双语，别挂到中英双语 i18n 上）
- [ ] 两份 README 都进 release zip 了吗？
- [ ] CHANGELOG 最新节与 tag 一致吗？
- [ ] git 里没有用户数据、构建产物、生成图标？
