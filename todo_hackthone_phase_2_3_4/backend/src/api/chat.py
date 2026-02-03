from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import json
from datetime import datetime

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..api.routes.auth import get_current_user
from ..database.models import Conversation, Message
from ..database.session import get_session
from ..agents.initialize import get_configured_agent

router = APIRouter()


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint
    """
    conversation_id: Optional[int] = None
    message: str


class ToolCall(BaseModel):
    """
    Model for representing a tool call made by the agent
    """
    name: str
    arguments: Dict[str, Any]


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint
    """
    conversation_id: int
    response: str
    tool_calls: List[ToolCall]


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    current_user = Depends(get_current_user),
    db_session: AsyncSession = Depends(get_session)
) -> ChatResponse:
    """
    Chat endpoint that processes user messages and returns AI responses
    """
    # Validate UUID format before proceeding
    try:
        from uuid import UUID
        UUID(user_id)  # Will raise ValueError if invalid
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid user_id format: '{user_id}'. Must be a valid UUID."
        )

    # Verify that the authenticated user matches the user_id in the URL
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID does not match authenticated user"
        )

    # Load conversation history if conversation_id is provided
    conversation = None
    if request.conversation_id:
        conversation_query = await db_session.execute(
            select(Conversation).where(
                Conversation.id == request.conversation_id,
                Conversation.user_id == user_id
            )
        )
        conversation = conversation_query.scalar_one_or_none()

        if not conversation:
            # If conversation not found, create a new one (better UX for in-memory DB resets)
            print(f"Warning: Conversation {request.conversation_id} not found for user {user_id}. Creating new conversation.")
            conversation = Conversation(user_id=user_id)
            db_session.add(conversation)
            await db_session.commit()
            await db_session.refresh(conversation)
    else:
        # Create a new conversation
        conversation = Conversation(user_id=user_id)
        db_session.add(conversation)
        await db_session.commit()
        await db_session.refresh(conversation)

    # Save the user's message to the database
    user_message = Message(
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content=request.message
    )
    db_session.add(user_message)
    await db_session.commit()
    await db_session.refresh(user_message)

    # Get the configured agent with all tools already bound
    agent = get_configured_agent()

    # Response Handling: If agent is None, return the 'System not configured' message as a valid JSON
    if agent is None:
        error_response = "System not configured: GEMINI_API_KEY is missing. Chat functionality is unavailable."

        assistant_message = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content=error_response
        )
        db_session.add(assistant_message)
        await db_session.commit()

        return ChatResponse(
            conversation_id=conversation.id,
            response=error_response,
            tool_calls=[]
        )

    try:
        # Import Runner from agents - only if agents are available
        try:
            from agents import Runner
            AGENTS_AVAILABLE_IN_CHAT = True
        except ImportError:
            AGENTS_AVAILABLE_IN_CHAT = False
            raise Exception("Agent system is not properly configured")

        # When running in an async context (like FastAPI), we need to run the agent in a separate thread
        # or use the async methods if available in the openai-agents package
        import asyncio
        import concurrent.futures
        from ..mcp.tools.todo import set_current_user_id, clear_current_user_id, get_current_user_id
        import traceback

        def run_agent_sync():
            try:
                print(f"DEBUG chat_endpoint: Setting user context to {user_id}")

                # Set the user context before running the agent using the global function
                set_current_user_id(user_id)

                # Verify context was set
                context_check = get_current_user_id()
                print(f"DEBUG chat_endpoint: Context verification - stored user_id={context_check}")

                if context_check != user_id:
                    print(f"ERROR chat_endpoint: Context mismatch! Expected {user_id}, got {context_check}")

                # Run without run_config to avoid session_input_callback issues
                # The user context is now managed through the tool context
                result = Runner.run_sync(
                    agent,
                    request.message
                )
                print(f"DEBUG chat_endpoint: Agent execution completed successfully")
                return result
            finally:
                # Clear the user context after running
                print(f"DEBUG chat_endpoint: Clearing user context")
                clear_current_user_id()

                # Verify context was cleared
                final_check = get_current_user_id()
                print(f"DEBUG chat_endpoint: Final context check - user_id={final_check} (should be None)")

        # Run the synchronous agent execution in a thread pool to avoid blocking
        print(f"DEBUG chat_endpoint: Running agent for user_id={user_id}, message='{request.message}'")
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, run_agent_sync)
        print(f"DEBUG chat_endpoint: Agent result received")

        # Handle the result appropriately based on its type
        if isinstance(result, dict):
            # If result is a dictionary, try to get the response text from common keys
            response_text = result.get('final_output', result.get('response', result.get('content', str(result))))
            # Try to get tool calls from the dictionary
            raw_tool_calls = result.get('tool_calls', [])
        else:
            # If result is an object, try to access its attributes
            response_text = getattr(result, 'final_output', str(result))
            raw_tool_calls = getattr(result, 'tool_calls', [])

        # Process any tool calls that were made
        tool_calls = []
        if raw_tool_calls:
            for tool_call in raw_tool_calls:
                if isinstance(tool_call, dict):
                    # Handle tool_call as dictionary
                    name = tool_call.get('name', 'unknown')
                    arguments = tool_call.get('arguments', {})
                    if isinstance(arguments, str):
                        try:
                            arguments = json.loads(arguments)
                        except json.JSONDecodeError:
                            arguments = {}

                    tool_calls.append(
                        ToolCall(
                            name=name,
                            arguments=arguments
                        )
                    )
                elif hasattr(tool_call, 'function'):
                    # Handle tool_call as object with function attribute
                    arguments = {}
                    if hasattr(tool_call.function, 'arguments') and tool_call.function.arguments:
                        try:
                            arguments = json.loads(tool_call.function.arguments)
                        except json.JSONDecodeError:
                            arguments = {}

                    tool_calls.append(
                        ToolCall(
                            name=tool_call.function.name,
                            arguments=arguments
                        )
                    )
                else:
                    # Handle tool_call as object with direct name and arguments
                    if hasattr(tool_call, 'name'):
                        tool_calls.append(
                            ToolCall(
                                name=getattr(tool_call, 'name', 'unknown'),
                                arguments=getattr(tool_call, 'arguments', {})
                            )
                        )

        # Create the agent response message
        assistant_message = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content=response_text
        )
        db_session.add(assistant_message)
        await db_session.commit()

        # Ensure the response is returned in a format the frontend expects (matching ChatResponse model)
        return ChatResponse(
            conversation_id=conversation.id,
            response=response_text,
            tool_calls=tool_calls
        )

    except Exception as e:
        # Handle any errors in agent execution gracefully
        error_response = f"Chat service temporarily unavailable: {str(e)}. Please try again later."

        # Create the error response message
        assistant_message = Message(
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content=error_response
        )
        db_session.add(assistant_message)
        await db_session.commit()

        return ChatResponse(
            conversation_id=conversation.id,
            response=error_response,
            tool_calls=[]
        )