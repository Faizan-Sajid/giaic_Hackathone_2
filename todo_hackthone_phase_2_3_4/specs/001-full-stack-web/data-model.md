# Data Model: Phase II Full-Stack Web Application

**Feature**: Phase II Full-Stack Web Application with JWT Authentication
**Date**: 2026-01-05
**Purpose**: Define entity schemas, relationships, validation rules, and state transitions

---

## Entity: User

### Purpose
Represents a registered user account with authentication credentials and metadata. Users are the primary actors who create and manage tasks.

### Fields

| Field | Type | Constraints | Validation | Purpose |
|--------|--------|-------------|-----------|
| id | string (UUID) | Primary key, auto-generated | Unique identifier for user |
| email | string | Unique, max 255 chars, email format | User's email address (login credential) |
| password_hash | string | bcrypt hash (12+ rounds) | Hashed password (never stored in plaintext) |
| created_at | timestamp | Auto-generated | Account creation timestamp |

### Relationships

| Relationship | Type | Target Entity | Description |
|-------------|--------|----------------|-------------|
| tasks | One-to-Many | Task | One user has many tasks |

### Constraints

- **UNIQUE(email)**: No two users can have the same email address
- **NOT NULL(email)**: Email is required for account creation
- **NOT NULL(password_hash)**: Password is required (as hash)
- **email format**: Must comply with RFC 5322 standards

### State Transitions

**User Account Lifecycle**:

```
[Unregistered] --register--> [Active] --logout--> [Inactive] --login--> [Active]
```

**States**:
- **Unregistered**: User does not exist in system (implicit, not stored state)
- **Active**: User can authenticate and access protected resources
- **Inactive**: User session ended (logout), cannot access protected resources until re-authenticated

### Schema Definition (SQL)

```sql
CREATE TABLE users (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL CHECK (length(email) >= 1 AND length(email) <= 255),
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

### SQLModel Definition (Python)

```python
from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True
    )
    email: str = Field(
        unique=True,
        max_length=255,
        index=True
    )
    password_hash: str = Field()
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## Entity: Task

### Purpose
Represents a todo item belonging to a specific user. Tasks are the core data entity managed by users.

### Fields

| Field | Type | Constraints | Validation | Purpose |
|--------|--------|-------------|-----------|
| id | integer | Primary key, auto-increment | Unique identifier for task |
| owner_user_id | string (UUID) | Foreign key to users, NOT NULL | Task owner (ensures isolation) |
| title | string | Min 1 char, max 200 chars, NOT NULL | Task title/description |
| description | string | Max 1000 chars, optional | Additional task details |
| completed | boolean | Default FALSE | Task completion status |
| created_at | timestamp | Auto-generated | Task creation timestamp |
| updated_at | timestamp | Auto-updated on modification | Last modification timestamp |

### Relationships

| Relationship | Type | Target Entity | Description |
|-------------|--------|----------------|-------------|
| owner | Many-to-One | User | Each task belongs to exactly one user |

### Constraints

- **PRIMARY KEY(id)**: Unique integer identifier
- **FOREIGN KEY(owner_user_id) REFERENCES users(id)**: Task must belong to valid user
- **NOT NULL(owner_user_id)**: Every task must have an owner
- **NOT NULL(title)**: Title is required
- **CHECK(length(title) >= 1 AND length(title) <= 200)**: Title length validation
- **CHECK(length(description) <= 1000)**: Description length validation (if provided)
- **DEFAULT completed = FALSE**: New tasks start as incomplete
- **CASCADE DELETE(owner_user_id)**: Deleting a user deletes all their tasks

### State Transitions

**Task Lifecycle**:

```
[Created] --complete--> [Completed] --toggle--> [Incomplete] --complete--> [Completed]
                      |                     ^
                      v                     |
                   [Deleted] ------------------+
```

**States**:
- **Created**: Task initially created by user (not completed)
- **Completed**: User marked task as done
- **Incomplete**: User toggled task from completed back to active
- **Deleted**: Task permanently removed from system

**Transition Rules**:
- **Created → Completed**: User marks task as complete
- **Completed → Incomplete**: User unchecks task, marks as incomplete
- **Incomplete → Completed**: User re-completes previously incomplete task
- **Created → Deleted**: User deletes task before completion
- **Completed → Deleted**: User deletes completed task
- **Incomplete → Deleted**: User deletes incomplete task

### Schema Definition (SQL)

```sql
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  owner_user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL CHECK (length(title) >= 1 AND length(title) <= 200),
  description TEXT CHECK (length(description) <= 1000),
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_tasks_owner_user_id ON tasks(owner_user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

### SQLModel Definition (Python)

```python
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
if TYPE_CHECKING:
    from .user import User

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_user_id: str = Field(foreign_key="user.id")
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

## Data Isolation Strategy

### Multi-Layer User Isolation

**Purpose**: Ensure no user can ever access another user's data under any circumstance.

#### Layer 1: Authentication (JWT Token)
- JWT token contains `sub` claim with user_id
- Token must be valid and not expired
- Middleware extracts user_id before request processing

**Attack Prevention**:
- Expired tokens rejected (401 Unauthorized)
- Tampered tokens rejected (invalid signature)
- Missing tokens rejected (no Authorization header)

#### Layer 2: Authorization (User ID Matching)
- URL contains `{user_id}` parameter (e.g., `/api/123/tasks`)
- Middleware compares: `token.sub == url_user_id`
- Mismatch results in 403 Forbidden

**Attack Prevention**:
- User A cannot access User B's tasks by changing URL
- Token reuse across different user IDs impossible
- URL parameter tampering detected

#### Layer 3: Data Query Filtering
- SQL query includes `WHERE owner_user_id = authenticated_user_id`
- ORM enforces filter at database level
- Even if previous layers bypassed, query returns empty results

**Attack Prevention**:
- SQL injection cannot modify query to return other users' tasks
- ORM prevents raw SQL injection
- Database-level filter ensures isolation

### Example: Prevention of Cross-User Access

**Attack Scenario**: User A (user_id=123) attempts to access User B's (user_id=456) task with id=789

```
Request: GET /api/456/tasks/789
Authorization: Bearer <JWT-with-sub=123>

Layer 1 (JWT Validation):
✅ Token valid
✅ Token not expired
Extracted: user_id = "123"

Layer 2 (Authorization Check):
❌ token_user_id (123) != url_user_id (456)
Result: 403 Forbidden

Even if Layer 2 bypassed:
Layer 3 (Data Query):
SELECT * FROM tasks WHERE id = 789 AND owner_user_id = 123
Result: Empty (task 789 belongs to user 456, not 123)
Response: 404 Not Found
```

**Conclusion**: Three independent layers ensure user isolation. Attack requires bypassing all three simultaneously, which is virtually impossible.

---

## Validation Rules

### User Validation

**Registration Validation**:

| Field | Rule | Error Handling |
|--------|--------|----------------|
| email | Must be valid email format (RFC 5322) | 400 Bad Request: "Invalid email format" |
| email | Must be unique (not already registered) | 409 Conflict: "Email already registered" |
| password | Minimum 8 characters | 400 Bad Request: "Password must be at least 8 characters" |
| password | Cannot be empty | 400 Bad Request: "Password is required" |

**Login Validation**:

| Field | Rule | Error Handling |
|--------|--------|----------------|
| email | Must exist in database | 401 Unauthorized: "Invalid email or password" |
| password | Must match bcrypt hash | 401 Unauthorized: "Invalid email or password" |

### Task Validation

**Create Task Validation**:

| Field | Rule | Error Handling |
|--------|--------|----------------|
| title | Minimum 1 character | 400 Bad Request: "Title is required" |
| title | Maximum 200 characters | 400 Bad Request: "Title too long (max 200 characters)" |
| description | Maximum 1000 characters | 400 Bad Request: "Description too long (max 1000 characters)" |

**Update Task Validation**:

| Field | Rule | Error Handling |
|--------|--------|----------------|
| id | Must exist and belong to user | 404 Not Found: "Task not found" or 403 Forbidden: "Access denied" |
| title | Minimum 1 character (if provided) | 400 Bad Request: "Title is required" |
| title | Maximum 200 characters (if provided) | 400 Bad Request: "Title too long (max 200 characters)" |
| description | Maximum 1000 characters (if provided) | 400 Bad Request: "Description too long (max 1000 characters)" |

**Delete Task Validation**:

| Field | Rule | Error Handling |
|--------|--------|----------------|
| id | Must exist and belong to user | 404 Not Found: "Task not found" or 403 Forbidden: "Access denied" |

---

## Index Strategy

### Performance Optimization

**Indexes for Users Table**:
```sql
CREATE INDEX idx_users_email ON users(email);
-- Purpose: Fast duplicate email lookup during registration
-- Expected: Query frequency: High (every registration)
```

**Indexes for Tasks Table**:
```sql
CREATE INDEX idx_tasks_owner_user_id ON tasks(owner_user_id);
-- Purpose: Fast user task list retrieval
-- Expected: Query frequency: Very High (every page load)

CREATE INDEX idx_tasks_completed ON tasks(completed);
-- Purpose: Fast filtering by completion status
-- Expected: Query frequency: High (toggle operations)
```

### Query Patterns

**User Task List**:
```sql
SELECT * FROM tasks
WHERE owner_user_id = 'user-uuid'
ORDER BY created_at DESC;
-- Uses: idx_tasks_owner_user_id
-- Expected performance: <10ms for 100 tasks
```

**Single Task Retrieval**:
```sql
SELECT * FROM tasks
WHERE id = 123 AND owner_user_id = 'user-uuid';
-- Uses: Primary key scan + idx_tasks_owner_user_id
-- Expected performance: <5ms
```

**Task Search** (Future Phase III):
```sql
SELECT * FROM tasks
WHERE owner_user_id = 'user-uuid'
  AND title ILIKE '%keyword%'
ORDER BY created_at DESC;
-- Uses: idx_tasks_owner_user_id
-- Expected performance: <50ms for 1000 tasks
```

---

## Migration Strategy

### Initial Schema Migration

**Version**: 001_initial_schema

**Up Migration**:
```sql
-- Create users table
CREATE TABLE users (
  id TEXT PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL CHECK (length(email) >= 1 AND length(email) <= 255),
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create tasks table
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  owner_user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL CHECK (length(title) >= 1 AND length(title) <= 200),
  description TEXT CHECK (length(description) <= 1000),
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_tasks_owner_user_id ON tasks(owner_user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
```

**Down Migration**:
```sql
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS users;
```

### Future Migrations (Examples)

**Adding Priority Field (Phase V)**:
```sql
ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'medium';
ALTER TABLE tasks ADD CONSTRAINT chk_priority CHECK (priority IN ('high', 'medium', 'low'));
```

**Adding Tags Array (Phase V)**:
```sql
ALTER TABLE tasks ADD COLUMN tags TEXT[] DEFAULT '{}';
CREATE INDEX idx_tasks_tags ON tasks USING gin(tags);
```

---

## Data Integrity

### Constraints Summary

| Constraint | Entity | Type | Description |
|------------|--------|-------------|
| PRIMARY KEY | User, Task | Unique identifier |
| UNIQUE(email) | User | No duplicate emails |
| NOT NULL(email, password_hash) | User | Required fields |
| FOREIGN KEY(owner_user_id) | Task | Referential integrity |
| CHECK(length(title) >= 1 AND <= 200) | Task | Title length validation |
| CHECK(length(description) <= 1000) | Task | Description length validation |
| DEFAULT completed = FALSE | Task | Initial state |
| CASCADE DELETE | Task (owner_user_id) | User deletion removes tasks |

### Cascade Behavior

**User Deletion**:
```
DELETE FROM users WHERE id = 'user-uuid';
-- CASCADE: Automatically deletes all tasks with owner_user_id = 'user-uuid'
-- Rationale: User's data belongs to them, cleanup on account deletion
```

### Transaction Requirements

**Task Creation**:
```python
async def create_task_with_transaction(session: AsyncSession, task: Task):
    async with session.begin():
        # Verify user exists
        user = await session.get(User, task.owner_user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Create task
        session.add(task)
        await session.commit()
```

**Batch Operations**:
```python
# Multiple tasks created in single transaction
async with session.begin():
    for task_data in task_list:
        task = Task(**task_data)
        session.add(task)
    await session.commit()
    # All tasks succeed or all fail
```

---

## Summary

### Entities
- **User**: Authentication and account management
- **Task**: Todo items with user ownership

### Relationships
- One User has Many Tasks (1:N)
- Each Task belongs to exactly one User

### Key Features
- Strict data isolation via multi-layer security
- Foreign key constraints with cascade delete
- Indexes for performance optimization
- Comprehensive validation rules
- Support for stateless JWT authentication

### Compliance
- ✅ Constitutional compliance verified
- ✅ Security requirements met (bcrypt, user isolation)
- ✅ Performance optimized (indexes, async operations)
- ✅ Data integrity ensured (constraints, transactions)
