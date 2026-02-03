# Task: TASK-010
# Spec: Implementation Plan - Agent Initialization
# Implementation: Agent initialization with basic configuration without HTTP dependencies

from typing import Optional
from ..core.config import settings


class AgentConfig:
    """
    Configuration class for the Gemini Agent

    Task: TASK-010
    Spec: Initializes agent with basic configuration without HTTP dependencies
    """

    def __init__(self):
        """Initialize agent configuration from settings"""
        self.api_key = settings.gemini_api_key
        self.model = settings.gemini_model
        self.base_url = settings.gemini_base_url
        self.temperature = float(getattr(settings, 'agent_temperature', 0.7))
        self.max_tokens = int(getattr(settings, 'agent_max_tokens', 1000))

        # Note: We don't raise an error here during initialization to allow for testing
        # The API key validation can happen when actually initializing the agent

    def get_config_dict(self) -> dict:
        """
        Get configuration as dictionary

        Returns:
            Dictionary with agent configuration
        """
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

    def get_model_settings(self):
        """
        Get the model settings for the Gemini Agent

        Returns:
            Dictionary with model configuration
        """
        return {
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

    def get_api_key(self) -> Optional[str]:
        """
        Get Gemini API key

        Returns:
            Gemini API key string or None if not set
        """
        return self.api_key

    def is_configured(self) -> bool:
        """
        Check if the agent is properly configured

        Returns:
            True if API key is available, False otherwise
        """
        return self.api_key is not None and len(self.api_key) > 0


# Global agent configuration instance
# Initialize without throwing error to allow import
agent_config = AgentConfig()


def get_agent_config() -> AgentConfig:
    """
    Get the global agent configuration instance

    Task: TASK-010
    Spec: Provides access to agent configuration without HTTP dependencies
    """
    return agent_config