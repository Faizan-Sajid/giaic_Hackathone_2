"""
Complete example usage of the TODO chatbot with proper user context handling.

This file demonstrates how to properly initialize the agent, set user context,
and run the chat system with all fixes applied.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import required modules
from src.agents.initialize import get_configured_agent
from src.mcp.tools.todo import set_current_user_id, clear_current_user_id
from agents import Runner


def example_chat_interaction():
    """
    Example demonstrating how to use the chat system with proper user context
    """
    print("=== TODO Chatbot Example ===")

    # Get the configured agent
    agent = get_configured_agent()

    if agent is None:
        print("❌ Agent not configured - check GEMINI_API_KEY environment variable")
        return

    print("✅ Agent configured successfully")

    # Example user ID (in real application, this comes from authentication)
    user_id = "123e4567-e89b-12d3-a456-426614174000"  # Example UUID

    # Example user message
    user_message = "Add a task: Buy groceries"

    print(f"\n👤 User ID: {user_id}")
    print(f"💬 Message: {user_message}")

    try:
        # Set user context BEFORE running the agent
        print("\n🔐 Setting user context...")
        set_current_user_id(user_id)

        print("🏃 Running agent...")
        # Run the agent with the user message
        result = Runner.run_sync(agent, user_message)

        print("✅ Agent execution completed")

        # Handle the result
        if isinstance(result, dict):
            response_text = result.get('final_output', result.get('response', result.get('content', str(result))))
        else:
            response_text = getattr(result, 'final_output', str(result))

        print(f"\n🤖 Agent Response: {response_text}")

    except Exception as e:
        print(f"❌ Error during agent execution: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        # Clear user context AFTER running the agent
        print("\n🔓 Clearing user context...")
        clear_current_user_id()
        print("✅ User context cleared")


def example_direct_tool_usage():
    """
    Example demonstrating how to use the tools directly with user context
    """
    print("\n=== Direct Tool Usage Example ===")

    from src.mcp.tools.todo import add_task, list_tasks

    # Example user ID
    user_id = "123e4567-e89b-12d3-a456-426614174000"

    # Set user context
    set_current_user_id(user_id)

    try:
        print("📝 Adding a task...")
        # Add a task directly
        result = add_task(
            title="Learn Python",
            description="Complete Python tutorial",
            user_id=user_id  # This can be passed explicitly or taken from context
        )

        print(f"✅ Add task result: {result}")

        print("\n📋 Listing tasks...")
        # List tasks for the user
        result = list_tasks(user_id=user_id)

        print(f"✅ List tasks result: {result}")

    except Exception as e:
        print(f"❌ Error in direct tool usage: {str(e)}")
        import traceback
        traceback.print_exc()

    finally:
        # Clear user context
        clear_current_user_id()


def simulate_fastapi_chat_endpoint(user_id: str, message: str):
    """
    Simulate how the FastAPI chat endpoint works with proper user context handling
    """
    print(f"\n=== Simulating FastAPI Chat Endpoint ===")
    print(f"👤 User ID: {user_id}")
    print(f"💬 Message: {message}")

    # Get agent
    agent = get_configured_agent()
    if agent is None:
        return {"error": "Agent not configured"}

    try:
        # Set user context before running agent (THIS WAS THE MISSING PART!)
        print("🔐 Setting user context in chat endpoint...")
        set_current_user_id(user_id)

        print("🏃 Running agent in endpoint...")
        # Run agent
        result = Runner.run_sync(agent, message)

        # Process result
        if isinstance(result, dict):
            response_text = result.get('final_output', result.get('response', result.get('content', str(result))))
        else:
            response_text = getattr(result, 'final_output', str(result))

        print(f"✅ Endpoint response: {response_text}")

        return {"response": response_text, "success": True}

    except Exception as e:
        print(f"❌ Error in chat endpoint: {str(e)}")
        import traceback
        traceback.print_exc()

        return {"response": f"An error occurred: {str(e)}", "success": False}

    finally:
        # Always clear user context
        print("🔓 Clearing user context after endpoint execution...")
        clear_current_user_id()


if __name__ == "__main__":
    print("🚀 Starting TODO Chatbot Example")

    # Example 1: Basic chat interaction
    example_chat_interaction()

    # Example 2: Direct tool usage
    example_direct_tool_usage()

    # Example 3: Simulated FastAPI endpoint (this shows the fix!)
    simulate_fastapi_chat_endpoint(
        user_id="123e4567-e89b-12d3-a456-426614174000",
        message="Add a task: Complete the project documentation"
    )

    print("\n✅ All examples completed!")
    print("\n📋 SUMMARY OF FIXES APPLIED:")
    print("1. ✅ Fixed TextContent access: Changed .get('text') to .text attribute")
    print("2. ✅ Improved async/sync handling: Better event loop management")
    print("3. ✅ Added proper user context: set_current_user_id() before agent.run()")
    print("4. ✅ Added error handling: Try-catch with traceback logging")
    print("5. ✅ Thread-safe context: Proper cleanup with finally blocks")
    print("6. ✅ Fixed nested event loops: Used run_coroutine_threadsafe for main thread")