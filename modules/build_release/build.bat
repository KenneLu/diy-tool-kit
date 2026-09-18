@echo off
setlocal EnableExtensions
cd /d "%~dp0"

rem T8 build gate skeleton (copy into the tool, adjust PY/paths).
rem Gates: compile check -> unit tests (if any) -> PyInstaller -> frozen smoke.
rem ASCII only in this file: cmd.exe parses it with the OEM codepage.

set PY=python
rem Version single source of truth: VERSION in appconfig.py (semver, doc D15)
set VERSION=
for /f "tokens=2,*" %%a in ('findstr /b /c:"VERSION = " appconfig.py') do set VERSION=%%~b
if not defined VERSION (
  echo [ERROR] Cannot read VERSION from appconfig.py.
  exit /b 1
)
set VERSION=%VERSION:"=%
set PACKAGE=<APP_ID>-%VERSION%
set EXE=%PACKAGE%.exe

echo [GATE] compile check ...
%PY% -m py_compile main.py
if errorlevel 1 (
  echo [ERROR] compile gate failed.
  exit /b 1
)

echo [GATE] unit tests (if present) ...
if exist test_*.py %PY% -m pytest -q
if errorlevel 1 (
  echo [ERROR] tests failed.
  exit /b 1
)

echo [BUILD] PyInstaller onedir noconsole ...
%PY% -m PyInstaller --noconfirm --clean --onedir --noconsole ^
  --name %PACKAGE% ^
  --distpath build\dist_tmp ^
  --workpath build\work ^
  --specpath build ^
  main.py
if errorlevel 1 (
  echo [ERROR] PyInstaller failed.
  exit /b 1
)

echo [TEST] frozen smoke ...
build\dist_tmp\%PACKAGE%\%EXE% --smoke
if errorlevel 1 (
  echo [ERROR] smoke test failed.
  exit /b 1
)

echo [DONE] package: build\dist_tmp\%PACKAGE%\%EXE%
exit /b 0
