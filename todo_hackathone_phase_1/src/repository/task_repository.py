"""In-memory task repository for Todo Console App."""

from typing import Optional

from src.models.task import Task


class TaskNotFoundError(ValueError):
    """Raised when a task ID is not found."""

    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task {task_id} not found.")


class TaskRepository:
    """In-memory storage for tasks with unique ID generation.

    Stores tasks in a list and generates unique integer IDs
    starting from 1 and incrementing for each new task.
    """

    def __init__(self):
        self._tasks: list[Task] = []
        self._next_id: int = 1

    def create(self, title: str, description: Optional[str] = None) -> Task:
        """Create a new task with a unique ID.

        Args:
            title: Task title (must be non-empty, validated by caller)
            description: Optional task description

        Returns:
            The newly created Task
        """
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            completed=False,
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def find_all(self) -> list[Task]:
        """Return all tasks in insertion order.

        Returns:
            List of all tasks
        """
        return list(self._tasks)

    def find_by_id(self, task_id: int) -> Optional[Task]:
        """Find a task by its ID.

        Args:
            task_id: The task ID to search for

        Returns:
            The Task if found, None otherwise
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update(
        self, task_id: int, title: str, description: Optional[str] = None
    ) -> Task:
        """Update a task's title and description.

        Args:
            task_id: The task ID to update
            title: New task title (must be non-empty, validated by caller)
            description: New task description or None

        Returns:
            The updated Task

        Raises:
            TaskNotFoundError: If task_id not found
        """
        task = self.find_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        task.title = title
        task.description = description
        return task

    def delete(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id: The task ID to delete

        Returns:
            True if task was found and deleted, False otherwise
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return True
        return False

    def toggle(self, task_id: int) -> Optional[Task]:
        """Toggle a task's completion status.

        Args:
            task_id: The task ID to toggle

        Returns:
            The updated Task if found, None otherwise
        """
        task = self.find_by_id(task_id)
        if task is None:
            return None
        task.completed = not task.completed
        return task

    def count(self) -> int:
        """Return the number of tasks in the repository.

        Returns:
            Task count
        """
        return len(self._tasks)
