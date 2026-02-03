# Authentication Implementation Skill

**Purpose**: Implement user registration, login, logout, and JWT-based authentication
**Coverage**: Phase 3 User Story 1 (T021-T032) - Complete authentication flow
**Project**: Phase II Full-Stack Web Application

---

## Skill Description

This skill handles all authentication implementation tasks for Phase II Todo Application. It creates backend authentication services and endpoints, plus frontend authentication UI including:

- Backend AuthService with bcrypt password hashing
- JWT token generation and verification
- User registration with email/password
- User login with credential verification
- User logout with cookie invalidation
- Session validation endpoint
- Frontend registration page with form
- Frontend login page with form
- Frontend logout functionality
- Form validation and error handling
- Better Auth integration for secure cookies

---

## Usage

### Basic Usage
```
/authentication
```

### With Specific Task
```
/authentication T023
```

### With Multiple Tasks
```
/authentication T021 T022 T023
```

---

## Implementation Guidelines

### Technology Stack

**Backend**:
- **Framework**: FastAPI 0.115+
- **Auth Library**: python-jose[cryptography] for JWT
- **Password Hashing**: bcrypt 12+ rounds
- **JWT Algorithm**: HS256 with shared secret
- **Token Expiration**: 7 days maximum

**Frontend**:
- **Auth Library**: Better Auth 1.0+
- **Cookie Storage**: HTTP-only cookies (Better Auth handles)
- **Form Validation**: Client-side + server-side
- **Session Management**: React Context API

### Security Requirements

- Passwords hashed with bcrypt 12+ rounds
- JWT tokens expire after 7 days
- JWT secret stored in environment variable
- JWT tokens stored in HTTP-only cookies (never localStorage)
- Email validation (RFC 5322)
- Password minimum 8 characters
- Unique email enforcement (no duplicate accounts)
- Never log passwords (even hashed)
- User ID validation in all protected routes

---

## Supported Tasks

### T021-T022: AuthService

**File**: `backend/src/services/auth_service.py`

**T021: Password Hashing**
```python
def hash_password(password: str) -> str:
    """
    Hash password using bcrypt with 12+ rounds
    Task: T021
    Spec: SEC-001 (bcrypt minimum 12 rounds)
    """
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against bcrypt hash
    Task: T021
    Spec: FR-003 (password verification)
    """
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )
```

**T022: JWT Generation**
```python
def create_jwt(user_id: str, email: str) -> str:
    """
    Create JWT token with user_id, email, expiration
    Task: T022
    Spec: FR-004 (JWT token with max 7-day expiration)
    SEC-002 (7-day max expiration)
    """
    payload = {
        "sub": user_id,  # Subject: User UUID
        "email": email,
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(
        payload,
        os.getenv("JWT_SECRET"),
        algorithm=os.getenv("JWT_ALGORITHM", "HS256")
    )
```

### T023: Register Endpoint

**File**: `backend/src/api/routes/auth.py`

**Route**: `POST /api/auth/register`

**Validation**:
- Email format (RFC 5322)
- Password length (minimum 8 characters)
- Email uniqueness (no duplicate accounts)

**Implementation**:
```python
@router.post("/register", status_code=201)
async def register(request: RegisterRequest, session: AsyncSession):
    """
    Register new user with email and password
    Task: T023
    Spec: FR-001 (registration with email and password)
    FR-016 (prevent duplicate email)
    """
    # Check if email already exists
    existing_user = await session.exec(
        select(User).where(User.email == request.email)
    )
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    # Hash password
    password_hash = hash_password(request.password)

    # Create user
    user = User(
        email=request.email,
        password_hash=password_hash
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "message": "User registered successfully"
    }
```

**Responses**:
- `201 Created`: User registered successfully
- `400 Bad Request`: Invalid email format or password too short
- `409 Conflict`: Email already registered
- `500 Internal Server Error`: Database failure

### T024: Login Endpoint

**File**: `backend/src/api/routes/auth.py`

**Route**: `POST /api/auth/login`

**Implementation**:
```python
@router.post("/login")
async def login(
    request: LoginRequest,
    response: Response,
    session: AsyncSession
):
    """
    Authenticate user and set JWT cookie
    Task: T024
    Spec: FR-003 (login with email and password)
    SEC-004 (JWT issuance on successful auth)
    """
    # Find user by email
    user = await session.exec(
        select(User).where(User.email == request.email)
    )
    user = user.one_or_none()

    # Verify password
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Generate JWT token
    token = create_jwt(user.id, user.email)

    # Set HTTP-only cookie
    response.set_cookie(
        key="token",
        value=token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=604800,  # 7 days in seconds
        path="/"
    )

    return {
        "id": user.id,
        "email": user.email,
        "message": "Login successful"
    }
```

**Responses**:
- `200 OK`: Login successful, JWT cookie set
- `400 Bad Request`: Invalid email format
- `401 Unauthorized`: Invalid email or password
- `500 Internal Server Error`: Database failure

**Cookie Attributes**:
- **HttpOnly**: True (prevents JavaScript access)
- **Secure**: True (HTTPS only in production)
- **SameSite**: Strict (CSRF protection)
- **Max-Age**: 604800 seconds (7 days)
- **Path**: `/` (valid for entire domain)

### T025: Logout Endpoint

**File**: `backend/src/api/routes/auth.py`

**Route**: `POST /api/auth/logout`

**Implementation**:
```python
@router.post("/logout")
async def logout(response: Response):
    """
    Invalidate session by clearing JWT cookie
    Task: T025
    Spec: FR-017 (invalidate JWT on logout)
    """
    response.delete_cookie("token", path="/")
    return {"message": "Logged out successfully"}
```

**Responses**:
- `200 OK`: Logout successful, cookie cleared
- `401 Unauthorized`: No valid JWT cookie
- `500 Internal Server Error**: Unexpected error

### T026: Session Endpoint

**File**: `backend/src/api/routes/auth.py`

**Route**: `GET /api/auth/session`

**Implementation**:
```python
@router.get("/session")
async def get_session(user_id: str = Depends(verify_jwt)):
    """
    Return user info if authenticated
    Task: T026
    Spec: Used by frontend to check auth state
    """
    # Get user from database
    user = await session.exec(
        select(User).where(User.id == user_id)
    )
    user = user.one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return {
        "user": {
            "id": user.id,
            "email": user.email
        },
        "authenticated": True
    }
```

**Responses**:
- `200 OK`: User info returned
- `401 Unauthorized`: Not authenticated (no/invalid token)

### T027: Registration Page UI

**File**: `frontend/src/app/(auth)/register/page.tsx`

**Implementation**:
```typescript
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function RegisterPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    // Client-side validation
    if (!email || !email.match(/^[^\s@]+@[^\s@]+\.[^\s@]+$/)) {
      setError('Invalid email format')
      setLoading(false)
      return
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters')
      setLoading(false)
      return
    }

    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })

      if (response.ok) {
        router.push('/login')
      } else if (response.status === 409) {
        setError('Email already registered')
      } else {
        setError('Registration failed')
      }
    } catch (err) {
      setError('Network error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={handleSubmit} className="w-full max-w-md">
        <h1>Register</h1>

        {error && <div className="error">{error}</div>}

        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />

        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password (min 8 characters)"
          required
          minLength={8}
        />

        <button type="submit" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </button>

        <p>
          Already have an account? <a href="/login">Login</a>
        </p>
      </form>
    </div>
  )
}
```

### T028: Login Page UI

**File**: `frontend/src/app/(auth)/login/page.tsx`

**Implementation**:
```typescript
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        credentials: 'include',  // Better Auth handles cookie
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })

      if (response.ok) {
        router.push('/tasks')
      } else if (response.status === 401) {
        setError('Invalid email or password')
      } else {
        setError('Login failed')
      }
    } catch (err) {
      setError('Network error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <form onSubmit={handleSubmit} className="w-full max-w-md">
        <h1>Login</h1>

        {error && <div className="error">{error}</div>}

        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Email"
          required
        />

        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />

        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>

        <p>
          Don't have an account? <a href="/register">Register</a>
        </p>
      </form>
    </div>
  )
}
```

### T029-T030: Form Integration

Already implemented in T027 and T028 above.

### T031: Logout Function

**Implementation**:
```typescript
export async function logout() {
  /**
   * Logout user and redirect to login
   * Task: T031
   * Spec: FR-017 (invalidate JWT on logout)
   */
  try {
    await fetch('/api/auth/logout', {
      method: 'POST',
      credentials: 'include'
    })

    // Redirect to login page
    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
  } catch (error) {
    console.error('Logout failed:', error)
  }
}
```

### T032: Auth Form Error Handling

Already implemented in T027-T028 above with:
- Email format validation
- Password length validation
- API error display (duplicate email, invalid credentials)
- Network error handling
- Loading states

---

## Examples

### Example 1: Complete Auth Flow
```
User: /authentication T021 T022 T023 T024 T025 T026 T027 T028 T031

Output:
- Backend AuthService created with password hashing and JWT generation
- Register endpoint implemented
- Login endpoint implemented
- Logout endpoint implemented
- Session endpoint implemented
- Frontend registration page created
- Frontend login page created
- Logout function implemented
```

### Example 2: Backend Auth Only
```
User: /authentication T021 T022 T023 T024

Output:
- AuthService created
- Register and login endpoints implemented
- JWT token generation and verification working
```

### Example 3: Frontend Auth Only
```
User: /authentication T027 T028 T031

Output:
- Registration page with form
- Login page with form
- Logout functionality
- All with validation and error handling
```

---

## Validation Checklist

After implementing authentication, verify:

### Backend Security
- [ ] Passwords hashed with bcrypt 12+ rounds
- [ ] JWT tokens expire after 7 days
- [ ] JWT secret stored in environment variable
- [ ] Email validation (RFC 5322) working
- [ ] Password minimum 8 characters enforced
- [ ] Duplicate email prevented (409 Conflict)
- [ ] No passwords logged in any form

### Backend API
- [ ] Register endpoint returns 201 on success
- [ ] Register endpoint returns 400 on invalid input
- [ ] Register endpoint returns 409 on duplicate email
- [ ] Login endpoint returns 200 on success
- [ ] Login endpoint returns 401 on invalid credentials
- [ ] JWT cookie set with HttpOnly, Secure, SameSite attributes
- [ ] Logout endpoint clears JWT cookie
- [ ] Session endpoint returns user info when authenticated

### Frontend Security
- [ ] JWT tokens stored in HTTP-only cookies only
- [ ] No JWT tokens in localStorage
- [ ] All fetch requests use `credentials: 'include'`
- [ ] Better Auth handling JWT cookies automatically

### Frontend UI
- [ ] Registration page displays correctly
- [ ] Login page displays correctly
- [ ] Email validation works client-side
- [ ] Password validation works client-side
- [ ] Form submission calls correct API endpoint
- [ ] Error messages displayed appropriately
- [ ] Loading states shown during API calls
- [ ] Redirect to /tasks on successful login
- [ ] Redirect to /login on logout
- [ ] Links between register and login pages work

### End-to-End Flow
- [ ] New user can register successfully
- [ ] Registered user can login successfully
- [ ] Logged in user can access protected pages
- [ ] Logged in user can logout successfully
- [ ] Logout redirects to login page
- [ ] JWT cookie persists across page refreshes

---

## Notes

- All authentication code must reference Task IDs in comments
- Never store JWT tokens in localStorage or React state
- Better Auth handles HTTP-only cookie management automatically
- Test authentication flow completely end-to-end
- Verify password hashing with 12+ bcrypt rounds
- Check JWT expiration is exactly 7 days
- Confirm email format validation matches RFC 5322
- Ensure unique email enforcement works
- Verify cookie attributes are correct
- Test with multiple browsers for cookie isolation
