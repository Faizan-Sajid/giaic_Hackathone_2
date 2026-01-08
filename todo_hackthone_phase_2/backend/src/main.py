# Task: T017
# Spec: Implementation Plan - Phase 2.1 Backend Foundation
# Spec: Architecture Overview (plan.md lines 316-361)
# Implementation: FastAPI application entry point with router mounting and middleware stack

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .core.database import get_session, init_db, engine
from .core.config import setup_cors
from .core.exceptions import register_error_handlers
from .core.logging import get_correlation_id, log_request
from .core.security import verify_jwt, create_jwt, hash_password, verify_password

# Import models to ensure they're registered
from .models import user, task
# Import SQLModel to ensure registry is configured
from sqlmodel import SQLModel

# Import routers
from .api.routes import auth as auth, tasks as tasks, health as health


# FastAPI application instance
# Task: T017
# Spec: Architecture Overview (plan.md lines 316-361)
app = FastAPI(
    title="TaskFlow Todo API",
    description="Phase II Full-Stack Web Application with JWT Authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Apply CORS middleware FIRST to ensure credentials are allowed
# Explicitly configure for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # ONLY allow this origin
    allow_credentials=True,  # Required for cookies - set BEFORE other middleware
    allow_methods=["*"],
    allow_headers=["*"],
)


# Middleware stack order (from Architecture Overview)
# Task: T017
# Spec: Architecture Overview (plan.md lines 316-361)
# Order: 1. CORS → 2. Request ID/Correlation ID → 3. Error Handler → 4. JWT (for protected routes)
@asynccontextmanager
async def request_context(request: Request):
    """
    Context manager for request-scoped correlation ID and logging

    Task: T017
    Spec: NFR-002 (structured JSON logging with correlation IDs)
    """
    correlation_id = get_correlation_id(request)

    # Set correlation ID in request state for logging
    request.state.correlation_id = correlation_id

    try:
        yield correlation_id
    finally:
        pass


# Register error handlers (Middleware Layer 3)
# Task: T017
# Spec: Error Handling Strategy (plan.md lines 480-508)
register_error_handlers(app)


@app.on_event("startup")
async def startup_event():
    """
    Initialize database tables on startup

    Task: T017
    Spec: Database Migrations (data-model.md lines 348-385)
    """
    await init_db()
    print("Database initialized successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Close database connections on shutdown

    Task: T017
    """
    await engine.dispose()


# Mount routers (Router Layer)
# Task: T017
# Spec: Architecture Overview (plan.md lines 316-361)
# /api routes
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api", tags=["Tasks"])
app.include_router(health.router, tags=["Health Check"])


# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint providing API information

    Task: T017
    """
    return JSONResponse({
        "name": "TaskFlow Todo API",
        "version": "1.0.0",
        "status": "operational",
        "documentation": "/docs"
    })
