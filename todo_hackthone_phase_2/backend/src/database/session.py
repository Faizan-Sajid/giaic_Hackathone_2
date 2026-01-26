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

print("=" * 80)
print("DATABASE INITIALIZATION DEBUG")
print("=" * 80)
print(f"DATABASE_URL from env: {DATABASE_URL}")

# CRITICAL FIX: Use ONLY PostgreSQL, no fallback to SQLite
if not DATABASE_URL or "postgresql" not in DATABASE_URL:
    raise ValueError(
        "XXX CRITICAL: DATABASE_URL must be set to a PostgreSQL connection string!\n"
        f"Found: {DATABASE_URL}\n"
        "Expected format: postgresql+asyncpg://user:pass@host/dbname"
    )

# Clean connection strings for specific drivers
# For Async (asyncpg) - asyncpg uses ssl=require in URL, not sslmode
ASYNC_DB_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://").replace("sslmode=require", "ssl=require")

# For Sync (psycopg2) - sync engine uses psycopg2 which expects sslmode=require
SYNC_DB_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
if "ssl=" in SYNC_DB_URL and "sslmode=" not in SYNC_DB_URL:
    # Convert ssl= to sslmode= for psycopg2
    SYNC_DB_URL = SYNC_DB_URL.replace("ssl=require", "sslmode=require").replace("ssl=true", "sslmode=require")

# Ensure both URLs have proper SSL configuration for Neon
if "ssl=require" not in ASYNC_DB_URL and "sslmode=require" not in ASYNC_DB_URL:
    # Add ssl=require to async URL (for asyncpg)
    if "?" in ASYNC_DB_URL:
        ASYNC_DB_URL = f"{ASYNC_DB_URL}&ssl=require"
    else:
        ASYNC_DB_URL = f"{ASYNC_DB_URL}?ssl=require"

if "sslmode=require" not in SYNC_DB_URL and "ssl=require" not in SYNC_DB_URL:
    # Add sslmode=require to sync URL
    if "?" in SYNC_DB_URL:
        SYNC_DB_URL = f"{SYNC_DB_URL}&sslmode=require"
    else:
        SYNC_DB_URL = f"{SYNC_DB_URL}?sslmode=require"

# Connection pool configuration
# pool_size=10: Maintain 10 connections in pool
# max_overflow=10: Allow 10 additional connections when pool exhausted
# pool_pre_ping=True: Verify connections before using
# pool_recycle=3600: Recycle connections after 1 hour (prevent connection rot)

# Create PostgreSQL async engine (for async operations) - NO FALLBACK!
# asyncpg handles SSL via URL parameters, not connect_args
async_engine = create_async_engine(
    ASYNC_DB_URL,
    echo=True,  # Keep this to see SQL queries
    pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
    pool_pre_ping=True,
    pool_recycle=3600,
)

print(f"XXX Async Engine Created: {async_engine.url}")
print(f"   Engine Type: PostgreSQL (asyncpg)")
print(f"   This will be used for: Chatbot tools, Async operations")

# Create PostgreSQL sync engine (for sync operations like MCP tools) - NO FALLBACK!
# psycopg2 handles SSL via sslmode parameter
sync_engine = create_engine(
    SYNC_DB_URL,
    echo=True,
    pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
    pool_pre_ping=True,
    pool_recycle=3600,
)

print(f"XXX Sync Engine Created: {sync_engine.url}")
print(f"   Engine Type: PostgreSQL (psycopg2/other)")
print(f"   This will be used for: MCP tools, Sync operations")
print("=" * 80)

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

    CRITICAL: This function is used by async operations!
    It MUST return a session connected to PostgreSQL (Neon)!
    """
    async with async_session() as session:
        # Debug: Log which database we're connected to
        db_name = async_engine.url.database
        db_host = async_engine.url.host
        print(f"[CONNECTION] Async Session created: Connected to {db_host}/{db_name} (PostgreSQL)")

        yield session
        print(f"[CONNECTION] Async Session closed: {db_host}/{db_name}")


def get_session_sync() -> Generator[Session, None, None]:
    """
    Synchronous database session generator for synchronous operations
    Like MCP tools that need to run synchronously for OpenAI Agents SDK

    CRITICAL: This function is used by MCP tool handlers!
    It MUST return a session connected to PostgreSQL (Neon)!

    Yields:
        SQLModel Session for synchronous database operations
    """
    # Debug: Log which database we're connected to
    db_name = sync_engine.url.database
    db_host = sync_engine.url.host
    print(f"[CONNECTION] Sync Session created: Connected to {db_host}/{db_name} (PostgreSQL)")

    session = Session(sync_engine)
    try:
        yield session
    finally:
        session.close()
        print(f"[CONNECTION] Sync Session closed: {db_host}/{db_name}")


async def init_db():
    """
    Initialize database tables

    Task: TASK-003
    Spec: DINT-001-DINT-007 (data integrity constraints)
    Creates all SQLModel tables on startup
    """
    print("\n" + "=" * 80)
    print("CREATING DATABASE TABLES")
    print("=" * 80)

    # Import all models to register them
    from .models import Conversation, Message
    from ..models.user import User
    from ..models.task import Task

    print("Imported models:", [Conversation.__tablename__, Message.__tablename__,
                               User.__tablename__, Task.__tablename__])

    # Create tables using async engine (PostgreSQL)
    print(f"Creating tables in: {async_engine.url}")
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Also create tables in sync engine (should be the same PostgreSQL)
    print(f"Ensuring tables in sync engine: {sync_engine.url}")
    SQLModel.metadata.create_all(sync_engine)

    print("XXX All tables created in PostgreSQL (Neon)")
    print("=" * 80 + "\n")