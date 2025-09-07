@echo off
REM Typing Racer Game - Windows Run Script

echo 🏁 Starting Typing Racer Game...

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Please install Python 3.9 or higher.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if pip is available  
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip not found! Please make sure pip is installed with Python.
    pause
    exit /b 1
)

REM Install requirements if not already installed
python -c "import pygame" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing requirements...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install requirements!
        pause
        exit /b 1
    )
)

REM Run the game
echo 🚗 Launching game...
python main.py

echo 👋 Thanks for playing!
pause