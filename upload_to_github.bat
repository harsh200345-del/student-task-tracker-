@echo off
title Push Student Study Planner to GitHub
echo =======================================================================
echo          Pushing Student Study Planner to GitHub...
echo          Repository: https://github.com/harsh200345-del/student-study-planner
echo =======================================================================
echo.

set GIT_PATH="C:\Users\Harsh mani pandey\.gemini\antigravity\scratch\MinGit\cmd\git.exe"

%GIT_PATH% push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo =======================================================================
    echo [SUCCESS] Your project has been uploaded to GitHub!
    echo Refresh your browser: https://github.com/harsh200345-del/student-study-planner
    echo =======================================================================
) else (
    echo.
    echo =======================================================================
    echo If GitHub asks to sign in:
    echo 1. Sign in via the browser popup window that appears.
    echo 2. Or use a GitHub Personal Access Token as the password.
    echo =======================================================================
)

echo.
echo Press any key to close this window.
pause >nul
