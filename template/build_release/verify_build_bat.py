# -*- coding: utf-8 -*-
"""build.bat 版本解析的**端到端**回归（模板专属件；`build_release/` 不参与 sync_check 比对）。

为什么不是"片段级"测试：cmd 的解析行为依赖**上下文**（setlocal、变量状态、代码页、
for /f 的执行环境），把两行抠出来单独跑通，不能证明它在**真实脚本里**也对——
1.2.0 的 `findstr` 前缀匹配就属于"片段看着对、两个分支都错"。
故本harness 的做法是：**把模板 build.bat 本体按文档填好占位符，放进一个临时工具骨架，
用 cmd.exe 真实执行整个脚本**，只观察阶段 0 的产物。

四个样本（缺一不可）：
  A  现模板两步式 + `VERSION` 行**带行尾中文注释** → 必须 `[VERSION] 1.4.0`；
     带注释的 VERSION 行正是 命名与版本 记录的故障输入（旧 `"tokens=2,*"` 会把它整段吞进版本号）。
  B  再预置 `release\\<APPNAME>-1.4.0` → 脚本必须按**这个解析出来的名字**拒绝
     （0.2 闸）——证明解析结果真的驱动了文件系统判定，而非只是打印好看。
  C  反向：把两步式换回记录中的旧写法 `"tokens=2,* delims=="` → 必须**把行尾注释吞进
     版本号**（这正是 命名与版本 记的故障：`VERSION = "1.4.0"  # 发版时才改` 整段成了版本号）。
  工具登记表 反向 × 预置目录：旧写法必须**认不出**那个目录、继续往下走（0.2 闸失效）。

模板不派发本文件（`build_release/` 为模板专属目录）；工具侧只要 `build.bat`。
用法：`python my-diy-tool-template/template/build_release/verify_build_bat.py`（退出码 0 = 全过）。
"""
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

try:  # Windows 控制台默认 GBK，中文判定标签会变乱码
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
TPL_BAT = HERE / "build.bat"
APP_ID = "e2etool"
APP_UC = "E2ETOOL"
# VERSION 行刻意带行尾中文注释：这是被记录过的真实故障输入
VERSION_LINE = 'VERSION = "1.4.0"  # 发版时才改'

_GOOD = (b"for /f \"tokens=2 delims==\" %%a in ('findstr /b /c:\"VERSION = \" "
         b"src" + b"\\" + b"main.py') do set VERSION=%%a\r\n"
         b"if defined VERSION for /f \"tokens=1\" %%a in (\"%VERSION:\"=%\") do set VERSION=%%a\r\n")
_BAD = (b"for /f \"tokens=2,* delims==\" %%a in ('findstr /b /c:\"VERSION = \" "
        b"src" + b"\\" + b"main.py') do set VERSION=%%a\r\n")

def _rmtree_strict(path, tries: int = 10, delay: float = 0.2) -> bool:
    """mkdtemp-owned-prefix：删完回读确认。返回 True = 确已消失；False = 还在（调用方计入失败）。

    与 `sync_check._rmtree_strict` 同一规则、同一形态——模板仓自己的脚本也要
    守自己立的判据。
    """
    p = Path(path)
    for _ in range(max(1, tries)):
        shutil.rmtree(p, ignore_errors=True)
        if not p.exists():
            return True
        time.sleep(delay)
    print("[FAIL] temp dir not removed (leak): %s" % p)
    return False

def _instantiate(dst: Path, old_parse: bool) -> None:
    """按文档填占位符（工具侧真实用法）。old_parse=True 造反向样本。"""
    raw = TPL_BAT.read_bytes()
    # 注意顺序：<APP_ID> 是 <APP_ID_UC> 的前缀，先换长的
    b = raw.replace(b"<APP_ID_UC>", APP_UC.encode()).replace(b"<APP_ID>", APP_ID.encode())
    if old_parse:
        assert _GOOD in b, "模板里的两步式解析行与预期不符——请同步本 harness"
        b = b.replace(_GOOD, _BAD)
    dst.write_bytes(b)

def _make_tool(root: Path, old_parse: bool, planted: bool) -> None:
    (root / "src").mkdir(parents=True)
    (root / "src" / "main.py").write_text(VERSION_LINE + "\n", encoding="utf-8")
    if planted:
        (root / "release" / ("%s-1.4.0" % APP_ID)).mkdir(parents=True)
    _instantiate(root / "build.bat", old_parse)

def _run(root: Path):
    proc = subprocess.run(["cmd", "/c", str(root / "build.bat"), "nopause"],
                          capture_output=True)
    out = (proc.stdout + proc.stderr).decode("utf-8", "replace")
    return proc.returncode, [ln.strip() for ln in out.splitlines()
                             if ln.strip().startswith(("[VERSION]", "[ERROR]"))]

def _byte_hygiene_failures(root: Path) -> list:
    """模板自己的 bat 也要过字节卫生。返回 [「文件名: 原因」]；空 = 合规。"""
    out = []
    for p in sorted(root.rglob("*.bat")):
        if any(part in {".git", "__pycache__", "release", "build", "dist"} for part in p.parts):
            continue
        data = p.read_bytes()
        line, lf, tab, nonascii = 1, [], [], []
        for i, b in enumerate(data):
            if b == 0x0A:
                if i == 0 or data[i - 1] != 0x0D:
                    lf.append(line)
                line += 1
            elif b == 0x09:
                tab.append(line)
            elif b > 0x7F and (not nonascii or nonascii[-1] != line):
                nonascii.append(line)
        if lf:
            out.append("%s: LF-only 行 %d 处（首见 第%d 行）" % (p.name, len(lf), lf[0]))
        if tab:
            out.append("%s: 含 0x09 TAB（第 %s 行）"
                       % (p.name, ",".join(str(n) for n in tab[:6])))
        if nonascii:
            out.append("%s: 非 ASCII（第 %s 行）"
                       % (p.name, ",".join(str(n) for n in nonascii[:6])))
    return out

def main() -> int:
    if not TPL_BAT.exists():
        print("[FAIL] 找不到 %s" % TPL_BAT)
        return 1
    base = Path(tempfile.mkdtemp(prefix="verify_build_bat_"))
    failed = 0
    # 0) 字节卫生：模板 bat 是**派发源**——自己带一个 TAB，四个工具就各带一个
    #    （判据同 bat-byte-hygiene：CRLF / 无 0x09 / 纯 ASCII；bat-byte-hygiene 只扫工具仓，模板不在其扫描面内）
    hygiene = _byte_hygiene_failures(HERE)
    failed += len(hygiene)
    print("[%s] 字节卫生（CRLF/无TAB/ASCII）: %s"
          % ("PASS" if not hygiene else "FAIL", "；".join(hygiene) if hygiene else "OK"))
    try:
        cases = (
            ("A  两步式 + 行尾注释", False, False, "1.4.0", True),
            ("B  预置同版本目录被拒", False, True, "1.4.0", False),
            ("C  反向：旧 tokens=2,* ", True, False, "1.4.0", False),
            ("工具登记表 反向 × 预置目录  ", True, True, "1.4.0", False),
        )
        for label, old, planted, want_ver, want_ok in cases:
            root = base / label.split()[0]
            _make_tool(root, old, planted)
            rc, lines = _run(root)
            ver_line = next((l for l in lines if l.startswith("[VERSION]")), "")
            parsed = ver_line[len("[VERSION] "):].split("  release:")[0].strip()
            refused = any(l.startswith("[ERROR]") and "already exists" in l for l in lines)
            if old:  # 反向样本：解析必须失败，且预置目录不得被认出
                ok = parsed != want_ver and not refused
                detail = "解析=%r（应≠%s）；预置目录认否=%s" % (parsed, want_ver, refused)
            elif planted:
                ok = refused and parsed == want_ver
                detail = "解析=%r；按名拒绝=%s" % (parsed, refused)
            else:
                ok = parsed == want_ver
                detail = "解析=%r" % parsed
            failed += 0 if ok else 1
            print("[%s] %s rc=%s  %s" % ("PASS" if ok else "FAIL", label, rc, detail))
    finally:
        # mkdtemp-owned-prefix：删完**回读确认**；删不掉就计入 failed（旧写法 `ignore_errors=True`
        # 会把"删不掉"变成"看起来删掉了"，每跑一次泄漏一个 %TEMP% 目录）。
        if not _rmtree_strict(base):
            failed += 1
    print("[verify_build_bat] " + ("ALL PASS" if not failed else "%d FAILED" % failed))
    return 1 if failed else 0

if __name__ == "__main__":
    sys.exit(main())
