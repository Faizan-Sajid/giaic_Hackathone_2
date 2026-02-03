# Research Document: Phase II Full-Stack Web Application

**Feature**: Phase II Full-Stack Web Application with JWT Authentication
**Date**: 2026-01-05
**Purpose**: Document technology decisions and research findings to guide implementation

---

## R-001: Better Auth Integration Pattern for FastAPI

### Decision
Use Better Auth on frontend for JWT management and secure cookie handling. Implement custom JWT middleware on FastAPI backend using shared secret.

### Rationale
- **Better Auth Strengths**: Best-in-class session management for Next.js, automatic secure HTTP-only cookie handling, built-in OAuth2 support (future phases)
- **FastAPI Role**: API-focused framework, excellent for custom middleware implementation
- **Separation of Concerns**: Frontend manages user sessions and cookies, backend focuses on API logic and business rules
- **Shared Secret**: Both services use identical JWT secret environment variable, enabling cross-platform token validation
- **Stateless Authentication**: JWT tokens contain all necessary claims (user_id, email), no server-side session storage required

### Alternatives Considered

#### Option A: Use Better Auth for both frontend and backend
**Description**: Use Better Auth's server-side components and middleware for both Next.js frontend and FastAPI backend.

**Evaluation**:
- Better Auth has excellent Next.js integration but limited FastAPI support and documentation
- Maintaining both systems would add complexity without clear benefit
- Better Auth is optimized for JavaScript/TypeScript ecosystems, less so for Python

**Rejected**: Insufficient FastAPI support and documentation would lead to increased implementation risk and maintenance burden.

#### Option B: Implement Custom Authentication from Scratch
**Description**: Build complete JWT authentication system manually for both frontend and backend.

**Evaluation**:
- Would violate constitutional requirement to use Better Auth 1.0+
- Increases security risk of rolling own auth implementation
- No benefit over leveraging proven Better Auth library
- Reinventing well-solved security problem

**Rejected**: Violates specification requirements and introduces unnecessary security risk.

#### Option C: Use Dedicated Auth Service (Auth0, Firebase, Supabase)
**Description**: Integrate third-party authentication-as-a-service provider.

**Evaluation**:
- Would add cost (provider fees)
- Introduces vendor lock-in and external dependency
- Adds complexity to Phase II scope (requires service setup, configuration, debugging)
- Not specified in requirements or approved technology baseline

**Rejected**: Outside Phase II scope and increases unnecessary complexity.

### Implementation Notes

**Frontend (Next.js)**:
```typescript
// Better Auth configuration
import { auth } from '@/auth'

export const { GET, POST } = auth({
  providers: [
    // Email/password provider
    credentials({
      name: "Credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" }
      },
      authorize: async (credentials) => {
        // Call backend /api/auth/login
        const response = await fetch('/api/auth/login', {
          method: 'POST',
          body: JSON.stringify(credentials)
        })
        if (response.ok) {
          // Better Auth handles JWT cookie setting
          return true
        }
        return false
      }
    })
  ]
})
```

**Backend (FastAPI)**:
```python
# JWT middleware (custom implementation)
from fastapi import Security, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def verify_jwt(credentials: HTTPAuthorizationCredentials):
    try:
        payload = jwt.decode(
            credentials.credentials,
            os.getenv("JWT_SECRET"),
            algorithms=[os.getenv("JWT_ALGORITHM")]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Usage in route
@router.get("/{user_id}/tasks", dependencies=[Depends(verify_jwt)])
async def list_tasks(user_id: str, token_user_id: str = Depends(verify_jwt)):
    # Validate user_id match
    if token_user_id != user_id:
        raise HTTPException(status_code=403, detail="User ID mismatch")
    # Query tasks with user isolation
    tasks = await TaskService.list_tasks(user_id)
    return tasks
```

---

## R-002: SQLModel Async vs Sync Operations

### Decision
Use async SQLModel with async engine configuration and asyncpg PostgreSQL driver.

### Rationale
- **SQLModel 0.0.22+ Support**: Robust native async operations with proper type hints
- **Performance Benefits**: Async operations enable better concurrency, handle multiple requests simultaneously without blocking
- **FastAPI Alignment**: FastAPI is async-first framework, async SQLModel complements this design
- **Scalability**: Async I/O operations scale better under load (100+ concurrent users target)
- **Resource Efficiency**: Connection pooling with async operations reduces resource usage compared to spawning threads/processes
- **Future-Proof**: Async patterns are industry standard for modern Python web frameworks

### Alternatives Considered

#### Option A: Sync SQLModel with Async Wrapper
**Description**: Use synchronous SQLModel and wrap database calls with async/await.

**Evaluation**:
- Adds unnecessary complexity and indirection
- Doesn't leverage native async benefits of SQLModel
- Still requires async engine under the hood
- Wrapper logic is maintenance overhead

**Rejected**: Adds complexity without benefit. Native async SQLModel is cleaner and more performant.

#### Option B: Use SQLAlchemy Async Directly
**Description**: Use SQLAlchemy's async API directly, bypassing SQLModel.

**Evaluation**:
- Loses SQLModel's declarative benefits (type-safe models, automatic schema generation)
- Requires manual table definitions and boilerplate
- More verbose, less maintainable
- Doesn't align with "use SQLModel ORM" constraint

**Rejected**: Loses SQLModel advantages, violates simplicity principle.

### Implementation Notes

**Engine Configuration**:
```python
# backend/src/core/database.py
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Async engine with connection pooling
engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Disable SQL logging in production
    pool_size=10,  # Default pool size
    max_overflow=10  # Allow 10 additional connections
)

# Async session factory
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Dependency for FastAPI routes
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
```

**Model Definition**:
```python
# backend/src/models/task.py
from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_user_id: str = Field(foreign_key="user.id")
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# Async operations
async def create_task(session: AsyncSession, task: Task) -> Task:
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task
```

---

## R-003: User ID Storage in JWT

### Decision
Store user_id as standard JWT claim under `sub` (subject) field.

### Rationale
- **JWT Standard (RFC 7519)**: `sub` claim is standardized for subject/identity
- **Clear Semantics**: `sub` universally recognized as the entity the token represents
- **Simple Extraction**: FastAPI middleware easily extracts: `token.get("sub")`
- **User Isolation Validation**: Enables clean comparison: `token.sub == url_user_id`
- **Email Avoidance**: Storing user_id instead of email eliminates database lookup on every request to convert email → user_id
- **Industry Best Practice**: Major auth libraries (Firebase, Auth0, Cognito) use `sub` for user identity

### Alternatives Considered

#### Option A: Custom Claim Named `user_id`
**Description**: Store user identification in custom JWT claim named `user_id`.

**Evaluation**:
- Not following JWT standards and conventions
- Would confuse developers familiar with JWT standards
- No benefit over using `sub`
- Less interoperable with standard JWT libraries and tools

**Rejected**: Deviates from standards without benefit, violates principle of using established patterns.

#### Option B: Store Email Instead of User ID
**Description**: Store user email in JWT token, perform database lookup to get user_id on each request.

**Evaluation**:
- Increases database load (additional query per request)
- Slower response time (extra round trip to database)
- Email is not stable identifier (users may change email)
- Violates "no unnecessary database lookups" principle

**Rejected**: Performance degradation and unnecessary complexity.

#### Option C: Store Both user_id and Email
**Description**: Include both user_id and email in JWT payload.

**Evaluation**:
- Increases JWT token size without benefit
- Email is redundant if user_id present
- No use case for having both in this phase
- Future phases may need email in token, can add then

**Rejected**: Unnecessary payload size increase, violates simplicity principle.

### Implementation Notes

**JWT Payload Structure**:
```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "iat": 1736102400,
  "exp": 1736707200
}
```

**JWT Generation (Backend)**:
```python
import jwt
import os
from datetime import datetime, timedelta

def create_jwt(user_id: str, email: str) -> str:
    payload = {
        "sub": user_id,
        "email": email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=7)  # Max 7 days
    }
    return jwt.encode(
        payload,
        os.getenv("JWT_SECRET"),
        algorithm=os.getenv("JWT_ALGORITHM", "HS256")
    )
```

**JWT Validation (Backend Middleware)**:
```python
async def verify_jwt(credentials: HTTPAuthorizationCredentials) -> str:
    try:
        payload = jwt.decode(
            credentials.credentials,
            os.getenv("JWT_SECRET"),
            algorithms=[os.getenv("JWT_ALGORITHM")]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token: missing user_id")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

---

## R-004: Database Connection Pooling Strategy

### Decision
Use asyncpg connection pool with default size of 10 connections and maximum of 20 (10 overflow).

### Rationale
- **Neon PostgreSQL Characteristics**: Neon is serverless PostgreSQL, connection establishment has latency cost
- **Connection Pool Benefits**: Reusing existing connections eliminates overhead of creating new connections per request
- **Performance**: Under 100 concurrent users, 10 connections efficiently serve requests with queuing
- **Scalability**: Configuration via environment variables allows tuning based on actual load
- **Async Alignment**: asyncpg async driver supports connection pooling with async operations
- **Resource Management**: Prevents connection exhaustion under load spikes
- **Production-Grade**: Connection pooling is standard practice for high-performance database access

### Alternatives Considered

#### Option A: No Pooling (One Connection Per Request)
**Description**: Establish new database connection for each request and close after.

**Evaluation**:
- High latency cost: Connection establishment is expensive operation
- Performance degradation: Under load, constant connection creation/response time increases
- Resource waste: Not leveraging connection reuse
- Not production-grade: Violates "production standards" principle

**Rejected**: Unacceptable performance for target of 100 concurrent users.

#### Option B: Larger Static Pool (50+ Connections)
**Description**: Configure large static connection pool for anticipated growth.

**Evaluation**:
- Unnecessary resource consumption: 50 connections idle during low traffic periods
- Cost implications: Some databases (Neon, cloud providers) charge per connection or connection minutes
- Over-engineering: No evidence initial deployment needs 50 connections
- Can scale later: Pool size is tunable via environment variable

**Rejected**: Unnecessary resource consumption, not cost-effective for initial deployment.

### Implementation Notes

**Connection Pool Configuration**:
```python
# backend/src/core/database.py
from sqlalchemy.ext.asyncio import create_async_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Parse connection string to add pool parameters
# Format: postgresql+asyncpg://user:pass@host:port/db?pool_size=10&max_overflow=10

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600  # Recycle connections after 1 hour
)
```

**Pool Parameters**:
- `pool_size=10`: Maintain 10 connections in pool
- `max_overflow=10`: Allow 10 additional connections when pool exhausted
- `pool_pre_ping=True`: Test connection validity before use
- `pool_recycle=3600`: Recycle connections after 1 hour (prevent connection rot)

**Monitoring**: Track pool metrics (connections in use, overflow count) via logging to detect need for adjustment.

---

## R-005: Frontend State Management for Auth

### Decision
Use React Context API with Better Auth client library. Store JWT token in HTTP-only cookies (not in component state or localStorage).

### Rationale
- **React Context**: Provides global auth state accessible by all components without prop drilling
- **Better Auth Client**: Automatically handles secure cookie operations, JWT management, and token refresh
- **HTTP-Only Cookies**: Constitutional requirement, prevents XSS attacks, more secure than localStorage
- **SSR Compatibility**: Server-side components can read cookies directly for initial page load
- **Simplicity**: Minimal complexity for Phase II scope
- **Stateless Client**: Frontend doesn't store auth state, server validates each request

### Alternatives Considered

#### Option A: Redux/Zustand for State Management
**Description**: Use dedicated state management library for auth state and tasks.

**Evaluation**:
- Overkill for Phase II scope: React Context sufficient
- Additional complexity: Actions, reducers, selectors, provider setup
- Learning curve: Team must learn Redux/Zustand patterns
- Not required: No complex state management needs in Phase II

**Rejected**: Unnecessary complexity, violates simplicity principle.

#### Option B: LocalStorage for JWT
**Description**: Store JWT token in browser localStorage.

**Evaluation**:
- **SECURITY VIOLATION**: Constitution explicitly prohibits JWT in localStorage
- XSS Vulnerability: Malicious scripts can read localStorage tokens
- Not HTTP-only: Cookies can be marked HTTP-only, localStorage cannot
- Industry Practice: HTTP-only cookies are modern security standard

**Rejected**: Violates constitution, security risk.

#### Option C: Query Parameters for JWT
**Description**: Pass JWT token in URL query parameters (e.g., `?token=xyz`).

**Evaluation**:
- **SEVERURITY RISK**: Tokens in URLs get logged (server logs, browser history, analytics)
- Leaks: Shared URLs accidentally expose tokens (e.g., copy-paste, email)
- No Cache Control: Query parameters not subject to cache control headers
- Not production-grade: Never used in secure applications

**Rejected**: Critical security vulnerability, unacceptable for production.

### Implementation Notes

**Auth Context Setup**:
```typescript
// frontend/src/contexts/AuthContext.tsx
'use client'

import { createContext, useContext, useState, useEffect } from 'react'
import { Session } from 'better-auth/react'

interface AuthContextType {
  session: Session | null
  isLoading: boolean
  refresh: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [session, setSession] = useState<Session | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Better Auth automatically loads session from HTTP-only cookie
    // No manual token handling required
    async function loadSession() {
      const response = await fetch('/api/auth/session')
      if (response.ok) {
        const data = await response.json()
        setSession(data.session)
      }
      setIsLoading(false)
    }

    loadSession()
  }, [])

  return (
    <AuthContext.Provider value={{ session, isLoading, refresh }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
```

**Protected Route Component**:
```typescript
// frontend/src/components/ProtectedRoute.tsx
'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { session, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !session) {
      router.push('/login')
    }
  }, [session, isLoading, router])

  if (isLoading) {
    return <div>Loading...</div>
  }

  return session ? children : null
}
```

**Usage in Pages**:
```typescript
// frontend/src/app/tasks/page.tsx
import { ProtectedRoute } from '@/components/ProtectedRoute'

export default function TasksPage() {
  return (
    <ProtectedRoute>
      <TaskList />
    </ProtectedRoute>
  )
}
```

---

## Summary of Technology Decisions

| Decision | Technology | Key Benefit | Constitutional Alignment |
|----------|-------------|----------------|------------------------|
| Auth Integration | Better Auth (frontend) + Custom JWT (backend) | Secure cookies, stateless | ✅ Spec, Security, Stateless |
| Database Operations | Async SQLModel with asyncpg | Performance, concurrency | ✅ Tech Baseline, Performance |
| User ID in JWT | Standard `sub` claim | Simplicity, interoperability | ✅ Tech Baseline, Security |
| Connection Pooling | asyncpg pool (10+10) | Performance, scalability | ✅ Production-Grade |
| Frontend State | React Context + HTTP-only cookies | Security, simplicity | ✅ Security, Stateless |

## Implementation Readiness

- ✅ All research questions resolved
- ✅ Technology choices justified with rationales
- ✅ Alternatives evaluated and rejected with clear reasons
- ✅ Constitutional compliance verified for all decisions
- ✅ Ready for Phase 1: Design & Architecture
