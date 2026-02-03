# Quick Start Guide: Phase II Full-Stack Web Application

**Feature**: Phase II Full-Stack Web Application with JWT Authentication
**Date**: 2026-01-05
**Purpose**: Step-by-step setup guide for local development environment

---

## Prerequisites

### Required Software

| Software | Minimum Version | Purpose |
|----------|----------------|---------|
| Python | 3.13+ | Backend development |
| UV | Latest | Python package manager |
| Node.js | 22 LTS | Frontend development |
| npm | Latest | Node.js package manager |
| PostgreSQL Client | 16+ | Database client (psql) |
| Git | Latest | Version control |

### Required Accounts

| Service | Purpose | Setup Instructions |
|----------|---------|--------------------|
| Neon | PostgreSQL database | Sign up at https://neon.tech, create project, get connection string |
| Git Hosting | Code repository | GitHub, GitLab, or Bitbucket |

### System Resources

| Resource | Minimum | Recommended |
|----------|--------|-------------|
| RAM | 4 GB | 8 GB |
| Disk | 10 GB | 20 GB |
| CPU | 2 cores | 4 cores |
| Internet | Broadband | High-speed (for faster npm/pip install) |

---

## Project Setup

### 1. Clone Repository

```bash
# Clone the repository
git clone <repository-url>
cd todo_hackthone_phase_2

# Switch to feature branch
git checkout 001-full-stack-web
```

### 2. Install UV (Python Package Manager)

```bash
# Install UV (Python package manager)
pip install uv

# Verify installation
uv --version
```

### 3. Backend Setup

#### 3.1 Navigate to Backend Directory

```bash
cd backend
```

#### 3.2 Create Virtual Environment with UV

```bash
# Create virtual environment
uv venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

#### 3.3 Install Dependencies

```bash
# Install Python dependencies from pyproject.toml
uv pip install fastapi uvicorn[standard] sqlmodel asyncpg sqlalchemy[async] pydantic python-jose[cryptography] python-multipart alembic

# Verify installation
uv pip list
```

#### 3.4 Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Windows: notepad .env
# Linux/Mac: nano .env or vim .env
```

**Required Environment Variables**:
```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/dbname?sslmode=require

# JWT
JWT_SECRET=your-secret-key-min-256-bits-generate-with-openssl-rand-hex-32
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# CORS
FRONTEND_URL=http://localhost:3000

# Logging
LOG_LEVEL=INFO
ENVIRONMENT=development
```

#### 3.5 Generate JWT Secret

```bash
# Generate secure 256-bit JWT secret
openssl rand -hex 32

# Output: 64-character hexadecimal string
# Copy this to JWT_SECRET in .env file
```

**Security Warning**:
- Never commit `.env` file to version control
- Never share JWT secret publicly
- Use different secrets for development and production
- Store secrets in environment variables, not in code

#### 3.6 Initialize Database Migrations

```bash
# Initialize Alembic for database migrations
alembic init alembic

# Verify alembic.ini was created
cat alembic.ini
```

#### 3.7 Run Database Migrations

```bash
# Generate initial migration (if not exists)
alembic revision --autogenerate -m "Initial schema"

# Apply migrations to database
alembic upgrade head

# Verify tables created
# Connect to Neon database and run:
\dt
# Should show users and tasks tables
```

#### 3.7 Test Backend Connection

```bash
# Run FastAPI development server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Server starts at http://localhost:8000
# Verify:
# 1. Open http://localhost:8000/docs for OpenAPI documentation
# 2. Test health endpoint: http://localhost:8000/health
```

**Expected Output**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 4. Frontend Setup

#### 4.1 Navigate to Frontend Directory

```bash
cd frontend
```

#### 4.2 Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Verify installation
npm list --depth=0
```

#### 4.3 Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env.local

# Edit .env.local with your configuration
# Windows: notepad .env.local
# Linux/Mac: nano .env.local or vim .env.local
```

**Required Environment Variables**:
```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### 4.4 Initialize Better Auth

```bash
# Better Auth is included in npm install
# Configuration will be in src/auth.ts or .auth.ts
# See Better Auth documentation: https://better-auth.com
```

#### 4.5 Start Frontend Development Server

```bash
# Run Next.js development server
npm run dev

# Server starts at http://localhost:3000
# Should automatically open in browser
```

**Expected Output**:
```
  ▲ Next.js 15.0.0
  - Local:        http://localhost:3000

 ✓ Ready in 2.3s
```

---

## Running the Application

### 1. Start Backend

**Terminal 1**:
```bash
cd backend
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Start backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Backend is ready when**:
- Output shows "Uvicorn running on http://0.0.0.0:8000"
- http://localhost:8000/health returns: `{"status": "healthy", "database": "connected"}`
- http://localhost:8000/docs shows OpenAPI documentation

### 2. Start Frontend

**Terminal 2**:
```bash
cd frontend

# Start frontend
npm run dev
```

**Frontend is ready when**:
- Output shows "✓ Ready in Xs"
- Browser opens to http://localhost:3000
- Page renders without errors

### 3. Access Application

**Browser**: Open http://localhost:3000

**Available Pages**:
- http://localhost:3000/register - User registration
- http://localhost:3000/login - User login
- http://localhost:3000/tasks - Task dashboard (requires authentication)

---

## Testing Setup

### Backend Tests

```bash
cd backend
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install test dependencies
uv pip install pytest pytest-asyncio httpx

# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run all tests with coverage
pytest --cov=src --cov-report=html tests/

# View coverage report
# Open htmlcov/index.html in browser
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
npm run test

# Run E2E tests (requires setup)
npm run test:e2e

# Run linting
npm run lint
```

### End-to-End Test

**Manual E2E Test Flow**:

1. **Registration**:
   - Navigate to http://localhost:3000/register
   - Enter email: `test@example.com`
   - Enter password: `TestPass123`
   - Submit registration form
   - **Expected**: Redirect to login page or tasks page

2. **Login**:
   - Navigate to http://localhost:3000/login
   - Enter email: `test@example.com`
   - Enter password: `TestPass123`
   - Submit login form
   - **Expected**: Redirect to tasks page

3. **Create Task**:
   - On tasks page, click "Add Task"
   - Enter title: `Buy groceries`
   - Enter description: `Milk, eggs, bread`
   - Submit form
   - **Expected**: Task appears in task list

4. **Update Task**:
   - Click on task to edit
   - Modify title: `Buy groceries and more`
   - Submit form
   - **Expected**: Task title updated in list

5. **Complete Task**:
   - Click checkbox or toggle button to mark task complete
   - **Expected**: Task marked as completed (visual change)

6. **Delete Task**:
   - Click delete button on task
   - **Expected**: Task removed from list

7. **Logout**:
   - Click logout button
   - **Expected**: Redirected to login page

8. **Verify Session**:
   - Try to access tasks page without logging in
   - **Expected**: Redirected to login page

---

## Troubleshooting

### Common Issues

#### Backend Won't Start

**Issue**: Port 8000 already in use

**Solution**:
```bash
# Windows
netstat -ano | findstr :8000
# Kill process using PID from above command

# Linux/Mac
lsof -i :8000
kill -9 <PID>

# Or use different port
uvicorn src.main:app --reload --host 0.0.0.0 --port 8001
```

#### Frontend Won't Start

**Issue**: Port 3000 already in use

**Solution**:
```bash
# Windows
netstat -ano | findstr :3000
# Kill process using PID

# Linux/Mac
lsof -i :3000
kill -9 <PID>

# Or use different port
NEXT_PUBLIC_PORT=3001 npm run dev
```

#### Database Connection Error

**Issue**: Connection refused to Neon PostgreSQL

**Check**:
```bash
# Verify DATABASE_URL in .env
cat backend/.env | grep DATABASE_URL

# Test database connection
# Using psql client
psql <DATABASE_URL>
```

**Common Causes**:
- Invalid connection string
- Network/firewall blocking port 5432
- Neon project paused/deleted

**Solutions**:
- Verify DATABASE_URL format: `postgresql://user:pass@host:5432/dbname`
- Add `?sslmode=require` for TLS
- Check Neon console for project status

#### JWT Secret Not Set

**Issue**: JWT_SECRET environment variable missing

**Check**:
```bash
# Windows
echo %JWT_SECRET%

# Linux/Mac
echo $JWT_SECRET
```

**Solution**:
```bash
# Add to backend/.env
JWT_SECRET=<your-generated-secret>
```

#### CORS Error in Browser

**Issue**: Browser console shows CORS error

**Check**:
```bash
# Verify FRONTEND_URL in backend/.env
cat backend/.env | grep FRONTEND_URL
```

**Solution**:
```bash
# Set correct frontend origin
FRONTEND_URL=http://localhost:3000

# Restart backend for changes to take effect
```

#### Module Import Error

**Issue**: Python cannot find FastAPI, SQLModel, etc.

**Check**:
```bash
# Verify virtual environment is activated
python -c "import sys; print(sys.executable)"

# Should show path to backend/.venv/.../python.exe
```

**Solution**:
```bash
# Activate virtual environment
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Reinstall dependencies if needed
uv pip install --upgrade -r requirements.txt
```

---

## Development Workflow

### Making Changes

```bash
# Always work on feature branch
git checkout 001-full-stack-web

# Check status
git status

# Stage changes
git add .

# Commit changes
git commit -m "feat: add task update functionality"

# Push changes
git push origin 001-full-stack-web
```

### Running Tests Before Commit

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Viewing Logs

**Backend Logs**:
```bash
# Console output from uvicorn shows all requests
# Structured JSON logs with correlation IDs
```

**Frontend Logs**:
```bash
# Browser console for client-side errors
# Next.js server logs in terminal
```

---

## Production Deployment (Future - Phase IV)

### Note

Production deployment with Kubernetes and Docker is planned for Phase IV. Phase II focuses on local development with Docker Compose.

### Current Deployment Options

**Option 1: Render/Vercel**:
- Frontend: Vercel (automatic deployment)
- Backend: Render (FastAPI support)

**Option 2: Railway/Fly.io**:
- Full-stack deployment with managed databases

**Option 3: AWS/GCP/Azure**:
- Manual deployment with cloud resources

### Production Readiness

Before production deployment:

1. ✅ Remove `.env` files from repository
2. ✅ Configure production database (Neon production)
3. ✅ Generate production JWT secret
4. ✅ Set `ENVIRONMENT=production`
5. ✅ Enable HTTPS/TLS for database
6. ✅ Configure CORS to production frontend URL
7. ✅ Set `LOG_LEVEL=WARNING` (reduce verbose logging)
8. ✅ Run full test suite and ensure 80% coverage
9. ✅ Review and remove debug code
10. ✅ Set secure cookie attributes (HttpOnly, Secure, SameSite)

---

## Next Steps

1. ✅ Complete backend setup and verify health endpoint
2. ✅ Complete frontend setup and access application
3. Run manual E2E test flow (registration → login → tasks → logout)
4. Review API documentation at http://localhost:8000/docs
5. Proceed to implementation tasks in `/sp.tasks`
6. Reference detailed contracts in `/contracts/` directory

---

## Resources

### Documentation

- [TaskFlow AI Constitution](../.specify/memory/constitution.md)
- [Phase II Specification](./spec.md)
- [Implementation Plan](./plan.md)
- [Data Model](./data-model.md)
- [API Contracts](./contracts/)

### External Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [Better Auth Documentation](https://better-auth.com)
- [Neon Documentation](https://neon.tech/docs)
- [OpenAPI Specification](https://swagger.io/specification/)

### Troubleshooting

- [UV Package Manager](https://github.com/astral-sh/uv)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)
- [Pytest Testing](https://docs.pytest.org/)

---

## Support

### Common Commands

| Task | Command |
|------|---------|
| Start backend | `cd backend && .venv\Scripts\activate && uvicorn src.main:app --reload` |
| Start frontend | `cd frontend && npm run dev` |
| Run backend tests | `cd backend && pytest` |
| Run frontend tests | `cd frontend && npm test` |
| Check backend logs | `tail -f logs/backend.log` |
| Check database | `psql $DATABASE_URL -c "\dt"` |

### Getting Help

- Review Phase II specification for requirements
- Check implementation plan for architecture decisions
- Review data model and API contracts
- Refer to constitution for quality standards

---

## Summary

This quickstart guide provides:

1. ✅ Prerequisites and required software
2. ✅ Complete project setup (backend + frontend)
3. ✅ Step-by-step environment configuration
4. ✅ Instructions to start application locally
5. ✅ Testing procedures and validation
6. ✅ Troubleshooting guide for common issues
7. ✅ Development workflow best practices
8. ✅ Production deployment notes (Phase IV)

**Ready for Development**: Follow these steps to set up local development environment for Phase II.
