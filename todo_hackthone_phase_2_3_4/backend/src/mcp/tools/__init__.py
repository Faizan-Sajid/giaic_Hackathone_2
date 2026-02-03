# Task: TASK-005, TASK-006, TASK-007, TASK-008, TASK-009
# Spec: Implementation Plan - MCP Tools Implementation
# Implementation: Export add_task, list_tasks, complete_task, update_task, and delete_task tool handlers

from .todo import (
    add_task_tool_handler,
    list_tasks_tool_handler,
    complete_task_tool_handler,
    update_task_tool_handler,
    delete_task_tool_handler,
    add_task_tool_handler_sync,
    list_tasks_tool_handler_sync,
    complete_task_tool_handler_sync,
    update_task_tool_handler_sync,
    delete_task_tool_handler_sync,
    add_task,  # New decorated function
    list_tasks,  # New decorated function
    complete_task,  # New decorated function
    update_task,  # New decorated function
    delete_task,  # New decorated function
    set_current_user_id,
    get_current_user_id,
    clear_current_user_id
)

__all__ = [
    "add_task_tool_handler",
    "list_tasks_tool_handler",
    "complete_task_tool_handler",
    "update_task_tool_handler",
    "delete_task_tool_handler",
    "add_task_tool_handler_sync",
    "list_tasks_tool_handler_sync",
    "complete_task_tool_handler_sync",
    "update_task_tool_handler_sync",
    "delete_task_tool_handler_sync",
    "add_task",  # New decorated function
    "list_tasks",  # New decorated function
    "complete_task",  # New decorated function
    "update_task",  # New decorated function
    "delete_task",  # New decorated function
    "set_current_user_id",
    "get_current_user_id",
    "clear_current_user_id"
]