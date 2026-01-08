# Task: T014
# Spec: Implementation Plan - Phase 2.1 Backend Foundation
# Spec: Error Handling Strategy (plan.md lines 480-508)
# Spec: Error Taxonomy (spec.md lines 484-491)
# Implementation: Global error handling middleware with proper HTTP status codes

import os
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Any, Dict
from .logging import log_error


# HTTP Status Code Mapping from spec.md
# Task: T014
# Spec: Error Taxonomy (spec.md lines 484-491)
#
# 401 Unauthorized: Missing/invalid/expired JWT
# 403 Forbidden: User ID mismatch
# 404 Not Found: Task doesn't exist
# 400 Bad Request: Validation errors
# 409 Conflict: Email already registered
# 500 Internal Server Error: Database failure, unexpected errors


class APIError(Exception):
    """
    Base exception for API errors

    Task: T014
    Spec: Error Handling Strategy (plan.md lines 480-508)
    """
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail


class UnauthorizedError(APIError):
    """
    Unauthorized exception (401)
    Missing/invalid/expired JWT token
    """
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class ForbiddenError(APIError):
    """
    Forbidden exception (403)
    User ID mismatch (token.sub != url.user_id)
    """
    def __init__(self, detail: str = "Access denied"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class NotFoundError(APIError):
    """
    Not found exception (404)
    Task or user doesn't exist
    """
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class ValidationError(APIError):
    """
    Validation error exception (400)
    Invalid input (email format, password length, task validation)
    """
    def __init__(self, detail: str = "Invalid input"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ConflictError(APIError):
    """
    Conflict exception (409)
    Email already registered
    """
    def __init__(self, detail: str = "Resource conflict", correlation_id: str = None):
        self.correlation_id = correlation_id
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


def error_response_generator(correlation_id: str, detail: str, status_code: int) -> Dict[str, Any]:
    """
    Generate standardized error response

    Task: T014
    Spec: Error Handling Strategy (plan.md lines 480-508)
    NFR-007 (clear error messages without exposing internal details)

    Returns JSON response with:
    - error: User-friendly message
    - correlation_id: Request tracing ID
    - NEVER: Stack traces, database schema, internal service names
    """
    response = {
        "error": detail,
        "correlation_id": correlation_id
    }
    return response


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle FastAPI HTTP exceptions

    Task: T014
    Spec: Error Handling Strategy (plan.md lines 480-508)
    """
    correlation_id = request.headers.get("X-Correlation-ID", "unknown")

    # Get detail from exception
    detail = exc.detail if hasattr(exc, 'detail') else "An error occurred"

    log_error(
        correlation_id=correlation_id,
        error=exc,
        context=f"HTTP {exc.status_code}: {exc.__class__.__name__}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response_generator(correlation_id, detail, exc.status_code)
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """
    Handle Pydantic validation errors

    Task: T014
    Spec: Error Handling Strategy (plan.md lines 480-508)
    """
    correlation_id = request.headers.get("X-Correlation-ID", "unknown")

    # Format validation errors
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        message = error["msg"]
        errors.append(f"{field}: {message}")

    detail = "; ".join(errors) if errors else "Validation failed"

    log_error(
        correlation_id=correlation_id,
        error=exc,
        context=f"Validation error: {detail}"
    )

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=error_response_generator(correlation_id, detail, status.HTTP_400_BAD_REQUEST)
    )


async def conflict_exception_handler(request: Request, exc: ConflictError) -> JSONResponse:
    """
    Handle conflict errors (409)

    Task: T014
    Spec: Error Handling Strategy (plan.md lines 480-508)
    """
    correlation_id = getattr(exc, 'correlation_id', None) or request.headers.get("X-Correlation-ID", "unknown")

    log_error(
        correlation_id=correlation_id,
        error=exc,
        context=f"Conflict error: {exc.detail}"
    )

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content=error_response_generator(
            correlation_id,
            exc.detail,
            status.HTTP_409_CONFLICT
        )
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handle unexpected exceptions

    Task: T014
    Spec: Error Handling Strategy (plan.md lines 480-508)

    NEVER exposes: Stack traces, database schema, internal service names
    Returns user-friendly error message
    """
    correlation_id = request.headers.get("X-Correlation-ID", "unknown")

    log_error(
        correlation_id=correlation_id,
        error=exc,
        context="Unexpected server error"
    )

    # User-friendly message without internal details
    detail = "An unexpected error occurred"

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response_generator(
            correlation_id,
            detail,
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    )


def register_error_handlers(app: FastAPI):
    """
    Register all exception handlers with FastAPI application

    Task: T014
    Spec: Error Handling Strategy (plan.md lines 480-508)
    """
    # FastAPI HTTP exceptions
    app.add_exception_handler(HTTPException, http_exception_handler)

    # Pydantic validation errors
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    # Custom API exceptions
    app.add_exception_handler(ConflictError, conflict_exception_handler)

    # General exceptions (catch-all)
    app.add_exception_handler(Exception, general_exception_handler)
