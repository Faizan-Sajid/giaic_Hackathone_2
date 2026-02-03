# API Contract: Todo AI Chatbot

**Feature**: 1-todo-ai-chatbot
**Date**: 2026-01-14

## Base Information
- **Base URL**: `/api`
- **Protocol**: HTTPS/HTTP
- **Content-Type**: `application/json`
- **Authentication**: JWT Bearer token in Authorization header

## Authentication
All endpoints require JWT authentication with the following validation:
- Token must be present in `Authorization: Bearer {token}` header
- JWT payload must contain `sub` field
- URL parameter `{user_id}` must match JWT `sub` field
- Token must not be expired

## Endpoints

### POST /{user_id}/chat

**Description**: Process a chat message and return AI response with potential tool calls

**Authentication**: Required (JWT with user_id validation)

**Path Parameters**:
- `user_id` (string): User identifier that must match JWT `sub` claim

**Request Body**:
```json
{
  "conversation_id": "integer | null",
  "message": "string"
}
```

**Request Body Validation**:
- `message` is required and must be a non-empty string
- `conversation_id` must be a positive integer if provided

**Response**:
```json
{
  "conversation_id": "integer",
  "response": "string",
  "tool_calls": "array"
}
```

**Response Fields**:
- `conversation_id`: The ID of the conversation (newly created if null was provided)
- `response`: The AI-generated response to the user's message
- `tool_calls`: Array of tool calls executed by the AI agent

**Response Codes**:
- `200`: Success - message processed and response returned
- `400`: Bad Request - invalid request format or missing required fields
- `401`: Unauthorized - missing or invalid JWT token
- `403`: Forbidden - JWT token valid but user_id doesn't match JWT `sub`
- `422`: Unprocessable Entity - validation errors in request body
- `500`: Internal Server Error - unexpected server error

**Example Request**:
```http
POST /api/user123/chat
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "conversation_id": null,
  "message": "Add a task to buy groceries"
}
```

**Example Response**:
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "conversation_id": 1,
  "response": "I've added the task 'buy groceries' to your list.",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {
        "user_id": "user123",
        "title": "buy groceries"
      }
    }
  ]
}
```

### GET /{user_id}/health

**Description**: Health check endpoint for the service

**Authentication**: Not required

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "string (ISO 8601 datetime)"
}
```

**Response Codes**:
- `200`: Healthy - service operational
- `500`: Unhealthy - service experiencing issues

## Error Response Format

All error responses follow this format:

```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "object | null"
  }
}
```

**Common Error Codes**:
- `INVALID_REQUEST`: Request format is invalid
- `AUTHENTICATION_FAILED`: JWT token is missing or invalid
- `AUTHORIZATION_FAILED`: User doesn't have access to requested resource
- `VALIDATION_ERROR`: Request parameters failed validation
- `INTERNAL_ERROR`: Unexpected server error occurred
- `DATABASE_ERROR`: Database operation failed