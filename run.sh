#!/bin/bash
cd "$(dirname "$0")"

echo "Installing / verifying dependencies..."
python3 -m pip install -r requirements.txt

echo "Starting ALGOX on port 8052..."
echo "Credentials: admin / algox"
python3 -m streamlit run app.py --server.port 8052
