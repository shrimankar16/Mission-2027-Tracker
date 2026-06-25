@echo off
echo ========================================
echo Career Command Center - Mission 2027
echo ========================================
echo.
echo Starting application...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found. Creating...
    python -m venv venv
    echo Installing dependencies...
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

REM Run the Streamlit app
streamlit run app.py

pause
