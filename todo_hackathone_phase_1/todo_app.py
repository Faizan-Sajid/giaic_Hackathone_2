"""Main entry point for Todo Console App."""

from src.cli.menu import Menu
from src.repository.task_repository import TaskRepository
from src.services.task_service import TaskService


def main() -> None:
    """Run the Todo Console App."""
    # Initialize the application
    repository = TaskRepository()
    service = TaskService(repository)
    menu = Menu(service)

    # Main loop
    running = True
    while running:
        menu.display()
        choice = menu.get_choice()
        running = menu.handle_choice(choice)


if __name__ == "__main__":
    main()
