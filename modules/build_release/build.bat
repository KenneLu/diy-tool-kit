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
set VERSION=
for /f "tokens=2,*" %%a in ('findstr /b /c:"VERSION = " src\main.py') do set VERSION=%%~b
if not defined VERSION (
  echo [ERROR] Cannot read VERSION.
  if not defined NOPAUSE pause
  exit /b 1
)
set VERSION=%VERSION:"=%
set RELEASE_DIR=release\%APPNAME%-%VERSION%
set FROZEN_EXE=%RELEASE_DIR%\%APPNAME%.exe

if exist "%RELEASE_DIR%" (
  echo [ERROR] %RELEASE_DIR% already exists. Delete it or bump VERSION.
  if not defined NOPAUSE pause
  exit /b 1
)

echo [GATE] running-instance check (prefix match - any version blocks) ...
tasklist /fo csv 2>/dev/null | findstr /i /c:"%APPNAME%" >/dev/null
if not errorlevel 1 (
  echo [ERROR] %APPNAME% is running. Exit the tray app first.
  if not defined NOPAUSE pause
  exit /b 1
)

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
