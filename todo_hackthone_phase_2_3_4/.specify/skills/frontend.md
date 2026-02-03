# Frontend Implementation Skill

**Purpose**: Implement Next.js pages, React components, and UI logic for Phase II Todo Application
**Coverage**: Phase 2-5 (T018-T049) - Auth context, protected routes, pages, components
**Project**: Phase II Full-Stack Web Application

---

## Skill Description

This skill handles all frontend implementation tasks for Phase II Todo Application. It creates Next.js pages using App Router, React components, TypeScript code, and UI logic including:

- Next.js 15+ App Router pages and layouts
- React functional components with hooks
- TypeScript strict mode code
- AuthContext provider for session management
- ProtectedRoute component for auth-gated pages
- API client with cookie support
- Task management UI (TaskList, TaskForm)
- Authentication UI (register, login, logout)
- Client-side validation and error handling
- Better Auth integration for secure cookies

---

## Usage

### Basic Usage
```
/frontend
```

### With Specific Task
```
/frontend T027
```

### With Multiple Tasks
```
/frontend T041 T042
```

---

## Implementation Guidelines

### Technology Stack

- **Framework**: Next.js 15+ with App Router
- **Language**: TypeScript 5.7+ (strict mode)
- **UI Library**: React 18+ with hooks
- **Styling**: Tailwind CSS
- **Auth**: Better Auth client for JWT cookie management
- **HTTP**: Fetch API with credentials support
- **State**: React Context API for global state

### Code Standards

- Use TypeScript strict mode
- Functional components with hooks (useEffect, useState, useContext)
- Client components marked with 'use client' directive
- Include inline comments referencing Task IDs
- Proper TypeScript types for all props and interfaces
- Use Next.js App Router for routing
- Server components for SSR where possible
- Loading states and error handling for all async operations

### Security Requirements

- JWT tokens stored in HTTP-only cookies only
- NEVER store JWT in localStorage
- Use `credentials: 'include'` for fetch requests
- Protected routes redirect unauthenticated users to /login
- Client-side validation before API calls
- Never expose tokens in URLs or console logs

---

## Supported Tasks

### Phase 2: Foundational Frontend (T018-T020)

**T018**: API Client Utility
- File: `frontend/src/lib/api/client.ts`
- Fetch wrapper with `credentials: 'include'`
- Type-safe request/response interfaces
- Error handling for common HTTP status codes
- Automatic correlation ID generation

**T019**: AuthContext Provider
- File: `frontend/src/contexts/AuthContext.tsx`
- React Context for global session state
- Session interface: `{ user: User | null, isLoading: boolean, refresh: () => Promise<void> }`
- Fetch session from /api/auth/session on mount
- Provide session state to all components
- NEVER store JWT in state or localStorage

**T020**: ProtectedRoute Component
- File: `frontend/src/components/ProtectedRoute.tsx`
- Check auth state before rendering children
- Redirect to /login if not authenticated
- Show loading spinner while checking session
- Wrap protected pages with this component

### Phase 3: User Story 1 - Authentication UI (T027-T032)

**T027**: Registration Page
- File: `frontend/src/app/(auth)/register/page.tsx`
- Form with email and password fields
- Email format validation (RFC 5322)
- Password length validation (min 8 characters)
- Submit to POST /api/auth/register
- Redirect to /tasks on success
- Display error messages on failure

**T028**: Login Page
- File: `frontend/src/app/(auth)/login/page.tsx`
- Form with email and password fields
- Email format validation
- Password required validation
- Submit to POST /api/auth/login
- Redirect to /tasks on success
- Better Auth handles HTTP-only cookie automatically
- Display error messages on failure

**T029**: Register Form Integration
- Integrate T027 with backend /api/auth/register endpoint
- Use fetch API with `credentials: 'include'`
- Handle 201 Created, 400 Bad Request, 409 Conflict responses
- Show appropriate error messages

**T030**: Login Form Integration
- Integrate T028 with backend /api/auth/login endpoint
- Use fetch API with `credentials: 'include'`
- Handle 200 OK, 401 Unauthorized responses
- Better Auth sets JWT cookie automatically
- Show appropriate error messages

**T031**: Logout Function
- Call POST /api/auth/logout endpoint
- Clear JWT cookie (handled by Better Auth)
- Redirect to /login page
- Update AuthContext state to null

**T032**: Auth Form Error Handling
- Display validation errors (email format, password length)
- Display API errors (duplicate email, invalid credentials)
- User-friendly error messages
- Clear errors on successful submission

### Phase 4: User Story 2 - Task Management UI (T041-T049)

**T041**: TaskList Component
- File: `frontend/src/components/TaskList.tsx`
- Display user's tasks with title, description, completed status
- Show completed tasks with visual distinction
- Empty state when no tasks
- Tasks ordered by created_at DESC

**T042**: TaskForm Component
- File: `frontend/src/components/TaskForm.tsx`
- Form with title and description fields
- Title required (1-200 characters)
- Description optional (max 1000 characters)
- Client-side validation before submission
- Used for both create and update modes
- Clear form after successful submission

**T043**: Task Creation
- Integrate T042 with POST /api/{user_id}/tasks
- On submit: call API with title and description
- Handle 201 Created, 400 Bad Request responses
- Update task list on success
- Show loading state during API call

**T044**: Task Update
- Integrate T042 with PUT /api/{user_id}/tasks/{id}
- On submit: call API with updated title and/or description
- Handle 200 OK, 400 Bad Request responses
- Update task list on success
- Show loading state during API call

**T045**: Task Completion Toggle
- Integrate T041 with PATCH /api/{user_id}/tasks/{id}/complete
- On click: toggle completed status
- Handle 200 OK, 403 Forbidden responses
- Update task list on success
- Visual indication of completed state (checkbox)

**T046**: Task Delete
- Integrate T041 with DELETE /api/{user_id}/tasks/{id}
- Show confirmation dialog before delete
- On confirm: call API
- Handle 200 OK, 403 Forbidden responses
- Update task list on success (remove deleted task)

**T047**: Tasks Page
- File: `frontend/src/app/(dashboard)/tasks/page.tsx`
- Wrap with ProtectedRoute component
- Include TaskList and TaskForm components
- Fetch tasks from GET /api/{user_id}/tasks
- Show loading state while fetching
- Display error messages on failure

**T048**: Task Loading & Error States
- Show loading spinner during API calls
- Display error messages on API failures
- Retry mechanism for failed requests
- User-friendly error messages
- Clear errors on successful operations

**T049**: Client-Side Task Validation
- Validate title: 1-200 characters
- Validate description: max 1000 characters
- Show validation errors inline
- Prevent form submission if invalid
- Validate on input change (real-time)

### Phase 5: User Story 3 - Persistence (T054-T056)

**T054**: API Client Error Handling
- File: `frontend/src/lib/api/client.ts`
- Graceful handling of network errors
- Retry logic for temporary failures
- Exponential backoff for retries
- User-friendly error messages

**T055**: Optimistic Refresh Strategy
- File: `frontend/src/components/TaskList.tsx`
- Auto-refresh task list on interval (e.g., every 30 seconds)
- Refresh on page focus
- Optimistic UI updates (don't wait for API response)
- Sync with server on next response

**T056**: HTTP-Only Cookie Persistence
- Verify Better Auth configuration for HTTP-only cookies
- Verify Secure attribute for production
- Verify SameSite=Strict attribute
- Test cookie persistence across browser sessions

---

## Examples

### Example 1: Implement AuthContext
```
User: /frontend T019

Output:
- Creates frontend/src/contexts/AuthContext.tsx
- Implements React Context provider
- Provides session state globally
- Fetches session from /api/auth/session
- Never stores JWT in localStorage
```

### Example 2: Implement TaskList Component
```
User: /frontend T041

Output:
- Creates frontend/src/components/TaskList.tsx
- Displays tasks with title, description, completed status
- Shows completed tasks with visual distinction
- Empty state handling
- Ordered by created_at DESC
```

### Example 3: Implement Login Page
```
User: /frontend T028 T030

Output:
- Creates frontend/src/app/(auth)/login/page.tsx
- Email/password form with validation
- Integration with /api/auth/login endpoint
- Better Auth cookie handling
- Error display and redirect logic
```

### Example 4: Implement Tasks Page
```
User: /frontend T047

Output:
- Creates frontend/src/app/(dashboard)/tasks/page.tsx
- ProtectedRoute wrapper
- TaskList and TaskForm integration
- API calls to fetch tasks
- Loading and error states
```

---

## Dependencies

### Required Files
- `specs/001-full-stack-web/spec.md` - Feature requirements
- `specs/001-full-stack-web/plan.md` - Implementation plan
- `specs/001-full-stack-web/contracts/task-endpoints.md` - Task API contracts
- `specs/001-full-stack-web/contracts/auth-endpoints.md` - Auth API contracts

### Required Environment Variables
- `NEXT_PUBLIC_API_URL` - Backend API URL (http://localhost:8000)
- `BETTER_AUTH_SECRET` - JWT secret (shared with backend)
- `BETTER_AUTH_URL` - Better Auth base URL (http://localhost:3000)

### Required Dependencies (package.json)
```json
{
  "dependencies": {
    "next": "^15.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "typescript": "^5.7.0",
    "better-auth": "^1.0.0",
    "tailwindcss": "^3.4.0"
  }
}
```

---

## TypeScript Interfaces

### User Interface
```typescript
interface User {
  id: string
  email: string
}
```

### Task Interface
```typescript
interface Task {
  id: number
  owner_user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}
```

### Session Interface
```typescript
interface Session {
  user: User | null
  isLoading: boolean
  refresh: () => Promise<void>
}
```

### API Response Interfaces
```typescript
interface ApiResponse<T> {
  data?: T
  error?: string
  correlation_id?: string
}

interface TaskListResponse {
  tasks: Task[]
  count: number
}
```

---

## Validation Checklist

After implementing frontend tasks, verify:

### Security
- [ ] JWT tokens stored in HTTP-only cookies only
- [ ] No JWT tokens in localStorage
- [ ] All fetch requests use `credentials: 'include'`
- [ ] ProtectedRoute redirects unauthenticated users
- [ ] No tokens exposed in console logs or URLs

### Authentication
- [ ] AuthContext provides session state globally
- [ ] Session fetched from /api/auth/session on mount
- [ ] Login page redirects to /tasks on success
- [ ] Register page redirects to /tasks on success
- [ ] Logout clears cookie and redirects to /login

### Task Management
- [ ] TaskList displays user's tasks only
- [ ] TaskForm validates input before submission
- [ ] Create task updates task list
- [ ] Update task refreshes task list
- [ ] Delete task removes from list
- [ ] Toggle complete updates task visually
- [ ] Loading states shown during API calls
- [ ] Error messages displayed on failures

### UI/UX
- [ ] Empty state shown when no tasks
- [ ] Loading spinner during async operations
- [ ] User-friendly error messages
- [ ] Tasks ordered by created_at DESC
- [ ] Completed tasks visually distinguished
- [ ] Forms have client-side validation
- [ ] Responsive design works on mobile

---

## File Structure Reference

```
frontend/src/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   ├── (dashboard)/
│   │   └── tasks/
│   │       └── page.tsx
│   ├── api/
│   │   └── client.ts
│   └── layout.tsx
├── components/
│   ├── ProtectedRoute.tsx
│   ├── TaskList.tsx
│   └── TaskForm.tsx
├── contexts/
│   └── AuthContext.tsx
└── lib/
    └── api/
        └── client.ts
```

---

## Notes

- All frontend code must reference Task IDs in comments
- Never manually modify generated code
- Follow exact technology versions from Constitution
- Test each page and component independently
- Verify no console errors in browser
- Check network tab for API call success/failure
- Ensure Better Auth cookies are set correctly
- Verify ProtectedRoute redirects work
- Test loading and error states
- Check responsive design on different screen sizes
