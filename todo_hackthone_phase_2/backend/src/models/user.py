# Task: T008
# Spec: Data Model - User Entity (data-model.md lines 9-84)
# Implementation: User SQLModel with UUID primary key, unique email, bcrypt password hash

from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
import uuid

if TYPE_CHECKING:
    from .task import Task


class User(SQLModel, table=True):
    """
    User entity representing a registered user account

    Task: T008
    Spec: FR-001 (registration with email and password)
    SEC-001 (bcrypt password hashing)
    DINT-001 (email uniqueness)
    """

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True,
        description="User UUID primary key"
    )
    email: str = Field(
        unique=True,
        max_length=255,
        index=True,
        description="User email address (unique, indexed)"
    )
    password_hash: str = Field(
        description="Bcrypt hashed password (never plain text)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp"
    )

    # Relationship: User has many tasks
    tasks: List["Task"] = Relationship(back_populates="owner", cascade_delete=True)
