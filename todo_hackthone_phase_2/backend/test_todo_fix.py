#!/usr/bin/env python3
"""
Test script to verify that the todo.py fix resolves the UI visibility issue
by ensuring both chatbot and dashboard use the same database instance.
"""

import asyncio
from src.mcp.tools.todo import add_task_tool_handler_sync_db_async
from src.core.database import get_session
from src.models.task import Task
from uuid import UUID
import uuid


async def test_database_connection():
    """Test that the database connection is working properly."""
    print("Testing database connection...")

    # Create a test user ID
    test_user_id = str(uuid.uuid4())
    test_task_title = "Test task from chatbot"

    # Add a task using the new async handler (like the chatbot would)
    params = {
        "user_id": test_user_id,
        "title": test_task_title,
        "description": "This is a test task added via the chatbot"
    }

    print(f"Adding task with params: {params}")
    result = add_task_tool_handler_sync_db_async(params)

    print(f"Add task result: {result}")

    # Now try to retrieve the task using the same session that the dashboard uses
    async with get_session() as session:
        from sqlalchemy import select

        # Query for the task we just added
        query = select(Task).where(Task.owner_user_id == test_user_id)
        result_query = await session.execute(query)
        tasks = result_query.scalars().all()

        print(f"Found {len(tasks)} tasks for user {test_user_id}")
        for task in tasks:
            print(f"  - Task ID: {task.id}, Title: {task.title}, Completed: {task.completed}")

        # Verify our test task is there
        matching_tasks = [t for t in tasks if t.title == test_task_title]
        if matching_tasks:
            print(f"✓ SUCCESS: Task added by chatbot is visible to dashboard (found {len(matching_tasks)} matching tasks)")
            return True
        else:
            print("✗ FAILURE: Task added by chatbot is NOT visible to dashboard")
            return False


if __name__ == "__main__":
    success = asyncio.run(test_database_connection())
    if success:
        print("\n🎉 Database fix verification PASSED!")
        print("Chatbot tasks will now be visible in the dashboard UI.")
    else:
        print("\n❌ Database fix verification FAILED!")
        print("Chatbot tasks are still not visible in the dashboard UI.")