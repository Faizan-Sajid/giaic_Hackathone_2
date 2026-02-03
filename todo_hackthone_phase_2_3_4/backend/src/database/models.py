# Task: TASK-001, TASK-002
# Spec: Implementation Plan - Database Foundation
# Implementation: Conversation and Message models with required fields and relationships

from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import datetime


class Conversation(SQLModel, table=True):
    """
    Conversation entity representing a single conversation thread between user and AI assistant

    Task: TASK-001
    Spec: FR-003 (persist conversation messages to database)
    FR-004 (load conversation history from database)
    """

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Conversation integer primary key (auto-increment)"
    )
    user_id: str = Field(
        description="User identifier for conversation ownership (enforces isolation)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Conversation creation timestamp (auto-generated)"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Conversation last update timestamp (auto-updated)"
    )

    # Define relationship for ORM queries
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={
            "lazy": "select"
        }
    )


class Message(SQLModel, table=True):
    """
    Message entity representing individual messages within a conversation

    Task: TASK-002
    Spec: FR-003 (persist conversation messages to database with user, role, content)
    FR-004 (load conversation history from database)
    """

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Message integer primary key (auto-increment)"
    )
    conversation_id: int = Field(
        foreign_key="conversation.id",
        description="Foreign key referencing the conversation this message belongs to"
    )
    user_id: str = Field(
        description="User identifier for message author (copy for quick filtering)"
    )
    role: str = Field(
        description="Message role (either 'user' or 'assistant')"
    )
    content: str = Field(
        description="Message content text"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Message creation timestamp (auto-generated)"
    )

    # Define relationship for ORM queries
    conversation: Optional["Conversation"] = Relationship(
        back_populates="messages",
        sa_relationship_kwargs={
            "lazy": "select"
        }
    )