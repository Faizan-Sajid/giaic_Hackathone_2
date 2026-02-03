# Environment Variables Configuration Guide

## Frontend (Next.js) Environment Variables

These variables should be set in your Vercel deployment settings under "Environment Variables":

### Required Variables
```
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
```

### Example for Development
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Example for Production
```
NEXT_PUBLIC_API_URL=https://your-backend-production-url.com
```

## Backend (FastAPI) Environment Variables

These variables should be set in your backend deployment environment:

### Required Variables
```
DATABASE_URL=postgresql://username:password@host:port/database_name
JWT_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random-32-chars-minimum
FRONTEND_URL=https://your-frontend-domain.vercel.app
GEMINI_API_KEY=your-gemini-api-key-here
```

### Optional Variables with Defaults
```
JWT_ALGORITHM=HS256
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=10
BCRYPT_ROUNDS=12
ENVIRONMENT=production
LOG_LEVEL=INFO
```

## Setting Up Environment Variables in Vercel

### For Frontend Deployment:
1. Go to your Vercel project dashboard
2. Navigate to Settings → Environment Variables
3. Add the following variables:

| Key | Value |
|-----|-------|
| NEXT_PUBLIC_API_URL | Your backend API URL |

### For Backend Deployment:
The backend environment variables should be set in your backend hosting environment (whether that's Vercel Functions, separate server, or cloud provider).

## Important Notes

1. **Frontend Variables**: Only variables prefixed with `NEXT_PUBLIC_` are available to the client-side code
2. **Secret Keys**: Never expose sensitive keys (like JWT_SECRET, database credentials) in frontend environment variables
3. **API URLs**: Always use the deployed backend URL in production, not localhost
4. **Database**: For production, use a managed PostgreSQL service (AWS RDS, Supabase, Neon, etc.)

## Sample .env.local for Development

### Frontend (./frontend/.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Backend (./backend/.env)
```
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/taskflow_db
JWT_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random-32-chars-minimum
JWT_ALGORITHM=HS256
FRONTEND_URL=http://localhost:3000
GEMINI_API_KEY=your-gemini-api-key-here
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=10
BCRYPT_ROUNDS=12
ENVIRONMENT=development
LOG_LEVEL=DEBUG
```

## Vercel CLI Commands for Environment Variables

To set environment variables using Vercel CLI:
```bash
vercel env add NEXT_PUBLIC_API_URL production
# Then enter your backend API URL when prompted
```

To list current environment variables:
```bash
vercel env ls
```

Remember to set these for each environment (development, preview, production) as needed.