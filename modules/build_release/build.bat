@echo off
setlocal EnableExtensions
cd /d "%~dp0"

rem T8 build gate skeleton (copy into the tool, adjust PY/APPNAME/gates).
rem Layout (G1/B3): release\<APPNAME>-<VERSION>\<APPNAME>.exe - the exe never
rem carries a version; the release folder and zip name do.
rem Gates: compile check -> unit tests (if any) -> PyInstaller -> frozen smoke.
rem ASCII only in this file: cmd.exe parses it with the OEM code page.
rem Usage: build.bat [norun] [nopause]

set RUN_AFTER=1
set NOPAUSE=
set BUILD_ARGS=%*
if not defined BUILD_ARGS goto :args_done
for %%a in (%BUILD_ARGS%) do (
  if /i "%%a"=="norun" set RUN_AFTER=
  if /i "%%a"=="nopause" set NOPAUSE=1
)
:args_done

set PY=python
set APPNAME=<APP_ID>
rem Version single source of truth: VERSION in src\main.py (or paths.py).
rem Parse BETWEEN THE QUOTES: the line may carry a trailing comment, e.g.
rem   VERSION = "1.4.0"   # only changed at release time
rem "tokens=2,*" would swallow the comment into VERSION and corrupt
rem RELEASE_DIR. Rule (B3): nothing after the closing quote but blanks.
set VERSION=
for /f tokens^=2^ delims^=^" %%a in ('findstr /b /c:"VERSION = " src\main.py') do set VERSION=%%a
if not defined VERSION (
  echo [ERROR] Cannot read VERSION.
  if not defined NOPAUSE pause
  exit /b 1
)
set RELEASE_DIR=release\%APPNAME%-%VERSION%
set FROZEN_EXE=%RELEASE_DIR%\%APPNAME%.exe

if exist "%RELEASE_DIR%" (
  echo [ERROR] %RELEASE_DIR% already exists. Delete it or bump VERSION.
  if not defined NOPAUSE pause
  exit /b 1
)

rem D1-02 refined (2026-09-19): building into a NEW version dir does not touch a
rem running instance - the smoke runs from the new dir with an isolated data dir
rem and takes no mutex. So do NOT block on "some instance is running"; block only
rem when the running instance lives INSIDE this build's target dir (the one truly
rem dangerous case: overwriting/deleting a release dir that is in use).
call :guard_target_not_running
if errorlevel 1 exit /b 1

echo [GATE] compile check ...
%PY% -m py_compile src\main.py
if errorlevel 1 (
  echo [ERROR] compile gate failed.
  if not defined NOPAUSE pause
  exit /b 1
)

echo [GATE] unit tests (if present) ...
if exist tests\*.py %PY% -m pytest -q tests
if errorlevel 1 (
  echo [ERROR] tests failed.
  if not defined NOPAUSE pause
  exit /b 1
)

echo [BUILD] PyInstaller onedir noconsole ...
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

echo [PACK] assembling %RELEASE_DIR% ...
if not exist "%RELEASE_DIR%" mkdir "%RELEASE_DIR%"
robocopy "build\dist_tmp\%APPNAME%" "%RELEASE_DIR%" /E /R:1 /W:1 /NFL /NDL /NP >/dev/null
if errorlevel 8 (
  echo [ERROR] package copy failed.
  if not defined NOPAUSE pause
  exit /b 1
)
rmdir /s /q "build\dist_tmp" 2>/dev/null

if exist README.md copy /y README.md "%RELEASE_DIR%" >/dev/null
if exist README.zh-CN.md copy /y README.zh-CN.md "%RELEASE_DIR%" >/dev/null

rem Deliverable checks: exe + runtime - guards against a silently empty package.
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

set "PYTHONUTF8=1"
echo [TEST] frozen smoke ...
"%FROZEN_EXE%" --smoke
if errorlevel 1 (
  echo [ERROR] smoke test failed.
  if not defined NOPAUSE pause
  exit /b 1
)
if exist "%RELEASE_DIR%\smoke.log" del /q "%RELEASE_DIR%\smoke.log"
if exist "%RELEASE_DIR%\log" rmdir /s /q "%RELEASE_DIR%\log"

echo.
echo [DONE] release: %FROZEN_EXE%
if defined RUN_AFTER start "" "%FROZEN_EXE%"
if not defined NOPAUSE pause
exit /b 0

rem ---------------------------------------------------------------------------
rem D1-02 guard: refuse only when a running instance lives under %RELEASE_DIR%.
rem MUST be called before ANY action that deletes/overwrites a release dir
rem (this build, a manual rmdir, or a future --clean switch) - the gate has to
rem protect the in-use directory, not "any running instance".
rem Returns errorlevel 1 when blocked.
rem ---------------------------------------------------------------------------
:guard_target_not_running
set "TARGET_ABS=%CD%\%RELEASE_DIR%"
set "RUN_EXE="
for /f "usebackq delims=" %%p in (`powershell -NoProfile -ExecutionPolicy Bypass -Command "(Get-Process -Name '%APPNAME%' -ErrorAction SilentlyContinue | Where-Object { $_.Path } | Select-Object -First 1 -ExpandProperty Path)" 2^>nul`) do set "RUN_EXE=%%p"
if not defined RUN_EXE exit /b 0
echo [GATE] running instance: %RUN_EXE%
rem Compare the instance's DIRECTORY with the target dir (strip the trailing
rem backslash %%~dpd adds). Beats string-prefix matching: no quoting pitfalls.
for %%d in ("%RUN_EXE%") do set "RUN_DIR=%%~dpd"
set "RUN_DIR=%RUN_DIR:~0,-1%"
if /i "%RUN_DIR%"=="%TARGET_ABS%" (
  echo [ERROR] The running instance lives inside %RELEASE_DIR%.
  echo         Exit it from the tray before touching THIS release dir.
  echo         (Building another version dir stays allowed - D1-02.)
  if not defined NOPAUSE pause
  exit /b 1
)
exit /b 0
