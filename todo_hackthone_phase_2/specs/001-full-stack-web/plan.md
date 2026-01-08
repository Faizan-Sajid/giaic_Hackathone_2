# Implementation Plan: Phase II Full-Stack Web Application with JWT Authentication

**Branch**: `001-full-stack-web` | **Date**: 2026-01-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-full-stack-web/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Transform the Phase I console todo application into a production-grade, multi-user web application with stateless JWT authentication, strict data isolation, and persistent storage. The system will use FastAPI (Python) for the backend, Next.js (TypeScript) for the frontend, Better Auth for JWT management, and PostgreSQL for data persistence, complying with TaskFlow AI Constitution v1.0.0.

## Technical Context

**Language/Version**: Python 3.13+ (backend), TypeScript 5.7+ (frontend)
**Primary Dependencies**:
- Backend: FastAPI 0.115.0+, SQLModel 0.0.22+, Better Auth 1.0+, bcrypt, python-jose, uvicorn
- Frontend: Next.js 15+, React 18+, TypeScript 5.7+, Better Auth client libraries
**Storage**: PostgreSQL 16+ (Neon Serverless)
**Testing**: pytest (backend), Jest/Playwright (frontend E2E)
**Target Platform**: Web application (browser-based, responsive design)
**Project Type**: web (monorepo with `/frontend` and `/backend` directories)
**Performance Goals**:
- API response time <300ms P95 under 100 concurrent users
- Frontend page load <2 seconds
- Support 100 concurrent users without degradation
**Constraints**:
- Stateless services - no in-memory session storage
- All JWT tokens expire within 7 days
- All API endpoints (except `/health`) require authentication
- User isolation enforced at database query level
- No raw SQL - ORM only
**Scale/Scope**:
- Initial deployment for 10k users
- Monorepo structure with separate frontend and backend
- RESTful API with user-scoped routes (`/api/{user_id}/tasks`)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Core Principles Compliance

- ✅ **Spec-First Development**: All implementation will be generated from specifications. Code comments will reference Task IDs and Spec sections.
- ✅ **AI as Controlled Executor**: AI agents will be constrained by specifications, MCP tools (future phases), and explicit contracts. No direct database access by AI.
- ✅ **Determinism and Reproducibility**: System behavior will be predictable with version-pinned dependencies and explicit side effects.
- ✅ **Production-Grade Standards**: No demo shortcuts. Real-world security, authentication, and data isolation patterns will be implemented.
- ✅ **Stateless Architecture Priority**: All services will be stateless. Session data externalized via JWT tokens and database storage.

### Global Quality Standards Compliance

- ✅ **Specification Standards**: Spec already references Constitution v1.0.0 with clear acceptance criteria.
- ✅ **Implementation Standards**: Implementation will use only approved technology versions, fail-fast validation, structured logging, and inline comments.
- ✅ **Security Standards**: All endpoints enforce JWT authentication (except `/health`), bcrypt password hashing (12+ rounds), user isolation at query level, secrets in environment variables.
- ✅ **Technology Baseline**: FastAPI 0.115.0+, SQLModel 0.0.22+, PostgreSQL 16+, Next.js 15+, TypeScript 5.7+, Better Auth 1.0+.
- ✅ **Code Quality Standards**: Python will follow PEP 8 with type hints, TypeScript strict mode enabled, 80% test coverage minimum.
- ✅ **Observability Standards**: Structured JSON logging with correlation IDs, `/health` endpoint exposed.

### Phase-Specific Compliance (Phase II)

- ✅ **Technology Constraints**: Monorepo with `/frontend` and `/backend`, FastAPI 0.115+, SQLModel 0.0.22+, Python 3.13+, Next.js 15+, TypeScript 5.7+, PostgreSQL 16+, Better Auth 1.0+.
- ✅ **Authentication**: JWT only, max 7-day expiration, user_id extracted from token and validated on every request.
- ✅ **Data Security**: Passwords hashed with bcrypt 12+ rounds, user isolation enforced at query level, no raw SQL, secrets in environment variables.
- ✅ **Prohibited Practices**: No JWT in localStorage, no hardcoded secrets, no missing user_id validation, no manual SQL queries.
- ✅ **Stateless Services**: No in-memory sessions, all session data in JWT tokens or database.
- ✅ **API Requirements**: All routes under `/api`, protected routes require JWT, user_id matching enforced.
- ✅ **Frontend Requirements**: Secure HTTP-only cookies for JWT, client-side validation, authenticated/unauthenticated route separation.

### Testing Gates (Phase II)

- ✅ **Phase II Testing Requirements**: Integration tests for authentication flow, E2E test for critical user journey, no data leakage between users.

**CONSTITUTION CHECK STATUS**: ✅ PASS - All constitutional requirements satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/001-full-stack-web/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Option 2: Web application (frontend + backend)
backend/
├── src/
│   ├── models/
│   │   ├── user.py
│   │   └── task.py
│   ├── api/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   └── tasks.py
│   │   └── deps.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── logging.py
│   └── main.py
├── tests/
│   ├── unit/
│   │   ├── test_auth.py
│   │   └── test_tasks.py
│   ├── integration/
│   │   ├── test_auth_flow.py
│   │   └── test_task_api.py
│   └── conftest.py
├── pyproject.toml
├── alembic.ini
└── alembic/
    └── versions/

frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/
│   │   │   ├── login/page.tsx
│   │   │   └── register/page.tsx
│   │   ├── (dashboard)/
│   │   │   ├── tasks/page.tsx
│   │   │   └── layout.tsx
│   │   ├── api/
│   │   │   └── client.ts
│   │   ├── components/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── ProtectedRoute.tsx
│   │   └── lib/
│   │       └── utils.ts
│   └── middleware.ts
├── tests/
│   ├── e2e/
│   │   └── user-journey.spec.ts
│   └── unit/
│       └── test-utils.tsx
├── package.json
├── tsconfig.json
└── next.config.js
```

**Structure Decision**: Monorepo with separate `/frontend` and `/backend` directories, enabling independent development, testing, and deployment of each component while maintaining shared specification governance.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | N/A | N/A - No constitutional violations identified |

All design choices align with constitutional requirements and industry best practices for production-grade web applications.

---

## Phase 0: Research & Technology Decisions

**Purpose**: Resolve technical unknowns, evaluate technology choices, and document research findings before proceeding to design.

### 0.1 Research Tasks

#### R-001: Better Auth Integration Pattern for FastAPI
**Context**: Better Auth is primarily designed for Next.js frontend. Need to determine optimal integration pattern with FastAPI backend for JWT token validation.

**Decision**: Use Better Auth on frontend for JWT management, implement custom JWT middleware on FastAPI backend using shared secret.

**Rationale**:
- Better Auth's strengths are in frontend session management and Next.js integration
- FastAPI will implement JWT verification middleware that validates tokens issued by Better Auth
- Both services share JWT secret via environment variable
- This separation leverages Better Auth's secure cookie handling while allowing FastAPI to focus on API logic

**Alternatives Considered**:
- Option A: Use Better Auth for both frontend and backend
  - Rejected: Better Auth has limited FastAPI support and documentation
- Option B: Implement custom auth from scratch
  - Rejected: Violates requirement to use Better Auth 1.0+, increases security risk of rolling own auth
- Option C: Use dedicated auth service (Auth0, Firebase)
  - Rejected: Adds complexity, cost, and vendor lock-in for Phase II scope

#### R-002: SQLModel Async vs Sync Operations
**Context**: Phase II requires async operations for production-grade performance. Need to determine whether to use async SQLModel or sync with async wrapper.

**Decision**: Use async SQLModel with async engine configuration.

**Rationale**:
- SQLModel 0.0.22+ has robust async support
- Async operations enable better concurrency and resource utilization
- Aligns with FastAPI's async-first design
- Better scalability for future multi-user scenarios

**Alternatives Considered**:
- Option A: Sync SQLModel with async/await wrapper
  - Rejected: Adds complexity, doesn't leverage native async benefits
- Option B: Use SQLAlchemy async directly
  - Rejected: Loses SQLModel's declarative benefits

#### R-003: User ID Storage in JWT
**Context**: Need to determine format and placement of user_id in JWT token for user isolation enforcement.

**Decision**: Store user_id as a standard claim in JWT payload under `sub` (subject) field.

**Rationale**:
- `sub` claim is JWT standard for identity/subject
- FastAPI middleware can easily extract: `token.get("sub")`
- Enables URL user_id validation: `token_user_id == url_user_id`
- Industry standard pattern with clear semantics

**Alternatives Considered**:
- Option A: Custom claim named `user_id`
  - Rejected: Not following JWT standards
- Option B: Store email instead of user_id
  - Rejected: Requires database lookup on every request to convert email → user_id
- Option C: Store both user_id and email
  - Rejected: Unnecessary payload size increase

#### R-004: Database Connection Pooling Strategy
**Context**: Neon PostgreSQL requires connection pooling for production performance. Need to select optimal pooling strategy.

**Decision**: Use asyncpg with connection pool (default 10 connections, max 20).

**Rationale**:
- asyncpg is the async PostgreSQL driver recommended for FastAPI
- Connection pooling reduces overhead of establishing new connections
- Default values suitable for initial 10k user target
- Can scale via environment configuration

**Alternatives Considered**:
- Option A: No pooling (one connection per request)
  - Rejected: Performance degradation under load
- Option B: Larger static pool (50+ connections)
  - Rejected: Unnecessary resource consumption for initial deployment

#### R-005: Frontend State Management for Auth
**Context**: Need to determine state management strategy for JWT token and authenticated state across components.

**Decision**: Use React Context API with Better Auth client library, store JWT in HTTP-only cookies (not component state).

**Rationale**:
- React Context provides global auth state across component tree
- Better Auth client handles secure cookie operations automatically
- Prevents localStorage storage (security requirement)
- Server components can read cookies directly for SSR

**Alternatives Considered**:
- Option A: Redux/Zustand for state management
  - Rejected: Unnecessary complexity for Phase II scope
- Option B: LocalStorage for JWT
  - Rejected: Security violation (Constitution explicitly prohibits)
- Option C: Query parameters for JWT
  - Rejected: Security risk (tokens in URLs, logs, history)

### 0.2 Environment Configuration Standards

**Required Environment Variables**:

Backend:
```bash
# Database
DATABASE_URL=postgresql://user:pass@host:port/db

# JWT
JWT_SECRET=your-secret-key-min-256-bits
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7

# CORS
FRONTEND_URL=http://localhost:3000

# Logging
LOG_LEVEL=INFO
ENVIRONMENT=development|production
```

Frontend:
```bash
# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth
BETTER_AUTH_SECRET=shared-secret-with-backend
BETTER_AUTH_URL=http://localhost:3000
```

### 0.3 Security Standards Confirmation

- ✅ JWT secret minimum 256 bits (use `openssl rand -hex 32` to generate)
- ✅ bcrypt minimum 12 rounds (configurable via BCRYPT_ROUNDS env var)
- ✅ TLS required for database connection in production (DATABASE_URL must use `postgresql://` with SSL parameter)
- ✅ CORS restricted to specific frontend origin (no `*` wildcard)
- ✅ Structured JSON logging with correlation IDs
- ✅ Error messages sanitize sensitive data

---

## Phase 1: Design & Architecture

**Purpose**: Define data model, API contracts, and system architecture before implementation.

### 1.1 Data Model Design

See [data-model.md](./data-model.md) for detailed entity definitions, relationships, validation rules, and state transitions.

### 1.2 API Contracts

See [contracts/](./contracts/) directory for detailed API endpoint specifications, request/response schemas, and error codes.

### 1.3 Architecture Overview

#### Backend Architecture (FastAPI)

```
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Application                 │
├─────────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────────┐    │
│  │           Middleware Layer                      │    │
│  │  - CORS Middleware                          │    │
│  │  - JWT Authentication Middleware              │    │
│  │  - Request ID (Correlation ID) Middleware     │    │
│  │  - Error Handling Middleware                 │    │
│  └───────────────────────────────────────────────────┘    │
│                         │                                 │
│                         ▼                                 │
│  ┌───────────────────────────────────────────────────┐    │
│  │           Router Layer (/api)                │    │
│  │  - /health (public)                        │    │
│  │  - /auth (public: register, login, logout)     │    │
│  │  - /{user_id}/tasks (protected)           │    │
│  └───────────────────────────────────────────────────┘    │
│                         │                                 │
│                         ▼                                 │
│  ┌───────────────────────────────────────────────────┐    │
│  │           Service Layer                      │    │
│  │  - AuthService (hashing, JWT generation)    │    │
│  │  - TaskService (CRUD, user isolation)      │    │
│  └───────────────────────────────────────────────────┘    │
│                         │                                 │
│                         ▼                                 │
│  ┌───────────────────────────────────────────────────┐    │
│  │           Data Layer (SQLModel)              │    │
│  │  - User Model                                 │    │
│  │  - Task Model                                 │    │
│  │  - Async Engine                                │    │
│  └───────────────────────────────────────────────────┘    │
│                         │                                 │
└─────────────────────────┼─────────────────────────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │ PostgreSQL DB │
                  │   (Neon)     │
                  └───────────────┘
```

#### Frontend Architecture (Next.js 15+ App Router)

```
┌─────────────────────────────────────────────────────────────┐
│                   Next.js 15+ Application               │
├─────────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────────┐    │
│  │           Middleware                          │    │
│  │  - Auth check for protected routes             │    │
│  │  - Request logging (correlation ID)            │    │
│  └───────────────────────────────────────────────────┘    │
│                         │                                 │
│                         ▼                                 │
│  ┌───────────────────────────────────────────────────┐    │
│  │           App Router                         │    │
│  │  /register (public)                         │    │
│  │  /login (public)                            │    │
│  │  /tasks (protected)                           │    │
│  └───────────────────────────────────────────────────┘    │
│                         │                                 │
│                         ▼                                 │
│  ┌───────────────────────────────────────────────────┐    │
│  │           Components                        │    │
│  │  - AuthProvider (Context)                    │    │
│  │  - TaskList, TaskForm                       │    │
│  │  - ProtectedRoute (HOC)                     │    │
│  └───────────────────────────────────────────────────┘    │
│                         │                                 │
│                         ▼                                 │
│  ┌───────────────────────────────────────────────────┐    │
│  │           API Client (/lib/api/client.ts)   │    │
│  └───────────────────────────────────────────────────┘    │
│                         │                                 │
└─────────────────────────┼─────────────────────────────────┘
                          │
          HTTP Only Cookie
                          │
                          ▼
                  ┌───────────────┐
                  │ FastAPI API  │
                  │   /api        │
                  └───────────────┘
```

#### Authentication Flow

```
1. Registration Flow:
   User → POST /api/auth/register
   → Backend validates email/password (bcrypt 12+ rounds)
   → Better Auth issues JWT
   → JWT stored in HTTP-only cookie
   → User redirected to /tasks

2. Login Flow:
   User → POST /api/auth/login
   → Backend verifies credentials (bcrypt compare)
   → Better Auth issues JWT
   → JWT stored in HTTP-only cookie
   → User redirected to /tasks

3. Protected Request Flow:
   User → GET /api/{user_id}/tasks
   → Cookie middleware extracts JWT
   → JWT middleware validates signature and extracts user_id
   → Route handler validates: token_user_id == url_user_id
   → Service queries tasks WHERE owner_user_id = authenticated_user_id
   → Response returned with user's tasks only

4. Logout Flow:
   User → POST /api/auth/logout
   → Better Auth invalidates cookie
   → User redirected to /login
```

### 1.4 Security Architecture

#### JWT Token Structure

```json
{
  "sub": "user-uuid-here",
  "email": "user@example.com",
  "iat": 1234567890,
  "exp": 1234567890 + (7 * 24 * 60 * 60)
}
```

#### User Isolation Enforcement

**Multi-Layer Protection**:

1. **Authentication Layer**: JWT must be valid and not expired
2. **Authorization Layer**: `token.sub == request.path.user_id`
3. **Data Layer**: Query `WHERE owner_user_id == authenticated_user_id`
4. **Frontend Layer**: Only render authenticated user's routes

**Example Violation Prevention**:

User A (user_id=123) tries to access User B's (user_id=456) task:

```
Request: GET /api/456/tasks/789
JWT: {sub: "123", exp: ...}

Step 1: JWT valid ✅
Step 2: Extract user_id from JWT = "123"
Step 3: Compare: token_user_id (123) != url_user_id (456)
Result: 403 Forbidden (user_id mismatch)

Even if URL mismatch bypassed:
Step 4: Query WHERE owner_user_id = 123 AND id = 789
Result: Empty result (task 789 belongs to user 456, not 123)
Response: 404 Not Found
```

### 1.5 Error Handling Strategy

#### Error Taxonomy

| Error Type | HTTP Status | Example Scenarios | User Message |
|-------------|-------------|---------------------|---------------|
| Unauthorized | 401 | Missing JWT, expired token, invalid token | "Please log in to continue" |
| Forbidden | 403 | user_id mismatch, accessing other user's task | "Access denied" |
| Not Found | 404 | Task doesn't exist, user doesn't exist | "Resource not found" |
| Validation Error | 400 | Email format invalid, password too short | "Invalid input: {field} validation failed" |
| Conflict | 409 | Email already registered | "Email already registered" |
| Server Error | 500 | Database failure, unexpected error | "Operation failed. Ref: {correlation-id}" |

#### Logging Strategy

**Structured JSON Format**:
```json
{
  "timestamp": "2026-01-05T12:00:00Z",
  "level": "INFO",
  "correlation_id": "uuid-here",
  "user_id": "user-uuid",
  "endpoint": "/api/{user_id}/tasks",
  "method": "POST",
  "status_code": 200,
  "duration_ms": 45,
  "message": "Task created successfully"
}
```

**No Sensitive Data Logged**:
- Passwords (never logged, only bcrypt hashes)
- JWT tokens (only expiration and user_id extracted)
- Personal information (PII)

### 1.6 Migration Strategy

#### Alembic Configuration

- Use Alembic for database schema versioning
- First migration: Create users and tasks tables with constraints
- Each schema change requires new migration
- Production deployment requires migration execution before app startup

#### Rollback Strategy

- All migrations are reversible
- Rollback script tests migration downgrade
- Production rollback reverts to previous schema version
- Data integrity checks before and after migration

---

## Phase 2: Implementation Planning

**Note**: Phase 2 detailed implementation tasks will be generated by `/sp.tasks` command after this plan is approved.

### 2.1 Implementation Phases (High-Level)

#### Phase 2.1: Backend Foundation
- Project structure setup (UV, pyproject.toml)
- Database connection and async engine configuration
- SQLModel base models (User, Task)
- Alembic initialization and first migration
- Logging middleware (correlation ID, structured JSON)
- Error handling middleware
- CORS middleware

#### Phase 2.2: Authentication Implementation
- AuthService (bcrypt hashing, JWT generation/verification)
- Better Auth integration on frontend
- JWT middleware for FastAPI
- Auth routes (register, login, logout)
- User isolation enforcement logic

#### Phase 2.3: Task Management API
- TaskService (CRUD with user isolation)
- Task routes under `/api/{user_id}/tasks`
- Input validation (Pydantic models)
- GET /api/{user_id}/tasks
- POST /api/{user_id}/tasks
- GET /api/{user_id}/tasks/{id}
- PUT /api/{user_id}/tasks/{id}
- PATCH /api/{user_id}/tasks/{id}/complete
- DELETE /api/{user_id}/tasks/{id}

#### Phase 2.4: Health Check
- GET /health endpoint (no auth required)
- Database connectivity check
- Environment info (for debugging)

#### Phase 2.5: Frontend Foundation
- Next.js project setup (App Router)
- TypeScript strict mode configuration
- Tailwind CSS setup
- API client (/lib/api/client.ts)
- Auth Context (React Context)
- ProtectedRoute component
- Middleware for auth check

#### Phase 2.6: Frontend Auth UI
- Registration page (/register)
- Login page (/login)
- Logout functionality
- Form validation (client-side)
- Error display

#### Phase 2.7: Frontend Task Management UI
- Tasks page (/tasks)
- TaskList component
- TaskForm component (create, update)
- Task completion toggle
- Task delete functionality
- Loading states and error handling

#### Phase 2.8: Integration & Testing
- End-to-end integration of frontend and backend
- Integration tests (auth flow, task CRUD)
- E2E tests (user journey)
- Security tests (user isolation, auth bypass prevention)
- Performance testing

### 2.2 Verification Checkpoints

#### Backend Checkpoints

| Checkpoint | Validation | Success Criteria |
|------------|------------|------------------|
| Project structure | Directories and config files exist | `/backend/src/` structure complete, `pyproject.toml` configured |
| Database connection | Connects to Neon PostgreSQL | Migration runs successfully, health check passes |
| Auth Service | Hashes and verifies correctly | Test user can register, login, logout |
| Task API | CRUD operations with isolation | Tasks created, updated, deleted only for authenticated user |
| JWT Middleware | Validates and extracts user_id | Unauthorized requests rejected, token user_id available |
| OpenAPI docs | Auto-generated and accessible | `/docs` endpoint returns valid OpenAPI spec |
| Logging | Structured JSON with correlation IDs | All requests logged with proper format |

#### Frontend Checkpoints

| Checkpoint | Validation | Success Criteria |
|------------|------------|------------------|
| Project structure | Next.js App Router configured | `/frontend/src/app/` with routes, `tsconfig.json` strict mode |
| API Client | Communicates with backend | Successful GET/POST to API endpoints |
| Auth Flow | Registers, logs in, logs out | User can complete full auth cycle |
| Task UI | Renders and manages tasks | User can create, view, update, delete tasks |
| Security | JWT in HTTP-only cookies | No localStorage usage, cookies marked HttpOnly |
| Error Handling | Displays clear errors | Validation errors and server errors shown to user |

#### Integration Checkpoints

| Checkpoint | Validation | Success Criteria |
|------------|------------|------------------|
| Frontend ↔ Backend | API calls succeed | Frontend can call all backend endpoints successfully |
| User Journey | Complete workflow works | User can register → login → create task → logout → login → view task |
| Data Isolation | No cross-user access | User A cannot see User B's data |
| Security | All auth enforced | Unauthenticated users rejected, user_id mismatch rejected |

### 2.3 Testing Strategy

#### Backend Tests

**Unit Tests** (`tests/unit/`):
- Test password hashing (bcrypt 12+ rounds)
- Test JWT generation and validation
- Test Pydantic models validation
- Test business logic (task CRUD, user filtering)

**Integration Tests** (`tests/integration/`):
- Test registration flow
- Test login/logout flow
- Test task CRUD operations
- Test user isolation enforcement
- Test error responses (401, 403, 404, 400, 409)

**Coverage Target**: 80% minimum

#### Frontend Tests

**Unit Tests** (`tests/unit/`):
- Test React components
- Test auth context
- Test API client functions

**E2E Tests** (`tests/e2e/`):
- Test user registration
- Test login
- Test task creation
- Test task list display
- Test task update and deletion
- Test logout

#### Security Tests

- SQL injection prevention
- XSS prevention
- JWT tampering detection
- Authentication bypass attempts
- User isolation verification

---

## Phase 3: Deployment Planning

**Note**: Deployment details for Phase II will focus on local development setup with Docker Compose. Production deployment planned for Phase IV.

### 3.1 Local Development Setup

#### Docker Compose Configuration

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: taskflow
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://user:pass@postgres:5432/taskflow
      JWT_SECRET: dev-secret-key-change-in-production
      FRONTEND_URL: http://localhost:3000
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  frontend:
    build: ./frontend
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    ports:
      - "3000:3000"
    depends_on:
      - backend
```

### 3.2 Environment Files

**`.env.example` (Backend)**:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/taskflow
JWT_SECRET=your-secret-key-min-256-bits
JWT_ALGORITHM=HS256
JWT_EXPIRATION_DAYS=7
FRONTEND_URL=http://localhost:3000
LOG_LEVEL=INFO
ENVIRONMENT=development
```

**`.env.example` (Frontend)**:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3.3 Quick Start Instructions

See [quickstart.md](./quickstart.md) for detailed setup instructions.

---

## Re-evaluation of Constitution Check (Post-Design)

### Updated Principles Compliance

- ✅ **Spec-First Development**: Plan derived directly from specification. All design decisions reference spec sections.
- ✅ **AI as Controlled Executor**: Clear constraints for AI implementation defined. No autonomous AI decisions.
- ✅ **Determinism and Reproducibility**: All technology choices documented with rationale. Environment variables defined.
- ✅ **Production-Grade Standards**: Real security practices, error handling, logging, testing strategy included.
- ✅ **Stateless Architecture Priority**: JWT-based stateless authentication confirmed. No in-memory sessions designed.

### Updated Quality Standards Compliance

- ✅ **Implementation Standards**: Clear separation of concerns, no raw SQL, ORM-only architecture designed.
- ✅ **Security Standards**: Multi-layer security (auth, authorization, data), HTTP-only cookies, bcrypt 12+ rounds confirmed.
- ✅ **Technology Baseline**: All chosen technologies meet or exceed constitutional minimums.
- ✅ **Code Quality Standards**: Testing strategy ensures 80% coverage, TypeScript strict mode enforced.
- ✅ **Observability Standards**: Structured JSON logging with correlation IDs defined in architecture.

### Updated Phase-Specific Compliance (Phase II)

- ✅ **Architecture**: Monorepo structure with `/frontend` and `/backend` defined.
- ✅ **API Requirements**: All routes under `/api`, user_id validation at multiple layers defined.
- ✅ **Authentication**: JWT-only, 7-day expiration, Better Auth integration confirmed.
- ✅ **Security Requirements**: Passwords hashed with bcrypt 12+ rounds, user isolation at query level confirmed.
- ✅ **Prohibited Practices**: No localStorage, no hardcoded secrets, no missing user_id validation enforced in design.
- ✅ **Frontend Requirements**: HTTP-only cookies, client-side validation, route separation designed.

**FINAL CONSTITUTION CHECK STATUS**: ✅ PASS - All constitutional requirements satisfied in design.

---

## Next Steps

### Immediate Actions

1. Review and approve this implementation plan
2. Execute `/sp.tasks` to generate detailed implementation tasks with dependencies and ordering
3. Begin Phase 2.1 (Backend Foundation) implementation

### Before Implementation

- Verify database connection string availability
- Generate JWT secret (256+ bits)
- Configure CORS origin for frontend
- Review API contracts in `/contracts/` directory

### During Implementation

- Follow task order from `/sp.tasks`
- Verify each checkpoint before proceeding
- Run tests after each phase
- Update plan if discoveries require design changes

### After Implementation

- Run full test suite (unit, integration, E2E)
- Verify all checkpoints pass
- Document any deviations from plan
- Prepare for Phase III (AI Chatbot with MCP)

---

## Architecture Decision Records

### ADR-001: JWT Middleware Strategy for FastAPI
**Status**: Accepted
**Context**: Need to authenticate and authorize all API requests using JWT tokens issued by Better Auth.
**Decision**: Implement custom JWT middleware in FastAPI using shared secret with Better Auth.
**Consequences**:
- Positive: Leverages Better Auth's secure cookie handling, FastAPI flexibility, clear separation of concerns
- Negative: Requires shared secret configuration, custom middleware maintenance

### ADR-002: User Isolation Enforcement Multi-Layer Strategy
**Status**: Accepted
**Context**: Constitutional requirement for strict user data isolation across all access layers.
**Decision**: Enforce isolation at authentication (token), authorization (user_id match), and data (query) layers.
**Consequences**:
- Positive: Defense in depth, multiple failure points prevent data leaks
- Negative: Slight performance overhead (multiple validations), requires coordination across layers

### ADR-003: Async SQLModel with Asyncpg
**Status**: Accepted
**Context**: Need async database operations for production-grade performance with FastAPI.
**Decision**: Use async SQLModel with asyncpg driver and connection pooling.
**Consequences**:
- Positive: Better concurrency, resource utilization, FastAPI async alignment
- Negative: Learning curve for async patterns, debugging complexity

---

## Notes

- This plan will be executed in sequence defined by `/sp.tasks` command
- All tasks will reference this plan and the specification
- Deviations from this plan must be documented and justified
- Constitutional compliance will be verified throughout implementation
