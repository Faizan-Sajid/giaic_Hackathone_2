---
id: 002
title: "Fix Gemini API Integration"
stage: "red"
date: "2026-01-19"
surface: "agent"
model: "Claude Sonnet 4.5"
feature: "todo-ai-chatbot"
branch: "main"
user: "user"
command: "fix-gemini-api-integration"
labels: ["api-integration", "gemini", "agent-sdk"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "backend/src/agents/initialize.py"
tests: []
outcome: "Configured OpenAI Agents SDK to use Gemini API endpoint"
evaluation: "Updated agent initialization to set proper environment variables for Gemini API"
---

# Fix Gemini API Integration

## Problem
The chatbot was showing the error: "The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable" when trying to use Gemini API instead of OpenAI API.

## Root Cause
The OpenAI Agents SDK is designed for OpenAI services and looks for the OPENAI_API_KEY environment variable. Even though the configuration was set up for Gemini API, the SDK was still expecting OpenAI-specific configuration.

## Solution
Updated the agent initialization in `backend/src/agents/initialize.py` to:
1. Set the `OPENAI_API_KEY` environment variable to the Gemini API key
2. Set the `OPENAI_BASE_URL` environment variable to the Gemini endpoint
3. This allows the OpenAI Agents SDK to work with the Gemini API through its OpenAI-compatible endpoint

## Files Modified
- `backend/src/agents/initialize.py`: Added environment variable configuration to use Gemini API

## Verification
- The OpenAI Agents SDK will now use the configured Gemini API key and endpoint
- The error should be resolved and the chatbot should connect to Gemini API

## Next Steps
- Ensure GEMINI_API_KEY environment variable is properly set in your deployment
- Test the chatbot functionality with Gemini API