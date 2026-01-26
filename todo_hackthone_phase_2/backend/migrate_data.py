import asyncio
import sqlite3
from uuid import UUID
from datetime import datetime
from sqlmodel import create_engine, select, Session
from src.models.task import Task
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Process the DATABASE_URL for sync compatibility
sync_database_url = DATABASE_URL
if DATABASE_URL.startswith("postgresql://"):
    # Handle SSL parameter issues in PostgreSQL URLs
    if "?ssl=require" in DATABASE_URL or "&ssl=require" in DATABASE_URL:
        sync_database_url = DATABASE_URL.replace("?ssl=require", "?sslmode=require").replace("&ssl=require", "&sslmode=require")
    elif "?ssl=true" in DATABASE_URL or "&ssl=true" in DATABASE_URL:
        sync_database_url = DATABASE_URL.replace("?ssl=true", "?sslmode=require").replace("&ssl=true", "&sslmode=require")
    elif "sslmode=require" not in DATABASE_URL:
        if "?" in DATABASE_URL:
            sync_database_url = f"{DATABASE_URL}&sslmode=require"
        else:
            sync_database_url = f"{DATABASE_URL}?sslmode=require"

# Ensure we use the psycopg2 compatible URL (not asyncpg)
sync_database_url = sync_database_url.replace("postgresql+asyncpg://", "postgresql://")

def migrate_sqlite_to_postgres():
    """Migrate tasks from SQLite to PostgreSQL"""

    print("Starting SQLite to PostgreSQL migration...")

    # Create sync engine for PostgreSQL
    sync_engine = create_engine(
        sync_database_url,
        echo=True,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

    # Read from SQLite - check the root directory where the project is located
    sqlite_conn = sqlite3.connect("../data/todo_app.db")  # Relative to backend directory
    cursor = sqlite_conn.execute("SELECT * FROM task")
    sqlite_tasks = cursor.fetchall()

    print(f"Found {len(sqlite_tasks)} tasks in SQLite database")

    if len(sqlite_tasks) == 0:
        print("No tasks to migrate.")
        sqlite_conn.close()
        return

    # Print tasks for verification
    print("Tasks to migrate:")
    for row in sqlite_tasks:
        print(f"  ID: {row[0]}, Owner: {row[1]}, Title: {row[2]}, Completed: {row[4]}")

    # Write to PostgreSQL using sync session
    with Session(sync_engine) as session:
        for row in sqlite_tasks:
            # Check if task already exists (by ID)
            existing = session.exec(
                select(Task).where(Task.id == row[0])
            )
            existing_task = existing.first()

            if existing_task:
                print(f"Task {row[0]} already exists in PostgreSQL, skipping...")
                continue

            # Parse datetime strings
            created_at_str = row[5] if row[5] else datetime.utcnow().isoformat()
            updated_at_str = row[6] if row[6] else datetime.utcnow().isoformat()

            # Handle potential timezone info by taking only the first 19 characters (YYYY-MM-DD HH:MM:SS)
            try:
                created_at = datetime.fromisoformat(created_at_str[:19])
            except ValueError:
                created_at = datetime.utcnow()

            try:
                updated_at = datetime.fromisoformat(updated_at_str[:19])
            except ValueError:
                updated_at = datetime.utcnow()

            # Create new task in PostgreSQL
            task = Task(
                id=row[0],
                owner_user_id=row[1],
                title=row[2],
                description=row[3] if row[3] and row[3].strip() != 'None' else None,
                completed=bool(row[4]),
                created_at=created_at,
                updated_at=updated_at,
            )
            session.add(task)
            print(f"Migrated task {task.id}: {task.title}")

        session.commit()
        print(f"XXX Successfully migrated {len(sqlite_tasks)} tasks to PostgreSQL!")

    sqlite_conn.close()

if __name__ == "__main__":
    migrate_sqlite_to_postgres()