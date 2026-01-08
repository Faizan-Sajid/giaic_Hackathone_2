# API Routes Package
# Task: T023-T026, T035-T040, T057 (part of T017)
# Spec: Authentication, Task Management, and Health Check Endpoints

from .routes.auth import router as auth_router
from .routes.tasks import router as tasks_router
from .routes.health import router as health_router
from .deps import validate_user_id

__all__ = ["auth_router", "tasks_router", "health_router", "validate_user_id"]
