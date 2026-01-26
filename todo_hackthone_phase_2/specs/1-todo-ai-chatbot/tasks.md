# Task List: Todo AI Chatbot Implementation

**Feature**: 1-todo-ai-chatbot
**Created**: 2026-01-14
**Status**: Ready for execution

## TASK-001: Conversation model

**Task ID**: TASK-001
**Objective**: Create the Conversation model using SQLModel with all required fields and relationships
**Allowed files/folders**: `backend/database/models.py`
**Explicit acceptance criteria**:
- Conversation model exists with id, user_id, created_at, updated_at fields
- Proper SQLModel inheritance and field typing
- Primary key correctly configured
- Created and updated timestamps with proper defaults
- Model validates user_id is not null
**Explicit forbidden actions**:
- No direct database access in model
- No hardcoded values in model
- No other models referenced without proper imports

## TASK-002: Message model

**Task ID**: TASK-002
**Objective**: Create the Message model using SQLModel with all required fields and relationships to Conversation
**Allowed files/folders**: `backend/database/models.py`
**Explicit acceptance criteria**:
- Message model exists with id, conversation_id, user_id, role, content, created_at fields
- Proper relationship with Conversation model
- Role field restricted to "user" or "assistant"
- Content field properly typed for text storage
- Foreign key constraint on conversation_id
**Explicit forbidden actions**:
- No direct database access in model
- No hardcoded values in model
- No circular imports between models

## TASK-003: DB migration

**Task ID**: TASK-003
**Objective**: Create database migration scripts to initialize the database schema
**Allowed files/folders**: `backend/database/migrations/`, `backend/database/session.py`
**Explicit acceptance criteria**:
- Alembic migration files created for Conversation and Message tables
- Database session management properly configured
- Connection pooling configured
- Migration can be applied without errors
- Tables are created with proper constraints
**Explicit forbidden actions**:
- No hardcoded database credentials
- No direct SQL execution in migration files
- No modification of model files

## TASK-004: MCP server bootstrap

**Task ID**: TASK-004
**Objective**: Initialize the Model Context Protocol server with basic configuration
**Allowed files/folders**: `backend/mcp/server.py`, `backend/mcp/__init__.py`
**Explicit acceptance criteria**:
- MCP server starts without errors
- Proper initialization with stdio transport
- Database connection established for MCP tools
- Server can register tools
- Proper shutdown handling implemented
**Explicit forbidden actions**:
- No direct database access from server initialization
- No hardcoded values in configuration
- No implementation of specific tools yet

## TASK-005: add_task MCP tool

**Task ID**: TASK-005
**Objective**: Implement the add_task MCP tool that creates new todo tasks in the database
**Allowed files/folders**: `backend/mcp/tools/todo.py`, `backend/mcp/server.py`
**Explicit acceptance criteria**:
- add_task function accepts user_id, title, and optional description
- Validates required parameters
- Creates new task in database with proper user association
- Returns structured response with task information
- Proper error handling for invalid inputs
**Explicit forbidden actions**:
- No access to other users' tasks
- No bypassing user_id validation
- No direct database access without proper validation

## TASK-006: list_tasks MCP tool

**Task ID**: TASK-006
**Objective**: Implement the list_tasks MCP tool that retrieves user's todo tasks
**Allowed files/folders**: `backend/mcp/tools/todo.py`, `backend/mcp/server.py`
**Explicit acceptance criteria**:
- list_tasks function accepts user_id and optional status filter
- Retrieves tasks belonging to specified user only
- Applies status filter if provided
- Returns properly formatted response with task list
- Proper error handling for invalid inputs
**Explicit forbidden actions**:
- No access to other users' tasks
- No bypassing user_id validation
- No exposure of other users' data

## TASK-007: complete_task MCP tool

**Task ID**: TASK-007
**Objective**: Implement the complete_task MCP tool that marks a user's task as completed
**Allowed files/folders**: `backend/mcp/tools/todo.py`, `backend/mcp/server.py`
**Explicit acceptance criteria**:
- complete_task function accepts user_id and task_id
- Validates that task belongs to the specified user
- Updates task status to completed in database
- Returns confirmation response
- Proper error handling for invalid inputs or unauthorized access
**Explicit forbidden actions**:
- No modification of other users' tasks
- No bypassing ownership validation
- No access to tasks without proper validation

## TASK-008: update_task MCP tool

**Task ID**: TASK-008
**Objective**: Implement the update_task MCP tool that modifies a user's task details
**Allowed files/folders**: `backend/mcp/tools/todo.py`, `backend/mcp/server.py`
**Explicit acceptance criteria**:
- update_task function accepts user_id, task_id, and optional update fields
- Validates that task belongs to the specified user
- Updates specified fields in database
- Returns confirmation response
- Proper error handling for invalid inputs or unauthorized access
**Explicit forbidden actions**:
- No modification of other users' tasks
- No bypassing ownership validation
- No updates without proper validation

## TASK-009: delete_task MCP tool

**Task ID**: TASK-009
**Objective**: Implement the delete_task MCP tool that removes a user's task from database
**Allowed files/folders**: `backend/mcp/tools/todo.py`, `backend/mcp/server.py`
**Explicit acceptance criteria**:
- delete_task function accepts user_id and task_id
- Validates that task belongs to the specified user
- Deletes task from database
- Returns confirmation response
- Proper error handling for invalid inputs or unauthorized access
**Explicit forbidden actions**:
- No deletion of other users' tasks
- No bypassing ownership validation
- No deletion without proper validation

## TASK-010: Agent initialization (no HTTP)

**Task ID**: TASK-010
**Objective**: Initialize the OpenAI Agent with basic configuration without HTTP dependencies
**Allowed files/folders**: `backend/agents/config.py`, `backend/agents/__init__.py`
**Explicit acceptance criteria**:
- Agent instance created successfully
- Proper OpenAI API configuration
- No HTTP dependencies in initialization
- Agent can be instantiated without network calls
- Proper error handling for configuration issues
**Explicit forbidden actions**:
- No direct HTTP requests during initialization
- No hardcoded API keys in code
- No database access during initialization

## TASK-011: Agent prompt + tool bindings

**Task ID**: TASK-011
**Objective**: Configure the agent's system prompt and bind MCP tools to the agent
**Allowed files/folders**: `backend/agents/prompts.py`, `backend/agents/config.py`
**Explicit acceptance criteria**:
- System prompt includes rules for intent inference and tool usage
- MCP tools properly bound to agent
- Agent knows to use only available tools
- Prompt includes error handling instructions
- Agent follows rules about confirming actions and avoiding hallucinations
**Explicit forbidden actions**:
- No direct database access from agent
- No hardcoded values in prompts
- No network calls during binding process

## TASK-012: Chat API endpoint

**Task ID**: TASK-012
**Objective**: Create the POST /api/{user_id}/chat endpoint with JWT validation and agent integration
**Allowed files/folders**: `backend/api/chat.py`, `backend/api/deps.py`, `backend/main.py`
**Explicit acceptance criteria**:
- Endpoint accepts POST requests at /api/{user_id}/chat
- JWT validation verifies token and matches user_id to JWT sub
- Loads conversation history from database
- Executes agent with conversation context
- Persists user and assistant messages
- Returns response in specified format with conversation_id, response, and tool_calls
**Explicit forbidden actions**:
- No storing of conversation state in server memory
- No bypassing JWT validation
- No direct database access by agent
- No user_id mismatch between URL and JWT

## TASK-013: Custom Resizable Floating Chatbot

**Task ID**: TASK-013
**Objective**: Implement Custom Resizable Floating Chatbot that connects to the chat API
**Allowed files/folders**: `frontend/src/components/chat/FloatingChatbot.tsx`, `frontend/src/app/ClientWrapper.tsx`
**Explicit acceptance criteria**:
- Floating chatbot must be resizable and persistent across dashboard/tasks
- Must connect to /api/{user_id}/chat using the existing JWT authentication
- Must correctly handle and display the response format defined in TASK-012 (including tool_calls)
- Chatbot must maintain state when navigating between routes
- UI must include resize handles and proper constraints (min-width: 320px, min-height: 400px, max-width: 600px, max-height: 800px)
**Explicit forbidden actions**:
- No storing of JWT in localStorage
- No direct API calls without proper authentication
- No exposure of sensitive tokens in client code
- No fixed dimensions without resize capability