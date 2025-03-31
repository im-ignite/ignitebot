@echo off
echo Checking Telegram Bot Setup...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or higher.
    pause
    exit /b 1
)

:: Run setup.py which will handle everything
python setup.py

pause 