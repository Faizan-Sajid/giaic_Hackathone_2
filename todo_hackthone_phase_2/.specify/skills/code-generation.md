# Code Generation for Specific File

**Purpose**: Generate implementation for a specific file/task
**Coverage**: Any single task (T001-T068) - Per-task flexibility
**Project**: Phase II Full-Stack Web Application

---

## Skill Description

This skill generates implementation for a specific file or task in Phase II Todo Application. It provides focused, targeted code generation for any task from the task list including:

- Backend files (models, services, routes, middleware, utilities)
- Frontend files (pages, components, contexts, utilities)
- Configuration files (pyproject.toml, package.json, .env files)
- Test files (unit tests, integration tests, E2E tests)
- Any specific file needed for the project

---

## Usage

### Generate Specific File
```
/codegen backend/src/models/user.py
```

### Generate by Task ID
```
/codegen T008
```

### Generate Multiple Files
```
/codegen backend/src/models/user.py backend/src/models/task.py
```

### Generate Frontend Component
```
/codegen frontend/src/components/TaskList.tsx
```

---

## Implementation Guidelines

### Code Standards

**Backend (Python)**:
- Follow PEP 8 style guide
- Use type hints for all functions and variables
- Include inline comments referencing Task IDs and Spec sections
- Use async/await for all database operations
- Proper docstrings for all functions
- Handle exceptions appropriately

**Frontend (TypeScript)**:
- Use TypeScript strict mode
- Functional components with hooks
- Client components marked with 'use client' directive
- Proper TypeScript types for all props and interfaces
- Include inline comments referencing Task IDs and Spec sections
- Handle loading and error states appropriately

### Comment Requirements

**All code MUST include**:
```python
# Task: TXXX
# Spec: Section reference (e.g., FR-001, SEC-001)
# Implementation: Brief description
```

**Example**:
```python
# Task: T008
# Spec: User Entity (data-model.md lines 87-180)
# Implementation: User SQLModel with UUID primary key, unique email, bcrypt password hash
class User(SQLModel, table=True):
    ...
```

---

## Supported Files

### Backend Files

**Models**:
- `backend/src/models/user.py` - User SQLModel (T008)
- `backend/src/models/task.py` - Task SQLModel (T009)

**Core Utilities**:
- `backend/src/core/database.py` - Database engine and session (T007)
- `backend/src/core/security.py` - JWT and password hashing (T015-T016)
- `backend/src/core/logging.py` - Structured logging (T012)
- `backend/src/core/config.py` - CORS and config (T013)
- `backend/src/core/exceptions.py` - Error handling (T014)

**Services**:
- `backend/src/services/auth_service.py` - Authentication service (T021-T022)
- `backend/src/services/task_service.py` - Task CRUD service (T033)

**API Routes**:
- `backend/src/api/routes/auth.py` - Auth endpoints (T023-T026)
- `backend/src/api/routes/tasks.py` - Task endpoints (T035-T040)
- `backend/src/api/routes/health.py` - Health check (T057)
- `backend/src/api/deps.py` - Dependencies (T034)

**Main Entry Point**:
- `backend/src/main.py` - FastAPI app (T017)

**Configuration**:
- `backend/pyproject.toml` - Python dependencies (T002)
- `backend/alembic.ini` - Alembic config (T010)
- `backend/.env.example` - Environment variables (T005)

**Tests**:
- `backend/tests/conftest.py` - Test fixtures
- `backend/tests/unit/test_auth.py` - Auth unit tests
- `backend/tests/unit/test_tasks.py` - Task unit tests
- `backend/tests/integration/test_auth_flow.py` - Auth integration tests
- `backend/tests/integration/test_task_api.py` - Task API tests

### Frontend Files

**Pages**:
- `frontend/src/app/(auth)/login/page.tsx` - Login page (T028)
- `frontend/src/app/(auth)/register/page.tsx` - Register page (T027)
- `frontend/src/app/(dashboard)/tasks/page.tsx` - Tasks page (T047)

**Components**:
- `frontend/src/components/ProtectedRoute.tsx` - Auth guard (T020)
- `frontend/src/components/TaskList.tsx` - Task display (T041)
- `frontend/src/components/TaskForm.tsx` - Task form (T042)

**Contexts**:
- `frontend/src/contexts/AuthContext.tsx` - Auth state (T019)

**Utilities**:
- `frontend/src/lib/api/client.ts` - API client (T018)

**Configuration**:
- `frontend/package.json` - Node dependencies (T004)
- `frontend/tsconfig.json` - TypeScript config
- `frontend/tailwind.config.js` - Tailwind config
- `frontend/next.config.js` - Next.js config
- `frontend/.env.example` - Environment variables (T006)
- `frontend/src/middleware.ts` - Middleware

**Tests**:
- `frontend/tests/unit/test-utils.tsx` - Test utilities
- `frontend/tests/e2e/user-journey.spec.ts` - E2E tests

---

## Examples

### Example 1: Generate User Model
```
User: /codegen backend/src/models/user.py

Output:
- Creates backend/src/models/user.py
- Implements User SQLModel with id, email, password_hash, created_at
- Includes Task ID (T008) and Spec references
- Follows PEP 8 style guide
```

### Example 2: Generate TaskList Component
```
User: /codegen frontend/src/components/TaskList.tsx

Output:
- Creates frontend/src/components/TaskList.tsx
- Implements task list display with React hooks
- Includes Task ID (T041) and Spec references
- Follows TypeScript strict mode
- Includes loading and error states
```

### Example 3: Generate Complete AuthService
```
User: /codegen T021 T022

Output:
- Creates backend/src/services/auth_service.py
- Implements hash_password() and verify_password()
- Implements create_jwt()
- Includes Task IDs (T021-T022) and Spec references
- Follows bcrypt 12+ rounds requirement
- Follows JWT 7-day expiration requirement
```

### Example 4: Generate Login Page
```
User: /codegen T028 T030

Output:
- Creates frontend/src/app/(auth)/login/page.tsx
- Implements login form with email/password fields
- Integrates with /api/auth/login endpoint
- Includes Task IDs (T028-T030) and Spec references
- Follows TypeScript strict mode
- Includes validation and error handling
```

### Example 5: Generate Multiple Backend Files
```
User: /codegen T008 T009 T010 T011

Output:
- Creates backend/src/models/user.py (T008)
- Creates backend/src/models/task.py (T009)
- Creates backend/alembic.ini (T010)
- Creates backend/alembic/versions/001_initial_schema.py (T011)
```

---

## Code Generation Rules

### DO's

✅ DO include Task ID and Spec references in comments
✅ DO follow exact technology versions from Constitution
✅ DO use proper type hints (Python) or TypeScript strict mode
✅ DO include docstrings for all functions
✅ DO handle all error cases appropriately
✅ DO follow PEP 8 (Python) or TypeScript best practices
✅ DO use async/await for database operations (backend)
✅ DO include loading and error states (frontend)
✅ DO validate inputs before processing
✅ DO enforce user isolation in all task queries

### DON'Ts

❌ DON'T skip Task ID or Spec references in comments
❌ DON'T use hardcoded secrets or tokens
❌ DON'T log passwords or sensitive data
❌ DON'T bypass user_id validation
❌ DON'T use raw SQL queries (use ORM only)
❌ DON'T store JWT in localStorage (frontend)
❌ DON'T skip type hints or TypeScript types
❌ DON'T ignore error handling
❌ DON'T use deprecated or incorrect technology versions

---

## File Template Structure

### Python File Template
```python
# Task: TXXX
# Spec: [Section reference]
# Implementation: [Brief description]

from typing import [imports]
from [module] import [imports]

class [ClassName]:
    """
    [Description]
    Task: TXXX
    Spec: [Section reference]
    """

    def [method_name](self, [params]) -> [return_type]:
        """
        [Method description]
        Task: TXXX
        Spec: [Section reference]
        """
        # Implementation
        pass
```

### TypeScript File Template
```typescript
// Task: TXXX
// Spec: [Section reference]
// Implementation: [Brief description]

'use client'

import { useState, useEffect } from 'react'

export default function [ComponentName]({ [props] }: [PropsType]) {
  /**
   * Component description
   * Task: TXXX
   * Spec: [Section reference]
   */
  const [state, setState] = useState(initial_value)

  useEffect(() => {
    // Effect
  }, [dependency])

  return (
    <div>
      {/* JSX */}
    </div>
  )
}
```

---

## Verification Checklist

After generating code, verify:

### Code Quality
- [ ] File follows PEP 8 (Python) or TypeScript strict mode
- [ ] All functions/methods have type hints
- [ ] Docstrings present for all functions
- [ ] Code is readable and well-formatted
- [ ] No hardcoded values that should be in config

### Task References
- [ ] Task ID included in comments (e.g., T008)
- [ ] Spec section referenced (e.g., FR-001)
- [ ] Brief description of implementation
- [ ] References are accurate and helpful

### Requirements Compliance
- [ ] Constitutional requirements met
- [ ] Technology versions match Constitution
- [ ] Security requirements implemented
- [ ] Data isolation enforced (if applicable)
- [ ] Input validation included
- [ ] Error handling appropriate

### Dependencies
- [ ] All required imports included
- [ ] No circular dependencies
- [ ] Dependencies are from project stack
- [ ] No missing dependencies

---

## Notes

- This skill provides flexible, per-task code generation
- Use for specific files when you need targeted implementation
- Always reference Task IDs and Spec sections in comments
- Never manually modify generated code without understanding impact
- Follow the generated code exactly as written
- Test generated code before moving to next task
- Use `/testing` skill to verify implementation
- All generated code is production-ready and follows best practices
