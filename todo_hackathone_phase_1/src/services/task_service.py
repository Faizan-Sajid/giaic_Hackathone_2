"""Task service with business logic and validation for Todo Console App."""

from typing import Optional

from src.models.task import Task
from src.repository.task_repository import TaskNotFoundError, TaskRepository


class EmptyTitleError(ValueError):
    """Raised when task title is empty or whitespace-only."""

    def __init__(self):
        super().__init__("Title cannot be empty.")


class TaskService:
    """Business logic layer for task operations.

    Handles validation and delegates to the repository for storage.
    """

    def __init__(self, repository: TaskRepository):
        self._repository = repository

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Add a new task.

        Args:
            title: Task title (required)
            description: Optional task description

        Returns:
            The created Task

        Raises:
            EmptyTitleError: If title is empty or whitespace-only
        """
        if not title or not title.strip():
            raise EmptyTitleError()
        return self._repository.create(title, description)

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks.

        Returns:
            List of all tasks in insertion order
        """
        return self._repository.find_all()

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: The task ID

        Returns:
            The Task if found, None otherwise
        """
        return self._repository.find_by_id(task_id)

    def update_task(
        self, task_id: int, title: str, description: Optional[str] = None
    ) -> Task:
        """Update a task's title and description.

        Args:
            task_id: The task ID to update
            title: New title (required)
            description: New description or None

        Returns:
            The updated Task

        Raises:
            EmptyTitleError: If title is empty or whitespace-only
            TaskNotFoundError: If task_id not found
        """
        if not title or not title.strip():
            raise EmptyTitleError()
        return self._repository.update(task_id, title, description)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task.

        Args:
            task_id: The task ID to delete

        Returns:
            True if deleted, False if not found
        """
        return self._repository.delete(task_id)

    def toggle_task(self, task_id: int) -> Optional[Task]:
        """Toggle a task's completion status.

        Args:
            task_id: The task ID to toggle

        Returns:
            The updated Task if found, None otherwise
        """
        return self._repository.toggle(task_id)

    def task_count(self) -> int:
        """Return the total number of tasks.

        Returns:
            Task count
        """
        return self._repository.count()
