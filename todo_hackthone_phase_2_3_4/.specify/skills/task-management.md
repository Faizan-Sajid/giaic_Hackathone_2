# Task Management Implementation Skill

**Purpose**: Implement task CRUD operations with strict user isolation
**Coverage**: Phase 4 User Story 2 (T033-T049) - Complete task management
**Project**: Phase II Full-Stack Web Application

---

## Skill Description

This skill handles all task management implementation tasks for Phase II Todo Application. It creates backend TaskService, task API endpoints, and frontend task management UI including:

- TaskService with CRUD operations
- User ID validation middleware
- All task API endpoints (list, create, get, update, toggle, delete)
- TaskList component for displaying tasks
- TaskForm component for creating/updating tasks
- Tasks page integration
- Task loading and error states
- Client-side validation
- Strict user isolation enforcement at all layers

---

## Usage

### Basic Usage
```
/task-management
```

### With Specific Task
```
/task-management T033
```

### With Multiple Tasks
```
/task-management T033 T034 T035 T036
```

---

## Implementation Guidelines

### Technology Stack

**Backend**:
- **Service Layer**: TaskService in `backend/src/services/`
- **API Routes**: Tasks router in `backend/src/api/routes/tasks.py`
- **ORM**: SQLModel 0.0.22+ with async operations
- **Validation**: Pydantic models for request/response

**Frontend**:
- **Components**: TaskList, TaskForm in `frontend/src/components/`
- **Pages**: Tasks page in `frontend/src/app/(dashboard)/tasks/`
- **State**: React hooks (useState, useEffect)

### Data Isolation Requirements

**Multi-Layer Enforcement**:
1. **Authentication Layer**: JWT must be valid and not expired
2. **Authorization Layer**: `token.sub == url_user_id`
3. **Data Layer**: Query `WHERE owner_user_id == authenticated_user_id`

**Example Attack Prevention**:
```python
# User A (user_id=123) tries to access User B's (user_id=456) task

# Layer 1: JWT valid ✅
# Layer 2: token_user_id (123) != url_user_id (456) → 403 Forbidden

# Even if Layer 2 bypassed:
# Layer 3: WHERE id = ? AND owner_user_id = 123 → Empty result → 404 Not Found
```

---

## Supported Tasks

### T033: TaskService

**File**: `backend/src/services/task_service.py`

**Methods**:
```python
async def create_task(session, user_id: str, title: str, description: str | None) -> Task:
    """
    Create task for specific user
    Task: T033
    Spec: FR-008 (create task with title and optional description)
    """
    task = Task(
        owner_user_id=user_id,
        title=title,
        description=description,
        completed=False
    )
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task

async def list_tasks(session, user_id: str, completed: bool | None = None) -> List[Task]:
    """
    List user's tasks, optionally filtered by completion status
    Task: T033
    Spec: FR-009 (list user's own tasks)
    """
    query = select(Task).where(Task.owner_user_id == user_id)
    if completed is not None:
        query = query.where(Task.completed == completed)
    query = query.order_by(desc(Task.created_at))
    result = await session.exec(query)
    return result.all()

async def get_task(session, user_id: str, task_id: int) -> Task | None:
    """
    Get specific task if owned by user
    Task: T033
    Spec: FR-010 (retrieve user's own specific task)
    """
    query = select(Task).where(
        Task.id == task_id,
        Task.owner_user_id == user_id
    )
    result = await session.exec(query)
    return result.one_or_none()

async def update_task(
    session,
    user_id: str,
    task_id: int,
    title: str | None = None,
    description: str | None = None
) -> Task | None:
    """
    Update task title and/or description if owned by user
    Task: T033
    Spec: FR-011 (update user's own tasks)
    """
    task = await get_task(session, user_id, task_id)
    if not task:
        return None

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)
    return task

async def delete_task(session, user_id: str, task_id: int) -> bool:
    """
    Delete task if owned by user
    Task: T033
    Spec: FR-013 (delete user's own tasks)
    """
    task = await get_task(session, user_id, task_id)
    if not task:
        return False

    await session.delete(task)
    await session.commit()
    return True

async def toggle_complete(session, user_id: str, task_id: int) -> Task | None:
    """
    Toggle task completion status
    Task: T033
    Spec: FR-012 (mark tasks as completed or incomplete)
    """
    task = await get_task(session, user_id, task_id)
    if not task:
        return None

    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)
    return task
```

### T034: User ID Validation Middleware

**File**: `backend/src/api/deps.py`

**Implementation**:
```python
from fastapi import Depends, HTTPException, status
from .core.security import verify_jwt

def validate_user_id(token_user_id: str = Depends(verify_jwt), user_id: str) -> str:
    """
    Validate that token user_id matches URL user_id
    Task: T034
    Spec: FR-007 (enforce user_id matching)
    FR-014 (token user_id matches request URL user_id)
    """
    if token_user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch"
        )
    return user_id
```

### T035-T040: Task API Endpoints

**File**: `backend/src/api/routes/tasks.py`

**T035: List Tasks**
```python
@router.get("/{user_id}/tasks")
async def list_tasks_endpoint(
    user_id: str = Depends(validate_user_id),
    completed: bool | None = None,
    session: AsyncSession = Depends(get_session)
):
    """
    List user's tasks
    Task: T035
    Spec: FR-009 (list user's own tasks)
    """
    tasks = await list_tasks(session, user_id, completed)
    return {
        "tasks": tasks,
        "count": len(tasks)
    }
```

**T036: Create Task**
```python
@router.post("/{user_id}/tasks", status_code=201)
async def create_task_endpoint(
    user_id: str = Depends(validate_user_id),
    request: CreateTaskRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Create new task
    Task: T036
    Spec: FR-008 (create task with title and optional description)
    """
    task = await create_task(session, user_id, request.title, request.description)
    return task
```

**T037: Get Task**
```python
@router.get("/{user_id}/tasks/{id}")
async def get_task_endpoint(
    user_id: str = Depends(validate_user_id),
    id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Get specific task
    Task: T037
    Spec: FR-010 (retrieve user's own specific task)
    """
    task = await get_task(session, user_id, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

**T038: Update Task**
```python
@router.put("/{user_id}/tasks/{id}")
async def update_task_endpoint(
    user_id: str = Depends(validate_user_id),
    id: int,
    request: UpdateTaskRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Update task
    Task: T038
    Spec: FR-011 (update user's own tasks)
    """
    task = await update_task(
        session, user_id, id, request.title, request.description
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

**T039: Toggle Complete**
```python
@router.patch("/{user_id}/tasks/{id}/complete")
async def toggle_complete_endpoint(
    user_id: str = Depends(validate_user_id),
    id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Toggle task completion
    Task: T039
    Spec: FR-012 (mark tasks as completed or incomplete)
    """
    task = await toggle_complete(session, user_id, id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

**T040: Delete Task**
```python
@router.delete("/{user_id}/tasks/{id}")
async def delete_task_endpoint(
    user_id: str = Depends(validate_user_id),
    id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Delete task
    Task: T040
    Spec: FR-013 (delete user's own tasks)
    """
    deleted = await delete_task(session, user_id, id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"id": id, "message": "Task deleted successfully"}
```

### T041: TaskList Component

**File**: `frontend/src/components/TaskList.tsx`

**Implementation**:
```typescript
'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'

interface Task {
  id: number
  owner_user_id: string
  title: string
  description: string | null
  completed: boolean
  created_at: string
  updated_at: string
}

interface TaskListProps {
  userId: string
}

export default function TaskList({ userId }: TaskListProps) {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const router = useRouter()

  useEffect(() => {
    fetchTasks()
  }, [userId])

  const fetchTasks = async () => {
    try {
      const response = await fetch(`/api/${userId}/tasks`, {
        credentials: 'include'
      })

      if (!response.ok) {
        throw new Error('Failed to fetch tasks')
      }

      const data = await response.json()
      setTasks(data.tasks)
    } catch (err) {
      setError('Failed to load tasks')
    } finally {
      setLoading(false)
    }
  }

  const toggleComplete = async (taskId: number) => {
    try {
      const response = await fetch(`/api/${userId}/tasks/${taskId}/complete`, {
        method: 'PATCH',
        credentials: 'include'
      })

      if (response.ok) {
        // Update local state
        setTasks(tasks.map(task =>
          task.id === taskId ? { ...task, completed: !task.completed } : task
        ))
      }
    } catch (err) {
      setError('Failed to update task')
    }
  }

  const deleteTask = async (taskId: number) => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return
    }

    try {
      const response = await fetch(`/api/${userId}/tasks/${taskId}`, {
        method: 'DELETE',
        credentials: 'include'
      })

      if (response.ok) {
        // Remove from local state
        setTasks(tasks.filter(task => task.id !== taskId))
      }
    } catch (err) {
      setError('Failed to delete task')
    }
  }

  if (loading) return <div>Loading tasks...</div>
  if (error) return <div className="error">{error}</div>
  if (tasks.length === 0) return <div>No tasks yet. Create one above!</div>

  return (
    <div className="task-list">
      {tasks.map(task => (
        <div key={task.id} className={`task ${task.completed ? 'completed' : ''}`}>
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => toggleComplete(task.id)}
          />
          <div className="task-content">
            <h3>{task.title}</h3>
            {task.description && <p>{task.description}</p>}
            <small>Created: {new Date(task.created_at).toLocaleString()}</small>
          </div>
          <button onClick={() => deleteTask(task.id)}>Delete</button>
        </div>
      ))}
    </div>
  )
}
```

### T042: TaskForm Component

**File**: `frontend/src/components/TaskForm.tsx`

**Implementation**:
```typescript
'use client'

import { useState } from 'react'

interface TaskFormProps {
  userId: string
  onTaskCreated?: (task: any) => void
  editingTask?: any
}

export default function TaskForm({ userId, onTaskCreated, editingTask }: TaskFormProps) {
  const [title, setTitle] = useState(editingTask?.title || '')
  const [description, setDescription] = useState(editingTask?.description || '')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const isEditing = !!editingTask

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    // Client-side validation
    if (!title || title.length < 1 || title.length > 200) {
      setError('Title must be between 1 and 200 characters')
      return
    }

    if (description && description.length > 1000) {
      setError('Description must be at most 1000 characters')
      return
    }

    setLoading(true)

    try {
      const url = isEditing
        ? `/api/${userId}/tasks/${editingTask.id}`
        : `/api/${userId}/tasks`

      const method = isEditing ? 'PUT' : 'POST'

      const response = await fetch(url, {
        method,
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, description: description || null })
      })

      if (response.ok) {
        const data = await response.json()
        onTaskCreated?.(data)
        setTitle('')
        setDescription('')
      } else {
        setError('Failed to save task')
      }
    } catch (err) {
      setError('Network error')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="task-form">
      {error && <div className="error">{error}</div>}

      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Task title (1-200 characters)"
        required
        maxLength={200}
      />

      <textarea
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Task description (optional, max 1000 characters)"
        maxLength={1000}
        rows={3}
      />

      <button type="submit" disabled={loading}>
        {loading ? 'Saving...' : isEditing ? 'Update Task' : 'Create Task'}
      </button>
    </form>
  )
}
```

### T043-T046: Task Operations Integration

Already implemented in T041-T042 above:
- T043: Task creation in TaskForm
- T044: Task update in TaskForm
- T045: Toggle complete in TaskList
- T046: Delete task in TaskList

### T047: Tasks Page

**File**: `frontend/src/app/(dashboard)/tasks/page.tsx`

**Implementation**:
```typescript
import ProtectedRoute from '@/components/ProtectedRoute'
import TaskList from '@/components/TaskList'
import TaskForm from '@/components/TaskForm'
import { useAuth } from '@/contexts/AuthContext'

export default function TasksPage() {
  const { session } = useAuth()

  if (!session?.user) {
    return null
  }

  return (
    <ProtectedRoute>
      <div className="tasks-page">
        <h1>My Tasks</h1>
        <TaskForm
          userId={session.user.id}
          onTaskCreated={() => {
            // Refresh task list
          }}
        />
        <TaskList userId={session.user.id} />
      </div>
    </ProtectedRoute>
  )
}
```

### T048: Loading & Error States

Already implemented in T041-T042 above.

### T049: Client-Side Validation

Already implemented in T042 above:
- Title: 1-200 characters
- Description: max 1000 characters
- Real-time validation on input change

---

## Examples

### Example 1: Complete Task Backend
```
User: /task-management T033 T034 T035 T036 T037 T038 T039 T040

Output:
- TaskService created with all CRUD methods
- User ID validation middleware implemented
- All task API endpoints created
- User isolation enforced at all layers
```

### Example 2: Task UI Components
```
User: /task-management T041 T042 T047

Output:
- TaskList component with display
- TaskForm component with validation
- Tasks page with integration
- Loading and error states
```

### Example 3: Single Task Service
```
User: /task-management T033

Output:
- TaskService created
- All CRUD methods implemented
- User_id filtering in all queries
```

---

## Validation Checklist

After implementing task management, verify:

### Backend Data Isolation
- [ ] User ID validation middleware active
- [ ] All task queries filter by user_id
- [ ] Token user_id must match URL user_id
- [ ] User A cannot access User B's tasks

### Backend API
- [ ] GET /api/{user_id}/tasks returns only user's tasks
- [ ] POST /api/{user_id}/tasks creates task for user
- [ ] GET /api/{user_id}/tasks/{id} returns task if owned
- [ ] PUT /api/{user_id}/tasks/{id} updates task if owned
- [ ] PATCH /api/{user_id}/tasks/{id}/complete toggles if owned
- [ ] DELETE /api/{user_id}/tasks/{id} deletes task if owned
- [ ] All endpoints return 403 on user_id mismatch
- [ ] All endpoints return 404 if task doesn't exist

### Frontend UI
- [ ] TaskList displays user's tasks only
- [ ] TaskList shows completed tasks distinctly
- [ ] TaskForm validates input before submission
- [ ] Create task updates task list
- [ ] Update task refreshes task list
- [ ] Delete task removes from list
- [ ] Toggle complete updates task visually
- [ ] Loading states shown during API calls
- [ ] Error messages displayed appropriately

### User Isolation Test
- [ ] User A creates tasks → User B logs in → User B cannot see User A's tasks
- [ ] User B creates tasks → User A logs in → User A cannot see User B's tasks
- [ ] Both users can only access their own data
- [ ] API rejects cross-user access with 403 Forbidden

---

## Notes

- All task management code must reference Task IDs in comments
- User isolation MUST be enforced at all 3 layers (auth, authz, data)
- Test with multiple users to verify isolation
- Never bypass user_id validation
- All task queries MUST include WHERE owner_user_id clause
- Frontend MUST NOT show tasks from other users
