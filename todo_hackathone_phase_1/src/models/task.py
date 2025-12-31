"""Task data model for Todo Console App."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """Represents a single todo item stored in memory.

    Attributes:
        id: Unique integer identifier (auto-generated)
        title: Task title (required, non-empty)
        description: Optional task details
        completed: Completion status (default: False)
    """

    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __str__(self) -> str:
        """Return a formatted string representation of the task."""
        status = "Done" if self.completed else "Pending"
        desc = f" - {self.description}" if self.description else ""
        return f"{self.id:3} | [{status:8}] | {self.title}{desc}"
