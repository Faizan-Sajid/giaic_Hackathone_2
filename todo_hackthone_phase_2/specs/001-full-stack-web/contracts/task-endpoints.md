# API Contract: Task Management Endpoints

**Feature**: Phase II Full-Stack Web Application
**Date**: 2026-01-05
**Purpose**: Define task CRUD API contracts with strict user isolation enforcement

---

## Common Headers

### Authentication Header

**Format**:
```
Authorization: Bearer <jwt_token>
```

**Note**: For Phase II, JWT is primarily stored in HTTP-only cookies. Authorization header may be used for testing or API clients.

### Content-Type

**Format**:
```
Content-Type: application/json
```

### Correlation ID (Recommended)

**Format**:
```
X-Correlation-ID: <uuid>
```

**Note**: Backend generates correlation ID if not provided. Used for request tracing and debugging.

---

## GET /api/{user_id}/tasks

### Description
Retrieve all tasks belonging to the authenticated user, ordered by creation date (newest first).

### Request

**URL Parameters**:

| Parameter | Type | Required | Description |
|-----------|--------|----------|-------------|
| user_id | string (UUID) | Yes | User's unique identifier (must match JWT `sub` claim) |

**Headers**:
```
Cookie: token=<jwt_value>
OR
Authorization: Bearer <jwt_token>
X-Correlation-ID: <uuid>
```

### Response - Success

**Status Code**: 200 OK

**Body**:
```json
{
  "tasks": [
    {
      "id": 1,
      "owner_user_id": "550e8400-e29b-41d4-a716-446655444000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-01-05T12:00:00Z",
      "updated_at": "2026-01-05T12:00:00Z"
    },
    {
      "id": 2,
      "owner_user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Call mom tonight",
      "description": "Ask about weekend plans",
      "completed": true,
      "created_at": "2026-01-04T18:00:00Z",
      "updated_at": "2026-01-04T18:30:00Z"
    }
  ],
  "count": 2
}
```

### Response - Error

| Status Code | Scenario | Body |
|-------------|---------|------|
| 401 Unauthorized | Missing or invalid JWT | `{"error": "Unauthorized", "correlation_id": "uuid"}` |
| 403 Forbidden | user_id mismatch (JWT `sub` ≠ URL `user_id`) | `{"error": "Access denied", "correlation_id": "uuid"}` |
| 500 Internal Server Error | Database failure | `{"error": "Failed to retrieve tasks", "ref": "uuid"}` |

### Example Request

```
GET /api/550e8400-e29b-41d4-a716-446655440000/tasks HTTP/1.1
Cookie: token=<valid_jwt_value>
X-Correlation-ID: 123e4567-e89b-12d3-a456-4266142555000
```

---

## POST /api/{user_id}/tasks

### Description
Create a new task for the authenticated user.

### Request

**URL Parameters**:

| Parameter | Type | Required | Description |
|-----------|--------|----------|-------------|
| user_id | string (UUID) | Yes | User's unique identifier (must match JWT `sub` claim) |

**Headers**:
```
Content-Type: application/json
Cookie: token=<jwt_value>
OR
Authorization: Bearer <jwt_token>
X-Correlation-ID: <uuid>
```

**Body**:
```json
{
  "title": "Task title here",
  "description": "Optional task description"
}
```

**Validation**:

| Field | Type | Required | Constraints | Error Response |
|--------|--------|----------|----------------|
| title | string | Yes | Min 1 char, max 200 chars | 400 Bad Request |
| description | string | No | Max 1000 chars | 400 Bad Request |

### Response - Success

**Status Code**: 201 Created

**Body**:
```json
{
  "id": 3,
  "owner_user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Task title here",
  "description": "Optional task description",
  "completed": false,
  "created_at": "2026-01-05T12:30:45Z",
  "updated_at": "2026-01-05T12:30:45Z"
}
```

### Response - Error

| Status Code | Scenario | Body |
|-------------|---------|------|
| 400 Bad Request | Invalid title or description length | `{"error": "Title is required", "field": "title", "correlation_id": "uuid"}` |
| 401 Unauthorized | Missing or invalid JWT | `{"error": "Unauthorized", "correlation_id": "uuid"}` |
| 403 Forbidden | user_id mismatch | `{"error": "Access denied", "correlation_id": "uuid"}` |
| 404 Not Found | User doesn't exist | `{"error": "User not found", "correlation_id": "uuid"}` |
| 500 Internal Server Error | Database failure | `{"error": "Failed to create task", "ref": "uuid"}` |

### Example Request

```
POST /api/550e8400-e29b-41d4-a716-446655440000/tasks HTTP/1.1
Content-Type: application/json
Cookie: token=<valid_jwt_value>
X-Correlation-ID: 123e4567-e89b-12d3-a456-4266142555000

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

---

## GET /api/{user_id}/tasks/{id}

### Description
Retrieve a specific task by ID for the authenticated user.

### Request

**URL Parameters**:

| Parameter | Type | Required | Description |
|-----------|--------|----------|-------------|
| user_id | string (UUID) | Yes | User's unique identifier (must match JWT `sub` claim) |
| id | integer | Yes | Task's unique identifier |

**Headers**:
```
Cookie: token=<jwt_value>
OR
Authorization: Bearer <jwt_token>
X-Correlation-ID: <uuid>
```

### Response - Success

**Status Code**: 200 OK

**Body**:
```json
{
  "id": 1,
  "owner_user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-05T12:00:00Z",
  "updated_at": "2026-01-05T12:00:00Z"
}
```

### Response - Error

| Status Code | Scenario | Body |
|-------------|---------|------|
| 401 Unauthorized | Missing or invalid JWT | `{"error": "Unauthorized", "correlation_id": "uuid"}` |
| 403 Forbidden | user_id mismatch OR task doesn't belong to user | `{"error": "Access denied", "correlation_id": "uuid"}` |
| 404 Not Found | Task doesn't exist | `{"error": "Task not found", "correlation_id": "uuid"}` |
| 500 Internal Server Error | Database failure | `{"error": "Failed to retrieve task", "ref": "uuid"}` |

### Example Request

```
GET /api/550e8400-e29b-41d4-a716-446655440000/tasks/1 HTTP/1.1
Cookie: token=<valid_jwt_value>
X-Correlation-ID: 123e4567-e89b-12d3-a456-4266142555000
```

---

## PUT /api/{user_id}/tasks/{id}

### Description
Update an existing task's title and/or description for the authenticated user.

### Request

**URL Parameters**:

| Parameter | Type | Required | Description |
|-----------|--------|----------|-------------|
| user_id | string (UUID) | Yes | User's unique identifier (must match JWT `sub` claim) |
| id | integer | Yes | Task's unique identifier |

**Headers**:
```
Content-Type: application/json
Cookie: token=<jwt_value>
OR
Authorization: Bearer <jwt_token>
X-Correlation-ID: <uuid>
```

**Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated task description"
}
```

**Validation**:

| Field | Type | Required | Constraints | Error Response |
|--------|--------|----------|----------------|
| title | string | No | Min 1 char, max 200 chars (if provided) | 400 Bad Request |
| description | string | No | Max 1000 chars (if provided) | 400 Bad Request |

### Response - Success

**Status Code**: 200 OK

**Body**:
```json
{
  "id": 1,
  "owner_user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Updated task title",
  "description": "Updated task description",
  "completed": false,
  "created_at": "2026-01-05T12:00:00Z",
  "updated_at": "2026-01-05T13:30:45Z"
}
```

### Response - Error

| Status Code | Scenario | Body |
|-------------|---------|------|
| 400 Bad Request | Invalid title or description length | `{"error": "Title too long", "field": "title", "correlation_id": "uuid"}` |
| 401 Unauthorized | Missing or invalid JWT | `{"error": "Unauthorized", "correlation_id": "uuid"}` |
| 403 Forbidden | user_id mismatch OR task doesn't belong to user | `{"error": "Access denied", "correlation_id": "uuid"}` |
| 404 Not Found | Task doesn't exist | `{"error": "Task not found", "correlation_id": "uuid"}` |
| 500 Internal Server Error | Database failure | `{"error": "Failed to update task", "ref": "uuid"}` |

### Example Request

```
PUT /api/550e8400-e29b-41d4-a716-446655440000/tasks/1 HTTP/1.1
Content-Type: application/json
Cookie: token=<valid_jwt_value>
X-Correlation-ID: 123e4567-e89b-12d3-a456-4266142555000

{
  "title": "Updated task title",
  "description": "Updated task description"
}
```

---

## PATCH /api/{user_id}/tasks/{id}/complete

### Description
Toggle a task's completion status (complete ↔ incomplete) for the authenticated user.

### Request

**URL Parameters**:

| Parameter | Type | Required | Description |
|-----------|--------|----------|-------------|
| user_id | string (UUID) | Yes | User's unique identifier (must match JWT `sub` claim) |
| id | integer | Yes | Task's unique identifier |

**Headers**:
```
Cookie: token=<jwt_value>
OR
Authorization: Bearer <jwt_token>
X-Correlation-ID: <uuid>
```

**Body**: None (toggle operation)

### Response - Success

**Status Code**: 200 OK

**Body**:
```json
{
  "id": 1,
  "owner_user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2026-01-05T12:00:00Z",
  "updated_at": "2026-01-05T13:45:30Z"
}
```

### Response - Error

| Status Code | Scenario | Body |
|-------------|---------|------|
| 401 Unauthorized | Missing or invalid JWT | `{"error": "Unauthorized", "correlation_id": "uuid"}` |
| 403 Forbidden | user_id mismatch OR task doesn't belong to user | `{"error": "Access denied", "correlation_id": "uuid"}` |
| 404 Not Found | Task doesn't exist | `{"error": "Task not found", "correlation_id": "uuid"}` |
| 500 Internal Server Error | Database failure | `{"error": "Failed to update task", "ref": "uuid"}` |

### Example Request

```
PATCH /api/550e8400-e29b-41d4-a716-446655440000/tasks/1/complete HTTP/1.1
Cookie: token=<valid_jwt_value>
X-Correlation-ID: 123e4567-e89b-12d3-a456-4266142555000
```

---

## DELETE /api/{user_id}/tasks/{id}

### Description
Permanently delete a task for the authenticated user.

### Request

**URL Parameters**:

| Parameter | Type | Required | Description |
|-----------|--------|----------|-------------|
| user_id | string (UUID) | Yes | User's unique identifier (must match JWT `sub` claim) |
| id | integer | Yes | Task's unique identifier |

**Headers**:
```
Cookie: token=<jwt_value>
OR
Authorization: Bearer <jwt_token>
X-Correlation-ID: <uuid>
```

**Body**: None

### Response - Success

**Status Code**: 200 OK

**Body**:
```json
{
  "id": 1,
  "message": "Task deleted successfully"
}
```

### Response - Error

| Status Code | Scenario | Body |
|-------------|---------|------|
| 401 Unauthorized | Missing or invalid JWT | `{"error": "Unauthorized", "correlation_id": "uuid"}` |
| 403 Forbidden | user_id mismatch OR task doesn't belong to user | `{"error": "Access denied", "correlation_id": "uuid"}` |
| 404 Not Found | Task doesn't exist | `{"error": "Task not found", "correlation_id": "uuid"}` |
| 500 Internal Server Error | Database failure | `{"error": "Failed to delete task", "ref": "uuid"}` |

### Example Request

```
DELETE /api/550e8400-e29b-41d4-a716-446655440000/tasks/1 HTTP/1.1
Cookie: token=<valid_jwt_value>
X-Correlation-ID: 123e4567-e89b-12d3-a456-4266142555000
```

---

## GET /health

### Description
Health check endpoint for monitoring and deployment verification. No authentication required.

### Request

**Headers**: None

**Body**: None

### Response - Healthy

**Status Code**: 200 OK

**Body**:
```json
{
  "status": "healthy",
  "database": "connected",
  "environment": "production",
  "timestamp": "2026-01-05T12:00:00Z",
  "version": "1.0.0"
}
```

### Response - Unhealthy

**Status Code**: 503 Service Unavailable

**Body**:
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "environment": "production",
  "timestamp": "2026-01-05T12:00:00Z",
  "version": "1.0.0"
}
```

---

## User Isolation Enforcement

### Multi-Layer Protection

Every protected task endpoint enforces user isolation through three independent layers:

#### Layer 1: Authentication
```
If JWT invalid or expired:
  → Return 401 Unauthorized
  → Stop processing
```

#### Layer 2: Authorization
```
Extract user_id from JWT (sub claim)
Compare: token_user_id == url_user_id
If mismatch:
  → Return 403 Forbidden
  → Stop processing
```

#### Layer 3: Data Query
```
Query: SELECT * FROM tasks WHERE id = ? AND owner_user_id = ?
If empty result:
  → Return 404 Not Found
```

### Attack Prevention Example

**Scenario**: User A (user_id=123) attempts to access User B's (user_id=456) task with id=789

```
Request: GET /api/456/tasks/789
JWT: {sub: "123", exp: ...}

Layer 1 (Auth):
✅ JWT valid
✅ Not expired
Result: PASS → Continue

Layer 2 (Authz):
Extracted: user_id = "123" from JWT
Compare: "123" == "456"
Result: MISMATCH → Return 403 Forbidden
Body: {"error": "Access denied", "correlation_id": "uuid"}
Stop processing
```

**Even if Layer 2 bypassed** (e.g., authentication bug):
```
Layer 3 (Data):
Query: SELECT * FROM tasks WHERE id = 789 AND owner_user_id = 123
Result: Empty (task 789 belongs to user 456, not 123)
Return: 404 Not Found
Body: {"error": "Task not found", "correlation_id": "uuid"}
```

**Conclusion**: Three independent layers ensure user isolation. Attack requires bypassing all three simultaneously, which is virtually impossible.

---

## Pagination (Optional Future Enhancement)

### Query Parameters

**GET /api/{user_id}/tasks** may support:

| Parameter | Type | Default | Description |
|-----------|--------|---------|-------------|
| limit | integer | 50 | Maximum tasks to return |
| offset | integer | 0 | Number of tasks to skip |
| completed | boolean | null | Filter by completion status |

### Example with Pagination

```
GET /api/550e8400-e29b-41d4-a716-446655440000/tasks?completed=false&limit=10&offset=20 HTTP/1.1
```

### Response with Pagination

```json
{
  "tasks": [...],
  "count": 100,
  "limit": 10,
  "offset": 20,
  "has_more": true
}
```

**Note**: Pagination is optional for Phase II. May be added in Phase III or V based on user feedback.

---

## Summary

### Endpoints

| Method | Path | Auth Required | Purpose |
|--------|--------|----------------|---------|
| GET | /api/{user_id}/tasks | Yes | List user's tasks |
| POST | /api/{user_id}/tasks | Yes | Create new task |
| GET | /api/{user_id}/tasks/{id} | Yes | Get task details |
| PUT | /api/{user_id}/tasks/{id} | Yes | Update task |
| PATCH | /api/{user_id}/tasks/{id}/complete | Yes | Toggle completion |
| DELETE | /api/{user_id}/tasks/{id} | Yes | Delete task |
| GET | /health | No | Health check |

### Key Features

- RESTful API design with proper HTTP methods
- Strict multi-layer user isolation (auth, authz, data)
- Comprehensive validation and error handling
- Correlation ID support for request tracing
- HTTP status code compliance (401, 403, 404, 400, 409, 500)
- Support for JWT in cookies or Authorization header
- Health check endpoint for monitoring
