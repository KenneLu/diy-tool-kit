@echo off
rem T9: tag the current commit and push the tag; a v* tag triggers
rem .github/workflows/release.yml which builds and publishes the release.
rem ASCII only in this file: cmd.exe parses it with the OEM codepage.

rem Version from the SAME single source as build.bat (D1 0.1) - the app and the tag
rem can never disagree. Two-step parse; "tokens=2,*" would swallow a trailing
rem comment into VERSION and produce a garbage tag (see STANDARDS B3/D1).
set VERSION=
for /f "tokens=2 delims==" %%a in ('%SystemRoot%\System32\findstr.exe /b /c:"VERSION = " src\main.py') do set VERSION=%%a
if defined VERSION for /f "tokens=1" %%a in ("%VERSION:"=%") do set VERSION=%%a
if not defined VERSION (
  echo [ERROR] Cannot read VERSION from src\main.py.
  exit /b 1
)
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
