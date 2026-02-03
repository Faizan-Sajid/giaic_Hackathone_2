# Task: TASK-005, TASK-006, TASK-007, TASK-008, TASK-009
# Spec: Implementation Plan - MCP Tools Implementation
# Implementation: add_task, list_tasks, complete_task, update_task, and delete_task MCP tools for managing todo tasks

from typing import Dict, Any
from pydantic import BaseModel
from sqlmodel import select
from ...models.task import Task
from ...database.session import get_session_sync
from sqlmodel import Session
from uuid import UUID
import json
import asyncio
import threading

# Import TextContent from the local server module to avoid circular import
from ..server import TextContent

# Import the function_tool decorator from the agents package
try:
    from agents import function_tool
except ImportError:
    # Define a mock decorator for testing when agents package is not available
    def function_tool(func):
        return func

# Thread-local storage for user context
_thread_local = threading.local()


class AddTaskInput(BaseModel):
    """Input schema for add_task MCP tool"""
    user_id: str
    title: str
    description: str = ""


from typing import Optional

class ListTasksInput(BaseModel):
    """Input schema for list_tasks MCP tool"""
    user_id: str
    status: Optional[str] = None  # Optional filter for task status (e.g., "completed", "pending")


class CompleteTaskInput(BaseModel):
    """Input schema for complete_task MCP tool"""
    user_id: str
    task_id: int


class UpdateTaskInput(BaseModel):
    """Input schema for update_task MCP tool"""
    user_id: str
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class DeleteTaskInput(BaseModel):
    """Input schema for delete_task MCP tool"""
    user_id: str
    task_id: int


def run_async_synchronously(func):
    """
    Helper function to run functions synchronously.
    This is maintained for compatibility but now simply returns the result of the function call.
    """
    # The function is already being called directly in the sync wrappers
    # This function is kept for compatibility but should not be used
    # The sync wrapper functions now call the handlers directly
    return func


def add_task_tool_handler_sync(title: str, description: str = "", user_id: str = None) -> Dict[str, Any]:
    """
    Synchronous wrapper for add_task_tool_handler that gets user_id from context
    """
    import traceback

    try:
        # Debug logging
        print(f"DEBUG add_task: title='{title}', user_id={user_id}")

        # Get user_id from context if not provided
        actual_user_id = user_id or getattr(_thread_local, 'user_id', None)
        print(f"DEBUG add_task: context_user_id from thread local={actual_user_id}")

        # Validation: Check if user_id exists
        if not actual_user_id:
            error_msg = "No user context available. User must be logged in."
            print(f"ERROR: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "task_id": None,
                "title": title,
                "message": f"❌ Failed to add task: {error_msg}"  # Clear message for agent
            }

        # Validation: Check if user_id is valid UUID format
        try:
            from uuid import UUID
            UUID(actual_user_id)
            print(f"DEBUG add_task: UUID validation passed for {actual_user_id}")
        except (ValueError, AttributeError) as e:
            error_msg = f"Invalid user session format"
            print(f"ERROR: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "task_id": None,
                "title": title,
                "message": f"❌ Failed to add task: {error_msg}"
            }

        # Prepare params for async function
        params = {
            "user_id": actual_user_id,
            "title": title,
            "description": description
        }

        print(f"DEBUG add_task: Calling async handler with params: {params}")

        # Run the async function synchronously
        result = add_task_tool_handler(params)

        print(f"DEBUG add_task: Async handler returned: {result}")

        # Check if there was an error from the async handler
        if result.get("is_error", False):
            # Extract error message from TextContent object
            content = result.get("content", [])
            if content and hasattr(content[0], 'text'):
                error_text = content[0].text  # ✅ Correct attribute access
            else:
                error_text = "Unknown error occurred"

            print(f"ERROR from async handler: {error_text}")
            return {
                "success": False,
                "error": error_text,
                "task_id": None,
                "title": title,
                "message": f"❌ Failed to add task '{title}': {error_text}"  # Clear for agent
            }

        # Extract structured result
        structured_result = result.get("structured_result", {})

        if structured_result:
            print(f"DEBUG add_task: Success! Structured result: {structured_result}")
            # Add clear success message for agent
            task_id = structured_result.get("task_id")
            title_from_result = structured_result.get("title", title)
            structured_result["message"] = f"✅ Successfully added task '{title_from_result}' with ID: {task_id}"
            return structured_result
        else:
            # No structured result but also no error - something is wrong
            error_msg = "Task creation failed - no result returned"
            print(f"WARNING: {error_msg}. Full result: {result}")
            return {
                "success": False,
                "error": error_msg,
                "task_id": None,
                "title": title,
                "message": f"❌ Failed to add task '{title}': {error_msg}"
            }

    except Exception as e:
        error_msg = f"Exception in add_task: {str(e)}"
        print(f"ERROR: {error_msg}")
        traceback.print_exc()
        return {
            "success": False,
            "error": error_msg,
            "task_id": None,
            "title": title,
            "message": f"❌ Error adding task '{title}': {str(e)}"
        }


# Decorated function for OpenAI Agents SDK
@function_tool
def add_task(title: str, description: str = "") -> Dict[str, Any]:
    """
    Create a new todo task for the current user.

    Use this tool when the user wants to:
    - Add a new task
    - Create a todo item
    - Remember something to do
    - Add something to their list

    Args:
        title (str): REQUIRED. The main task title or what needs to be done.
                    Examples: "Buy groceries", "Call mom", "Finish report"
        description (str): OPTIONAL. Additional details about the task.
                          Examples: "Get milk, eggs, bread", "Wish her happy birthday"

    Returns:
        Dict with 'success' (bool), 'task_id' (int or None), 'title' (str), 'error' (str or None)

    Example Usage:
        User says: "Add a task to buy groceries"
        You call: add_task(title="buy groceries", description="")

        User says: "Remind me to call mom tomorrow about her birthday"
        You call: add_task(title="call mom", description="about her birthday tomorrow")
    """
    return add_task_tool_handler_sync(title=title, description=description, user_id=None)


def list_tasks_tool_handler_sync(status: str = None, user_id: str = None) -> Dict[str, Any]:
    """Synchronous wrapper"""
    import traceback

    try:
        print(f"DEBUG list_tasks: status='{status}', user_id={user_id}")

        # 1. Get user_id from context
        actual_user_id = user_id or getattr(_thread_local, 'user_id', None)
        print(f"DEBUG list_tasks: context_user_id={actual_user_id}")

        # 2. Validate user_id exists
        if not actual_user_id:
            error_msg = "No user context available. User must be logged in."
            print(f"ERROR: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "tasks": [],
                "count": 0,
                "message": f"❌ Failed to list tasks: {error_msg}"  # Clear message for agent
            }

        # 3. Validate UUID format
        try:
            from uuid import UUID
            UUID(actual_user_id)
        except (ValueError, AttributeError):
            error_msg = "Invalid user session format"
            print(f"ERROR: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "tasks": [],
                "count": 0,
                "message": f"❌ Failed to list tasks: {error_msg}"
            }

        # 4. Call async handler
        params = {
            "user_id": actual_user_id,
            "status": status
        }
        result = list_tasks_tool_handler(params)
        print(f"DEBUG list_tasks: result={result}")

        # 5. Check for errors
        if result.get("is_error", False):
            content = result.get("content", [])
            error_text = content[0].text if content and hasattr(content[0], 'text') else "Unknown error"
            return {
                "success": False,
                "error": error_text,
                "tasks": [],
                "count": 0,
                "message": f"❌ Failed to list tasks: {error_text}"  # Clear for agent
            }

        # 6. Return structured result
        structured_result = result.get("structured_result", {})
        if structured_result:
            count = structured_result.get("count", 0)
            status_filter = f" ({status})" if status else ""
            structured_result["message"] = f"✅ Found {count} task{'' if count == 1 else 's'}{status_filter} in your list"
            return structured_result
        else:
            error_msg = "Task listing failed - no result returned"
            print(f"WARNING: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "tasks": [],
                "count": 0,
                "message": f"❌ Failed to list tasks: {error_msg}"
            }

    except Exception as e:
        error_msg = f"Exception in list_tasks: {str(e)}"
        print(f"ERROR: {error_msg}")
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "tasks": [],
            "count": 0,
            "message": f"❌ Error listing tasks: {str(e)}"
        }


# Decorated function for OpenAI Agents SDK
@function_tool
def list_tasks(status: str = None) -> Dict[str, Any]:
    """
    Retrieve and display the user's todo tasks.

    Use this tool when the user wants to:
    - See their tasks
    - View their todo list
    - Check what they need to do
    - List pending or completed items

    Args:
        status (str): OPTIONAL. Filter tasks by completion status.
                     - Use "pending" for incomplete tasks
                     - Use "completed" for finished tasks
                     - Use None or omit to see ALL tasks

    Returns:
        Dict with 'success' (bool), 'tasks' (list), 'count' (int), 'error' (str or None)

    Example Usage:
        User says: "Show me my tasks"
        You call: list_tasks(status=None)

        User says: "What tasks do I still need to do?"
        You call: list_tasks(status="pending")

        User says: "Show me completed tasks"
        You call: list_tasks(status="completed")
    """
    return list_tasks_tool_handler_sync(status=status, user_id=None)


def complete_task_tool_handler_sync(task_id: int, user_id: str = None) -> Dict[str, Any]:
    """Synchronous wrapper"""
    import traceback

    try:
        print(f"DEBUG complete_task: task_id={task_id}, user_id={user_id}")

        # 1. Get user_id from context
        actual_user_id = user_id or getattr(_thread_local, 'user_id', None)
        print(f"DEBUG complete_task: context_user_id={actual_user_id}")

        # 2. Validate user_id exists
        if not actual_user_id:
            error_msg = "No user context available. User must be logged in."
            print(f"ERROR: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "task_id": task_id,
                "title": None,
                "message": f"❌ Failed to complete task: {error_msg}"  # Clear message for agent
            }

        # 3. Validate UUID format
        try:
            from uuid import UUID
            UUID(actual_user_id)
        except (ValueError, AttributeError):
            error_msg = "Invalid user session format"
            print(f"ERROR: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "task_id": task_id,
                "title": None,
                "message": f"❌ Failed to complete task: {error_msg}"
            }

        # 4. Call async handler
        params = {
            "user_id": actual_user_id,
            "task_id": task_id
        }
        result = complete_task_tool_handler(params)
        print(f"DEBUG complete_task: result={result}")

        # 5. Check for errors
        if result.get("is_error", False):
            content = result.get("content", [])
            error_text = content[0].text if content and hasattr(content[0], 'text') else "Unknown error"
            return {
                "success": False,
                "error": error_text,
                "task_id": task_id,
                "title": None,
                "message": f"❌ Failed to complete task: {error_text}"  # Clear for agent
            }

        # 6. Return structured result
        structured_result = result.get("structured_result", {})
        if structured_result:
            title = structured_result.get("title", "Unknown Task")
            structured_result["message"] = f"✅ Successfully marked task '{title}' as completed"
            return structured_result
        else:
            error_msg = "Task completion failed - no result returned"
            print(f"WARNING: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "task_id": task_id,
                "title": None,
                "message": f"❌ Failed to complete task: {error_msg}"
            }

    except Exception as e:
        error_msg = f"Exception in complete_task: {str(e)}"
        print(f"ERROR: {error_msg}")
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "task_id": task_id,
            "title": None,
            "message": f"❌ Error completing task: {str(e)}"
        }


# Decorated function for OpenAI Agents SDK
@function_tool
def complete_task(task_id: int) -> Dict[str, Any]:
    """
    Mark a specific task as completed/done.

    Use this tool when the user wants to:
    - Mark a task as done
    - Complete a task
    - Check off an item
    - Finish a todo

    Args:
        task_id (int): REQUIRED. The ID number of the task to mark as complete.
                      You can get this from list_tasks() results.

    Returns:
        Dict with 'success' (bool), 'task_id' (int), 'title' (str), 'error' (str or None)

    Example Usage:
        User says: "Mark task 5 as done"
        You call: complete_task(task_id=5)

        User says: "I finished the groceries task" (assume it's task ID 3)
        You call: complete_task(task_id=3)

    Note: If you don't know the task_id, call list_tasks() first to find it.
    """
    return complete_task_tool_handler_sync(task_id=task_id, user_id=None)


def update_task_tool_handler_sync(task_id: int, title: str = None, description: str = None, completed: bool = None, user_id: str = None) -> Dict[str, Any]:
    """Synchronous wrapper"""
    import traceback

    try:
        print(f"DEBUG update_task: task_id={task_id}, title='{title}', user_id={user_id}")

        # 1. Get user_id from context
        actual_user_id = user_id or getattr(_thread_local, 'user_id', None)
        print(f"DEBUG update_task: context_user_id={actual_user_id}")

        # 2. Validate user_id exists
        if not actual_user_id:
            error_msg = "No user context available. User must be logged in."
            print(f"ERROR: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "task_id": task_id,
                "title": title,
                "message": f"❌ Failed to update task: {error_msg}"  # Clear message for agent
            }

        # 3. Validate UUID format
        try:
            from uuid import UUID
            UUID(actual_user_id)
        except (ValueError, AttributeError):
            error_msg = "Invalid user session format"
            print(f"ERROR: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "task_id": task_id,
                "title": title,
                "message": f"❌ Failed to update task: {error_msg}"
            }

        # 4. Call async handler
        params = {
            "user_id": actual_user_id,
            "task_id": task_id,
            "title": title,
            "description": description,
            "completed": completed
        }
        result = update_task_tool_handler(params)
        print(f"DEBUG update_task: result={result}")

        # 5. Check for errors
        if result.get("is_error", False):
            content = result.get("content", [])
            error_text = content[0].text if content and hasattr(content[0], 'text') else "Unknown error"
            return {
                "success": False,
                "error": error_text,
                "task_id": task_id,
                "title": title,
                "message": f"❌ Failed to update task: {error_text}"  # Clear for agent
            }

        # 6. Return structured result
        structured_result = result.get("structured_result", {})
        if structured_result:
            updated_title = structured_result.get("title", title or "Unknown Task")
            structured_result["message"] = f"✅ Successfully updated task '{updated_title}'"
            return structured_result
        else:
            error_msg = "Task update failed - no result returned"
            print(f"WARNING: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "task_id": task_id,
                "title": title,
                "message": f"❌ Failed to update task: {error_msg}"
            }

    except Exception as e:
        error_msg = f"Exception in update_task: {str(e)}"
        print(f"ERROR: {error_msg}")
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "task_id": task_id,
            "title": title,
            "message": f"❌ Error updating task: {str(e)}"
        }


# Decorated function for OpenAI Agents SDK
@function_tool
def update_task(task_id: int, title: str = None, description: str = None, completed: bool = None) -> Dict[str, Any]:
    """
    Modify an existing task's details (title, description, or completion status).

    Use this tool when the user wants to:
    - Change a task's title
    - Update task description
    - Edit task details
    - Rename a task

    Args:
        task_id (int): REQUIRED. The ID of the task to update.
        title (str): OPTIONAL. New title for the task.
        description (str): OPTIONAL. New description for the task.
        completed (bool): OPTIONAL. New completion status (true/false).

    Returns:
        Dict with 'success' (bool), 'task_id' (int), 'title' (str), 'error' (str or None)

    Example Usage:
        User says: "Change task 3's title to 'Buy organic groceries'"
        You call: update_task(task_id=3, title="Buy organic groceries")

        User says: "Add description 'urgent' to task 5"
        You call: update_task(task_id=5, description="urgent")

    Note: You must provide at least ONE field to update (title, description, or completed).
    """
    return update_task_tool_handler_sync(
        task_id=task_id,
        title=title,
        description=description,
        completed=completed,
        user_id=None
    )


def delete_task_tool_handler_sync(task_id: int, user_id: str = None) -> Dict[str, Any]:
    """Synchronous wrapper"""
    import traceback

    try:
        print(f"DEBUG delete_task: task_id={task_id}, user_id={user_id}")

        # 1. Get user_id from context
        actual_user_id = user_id or getattr(_thread_local, 'user_id', None)
        print(f"DEBUG delete_task: context_user_id={actual_user_id}")

        # 2. Validate user_id exists
        if not actual_user_id:
            error_msg = "No user context available. User must be logged in."
            print(f"ERROR: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "task_id": task_id,
                "title": None,
                "message": f"❌ Failed to delete task: {error_msg}"  # Clear message for agent
            }

        # 3. Validate UUID format
        try:
            from uuid import UUID
            UUID(actual_user_id)
        except (ValueError, AttributeError):
            error_msg = "Invalid user session format"
            print(f"ERROR: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "task_id": task_id,
                "title": None,
                "message": f"❌ Failed to delete task: {error_msg}"
            }

        # 4. Call async handler
        params = {
            "user_id": actual_user_id,
            "task_id": task_id
        }
        result = delete_task_tool_handler(params)
        print(f"DEBUG delete_task: result={result}")

        # 5. Check for errors
        if result.get("is_error", False):
            content = result.get("content", [])
            error_text = content[0].text if content and hasattr(content[0], 'text') else "Unknown error"
            return {
                "success": False,
                "error": error_text,
                "task_id": task_id,
                "title": None,
                "message": f"❌ Failed to delete task: {error_text}"  # Clear for agent
            }

        # 6. Return structured result
        structured_result = result.get("structured_result", {})
        if structured_result:
            deleted_title = structured_result.get("title", "Unknown Task")
            structured_result["message"] = f"✅ Successfully deleted task '{deleted_title}'"
            return structured_result
        else:
            error_msg = "Task deletion failed - no result returned"
            print(f"WARNING: {error_msg}")
            return {
                "success": False,
                "error": error_msg,
                "task_id": task_id,
                "title": None,
                "message": f"❌ Failed to delete task: {error_msg}"
            }

    except Exception as e:
        error_msg = f"Exception in delete_task: {str(e)}"
        print(f"ERROR: {error_msg}")
        traceback.print_exc()
        return {
            "success": False,
            "error": str(e),
            "task_id": task_id,
            "title": None,
            "message": f"❌ Error deleting task: {str(e)}"
        }


# Decorated function for OpenAI Agents SDK
@function_tool
def delete_task(task_id: int) -> Dict[str, Any]:
    """
    Permanently remove a task from the user's todo list.

    Use this tool when the user wants to:
    - Delete a task
    - Remove an item
    - Get rid of a task
    - Clear a specific todo

    Args:
        task_id (int): REQUIRED. The ID of the task to delete.

    Returns:
        Dict with 'success' (bool), 'task_id' (int), 'title' (str), 'error' (str or None)

    Example Usage:
        User says: "Delete task 7"
        You call: delete_task(task_id=7)

        User says: "Remove the groceries task" (assume it's task ID 3)
        You call: delete_task(task_id=3)

    Warning: This action is permanent and cannot be undone!
    Note: If you don't know the task_id, call list_tasks() first to find it.
    """
    return delete_task_tool_handler_sync(task_id=task_id, user_id=None)


def add_task_tool_handler_sync_db(params: Dict[str, Any], db_session: Session) -> Dict[str, Any]:
    """
    Synchronous handler for the add_task MCP tool that operates on a provided database session

    Args:
        params: Parameters for the task to add
        db_session: Active database session

    Returns:
        Dictionary with structured response
    """
    # Parse and validate input parameters
    input_data = AddTaskInput(**params)

    # Validate required fields
    if not input_data.title.strip():
        return {
            "content": [
                TextContent(
                    text=f"Error: Task title is required and cannot be empty"
                )
            ],
            "is_error": True
        }

    # Validate user_id format and convert to UUID
    try:
        user_id_uuid = UUID(input_data.user_id)
    except ValueError:
        return {
            "content": [
                TextContent(
                    text=f"Error: Invalid user_id format - not a valid UUID"
                )
            ],
            "is_error": True
        }

    try:
        # Create new task instance using the existing Task model
        new_task = Task(
            owner_user_id=str(user_id_uuid),  # Ensure UUID is converted to string
            title=input_data.title,
            description=input_data.description if input_data.description and input_data.description.strip() else None,
            completed=False
        )

        # Add to database
        db_session.add(new_task)
        db_session.commit()
        db_session.refresh(new_task)

        # Return success response
        return {
            "content": [
                TextContent(
                    text=f"Successfully added task '{new_task.title}' (ID: {new_task.id})"
                )
            ],
            "is_error": False,
            "structured_result": {
                "task_id": new_task.id,
                "title": new_task.title,
                "description": new_task.description,
                "completed": new_task.completed,
                "success": True
            }
        }

    except Exception as e:
        # Handle database errors
        try:
            db_session.rollback()
        except:
            pass  # Ignore rollback errors
        return {
            "content": [
                TextContent(
                    text=f"Error creating task: {str(e)}"
                )
            ],
            "is_error": True
        }


def add_task_tool_handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for the add_task MCP tool

    Task: TASK-005
    Spec: Implements MCP tool for adding new todo tasks to database
    """
    # Use the synchronous session with proper generator handling
    gen = get_session_sync()
    try:
        # Get the session from the generator
        session = next(gen)
        result = add_task_tool_handler_sync_db(params, session)
        return result
    except Exception as e:
        return {
            "content": [
                TextContent(
                    text=f"Error in add_task_tool_handler: {str(e)}"
                )
            ],
            "is_error": True
        }
    finally:
        # Consume the rest of the generator to trigger the finally block and close the session
        try:
            while True:
                next(gen)
        except StopIteration:
            pass  # Expected when generator is exhausted


def list_tasks_tool_handler_sync_db(params: Dict[str, Any], db_session: Session) -> Dict[str, Any]:
    """
    Synchronous handler for the list_tasks MCP tool that operates on a provided database session

    Args:
        params: Parameters for the task listing
        db_session: Active database session

    Returns:
        Dictionary with structured response
    """
    # Parse and validate input parameters
    input_data = ListTasksInput(**params)

    # Validate user_id format and convert to UUID
    try:
        user_id_uuid = UUID(input_data.user_id)
    except ValueError:
        return {
            "content": [
                TextContent(
                    text=f"Error: Invalid user_id format - not a valid UUID"
                )
            ],
            "is_error": True
        }

    try:
        # Build query to fetch tasks for the user
        query = select(Task).where(Task.owner_user_id == str(user_id_uuid))  # Convert UUID to string

        # Apply status filter if provided
        if input_data.status:
            if input_data.status.lower() == "completed":
                query = query.where(Task.completed == True)
            elif input_data.status.lower() == "pending":
                query = query.where(Task.completed == False)
            # If an invalid status is provided, we ignore the filter and return all tasks

        # Execute query
        result = db_session.exec(query)
        tasks = result.all()

        # Format response
        if not tasks:
            response_text = f"No tasks found for user {input_data.user_id}."
        else:
            task_list = []
            for task in tasks:
                status = "completed" if task.completed else "pending"
                task_info = f"- ID: {task.id}, Title: {task.title}, Status: {status}"
                if task.description:
                    task_info += f", Description: {task.description}"
                task_list.append(task_info)

            response_text = f"Found {len(tasks)} task(s) for user {input_data.user_id}:\n" + "\n".join(task_list)

        # Return success response
        return {
            "content": [
                TextContent(
                    text=response_text
                )
            ],
            "is_error": False,
            "structured_result": {
                "tasks": [
                    {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "completed": task.completed,
                        "created_at": task.created_at.isoformat() if task.created_at else None,
                        "updated_at": task.updated_at.isoformat() if task.updated_at else None
                    }
                    for task in tasks
                ],
                "count": len(tasks),
                "success": True
            }
        }

    except Exception as e:
        # Handle database errors
        return {
            "content": [
                TextContent(
                    text=f"Error listing tasks: {str(e)}"
                )
            ],
            "is_error": True
        }


def list_tasks_tool_handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for the list_tasks MCP tool

    Task: TASK-006
    Spec: Implements MCP tool for listing user's todo tasks from database
    """
    # Use the synchronous session with proper generator handling
    gen = get_session_sync()
    try:
        # Get the session from the generator
        session = next(gen)
        result = list_tasks_tool_handler_sync_db(params, session)
        return result
    except Exception as e:
        return {
            "content": [
                TextContent(
                    text=f"Error in list_tasks_tool_handler: {str(e)}"
                )
            ],
            "is_error": True
        }
    finally:
        # Consume the rest of the generator to trigger the finally block and close the session
        try:
            while True:
                next(gen)
        except StopIteration:
            pass  # Expected when generator is exhausted


def complete_task_tool_handler_sync_db(params: Dict[str, Any], db_session: Session) -> Dict[str, Any]:
    """
    Synchronous handler for the complete_task MCP tool that operates on a provided database session

    Args:
        params: Parameters for the task completion
        db_session: Active database session

    Returns:
        Dictionary with structured response
    """
    # Parse and validate input parameters
    input_data = CompleteTaskInput(**params)

    # Validate user_id format and convert to UUID
    try:
        user_id_uuid = UUID(input_data.user_id)
    except ValueError:
        return {
            "content": [
                TextContent(
                    text=f"Error: Invalid user_id format - not a valid UUID"
                )
            ],
            "is_error": True
        }

    # Validate task_id
    if not isinstance(input_data.task_id, int) or input_data.task_id <= 0:
        return {
            "content": [
                TextContent(
                    text=f"Error: Invalid task_id provided"
                )
            ],
            "is_error": True
        }

    try:
        # Find the task by ID and user_id to ensure the user owns the task
        query = select(Task).where(
            Task.id == input_data.task_id,
            Task.owner_user_id == str(user_id_uuid)  # Convert UUID to string
        )

        result = db_session.exec(query)
        task = result.first()

        if not task:
            return {
                "content": [
                    TextContent(
                        text=f"Error: Task with ID {input_data.task_id} not found for user {input_data.user_id} or you don't have permission to modify it"
                    )
                ],
                "is_error": True
            }

        # Update the task to mark it as completed
        task.completed = True
        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        # Return success response
        return {
            "content": [
                TextContent(
                    text=f"Successfully marked task '{task.title}' (ID: {task.id}) as completed"
                )
            ],
            "is_error": False,
            "structured_result": {
                "task_id": task.id,
                "title": task.title,
                "completed": task.completed,
                "success": True
            }
        }

    except Exception as e:
        # Handle database errors
        try:
            db_session.rollback()
        except:
            pass  # Ignore rollback errors
        return {
            "content": [
                TextContent(
                    text=f"Error completing task: {str(e)}"
                )
            ],
            "is_error": True
        }


def complete_task_tool_handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for the complete_task MCP tool

    Task: TASK-007
    Spec: Implements MCP tool for marking a user's todo task as completed
    """
    # Use the synchronous session with proper generator handling
    gen = get_session_sync()
    try:
        # Get the session from the generator
        session = next(gen)
        result = complete_task_tool_handler_sync_db(params, session)
        return result
    except Exception as e:
        return {
            "content": [
                TextContent(
                    text=f"Error in complete_task_tool_handler: {str(e)}"
                )
            ],
            "is_error": True
        }
    finally:
        # Consume the rest of the generator to trigger the finally block and close the session
        try:
            while True:
                next(gen)
        except StopIteration:
            pass  # Expected when generator is exhausted


def update_task_tool_handler_sync_db(params: Dict[str, Any], db_session: Session) -> Dict[str, Any]:
    """
    Synchronous handler for the update_task MCP tool that operates on a provided database session

    Args:
        params: Parameters for the task update
        db_session: Active database session

    Returns:
        Dictionary with structured response
    """
    # Parse and validate input parameters
    input_data = UpdateTaskInput(**params)

    # Validate user_id format and convert to UUID
    try:
        user_id_uuid = UUID(input_data.user_id)
    except ValueError:
        return {
            "content": [
                TextContent(
                    text=f"Error: Invalid user_id format - not a valid UUID"
                )
            ],
            "is_error": True
        }

    # Validate task_id
    if not isinstance(input_data.task_id, int) or input_data.task_id <= 0:
        return {
            "content": [
                TextContent(
                    text=f"Error: Invalid task_id provided"
                )
            ],
            "is_error": True
        }

    # At least one field to update must be provided
    if input_data.title is None and input_data.description is None and input_data.completed is None:
        return {
            "content": [
                TextContent(
                    text=f"Error: At least one field (title, description, or completed) must be provided for update"
                )
            ],
            "is_error": True
        }

    try:
        # Find the task by ID and user_id to ensure the user owns the task
        query = select(Task).where(
            Task.id == input_data.task_id,
            Task.owner_user_id == str(user_id_uuid)  # Convert UUID to string
        )

        result = db_session.exec(query)
        task = result.first()

        if not task:
            return {
                "content": [
                    TextContent(
                        text=f"Error: Task with ID {input_data.task_id} not found for user {input_data.user_id} or you don't have permission to modify it"
                    )
                ],
                "is_error": True
            }

        # Update the task fields that were provided
        if input_data.title is not None:
            task.title = input_data.title
        if input_data.description is not None:
            task.description = input_data.description if input_data.description and input_data.description.strip() else None
        if input_data.completed is not None:
            task.completed = input_data.completed

        db_session.add(task)
        db_session.commit()
        db_session.refresh(task)

        # Return success response
        update_fields = []
        if input_data.title is not None:
            update_fields.append("title")
        if input_data.description is not None:
            update_fields.append("description")
        if input_data.completed is not None:
            update_fields.append("completed")

        return {
            "content": [
                TextContent(
                    text=f"Successfully updated task '{task.title}' (ID: {task.id}): {', '.join(update_fields)} changed"
                )
            ],
            "is_error": False,
            "structured_result": {
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "success": True
            }
        }

    except Exception as e:
        # Handle database errors
        try:
            db_session.rollback()
        except:
            pass  # Ignore rollback errors
        return {
            "content": [
                TextContent(
                    text=f"Error updating task: {str(e)}"
                )
            ],
            "is_error": True
        }


def update_task_tool_handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for the update_task MCP tool

    Task: TASK-008
    Spec: Implements MCP tool for updating a user's todo task details
    """
    # Use the synchronous session with proper generator handling
    gen = get_session_sync()
    try:
        # Get the session from the generator
        session = next(gen)
        result = update_task_tool_handler_sync_db(params, session)
        return result
    except Exception as e:
        return {
            "content": [
                TextContent(
                    text=f"Error in update_task_tool_handler: {str(e)}"
                )
            ],
            "is_error": True
        }
    finally:
        # Consume the rest of the generator to trigger the finally block and close the session
        try:
            while True:
                next(gen)
        except StopIteration:
            pass  # Expected when generator is exhausted


def delete_task_tool_handler_sync_db(params: Dict[str, Any], db_session: Session) -> Dict[str, Any]:
    """
    Synchronous handler for the delete_task MCP tool that operates on a provided database session

    Args:
        params: Parameters for the task deletion
        db_session: Active database session

    Returns:
        Dictionary with structured response
    """
    # Parse and validate input parameters
    input_data = DeleteTaskInput(**params)

    # Validate user_id format and convert to UUID
    try:
        user_id_uuid = UUID(input_data.user_id)
    except ValueError:
        return {
            "content": [
                TextContent(
                    text=f"Error: Invalid user_id format - not a valid UUID"
                )
            ],
            "is_error": True
        }

    # Validate task_id
    if not isinstance(input_data.task_id, int) or input_data.task_id <= 0:
        return {
            "content": [
                TextContent(
                    text=f"Error: Invalid task_id provided"
                )
            ],
            "is_error": True
        }

    try:
        # Find the task by ID and user_id to ensure the user owns the task
        query = select(Task).where(
            Task.id == input_data.task_id,
            Task.owner_user_id == str(user_id_uuid)  # Convert UUID to string
        )

        result = db_session.exec(query)
        task = result.first()

        if not task:
            return {
                "content": [
                    TextContent(
                        text=f"Error: Task with ID {input_data.task_id} not found for user {input_data.user_id} or you don't have permission to delete it"
                    )
                ],
                "is_error": True
            }

        # Delete the task from the database
        db_session.delete(task)
        db_session.commit()

        # Return success response
        return {
            "content": [
                TextContent(
                    text=f"Successfully deleted task '{task.title}' (ID: {task.id})"
                )
            ],
            "is_error": False,
            "structured_result": {
                "task_id": task.id,
                "title": task.title,
                "success": True
            }
        }

    except Exception as e:
        # Handle database errors
        try:
            db_session.rollback()
        except:
            pass  # Ignore rollback errors
        return {
            "content": [
                TextContent(
                    text=f"Error deleting task: {str(e)}"
                )
            ],
            "is_error": True
        }


def delete_task_tool_handler(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    Handler for the delete_task MCP tool

    Task: TASK-009
    Spec: Implements MCP tool for deleting a user's todo task from database
    """
    # Use the synchronous session with proper generator handling
    gen = get_session_sync()
    try:
        # Get the session from the generator
        session = next(gen)
        result = delete_task_tool_handler_sync_db(params, session)
        return result
    except Exception as e:
        return {
            "content": [
                TextContent(
                    text=f"Error in delete_task_tool_handler: {str(e)}"
                )
            ],
            "is_error": True
        }
    finally:
        # Consume the rest of the generator to trigger the finally block and close the session
        try:
            while True:
                next(gen)
        except StopIteration:
            pass  # Expected when generator is exhausted


def set_current_user_id(user_id: str):
    """Set the current user ID in thread-local storage for the tool context"""
    _thread_local.user_id = user_id


def get_current_user_id() -> str:
    """Get the current user ID from thread-local storage"""
    return getattr(_thread_local, 'user_id', None)


def clear_current_user_id():
    """Clear the current user ID from thread-local storage"""
    if hasattr(_thread_local, 'user_id'):
        delattr(_thread_local, 'user_id')