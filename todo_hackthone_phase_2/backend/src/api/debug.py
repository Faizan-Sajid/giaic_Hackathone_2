from fastapi import APIRouter, HTTPException
from sqlmodel import select
from ..database.session import get_session, async_engine
from ..models.task import Task

router = APIRouter()

@router.get("/api/debug/db-info")
async def debug_database_info():
    """
    Debug endpoint to verify which database is being used
    CRITICAL: Use this to confirm PostgreSQL is active
    """

    # Get engine info
    engine_url = str(async_engine.url)
    engine_dialect = async_engine.dialect.name

    # Test query
    async with get_session() as session:
        # Count tasks
        query = select(Task)
        result = await session.exec(query)
        all_tasks = result.all()

        return {
            "database_type": engine_dialect,
            "database_url": engine_url.replace(async_engine.url.password or "", "****") if hasattr(async_engine.url, 'password') else engine_url,
            "database_host": async_engine.url.host,
            "database_name": async_engine.url.database,
            "total_tasks_in_db": len(all_tasks),
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "owner_user_id": str(task.owner_user_id),
                    "completed": task.completed,
                }
                for task in all_tasks
            ],
            "status": "XXX Connected to correct database" if engine_dialect == "postgresql" else "XXX WRONG DATABASE!",
        }

@router.get("/api/debug/verify-task-creation")
async def verify_task_creation():
    """
    Verify that tasks created via chatbot appear in the main database
    """
    async with get_session() as session:
        # Get last 5 tasks
        query = select(Task).order_by(Task.created_at.desc()).limit(5)
        result = await session.exec(query)
        recent_tasks = result.all()

        return {
            "message": "These are the most recent tasks in the database",
            "database": str(async_engine.url.host),
            "recent_tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "created_at": task.created_at.isoformat(),
                    "source": "Check if this matches chatbot tasks"
                }
                for task in recent_tasks
            ]
        }