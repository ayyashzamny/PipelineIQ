@echo off
REM DevOps Agent Setup Script for Windows

echo ================================
echo DevOps Helper Agent - Setup
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/4] Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo [2/4] Installing dependencies...
pip install -r requirements.txt --quiet

echo [3/4] Creating .env file from template...
if not exist .env (
    copy .env.example .env
    echo Created .env file - EDIT with your Gmail credentials!
)

echo [4/4] Checking configuration...
python main.py check-config

echo.
echo ================================
echo ✓ Setup Complete!
echo ================================
echo.
echo Next steps:
echo 1. Edit .env file with your Gmail credentials
echo 2. Make sure Ollama is running (ollama serve in another terminal)
echo 3. Run: python main.py run --fail-at Test
echo.
pause
