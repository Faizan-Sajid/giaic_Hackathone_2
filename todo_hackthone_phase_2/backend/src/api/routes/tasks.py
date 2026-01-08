# Task: T035-T040
# Spec: API Contracts - Task Endpoints (contracts/task-endpoints.md)
# Spec: Data Model - Task Entity (data-model.md lines 87-180)
# Spec: Implementation Plan - Phase 4: User Story 2 - Task Management

from fastapi import APIRouter, Depends, status, Response, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.logging import get_correlation_id
from src.core.exceptions import (
    APIError,
    NotFoundError,
    ValidationError,
    error_response_generator
)
from src.core.security import verify_jwt
from src.services.task_service import TaskService


# Task: T035-T040
# Spec: API Contracts - Task Endpoints (contracts/task-endpoints.md)
# Spec: Data Model - Task Entity (data-model.md lines 87-180)
# Implementation: Full task CRUD API with user isolation

router = APIRouter(tags=["Tasks"])


# Request/Response Models
class TaskCreateRequest(BaseModel):
    """
    Request model for creating a task

    Task: T036
    Spec: FR-010 (create task with title and optional description)
    """
    title: str = Field(min_length=1, max_length=200, description="Task title (1-200 characters)")
    description: Optional[str] = Field(default=None, max_length=1000, description="Task description (max 1000 characters)")


class TaskUpdateRequest(BaseModel):
    """
    Request model for updating a task

    Task: T038
    Spec: FR-013 (update task title and/or description)
    """
    title: Optional[str] = Field(default=None, min_length=1, max_length=200, description="Task title (1-200 characters)")
    description: Optional[str] = Field(default=None, max_length=1000, description="Task description (max 1000 characters)")


class TaskResponse(BaseModel):
    """
    Response model for task

    Task: T035-T040
    Spec: API Contracts - Task Endpoints
    """
    id: int
    owner_user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: str
    updated_at: str


# Task: T035
# Spec: FR-011 (list user's own tasks)
# Implementation: GET /api/{user_id}/tasks endpoint

@router.get("/{user_id}/tasks", response_model=list[TaskResponse])
async def list_tasks(
    request: Request,
    response: Response,
    user_id: str,
    session: AsyncSession = Depends(get_session)
):
    """
    List all tasks for authenticated user

    Task: T035
    Spec: FR-011 (list user's own tasks)
    FR-018 (return only authenticated user's tasks)

    Returns:
        - 200 OK: List of user's tasks ordered by created_at DESC
        - 401 Unauthorized: No valid JWT token
        - 403 Forbidden: token user_id != URL user_id
        - 500 Internal Server Error: Database error

    Security:
        - Requires valid JWT token
        - Only returns tasks where owner_user_id matches authenticated user
        - Layer 2: URL user_id must match token user_id
        - Layer 3: Query filters by owner_user_id
    """
    correlation_id = await get_correlation_id(request)

    # Verify JWT token and extract user_id
    token = request.cookies.get("token")
    if not token:
        raise APIError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            correlation_id=correlation_id
        )

    token_user_id = verify_jwt(token)

    # Validate user_id matches (Layer 2 Authorization)
    if token_user_id != user_id:
        raise APIError(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: cannot access other users' data",
            correlation_id=correlation_id
        )

    # List tasks (Layer 3: filtered by owner_user_id)
    tasks = await TaskService.list_tasks(session, user_id)

    # Convert to response format
    task_responses = [
        TaskResponse(
            id=task.id,
            owner_user_id=task.owner_user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            created_at=task.created_at.isoformat(),
            updated_at=task.updated_at.isoformat()
        )
        for task in tasks
    ]

    response.headers["X-Correlation-ID"] = correlation_id
    return task_responses


# Task: T036
# Spec: FR-010 (create task with title and optional description)
# Implementation: POST /api/{user_id}/tasks endpoint

@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskCreateRequest,
    http_response: Response,
    api_request: Request,
    user_id: str,
    session=Depends(get_session)
):
    """
    Create new task for authenticated user

    Task: T036
    Spec: FR-010 (create task with title and optional description)
    FR-012 (title minimum 1 character, maximum 200)
    FR-013 (description maximum 1000 characters)

    Returns:
        - 201 Created: Task created successfully
        - 400 Bad Request: Invalid title length or description length
        - 401 Unauthorized: No valid JWT token
        - 403 Forbidden: token user_id != URL user_id
        - 404 Not Found: User not found
        - 500 Internal Server Error: Database error

    Security:
        - Requires valid JWT token
        - Task ownership enforced via owner_user_id
        - Layer 2: URL user_id must match token user_id
    """
    correlation_id = await get_correlation_id(api_request)

    # Verify JWT token and extract user_id
    token = api_request.cookies.get("token")
    if not token:
        raise APIError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            correlation_id=correlation_id
        )

    token_user_id = verify_jwt(token)

    # Validate user_id matches (Layer 2 Authorization)
    if token_user_id != user_id:
        raise APIError(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: cannot access other users' data",
            correlation_id=correlation_id
        )

    # Create task
    task = await TaskService.create_task(
        session,
        user_id,
        request.title,
        request.description
    )

    # Convert to response format
    task_response = TaskResponse(
        id=task.id,
        owner_user_id=task.owner_user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )

    http_response.headers["X-Correlation-ID"] = correlation_id
    return task_response


# Task: T037
# Spec: FR-012 (get specific task by ID)
# Implementation: GET /api/{user_id}/tasks/{id} endpoint

@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def get_task(
    request: Request,
    response: Response,
    user_id: str,
    task_id: int,
    session=Depends(get_session)
):
    """
    Get specific task for authenticated user

    Task: T037
    Spec: FR-012 (get specific task by ID)
    FR-018 (return only tasks owned by authenticated user)

    Returns:
        - 200 OK: Task details if owned by user
        - 401 Unauthorized: No valid JWT token
        - 403 Forbidden: token user_id != URL user_id
        - 404 Not Found: Task not found or doesn't belong to user
        - 500 Internal Server Error: Database error

    Security:
        - Requires valid JWT token
        - Layer 2: URL user_id must match token user_id
        - Layer 3: Query filters by owner_user_id
    """
    correlation_id = await get_correlation_id(request)

    # Verify JWT token and extract user_id
    token = request.cookies.get("token")
    if not token:
        raise APIError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            correlation_id=correlation_id
        )

    token_user_id = verify_jwt(token)

    # Validate user_id matches (Layer 2 Authorization)
    if token_user_id != user_id:
        raise APIError(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: cannot access other users' data",
            correlation_id=correlation_id
        )

    # Get task (Layer 3: filtered by owner_user_id)
    task = await TaskService.get_task(session, user_id, task_id)

    # Convert to response format
    task_response = TaskResponse(
        id=task.id,
        owner_user_id=task.owner_user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )

    response.headers["X-Correlation-ID"] = correlation_id
    return task_response


# Task: T038
# Spec: FR-013 (update task title and/or description)
# Implementation: PUT /api/{user_id}/tasks/{id} endpoint

@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    request: TaskUpdateRequest,
    http_response: Response,
    api_request: Request,
    user_id: str,
    task_id: int,
    session=Depends(get_session)
):
    """
    Update task for authenticated user

    Task: T038
    Spec: FR-013 (update task title and/or description)
    FR-012 (title minimum 1 character, maximum 200)
    FR-013 (description maximum 1000 characters)

    Returns:
        - 200 OK: Task updated successfully
        - 400 Bad Request: Invalid title length or description length
        - 401 Unauthorized: No valid JWT token
        - 403 Forbidden: token user_id != URL user_id
        - 404 Not Found: Task not found or doesn't belong to user
        - 500 Internal Server Error: Database error

    Security:
        - Requires valid JWT token
        - Layer 2: URL user_id must match token user_id
        - Layer 3: Query filters by owner_user_id
    """
    correlation_id = await get_correlation_id(api_request)

    # Verify JWT token and extract user_id
    token = api_request.cookies.get("token")
    if not token:
        raise APIError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            correlation_id=correlation_id
        )

    token_user_id = verify_jwt(token)

    # Validate user_id matches (Layer 2 Authorization)
    if token_user_id != user_id:
        raise APIError(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: cannot access other users' data",
            correlation_id=correlation_id
        )

    # Update task (Layer 3: filtered by owner_user_id)
    task = await TaskService.update_task(
        session,
        user_id,
        task_id,
        request.title,
        request.description
    )

    # Convert to response format
    task_response = TaskResponse(
        id=task.id,
        owner_user_id=task.owner_user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )

    http_response.headers["X-Correlation-ID"] = correlation_id
    return task_response


# Task: T039
# Spec: FR-015 (mark task as complete or incomplete)
# Implementation: PATCH /api/{user_id}/tasks/{id}/complete endpoint

@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_complete(
    request: Request,
    response: Response,
    user_id: str,
    task_id: int,
    session=Depends(get_session)
):
    """
    Toggle task completion status

    Task: T039
    Spec: FR-015 (mark task as complete or incomplete)

    Returns:
        - 200 OK: Task completion status toggled
        - 401 Unauthorized: No valid JWT token
        - 403 Forbidden: token user_id != URL user_id
        - 404 Not Found: Task not found or doesn't belong to user
        - 500 Internal Server Error: Database error

    Security:
        - Requires valid JWT token
        - Layer 2: URL user_id must match token user_id
        - Layer 3: Query filters by owner_user_id
    """
    correlation_id = await get_correlation_id(request)

    # Verify JWT token and extract user_id
    token = request.cookies.get("token")
    if not token:
        raise APIError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            correlation_id=correlation_id
        )

    token_user_id = verify_jwt(token)

    # Validate user_id matches (Layer 2 Authorization)
    if token_user_id != user_id:
        raise APIError(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: cannot access other users' data",
            correlation_id=correlation_id
        )

    # Toggle completion (Layer 3: filtered by owner_user_id)
    task = await TaskService.toggle_complete(session, user_id, task_id)

    # Convert to response format
    task_response = TaskResponse(
        id=task.id,
        owner_user_id=task.owner_user_id,
        title=task.title,
        description=task.description,
        completed=task.completed,
        created_at=task.created_at.isoformat(),
        updated_at=task.updated_at.isoformat()
    )

    response.headers["X-Correlation-ID"] = correlation_id
    return task_response


# Task: T040
# Spec: FR-014 (delete task by ID)
# Implementation: DELETE /api/{user_id}/tasks/{id} endpoint

@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task(
    request: Request,
    response: Response,
    user_id: str,
    task_id: int,
    session=Depends(get_session)
):
    """
    Delete task for authenticated user

    Task: T040
    Spec: FR-014 (delete task by ID)

    Returns:
        - 200 OK: Task deleted successfully
        - 401 Unauthorized: No valid JWT token
        - 403 Forbidden: token user_id != URL user_id
        - 404 Not Found: Task not found or doesn't belong to user
        - 500 Internal Server Error: Database error

    Security:
        - Requires valid JWT token
        - Layer 2: URL user_id must match token user_id
        - Layer 3: Query filters by owner_user_id
    """
    correlation_id = await get_correlation_id(request)

    # Verify JWT token and extract user_id
    token = request.cookies.get("token")
    if not token:
        raise APIError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            correlation_id=correlation_id
        )

    token_user_id = verify_jwt(token)

    # Validate user_id matches (Layer 2 Authorization)
    if token_user_id != user_id:
        raise APIError(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: cannot access other users' data",
            correlation_id=correlation_id
        )

    # Delete task (Layer 3: filtered by owner_user_id)
    await TaskService.delete_task(session, user_id, task_id)

    response.headers["X-Correlation-ID"] = correlation_id

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Task deleted successfully"
        },
        headers={"X-Correlation-ID": correlation_id}
    )
