#!/bin/bash
# Startup script for Prometheus Recruitment API Server (Linux/Mac)

echo "========================================"
echo "Prometheus Recruitment API Server"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[1/3] Checking Python installation..."
python3 --version
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[2/3] Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created successfully!"
else
    echo "[2/3] Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "[3/3] Installing dependencies..."
pip install -r requirements.txt
echo ""

echo "========================================"
echo "Starting API Server..."
echo "========================================"
echo "Server URL: http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo "ReDoc: http://localhost:8000/redoc"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python main.py
