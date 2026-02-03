# Data Model: Todo AI Chatbot

**Feature**: 1-todo-ai-chatbot
**Date**: 2026-01-14

## Entity Definitions

### Conversation
Represents a single conversation thread between user and AI assistant

**Fields**:
- `id` (Integer): Primary key, auto-incrementing
- `user_id` (String): Foreign key to user, required for data isolation
- `created_at` (DateTime): Timestamp when conversation was created
- `updated_at` (DateTime): Timestamp when conversation was last updated

**Validation Rules**:
- `user_id` must not be null
- `created_at` defaults to current timestamp
- `updated_at` updates on any modification

**Relationships**:
- One-to-many with Message entity (one conversation has many messages)

### Message
Represents individual messages within a conversation

**Fields**:
- `id` (Integer): Primary key, auto-incrementing
- `conversation_id` (Integer): Foreign key to Conversation, required
- `user_id` (String): Copy of user identifier for quick filtering
- `role` (String): Either "user" or "assistant", required
- `content` (Text): The actual message content, required
- `created_at` (DateTime): Timestamp when message was created

**Validation Rules**:
- `conversation_id` must reference existing conversation
- `role` must be either "user" or "assistant"
- `content` length must be within reasonable limits
- `user_id` must match the conversation owner

**Relationships**:
- Many-to-one with Conversation entity (many messages belong to one conversation)

### Todo Task
Represents user's todo tasks managed through the system

**Fields**:
- `id` (Integer): Primary key, auto-incrementing
- `user_id` (String): Foreign key to user, required for data isolation
- `title` (String): Task title, required
- `description` (Text): Optional task description
- `status` (String): Task status (e.g., "pending", "completed"), defaults to "pending"
- `created_at` (DateTime): Timestamp when task was created
- `updated_at` (DateTime): Timestamp when task was last updated

**Validation Rules**:
- `user_id` must not be null
- `title` must not be null or empty
- `status` must be one of allowed values
- `user_id` must match the authenticated user

**State Transitions**:
- "pending" → "completed" (via complete_task MCP tool)
- "completed" → "pending" (via update_task MCP tool with status change)
- "pending" → "pending" (via update_task MCP tool with other fields)

## Database Constraints

### Primary Keys
- All entities have auto-incrementing integer primary keys
- Primary keys are never exposed to external systems directly

### Foreign Keys
- `Message.conversation_id` references `Conversation.id`
- All foreign key relationships enforce referential integrity

### Unique Constraints
- None required for basic functionality
- Additional indexes may be added for performance optimization

### Indexes
- Index on `Conversation.user_id` for efficient user-based queries
- Index on `Message.conversation_id` for conversation history retrieval
- Index on `TodoTask.user_id` for efficient user-based queries