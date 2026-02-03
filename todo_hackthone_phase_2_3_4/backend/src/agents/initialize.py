# Handle import errors gracefully
AGENTS_AVAILABLE = False
try:
    from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Agent, Runner, function_tool
    AGENTS_AVAILABLE = True
    print("DEBUG: Successfully imported from 'agents' package")
except ImportError as e:
    print(f"Warning: Could not import from 'agents' package: {e}")
    print("Falling back to mock agent functionality for testing...")
    # Define mock objects for testing
    AsyncOpenAI = None
    OpenAIChatCompletionsModel = None
    Agent = None
    Runner = None
    function_tool = lambda f: f  # Decorator that does nothing
except Exception as e:
    print(f"Warning: Error importing from 'agents' package: {e}")
    print("Falling back to mock agent functionality for testing...")
    # Define mock objects for testing
    AsyncOpenAI = None
    OpenAIChatCompletionsModel = None
    Agent = None
    Runner = None
    function_tool = lambda f: f  # Decorator that does nothing

from ..mcp.tools.todo import (
    add_task,  # Pre-decorated function
    list_tasks,  # Pre-decorated function
    complete_task,  # Pre-decorated function
    update_task,  # Pre-decorated function
    delete_task,  # Pre-decorated function
    set_current_user_id,
    clear_current_user_id,
    get_current_user_id
)
from .prompts import get_agent_instructions
from dotenv import load_dotenv
import os
from agents import ModelSettings

load_dotenv()


def initialize_gemini_agent():
    """
    Initialize the Gemini agent with all required prompts and tool bindings
    """
    if not AGENTS_AVAILABLE:
        print("DEBUG: Agents package not available, returning None")
        return None

    # Client Setup - EXACT pattern as requested
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    # Safety Check: If gemini_api_key is missing, return None and print a debug message
    if not gemini_api_key:
        print("DEBUG: GEMINI_API_KEY is not set in environment variables")
        return None

    # Create the client as shown in the reference
    openai_client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    # Get agent instructions first
    instructions = get_agent_instructions()

    # Tool Integration: Use the pre-decorated tools from todo.py
    # These tools already have the @function_tool decorator and handle user_id context internally

    # Create the agent with pre-decorated tools from todo.py - use the exact format from reference
    gemini_agent = Agent(
        name="TaskFlow Assistant",
        instructions=instructions["system"],
        model=OpenAIChatCompletionsModel(
            model='gemini-2.5-flash',  # Fixed: was gemini-2.5-flash
            openai_client=openai_client
        ),
        tools=[add_task, list_tasks, complete_task, update_task, delete_task],
        
        model_settings=ModelSettings(tool_choice="required")  # Enable automatic tool use as required by the flow
    )

    # The user context is now managed through the global functions in todo.py
    # No need to attach these methods to the agent object

    return gemini_agent


def get_configured_agent():
    """
    Get a pre-configured Gemini agent instance with all tools and prompts
    """
    return initialize_gemini_agent()