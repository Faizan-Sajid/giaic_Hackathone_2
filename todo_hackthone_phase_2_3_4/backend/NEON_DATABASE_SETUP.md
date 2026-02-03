# Neon Database Setup Guide

## Step 1: Create Neon Account & Database

1. Go to: https://console.neon.tech
2. Sign up/Login
3. Create new project:
   - Click "New Project"
   - Name: `taskflow` (or any name)
   - Region: Choose nearest to you (US East 2 recommended)
   - Click "Create Project"

## Step 2: Get Database Connection String

1. After project creation, click on your project
2. Find "Connection Details" or "Connection Strings"
3. Copy the connection string in this format:
   ```
   postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
   ```

## Step 3: Update Backend .env File

Open `backend/.env` and replace `DATABASE_URL` with your Neon connection string:

```bash
# Database Configuration - Neon PostgreSQL (Cloud Database)
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

### Important: Update Connection String to Use asyncpg

Neon's connection string starts with `postgresql://` but we need `postgresql+asyncpg://` for async support.

**Example conversion:**

Neon provides:
```
postgresql://username:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

Change to:
```
postgresql+asyncpg://username:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
```

## Step 4: Start Backend

```bash
cd backend
.venv\Scripts\activate
uvicorn src.main:app --reload
```

## Step 5: Run Database Initialization

The backend will automatically create tables on startup. You should see:
```
✓ Database initialized
INFO:     Uvicorn running on http://127.0.0.1:8000
```

## Troubleshooting

### Error: "no pg_hba.conf entry for host"
**Solution**: Make sure DATABASE_URL includes `?sslmode=require` or `?sslmode=require` at the end

### Error: "FATAL: password authentication failed"
**Solution**: Double-check username and password are correct in connection string

### Error: "could not translate host name"
**Solution**: Ensure you have internet connection (Neon is a cloud service)

### Connection string not working?
Try using Neon's "Raw" connection string format without extra parameters.

## Neon Dashboard Useful Features

- **SQL Editor**: Run SQL queries directly in browser
- **Tables**: View created tables and data
- **Connection Pooling**: Neon handles this automatically
- **Backup**: Automatic backups included
- **Branching**: Create dev/staging branches (Pro feature)

## Recommended Environment Variables for Neon

```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.aws.neon.tech/neondb?sslmode=require

# Database Connection Pooling (Neon handles, but we can override)
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=10

# JWT Configuration
JWT_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random-32-chars-minimum
JWT_ALGORITHM=HS256

# Frontend Configuration
FRONTEND_URL=http://localhost:3000

# Bcrypt Configuration
BCRYPT_ROUNDS=12

# Development Settings
DEBUG=true
```

## Next Steps After Setup

1. Backend starts successfully ✓
2. Test registration: `POST http://127.0.0.1:8000/api/auth/register`
3. Test login: `POST http://127.0.0.1:8000/api/auth/login`
4. View API docs: `http://127.0.0.1:8000/docs`
5. Check database tables in Neon dashboard
