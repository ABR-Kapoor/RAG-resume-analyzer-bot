@echo off
echo ========================================
echo  Starting Noddy Bot - Resume Analyzer
echo ========================================
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo Please copy .env.example to .env and add your API keys
    pause
    exit /b 1
)

echo Starting Streamlit application...
echo App will open at: http://localhost:8502
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
python -m streamlit run app.py --server.port 8502

pause
