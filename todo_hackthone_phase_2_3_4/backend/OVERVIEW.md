# Backend Overview

## FastAPI Structure and API Routes

The backend is built using FastAPI with a modular architecture. The main application is defined in `src/main.py`.

### Application Configuration
- **Title**: "TaskFlow Todo API"
- **Description**: "Phase II Full-Stack Web Application with JWT Authentication"
- **Version**: "1.0.0"
- **Documentation**: Available at `/docs` and `/redoc`

### Middleware Stack
The middleware is applied in the following order:
1. **CORS Middleware**: Configured to allow only `https://giaic-hackathone-2.vercel.app` origin with credentials enabled
2. **Request ID/Correlation ID Middleware**: For structured logging and request tracking
3. **Error Handler Middleware**: Centralized error handling
4. **JWT Authentication Middleware**: For protected routes (implicitly applied via dependencies)

### API Routes
The application includes three main router groups mounted under `/api`:

#### Authentication Routes (`/api/auth`)
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login with JWT cookie setting
- `POST /api/auth/logout` - Session invalidation
- `GET /api/auth/session` - Session validation and user info retrieval

#### Task Routes (`/api/{user_id}/tasks`)
- `GET /api/{user_id}/tasks` - List user's tasks
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{task_id}` - Get specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete task

#### Health Check Route (`/`)
- `GET /` - Root endpoint providing API information

## Database Models (SQLModel) and Neon Connection Setup

### Database Configuration (`src/core/database.py`)
- **Engine**: Async SQLAlchemy engine with SQLModel
- **Connection Pool**: Configured with:
  - `pool_size`: 10 connections (configurable via `DB_POOL_SIZE` env var)
  - `max_overflow`: 10 additional connections (configurable via `DB_MAX_OVERFLOW` env var)
  - `pool_pre_ping`: Enabled for connection validation
  - `pool_recycle`: 3600 seconds (1 hour) to prevent connection rot
- **URL**: Retrieved from `DATABASE_URL` environment variable
- **Echo**: Disabled in production for security

### Database Models

#### User Model (`src/models/user.py`)
- **Primary Key**: `id` (UUID string, auto-generated)
- **Fields**:
  - `email` (string, unique, indexed, max 255 chars)
  - `password_hash` (string, bcrypt hashed)
  - `created_at` (datetime, auto-generated)
- **Relationships**: One-to-many with Task model (user has many tasks)

#### Task Model (`src/models/task.py`)
- **Primary Key**: `id` (integer, auto-increment)
- **Fields**:
  - `owner_user_id` (string, foreign key to user.id)
  - `title` (string, 1-200 characters, required)
  - `description` (string, optional, max 1000 characters)
  - `completed` (boolean, default false, indexed)
  - `created_at` (datetime, auto-generated)
  - `updated_at` (datetime, auto-generated)
- **Relationships**: Many-to-one with User model (task belongs to user)
- **Constraints**: Cascade delete on user deletion

## Authentication Middleware and JWT Handling

### Security Module (`src/core/security.py`)
- **JWT Creation**: `create_jwt(user_id, email?)` - Creates JWT with 7-day expiration
- **JWT Verification**: `verify_jwt(token)` - Verifies token and extracts user_id from 'sub' claim
- **Password Hashing**: `hash_password(password, rounds?)` - Uses bcrypt with 12+ rounds
- **Password Verification**: `verify_password(plain, hashed)` - Compares password with hash

### Authentication Flow
1. **Registration**: Email/password validated, password hashed with bcrypt, JWT cookie set
2. **Login**: Credentials verified against hashed password, JWT cookie set with HttpOnly, Secure, SameSite attributes
3. **Session Validation**: JWT token extracted from cookie, decoded and validated
4. **Logout**: JWT cookie cleared by setting expiration to past date

### JWT Configuration
- **Algorithm**: HS256 (configurable via `JWT_ALGORITHM` env var)
- **Secret**: Retrieved from `JWT_SECRET` environment variable
- **Expiration**: 7 days maximum
- **Claims**: Contains `sub` (user_id), `iat` (issued at), `exp` (expiration)
- **Storage**: HTTP-only cookies with SameSite="none", Secure=True for cross-origin compatibility

### Authorization Layers
1. **Layer 1**: JWT token presence and validity
2. **Layer 2**: URL user_id matches token user_id
3. **Layer 3**: Database queries filtered by owner_user_id for data isolation

### Security Features
- Passwords never logged or exposed
- JWT tokens stored only in HTTP-only cookies (not localStorage)
- Constant-time password comparison
- Correlation IDs for request tracing
- Structured JSON logging