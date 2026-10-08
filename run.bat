@echo off
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python is not installed. Please install it from https://www.python.org/downloads/
    echo Tick "Add Python to PATH" during installation, then run this file again.
    pause
    exit /b
)

if not exist venv (
    echo Setting up for the first time, please wait...
    python -m venv venv
)

call venv\Scripts\activate.bat
pip install -r requirements.txt
streamlit run app.py
pause