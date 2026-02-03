# Task: T033
# Spec: Implementation Plan - Phase 4: User Story 2 - Task Management
# Spec: Data Model - Task Entity (data-model.md lines 87-180)
# Implementation: TaskService with full CRUD operations

from typing import List, Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Task
from src.core.exceptions import NotFoundError, ValidationError, APIError


# Task: T033
# Spec: Data Model - Task Entity (data-model.md lines 87-180)
# Spec: User Story 2 - Task Management (FR-010 through FR-015)
# Implementation: TaskService with create_task, list_tasks, get_task, update_task, delete_task, toggle_complete methods

class TaskService:
    """
    Task management service with user isolation

    Task: T033
    Spec: Data Model - Task Entity (data-model.md lines 87-180)
    Spec: User Story 2 - Task Management (FR-010 through FR-015)

    Features:
        - Create task (FR-010)
        - List user's tasks (FR-011)
        - Get specific task (FR-012)
        - Update task (FR-013)
        - Delete task (FR-014)
        - Toggle task completion (FR-015)
        - Strict user isolation (all queries include owner_user_id filter)
        - Automatic updated_at timestamp management
        - ORDER BY created_at DESC for consistent listing
    """

    @staticmethod
    async def create_task(
        session: AsyncSession,
        user_id: str,
        title: str,
        description: Optional[str] = None
    ) -> Task:
        """
        Create new task for user

        Task: T033
        Spec: FR-010 (create task with title and optional description)

        Args:
            session: Database session
            user_id: Owner user ID (from JWT token)
            title: Task title (1-200 characters, required)
            description: Task description (max 1000 characters, optional)

        Returns:
            Created Task object

        Raises:
            ValidationError: If title is empty or too long, or description too long

        Security:
            - Always sets owner_user_id to authenticated user ID
            - Prevents cross-user task creation
        """
        # Validate title length
        if not title or len(title.strip()) == 0:
            raise ValidationError(detail="Title is required")
        if len(title) > 200:
            raise ValidationError(detail="Title too long (max 200 characters)")

        # Validate description length
        if description and len(description) > 1000:
            raise ValidationError(detail="Description too long (max 1000 characters)")

        # Create task with user ownership
        task = Task(
            owner_user_id=user_id,
            title=title.strip(),
            description=description.strip() if description else None
        )

        session.add(task)
        await session.commit()
        await session.refresh(task)

        return task

    @staticmethod
    async def list_tasks(
        session: AsyncSession,
        user_id: str,
        limit: int = 100
    ) -> List[Task]:
        """
        List all tasks for authenticated user

        Task: T033
        Spec: FR-011 (list user's own tasks)

        Args:
            session: Database session
            user_id: Owner user ID (from JWT token)
            limit: Maximum number of tasks to return (default 100)

        Returns:
            List of Task objects ordered by created_at DESC

        Security:
            - Only returns tasks where owner_user_id matches authenticated user
            - Prevents cross-user data access
        """
        result = await session.execute(
            select(Task)
            .where(Task.owner_user_id == user_id)
            .order_by(Task.created_at.desc())
            .limit(limit)
        )

        return result.scalars().all()

    @staticmethod
    async def get_task(
        session: AsyncSession,
        user_id: str,
        task_id: int
    ) -> Task:
        """
        Get specific task for authenticated user

        Task: T033
        Spec: FR-012 (get specific task by ID)

        Args:
            session: Database session
            user_id: Owner user ID (from JWT token)
            task_id: Task ID to retrieve

        Returns:
            Task object

        Raises:
            NotFoundError: If task not found or doesn't belong to user

        Security:
            - Only returns task if owner_user_id matches authenticated user
            - Prevents cross-user data access
        """
        result = await session.execute(
            select(Task)
            .where(Task.id == task_id)
            .where(Task.owner_user_id == user_id)
        )

        task = result.scalar_one_or_none()

        if not task:
            raise NotFoundError(detail="Task not found")

        return task

    @staticmethod
    async def update_task(
        session: AsyncSession,
        user_id: str,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Task:
        """
        Update task for authenticated user

        Task: T033
        Spec: FR-013 (update task title and/or description)

        Args:
            session: Database session
            user_id: Owner user ID (from JWT token)
            task_id: Task ID to update
            title: New title (optional, 1-200 characters)
            description: New description (optional, max 1000 characters)

        Returns:
            Updated Task object

        Raises:
            NotFoundError: If task not found or doesn't belong to user
            ValidationError: If title/description validation fails

        Security:
            - Only updates task if owner_user_id matches authenticated user
            - Prevents cross-user data modification
            - Automatically updates updated_at timestamp
        """
        # Get existing task (with ownership check)
        task = await TaskService.get_task(session, user_id, task_id)

        # Validate and update title if provided
        if title is not None:
            if not title or len(title.strip()) == 0:
                raise ValidationError(detail="Title is required")
            if len(title) > 200:
                raise ValidationError(detail="Title too long (max 200 characters)")
            task.title = title.strip()

        # Validate and update description if provided
        if description is not None:
            if description and len(description) > 1000:
                raise ValidationError(detail="Description too long (max 1000 characters)")
            task.description = description.strip() if description else None

        # Update timestamp automatically via database default
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return task

    @staticmethod
    async def delete_task(
        session: AsyncSession,
        user_id: str,
        task_id: int
    ) -> None:
        """
        Delete task for authenticated user

        Task: T033
        Spec: FR-014 (delete task by ID)

        Args:
            session: Database session
            user_id: Owner user ID (from JWT token)
            task_id: Task ID to delete

        Raises:
            NotFoundError: If task not found or doesn't belong to user

        Security:
            - Only deletes task if owner_user_id matches authenticated user
            - Prevents cross-user data deletion
        """
        # Get existing task (with ownership check)
        task = await TaskService.get_task(session, user_id, task_id)

        # Delete task
        await session.delete(task)
        await session.commit()

    @staticmethod
    async def toggle_complete(
        session: AsyncSession,
        user_id: str,
        task_id: int
    ) -> Task:
        """
        Toggle task completion status

        Task: T033
        Spec: FR-015 (mark task as complete or incomplete)

        Args:
            session: Database session
            user_id: Owner user ID (from JWT token)
            task_id: Task ID to toggle

        Returns:
            Updated Task object with toggled completed status

        Raises:
            NotFoundError: If task not found or doesn't belong to user

        Security:
            - Only toggles task if owner_user_id matches authenticated user
            - Prevents cross-user data modification
        """
        # Get existing task (with ownership check)
        task = await TaskService.get_task(session, user_id, task_id)

        # Toggle completion status
        task.completed = not task.completed

        # Update timestamp automatically via database default
        session.add(task)
        await session.commit()
        await session.refresh(task)

        return task
