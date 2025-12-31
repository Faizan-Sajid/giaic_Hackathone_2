# Data Model: Todo Console App

**Date**: 2025-12-31
**Feature**: 001-todo-cli

## Entities

### Task

Represents a single todo item stored in memory.

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `id` | int | Yes | Auto-generated | Unique integer identifier |
| `title` | str | Yes | None | Task title (non-empty) |
| `description` | str \| None | No | None | Optional task details |
| `completed` | bool | No | False | Completion status |

### Validation Rules

| Rule | Description | Error Message |
|------|-------------|---------------|
| Title required | Title cannot be empty or whitespace-only | "Title cannot be empty" |
| ID must exist | Operation target must exist in repository | "Task not found" |
| ID uniqueness | New tasks get unique IDs | N/A (automatic) |

## State Transitions

```
Pending ----(toggle)----> Completed
   ^                        |
   |________________________|
      (toggle back)
```

## Repository Operations

### TaskRepository Interface

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `create(title, description)` | str, str \| None | Task | Creates new task with generated ID |
| `find_all()` | None | list[Task] | Returns all tasks in insertion order |
| `find_by_id(id)` | int | Task \| None | Returns task or None |
| `update(id, title, description)` | int, str, str \| None | Task | Updates task fields |
| `delete(id)` | int | bool | Removes task, returns True if found |
| `toggle(id)` | int | Task \| None | Toggles completion, returns updated task |

## CLI Menu Contract

### Menu Options

| Option | Action | Input Required | Output |
|--------|--------|----------------|--------|
| 1 | Add Task | Title, Description (optional) | Task ID, confirmation |
| 2 | View Tasks | None | Formatted task list |
| 3 | Update Task | Task ID, New Title, New Description | Confirmation |
| 4 | Delete Task | Task ID | Confirmation or error |
| 5 | Toggle Completion | Task ID | New status |
| 6 | Exit | None | Goodbye message |
