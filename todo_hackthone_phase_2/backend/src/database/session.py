# Task: TASK-003
# Spec: Implementation Plan - DB Migration
# Implementation: Database session management with connection pooling

import os
from typing import AsyncGenerator, Generator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Connection pool configuration
# pool_size=10: Maintain 10 connections in pool
# max_overflow=10: Allow 10 additional connections when pool exhausted
# pool_pre_ping=True: Verify connections before using
# pool_recycle=3600: Recycle connections after 1 hour (prevent connection rot)

# Async engine for FastAPI - with fallback for SSL/connection issues
import re

# Process the DATABASE_URL for async compatibility
async_database_url = DATABASE_URL
if DATABASE_URL.startswith("postgresql://"):
    # Handle SSL parameter issues in PostgreSQL URLs
    # Remove problematic ssl parameters or convert them
    if "?ssl=require" in DATABASE_URL or "&ssl=require" in DATABASE_URL:
        # Replace with proper asyncpg SSL handling
        async_database_url = DATABASE_URL.replace("?ssl=require", "?sslmode=require").replace("&ssl=require", "&sslmode=require")
    elif "?ssl=true" in DATABASE_URL or "&ssl=true" in DATABASE_URL:
        async_database_url = DATABASE_URL.replace("?ssl=true", "?sslmode=require").replace("&ssl=true", "&sslmode=require")

try:
    # Determine if we need SQLite-specific connect_args
    if "sqlite" in async_database_url.lower():
        connect_args = {"check_same_thread": False}  # Required for SQLite
    else:
        connect_args = {}  # PostgreSQL doesn't need this

    async_engine = create_async_engine(
        async_database_url,
        echo=True,  # Enable SQL logging for debugging
        pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
        max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args=connect_args
    )

    # Test the async engine immediately to catch SSL or other connection issues early
    # Don't use asyncio.run() from module level when running inside an event loop
    import asyncio
    from sqlalchemy.ext.asyncio import create_async_engine as temp_create_async_engine

    async def test_async_engine():
        # Determine if we need SQLite-specific connect_args
        if "sqlite" in async_database_url.lower():
            connect_args = {"check_same_thread": False}  # Required for SQLite
        else:
            connect_args = {}  # PostgreSQL doesn't need this

        temp_engine = create_async_engine(
            async_database_url,
            echo=True,
            pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args=connect_args
        )
        async with temp_engine.connect() as conn:
            pass  # Just test if we can connect
        await temp_engine.dispose()

    # Check if we're already in an event loop (e.g., when running in Jupyter or FastAPI)
    try:
        loop = asyncio.get_running_loop()
        # We're in an event loop, so we can't use asyncio.run()
        # Instead, we'll test the connection later during initialization
        print("Note: Running inside an event loop, deferring async engine test")
    except RuntimeError:
        # No event loop running, safe to use asyncio.run()
        asyncio.run(test_async_engine())

except Exception as e:
    print(f"Warning: Could not create async engine with URL {async_database_url}: {e}")
    print(f"Falling back to file-based SQLite async engine at: {SQLITE_FILE}")

    # Use the file-based SQLite async engine
    async_engine = create_async_engine(
        SQLITE_ASYNC_URL,
        echo=True,  # Enable SQL logging for debugging
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args={"check_same_thread": False}  # Required for SQLite
    )

# Sync engine for synchronous operations (like MCP tools)
# Handle different database URL schemes appropriately and use available drivers
db_url_for_sync = DATABASE_URL
if DATABASE_URL.startswith("postgresql+asyncpg://"):
    # Convert asyncpg URL to regular postgresql URL, try psycopg2 then pg8000
    db_url_for_sync = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://", 1)
elif DATABASE_URL.startswith("sqlite+aiosqlite://"):
    # Convert aiosqlite URL to regular sqlite URL
    db_url_for_sync = DATABASE_URL.replace("sqlite+aiosqlite://", "sqlite://", 1)

# Import models early to ensure they're registered with SQLModel
from sqlmodel import SQLModel
from . import Conversation, Message  # Import the conversation/message models
from ..models import user, task     # Import the user/task models

import os
from pathlib import Path
from sqlalchemy import text

# Create a data directory for SQLite database
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent  # Go to project root
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

# Use file-based SQLite instead of in-memory
SQLITE_FILE = DATA_DIR / "todo_app.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILE}"
SQLITE_ASYNC_URL = f"sqlite+aiosqlite:///{SQLITE_FILE}"

print(f"DEBUG: Using SQLite database at: {SQLITE_FILE}")

# Try to create sync engine with fallback drivers if needed
try:
    # Determine if we need SQLite-specific connect_args
    if "sqlite" in db_url_for_sync.lower():
        connect_args = {"check_same_thread": False}  # Required for SQLite
    else:
        connect_args = {}  # PostgreSQL doesn't need this

    # First, let's try to create the sync engine with the processed URL
    sync_engine = create_engine(
        db_url_for_sync,
        echo=True,  # Enable SQL logging for debugging
        pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
        max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args=connect_args
    )

    # Test the connection to see if it actually works
    with sync_engine.connect() as conn:
        pass  # Just test if we can connect

    # Create tables for the sync engine
    print("DEBUG: Creating tables for sync engine (primary)")
    SQLModel.metadata.create_all(sync_engine)

except Exception as e:
    # If there's an issue with the primary database driver, try with file-based SQLite for testing
    print(f"Warning: Could not create sync engine with URL {db_url_for_sync}: {e}")
    print(f"Falling back to file-based SQLite at: {SQLITE_FILE}")

    sync_engine = create_engine(
        SQLITE_URL,
        echo=True,  # Enable SQL logging for debugging
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args={"check_same_thread": False}  # Required for SQLite
    )

    # Create the tables in the file-based SQLite database
    # Models are already imported above

    # Ensure the models are registered with SQLModel before creating tables
    SQLModel.metadata.create_all(sync_engine)
    print("DEBUG: Tables created for fallback file-based sync engine")

# Async session factory for FastAPI dependency injection
async_session = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit
)

# Export the async_engine as 'engine' to match what other modules expect
engine = async_engine


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency injection for database sessions

    Task: TASK-003
    Spec: NFR-001 (stateless services)
    Provides async session to FastAPI routes
    Session is automatically closed after request
    """
    async with async_session() as session:
        yield session


def get_session_sync() -> Generator[Session, None, None]:
    """
    Synchronous database session generator for synchronous operations
    Like MCP tools that need to run synchronously for OpenAI Agents SDK

    Yields:
        SQLModel Session for synchronous database operations
    """
    session = Session(sync_engine)
    try:
        yield session
    finally:
        session.close()


async def init_db():
    """
    Initialize database tables

    Task: TASK-003
    Spec: DINT-001-DINT-007 (data integrity constraints)
    Creates all SQLModel tables on startup
    """
    print("DEBUG: Starting database initialization...")

    # Import models to ensure they're registered with SQLModel first
    from . import Conversation, Message
    from ..models import user, task  # Import user and task models too

    print(f"DEBUG: Available models in metadata: {list(SQLModel.metadata.tables.keys())}")

    # Test the async engine connection during initialization
    try:
        from sqlalchemy.ext.asyncio import create_async_engine as temp_create_async_engine
        import os

        # Get the database URL again to test
        DATABASE_URL = os.getenv("DATABASE_URL")
        async_database_url = DATABASE_URL
        if DATABASE_URL.startswith("postgresql://"):
            if "?ssl=require" in DATABASE_URL or "&ssl=require" in DATABASE_URL:
                async_database_url = DATABASE_URL.replace("?ssl=require", "?sslmode=require").replace("&ssl=require", "&sslmode=require")
            elif "?ssl=true" in DATABASE_URL or "&ssl=true" in DATABASE_URL:
                async_database_url = DATABASE_URL.replace("?ssl=true", "?sslmode=require").replace("&ssl=true", "&sslmode=require")

        # Test connection with the async engine
        async with async_engine.connect() as conn:
            # This will raise an exception if there are connection issues
            await conn.commit()  # Simple test transaction
        print("DEBUG: Async engine connection test passed")
    except Exception as e:
        print(f"Warning: Could not connect to async engine with URL {async_database_url}: {e}")
        print(f"Using fallback file-based SQLite async engine at: {SQLITE_FILE}")

        # Update the global variable to use the file-based SQLite engine
        globals()['async_engine'] = create_async_engine(
            SQLITE_ASYNC_URL,
            echo=True,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={"check_same_thread": False}  # Required for SQLite
        )

    # Create tables for the async engine
    print("DEBUG: Creating tables for async engine...")
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Verify tables were created in the database
    async with async_engine.connect() as conn:
        if "sqlite" in str(async_engine.url):
            # For SQLite, check tables
            result = await conn.run_sync(
                lambda sync_conn: sync_conn.execute(
                    text("SELECT name FROM sqlite_master WHERE type='table'")
                ).fetchall()
            )
            table_names = [row[0] for row in result]
            print(f"DEBUG: Tables in async database: {table_names}")

    print(f"DEBUG: Async engine tables created successfully: {list(SQLModel.metadata.tables.keys())}")

    # Also ensure sync engine tables are created if it's different from async engine
    # (This handles the fallback case where sync engine might be different)
    print("DEBUG: Creating tables for sync engine...")
    global sync_engine
    if sync_engine is not None:
        SQLModel.metadata.create_all(sync_engine)

        # Verify tables were created in sync engine too
        if "sqlite" in str(sync_engine.url):
            # For SQLite, check tables
            with sync_engine.connect() as conn:
                result = conn.execute(
                    text("SELECT name FROM sqlite_master WHERE type='table'")
                ).fetchall()
                table_names = [row[0] for row in result]
                print(f"DEBUG: Tables in sync database: {table_names}")

        print(f"DEBUG: Sync engine tables created successfully")
    else:
        print("WARNING: sync_engine is None, unable to create sync tables")

    print("DEBUG: Database initialization complete!")