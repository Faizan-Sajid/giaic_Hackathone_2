# Task: TASK-010, TASK-011
# Spec: Implementation Plan - Agent Initialization and Tool Bindings
# Implementation: Agent initialization with basic configuration and tool bindings without HTTP dependencies

from typing import Optional, Dict, Any, List, Callable
from .config import get_agent_config, AgentConfig
from agents import Agent as SDKAgent, Runner, function_tool
import asyncio


class Agent:
    """
    OpenAI Agent wrapper class using the official OpenAI Agents SDK

    Task: TASK-010, TASK-011
    Spec: Initializes agent with basic configuration and tool bindings without HTTP dependencies
    """

    def __init__(self, config: Optional[AgentConfig] = None, name: str = "TodoAssistant"):
        """
        Initialize the agent with configuration

        Args:
            config: Agent configuration object. If None, uses global config
            name: Name of the agent
        """
        self.config = config or get_agent_config()
        self.initialized = False

        # Set up basic agent properties
        self.model = self.config.model
        self.temperature = self.config.temperature
        self.max_tokens = self.config.max_tokens
        self.api_key = self.config.get_api_key()
        self.name = name

        # Initialize tool bindings
        self._tool_bindings = {}
        self._tools = []  # Store actual tool functions

        # Check if properly configured
        self._is_configured = self.config.is_configured()

        # Initialize is now complete - no HTTP calls made yet
        self.initialized = True

    def is_properly_configured(self) -> bool:
        """
        Check if the agent is properly configured with required credentials

        Returns:
            True if agent has all required configuration, False otherwise
        """
        return self._is_configured

    def is_initialized(self) -> bool:
        """
        Check if the agent is properly initialized

        Returns:
            True if agent is initialized, False otherwise
        """
        return self.initialized

    def get_model_settings(self):
        """
        Get the model settings for the OpenAI Agent SDK

        Note: This will only be available if the agent is properly configured

        Returns:
            ModelSettings object for the OpenAI Agent SDK, or None if not configured
        """
        if self._is_configured:
            return self.config.get_model_settings()
        else:
            return None

    def get_model_config(self) -> Dict[str, Any]:
        """
        Get the model configuration

        Returns:
            Dictionary with model configuration parameters
        """
        return self.config.get_config_dict()

    def get_sdk_agent_class(self):
        """
        Get the underlying OpenAI Agents SDK agent class

        Note: This method will be used in later tasks when we create the actual agent
        with instructions and tools, but for TASK-010 we just prepare the configuration

        Returns:
            The OpenAI Agents SDK Agent class ready for instantiation
        """
        return SDKAgent

    def get_runner_class(self):
        """
        Get the underlying OpenAI Agents SDK runner class

        Note: This method will be used in later tasks when we run the agent
        but for TASK-010 we just prepare the configuration

        Returns:
            The OpenAI Agents SDK Runner class ready for instantiation
        """
        return Runner

    def bind_tool(self, name: str, handler: Callable, description: str = ""):
        """
        Bind an MCP tool to the agent

        Task: TASK-011
        Spec: Registers MCP tools with the agent for natural language processing

        Args:
            name: Name of the tool
            handler: Function that handles the tool execution
            description: Description of what the tool does
        """
        self._tool_bindings[name] = {
            "handler": handler,
            "description": description
        }

    def create_sdk_agent_with_tools(self, instructions: str = None):
        """
        Create the actual OpenAI Agent SDK instance with tools bound

        Task: TASK-011
        Spec: Creates an agent instance with system instructions and bound tools

        Args:
            instructions: System instructions for the agent. If None, uses default

        Returns:
            OpenAI Agent instance with tools attached
        """
        from agents import Agent as SDKAgent
        from .prompts import get_agent_instructions

        # Use provided instructions or get from prompts
        if instructions is None:
            instructions = get_agent_instructions()["system"]

        # Get the bound tools as a list of tool functions
        tool_functions = []
        for tool_name, tool_info in self._tool_bindings.items():
            # Get the actual function from the tool handler
            tool_func = tool_info["handler"]
            tool_functions.append(tool_func)

        # Create the OpenAI Agent with instructions and tools
        sdk_agent = SDKAgent(
            name="TodoAssistant",
            instructions=instructions,
            tools=tool_functions
        )

        return sdk_agent

    def get_tool_bindings(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all registered tool bindings

        Returns:
            Dictionary of tool bindings
        """
        return self._tool_bindings

    def get_tool_handler(self, tool_name: str) -> Optional[Callable]:
        """
        Get the handler for a specific tool

        Args:
            tool_name: Name of the tool to retrieve

        Returns:
            Tool handler function or None if not found
        """
        if tool_name in self._tool_bindings:
            return self._tool_bindings[tool_name]["handler"]
        return None

    async def run_basic_check(self) -> bool:
        """
        Perform a basic check to see if the agent can be used

        Note: This is a placeholder that would normally make an API call
        but for TASK-010 we're not making HTTP calls, so we just check config

        Returns:
            True if agent is properly configured
        """
        return self._is_configured

    async def run_with_input(self, user_input: str) -> Any:
        """
        Run the agent with a user input using the configured tools

        Task: TASK-011
        Spec: Runs the agent with example inputs and verifies tool invocation

        Args:
            user_input: The user's input to process

        Returns:
            Result from the agent execution
        """
        from agents import Runner
        import asyncio
        import concurrent.futures

        # Create the SDK agent with tools
        sdk_agent = self.create_sdk_agent_with_tools()

        def run_agent_sync():
            return Runner.run_sync(sdk_agent, user_input)

        # Run the synchronous agent execution in a thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, run_agent_sync)
        return result


# Global agent instance
_agent_instance: Optional[Agent] = None


def get_agent() -> Optional[Agent]:
    """
    Get the global agent instance if configured

    Task: TASK-010, TASK-011
    Spec: Provides access to agent instance without HTTP dependencies during initialization
    """
    global _agent_instance
    if _agent_instance is None:
        config = get_agent_config()
        _agent_instance = Agent(config)
    return _agent_instance


def create_agent(config: Optional[AgentConfig] = None) -> Agent:
    """
    Create a new agent instance with the given configuration

    Args:
        config: Agent configuration object. If None, uses global config

    Returns:
        New Agent instance
    """
    return Agent(config)


def create_agent_with_todo_tools(config: Optional[AgentConfig] = None) -> Agent:
    """
    Create an agent instance with the initial todo management tools bound

    Task: TASK-011
    Spec: Creates an agent with add_task_tool and list_tasks_tool bound

    Returns:
        New Agent instance with todo tools bound
    """
    from ..mcp.tools.todo import (
        add_task_tool_handler as add_task_tool,
        list_tasks_tool_handler as list_tasks_tool,
        AddTaskInput,
        ListTasksInput
    )
    from agents import function_tool

    # Create the actual tool functions using @function_tool decorator
    # Note: openai-agents expects synchronous functions, so we need to handle async calls properly
    import asyncio
    import concurrent.futures

    def run_async_synchronously(async_func, *args, **kwargs):
        """Helper to run async functions synchronously for openai-agents compatibility"""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No event loop running, create a new one
            return asyncio.run(async_func(*args, **kwargs))
        else:
            # Event loop is already running, create a new one in a new thread
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, async_func(*args, **kwargs))
                return future.result()

    @function_tool
    def add_task(title: str, description: str = "") -> dict:
        """
        Add a new todo task with title and optional description

        Args:
            title: The title of the task
            description: Optional description of the task
        """
        # Simulate calling the actual handler with dummy user_id
        # In a real scenario, user_id would come from context
        params = {"user_id": "test_user", "title": title, "description": description}
        result = run_async_synchronously(add_task_tool, params)
        return result.get("structured_result", {"success": False, "error": "No structured result"})

    @function_tool
    def list_tasks(status: str = None) -> dict:
        """
        List user's todo tasks, optionally filtered by status

        Args:
            status: Optional status filter ("completed", "pending", or None for all)
        """
        # Simulate calling the actual handler with dummy user_id
        params = {"user_id": "test_user", "status": status}
        result = run_async_synchronously(list_tasks_tool, params)
        return result.get("structured_result", {"success": False, "error": "No structured result"})

    # Create the agent
    agent = Agent(config)

    # Bind the tools to the agent
    agent.bind_tool("add_task", add_task, "Add a new todo task with title and optional description")
    agent.bind_tool("list_tasks", list_tasks, "List user's todo tasks, optionally filtered by status")

    return agent