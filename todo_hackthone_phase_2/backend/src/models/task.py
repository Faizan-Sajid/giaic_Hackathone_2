# Task: T009
# Spec: Data Model - Task Entity (data-model.md lines 87-180)
# Implementation: Task SQLModel with foreign key, constraints, timestamps

from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime
if TYPE_CHECKING:
    from .user import User


class Task(SQLModel, table=True):
    """
    Task entity representing a todo item belonging to a specific user

    Task: T009
    Spec: FR-008 (create task with title and optional description)
    FR-009 (list user's own tasks)
    FR-011 (update user's own tasks)
    FR-012 (mark tasks as completed)
    FR-013 (delete user's own tasks)
    DINT-002 (task owner_user_id references valid user)
    DINT-003 (cascade delete on user deletion)
    DINT-004-DINT-007 (title/description length constraints, timestamps)
    """

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Task integer primary key (auto-increment)"
    )
    owner_user_id: str = Field(
        foreign_key="user.id",
        description="Task owner (user UUID) - enforces isolation"
    )
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Task title (required, 1-200 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Task description (optional, max 1000 characters)"
    )
    completed: bool = Field(
        default=False,
        index=True,
        description="Task completion status (indexed for filtering)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task creation timestamp (auto-generated)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Task last update timestamp (auto-updated)"
    )

    # Define relationship for ORM queries
    owner: Optional["User"] = Relationship(
        back_populates="tasks",
        sa_relationship_kwargs={
            "lazy": "select"
        }
    )
