# Implementation Plan: Todo AI Chatbot (Basic Level)

**Feature**: 1-todo-ai-chatbot
**Created**: 2026-01-14
**Status**: Draft
**Plan Version**: 1.0.0

## Technical Context

This implementation will create a stateless, AI-powered conversational interface for managing todo tasks. The system will use OpenAI Agents SDK for natural language processing, MCP SDK for database operations, FastAPI for the backend API, and ChatKit for the frontend. All conversation state will be stored in the database, with no state maintained in the server or AI agent.

**Technologies**:
- Backend: FastAPI 0.115+, Python 3.13+
- Database: PostgreSQL 16+ with SQLModel 0.0.22+
- AI: OpenAI Agents SDK
- MCP: Model Context Protocol SDK
- Frontend: OpenAI ChatKit
- Authentication: JWT tokens

## Constitution Check

- [x] Spec-first development: Following approved spec from spec.md
- [x] AI as controlled executor: AI will only access data through MCP tools
- [x] Determinism and reproducibility: State stored in database, stateless server
- [x] Production-grade standards: Following security-first design
- [x] Stateless architecture: Server maintains no runtime state
- [x] Security standards: JWT authentication, user data isolation
- [x] Technology baseline: Using approved versions

## Phase 0: Research & Preparation

### Research Tasks

1. **OpenAI Agents SDK Integration**: Research how to integrate the OpenAI Agents SDK with FastAPI backend
2. **MCP SDK Implementation**: Research implementation patterns for MCP tools with database operations
3. **JWT Validation in FastAPI**: Research best practices for JWT validation with user_id matching
4. **ChatKit Integration**: Research integration of ChatKit with the backend API

## Phase 1: Foundation Setup

### Step 1: Database Foundation

**Goal**: Establish database schema and models for conversations and messages

**What is implemented**:
- PostgreSQL database schema with Conversation and Message tables
- SQLModel definitions for Conversation and Message entities
- Database connection setup with connection pooling
- Migration scripts for schema creation

**What is explicitly forbidden**:
- Direct database access from AI agent
- Hardcoded database credentials
- Schema modifications outside of migration process

**Completion criteria**:
- Database schema matches entities defined in spec
- Connection pooling configured properly
- Unit tests for database operations pass
- Migration scripts successfully create tables

### Step 2: MCP Server Bootstrap

**Goal**: Set up the Model Context Protocol server to handle todo operations

**What is implemented**:
- MCP server initialization with stdio transport
- Base MCP tool registration framework
- Database connection for MCP tools
- User authentication validation in MCP layer

**What is explicitly forbidden**:
- MCP tools with direct access to other users' data
- MCP tools that don't validate user_id
- MCP tools that maintain state between calls

**Completion criteria**:
- MCP server starts successfully
- Base tool registration works
- Database connection established for MCP tools
- Authentication validation functions correctly

### Step 3: Individual MCP Tools Implementation

**Goal**: Implement each MCP tool for todo operations one by one

**Step 3.1: add_task MCP Tool**

**Goal**: Implement the add_task MCP tool

**What is implemented**:
- add_task function accepting user_id, title, and optional description
- Input validation for required parameters
- Database insertion for new todo task
- Proper error handling and response formatting

**What is explicitly forbidden**:
- Creating tasks without validating user_id
- Adding tasks without proper input validation
- Returning success without database confirmation

**Completion criteria**:
- add_task tool accepts parameters as specified in spec
- Task is properly inserted into database
- Proper error responses for invalid inputs
- User isolation maintained (can't access others' tasks)

**Step 3.2: list_tasks MCP Tool**

**Goal**: Implement the list_tasks MCP tool

**What is implemented**:
- list_tasks function accepting user_id and optional status filter
- Database query to retrieve user's tasks
- Filtering by status if provided
- Proper response formatting

**What is explicitly forbidden**:
- Returning other users' tasks
- Bypassing user_id validation
- Exposing sensitive data in responses

**Completion criteria**:
- list_tasks tool accepts parameters as specified in spec
- Correctly retrieves user's tasks from database
- Status filtering works when provided
- User isolation maintained

**Step 3.3: complete_task MCP Tool**

**Goal**: Implement the complete_task MCP tool

**What is implemented**:
- complete_task function accepting user_id and task_id
- Validation that task belongs to user
- Database update to mark task as completed
- Proper response and error handling

**What is explicitly forbidden**:
- Completing other users' tasks
- Updating tasks without ownership validation
- Returning success without database confirmation

**Completion criteria**:
- complete_task tool accepts parameters as specified in spec
- Task is properly updated in database
- Proper error responses for invalid operations
- User isolation maintained

**Step 3.4: update_task MCP Tool**

**Goal**: Implement the update_task MCP tool

**What is implemented**:
- update_task function accepting user_id, task_id, and optional update fields
- Validation that task belongs to user
- Database update with provided fields
- Proper response and error handling

**What is explicitly forbidden**:
- Updating other users' tasks
- Updating tasks without ownership validation
- Partial updates without proper validation

**Completion criteria**:
- update_task tool accepts parameters as specified in spec
- Task is properly updated in database
- Proper error responses for invalid operations
- User isolation maintained

**Step 3.5: delete_task MCP Tool**

**Goal**: Implement the delete_task MCP tool

**What is implemented**:
- delete_task function accepting user_id and task_id
- Validation that task belongs to user
- Database deletion of task
- Proper response and error handling

**What is explicitly forbidden**:
- Deleting other users' tasks
- Deleting tasks without ownership validation
- Returning success without database confirmation

**Completion criteria**:
- delete_task tool accepts parameters as specified in spec
- Task is properly deleted from database
- Proper error responses for invalid operations
- User isolation maintained

### Step 4: Agent Setup & Prompt

**Goal**: Configure the OpenAI agent with appropriate instructions and tool access

**What is implemented**:
- Agent initialization with OpenAI Agents SDK
- System prompt defining agent behavior and rules
- Tool access configuration to MCP tools
- Conversation history integration

**What is explicitly forbidden**:
- Agent with direct database access
- Agent without proper tool restrictions
- Agent without conversation history context

**Completion criteria**:
- Agent initialized successfully with SDK
- Agent follows rules defined in spec (infer intent, choose correct tool, etc.)
- Agent can access MCP tools appropriately
- Agent receives conversation history context

### Step 5: Stateless Chat Endpoint

**Goal**: Create the POST /api/{user_id}/chat endpoint following stateless principles

**What is implemented**:
- POST endpoint at /api/{user_id}/chat with proper authentication
- JWT validation ensuring URL user_id matches JWT sub
- Conversation history loading from database
- Agent execution with conversation context
- Response formatting with conversation_id, response, and tool_calls
- Message persistence for both user and assistant messages

**What is explicitly forbidden**:
- Storing conversation state in server memory
- Bypassing JWT validation
- Allowing user_id mismatch between URL and JWT
- Direct database access by agent

**Completion criteria**:
- Endpoint accepts requests as specified in spec
- JWT validation works correctly
- Conversation history loads properly
- Agent executes and returns expected response format
- Messages are persisted correctly
- No state retained between requests

### Step 6: ChatKit Frontend

**Goal**: Implement the ChatKit frontend to interact with the backend API

**What is implemented**:
- ChatKit component configuration
- API integration with the chat endpoint
- User authentication handling
- Conversation display and interaction

**What is explicitly forbidden**:
- Storing sensitive tokens in localStorage
- Bypassing authentication requirements
- Direct API access without proper headers

**Completion criteria**:
- ChatKit component renders properly
- Successful communication with backend API
- Proper authentication handling
- Smooth conversation experience for users

## Phase 2: Integration & Testing

### Integration Tasks
- End-to-end testing of conversation flow
- MCP tool integration validation
- Authentication flow testing
- Error handling verification

### Quality Gates
- All MCP tools work securely with proper user isolation
- AI cannot access other users' data
- Statelessness maintained throughout
- Performance meets success criteria