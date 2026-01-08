# Tasks: Phase II Full-Stack Web Application

**Input**: Design documents from `/specs/001-full-stack-web/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - only included if explicitly requested in feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/src/`
- **Frontend**: `frontend/src/`
- Tests: `backend/tests/` and `frontend/tests/`

---

## Phase 1: Setup (Project Initialization)

**Purpose**: Backend and frontend project structure setup

- [ ] T001 Create backend directory structure: backend/src/{models,api/routes,core,main.py}, backend/tests/{unit,integration,conftest.py}
- [ ] T002 Initialize Python backend with UV: backend/pyproject.toml with fastapi 0.115+, sqlmodel 0.0.22+, asyncpg, python-jose[cryptography], bcrypt, alembic, uvicorn[standard], pytest, pytest-asyncio, httpx
- [ ] T003 [P] Create frontend Next.js 15+ project structure: frontend/src/app/{(auth),(dashboard),api,components,lib}, frontend/tests/{e2e,unit}
- [ ] T004 [P] Initialize frontend with package.json: next 15+, react 18+, typescript 5.7+, better-auth, tailwindcss, jest, @playwright/test
- [ ] T005 Create backend/.env.example with DATABASE_URL, JWT_SECRET, JWT_ALGORITHM, JWT_EXPIRATION_DAYS, FRONTEND_URL, LOG_LEVEL, ENVIRONMENT
- [ ] T006 [P] Create frontend/.env.example with NEXT_PUBLIC_API_URL, BETTER_AUTH_SECRET, BETTER_AUTH_URL

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T007 Configure async SQLModel database engine in backend/src/core/database.py with connection pooling (pool_size=10, max_overflow=10)
- [ ] T008 [P] Create User SQLModel in backend/src/models/user.py with id (UUID), email (unique), password_hash, created_at
- [ ] T009 [P] Create Task SQLModel in backend/src/models/task.py with id, owner_user_id (FK), title, description, completed, created_at, updated_at
- [ ] T010 Initialize Alembic in backend/ with alembic.ini and backend/alembic/versions/ structure
- [ ] T011 Generate initial Alembic migration 001_initial_schema creating users and tasks tables with constraints and indexes
- [ ] T012 [P] Implement structured JSON logging with correlation ID middleware in backend/src/core/logging.py
- [ ] T013 [P] Implement CORS middleware configuration in backend/src/core/config.py with FRONTEND_URL origin
- [ ] T014 Implement global error handling middleware in backend/src/core/exceptions.py with proper HTTP status codes (401, 403, 404, 400, 409, 500)
- [ ] T015 [P] Implement JWT verification utility in backend/src/core/security.py with decode function extracting user_id from sub claim
- [ ] T016 Implement password hashing utility in backend/src/core/security.py with bcrypt 12+ rounds
- [ ] T017 Create FastAPI application entry point in backend/src/main.py with router mounting and middleware stack
- [ ] T018 [P] Create API client utility in frontend/src/lib/api/client.ts for HTTP requests with cookie support
- [ ] T019 [P] Implement AuthContext provider in frontend/src/contexts/AuthContext.tsx with React Context API for session state
- [ ] T020 Implement ProtectedRoute component in frontend/src/components/ProtectedRoute.tsx for auth-gated pages

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Secure Login (Priority: P1) 🎯 MVP

**Goal**: Enable new users to register accounts with email/password and securely log in to access their personal task dashboard

**Independent Test**: New user completes registration → receives confirmation → logs in with credentials → accesses dashboard → logs out, all without seeing other users' data

### Implementation for User Story 1

- [ ] T021 [P] [US1] Create AuthService in backend/src/services/auth_service.py with hash_password and verify_password functions using bcrypt 12+ rounds
- [ ] T022 [P] [US1] Create JWT generation function in AuthService returning token with sub=user_id, email, iat, exp (7 days)
- [ ] T023 [P] [US1] Implement POST /api/auth/register endpoint in backend/src/api/routes/auth.py with email validation, password hashing, user creation, 201/400/409 responses
- [ ] T024 [P] [US1] Implement POST /api/auth/login endpoint in backend/src/api/routes/auth.py with credential verification, JWT cookie setting, 200/401 responses
- [ ] T025 [P] [US1] Implement POST /api/auth/logout endpoint in backend/src/api/routes/auth.py with JWT cookie clearing, 200/401 responses
- [ ] T026 [P] [US1] Implement GET /api/auth/session endpoint in backend/src/api/routes/auth.py returning user info if authenticated, 401/200 responses
- [ ] T027 [US1] Create registration page UI in frontend/src/app/(auth)/register/page.tsx with email/password form and validation
- [ ] T028 [US1] Create login page UI in frontend/src/app/(auth)/login/page.tsx with email/password form and validation
- [ ] T029 [US1] Integrate register form with POST /api/auth/register endpoint in frontend/src/app/(auth)/register/page.tsx
- [ ] T030 [US1] Integrate login form with POST /api/auth/login endpoint in frontend/src/app/(auth)/login/page.tsx with Better Auth cookie handling
- [ ] T031 [US1] Implement logout function in frontend calling POST /api/auth/logout and redirecting to login page
- [ ] T032 [US1] Add error handling and display for auth forms (email format, password length, duplicate email, invalid credentials)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Task Management with Strict User Isolation (Priority: P1)

**Goal**: Enable authenticated users to create, view, edit, and delete their own tasks while being completely isolated from other users' data

**Independent Test**: User A creates tasks → User B logs in → User B cannot see User A's tasks → User B creates tasks → User A cannot see User B's tasks → Both can only access their own data

### Implementation for User Story 2

- [ ] T033 [P] [US2] Create TaskService in backend/src/services/task_service.py with create_task, list_tasks, get_task, update_task, delete_task, toggle_complete methods
- [ ] T034 [P] [US2] Implement user_id validation middleware in backend/src/api/deps.py checking token.sub == request.path.user_id
- [ ] T035 [P] [US2] Implement GET /api/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py returning only authenticated user's tasks, 401/403/500 responses
- [ ] T036 [P] [US2] Implement POST /api/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py creating task with user_id validation, 201/400/401/403/404/500 responses
- [ ] T037 [P] [US2] Implement GET /api/{user_id}/tasks/{id} endpoint in backend/src/api/routes/tasks.py returning specific task if owned by user, 401/403/404/500 responses
- [ ] T038 [P] [US2] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/src/api/routes/tasks.py updating task if owned by user, 200/400/401/403/404/500 responses
- [ ] T039 [P] [US2] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/src/api/routes/tasks.py toggling completion if owned by user, 200/401/403/404/500 responses
- [ ] T040 [P] [US2] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/src/api/routes/tasks.py deleting task if owned by user, 200/401/403/404/500 responses
- [ ] T041 [US2] Create TaskList component in frontend/src/components/TaskList.tsx displaying user's tasks with title, description, completed status
- [ ] T042 [US2] Create TaskForm component in frontend/src/components/TaskForm.tsx for creating and updating tasks with validation
- [ ] T043 [US2] Implement task creation in TaskForm calling POST /api/{user_id}/tasks with title/description
- [ ] T044 [US2] Implement task update in TaskForm calling PUT /api/{user_id}/tasks/{id} with updated fields
- [ ] T045 [US2] Implement task completion toggle in TaskList calling PATCH /api/{user_id}/tasks/{id}/complete
- [ ] T046 [US2] Implement task delete in TaskList calling DELETE /api/{user_id}/tasks/{id} with confirmation
- [ ] T047 [US2] Create tasks page UI in frontend/src/app/(dashboard)/tasks/page.tsx with ProtectedRoute, TaskList, and TaskForm
- [ ] T048 [US2] Add loading states and error handling for all task operations in TaskList and TaskForm components
- [ ] T049 [US2] Implement client-side validation for task title (1-200 chars) and description (max 1000 chars)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Data Persistence Across Sessions (Priority: P2)

**Goal**: Ensure users' tasks and account data persist securely across login sessions and browser restarts with no data loss

**Independent Test**: User logs in, creates tasks, logs out, closes browser, reopens, logs back in, and all previously created tasks are present and unchanged

### Implementation for User Story 3

- [ ] T050 [P] [US3] Verify all task queries in TaskService include ORDER BY created_at DESC in backend/src/services/task_service.py
- [ ] T051 [P] [US3] Verify all task update operations update updated_at timestamp in backend/src/services/task_service.py
- [ ] T052 [US3] Verify database migration includes CASCADE DELETE for owner_user_id foreign key in backend/alembic/versions/001_initial_schema.py
- [ ] T053 [US3] Add database connection retry logic in backend/src/core/database.py for temporary connection failures
- [ ] T054 [US3] Implement graceful error handling in API client for network errors in frontend/src/lib/api/client.ts
- [ ] T055 [US3] Add optimistic refresh strategy in TaskList component for concurrent session updates in frontend/src/components/TaskList.tsx
- [ ] T056 [US3] Verify HTTP-only cookie persistence across browser sessions in frontend middleware configuration

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Health Check & API Documentation

**Purpose**: Service monitoring and developer documentation

- [ ] T057 Implement GET /health endpoint in backend/src/api/routes/health.py returning status, database connectivity, environment info
- [ ] T058 Enable OpenAPI/Swagger automatic documentation in backend/src/main.py with /docs endpoint
- [ ] T059 Verify all API routes have proper Pydantic request/response models for auto-generated docs

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T060 [P] Run quickstart.md validation to ensure all setup steps work correctly
- [ ] T061 Code cleanup and refactoring to ensure adherence to PEP 8 (Python) and TypeScript strict mode
- [ ] T062 Add structured JSON logging to all backend endpoints with correlation IDs
- [ ] T063 Verify no sensitive data (passwords, tokens, PII) is logged in backend/src/core/logging.py
- [ ] T064 Verify all error messages are user-friendly and don't expose internal details in backend/src/core/exceptions.py
- [ ] T065 Verify JWT cookies have HttpOnly, Secure, SameSite=Strict attributes set correctly
- [ ] T066 Add input validation for email format (RFC 5322) in registration endpoint in backend/src/api/routes/auth.py
- [ ] T067 Add input validation for task title length (1-200 chars) and description (max 1000 chars) in task endpoints
- [ ] T068 Verify CORS configuration restricts to specific frontend origin in backend/src/core/config.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3, 4, 5)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P1 → P2)
- **Health Check (Phase 6)**: Depends on Foundational phase completion
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on US1 but uses same auth infrastructure
- **User Story 3 (P2)**: Depends on US2 completion - adds persistence guarantees to task management

### Within Each User Story

- Services before endpoints
- Authentication endpoints before auth UI
- TaskService before task endpoints
- Task endpoints before task UI components
- Core implementation before integration

### Parallel Opportunities

- All Setup tasks (T001-T006) can run in parallel
- All Foundational tasks marked [P] (T008-T020) can run in parallel (within Phase 2)
- Once Foundational phase completes, US1 (T021-T032) and US2 (T033-T049) can be worked on in parallel (if team capacity allows)
- All task endpoints in US2 marked [P] (T035-T040) can run in parallel
- US3 tasks marked [P] (T050-T056) can run in parallel
- Polish tasks marked [P] (T060, T062) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all endpoints for User Story 1 together:
Task: "Implement POST /api/auth/register endpoint in backend/src/api/routes/auth.py"
Task: "Implement POST /api/auth/login endpoint in backend/src/api/routes/auth.py"
Task: "Implement POST /api/auth/logout endpoint in backend/src/api/routes/auth.py"
Task: "Implement GET /api/auth/session endpoint in backend/src/api/routes/auth.py"

# Launch all UI components for User Story 1 together:
Task: "Create registration page UI in frontend/src/app/(auth)/register/page.tsx"
Task: "Create login page UI in frontend/src/app/(auth)/login/page.tsx"
```

## Parallel Example: User Story 2

```bash
# Launch all task endpoints together:
Task: "Implement GET /api/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py"
Task: "Implement POST /api/{user_id}/tasks endpoint in backend/src/api/routes/tasks.py"
Task: "Implement GET /api/{user_id}/tasks/{id} endpoint in backend/src/api/routes/tasks.py"
Task: "Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/src/api/routes/tasks.py"
Task: "Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/src/api/routes/tasks.py"
Task: "Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/src/api/routes/tasks.py"

# Launch all frontend components together:
Task: "Create TaskList component in frontend/src/components/TaskList.tsx"
Task: "Create TaskForm component in frontend/src/components/TaskForm.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T020) - **CRITICAL: blocks all stories**
3. Complete Phase 3: User Story 1 (T021-T032)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready (auth flow working)

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP auth!)
3. Add User Story 2 → Test independently → Deploy/Demo (full task management!)
4. Add User Story 3 → Test independently → Deploy/Demo (persistence guaranteed)
5. Add Health Check + Polish → Final production-ready system
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup (Phase 1) and Foundational (Phase 2) together
2. Once Foundational is done:
   - Developer A: User Story 1 (auth flow) - T021-T032
   - Developer B: User Story 2 (task management) - T033-T049
   - Developer C: Health check and early polish - T057-T059
3. Stories complete and integrate independently
4. Developer A/B/C together: Phase 7 Polish

---

## Task Breakdown by Category

### Backend Setup (8 tasks)
- T001-T007: Project structure, dependencies, database engine

### Database Models and Migrations (3 tasks)
- T008, T009: User and Task models
- T011: Initial migration

### Authentication and Authorization (7 tasks)
- T015-T016: Security utilities
- T021-T026: Auth service and endpoints
- T034: User ID validation middleware

### Task CRUD API (7 tasks)
- T033: TaskService
- T035-T040: Task endpoints

### Frontend Pages and Components (9 tasks)
- T019-T020: Auth context and protected routes
- T027-T030, T032: Auth UI (US1)
- T041-T049: Task UI (US2)

### API Integration (1 task)
- T018: API client utility

### Validation and Error Handling (5 tasks)
- T014, T032, T048, T049, T066-T067: Error handling and validation

### Testing and Verification (0 tasks)
- Tests are OPTIONAL per specification - not included in this task list

### Cross-Cutting & Polish (9 tasks)
- T012-T013, T053-T056, T060-T068: Logging, persistence, polish

---

## Summary

- **Total Tasks**: 69
- **Task Count by User Story**:
  - Setup: 6
  - Foundational: 14
  - US1 (Auth): 12
  - US2 (Task Management): 17
  - US3 (Persistence): 7
  - Health Check: 3
  - Polish: 9

- **Parallel Opportunities Identified**:
  - 5 parallel opportunities in Setup phase
  - 8 parallel opportunities in Foundational phase
  - 10 parallel opportunities across User Stories 1 and 2
  - 4 parallel opportunities in Polish phase

- **Independent Test Criteria for Each Story**:
  - US1: New user can register → login → access dashboard → logout without seeing other users' data
  - US2: User A and User B can create tasks simultaneously without seeing each other's data
  - US3: User can create tasks, close browser, reopen, log in, and see all tasks unchanged

- **Suggested MVP Scope**: Phase 1 (Setup) + Phase 2 (Foundational) + Phase 3 (User Story 1)
  - Total tasks for MVP: 32
  - Deliverable: Working authentication flow with registration, login, logout

---

## Format Validation

✅ ALL tasks follow the checklist format:
- [ ] Checkbox at start
- Task ID (T001-T069) in execution order
- [P] marker included for parallelizable tasks
- [Story] label (US1, US2, US3) for user story phase tasks
- Clear descriptions with exact file paths
- No story labels for Setup, Foundational, Polish phases

✅ Tasks are organized by user story to enable independent implementation and testing
✅ Each phase is a complete, independently testable increment
✅ Dependencies clearly defined across phases
✅ Parallel execution opportunities identified
