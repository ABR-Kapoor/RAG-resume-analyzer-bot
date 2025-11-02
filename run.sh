#!/bin/bash

echo "========================================"
echo " Starting Noddy Bot - Resume Analyzer"
echo "========================================"
echo

# Check if .env exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found!"
    echo "Please copy .env.example to .env and add your API keys"
    exit 1
fi

echo "Starting Streamlit application..."
echo "App will open at: http://localhost:8502"
echo
echo "Press Ctrl+C to stop the server"
echo

python -m streamlit run app.py --server.port 8502
