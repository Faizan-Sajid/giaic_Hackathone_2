# Quickstart: Todo Console App

**Feature**: 001-todo-cli
**Date**: 2025-12-31

## Prerequisites

- Python 3.13 or higher
- Terminal access (Windows, macOS, or Linux)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd phase_1

# Verify Python version
python --version  # Should show 3.13.x
```

## Running the Application

```bash
python src/todo_app.py
```

## Usage Walkthrough

### Adding Your First Task

```
=== Todo Console App ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Completion
6. Exit

Enter your choice (1-6): 1
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread
Task added successfully! ID: 1
```

### Viewing All Tasks

```
Enter your choice (1-6): 2
ID | Status    | Title
---+-----------+-------------------------
1  | [Pending] | Buy groceries
```

### Completing a Task

```
Enter your choice (1-6): 5
Enter task ID to toggle: 1
Task 1 marked as completed.
```

### Updating a Task

```
Enter your choice (1-6): 3
Enter task ID to update: 1
Enter new title: Buy groceries and cook dinner
Enter new description (optional): Get ingredients for pasta
Task 1 updated successfully.
```

### Deleting a Task

```
Enter your choice (1-6): 4
Enter task ID to delete: 1
Task 1 deleted successfully.
```

## Error Examples

### Invalid Menu Choice

```
Invalid choice. Please enter a number 1-6.
```

### Task Not Found

```
Error: Task 99 not found.
```

### Empty Title

```
Error: Title cannot be empty.
```

## Exiting

```
Enter your choice (1-6): 6
Goodbye! Thanks for using Todo Console App.
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/unit/test_task.py -v

# Run with coverage
pytest tests/ --cov=src
```

## Project Structure

```
src/
├── todo_app.py          # Entry point
├── models/
│   └── task.py          # Task dataclass
├── services/
│   └── task_service.py  # Business logic
├── repository/
│   └── task_repository.py  # In-memory storage
└── cli/
    └── menu.py          # CLI interface

tests/
├── unit/                # Unit tests
└── integration/         # End-to-end tests
```

## Next Steps

1. Run `/sp.tasks` to generate implementation tasks
2. Implement each task following the data model and contracts
3. Write tests before implementation (TDD approach)
4. Validate with `pytest` after each implementation
