#!/bin/bash
# DevOps Agent Setup Script for macOS/Linux

echo "================================"
echo "DevOps Helper Agent - Setup"
echo "================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed"
    echo "Install: brew install python3 (macOS) or apt-get install python3 (Ubuntu)"
    exit 1
fi

echo "[1/4] Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[2/4] Installing dependencies..."
pip install -r requirements.txt -q

echo "[3/4] Creating .env file from template..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file - EDIT with your Gmail credentials!"
fi

echo "[4/4] Checking configuration..."
python main.py check-config

echo
echo "================================"
echo "✓ Setup Complete!"
echo "================================"
echo
echo "Next steps:"
echo "1. Edit .env file with your Gmail credentials"
echo "2. Make sure Ollama is running (ollama serve in another terminal)"
echo "3. Run: python main.py run --fail-at Test"
echo
