#!/bin/bash
# Typing Racer Game - Unix/macOS Run Script

echo "🏁 Starting Typing Racer Game..."

# Check if Python 3 is available
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "❌ Python not found! Please install Python 3.9 or higher."
    exit 1
fi

# Check if pip is available
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "❌ pip not found! Please install pip."
    exit 1
fi

# Install requirements if not already installed
if ! $PYTHON_CMD -c "import pygame" &> /dev/null; then
    echo "📦 Installing requirements..."
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt
    else
        pip install -r requirements.txt
    fi
fi

# Run the game
echo "🚗 Launching game..."
$PYTHON_CMD main.py

echo "👋 Thanks for playing!"