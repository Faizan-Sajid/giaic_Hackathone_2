# Testing & Verification Skill

**Purpose**: Run tests, verify functionality, and validate implementation
**Coverage**: All verification checkpoints across Phase 2-7
**Project**: Phase II Full-Stack Web Application

---

## Skill Description

This skill handles all testing and verification tasks for Phase II Todo Application. It runs backend tests, frontend tests, integration tests, and validates implementation checkpoints including:

- Backend unit tests for services and utilities
- Backend integration tests for API endpoints
- Frontend unit tests for components
- End-to-end (E2E) tests for user journeys
- Verification checkpoints after each phase
- Security testing for user isolation
- Performance testing for API responses
- Database migration validation

---

## Usage

### Basic Usage
```
/testing
```

### With Specific Task
```
/testing verify backend
```

### Run Specific Test Suite
```
/testing backend unit
/testing backend integration
/testing frontend e2e
```

---

## Implementation Guidelines

### Testing Stack

**Backend**:
- **Framework**: pytest 7.4+
- **Async Support**: pytest-asyncio 0.21+
- **HTTP Client**: httpx 0.24+ for API testing
- **Coverage**: pytest-cov (optional)

**Frontend**:
- **Framework**: Jest 29.7+
- **E2E**: Playwright 1.40+
- **Testing Library**: React Testing Library
- **Coverage**: Jest coverage (optional)

### Test Categories

**Unit Tests**: Test individual functions/classes in isolation
- Password hashing verification
- JWT generation/validation
- Business logic (task CRUD)
- Component rendering

**Integration Tests**: Test multiple components working together
- API endpoint tests with database
- Frontend-backend API integration
- Authentication flow tests

**End-to-End (E2E) Tests**: Test complete user journeys
- Registration → Login → Create Task → Logout
- Multi-user isolation verification
- Session persistence tests

**Security Tests**: Verify security requirements
- User isolation enforcement
- SQL injection prevention
- JWT tampering detection
- XSS prevention

---

## Supported Verification Tasks

### Backend Unit Tests

**File**: `backend/tests/unit/test_auth.py`

**Test: Password Hashing**
```python
def test_hash_password_rounds():
    """
    Verify bcrypt uses 12+ rounds
    Task: Verify SEC-001 (bcrypt 12+ rounds)
    """
    password = "TestPassword123"
    hashed = hash_password(password)

    # Verify hash is different from password
    assert hashed != password

    # Verify hash length is consistent (bcrypt 60 chars)
    assert len(hashed) == 60

def test_verify_password_correct():
    """
    Verify password verification with correct password
    """
    password = "TestPassword123"
    hashed = hash_password(password)
    assert verify_password(password, hashed) == True

def test_verify_password_incorrect():
    """
    Verify password verification fails with wrong password
    """
    password1 = "TestPassword123"
    password2 = "WrongPassword456"
    hashed = hash_password(password1)
    assert verify_password(password2, hashed) == False
```

**Test: JWT Generation**
```python
def test_create_jwt_structure():
    """
    Verify JWT token structure and claims
    Task: Verify SEC-002 (7-day expiration)
    """
    user_id = "test-user-123"
    email = "test@example.com"

    token = create_jwt(user_id, email)

    # Decode without verification
    decoded = jwt.decode(
        token,
        os.getenv("JWT_SECRET"),
        algorithms=[os.getenv("JWT_ALGORITHM")]
    )

    assert decoded["sub"] == user_id
    assert decoded["email"] == email
    assert "iat" in decoded
    assert "exp" in decoded

    # Verify expiration is approximately 7 days
    exp_timestamp = decoded["exp"]
    iat_timestamp = decoded["iat"]
    exp_seconds = exp_timestamp - iat_timestamp
    expected_days = 7 * 24 * 60 * 60  # 7 days in seconds
    assert abs(exp_seconds - expected_days) < 10  # Allow 10 second tolerance
```

### Backend Integration Tests

**File**: `backend/tests/integration/test_auth_flow.py`

**Test: Registration Flow**
```python
async def test_register_new_user(async_client):
    """
    Test complete user registration
    Task: Verify FR-001 (registration flow)
    """
    response = await async_client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "TestPassword123"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "email" in data
    assert data["email"] == "newuser@example.com"
```

**Test: Duplicate Email**
```python
async def test_register_duplicate_email(async_client, test_user):
    """
    Test registration with duplicate email returns 409
    Task: Verify FR-016 (prevent duplicate email)
    """
    # Register user first
    await async_client.post(
        "/api/auth/register",
        json={
            "email": test_user["email"],
            "password": test_user["password"]
        }
    )

    # Try to register again with same email
    response = await async_client.post(
        "/api/auth/register",
        json={
            "email": test_user["email"],
            "password": "DifferentPassword456"
        }
    )

    assert response.status_code == 409
```

**Test: Login Flow**
```python
async def test_login_success(async_client, test_user):
    """
    Test successful login and JWT cookie
    Task: Verify FR-003 (login flow)
    """
    # Register user first
    await async_client.post(
        "/api/auth/register",
        json={
            "email": test_user["email"],
            "password": test_user["password"]
        }
    )

    # Login
    response = await async_client.post(
        "/api/auth/login",
        json={
            "email": test_user["email"],
            "password": test_user["password"]
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "email" in data

    # Verify JWT cookie is set
    cookies = response.cookies
    assert "token" in cookies
    assert cookies["token"].httponly is True
```

### Task API Integration Tests

**File**: `backend/tests/integration/test_task_api.py`

**Test: Create Task**
```python
async def test_create_task(async_client, auth_token, test_user):
    """
    Test task creation for authenticated user
    Task: Verify FR-008 (create task)
    """
    response = await async_client.post(
        f"/api/{test_user['id']}/tasks",
        json={
            "title": "Test Task",
            "description": "Test Description"
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] == False
```

**Test: User Isolation**
```python
async def test_user_isolation(
    async_client,
    user_a_token,
    user_a_id,
    user_b_id
):
    """
    Test User A cannot access User B's tasks
    Task: Verify FR-014 (strict data isolation)
    """
    # Create task for User A
    response = await async_client.post(
        f"/api/{user_a_id}/tasks",
        json={"title": "User A Task"},
        headers={"Authorization": f"Bearer {user_a_token}"}
    )
    assert response.status_code == 201
    task = response.json()

    # User A tries to access task through User B's URL
    response = await async_client.get(
        f"/api/{user_b_id}/tasks/{task['id']}",
        headers={"Authorization": f"Bearer {user_a_token}"}
    )

    # Should return 403 Forbidden
    assert response.status_code == 403
```

### Frontend E2E Tests

**File**: `frontend/tests/e2e/user-journey.spec.ts`

**Test: Complete User Journey**
```typescript
import { test, expect } from '@playwright/test'

test('complete user registration and task creation flow', async ({ page }) => {
  /**
   * Test: Register → Login → Create Task → Logout
   * Task: Verify end-to-end user journey
   */

  // Navigate to registration
  await page.goto('http://localhost:3000/register')

  // Fill registration form
  await page.fill('input[type="email"]', 'test@example.com')
  await page.fill('input[type="password"]', 'TestPassword123')
  await page.click('button[type="submit"]')

  // Should redirect to login or tasks
  await page.waitForURL(/\/(login|tasks)/)

  // Login
  await page.goto('http://localhost:3000/login')
  await page.fill('input[type="email"]', 'test@example.com')
  await page.fill('input[type="password"]', 'TestPassword123')
  await page.click('button[type="submit"]')

  // Should redirect to tasks
  await page.waitForURL(/\/tasks/)

  // Verify tasks page loaded
  await expect(page.locator('h1')).toContainText('My Tasks')

  // Create task
  await page.fill('input[name="title"]', 'Test Task from E2E')
  await page.fill('textarea[name="description"]', 'Test Description')
  await page.click('button[type="submit"]')

  // Verify task appears in list
  await expect(page.locator('.task-list')).toContainText('Test Task from E2E')

  // Logout
  await page.click('button:has-text("Logout")')

  // Should redirect to login
  await page.waitForURL(/\/login/)

  // Verify cannot access tasks without login
  await page.goto('http://localhost:3000/tasks')
  await page.waitForURL(/\/login/)
})
```

### Security Tests

**Test: Cross-User Access Prevention**
```python
async def test_prevent_cross_user_access(
    async_client,
    user_a_token,
    user_a_id,
    user_b_id
):
    """
    Test User A cannot list User B's tasks
    Task: Verify FR-014 (strict data isolation)
    """
    response = await async_client.get(
        f"/api/{user_b_id}/tasks",
        headers={"Authorization": f"Bearer {user_a_token}"}
    )

    # Should return 403 Forbidden
    assert response.status_code == 403
    assert "Access denied" in response.json()["detail"]
```

### Performance Tests

**Test: API Response Time**
```python
import time

async def test_api_response_time(async_client, auth_token, user_id):
    """
    Verify API responds within 300ms
    Task: Verify performance goals (p95 <300ms)
    """
    start_time = time.time()

    response = await async_client.get(
        f"/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    end_time = time.time()
    response_time_ms = (end_time - start_time) * 1000

    assert response_time_ms < 300  # Should respond in <300ms
```

---

## Test Commands

### Backend Tests

```bash
# Run all backend tests
cd backend
pytest

# Run specific test file
pytest tests/unit/test_auth.py

# Run with coverage
pytest --cov=src --cov-report=html

# Run integration tests only
pytest tests/integration/

# Run unit tests only
pytest tests/unit/

# Run tests with verbose output
pytest -v

# Run specific test
pytest tests/unit/test_auth.py::test_hash_password_rounds
```

### Frontend Tests

```bash
# Run all frontend tests
cd frontend
npm test

# Run in watch mode
npm test -- --watch

# Run with coverage
npm test -- --coverage

# Run E2E tests
npm run test:e2e

# Run specific test file
npm test TaskList.test
```

---

## Verification Checkpoints

### Phase 1: Setup Verification
- [ ] Backend directory structure created
- [ ] Frontend directory structure created
- [ ] `pyproject.toml` configured with all dependencies
- [ ] `package.json` configured with all dependencies
- [ ] `.env.example` files created for both backend and frontend
- [ ] Backend virtual environment created
- [ ] Frontend dependencies installed

### Phase 2: Foundational Verification
- [ ] Database connection succeeds (`alembic upgrade head`)
- [ ] Users table created with `UNIQUE(email)` constraint
- [ ] Tasks table created with `owner_user_id` FK and `CASCADE DELETE`
- [ ] Indexes created: `idx_users_email`, `idx_tasks_owner_user_id`, `idx_tasks_completed`
- [ ] CORS configured with `FRONTEND_URL` (no wildcards)
- [ ] JWT verification extracts `user_id` from `sub` claim
- [ ] Password hashing uses bcrypt 12+ rounds
- [ ] Error handler returns correct HTTP status codes
- [ ] Logging outputs structured JSON with correlation IDs
- [ ] FastAPI app starts on `uvicorn src.main:app --reload`
- [ ] `/health` endpoint accessible without auth
- [ ] OpenAPI docs accessible at `/docs`
- [ ] API client makes requests with `credentials: 'include'`
- [ ] AuthContext provides session state to all components
- [ ] ProtectedRoute redirects unauthenticated users to `/login`

### Phase 3: User Story 1 Verification (Auth)
- [ ] New user can register successfully
- [ ] Registration validates email format
- [ ] Registration validates password length (8+ chars)
- [ ] Registration rejects duplicate email (409 Conflict)
- [ ] Registered user can login successfully
- [ ] Login sets HTTP-only JWT cookie
- [ ] Login rejects invalid credentials (401 Unauthorized)
- [ ] Logout clears JWT cookie
- [ ] Logout redirects to login page
- [ ] Session endpoint returns user info when authenticated
- [ ] Session endpoint returns 401 when not authenticated
- [ ] Frontend registration page displays correctly
- [ ] Frontend login page displays correctly
- [ ] Auth forms show validation errors
- [ ] Auth forms show API errors
- [ ] JWT tokens stored in HTTP-only cookies only
- [ ] No JWT tokens in localStorage

### Phase 4: User Story 2 Verification (Tasks)
- [ ] Authenticated user can list their tasks
- [ ] Authenticated user can create task
- [ ] Authenticated user can get specific task
- [ ] Authenticated user can update task
- [ ] Authenticated user can toggle task completion
- [ ] Authenticated user can delete task
- [ ] Task API returns 403 on user_id mismatch
- [ ] Task API returns 404 if task doesn't exist
- [ ] Task API validates title (1-200 chars)
- [ ] Task API validates description (max 1000 chars)
- [ ] TaskList displays user's tasks
- [ ] TaskList shows completed tasks distinctly
- [ ] TaskForm validates input before submission
- [ ] TaskForm creates task successfully
- [ ] TaskForm updates task successfully
- [ ] Tasks page loads correctly
- [ ] Loading states shown during API calls
- [ ] Error messages displayed on failures
- [ ] User A cannot see User B's tasks
- [ ] User B cannot see User A's tasks
- [ ] Both users can only access their own data

### Phase 5: User Story 3 Verification (Persistence)
- [ ] Task queries include `ORDER BY created_at DESC`
- [ ] Task updates set `updated_at` timestamp
- [ ] Migration includes `CASCADE DELETE` for `owner_user_id` FK
- [ ] Database connection retry logic works
- [ ] API client handles network errors gracefully
- [ ] TaskList refreshes on interval
- [ ] HTTP-only cookies persist across browser sessions
- [ ] User logs in, creates tasks, logs out, closes browser, reopens, logs in → tasks present

### Cross-Cutting Verification
- [ ] No passwords logged in any form
- [ ] No JWT tokens logged
- [ ] No PII (personal info) logged
- [ ] All error messages user-friendly
- [ ] No stack traces exposed to users
- [ ] No internal service names exposed
- [ ] CORS restricted to specific origin (no wildcards)
- [ ] JWT secret stored in environment variable
- [ ] Database connection uses TLS (sslmode=require)
- [ ] All API endpoints use ORM (no raw SQL)
- [ ] Structured JSON logs with correlation IDs
- [ ] All code follows PEP 8 (Python)
- [ ] All code follows TypeScript strict mode
- [ ] Test coverage >= 80%

---

## Test Data Setup

**File**: `backend/tests/conftest.py`

```python
import pytest
from httpx import AsyncClient
from sqlmodel import create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession

@pytest.fixture(scope="function")
async def async_client():
    """Create async test client"""
    async with AsyncClient(app=app) as client:
        yield client

@pytest.fixture(scope="function")
async def test_user(async_client, session):
    """Create test user and return credentials"""
    user_data = {
        "email": "test@example.com",
        "password": "TestPassword123",
        "id": "test-user-id"
    }
    return user_data

@pytest.fixture(scope="function")
async def auth_token(async_client, test_user):
    """Register and login user, return JWT token"""
    # Register
    await async_client.post(
        "/api/auth/register",
        json={
            "email": test_user["email"],
            "password": test_user["password"]
        }
    )

    # Login
    response = await async_client.post(
        "/api/auth/login",
        json={
            "email": test_user["email"],
            "password": test_user["password"]
        }
    )

    data = response.json()
    # Extract token from response or cookies
    return data.get("token")
```

---

## Notes

- All tests must be deterministic (same inputs = same outputs)
- Use fixtures for test data setup and cleanup
- Mock external services when appropriate
- Tests should be fast (run in seconds, not minutes)
- Test both success and failure paths
- Test edge cases (empty strings, null values, boundary values)
- Security tests are critical (user isolation, auth bypass)
- Performance tests verify SLA compliance (<300ms response time)
- Run tests before committing code
- Aim for 80%+ code coverage
- Keep test files organized (unit vs integration vs e2e)
