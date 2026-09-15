@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0status.ps1" %*
if %ERRORLEVEL% neq 0 (
    exit /b %ERRORLEVEL%
)
