#!/bin/bash
cd "$(dirname "$0")"

echo "======================================================"
echo "    ALGOX — Algorithm Intelligence Platform"
echo "======================================================"
echo ""

# Check for python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH."
    echo "Please install Python 3 from https://www.python.org/ or via Homebrew (brew install python3)."
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Check / create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment (venv)..."
    python3 -m venv venv
fi

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    PIP_CMD="pip"
    PYTHON_CMD="python"
else
    PIP_CMD="python3 -m pip"
    PYTHON_CMD="python3"
fi

echo "Installing / verifying dependencies from requirements.txt..."
$PIP_CMD install -r requirements.txt

echo ""
echo "======================================================"
echo "🚀 Launching ALGOX..."
echo "Local URL: http://localhost:8052"
echo "Login: admin / algox"
echo "======================================================"
echo ""

$PYTHON_CMD -m streamlit run app.py --server.port 8052
