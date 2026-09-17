@echo off
rem T9: tag the current commit and push the tag; a v* tag triggers
rem .github/workflows/release.yml which builds and publishes the release.
rem ASCII only in this file: cmd.exe parses it with the OEM codepage.

rem Version from appconfig.py - the app and the tag can never disagree
set VERSION=
for /f "tokens=2,*" %%a in ('findstr /b /c:"VERSION = " appconfig.py') do set VERSION=%%~b
if not defined VERSION (
  echo [ERROR] Cannot read VERSION from appconfig.py.
  exit /b 1
)
set VERSION=%VERSION:"=%
set TAG=v%VERSION%
echo [VERSION] %VERSION%   [TAG] %TAG%

git rev-parse v%TAG% >nul 2>&1
if not errorlevel 1 (
  echo [ERROR] tag %TAG% already exists.
  exit /b 1
)

set /p CONFIRM=Tag %TAG% and push? (y/N)
if /i not "%CONFIRM%"=="y" (
  echo cancelled.
  exit /b 1
)

git tag v%VERSION% || exit /b 1
git push origin v%VERSION% || exit /b 1
echo [DONE] tag pushed; watch the Actions tab for the release build.
