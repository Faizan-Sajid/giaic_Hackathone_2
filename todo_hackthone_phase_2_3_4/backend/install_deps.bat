@echo off
echo Installing TaskFlow AI Backend dependencies with UV package manager...

REM Check if UV is installed
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo UV package manager not found. Installing UV...
    pip install uv
    if %errorlevel% neq 0 (
        echo Failed to install UV. Please install it manually with 'pip install uv'
        pause
        exit /b 1
    )
    echo UV installed successfully!
)

REM Create virtual environment
echo.
echo --- Creating virtual environment ---
uv venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment
    pause
    exit /b 1
)

REM Install dependencies one by one
echo.
echo --- Installing dependencies one by one ---
set deps=fastapi>=0.115.0 sqlmodel>=0.0.22 pydantic>=2.8.0 pydantic-settings>=2.0.0 uvicorn>=0.30.0 asyncpg>=0.29.0 bcrypt>=4.0.0 pyjwt>=2.8.0 python-multipart>=0.0.9 python-dotenv>=1.0.0 alembic>=1.13.0 sqlalchemy>=2.0.0 httpx>=0.27.0

for %%d in (%deps%) do (
    echo.
    echo Installing %%d...
    uv pip install "%%d"
    if !errorlevel! neq 0 (
        echo Failed to install %%d
        pause
        exit /b 1
    )
    echo Successfully installed %%d
)

echo.
echo --- All dependencies installed successfully! ---
echo.
echo To activate the virtual environment, run:
echo   .venv\Scripts\activate
echo.
echo Then you can run the application with:
echo   uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
echo.
pause