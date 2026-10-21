@echo off
title Student Study Planner
echo ========================================================
echo         Starting Student Study Planner...
echo ========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

REM Install dependencies if needed
echo Checking dependencies...
python -m pip install -r requirements.txt --quiet

echo.
echo Launching server at http://127.0.0.1:5000 ...
echo Press Ctrl+C in this terminal window to stop the server.
echo.

REM Start browser automatically
start http://127.0.0.1:5000

REM Run Flask app
python app.py

pause
