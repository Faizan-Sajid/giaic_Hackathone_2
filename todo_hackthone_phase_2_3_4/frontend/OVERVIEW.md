# Frontend Overview

## Next.js 15+ App Router Structure

The frontend follows the Next.js App Router convention with a clean folder-based routing system located in `src/app/`.

### Route Structure
- **Root Layout** (`src/app/layout.tsx`): Global HTML structure with metadata
- **Home Page** (`src/app/page.tsx`): Landing page with ClientWrapper
- **Authentication Routes** (`src/app/(auth)/`):
  - `src/app/(auth)/layout.tsx`: Auth layout wrapper
  - `src/app/(auth)/login/page.tsx`: Login page
  - `src/app/(auth)/register/page.tsx`: Registration page
- **Dashboard Routes** (`src/app/(dashboard)/`):
  - `src/app/(dashboard)/layout.tsx`: Dashboard layout wrapper
  - `src/app/(dashboard)/dashboard/page.tsx`: Dashboard page with task statistics
  - `src/app/(dashboard)/tasks/page.tsx`: Tasks management page

### Route Groups
- `(auth)`: Authentication-related pages (login, register)
- `(dashboard)`: Protected dashboard and task management pages
- Both route groups use ClientWrapper to provide client-side context

### Client-Side Wrapping
- `ClientWrapper.tsx`: Wraps route groups with AuthProvider
- `HomePageClient.tsx`: Client component for home page functionality

## Key Components and Data Fetching

### Authentication Components
- **AuthContext** (`src/contexts/AuthContext.tsx`): Manages authentication state globally
  - Provides user object, loading state, refresh and logout functions
  - Handles JWT token via HTTP-only cookies (never stored in localStorage)
  - Automatic session loading on mount
  - Session validation via `/api/auth/session` endpoint

- **ProtectedRoute** (`src/components/ProtectedRoute.tsx`): Wrapper for protected pages
  - Checks authentication state before rendering children
  - Redirects to `/login` if not authenticated
  - Shows loading state while checking session

- **LoginForm** (`src/components/auth/LoginForm.tsx`): Handles user login
  - Validates email and password inputs
  - Calls `/api/auth/login` endpoint
  - Sets user in context on successful login
  - Redirects to dashboard after login

- **RegisterForm** (`src/components/auth/RegisterForm.tsx`): Handles user registration
  - Validates email and password inputs
  - Calls `/api/auth/register` endpoint
  - Sets user in context on successful registration
  - Redirects to dashboard after registration

### Task Management Components
- **TaskList** (`src/components/TaskList.tsx`): Displays user's tasks
  - Fetches tasks from `/api/{user_id}/tasks` endpoint
  - Allows toggling task completion status
  - Provides delete functionality with confirmation
  - Optimistic UI updates

- **TaskForm** (`src/components/TaskForm.tsx`): Handles task creation/editing
  - Validates task title and description
  - Interacts with task API endpoints

### UI Components
- **LoadingSkeleton** (`src/components/LoadingSkeleton.tsx`): Provides loading states
- Various reusable UI components for consistent design

## Better Auth Integration on Client Side

### API Client (`src/lib/api/client.ts`)
- **Base URL**: Configured via `NEXT_PUBLIC_API_URL` environment variable
- **Credentials**: Automatically includes HTTP-only cookies with `credentials: 'include'`
- **Error Handling**: Comprehensive error mapping for different HTTP status codes
- **Correlation IDs**: Automatic request tracing with correlation IDs
- **Generic Methods**: `get`, `post`, `put`, `delete`, `patch` with consistent error handling

### Authentication Flow
1. **Session Management**: AuthContext automatically checks `/api/auth/session` on mount
2. **Login**: Calls `/api/auth/login` with email/password, receives JWT in HTTP-only cookie
3. **Registration**: Calls `/api/auth/register` with email/password, receives JWT in HTTP-only cookie
4. **Logout**: Calls `/api/auth/logout` to clear JWT cookie and resets local state
5. **Protected Routes**: ProtectedRoute component guards pages requiring authentication

### Security Measures
- JWT tokens stored only in HTTP-only cookies (not localStorage)
- Automatic credential inclusion for all API requests
- Strict type checking for API responses
- Comprehensive error handling and user feedback
- Client-side route protection via ProtectedRoute component

### State Management
- **React Context**: AuthContext provides global authentication state
- **Component State**: Individual components manage their own state for forms and UI interactions
- **Data Fetching**: Components use the API client to interact with backend endpoints
- **Session Persistence**: Authentication state maintained across page navigations via context