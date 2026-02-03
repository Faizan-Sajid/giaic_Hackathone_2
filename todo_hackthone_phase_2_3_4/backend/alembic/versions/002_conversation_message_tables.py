# Task: TASK-003
# Spec: Implementation Plan - DB Migration
# Implementation: Generate Alembic migration for conversation and message tables

"""Conversation and message tables migration

Creates conversation and message tables with all constraints and indexes.
Enforces data integrity with foreign keys and proper indexing for performance.

Task: TASK-003
Spec: FR-003 (persist conversation messages to database)
FR-004 (load conversation history from database)
"""

from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '002_conversation_message_tables'
down_revision = '001_initial_schema'
branch_labels = None
depends_on = None


def upgrade():
    """
    Create conversation and message tables with all constraints and indexes

    Task: TASK-003
    Spec: FR-003, FR-004 (data persistence and retrieval)
    """
    # Create conversation table
    op.create_table(
        'conversation',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True,
                  comment='Conversation integer primary key (auto-increment)'),
        sa.Column('user_id', sa.String(), nullable=False,
                  comment='User identifier for conversation ownership (enforces isolation)'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'),
                  comment='Conversation creation timestamp (auto-generated)'),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'),
                  comment='Conversation last update timestamp (auto-updated)'),
    )

    # Create message table
    op.create_table(
        'message',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True,
                  comment='Message integer primary key (auto-increment)'),
        sa.Column('conversation_id', sa.Integer(), nullable=False,
                  comment='Foreign key referencing the conversation this message belongs to'),
        sa.Column('user_id', sa.String(), nullable=False,
                  comment='User identifier for message author (copy for quick filtering)'),
        sa.Column('role', sa.String(), nullable=False,
                  comment='Message role (either user or assistant)'),
        sa.Column('content', sa.String(), nullable=False,
                  comment='Message content text'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('NOW()'),
                  comment='Message creation timestamp (auto-generated)'),
    )

    # Create foreign key constraint for message table
    op.create_foreign_key(
        constraint_name='fk_message_conversation_id_conversation',
        source_table='message',
        referent_table='conversation',
        local_cols=['conversation_id'],
        referent_cols=['id'],
        ondelete='CASCADE',  # Cascade delete: Deleting conversation deletes all its messages
    )

    # Create indexes for performance
    op.create_index('idx_conversation_user_id', 'conversation', ['user_id'],
                  comment='Index for filtering conversations by user')
    op.create_index('idx_message_conversation_id', 'message', ['conversation_id'],
                  comment='Index for filtering messages by conversation')
    op.create_index('idx_message_role', 'message', ['role'],
                  comment='Index for filtering messages by role')


def downgrade():
    """
    Revert schema - drop message and conversation tables and indexes

    Task: TASK-003
    Spec: FR-003, FR-004 (data persistence and retrieval)
    """
    # Drop indexes
    op.drop_index('idx_message_role', table_name='message')
    op.drop_index('idx_message_conversation_id', table_name='message')
    op.drop_index('idx_conversation_user_id', table_name='conversation')

    # Drop foreign key
    op.drop_constraint('fk_message_conversation_id_conversation', 'message', type_='foreignkey')

    # Drop tables (message first due to foreign key)
    op.drop_table('message')
    op.drop_table('conversation')