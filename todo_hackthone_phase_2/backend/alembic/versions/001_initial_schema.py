# Task: T011
# Spec: Data Model - Initial Schema (data-model.md lines 147-160)
# Spec: Migrations - Migration Strategy (data-model.md lines 348-385)
# Implementation: Generate initial Alembic migration with users and tasks tables

"""Initial schema migration

Creates users and tasks tables with all constraints and indexes.
Enforces data integrity with foreign keys, uniqueness constraints,
and cascade delete behavior.

Task: T011
Spec: DINT-001-DINT-007 (data integrity constraints)
DINT-002 (foreign key with cascade delete)
"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """
    Create users and tasks tables with all constraints and indexes

    Task: T011
    Spec: DINT-001-DINT-007 (data integrity)
    """
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.TEXT(), primary_key=True, comment='User UUID primary key'),
        sa.Column('email', sa.String(255), nullable=False, unique=True, index=True,
                  comment='User email address (unique, indexed)'),
        sa.Column('password_hash', sa.String(), nullable=False,
                  comment='Bcrypt hashed password (never plain text)'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'),
                  comment='Account creation timestamp'),
    )

    # Create tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True,
                  comment='Task integer primary key (auto-increment)'),
        sa.Column('owner_user_id', sa.String(), nullable=False,
                  comment='Task owner UUID (foreign key to users)'),
        sa.Column('title', sa.String(), nullable=False,
                  comment='Task title (required, 1-200 chars)'),
        sa.Column('description', sa.String(), nullable=True,
                  comment='Task description (optional, max 1000 chars)'),
        sa.Column('completed', sa.Boolean(), server_default='false', nullable=False,
                  comment='Task completion status (indexed)'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'),
                  comment='Task creation timestamp (auto-generated)'),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'),
                  comment='Task last update timestamp (auto-updated)'),
    )

    # Create foreign key constraint with CASCADE DELETE
    op.create_foreign_key(
        constraint_name='fk_tasks_owner_user_id_users',
        source_table='tasks',
        referent_table='users',
        local_cols=['owner_user_id'],
        referent_cols=['id'],
        ondelete='CASCADE',  # Cascade delete: Deleting user deletes all their tasks
    )

    # Create check constraints
    op.execute("ALTER TABLE tasks ADD CONSTRAINT chk_title_length "
                "CHECK (length(title) >= 1 AND length(title) <= 200)")
    op.execute("ALTER TABLE tasks ADD CONSTRAINT chk_description_length "
                "CHECK (length(description) <= 1000)")

    # Create indexes
    # Note: idx_users_email and idx_tasks_owner_user_id already created with table
    op.create_index('idx_tasks_completed', 'tasks', ['completed'],
                  comment='Index for filtering by completion status')

    # Insert initial data (optional - for development)
    # No initial data needed for this phase


def downgrade():
    """
    Revert schema - drop all tables and indexes

    Task: T011
    Spec: DINT-001-DINT-007 (data integrity)
    """
    # Drop indexes
    op.drop_index('idx_tasks_completed', table_name='tasks')

    # Drop check constraints
    op.drop_constraint('chk_description_length', 'tasks', type_='check')
    op.drop_constraint('chk_title_length', 'tasks', type_='check')

    # Drop foreign key
    op.drop_constraint('fk_tasks_owner_user_id_users', 'tasks', type_='foreignkey')

    # Drop tables (tasks first due to foreign key)
    op.drop_table('tasks')
    op.drop_table('users')
