#!/usr/bin/env python3
"""
Test script to verify the database fix is working correctly.
This verifies that both async and sync engines connect to the same PostgreSQL database.
"""

import asyncio
from src.database.session import async_engine, sync_engine, get_session, get_session_sync
from sqlmodel import select
from src.models.task import Task

async def test_db_connection():
    print("=" * 60)
    print("TESTING DATABASE CONNECTION FIX")
    print("=" * 60)

    # Check engine URLs
    print(f"Async Engine URL: {async_engine.url}")
    print(f"Sync Engine URL: {sync_engine.url}")

    # Verify they point to the same database
    async_host = async_engine.url.host
    sync_host = sync_engine.url.host
    async_db = async_engine.url.database
    sync_db = sync_engine.url.database

    print(f"\nAsync Engine Host: {async_host}")
    print(f"Sync Engine Host: {sync_host}")
    print(f"Async Engine DB: {async_db}")
    print(f"Sync Engine DB: {sync_db}")

    if async_host == sync_host and async_db == sync_db:
        print("XXX Both engines connect to the same PostgreSQL database!")
    else:
        print("XXX Engines connect to different databases!")
        return False

    # Check engine types
    async_driver = async_engine.dialect.name
    sync_driver = sync_engine.dialect.name
    print(f"\nAsync Engine Driver: {async_driver}")
    print(f"Sync Engine Driver: {sync_driver}")

    if async_driver == "postgresql" and sync_driver == "postgresql":
        print("XXX Both engines use PostgreSQL!")
    else:
        print("XXX Engines don't both use PostgreSQL!")
        return False

    # Test async session
    print("\nTesting async session...")
    session_gen = get_session()
    session = await session_gen.__anext__()
    try:
        # Count tasks using async session
        result = await session.exec(select(Task))
        tasks = result.all()
        print(f"XXX Async session works! Found {len(tasks)} tasks in database")
    finally:
        await session_gen.aclose()

    # Test sync session
    print("\nTesting sync session...")
    with get_session_sync() as session:
        # Count tasks using sync session
        result = session.exec(select(Task))
        tasks = result.all()
        print(f"XXX Sync session works! Found {len(tasks)} tasks in database")

    print("\n" + "=" * 60)
    print("DATABASE FIX VERIFICATION: SUCCESS XXX")
    print("- Both async and sync engines connect to PostgreSQL")
    print("- Both engines connect to the same database")
    print("- Both sessions can query the database")
    print("- No more SQLite fallback!")
    print("=" * 60)

    return True

if __name__ == "__main__":
    asyncio.run(test_db_connection())