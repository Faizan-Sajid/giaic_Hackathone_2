import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """
    Application settings using Pydantic BaseSettings
    """
    # Database Configuration
    database_url: str = "sqlite:///./todo_app.db"

    # JWT Configuration
    jwt_secret: str = "your-super-secret-jwt-key-here-make-it-long-and-random-32-chars-minimum"
    jwt_algorithm: str = "HS256"

    # Frontend Configuration
    frontend_url: str = "http://localhost:3000"

    # Database Connection Pooling
    db_pool_size: int = 10
    db_max_overflow: int = 10

    # Bcrypt Configuration
    bcrypt_rounds: int = 12

    # Development Settings
    debug: bool = True

    # Gemini Configuration
    gemini_api_key: str = ""
    gemini_base_url: str = "https://generativelanguage.googleapis.com/v1beta/openai/"
    gemini_model: str = "gemini-2.0-flash"

    # Temperature setting for agent
    agent_temperature: float = 0.7

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra environment variables that aren't explicitly defined

    def model_post_init(self, __context):
        """Check if GEMINI_API_KEY is available after initialization"""
        if not self.gemini_api_key:
            print("!!! CRITICAL: GEMINI_API_KEY MISSING !!!")


# Create settings instance
settings = Settings()


def get_cors_origins() -> list[str]:
    """
    Get allowed CORS origins from environment variable

    Returns list of allowed origins
    NEVER uses wildcard (*) - security requirement
    """
    frontend_url = settings.frontend_url
    # For local development, also allow 127.0.0.1:3000
    origins = [frontend_url]

    # Add alternative origin for local development if not already present
    if frontend_url == "http://localhost:3000":
        origins.append("http://127.0.0.1:3000")
    elif frontend_url == "http://127.0.0.1:3000":
        origins.append("http://localhost:3000")

    return origins


def setup_cors(app: FastAPI):
    """
    Configure CORS middleware for FastAPI application

    CORS Settings:
    - Allow specific frontend origin (NO wildcards)
    - Allow credentials (for cookies)
    - Allow common headers
    - Allow all methods for API routes
    """
    origins = get_cors_origins()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # NEVER use ["*"] - security violation
        allow_credentials=True,  # Required for HTTP-only cookies
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers for local development
    )