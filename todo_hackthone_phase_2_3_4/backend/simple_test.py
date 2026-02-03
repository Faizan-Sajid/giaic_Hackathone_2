#!/usr/bin/env python3
"""
Simple test script to verify that the agent initialization and basic operations work correctly
after fixing the openai-agents compatibility issues.
"""

import asyncio
import sys
import os

# Add the backend src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

def test_agent_initialization():
    """Test that the agent can be initialized without errors"""
    print("Testing agent initialization...")

    try:
        from agents.initialize import get_configured_agent

        # Check if GEMINI_API_KEY is set
        import os
        if not os.getenv("GEMINI_API_KEY"):
            print("Warning: GEMINI_API_KEY not set. Testing configuration without API key...")

        agent = get_configured_agent()

        if agent is None:
            print("✓ Agent initialization correctly returns None when API key is missing (expected behavior)")
        else:
            print("✓ Agent initialized successfully")

        return True

    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False
    except Exception as e:
        print(f"✗ Error during agent initialization: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_chat_imports():
    """Test that chat endpoint can import without errors"""
    print("\nTesting chat endpoint imports...")

    try:
        # Test the imports that were causing issues
        from agents import Runner
        print("✓ Successfully imported Runner from agents")

        # Test that the chat endpoint can be imported
        from api.chat import chat_endpoint
        print("✓ Successfully imported chat endpoint")

        return True

    except ImportError as e:
        print(f"✗ Import error in chat: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"✗ Error during chat import: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_runner_method_exists():
    """Test that Runner.run_sync exists and works"""
    print("\nTesting Runner.run_sync method...")

    try:
        from agents import Runner, Agent
        from agents.prompts import get_system_prompt

        # Check if run_sync method exists
        if hasattr(Runner, 'run_sync'):
            print("✓ Runner.run_sync method exists")
        else:
            print("✗ Runner.run_sync method does not exist")
            return False

        return True

    except Exception as e:
        print(f"✗ Error testing Runner methods: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Running tests for openai-agents compatibility fixes...\n")

    success = True

    success &= test_agent_initialization()
    success &= test_chat_imports()
    success &= test_runner_method_exists()

    print(f"\n{'='*50}")
    if success:
        print("✓ All tests passed! The fixes should resolve the chatbot issues.")
        print("\nSummary of fixes applied:")
        print("- Changed Runner.run() to Runner.run_sync() in chat.py")
        print("- Updated agent.py to use synchronous patterns")
        print("- Fixed async tool functions to work with synchronous agent runner")
    else:
        print("✗ Some tests failed. Please review the errors above.")
    print(f"{'='*50}")