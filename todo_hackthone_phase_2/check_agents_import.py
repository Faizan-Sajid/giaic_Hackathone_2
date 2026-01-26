#!/usr/bin/env python3
"""
Simple test to check the correct import for openai-agents
"""

import sys
import os

# Add the backend src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

try:
    # Try importing from the openai_agents package
    from openai import OpenAI
    print("V Successfully imported OpenAI from openai package")

    # Try importing the specific classes from agents
    from agents import AsyncOpenAI, Agent, Runner, function_tool
    print("V Successfully imported from agents")
    print(f"  - AsyncOpenAI: {AsyncOpenAI}")
    print(f"  - Agent: {Agent}")
    print(f"  - Runner: {Runner}")
    print(f"  - function_tool: {function_tool}")
except ImportError as e:
    print(f"Import error: {e}")
    print("\\nTrying alternative import methods...")

    # Check what's available in the agents module
    try:
        import agents
        print(f"Agents module: {agents}")
        print(f"Agents module file: {agents.__file__ if hasattr(agents, '__file__') else 'N/A'}")

        # List attributes
        attrs = [attr for attr in dir(agents) if not attr.startswith('_')]
        print(f"Available attributes: {attrs}")
    except Exception as e2:
        print(f"Could not inspect agents module: {e2}")

    # Try the openai-agents import
    try:
        from openai_agents import AsyncOpenAI, Agent, Runner, function_tool
        print("V Successfully imported from openai_agents")
    except ImportError as e3:
        print(f"Also failed to import from openai_agents: {e3}")

        # Try importing from the openai library directly
        try:
            from openai import OpenAI as AsyncOpenAI
            from openai.lib.azure import AzureOpenAI
            print("V Successfully imported from openai")
        except ImportError as e4:
            print(f"All import attempts failed: {e4}")