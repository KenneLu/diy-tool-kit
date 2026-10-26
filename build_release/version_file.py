# -*- coding: utf-8 -*-
"""版本元数据写入器：把版本号写进 exe 的 PE 文件属性（PyInstaller --version-file）。

命名规则（2026-10-26 用户定）：**安装目录、exe 文件名、zip 内层目录都不携带版本号**，
否则频繁更新会让快捷方式/自启/更新链里的路径反复变更。版本号只出现在两处：

  * exe 的 PE 文件属性（FileVersion / ProductVersion）——本脚本负责生成；
  * 发布资产文件名（`<app>-<version>-windows-x64.zip`）——下载 URL 需要，且是文件
    而非任何运行期依赖的路径。

用法（构建脚本调用；纯标准库，不 import 模板包）：

    python version_file.py <输出路径> <版本号> [<app 名>] [<公司名>]

生成的是 PyInstaller 认识的 VSVersionInfo Python 文本；构建脚本把它传给
`PyInstaller --version-file <输出路径>`。字符串刻意保持 ASCII，避免版本资源代码页问题。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def _version_quad(version: str) -> tuple[int, int, int, int]:
    """'1.2.18' -> (1,2,18,0)；取不到数字按 0。"""
    nums = [int(x) for x in re.findall(r"\d+", str(version or ""))][:3]
    nums += [0] * (3 - len(nums))
    return (nums[0], nums[1], nums[2], 0)


def build_version_info_text(version: str, app_name: str = "app", company: str = "") -> str:
    """返回 PyInstaller version-file 的文本内容（ASCII）。

    `app_name` 用作 ProductName / InternalName；exe 文件名按 `<app_name>.exe` 记
    OriginalFilename（调用方传的应是稳定的 APP_ID，不含版本号）。
    """
    a, b, c, d = _version_quad(version)
    app_name = str(app_name or "app")
    company = str(company or "")
    copyright_text = "Copyright (C) " + company if company else ""
    # 040904b0 = 语言 0x0409(en-US) + 代码页 0x04b0(Unicode)
    fields = [
        ("CompanyName", company),
        ("FileDescription", app_name),
        ("FileVersion", str(version)),
        ("InternalName", app_name),
        ("LegalCopyright", copyright_text),
        ("OriginalFilename", app_name + ".exe"),
        ("ProductName", app_name),
        ("ProductVersion", str(version)),
    ]
    strings = ",\n".join(
        "        StringStruct(%r, %r)" % (name, value) for name, value in fields
    )
    return (
        "VSVersionInfo(\n"
        "  ffi=FixedFileInfo(\n"
        "    filevers=(%d, %d, %d, %d),\n"
        "    prodvers=(%d, %d, %d, %d),\n"
        "    mask=0x3f, flags=0x0, OS=0x40004, fileType=0x1, subtype=0x0, date=(0, 0)\n"
        "  ),\n"
        "  kids=[\n"
        "    StringFileInfo([\n"
        "      StringTable('040904b0', [\n"
        "%s\n"
        "      ])\n"
        "    ]),\n"
        "    VarFileInfo([VarStruct('Translation', [1033, 1200])])\n"
        "  ]\n"
        ")\n" % (a, b, c, d, a, b, c, d, strings)
    )


def write_version_file(path, version: str, app_name: str = "app", company: str = "") -> Path:
    """把 version-file 写到 `path`（父目录不存在则创建），返回 Path。"""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(build_version_info_text(version, app_name, company), encoding="utf-8")
    return target


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print("usage: version_file.py <output> <version> [app_name] [company]", file=sys.stderr)
        return 2
    out, version = argv[1], argv[2]
    app_name = argv[3] if len(argv) > 3 else "app"
    company = argv[4] if len(argv) > 4 else ""
    try:
        target = write_version_file(out, version, app_name, company)
    except OSError as exc:
        print("version-file write failed: %s" % exc, file=sys.stderr)
        return 1
    print("version-file written: %s (Version=%s, app=%s)" % (target, version, app_name))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
