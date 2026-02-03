#!/usr/bin/env python3
"""
Script to install backend dependencies one by one with UV package manager
"""

import subprocess
import sys
import os

def run_command(cmd):
    """Run a command and check if it succeeds"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(f"Success: {result.stdout}")
    return True

def install_with_uv():
    """Install dependencies one by one with UV"""

    # Check if UV is installed
    if not run_command("uv --version"):
        print("UV package manager not found. Installing UV...")
        if not run_command("pip install uv"):
            print("Failed to install UV. Please install it manually with 'pip install uv'")
            return False
        print("UV installed successfully!")

    # Change to backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"Changed to directory: {os.getcwd()}")

    # Create virtual environment
    print("\n--- Creating virtual environment ---")
    if not run_command("uv venv"):
        print("Failed to create virtual environment")
        return False

    # Activate virtual environment and install dependencies one by one
    dependencies = [
        "fastapi>=0.115.0",
        "sqlmodel>=0.0.22",
        "pydantic>=2.8.0",
        "pydantic-settings>=2.0.0",
        "uvicorn>=0.30.0",
        "asyncpg>=0.29.0",
        "bcrypt>=4.0.0",
        "pyjwt>=2.8.0",
        "python-multipart>=0.0.9",
        "python-dotenv>=1.0.0",
        "alembic>=1.13.0",
        "sqlalchemy>=2.0.0",
        "httpx>=0.27.0"
    ]

    print("\n--- Installing dependencies one by one ---")
    for dep in dependencies:
        print(f"\nInstalling {dep}...")
        if not run_command(f"uv pip install '{dep}'"):
            print(f"Failed to install {dep}")
            return False
        print(f"Successfully installed {dep}")

    print("\n--- All dependencies installed successfully! ---")
    print("\nTo activate the virtual environment, run:")
    print("  source .venv/Scripts/activate    # On Windows")
    print("  source .venv/bin/activate        # On macOS/Linux")
    print("\nThen you can run the application with:")
    print("  uvicorn src.main:app --reload --host 0.0.0.0 --port 8000")

    return True

if __name__ == "__main__":
    print("Installing TaskFlow AI Backend dependencies with UV package manager...")
    success = install_with_uv()
    if success:
        print("\n✅ Installation completed successfully!")
    else:
        print("\n❌ Installation failed!")
        sys.exit(1)