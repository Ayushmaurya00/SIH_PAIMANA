@echo off
title PAIMANA AI - System Launcher
color 0B

echo ======================================================================
echo    🏛️  PAIMANA AI - Infrastructure Project Monitoring ^& Early Warning
echo    Ministry of Statistics and Programme Implementation (MoSPI)
echo ======================================================================
echo.

:: 1. Comprehensive Python Detection
set PYTHON_CMD=

:: Check local virtual environments first
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
) else (
    where python >nul 2>&1
    if %ERRORLEVEL% equ 0 (
        set PYTHON_CMD=python
    ) else (
        where py >nul 2>&1
        if %ERRORLEVEL% equ 0 (
            set PYTHON_CMD=py
        ) else (
            echo [ERROR] Python was not found on your system.
            echo Please install Python 3.10+ or UV.
            pause
            exit /b 1
        )
    )
)

echo [OK] Using Python: %PYTHON_CMD%
echo.

:: 2. Pre-flight dependency check for PyMuPDF
%PYTHON_CMD% -c "import fitz" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [INFO] Installing PyMuPDF for Flash Report parsing...
    %PYTHON_CMD% -m pip install "pymupdf>=1.23.0"
)

:: 3. Launch unified cross-platform orchestrator
%PYTHON_CMD% scripts/run_system.py
pause
