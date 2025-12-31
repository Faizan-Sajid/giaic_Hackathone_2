"""CLI menu interface for Todo Console App."""

from typing import Optional

from src.models.task import Task
from src.services.task_service import EmptyTitleError, TaskService


class MenuOption:
    """Represents a menu option."""

    def __init__(self, number: int, description: str):
        self.number = number
        self.description = description

    def __str__(self) -> str:
        return f"{self.number}. {self.description}"


class Menu:
    """CLI menu for Todo Console App."""

    OPTIONS = [
        MenuOption(1, "Add Task"),
        MenuOption(2, "View Tasks"),
        MenuOption(3, "Update Task"),
        MenuOption(4, "Delete Task"),
        MenuOption(5, "Toggle Completion"),
        MenuOption(6, "Exit"),
    ]

    def __init__(self, service: TaskService):
        self._service = service

    def display(self) -> None:
        """Display the main menu."""
        print()
        print("=== Todo Console App ===")
        for option in self.OPTIONS:
            print(option)
        print()

    def get_choice(self) -> int:
        """Get user menu choice.

        Returns:
            The selected menu option number (1-6)

        Raises:
            ValueError: If input is not a valid integer 1-6
        """
        while True:
            try:
                choice = input("Enter your choice (1-6): ").strip()
                option = int(choice)
                if 1 <= option <= 6:
                    return option
                print("Invalid choice. Please enter a number 1-6.")
            except ValueError:
                print("Invalid choice. Please enter a number 1-6.")

    def get_task_id(self, prompt: str) -> Optional[int]:
        """Get a task ID from user input.

        Args:
            prompt: The prompt to display

        Returns:
            The task ID if valid, None if not an integer

        Raises:
            ValueError: If input is not a valid integer
        """
        while True:
            try:
                value = input(prompt).strip()
                task_id = int(value)
                return task_id
            except ValueError:
                print("Invalid ID. Please enter a number.")

    def get_title(self, prompt: str) -> str:
        """Get a task title from user input.

        Args:
            prompt: The prompt to display

        Returns:
            The title string
        """
        return input(prompt).strip()

    def get_description(self, prompt: str) -> Optional[str]:
        """Get an optional task description from user input.

        Args:
            prompt: The prompt to display

        Returns:
            The description string or None if empty
        """
        value = input(prompt).strip()
        return value if value else None

    def format_task(self, task: Task) -> str:
        """Format a single task for display.

        Args:
            task: The task to format

        Returns:
            Formatted task string
        """
        status = "Done" if task.completed else "Pending"
        desc = f" - {task.description}" if task.description else ""
        return f"{task.id:3} | [{status:8}] | {task.title}{desc}"

    def format_header(self) -> str:
        """Format the task list header.

        Returns:
            Header string
        """
        return "ID | Status    | Title"

    def format_separator(self) -> str:
        """Format the task list separator.

        Returns:
            Separator string
        """
        return "---+-----------+-------------------------"

    def run_add_task(self) -> None:
        """Run the Add Task workflow."""
        print()
        title = self.get_title("Enter task title: ")
        if not title:
            print("Error: Title cannot be empty.")
            return

        description = self.get_description(
            "Enter task description (optional): "
        )

        try:
            task = self._service.add_task(title, description)
            print(f"Task added successfully! ID: {task.id}")
        except EmptyTitleError as e:
            print(f"Error: {e}")

    def run_view_tasks(self) -> None:
        """Run the View Tasks workflow."""
        tasks = self._service.get_all_tasks()
        print()
        if not tasks:
            print("No tasks found. Add a task to get started!")
            return

        print(self.format_header())
        print(self.format_separator())
        for task in tasks:
            print(self.format_task(task))

    def run_update_task(self) -> None:
        """Run the Update Task workflow."""
        print()
        task_id = self.get_task_id("Enter task ID to update: ")
        task = self._service.get_task(task_id)
        if task is None:
            print(f"Error: Task {task_id} not found.")
            return

        title = self.get_title("Enter new title: ")
        if not title:
            print("Error: Title cannot be empty.")
            return

        description = self.get_description(
            "Enter new description (optional): "
        )

        try:
            self._service.update_task(task_id, title, description)
            print(f"Task {task_id} updated successfully.")
        except EmptyTitleError as e:
            print(f"Error: {e}")

    def run_delete_task(self) -> None:
        """Run the Delete Task workflow."""
        print()
        task_id = self.get_task_id("Enter task ID to delete: ")
        deleted = self._service.delete_task(task_id)
        if deleted:
            print(f"Task {task_id} deleted successfully.")
        else:
            print(f"Error: Task {task_id} not found.")

    def run_toggle_completion(self) -> None:
        """Run the Toggle Completion workflow."""
        print()
        task_id = self.get_task_id("Enter task ID to toggle: ")
        task = self._service.toggle_task(task_id)
        if task is None:
            print(f"Error: Task {task_id} not found.")
        elif task.completed:
            print(f"Task {task_id} marked as completed.")
        else:
            print(f"Task {task_id} marked as pending.")

    def run_exit(self) -> None:
        """Run the Exit workflow."""
        print("Goodbye! Thanks for using Todo Console App.")

    def handle_choice(self, choice: int) -> bool:
        """Handle a menu choice.

        Args:
            choice: The menu choice number

        Returns:
            True if application should continue, False if should exit
        """
        if choice == 1:
            self.run_add_task()
        elif choice == 2:
            self.run_view_tasks()
        elif choice == 3:
            self.run_update_task()
        elif choice == 4:
            self.run_delete_task()
        elif choice == 5:
            self.run_toggle_completion()
        elif choice == 6:
            self.run_exit()
            return False
        return True
