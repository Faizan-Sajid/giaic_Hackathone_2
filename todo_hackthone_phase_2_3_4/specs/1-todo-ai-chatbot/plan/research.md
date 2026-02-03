# Research Document: Todo AI Chatbot Implementation

**Feature**: 1-todo-ai-chatbot
**Date**: 2026-01-14

## Research Findings Summary

### 1. OpenAI Agents SDK Integration

**Decision**: Integrate OpenAI Agents SDK with FastAPI using async patterns
**Rationale**: The OpenAI Agents SDK is designed for async operations which aligns well with FastAPI's async nature. This allows for efficient handling of multiple concurrent conversations.
**Alternatives considered**:
- Synchronous blocking calls (rejected - would block event loop)
- Separate agent service (overcomplicated for initial implementation)

### 2. MCP SDK Implementation Patterns

**Decision**: Implement MCP tools as stateless functions with proper user validation
**Rationale**: MCP tools need to be stateless to maintain the architecture principle, with each tool validating user access to ensure data isolation.
**Alternatives considered**:
- Stateful MCP tools (rejected - violates statelessness principle)
- Shared database connections (accepted - connection pooling is acceptable)

### 3. JWT Validation in FastAPI

**Decision**: Use FastAPI dependencies with custom JWT validator that checks user_id matching
**Rationale**: FastAPI's dependency injection system provides clean separation of authentication concerns while allowing validation of user_id matching.
**Alternatives considered**:
- Manual validation in each endpoint (rejected - repetitive and error-prone)
- Middleware approach (rejected - less flexible for specific endpoint needs)

### 4. ChatKit Integration

**Decision**: Integrate ChatKit with the backend API using custom API configuration
**Rationale**: ChatKit provides a robust frontend framework that can be configured to work with our custom backend API endpoints.
**Alternatives considered**:
- Building custom chat interface (rejected - reinventing existing solution)
- Different chat frameworks (rejected - ChatKit specifically required by spec)

## MCP Tool Architecture

### Design Pattern
Each MCP tool follows the same pattern:
1. Accept user_id as the first parameter for validation
2. Validate that the user has access to the requested resource
3. Perform the database operation
4. Return structured response

### Error Handling
All MCP tools implement consistent error handling:
- Input validation errors return descriptive messages
- Authorization errors return 403-like responses
- Database errors are logged internally but return generic user messages

## Agent Configuration

### System Prompt Design
The agent system prompt includes:
- Rules for inferring intent from natural language
- Instructions to use only available MCP tools
- Guidelines for confirming actions with users
- Error handling procedures
- Prohibition on hallucinating success

### Conversation Context
The agent receives conversation history to maintain context:
- Previous messages are formatted appropriately for the agent
- History is limited to prevent token overflow
- Recent context is prioritized for relevance