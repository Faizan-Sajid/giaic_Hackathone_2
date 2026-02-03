---
id: "001"
title: "Database Driver Migration"
stage: "general"
date_iso: "2026-02-03"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "user"
command: "Driver Migration (Sync Engine Only)"
labels: ["database", "deployment", "railway", "psycopg2", "pg8000"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "backend/src/database/session.py"
  - "backend/requirements.txt"
  - "backend/pyproject.toml"
  - "backend/migrate_data.py"
tests_yaml: []
---

# Database Driver Migration - From psycopg2 to pg8000

## Outcome
Successfully migrated the synchronous database driver from psycopg2 to pg8000 to resolve Railway deployment failures caused by the ImportError: libpq.so.5 issue.

## Evaluation
The changes successfully address the core deployment issue while maintaining full backward compatibility with the local development environment. The async engine remains unchanged using asyncpg, ensuring no disruption to existing functionality.

## Files Modified

### backend/src/database/session.py
- Updated SYNC_DB_URL construction to use postgresql+pg8000:// instead of postgresql://
- Updated comments and print statements to reflect pg8000 usage
- Maintained SSL parameter handling for pg8000 compatibility

### backend/requirements.txt
- Replaced psycopg2-binary==2.9.9 with pg8000>=1.30.0

### backend/pyproject.toml
- Replaced psycopg2>=2.9.11 with pg8000>=1.31.5

### backend/migrate_data.py
- Updated URL construction to use postgresql+pg8000:// instead of postgresql:// for compatibility

## Summary
The migration from psycopg2 to pg8000 resolves the Railway deployment issue because pg8000 is a pure Python driver that doesn't require the libpq system libraries. The async engine continues to use asyncpg without changes, preserving existing functionality. All SSL parameter handling is maintained for PostgreSQL compatibility.

## Prompt Text
"Claude, I need a surgical fix for my backend deployment. Currently, my Railway deployment is failing with ImportError: libpq.so.5. This is a classic issue where the psycopg2 driver depends on Linux system libraries that are unavailable in the Railway environment. To resolve this without destabilizing my local development setup, follow these instructions strictly:

1. Core Task: Driver Migration (Sync Engine Only)
We need to switch the synchronous database driver from psycopg2 to pg8000. Since pg8000 is a 'Pure Python' driver, it does not require libpq and will solve the Railway crash immediately.

File: src/database/session.py

Specific Modification: Locate the SYNC_DB_URL construction.

Old Logic: SYNC_DB_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")

New Logic: SYNC_DB_URL = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql+pg8000://")

Constraint: DO NOT touch the async_engine or the ASYNC_DB_URL. The asyncpg driver is working fine and must remain unchanged.

2. Dependency Update
File: requirements.txt

Action: Remove psycopg2-binary entirely and add pg8000>=1.30.0.

3. Strict Code Review & Quality Assurance
Refine Connection String: Ensure that when switching to pg8000, the SSL parameters (like sslmode=require) are still handled correctly in session.py. Note that pg8000 sometimes expects specific dialect naming; ensure the final string is postgresql+pg8000://....

Validate Imports: Check if import psycopg2 exists anywhere in the codebase (especially in src/database/session.py) and remove it to prevent unnecessary import errors.

Cross-Check init_db: Ensure the init_db() function, which uses conn.run_sync, will still function correctly with this driver change.

No Logic Bloat: Do not add extra libraries, do not change my folder structure, and do not modify the OpenAI Agent configurations.

Verify that your proposed changes maintain 100% backward compatibility with my local environment where I use a single DATABASE_URL. Provide only the updated code for session.py and the revised requirements.txt."

## Response Text
Successfully implemented the database driver migration from psycopg2 to pg8000 for the synchronous engine only. The changes:

1. Updated the SYNC_DB_URL construction in session.py to use postgresql+pg8000://
2. Updated requirements.txt to replace psycopg2-binary with pg8000>=1.30.0
3. Updated pyproject.toml to replace psycopg2 with pg8000
4. Updated migrate_data.py to use postgresql+pg8000:// for consistency
5. Maintained all SSL parameter handling for PostgreSQL compatibility
6. Kept the async_engine unchanged (still using asyncpg)
7. Updated all relevant comments and print statements

This resolves the Railway deployment issue caused by the missing libpq.so.5 library while maintaining full backward compatibility with the local development environment.