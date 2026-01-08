# Task: T013
# Spec: Implementation Plan - Phase 2.1 Backend Foundation
# Spec: Security Standards (plan.md lines 51-56)
# Implementation: CORS middleware configuration with frontend origin restriction

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def get_cors_origins() -> list[str]:
    """
    Get allowed CORS origins from environment variable

    Task: T013
    Spec: NFR-004 (enforce CORS policies for specific frontend origin)

    Returns list of allowed origins
    NEVER uses wildcard (*) - security requirement
    """
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
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

    Task: T013
    Spec: NFR-004 (enforce CORS policies for specific frontend origin)

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
