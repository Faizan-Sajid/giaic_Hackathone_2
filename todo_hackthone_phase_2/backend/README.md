# TaskFlow AI Backend

## Setup Instructions

### Prerequisites
- Python 3.13+
- UV package manager installed

### Installation

1. **Install UV package manager (if not already installed):**
```bash
pip install uv
```

2. **Create virtual environment and install dependencies:**
```bash
# Navigate to the backend directory
cd backend

# Create and activate virtual environment with UV
uv venv

# Activate the virtual environment
# On Windows:
source .venv/Scripts/activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies with UV
uv pip install -r requirements.txt
```

Alternatively, you can install directly with UV:
```bash
# Install all dependencies at once
uv pip install fastapi>=0.115.0 sqlmodel>=0.0.22 pydantic>=2.8.0 pydantic-settings>=2.0.0 uvicorn>=0.30.0 asyncpg>=0.29.0 bcrypt>=4.0.0 pyjwt>=2.8.0 python-multipart>=0.0.9 python-dotenv>=1.0.0 alembic>=1.13.0 sqlalchemy>=2.0.0 httpx>=0.27.0
```

3. **Set up environment variables:**
Copy the example environment file and update the values:
```bash
cp .env.example .env
```

Edit the `.env` file with your actual database connection details and a strong JWT secret.

4. **Run the application:**
```bash
# Activate the virtual environment (if not already activated)
source .venv/Scripts/activate  # Windows
# or
source .venv/bin/activate      # macOS/Linux

# Run the backend server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at `http://localhost:8000` with documentation at `http://localhost:8000/docs`.

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (e.g., `postgresql+asyncpg://user:pass@localhost:5432/taskflow_db`)
- `JWT_SECRET`: Secret key for JWT token signing (minimum 32 characters)
- `FRONTEND_URL`: URL of the frontend application for CORS (e.g., `http://localhost:3000`)
- `DB_POOL_SIZE`: Database connection pool size (default: 10)
- `DB_MAX_OVERFLOW`: Database connection pool overflow (default: 10)
- `BCRYPT_ROUNDS`: Number of bcrypt rounds for password hashing (default: 12)
- `DEBUG`: Enable debug mode (default: true)