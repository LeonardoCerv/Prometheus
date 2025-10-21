@echo off
REM Startup script for Prometheus Recruitment API Server (Windows)

echo ========================================
echo Prometheus Recruitment API Server
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [1/3] Checking Python installation...
python --version
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [2/3] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created successfully!
) else (
    echo [2/3] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo [3/3] Installing dependencies...
pip install -r requirements.txt
echo.

echo ========================================
echo Starting API Server...
echo ========================================
echo Server URL: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo ReDoc: http://localhost:8000/redoc
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python main.py
