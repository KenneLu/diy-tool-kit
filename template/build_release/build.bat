@echo off
rem build_release build gate skeleton - copy into the tool and fill the <...> placeholders.
rem Layout (naming-and-version): release\<APPNAME>-<VERSION>\<APPNAME>.exe - the exe never carries
rem a version; the release folder and zip name do.
rem ASCII only in this file: cmd.exe parses it with the OEM code page.
rem Usage: build.bat [norun] [nopause] | build.bat clean --force
rem
rem Step skeleton = STANDARDS build-gate (public build flow). Keep the ORDER; tool-specific
rem steps go ONLY at the marked INSERT POINTS. Every step fails non-zero - never
rem judge success by eye.
rem   0 preflight : VERSION parse / target dir free / running-instance target guard
rem   1 cheap     : compile -> template sync -> i18n -> tray suites -> tests
rem   2 selftest  : core path with real resources
rem   3 package   : icon -> PyInstaller -> assemble -> deliverable checks
rem   4 frozen    : smoke (dual env pin) -> trigger checks -> DONE

setlocal EnableExtensions
cd /d "%~dp0"

set RUN_AFTER=1
set NOPAUSE=
set BUILD_ARGS=%*
if not defined BUILD_ARGS goto :args_done
for %%a in (%BUILD_ARGS%) do (
  if /i "%%a"=="norun" set RUN_AFTER=
  if /i "%%a"=="nopause" set NOPAUSE=1
)
:args_done
if /i "%~1"=="clean" goto :do_clean

set PY=python
set APPNAME=<APP_ID>
rem APP_UC = APP_ID uppercased with '-' turned into '_' (naming-and-version/env-var-derivation),
rem e.g. dsh-helper -> DSH_HELPER. Used for the dual isolation pin below.
set APP_UC=<APP_ID_UC>
rem Path of the template repo as seen from this tool (for the sync gate).
set TEMPLATE=..\my-diy-tool-template

rem ---------------------------------------------------------------------------
rem 0.1 VERSION - single source of truth (point at ONE place: main.py or appconfig.py)
rem Two-step parse. Do NOT use "tokens=2,*": it hands the REST OF THE LINE to the
rem variable, so a trailing comment becomes part of the version and turns
rem RELEASE_DIR into garbage. Rule (naming-and-version): nothing after the closing quote but blanks.
rem   step 1  split on '='                               ->  "1.4.0"   # comment
rem   step 2  drop quotes, keep first space-delimited token  ->  1.4.0
rem ---------------------------------------------------------------------------
set VERSION=
for /f "tokens=2 delims==" %%a in ('%SystemRoot%\System32\findstr.exe /b /c:"VERSION = " src\main.py') do set VERSION=%%a
if defined VERSION for /f "tokens=1" %%a in ("%VERSION:"=%") do set VERSION=%%a
if not defined VERSION (
  echo [ERROR] Cannot read VERSION from src\main.py.
  if not defined NOPAUSE pause
  exit /b 1
)
set RELEASE_DIR=release\%APPNAME%-%VERSION%
set FROZEN_EXE=%RELEASE_DIR%\%APPNAME%.exe
echo [VERSION] %VERSION%  release: %RELEASE_DIR%

rem ---------------------------------------------------------------------------
rem 0.2 target dir (RELAXED 2026-09-19, exe-delete-guard): existence is INFO, not a refusal.
rem One-version-one-dir is kept by *rebuilding from scratch*, not by refusing.
rem The refusal condition is 0.3 (live instance running FROM the target dir); the
rem kernel side is exe-delete-guard - the instance holds its own exe without FILE_SHARE_DELETE,
rem so deleting it fails loudly (winerror 32) instead of hollowing it silently.
rem CLEANLINESS IS NOT RELAXED: the old dir is removed in 0.3b, after the guard.
rem ---------------------------------------------------------------------------
if exist "%RELEASE_DIR%" echo [INFO] %RELEASE_DIR% exists - will be removed and rebuilt from scratch.

rem ---------------------------------------------------------------------------
rem 0.3 running-instance guard (build-run-detect refined 2026-09-19)
rem Refuse ONLY when a live instance runs FROM this build's target dir. Building a
rem DIFFERENT version dir is safe: files differ, the frozen smoke pins its own data
rem dir and takes no mutex. The dangerous case is deleting/overwriting the dir a
rem live instance runs from - and that rule covers EVERY delete of a release dir
rem (this build, a manual rmdir, build.bat clean), not just building.
rem ---------------------------------------------------------------------------
set "TARGET_ABS=%CD%\%RELEASE_DIR%"
call :guard_target_not_running
if errorlevel 1 (
  echo [ERROR] A %APPNAME% instance is running FROM %RELEASE_DIR%.
  echo [ERROR] Exit it from the tray before touching this directory.
  if not defined NOPAUSE pause
  exit /b 1
)

rem ---------------------------------------------------------------------------
rem 0.3b cleanliness (relaxed): remove the existing same-version dir NOW, so the
rem build always assembles from scratch and never reuses a stale file. A live
rem instance would have been refused in 0.3; any other lock fails loudly here.
rem ---------------------------------------------------------------------------
if exist "%RELEASE_DIR%" (
  echo [INFO] removing %RELEASE_DIR% - rebuild from scratch ...
  rmdir /s /q "%RELEASE_DIR%"
)
if exist "%RELEASE_DIR%" (
  echo [ERROR] could not remove %RELEASE_DIR% - it is locked, possibly by a live instance.
  if not defined NOPAUSE pause
  exit /b 1
)

rem ---------------------------------------------------------------------------
rem 1 cheap gates (cheap first, expensive later)
rem ---------------------------------------------------------------------------
echo [GATE] 1.1 compile ...
%PY% -m py_compile src\main.py
if errorlevel 1 (
  echo [ERROR] compile gate failed.
  if not defined NOPAUSE pause
  exit /b 1
)

echo [GATE] 1.2 template sync check ...
if exist "%TEMPLATE%\sync_check.py" (
  %PY% "%TEMPLATE%\sync_check.py" --roots %APPNAME%
  if errorlevel 1 (
    echo [ERROR] template drift - see the sync_check output above.
    if not defined NOPAUSE pause
    exit /b 1
  )
) else (
  echo [WARN] sync_check.py not found next to this tool - gate skipped. CI checkouts
  echo [WARN] do not contain the template repo; that gap is accepted and documented.
)

rem 1.3 i18n table coverage (bilingual-i18n triggers) - enable when the tool ships i18n
rem echo [GATE] 1.3 i18n coverage ...
rem %PY% tests\test_i18n.py

rem 1.4 tray suites: single instance / startup path / i18n menu refresh (tray tools)
rem echo [GATE] 1.4 tray suites ...
rem %PY% tests\test_single_instance.py
rem %PY% tests\test_startup_path.py

echo [GATE] 1.5 tests (full suite set) ...
if exist tests\*.py (
  %PY% -m pytest -q tests
  if errorlevel 1 (
    echo [ERROR] tests failed.
    if not defined NOPAUSE pause
    exit /b 1
  )
) else (
  echo [ERROR] no tests\ directory - build-gate requires one (capabilities exist, so do
  echo [ERROR] regressions). Missing tests are a GAP, not an allowed difference.
  if not defined NOPAUSE pause
  exit /b 1
)

rem ==== INSERT POINT A: tool-specific static / side-effect-free checks ====

rem ---------------------------------------------------------------------------
rem 2 business selftest - core path with REAL resources (not covered by unit tests)
rem ---------------------------------------------------------------------------
rem echo [TEST] 2.1 core selftest ...
rem %PY% src\pipeline.py

rem ==== INSERT POINT B: tool-specific heavy-resource checks ====

rem ---------------------------------------------------------------------------
rem 3 package
rem ---------------------------------------------------------------------------
echo [BUILD] 3.1 icon ...
if exist src\icons.py (
  %PY% src\icons.py
  if errorlevel 1 (
    echo [ERROR] icon generation failed.
    if not defined NOPAUSE pause
    exit /b 1
  )
)

echo [BUILD] 3.2 PyInstaller onedir noconsole ...
%PY% -m PyInstaller --noconfirm --clean --onedir --noconsole ^
  --name %APPNAME% ^
  --distpath build\dist_tmp ^
  --workpath build\work ^
  --specpath build ^
  src\main.py
if errorlevel 1 (
  echo [ERROR] PyInstaller failed.
  if not defined NOPAUSE pause
  exit /b 1
)

echo [PACK] 3.3 assembling %RELEASE_DIR% ...
if not exist "%RELEASE_DIR%" mkdir "%RELEASE_DIR%"
%SystemRoot%\System32\Robocopy.exe "build\dist_tmp\%APPNAME%" "%RELEASE_DIR%" /E /R:1 /W:1 /NFL /NDL /NP >nul
if errorlevel 8 (
  echo [ERROR] package copy failed.
  if not defined NOPAUSE pause
  exit /b 1
)
rmdir /s /q "build\dist_tmp" 2>nul
if exist README.md copy /y README.md "%RELEASE_DIR%" >nul
if exist README.zh-CN.md copy /y README.zh-CN.md "%RELEASE_DIR%" >nul

echo [GATE] 3.4 deliverable checks ...
if not exist "%FROZEN_EXE%" (
  echo [ERROR] %APPNAME%.exe missing from the release.
  if not defined NOPAUSE pause
  exit /b 1
)
if not exist "%RELEASE_DIR%\_internal\base_library.zip" (
  echo [ERROR] _internal has no runtime - the package is incomplete.
  if not defined NOPAUSE pause
  exit /b 1
)

rem ---------------------------------------------------------------------------
rem 4 frozen verify - ALWAYS pin BOTH env vars (instance isolation):
rem   APP_UC_CONFIG    the config THIS package ships
rem   APP_UC_DATA_DIR  the whole data root -> inside the release dir
rem Without the data-dir pin the smoke writes into the user's live AppData.
rem ---------------------------------------------------------------------------
set "PYTHONUTF8=1"
set "%APP_UC%_CONFIG=%CD%\%RELEASE_DIR%\config.json"
set "%APP_UC%_DATA_DIR=%CD%\%RELEASE_DIR%\smoke-data"
echo [TEST] 4.1 frozen smoke ...
"%FROZEN_EXE%" --smoke
set SMOKE_RC=%errorlevel%
set "%APP_UC%_CONFIG="
set "%APP_UC%_DATA_DIR="
if exist "%RELEASE_DIR%\smoke.log" del /q "%RELEASE_DIR%\smoke.log"
if exist "%RELEASE_DIR%\log" rmdir /s /q "%RELEASE_DIR%\log"
if exist "%RELEASE_DIR%\smoke-data" rmdir /s /q "%RELEASE_DIR%\smoke-data"
if not "%SMOKE_RC%"=="0" (
  echo [ERROR] smoke test failed.
  if not defined NOPAUSE pause
  exit /b 1
)

rem 4.2 frozen trigger checks (enable when the tool has them)
rem echo [TEST] 4.2 frozen ui-check ...
rem "%FROZEN_EXE%" --ui-check

rem ==== INSERT POINT C: tool-specific frozen-state checks ====

echo.
echo [DONE] 4.3 release: %FROZEN_EXE%
if defined RUN_AFTER start "" "%FROZEN_EXE%"
if not defined NOPAUSE pause
exit /b 0

rem ---------------------------------------------------------------------------
rem guard: errorlevel 1 when a live %APPNAME% instance runs from %TARGET_ABS%
rem Caller sets TARGET_ABS (absolute dir, NO trailing backslash).
rem MUST precede any build, rmdir or clean that deletes/overwrites a release dir.
rem ---------------------------------------------------------------------------
:guard_target_not_running
set "RUN_EXE="
for /f "usebackq delims=" %%p in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "(Get-Process -Name '%APPNAME%' -ErrorAction SilentlyContinue | Where-Object { $_.Path } | Select-Object -First 1 -ExpandProperty Path)" 2^>nul`) do set "RUN_EXE=%%p"
if not defined RUN_EXE exit /b 0
echo [GATE] running instance: %RUN_EXE%
for %%d in ("%RUN_EXE%") do set "RUN_DIR=%%~dpd"
set "RUN_DIR=%RUN_DIR:~0,-1%"
if /i "%RUN_DIR%"=="%TARGET_ABS%" exit /b 1
exit /b 0

rem ---------------------------------------------------------------------------
rem clean: remove release\ - but never the directory a live instance runs from
rem ---------------------------------------------------------------------------
:do_clean
if /i not "%~2"=="--force" (
  echo [ERROR] clean removes release\ - pass --force to confirm.
  exit /b 1
)
for /d %%D in ("release\%APPNAME%-*") do (
  set "TARGET_ABS=%%~fD"
  call :guard_target_not_running
  if errorlevel 1 (
    echo [ERROR] refusing to clean %%~fD - a live instance runs from it.
    exit /b 1
  )
)
rmdir /s /q "release" 2>nul
echo [CLEAN] removed release\
exit /b 0
