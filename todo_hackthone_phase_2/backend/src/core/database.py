# Task: T007
# Spec: Implementation Plan - Phase 2.1 Backend Foundation
# Implementation: Configure async SQLModel database engine with connection pooling

import os
import time
from typing import Optional
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlmodel import SQLModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Connection pool configuration from plan.md R-004
# pool_size=10: Maintain 10 connections in pool
# max_overflow=10: Allow 10 additional connections when pool exhausted
# pool_pre_ping=True: Verify connections before using
# pool_recycle=3600: Recycle connections after 1 hour (prevent connection rot)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,  # Disable SQL logging in production (security requirement)
    pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "10")),
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Async session factory for FastAPI dependency injection
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit
)


async def get_session() -> AsyncSession:
    """
    FastAPI dependency injection for database sessions

    Task: T007
    Spec: NFR-001 (stateless services)
    Provides async session to FastAPI routes
    Session is automatically closed after request
    """
    async with async_session() as session:
        yield session


async def init_db():
    """
    Initialize database tables

    Task: T007
    Spec: DINT-001-DINT-007 (data integrity constraints)
    Creates all SQLModel tables on startup
    """
    # This will also configure the registry
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
