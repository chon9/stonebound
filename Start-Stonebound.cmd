@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Stonebound needs its first-time setup.
    powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\setup.ps1"
    if errorlevel 1 (
        echo Setup did not finish. See the README for manual setup.
        pause
        exit /b 1
    )
)
".venv\Scripts\python.exe" server.py --open
if errorlevel 1 pause
