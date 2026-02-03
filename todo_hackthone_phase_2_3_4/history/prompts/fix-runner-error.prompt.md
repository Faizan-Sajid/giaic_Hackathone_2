---
id: 001
title: "Fix Runner.run() Unexpected Keyword Argument Error"
stage: "red"
date: "2026-01-19"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "todo-ai-chatbot"
branch: "main"
user: "user"
command: "fix-runner-error"
labels: ["bug-fix", "agent-sdk", "chat-api"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "backend/src/api/chat.py"
tests: []
outcome: "Fixed the Runner.run() call to use correct positional arguments instead of keyword arguments"
evaluation: "Verified the fix matches the OpenAI Agents SDK documentation and existing test patterns"
---

# Fix Runner.run() Unexpected Keyword Argument Error

## Problem
The chatbot API was throwing the error: `Runner.run() got an unexpected keyword argument 'agent'`

## Root Cause
In `backend/src/api/chat.py`, the `Runner.run()` method was being called with keyword arguments:
```python
result = await Runner.run(
    agent=agent,  # Incorrect - using keyword argument
    input=request.message  # Incorrect - using keyword argument
)
```

According to the OpenAI Agents SDK documentation, `Runner.run()` expects positional arguments.

## Solution
Changed the call to use positional arguments as shown in the official documentation and confirmed by test files:
```python
result = await Runner.run(
    agent,               # Correct - positional argument
    request.message      # Correct - positional argument
)
```

Note: Context parameter was considered but omitted for safety as it may not be supported in all versions of the SDK and could cause similar errors.

## Files Modified
- `backend/src/api/chat.py`: Fixed the Runner.run() call to use correct positional arguments

## Verification
- Updated code follows the OpenAI Agents SDK documentation pattern
- Matches the usage pattern seen in test files (e.g., patch_and_test_agent.py)
- Should resolve the "unexpected keyword argument 'agent'" error

## Next Steps
- Test the chatbot functionality to confirm the fix works
- Verify that the agent can properly process user messages