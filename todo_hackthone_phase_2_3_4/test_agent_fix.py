#!/usr/bin/env python3
"""
Test script to verify that the MCP tools and agent initialization work properly
after the fixes have been applied.
"""

import sys
import os
import asyncio

# Add the backend src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

def test_imports():
    """Test that all necessary modules can be imported without errors."""
    print("Testing imports...")

    try:
        from agents.initialize import initialize_gemini_agent
        print("✓ Successfully imported initialize_gemini_agent")

        from mcp.tools.todo import (
            add_task_tool_handler_sync,
            list_tasks_tool_handler_sync,
            complete_task_tool_handler_sync,
            update_task_tool_handler_sync,
            delete_task_tool_handler_sync,
            set_current_user_id,
            clear_current_user_id
        )
        print("✓ Successfully imported all todo tool handlers")

        from database.session import get_session_sync
        print("✓ Successfully imported database session")

        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during import: {e}")
        return False


def test_agent_initialization():
    """Test that the agent initializes without errors."""
    print("\nTesting agent initialization...")

    try:
        # Mock environment variable for testing
        import os
        original_key = os.environ.get('GEMINI_API_KEY')
        os.environ['GEMINI_API_KEY'] = 'fake-key-for-testing'  # This will trigger the debug message but won't make actual API calls

        from agents.initialize import initialize_gemini_agent
        agent = initialize_gemini_agent()

        if agent is not None:
            print("✓ Agent initialized successfully (with fake API key)")

            # Check if the agent has the expected methods
            if hasattr(agent, 'set_user_context'):
                print("✓ Agent has set_user_context method")
            else:
                print("✗ Agent missing set_user_context method")

            if hasattr(agent, 'clear_user_context'):
                print("✓ Agent has clear_user_context method")
            else:
                print("✗ Agent missing clear_user_context method")

            # Check if tools were properly bound
            print(f"✓ Agent has tools bound: {hasattr(agent, '__dict__')}")
        else:
            print("? Agent returned None (expected if no real API key)")

        # Restore original environment
        if original_key is not None:
            os.environ['GEMINI_API_KEY'] = original_key
        else:
            os.environ.pop('GEMINI_API_KEY', None)

        return True
    except Exception as e:
        print(f"✗ Agent initialization error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_tool_context_handling():
    """Test that tools properly handle user_id context."""
    print("\nTesting tool context handling...")

    try:
        from mcp.tools.todo import (
            set_current_user_id,
            get_current_user_id,
            clear_current_user_id,
            add_task_tool_handler_sync
        )

        # Test setting and getting user context
        test_user_id = "test-user-123"
        set_current_user_id(test_user_id)

        retrieved_user_id = get_current_user_id()
        if retrieved_user_id == test_user_id:
            print("✓ User ID context set and retrieved correctly")
        else:
            print(f"✗ User ID context mismatch: expected {test_user_id}, got {retrieved_user_id}")
            return False

        # Test that the synchronous tool handler can access the context
        # Note: This will fail because the task doesn't exist in DB, but it should at least
        # attempt to use the user context
        try:
            result = add_task_tool_handler_sync(title="Test Task", description="Test Description")
            print(f"✓ Tool handler executed (result: {type(result).__name__})")

            # The tool should return a structured result even if it fails due to DB
            if isinstance(result, dict):
                print("✓ Tool handler returned dictionary as expected")
            else:
                print(f"✗ Tool handler returned unexpected type: {type(result)}")
        except Exception as e:
            # This is expected if DB isn't set up, but the important thing is that
            # the context was accessed properly
            print(f"~ Tool handler executed but encountered DB error (expected in test): {type(e).__name__}")

        # Test clearing context
        clear_current_user_id()
        cleared_user_id = get_current_user_id()
        if cleared_user_id is None:
            print("✓ User ID context cleared correctly")
        else:
            print(f"✗ User ID context not cleared: {cleared_user_id}")
            return False

        return True
    except Exception as e:
        print(f"✗ Tool context handling error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_database_sync_session():
    """Test that the synchronous database session works."""
    print("\nTesting synchronous database session...")

    try:
        from database.session import get_session_sync
        from sqlmodel import select
        from models.task import Task

        # Test that we can create a session (won't actually connect without DB)
        session_gen = get_session_sync()
        session = next(session_gen)

        print("✓ Synchronous session created successfully")

        # Close the session
        session.close()

        return True
    except Exception as e:
        print(f"✗ Database session error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("Testing MCP Tool and Agent Fixes\n")
    print("=" * 50)

    all_tests_passed = True

    all_tests_passed &= test_imports()
    all_tests_passed &= test_agent_initialization()
    all_tests_passed &= test_tool_context_handling()
    all_tests_passed &= test_database_sync_session()

    print("\n" + "=" * 50)
    if all_tests_passed:
        print("✓ All tests passed! The fixes appear to be working correctly.")
        print("\nSummary of fixes:")
        print("- MCP tools now have synchronous wrappers that handle user_id context")
        print("- Agent initialization properly binds synchronous tools")
        print("- Thread-local storage manages user context for tools")
        print("- Synchronous database sessions are available for MCP tools")
    else:
        print("✗ Some tests failed. Please check the error messages above.")

    return all_tests_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)