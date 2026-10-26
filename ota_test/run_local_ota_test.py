# -*- coding: utf-8 -*-
"""模板自带「本地 OTA 验收测试」：无网络、无真应用、无可见窗口。

为什么放在模板仓：更新链是 4 个工具共用的公共模块，OTA 的**接缝**（下载→解压→选包根→
写替换脚本→等旧进程→快照→铺设→重启）必须由模板统一验收，而不是各工具各写一份。工具
仓只需要在本地跑这个脚本（见下），CI/构建脚本也可以挂它。

它验证什么（用 probe.vbs 当替身 exe，`--version-file` 的 PE 元数据不在本测试范围）：

  1. 包根解析：稳定目录（``<APP_ID>/``）、任意目录名（含旧版本化目录）、扁平 zip、
     歧义/缺 exe 的 fail-closed；
  2. 完整替换链：真 `download_and_prepare()` + 真生成的 bat → 快照 → robocopy → 新
     exe 被启动 → 旧版进 `_backup` → 暂存被清理 → `update.log` 有 done。

运行方式（在借用模板的工具仓根目录；模板落在 `src/template/`）：

    python src/template/ota_test/run_local_ota_test.py
    python src/template/ota_test/run_local_ota_test.py --app-id reme-helper

`--app-id` 只影响合成包里的目录名（让测试贴近该工具的真实发布布局）。
**完整替换链固定用 `probe.vbs`**：不能用真实 exe 名——真机上可能正跑着同名进程，
替换 bat 的等待循环会一直等它（这正是真实产品要等玩家退出的行为，但在测试里是死等）。
CI/构建脚本应当跑同一条命令。
"""
from __future__ import annotations

import hashlib
import os
import shutil
import sys
import tempfile
import time
import types
import zipfile
from pathlib import Path

SCRIPT = Path(__file__).resolve()
# 工具侧布局：<tool>/src/template/ota_test/run_local_ota_test.py -> 把 <tool>/src 放进
# sys.path，`import template.update_helper` 才能按产品同一条 import 面走。
TOOL_SRC = SCRIPT.parents[2]
if not (TOOL_SRC / "template" / "update_helper").is_dir():
    print("OTA LOCAL TEST SKIP/FAILED: run this from a tool repo that borrows the template "
          "(expected %s)" % (TOOL_SRC / "template" / "update_helper"), flush=True)
    sys.exit(2)
sys.path.insert(0, str(TOOL_SRC))

from template.update_helper import update_helper as uh  # noqa: E402

FAILS: list[str] = []


def check(name: str, ok, detail: str = "") -> None:
    print(("  ok  " if ok else "  FAIL") + " " + name + ("  " + detail if detail else ""),
          flush=True)
    if not ok:
        FAILS.append(name)


def _vbs(marker: Path, note: str = "") -> str:
    """假 exe：被 `start` 启动时写 marker（wscript，无控制台窗口）。"""
    body = ('CreateObject("Scripting.FileSystemObject").CreateTextFile("%s", True).Write "x"\r\n'
            % str(marker))
    return ("' %s\r\n%s" % (note, body)) if note else body


def _resolver_case(root: Path, name: str, entries: dict[str, bytes]):
    """在合成的 update_dir 里放文件，返回 (resolved, error)。"""
    update_dir = root / name
    update_dir.mkdir(parents=True)
    for rel, data in entries.items():
        target = update_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    # 真实暂存根里还会有刚下载的 zip / sha256；它们不能影响包根判定。
    (update_dir / "pkg.zip").write_bytes(b"zip")
    (update_dir / "pkg.zip.sha256").write_text("0" * 64, encoding="utf-8")
    try:
        resolved = uh.resolve_staged_dir(str(update_dir), exe_name="probe.vbs")
        return resolved, None
    except RuntimeError as exc:
        return None, str(exc)


def resolver_cases(root: Path) -> None:
    print("[1/3] package-root resolution (name/version agnostic)", flush=True)
    resolved, err = _resolver_case(root, "stable-folder",
                                   {"ota-probe/probe.vbs": b"new"})
    check("stable <APP_ID>/ folder", resolved == root / "stable-folder" / "ota-probe", err or str(resolved))

    resolved, err = _resolver_case(root, "legacy-versioned-folder",
                                   {"ota-probe-9.9.9/probe.vbs": b"new"})
    # 名称不是判据：旧版本化目录名也能被认出来（其它工具的存量发布包不会因此断更）。
    check("any single folder name is resolved", resolved == root / "legacy-versioned-folder" / "ota-probe-9.9.9",
          err or str(resolved))

    resolved, err = _resolver_case(root, "flat-zip", {"probe.vbs": b"new"})
    check("flat zip (exe at extraction root)", resolved == root / "flat-zip", err or str(resolved))

    _, err = _resolver_case(root, "ambiguous",
                            {"a/probe.vbs": b"1", "b/probe.vbs": b"2"})
    check("ambiguous (two folders hold exe) fails closed",
          err is not None and "staged exe missing" in err, err or "no error")

    _, err = _resolver_case(root, "missing-exe", {"ota-probe/README.md": b"doc"})
    check("no exe anywhere fails closed", err is not None and "staged exe missing" in err,
          err or "no error")


def _make_package(root: Path, app_id: str, exe_name: str, marker: Path) -> tuple[bytes, str, Path]:
    pkg_root = root / "pkg" / app_id
    pkg_root.mkdir(parents=True)
    (pkg_root / exe_name).write_text(_vbs(marker, "new build"), encoding="utf-8")
    (pkg_root / "new.txt").write_text("new", encoding="utf-8")
    (pkg_root / "README.md").write_text("pkg", encoding="utf-8")
    zip_path = root / "pkg.zip"
    with zipfile.ZipFile(str(zip_path), "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(pkg_root.rglob("*")):
            if path.is_file():
                z.write(str(path), path.relative_to(root / "pkg").as_posix())
    raw = zip_path.read_bytes()
    return raw, hashlib.sha256(raw).hexdigest(), pkg_root


def full_chain_case(root: Path, app_id: str, exe_name: str) -> None:
    print("[2/3] full replace chain (real download_and_prepare + real bat)", flush=True)
    data = root / "data"
    install = data / "install"
    install.mkdir(parents=True)
    (install / exe_name).write_text("' old build\r\n", encoding="utf-8")
    (install / "old.txt").write_text("old", encoding="utf-8")
    staging = data / "update-staging"
    marker = root / "restarted.txt"
    raw, digest, _pkg_root = _make_package(root, app_id, exe_name, marker)
    tmpdir = root / "tmp"
    tmpdir.mkdir()

    saved_download = uh._download
    saved_tempfile = uh.tempfile
    progress_calls = []
    try:
        def fake_download(url, dest, timeout=120.0, progress=None):
            dest = Path(dest)
            # 真 _download 会自建父目录；替身必须同形，否则会在"暂存根还不存在"时炸。
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.name.endswith(".zip"):
                dest.write_bytes(raw)
                if progress is not None:   # 1.5.2：进度回调必须真的被调用
                    progress(len(raw) // 2, len(raw))
                    progress(len(raw), len(raw))
                    progress_calls.extend([len(raw) // 2, len(raw)])
            elif dest.name.endswith(".zip.sha256"):
                dest.write_text(digest + "  pkg.zip\n", encoding="utf-8")
            else:
                raise AssertionError("unexpected download target: %s" % dest)

        uh._download = fake_download
        uh.tempfile = types.SimpleNamespace(gettempdir=lambda: str(tmpdir))
        uh.download_and_prepare("9.9.9", str(install), str(staging), log=lambda *a: None,
                                repo="example/ota", exe_name=exe_name, progress=lambda *a: None)
        check("download progress callback delivered (1.5.2)",
              len(progress_calls) == 2 and progress_calls[-1] == len(raw), str(progress_calls))
        pending = uh.pending_cmd()
        check("replace script generated", bool(pending) and Path(pending).is_file(),
              str(pending))
        check("replace script lives outside the stage dir",
              bool(pending) and Path(pending).parent == tmpdir)
        check("pending script launches", uh.launch_pending_cmd(log=lambda *a: None))

        deadline = time.time() + 90
        while time.time() < deadline and not marker.is_file():
            time.sleep(0.2)
        check("new build was started", marker.is_file())
        check("new package laid down", (install / "new.txt").is_file())
        check("old payload purged", not (install / "old.txt").exists())
        check("exe replaced", "new build" in (install / exe_name).read_text(encoding="utf-8",
                                                                            errors="replace"))
        backup = data / "_backup"
        check("previous build rotated into _backup",
              (backup / exe_name).is_file() and (backup / "old.txt").is_file())
        check("staging cleaned after success", not staging.exists())
        log_text = (data / "update.log").read_text(encoding="utf-8", errors="replace")
        check("update.log records done", "done" in log_text, log_text.replace("\r", " ").strip()[-160:])
    finally:
        uh._download = saved_download
        uh.tempfile = saved_tempfile
        uh._PUBLISHED["pending_cmd"] = None


def missing_exe_chain_case(root: Path) -> None:
    print("[3/3] fail-closed before generating a replace script", flush=True)
    data = root / "data"
    install = data / "install"
    install.mkdir(parents=True)
    staging = data / "update-staging"
    pkg_root = root / "pkg" / "ota-probe"
    pkg_root.mkdir(parents=True)
    (pkg_root / "README.md").write_text("no exe", encoding="utf-8")
    zip_path = root / "pkg.zip"
    with zipfile.ZipFile(str(zip_path), "w") as z:
        for path in sorted(pkg_root.rglob("*")):
            if path.is_file():
                z.write(str(path), path.relative_to(root / "pkg").as_posix())
    raw = zip_path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    tmpdir = root / "tmp"
    tmpdir.mkdir()
    saved_download = uh._download
    saved_tempfile = uh.tempfile
    try:
        def fake_download(url, dest, timeout=120.0, progress=None):
            dest = Path(dest)
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.name.endswith(".zip"):
                dest.write_bytes(raw)
            elif dest.name.endswith(".zip.sha256"):
                dest.write_text(digest + "  pkg.zip\n", encoding="utf-8")

        uh._download = fake_download
        uh.tempfile = types.SimpleNamespace(gettempdir=lambda: str(tmpdir))
        error = None
        try:
            uh.download_and_prepare("9.9.9", str(install), str(staging),
                                    log=lambda *a: None, repo="example/ota",
                                    exe_name="probe.vbs")
        except RuntimeError as exc:
            error = str(exc)
        check("exe-less package aborts with staged-exe error",
              error is not None and "staged exe missing" in error, error or "no error")
        check("no replace script was generated", uh.pending_cmd() is None)
    finally:
        uh._download = saved_download
        uh.tempfile = saved_tempfile
        uh._PUBLISHED["pending_cmd"] = None


def update_ui_checks() -> None:
    """统一更新交互的**无窗口**静态断言（弹窗行为本身用 --ui-demo 肉眼验收）。"""
    print("[4/4] update_ui static checks (no window)", flush=True)
    try:
        from template.update_ui import update_ui as uu
    except Exception as exc:  # noqa: BLE001
        check("update_ui importable", False, "%s: %s" % (type(exc).__name__, exc))
        return
    check("update_ui importable", True)
    check("zh/en key parity", set(uu.STRINGS["zh"]) == set(uu.STRINGS["en"]),
          sorted(set(uu.STRINGS["zh"]) ^ set(uu.STRINGS["en"])))
    zh = uu.format_progress(50, 100, "zh")
    en = uu.format_progress(50, 100, "en")
    check("zh progress contains 50%", "50%" in zh, zh)
    check("en progress contains 50%", "50%" in en, en)
    unknown = uu.format_progress(1234567, 0, "zh")
    check("unknown total still shows downloaded bytes", "1.2 MB" in unknown, unknown)
    for key in ("downloaded", "hint", "apply", "later", "error"):
        check("both languages have %r" % key,
              bool(uu.STRINGS["zh"].get(key)) and bool(uu.STRINGS["en"].get(key)))
    check("hint states the exit requirement",
          "退出" in uu.STRINGS["zh"]["hint"] and "quit" in uu.STRINGS["en"]["hint"].lower(),
          uu.STRINGS["en"]["hint"][:60])


def ui_demo(app_id: str) -> None:
    """可选：打开真实更新弹窗（本地视觉验收；CI 不要开）。"""
    try:
        from template.update_ui import update_ui as uu
    except Exception as exc:  # noqa: BLE001
        print("[demo] update_ui unavailable: %s" % exc, flush=True)
        return

    def fake_download(progress, total=17_519_328, steps=40, delay=0.05):
        for step in range(1, steps + 1):
            progress(int(total * step / steps), total)
            time.sleep(delay)
        time.sleep(0.5)

    print("[demo] opening the real update dialog (visual acceptance) ...", flush=True)
    decision = uu.run_download_dialog(fake_download, lang="zh", app_name=app_id, log=print)
    print("[demo] user decision: %r" % (decision,), flush=True)


def main(argv: list[str]) -> int:
    if os.name != "nt":
        print("OTA LOCAL TEST SKIPPED (Windows-only replacement chain)", flush=True)
        return 0
    app_id = "ota-probe"
    ui_demo_requested = False
    args = list(argv[1:])
    while args:
        arg = args.pop(0)
        if arg == "--app-id" and args:
            app_id = args.pop(0)
        elif arg == "--ui-demo":
            ui_demo_requested = True
        else:
            print("OTA LOCAL TEST FAILED: unknown argument %r" % arg, flush=True)
            return 2
    # 完整替换链的替身 exe 固定用 probe.vbs：真实 exe 名若恰好有常驻进程（用户机器上很
    # 常见），bat 的"等旧进程退出"会等满预算，测试会变成假红/慢红。
    probe_exe = "probe.vbs"
    root = Path(tempfile.mkdtemp(prefix="ota-local-test-"))
    try:
        resolver_cases(root / "resolver")
        full_chain_case(root / "chain", app_id, probe_exe)
        missing_exe_chain_case(root / "negative")
    finally:
        shutil.rmtree(root, ignore_errors=True)
    update_ui_checks()
    if ui_demo_requested:
        ui_demo(app_id)
    print("OTA LOCAL TEST " + ("FAILED: " + ",".join(FAILS) if FAILS else "OK"), flush=True)
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
