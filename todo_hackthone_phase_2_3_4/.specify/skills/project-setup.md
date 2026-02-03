# Project Setup Skill

**Purpose**: Initialize project structure, dependencies, and configuration
**Coverage**: Phase 1 (T001-T006) - Complete project setup
**Project**: Phase II Full-Stack Web Application

---

## Skill Description

This skill handles all project setup tasks for Phase II Todo Application. It creates directory structure, configuration files, and dependency specifications for both backend and frontend including:

- Backend directory structure (models, API routes, core, tests)
- Frontend directory structure (App Router, components, pages, lib)
- Python backend dependencies (pyproject.toml)
- Node.js frontend dependencies (package.json)
- Environment configuration (.env.example files)
- TypeScript configuration (tsconfig.json)
- Alembic configuration for database migrations
- Better Auth configuration for frontend

---

## Usage

### Basic Usage
```
/project-setup
```

### With Specific Task
```
/project-setup T001
```

### With Multiple Tasks
```
/project-setup T001 T002 T003
```

---

## Implementation Guidelines

### Technology Stack

**Backend**:
- **Language**: Python 3.13+
- **Package Manager**: UV (fast Python package installer)
- **Framework**: FastAPI 0.115+
- **ORM**: SQLModel 0.0.22+
- **Database**: PostgreSQL 16+ (Neon)

**Frontend**:
- **Framework**: Next.js 15+ with App Router
- **Language**: TypeScript 5.7+ (strict mode)
- **Package Manager**: npm or yarn
- **UI Library**: React 18+
- **Styling**: Tailwind CSS
- **Auth**: Better Auth 1.0+

---

## Supported Tasks

### T001: Backend Directory Structure

**Create**:
```bash
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── task.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── tasks.py
│   │   │   └── health.py
│   │   └── deps.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── logging.py
│   │   ├── config.py
│   │   └── exceptions.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py
│   │   └── task_service.py
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_auth.py
│   │   └── test_tasks.py
│   └── integration/
│       ├── test_auth_flow.py
│       └── test_task_api.py
└── alembic/
    └── versions/
```

**Files to Create**:
- All `__init__.py` files (empty or with imports)
- All module files (initially empty or with basic structure)

### T002: Backend Dependencies

**File**: `backend/pyproject.toml`

```toml
[project]
name = "todo-backend"
version = "0.1.0"
description = "Phase II Todo Application Backend"
requires-python = ">=3.13"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.24.0",
    "sqlmodel>=0.0.22",
    "asyncpg>=0.29.0",
    "python-jose[cryptography]>=3.3.0",
    "bcrypt>=4.1.0",
    "alembic>=1.13.0",
    "pydantic>=2.5.0",
    "python-multipart>=0.0.6",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "httpx>=0.24.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src"]
```

### T003: Frontend Directory Structure

**Create**:
```bash
frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── layout.tsx
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── register/
│   │   │       └── page.tsx
│   │   ├── (dashboard)/
│   │   │   ├── layout.tsx
│   │   │   └── tasks/
│   │   │       └── page.tsx
│   │   ├── api/
│   │   │   └── client.ts
│   │   ├── components/
│   │   │   ├── ProtectedRoute.tsx
│   │   │   ├── TaskList.tsx
│   │   │   └── TaskForm.tsx
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx
│   │   ├── lib/
│   │   │   └── api/
│   │   │       └── client.ts
│   │   └── layout.tsx
│   └── middleware.ts
├── tests/
│   ├── e2e/
│   │   └── user-journey.spec.ts
│   └── unit/
│       └── test-utils.tsx
└── public/
```

### T004: Frontend Dependencies

**File**: `frontend/package.json`

```json
{
  "name": "todo-frontend",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "test": "jest",
    "test:e2e": "playwright test"
  },
  "dependencies": {
    "next": "^15.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "typescript": "^5.7.0",
    "better-auth": "^1.0.0",
    "tailwindcss": "^3.4.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "@types/react": "^18.0.0",
    "@types/react-dom": "^18.0.0",
    "jest": "^29.7.0",
    "@playwright/test": "^1.40.0"
  }
}
```

### T005: Backend Environment Configuration

**File**: `backend/.env.example`

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db?sslmode=require

# JWT Configuration
JWT_SECRET=your-secret-key-min-256-bits-generate-with-openssl-rand-hex-32
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# CORS Configuration
FRONTEND_URL=http://localhost:3000

# Logging Configuration
LOG_LEVEL=INFO
ENVIRONMENT=development

# Better Auth Configuration (shared with frontend)
BETTER_AUTH_SECRET=your-secret-key-min-256-bits
```

**Instructions**:
```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env with your values
# Generate JWT secret with:
openssl rand -hex 32
```

### T006: Frontend Environment Configuration

**File**: `frontend/.env.example`

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
BETTER_AUTH_SECRET=your-secret-key-min-256-bits
BETTER_AUTH_URL=http://localhost:3000
```

**Instructions**:
```bash
# Copy .env.example to .env.local
cp .env.example .env.local

# Edit .env.local with your values
```

---

## Setup Commands

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment with UV
uv venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
uv pip install -e .

# Copy environment file
cp .env.example .env

# Edit .env with your configuration
notepad .env
```

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env.local

# Edit .env.local with your configuration
notepad .env.local
```

---

## Verification Checklist

After completing project setup, verify:

### Backend Setup
- [ ] All directories created (models, api/routes, core, services, tests, alembic)
- [ ] All `__init__.py` files created
- [ ] `pyproject.toml` created with all dependencies
- [ ] Virtual environment created with UV
- [ ] Dependencies installed (`uv pip list`)
- [ ] `.env.example` file created
- [ ] `.env` file created and configured

### Frontend Setup
- [ ] All directories created (app, components, contexts, lib, tests)
- [ ] `package.json` created with all dependencies
- [ ] Dependencies installed (`npm list --depth=0`)
- [ ] `.env.example` file created
- [ ] `.env.local` file created and configured
- [ ] TypeScript configuration created (tsconfig.json)
- [ ] Tailwind CSS configured

### Configuration
- [ ] DATABASE_URL configured in backend/.env
- [ ] JWT_SECRET generated (256+ bits)
- [ ] FRONTEND_URL matches frontend URL
- [ ] NEXT_PUBLIC_API_URL matches backend URL
- [ ] BETTER_AUTH_SECRET matches backend JWT_SECRET

---

## Common Issues & Solutions

### Issue: UV Not Installed

**Problem**: `uv: command not found`

**Solution**:
```bash
# Install UV
pip install uv
```

### Issue: Node.js Version Too Old

**Problem**: Next.js 15+ requires Node.js 18+

**Solution**:
```bash
# Check version
node --version

# Upgrade with nvm
nvm install 20
nvm use 20
```

### Issue: TypeScript Configuration Missing

**Problem**: `tsconfig.json not found`

**Solution**: Next.js generates it automatically on first run
```bash
npm run dev
# tsconfig.json will be created
```

### Issue: Environment Variables Not Loading

**Problem**: `process.env` values undefined

**Solution**:
- Backend: Ensure `.env` file exists in backend directory
- Frontend: Use `NEXT_PUBLIC_` prefix for client-side access

---

## Notes

- All setup files must reference Task IDs in comments
- Never commit `.env` or `.env.local` files to version control
- Only commit `.env.example` files
- Generate JWT secret with `openssl rand -hex 32` (256 bits)
- Ensure DATABASE_URL includes `?sslmode=require` for TLS
- Verify all dependencies are correct versions
- Test project startup after setup
- Check that both backend and frontend can start successfully
