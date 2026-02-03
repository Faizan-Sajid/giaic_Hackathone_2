---
id: 003
title: "Fix OpenAI-Agents Package Name and Import Configuration"
stage: "red"
date: "2026-01-19"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "todo-ai-chatbot"
branch: "main"
user: "user"
command: "fix-openai-agents-package"
labels: ["agents-sdk", "package-import", "gemini-integration"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "backend/pyproject.toml"
  - "backend/src/agents/initialize.py"
tests: []
outcome: "Corrected package name and import statements for openai-agents"
evaluation: "Updated dependencies and imports to use correct package name"
---

# Fix OpenAI-Agents Package Name and Import Configuration

## Problem
The package name was incorrectly specified as `agents` instead of `openai-agents`. Additionally, the import statements needed to be consistent with the correct package structure.

## Root Cause
- Package name in pyproject.toml was incorrect
- Needed to ensure proper import statements align with the package structure

## Solution
Updated both files to use the correct configuration:
1. `backend/pyproject.toml`: Changed dependency to `openai-agents>=0.1.0`
2. `backend/src/agents/initialize.py`: Ensured imports use `from agents import ...` format while the package name is `openai-agents`

## Files Modified
- `backend/pyproject.toml`: Updated dependencies to use `openai-agents`
- `backend/src/agents/initialize.py`: Updated import statements and error handling

## Verification
- Package name is now correctly specified as `openai-agents` in dependencies
- Import statements use the correct `agents` module format
- Fallback mechanism in place for different library versions

## Next Steps
- Install/update dependencies with the corrected package name
- Test the chatbot functionality to ensure proper integration