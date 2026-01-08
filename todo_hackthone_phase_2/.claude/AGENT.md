# Agent Configuration and Context

**Project**: TaskFlow AI — Phase II Full-Stack Web Application
**Last Updated**: 2026-01-05

---

## Technology Stack

### Backend
- **Python**: 3.13+
- **Framework**: FastAPI 0.115.0+
- **ORM**: SQLModel 0.0.22+
- **Database**: PostgreSQL 16+ (Neon Serverless)
- **Async Driver**: asyncpg
- **Authentication**: Custom JWT middleware (shared secret with Better Auth frontend)
- **Package Manager**: UV
- **Testing**: pytest, pytest-asyncio
- **Migrations**: Alembic

### Frontend
- **Language**: TypeScript 5.7+
- **Framework**: Next.js 15+ (App Router)
- **UI Library**: React 18+
- **Authentication**: Better Auth 1.0+
- **Styling**: Tailwind CSS
- **Package Manager**: npm
- **Testing**: Jest, Playwright (E2E)
- **Mode**: Strict TypeScript enabled

---

## Architecture Patterns

### Backend Patterns
- **Async/await**: All I/O operations use async/await pattern
- **Dependency Injection**: FastAPI Depends() for middleware and services
- **Repository Pattern**: Service layer abstracts database operations
- **Middleware Chain**: CORS → JWT Auth → Request ID → Error Handling
- **Stateless Services**: No in-memory session storage, all state in JWT tokens and database

### Frontend Patterns
- **React Context**: Global auth state management
- **Server Components**: Default for performance, Client components only for interactivity
- **Protected Routes**: Higher-order component or middleware for auth checks
- **HTTP-Only Cookies**: JWT storage in secure cookies, not localStorage

---

## Code Conventions

### Python (Backend)
- **Style Guide**: PEP 8
- **Type Hints**: Required on all function signatures
- **Docstrings**: Required on all public functions
- **Max Function Length**: 50 lines
- **Max File Length**: 500 lines
- **Async I/O**: All database and external API calls use async/await
- **Error Handling**: Raise HTTPException with appropriate status codes
- **Logging**: Structured JSON logging with correlation IDs

### TypeScript (Frontend)
- **Mode**: Strict (`"strict": true` in tsconfig.json)
- **No `any` Types**: Without explicit justification
- **Component Style**: Functional components
- **Max Component Length**: 200 lines
- **Style Guide**: Airbnb ESLint rules

---

## Project Structure

### Monorepo Layout

```
/
├── backend/          # FastAPI application
│   ├── src/
│   │   ├── models/    # SQLModel models
│   │   ├── api/        # Routes and handlers
│   │   ├── core/       # Configuration, security, logging
│   │   ├── services/   # Business logic
│   │   └── main.py    # Application entry
│   ├── tests/
│   │   ├── unit/
│   │   └── integration/
│   ├── pyproject.toml
│   └── alembic/
│
├── frontend/         # Next.js application
│   ├── src/app/      # App Router pages
│   ├── src/components/ # React components
│   ├── src/lib/       # Utilities and API client
│   ├── src/contexts/  # React Context providers
│   ├── tests/
│   │   ├── unit/
│   │   └── e2e/
│   ├── package.json
│   └── tsconfig.json
│
└── specs/            # Specifications and plans (this directory)
    └── 001-full-stack-web/
```

---

## Configuration Standards

### Environment Variables

**Backend (.env)**:
- `DATABASE_URL` - PostgreSQL connection string with TLS
- `JWT_SECRET` - 256-bit secret for JWT signing
- `JWT_ALGORITHM` - HS256
- `JWT_EXPIRATION_DAYS` - 7 (maximum per Constitution)
- `FRONTEND_URL` - Frontend origin for CORS
- `LOG_LEVEL` - DEBUG, INFO, WARNING, ERROR
- `ENVIRONMENT` - development, staging, production

**Frontend (.env.local)**:
- `NEXT_PUBLIC_API_URL` - Backend API base URL

### Secrets Management

- **Never commit secrets** to version control (.gitignore includes .env)
- **Use environment variables** for all sensitive data
- **Generate secrets** with: `openssl rand -hex 32`
- **Different secrets** for development and production

---

## Security Requirements

### Authentication & Authorization
- All API endpoints (except `/health`) require valid JWT
- JWT tokens expire in maximum 7 days
- User isolation enforced at three layers: JWT validation, user_id matching, database query filtering
- Passwords hashed with bcrypt minimum 12 rounds

### Data Protection
- No plaintext passwords in logs, database, or code
- Input validation prevents SQL injection, XSS, command injection
- Structured error responses without exposing sensitive data
- CORS restricted to specific frontend origin (no wildcard in production)

### Cookie Security
- JWT stored in HTTP-only cookies (not localStorage)
- Secure flag enabled (HTTPS only)
- SameSite=Strict (CSRF protection)

---

## Testing Standards

### Backend Testing
- **Framework**: pytest
- **Coverage Minimum**: 80%
- **Test Types**: Unit tests, integration tests
- **Async Testing**: pytest-asyncio for async operations
- **Fixtures**: conftest.py for test database setup

### Frontend Testing
- **Framework**: Jest for unit tests
- **E2E Testing**: Playwright for end-to-end scenarios
- **Test Coverage**: Component testing for critical user flows

---

## Quality Standards

### Code Quality
- All code generated from specifications (spec-first development)
- Every code file contains comments referencing Task IDs and Spec sections
- Fail-fast validation on all inputs
- No manual code writing without spec updates

### Observability
- Structured JSON logging with correlation IDs
- Health check endpoint at `/health`
- Database connectivity verification
- Request/response time tracking

---

## Development Workflow

### Branching
- Feature work on numbered branches: `001-feature-name`, `002-feature-name`
- Main branch: `main` or `master`
- PRs require review and constitutional compliance check

### Commit Standards
- Conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `refactor:`
- Commit messages reference feature specification sections
- All changes pass linting and tests before commit

### Review Process
- Code review verifies constitutional compliance
- Complexity must be justified
- All PRs linked to specification or plan

---

## Current Feature Context

**Active Feature**: Phase II Full-Stack Web Application (001-full-stack-web)
**Specification**: `specs/001-full-stack-web/spec.md`
**Implementation Plan**: `specs/001-full-stack-web/plan.md`
**Current Phase**: Planning complete, awaiting `/sp.tasks` for implementation tasks

### Key Constraints
- Stateless authentication (JWT tokens, no server-side sessions)
- Strict user data isolation (multi-layer enforcement)
- Multi-user support with complete data separation
- Production-grade security (bcrypt, TLS, input validation)
- No manual SQL queries (ORM only)

### Known Decisions
- Better Auth on frontend, custom JWT middleware on FastAPI
- Async SQLModel with asyncpg driver and connection pooling
- User ID stored in JWT `sub` claim
- React Context for auth state, HTTP-only cookies
- Multi-layer user isolation (auth, authorization, data layers)

---

## Resources

### Documentation
- [TaskFlow AI Constitution](../.specify/memory/constitution.md)
- [Phase II Specification](../specs/001-full-stack-web/spec.md)
- [Implementation Plan](../specs/001-full-stack-web/plan.md)
- [Research Document](../specs/001-full-stack-web/research.md)
- [Data Model](../specs/001-full-stack-web/data-model.md)
- [API Contracts](../specs/001-full-stack-web/contracts/)

### External References
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLModel](https://sqlmodel.tiangolo.com/)
- [Next.js](https://nextjs.org/docs)
- [Better Auth](https://better-auth.com)
- [Pytest](https://docs.pytest.org/)
- [TypeScript](https://www.typescriptlang.org/docs/)
