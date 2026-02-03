# Database Migration Skill

**Purpose**: Create and run Alembic database migrations for schema changes
**Coverage**: Phase 2 (T010-T011) - Alembic initialization and initial schema
**Project**: Phase II Full-Stack Web Application

---

## Skill Description

This skill handles all database migration tasks using Alembic with SQLModel. It creates database schema versions, manages schema evolution, and ensures data integrity including:

- Alembic configuration and initialization
- Initial schema migration (users and tasks tables)
- Database constraints and indexes
- Foreign key relationships with CASCADE DELETE
- Migration rollback support
- Schema evolution for future changes

---

## Usage

### Basic Usage
```
/database
```

### With Specific Task
```
/database T010
```

### Create New Migration
```
/database create migration_name
```

### Run Migrations
```
/database upgrade
```

### Rollback Migration
```
/database downgrade
```

---

## Implementation Guidelines

### Technology Stack

- **Migration Tool**: Alembic
- **ORM**: SQLModel 0.0.22+
- **Database**: PostgreSQL 16+ (Neon)
- **Driver**: asyncpg (async PostgreSQL driver)

### Migration Best Practices

- Always generate migration with `--autogenerate` flag
- Review generated migration before applying
- Test migrations on development database first
- Migrations MUST be reversible (include downgrade)
- Use descriptive migration names
- Add migration comments explaining changes
- Include foreign key constraints with CASCADE behavior
- Create indexes for frequently queried columns

### Schema Requirements

**Users Table**:
- id: TEXT PRIMARY KEY (UUID)
- email: TEXT UNIQUE NOT NULL (max 255 chars)
- password_hash: TEXT NOT NULL
- created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()

**Tasks Table**:
- id: SERIAL PRIMARY KEY (auto-increment)
- owner_user_id: TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE
- title: TEXT NOT NULL CHECK (length(title) >= 1 AND length(title) <= 200)
- description: TEXT CHECK (length(description) <= 1000)
- completed: BOOLEAN DEFAULT FALSE
- created_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()
- updated_at: TIMESTAMP WITH TIME ZONE DEFAULT NOW()

**Indexes**:
- idx_users_email ON users(email)
- idx_tasks_owner_user_id ON tasks(owner_user_id)
- idx_tasks_completed ON tasks(completed)

---

## Supported Tasks

### T010: Alembic Initialization

**File**: `backend/alembic.ini`
- Configure Alembic for SQLModel
- Set database connection string
- Configure migration versions directory
- Enable version control

**Directory**: `backend/alembic/versions/`
- Create versions directory structure
- Store migration files here

**Configuration** (alembic.ini):
```ini
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os
version_locations = %(here)s/bar
output_encoding = utf-8
sqlalchemy.url = driver://user:pass@localhost/dbname
```

### T011: Initial Schema Migration

**File**: `backend/alembic/versions/001_initial_schema.py`
- Create users table with constraints
- Create tasks table with foreign key
- Add CASCADE DELETE on owner_user_id foreign key
- Create all indexes
- Include downgrade function (reversible migration)

**Migration Up** (creates schema):
```python
def upgrade():
    # Create users table
    op.create_table('users',
        sa.Column('id', sa.TEXT(), primary_key=True),
        sa.Column('email', sa.String(255), unique=True, nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'))
    )

    # Create tasks table
    op.create_table('tasks',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('owner_user_id', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['owner_user_id'], ['users.id'], ondelete='CASCADE'),
        sa.Column('title', sa.String(), nullable=False),
        sa.CheckConstraint('length(title) >= 1 AND length(title) <= 200'),
        sa.Column('description', sa.String()),
        sa.CheckConstraint('length(description) <= 1000'),
        sa.Column('completed', sa.Boolean(), server_default='false'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'))
    )

    # Create indexes
    op.create_index('idx_users_email', 'users', ['email'])
    op.create_index('idx_tasks_owner_user_id', 'tasks', ['owner_user_id'])
    op.create_index('idx_tasks_completed', 'tasks', ['completed'])
```

**Migration Down** (reverts schema):
```python
def downgrade():
    # Drop indexes
    op.drop_index('idx_users_email', table_name='users')
    op.drop_index('idx_tasks_owner_user_id', table_name='tasks')
    op.drop_index('idx_tasks_completed', table_name='tasks')

    # Drop tables (tasks first due to foreign key)
    op.drop_table('tasks')
    op.drop_table('users')
```

---

## Migration Commands

### Initialize Alembic
```bash
# From backend directory
alembic init alembic
```

### Generate New Migration
```bash
# Generate migration from model changes
alembic revision --autogenerate -m "Description of changes"

# Example:
alembic revision --autogenerate -m "Add priority field to tasks"
```

### Apply Migrations (Upgrade)
```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade +001

# Show SQL without executing (dry run)
alembic upgrade head --sql
```

### Rollback Migration (Downgrade)
```bash
# Rollback one migration
alembic downgrade -1

# Rollback to base (no migrations)
alembic downgrade base

# Show SQL without executing (dry run)
alembic downgrade -1 --sql
```

### View Migration History
```bash
# Show current migration version
alembic current

# Show migration history
alembic history
```

---

## Migration Examples

### Example 1: Create Priority Field
```bash
# Generate migration
alembic revision --autogenerate -m "Add priority field to tasks"
```

**Migration Up**:
```python
def upgrade():
    op.add_column('tasks', sa.Column('priority', sa.String(), server_default='medium'))
    op.execute("ALTER TABLE tasks ADD CONSTRAINT chk_priority CHECK (priority IN ('high', 'medium', 'low'))")
```

### Example 2: Add Tags Array
```bash
# Generate migration
alembic revision --autogenerate -m "Add tags array to tasks"
```

**Migration Up**:
```python
def upgrade():
    op.add_column('tasks', sa.Column('tags', sa.ARRAY(sa.String()), server_default='{}'))
    op.create_index('idx_tasks_tags', 'tasks', ['tags'], postgresql_using='gin')
```

### Example 3: Rename Column
```bash
# Generate migration
alembic revision --autogenerate -m "Rename task_name to title"
```

**Migration Up**:
```python
def upgrade():
    op.alter_column('tasks', 'task_name', new_column_name='title')
```

**Migration Down**:
```python
def downgrade():
    op.alter_column('tasks', 'title', new_column_name='task_name')
```

---

## Migration Workflow

### Development Workflow

1. **Modify SQLModel** in `backend/src/models/`
   - Add/remove columns, tables, constraints

2. **Generate Migration**:
   ```bash
   alembic revision --autogenerate -m "Description"
   ```

3. **Review Generated Migration**:
   - Check upgrade() function
   - Verify downgrade() exists and is correct
   - Ensure foreign keys and constraints are correct

4. **Test Migration**:
   ```bash
   # Test on development database
   alembic upgrade head --sql

   # Actually apply
   alembic upgrade head
   ```

5. **Verify Schema**:
   ```bash
   # Connect to database and check
   \d users
   \d tasks
   ```

### Production Workflow

1. **Backup Database** before migration
2. **Test Migration** on staging database
3. **Review Migration** with team
4. **Apply Migration** to production:
   ```bash
   alembic upgrade head
   ```
5. **Verify Application** works correctly
6. **Monitor for Issues** after deployment

---

## Migration Validation

### Before Applying Migration

- [ ] Backup database (production)
- [ ] Review generated migration code
- [ ] Verify upgrade() and downgrade() both correct
- [ ] Test migration on development database
- [ ] Check for data loss in downgrade

### After Applying Migration

- [ ] Verify tables exist
- [ ] Verify foreign keys and constraints
- [ ] Verify indexes created
- [ ] Verify application connects to database
- [ ] Test all affected API endpoints
- [ ] Check application logs for errors

### Schema Validation Checklist

**Users Table**:
- [ ] id: TEXT PRIMARY KEY (UUID)
- [ ] email: TEXT UNIQUE NOT NULL
- [ ] password_hash: TEXT NOT NULL
- [ ] created_at: TIMESTAMP WITH TIME ZONE
- [ ] Index: idx_users_email on email column

**Tasks Table**:
- [ ] id: INTEGER PRIMARY KEY (auto-increment)
- [ ] owner_user_id: TEXT NOT NULL
- [ ] Foreign Key: REFERENCES users(id) ON DELETE CASCADE
- [ ] title: TEXT NOT NULL
- [ ] Check: length(title) >= 1 AND <= 200
- [ ] description: TEXT
- [ ] Check: length(description) <= 1000
- [ ] completed: BOOLEAN DEFAULT FALSE
- [ ] created_at: TIMESTAMP WITH TIME ZONE
- [ ] updated_at: TIMESTAMP WITH TIME ZONE
- [ ] Index: idx_tasks_owner_user_id on owner_user_id
- [ ] Index: idx_tasks_completed on completed

---

## Migration Best Practices

### DO's

✅ DO use descriptive migration names
✅ DO review generated migrations before applying
✅ DO test migrations on development database first
✅ DO include downgrade functions (make migrations reversible)
✅ DO backup database before production migrations
✅ DO add comments explaining schema changes
✅ DO use CHECK constraints for data validation
✅ DO create indexes for frequently queried columns
✅ DO use CASCADE DELETE for foreign keys

### DON'Ts

❌ DON'T manually write migrations (use --autogenerate)
❌ DON'T apply migrations without testing
❌ DON'T skip reviewing generated migration code
❌ DON'T forget downgrade functions
❌ DON'T use raw SQL in migrations (use op.* functions)
❌ DON'T delete migration files
❌ DON'T edit applied migration history files
❌ DON'T apply migrations to production without backup

---

## Troubleshooting

### Issue: Alembic Not Detecting Changes

**Problem**: Running `alembic revision --autogenerate` generates empty migration

**Solutions**:
- Ensure SQLModel models are imported before running command
- Check that models have `table=True` attribute
- Verify database URL in alembic.ini is correct
- Run `alembic current` to see current version

### Issue: Migration Fails with Foreign Key Error

**Problem**: `sqlalchemy.exc.IntegrityError: foreign key constraint fails`

**Solutions**:
- Check that referenced table exists before adding foreign key
- Verify foreign key column types match referenced primary key types
- Ensure CASCADE DELETE is correctly specified

### Issue: Downgrade Not Working

**Problem**: Downgrade function fails or doesn't properly revert

**Solutions**:
- Ensure downgrade() reverses all upgrade() changes
- Check that tables are dropped in correct order (child before parent)
- Verify constraints are dropped before tables
- Test downgrade on development database

### Issue: Index Already Exists

**Problem**: `sqlalchemy.exc.OperationalError: index already exists`

**Solutions**:
- Check `if not exists` in migration before creating index
- Run `alembic downgrade -1` and `alembic upgrade head` to reset
- Manually drop index from database and re-run migration

---

## Notes

- Migration files should NEVER be manually edited after generation
- Always use `--autogenerate` to generate migrations from model changes
- Test all migrations on development database before production
- Backup database before applying migrations in production
- Review migration code with team before production deployment
- Document all schema changes in migration comments
- Keep migration history clean (don't delete or edit old migrations)
- Monitor database performance after schema changes
