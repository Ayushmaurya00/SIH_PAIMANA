@echo off
title PAIMANA AI - Codebase Text Bundler
color 0A

:: Ensure working directory is project root
cd /d "%~dp0"

echo ======================================================================
echo    PAIMANA AI - Complete Codebase Text Bundler (.txt)
echo    Ministry of Statistics and Programme Implementation (MoSPI)
echo ======================================================================
echo.

:: 1. Comprehensive Python Detection (matching start.bat)
set PYTHON_CMD=

if exist ".venv\Scripts\python.exe" (
    set PYTHON_CMD=".venv\Scripts\python.exe"
) else if exist "venv\Scripts\python.exe" (
    set PYTHON_CMD="venv\Scripts\python.exe"
) else if exist "%APPDATA%\uv\python\cpython-3.11-windows-x86_64-none\python.exe" (
    set PYTHON_CMD="%APPDATA%\uv\python\cpython-3.11-windows-x86_64-none\python.exe"
) else if exist "%APPDATA%\uv\python\cpython-3.11.16-windows-x86_64-none\python.exe" (
    set PYTHON_CMD="%APPDATA%\uv\python\cpython-3.11.16-windows-x86_64-none\python.exe"
) else if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
) else if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
) else if exist "%LOCALAPPDATA%\Programs\Python\Python310\python.exe" (
    set PYTHON_CMD="%LOCALAPPDATA%\Programs\Python\Python310\python.exe"
) else if exist "%LOCALAPPDATA%\Python\bin\python.exe" (
    set PYTHON_CMD="%LOCALAPPDATA%\Python\bin\python.exe"
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        set PYTHON_CMD=python
    ) else (
        where py >nul 2>&1
        if %ERRORLEVEL% equ 0 (
            set PYTHON_CMD=py
        )
    )
)

if defined PYTHON_CMD (
    echo [OK] Using Python: %PYTHON_CMD%
    echo [INFO] Generating complete codebase text bundle...
    echo.
    %PYTHON_CMD% scripts\export_codebase.py
) else (
    echo [INFO] Python executable not detected, using PowerShell Bundler...
    powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\export_codebase.ps1"
)

:: 2. Completion notice
echo.
echo ======================================================================
echo    Done! File generated directly in project root:
echo    PAIMANA_AI_CODE_BUNDLE.txt
echo ======================================================================
echo.
pause
