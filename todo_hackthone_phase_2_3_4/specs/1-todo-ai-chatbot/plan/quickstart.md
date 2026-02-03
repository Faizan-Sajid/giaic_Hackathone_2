# Quickstart Guide: Todo AI Chatbot Implementation

**Feature**: 1-todo-ai-chatbot
**Date**: 2026-01-14

## Prerequisites

### System Requirements
- Python 3.13+
- PostgreSQL 16+
- Node.js 22 LTS
- uv (Python package manager)

### Environment Setup
1. Install Python 3.13+ and verify with `python --version`
2. Install PostgreSQL 16+ and start the service
3. Install Node.js 22 LTS and verify with `node --version`
4. Install uv with `pip install uv`

### Environment Variables
Create a `.env` file in the backend directory with:
```
DATABASE_URL=postgresql://username:password@localhost:5432/todo_chatbot
JWT_SECRET=your-super-secret-jwt-key-here
OPENAI_API_KEY=your-openai-api-key
```

## Repository Structure

```
todo_hackthone_phase_2/
├── backend/
│   ├── main.py              # FastAPI application entrypoint
│   ├── database/
│   │   ├── models.py        # SQLModel definitions
│   │   └── session.py       # Database session management
│   ├── api/
│   │   ├── deps.py          # Dependency injection (JWT validation)
│   │   └── chat.py          # Chat endpoint implementation
│   ├── mcp/
│   │   ├── server.py        # MCP server implementation
│   │   └── tools/           # MCP tools (add_task, list_tasks, etc.)
│   ├── agents/
│   │   ├── config.py        # Agent configuration
│   │   └── prompts.py       # Agent system prompts
│   └── tests/               # Test files
└── frontend/
    ├── pages/               # Next.js pages
    ├── components/          # React components
    └── chatkit-config.js    # ChatKit configuration
```

## Implementation Steps

### 1. Database Foundation
1. Set up PostgreSQL database with required tables
2. Create SQLModel models for Conversation and Message
3. Implement database session management
4. Create migration scripts

### 2. MCP Server Bootstrap
1. Initialize MCP server with stdio transport
2. Set up database connection for MCP tools
3. Implement user validation framework

### 3. MCP Tools Implementation
1. Implement `add_task` MCP tool
2. Implement `list_tasks` MCP tool
3. Implement `complete_task` MCP tool
4. Implement `update_task` MCP tool
5. Implement `delete_task` MCP tool

### 4. Agent Setup
1. Configure OpenAI Agent with appropriate system prompt
2. Connect agent to MCP tools
3. Implement conversation history loading for agent context

### 5. Chat API Endpoint
1. Create `/api/{user_id}/chat` endpoint
2. Implement JWT validation with user_id matching
3. Integrate with agent and MCP tools
4. Handle message persistence

### 6. Frontend Integration
1. Configure ChatKit component
2. Connect to backend API
3. Implement authentication flow

## Development Commands

### Backend
```bash
# Install dependencies
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install fastapi[standard] sqlmodel openai agents mcp-sdk psycopg2-binary python-jose[cryptography] passlib[bcrypt]

# Run the application
uv run uvicorn main:app --reload --port 8000

# Run tests
uv run pytest
```

### Frontend
```bash
# Install dependencies
cd frontend
npm install

# Run development server
npm run dev
```

## Testing the Implementation

### Unit Tests
- Database model validation
- MCP tool functionality
- JWT validation logic

### Integration Tests
- End-to-end chat flow
- MCP tool security (user isolation)
- API contract compliance

### Manual Testing
1. Start backend server
2. Navigate to frontend
3. Authenticate with valid JWT
4. Send a message like "Add a task to buy groceries"
5. Verify task appears in user's task list