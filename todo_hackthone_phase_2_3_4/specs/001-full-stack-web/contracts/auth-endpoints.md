# API Contract: Authentication Endpoints

**Feature**: Phase II Full-Stack Web Application
**Date**: 2026-01-05
**Purpose**: Define authentication API contracts for user registration, login, and logout

---

## POST /api/auth/register

### Description
Register a new user account with email and password.

### Request

**Headers**:
```
Content-Type: application/json
```

**Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Validation**:

| Field | Type | Required | Constraints | Error Response |
|--------|--------|----------|----------------|
| email | string | Yes | Valid email format (RFC 5322), max 255 chars | 400 Bad Request |
| password | string | Yes | Min 8 characters, no constraints on max | 400 Bad Request |

### Response - Success

**Status Code**: 201 Created

**Body**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655444000",
  "email": "user@example.com",
  "message": "User registered successfully"
}
```

### Response - Error

| Status Code | Scenario | Body |
|-------------|---------|------|
| 400 Bad Request | Invalid email format | `{"error": "Invalid email format", "correlation_id": "uuid"}` |
| 400 Bad Request | Password too short (<8 chars) | `{"error": "Password must be at least 8 characters", "correlation_id": "uuid"}` |
| 409 Conflict | Email already registered | `{"error": "Email already registered", "correlation_id": "uuid"}` |
| 500 Internal Server Error | Database or unexpected error | `{"error": "Registration failed", "ref": "uuid"}` |

---

## POST /api/auth/login

### Description
Authenticate user with email and password, return JWT token stored in HTTP-only cookie.

### Request

**Headers**:
```
Content-Type: application/json
```

**Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Validation**:

| Field | Type | Required | Error Response |
|--------|--------|----------|----------------|
| email | string | Yes | Valid email format | 400 Bad Request |
| password | string | Yes | Any non-empty string | 400 Bad Request |

### Response - Success

**Status Code**: 200 OK

**Headers**:
```
Set-Cookie: token=<jwt_value>; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=604800
Content-Type: application/json
```

**Body**:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655444000",
  "email": "user@example.com",
  "message": "Login successful"
}
```

**Cookie Attributes**:
- **HttpOnly**: True (prevents JavaScript access, XSS protection)
- **Secure**: True (HTTPS only)
- **SameSite**: Strict (CSRF protection)
- **Path**: `/` (valid for entire domain)
- **Max-Age**: 604800 seconds (7 days = 7 * 24 * 60 * 60)

### Response - Error

| Status Code | Scenario | Body |
|-------------|---------|------|
| 400 Bad Request | Invalid email format | `{"error": "Invalid email format", "correlation_id": "uuid"}` |
| 401 Unauthorized | Invalid email or password | `{"error": "Invalid email or password", "correlation_id": "uuid"}` |
| 500 Internal Server Error | Database or unexpected error | `{"error": "Login failed", "ref": "uuid"}` |

---

## POST /api/auth/logout

### Description
Invalidate user session by clearing JWT cookie and redirecting to login.

### Request

**Headers**:
```
Content-Type: application/json
Cookie: token=<jwt_value>
```

**Body**: None

### Response - Success

**Status Code**: 200 OK

**Headers**:
```
Set-Cookie: token=; Expires=Thu, 01 Jan 1970 00:00:00 GMT; HttpOnly; Secure; SameSite=Strict; Path=/
Content-Type: application/json
```

**Body**:
```json
{
  "message": "Logged out successfully"
}
```

**Cookie Clearing**:
- Sets cookie to empty string
- Sets expiration to past date (1970-01-01)
- All security attributes maintained (HttpOnly, Secure, SameSite)

### Response - Error

| Status Code | Scenario | Body |
|-------------|---------|------|
| 401 Unauthorized | No valid JWT cookie | `{"error": "Not authenticated", "correlation_id": "uuid"}` |
| 500 Internal Server Error | Unexpected error | `{"error": "Logout failed", "ref": "uuid"}` |

---

## GET /api/auth/session

### Description
Validate current session and return user information if authenticated. Used by frontend to check auth state.

### Request

**Headers**:
```
Cookie: token=<jwt_value>
```

### Response - Authenticated

**Status Code**: 200 OK

**Body**:
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655444000",
    "email": "user@example.com"
  },
  "authenticated": true
}
```

### Response - Not Authenticated

**Status Code**: 401 Unauthorized

**Body**:
```json
{
  "error": "Not authenticated",
  "authenticated": false
}
```

---

## JWT Token Structure

### Payload

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655444000",
  "email": "user@example.com",
  "iat": 1736102400,
  "exp": 1736707200
}
```

### Claims

| Claim | Type | Description | Example |
|-------|--------|-------------|---------|
| sub | string | Subject: User UUID | `"550e8400-e29b-41d4-a716-446655444000"` |
| email | string | User email address | `"user@example.com"` |
| iat | integer | Issued at: Unix timestamp | `1736102400` |
| exp | integer | Expiration: Unix timestamp (max 7 days from iat) | `1736707200` |

### Token Generation Rules

- **Algorithm**: HS256 (HMAC with SHA-256)
- **Secret**: Shared between Better Auth (frontend) and FastAPI (backend)
- **Expiration**: Maximum 7 days (604800 seconds)
- **Encoding**: Base64URL-encoded JSON

---

## Security Considerations

### Password Storage

- **NEVER log passwords** (in plaintext or hashed)
- **bcrypt hashing**: Minimum 12 rounds
- **NO plaintext storage**: Only `password_hash` stored in database

### JWT Security

- **Secret strength**: Minimum 256 bits (use `openssl rand -hex 32`)
- **Signature validation**: Every request verifies JWT signature
- **Expiration enforcement**: Tokens rejected after 7 days
- **Tampering detection**: Invalid signature results in 401 Unauthorized

### Cookie Security

- **HttpOnly**: True (prevents XSS access)
- **Secure**: True (HTTPS only, production)
- **SameSite**: Strict (CSRF protection)
- **NO localStorage**: JWT never stored in browser localStorage
- **Path**: `/` (cookie valid for entire domain)

### Rate Limiting (Recommended for Production)

| Endpoint | Recommended Limit | Rationale |
|----------|-----------------|-----------|
| /api/auth/register | 3 requests per IP per hour | Prevent email abuse |
| /api/auth/login | 10 requests per IP per minute | Prevent brute force attacks |
| /api/auth/logout | 30 requests per IP per minute | Prevent session flooding |

### Input Sanitization

| Input | Sanitization |
|--------|---------------|
| email | Trim whitespace, validate format (RFC 5322) |
| password | Trim whitespace, no sanitization (raw bcrypt input) |

---

## Testing Scenarios

### Unit Tests

1. **Test email validation**:
   - Valid email format → Success
   - Invalid email format → 400 Bad Request

2. **Test password validation**:
   - Password 8+ characters → Success
   - Password <8 characters → 400 Bad Request

3. **Test duplicate email**:
   - Register user with existing email → 409 Conflict
   - Register user with new email → 201 Created

4. **Test login success**:
   - Valid credentials → 200 OK, JWT cookie set
   - JWT contains correct `sub` and `email` claims

5. **Test login failure**:
   - Invalid credentials → 401 Unauthorized

6. **Test logout**:
   - Authenticated user → 200 OK, cookie cleared
   - Unauthenticated user → 401 Unauthorized

### Integration Tests

1. **Complete auth flow**:
   - Register → Login → Access protected resource → Logout

2. **Cookie persistence**:
   - Login → Close browser → Reopen → Still authenticated (cookie persists)

3. **Cookie expiration**:
   - Login → Wait 7 days → Attempt protected access → 401 Unauthorized

4. **JWT tampering**:
   - Modify JWT cookie → Attempt protected access → 401 Unauthorized

---

## Summary

### Endpoints

| Method | Path | Auth Required | Purpose |
|--------|--------|----------------|---------|
| POST | /api/auth/register | No | Register new user |
| POST | /api/auth/login | No | Authenticate user, set JWT cookie |
| POST | /api/auth/logout | Yes | Invalidate session, clear cookie |
| GET | /api/auth/session | Yes | Check current auth state |

### Key Features

- Secure HTTP-only JWT cookies
- 7-day token expiration
- bcrypt password hashing (12+ rounds)
- Comprehensive validation and error handling
- Rate limiting recommendations
- User isolation foundation (JWT contains user_id)
