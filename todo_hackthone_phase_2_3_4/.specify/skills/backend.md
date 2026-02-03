# Backend Implementation Skill

**Purpose**: Implement FastAPI routes, SQLModel models, services, and backend infrastructure
**Coverage**: Phase 2-5 (T007-T049) - Database, models, services, API endpoints
**Project**: Phase II Full-Stack Web Application

---

## Skill Description

This skill handles all backend implementation tasks for the Phase II Todo Application. It creates FastAPI routes, SQLModel database models, service layer logic, and backend infrastructure including:

- Database connection and async engine configuration
- SQLModel models (User, Task) with proper constraints
- Alembic database migrations
- JWT authentication and authorization
- Service layer with business logic
- RESTful API endpoints with proper error handling
- CORS and middleware configuration
- Structured JSON logging with correlation IDs

---

## Usage

### Basic Usage
```
/backend
```

### With Specific Task
```
/backend T007
```

### With Multiple Tasks
```
/backend T008 T009
```

---

## Implementation Guidelines

### Technology Stack

- **Framework**: FastAPI 0.115+
- **ORM**: SQLModel 0.0.22+
- **Database**: PostgreSQL 16+ (Neon)
- **Driver**: asyncpg (async PostgreSQL driver)
- **Auth**: JWT tokens with bcrypt hashing
- **Logging**: Structured JSON with correlation IDs

### Code Standards

- Follow PEP 8 style guide
- Use type hints for all functions
- Include inline comments referencing Task IDs
- Never log passwords or sensitive data
- Use async/await for all database operations
- Proper HTTP status codes (401, 403, 404, 400, 409, 500)

### Security Requirements

- All passwords hashed with bcrypt 12+ rounds
- JWT tokens use HS256 algorithm with 7-day expiration
- User isolation enforced at query level
- No raw SQL queries (ORM only)
- CORS restricted to specific frontend origin
- Secrets in environment variables only

---

## Supported Tasks

### Phase 2: Foundational (T007-T017)

**T007**: Database Engine Configuration
- File: `backend/src/core/database.py`
- Async SQLModel with asyncpg driver
- Connection pooling (pool_size=10, max_overflow=10)
- Dependency injection for FastAPI routes

**T008**: User Model
- File: `backend/src/models/user.py`
- UUID primary key
- Unique email with index
- Bcrypt password hash
- Auto-generated created_at timestamp

**T009**: Task Model
- File: `backend/src/models/task.py`
- Integer primary key (auto-increment)
- Foreign key to users with CASCADE DELETE
- Title (1-200 chars), description (max 1000 chars)
- Completed boolean with index
- Auto-generated created_at, updated_at

**T010**: Alembic Initialization
- File: `backend/alembic.ini`
- Directory: `backend/alembic/versions/`
- Configuration for PostgreSQL migrations

**T011**: Initial Migration
- File: `backend/alembic/versions/001_initial_schema.py`
- Users table with constraints and indexes
- Tasks table with foreign key and indexes
- CASCADE DELETE on user_id foreign key

**T012**: Structured Logging
- File: `backend/src/core/logging.py`
- JSON format logs
- Correlation ID per request
- Never log passwords, tokens, or PII
- Fields: timestamp, level, correlation_id, user_id, endpoint, status_code, duration_ms

**T013**: CORS Middleware
- File: `backend/src/core/config.py`
- Restrict to FRONTEND_URL (no wildcards)
- AllowCredentials: True (for cookies)
- Proper headers: Content-Type, Authorization

**T014**: Global Error Handling
- File: `backend/src/core/exceptions.py`
- HTTP status code mapping
- User-friendly error messages
- Never expose stack traces or internal details

**T015**: JWT Verification
- File: `backend/src/core/security.py`
- Decode JWT token
- Extract user_id from `sub` claim
- Validate expiration
- Raise 401 if invalid/expired

**T016**: Password Hashing
- File: `backend/src/core/security.py`
- Hash with bcrypt 12+ rounds
- Verify password hashes
- Never log passwords

**T017**: FastAPI App Entry Point
- File: `backend/src/main.py`
- Middleware stack: CORS → Logging → Error Handler
- Router mounting (/api routes)
- Health check endpoint (/health)
- OpenAPI documentation (/docs)

### Phase 3: User Story 1 - Authentication (T021-T026)

**T021-T022**: AuthService
- File: `backend/src/services/auth_service.py`
- hash_password(): bcrypt 12+ rounds
- verify_password(): bcrypt comparison
- create_jwt(): Generate token with sub=user_id, email, iat, exp (7 days)

**T023**: Register Endpoint
- Route: `POST /api/auth/register`
- Validate email format (RFC 5322)
- Validate password length (min 8 chars)
- Check for duplicate email (409 Conflict)
- Hash password, create user, return 201

**T024**: Login Endpoint
- Route: `POST /api/auth/login`
- Verify credentials
- Generate JWT token
- Set HTTP-only cookie: token=<jwt>; HttpOnly; Secure; SameSite=Strict; Max-Age=604800
- Return 200 with user info

**T025**: Logout Endpoint
- Route: `POST /api/auth/logout`
- Clear JWT cookie
- Return 200

**T026**: Session Endpoint
- Route: `GET /api/auth/session`
- Return user info if authenticated
- Return 401 if not authenticated

### Phase 4: User Story 2 - Task Management (T033-T040)

**T033**: TaskService
- File: `backend/src/services/task_service.py`
- create_task(user_id, title, description)
- list_tasks(user_id, completed=None)
- get_task(user_id, task_id)
- update_task(user_id, task_id, title=None, description=None)
- delete_task(user_id, task_id)
- toggle_complete(user_id, task_id)
- All methods enforce user_id in queries

**T034**: User ID Validation Middleware
- File: `backend/src/api/deps.py`
- Extract user_id from JWT
- Verify: token.sub == request.path.user_id
- Raise 403 Forbidden if mismatch

**T035**: List Tasks Endpoint
- Route: `GET /api/{user_id}/tasks`
- Auth required
- User ID validation
- Return only authenticated user's tasks
- Order by created_at DESC
- 401/403/500 responses

**T036**: Create Task Endpoint
- Route: `POST /api/{user_id}/tasks`
- Auth required
- User ID validation
- Create task for authenticated user
- Validate title (1-200 chars), description (max 1000 chars)
- 201/400/401/403/404/500 responses

**T037**: Get Task Endpoint
- Route: `GET /api/{user_id}/tasks/{id}`
- Auth required
- User ID validation
- Return task if owned by user
- 401/403/404/500 responses

**T038**: Update Task Endpoint
- Route: `PUT /api/{user_id}/tasks/{id}`
- Auth required
- User ID validation
- Update task if owned by user
- Update title and/or description
- Auto-update updated_at
- 200/400/401/403/404/500 responses

**T039**: Toggle Complete Endpoint
- Route: `PATCH /api/{user_id}/tasks/{id}/complete`
- Auth required
- User ID validation
- Toggle completed status
- Auto-update updated_at
- 200/401/403/404/500 responses

**T040**: Delete Task Endpoint
- Route: `DELETE /api/{user_id}/tasks/{id}`
- Auth required
- User ID validation
- Delete task if owned by user
- 200/401/403/404/500 responses

### Phase 5: User Story 3 - Persistence (T050-T053)

**T050-T051**: Timestamp Verification
- Verify task queries include ORDER BY created_at DESC
- Verify task updates set updated_at timestamp

**T052**: Cascade Delete Verification
- Verify migration includes CASCADE DELETE
- Foreign key: REFERENCES users(id) ON DELETE CASCADE

**T053**: Connection Retry Logic
- File: `backend/src/core/database.py`
- Retry on connection failures
- Exponential backoff
- Max retry attempts

### Phase 6: Health Check (T057)

**T057**: Health Check Endpoint
- File: `backend/src/api/routes/health.py`
- Route: `GET /health`
- No auth required
- Return: status, database connectivity, environment, timestamp
- 200/503 responses

---

## Examples

### Example 1: Implement Database Engine
```
User: /backend T007

Output:
- Creates backend/src/core/database.py
- Configures async SQLModel with asyncpg
- Sets connection pooling (pool_size=10, max_overflow=10)
- Provides FastAPI dependency injection
```

### Example 2: Implement Task Endpoints
```
User: /backend T035 T036 T037

Output:
- Creates task endpoints in backend/src/api/routes/tasks.py
- Implements GET, POST, and individual task GET
- All with JWT auth and user ID validation
- Proper error handling and status codes
```

### Example 3: Implement Complete TaskService
```
User: /backend T033

Output:
- Creates backend/src/services/task_service.py
- Implements all CRUD methods
- Enforces user_id in all queries
- Proper error handling
```

---

## Dependencies

### Required Files
- `specs/001-full-stack-web/spec.md` - Feature requirements
- `specs/001-full-stack-web/plan.md` - Implementation plan
- `specs/001-full-stack-web/data-model.md` - Entity definitions
- `specs/001-full-stack-web/contracts/` - API contracts

### Required Environment Variables
- `DATABASE_URL` - PostgreSQL connection string
- `JWT_SECRET` - JWT signing secret (256+ bits)
- `JWT_ALGORITHM` - HS256
- `JWT_EXPIRATION_DAYS` - 7
- `FRONTEND_URL` - Frontend origin for CORS
- `LOG_LEVEL` - INFO, WARNING, ERROR
- `ENVIRONMENT` - development or production

---

## Validation Checklist

After implementing backend tasks, verify:

### Database
- [ ] Database connection succeeds
- [ ] Users table created with UNIQUE(email)
- [ ] Tasks table created with owner_user_id FK
- [ ] CASCADE DELETE configured on owner_user_id FK
- [ ] Indexes created: idx_users_email, idx_tasks_owner_user_id, idx_tasks_completed

### Security
- [ ] Passwords hashed with bcrypt 12+ rounds
- [ ] JWT tokens expire after 7 days
- [ ] JWT secret stored in environment variable
- [ ] CORS restricted to specific frontend origin
- [ ] No raw SQL queries used

### API
- [ ] All endpoints return proper HTTP status codes
- [ ] Error messages don't expose internal details
- [ ] Structured JSON logs with correlation IDs
- [ ] OpenAPI docs accessible at /docs
- [ ] /health endpoint accessible without auth

### User Isolation
- [ ] User ID validation middleware active
- [ ] All task queries filter by user_id
- [ ] Token user_id must match URL user_id

---

## Notes

- All backend code must reference Task IDs in comments
- Never manually modify generated code
- Follow exact technology versions from Constitution
- Test each endpoint independently
- Run migrations before starting server
- Check logs for structured JSON output
