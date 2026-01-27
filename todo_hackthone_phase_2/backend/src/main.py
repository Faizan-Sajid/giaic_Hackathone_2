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

from .database.session import get_session, init_db, engine
from .core.config import setup_cors
from .core.exceptions import register_error_handlers
from .core.logging import get_correlation_id, log_request
from .core.security import verify_jwt, create_jwt, hash_password, verify_password

# Import models to ensure they're registered
from .models import user, task
from .database.models import Conversation, Message
# Import SQLModel to ensure registry is configured
from sqlmodel import SQLModel

# Import routers
from .api.routes import auth as auth, tasks as tasks, health as health
from .api.chat import router as chat
from .api.debug import router as debug


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
# Explicitly configure for frontend - use environment variable for production URL
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
allowed_origins = [frontend_url]

# Always allow localhost for development
if frontend_url != "http://localhost:3000":
    allowed_origins.append("http://localhost:3000")
    allowed_origins.append("http://127.0.0.1:3000")
else:
    allowed_origins.append("http://127.0.0.1:3000")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Use environment variable for production
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
app.include_router(chat, prefix="/api", tags=["Chat"])
app.include_router(debug, prefix="/api", tags=["Debug"])
app.include_router(health.router, tags=["Health Check"])


# Debug endpoint to check database tables
@app.get("/debug/tables")
async def debug_tables():
    """
    Debug endpoint to check database tables
    """
    from sqlmodel import SQLModel
    from .database.session import async_engine

    async with async_engine.begin() as conn:
        # Check what tables exist
        result = await conn.run_sync(
            lambda sync_conn: sync_conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        )

    tables = [row[0] for row in result]

    return {
        "tables_in_database": tables,
        "tables_in_metadata": list(SQLModel.metadata.tables.keys()),
        "expected_tables": ["task", "user", "conversation", "message"]  # Your expected tables
    }


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
