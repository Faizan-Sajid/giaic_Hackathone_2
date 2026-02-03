# Task: T012
# Spec: Implementation Plan - Phase 2.1 Backend Foundation
# Spec: Error Handling Strategy (plan.md lines 480-508)
# Spec: Logging Strategy (plan.md lines 493-508)
# Implementation: Structured JSON logging with correlation ID middleware

import os
import uuid
import json
import logging
from fastapi import Request
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from datetime import datetime


# Structured JSON logger configuration
# Task: T012
# Spec: NFR-002 (structured JSON logging with correlation IDs)
# SEC-010 (log authentication events with correlation IDs)
class JSONFormatter(logging.Formatter):
    """
    Format log records as structured JSON

    Task: T012
    Spec: NFR-002 (structured JSON logging with correlation IDs)
    """

    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "correlation_id": getattr(record, 'correlation_id', None),
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Include exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Include extra fields
        if hasattr(record, 'correlation_id'):
            log_entry["correlation_id"] = record.correlation_id

        return json.dumps(log_entry)


# Configure structured JSON logger
logger = logging.getLogger("todo_app")
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)


async def get_correlation_id(request: Request) -> str:
    """
    Extract or generate correlation ID from request

    Task: T012
    Spec: NFR-002 (correlation ID for request tracing)
    SEC-010 (correlation ID in auth event logs)

    Returns correlation ID for request tracing
    """
    # Check for X-Correlation-ID header
    correlation_id = request.headers.get("X-Correlation-ID")

    # Generate new UUID if not present
    if not correlation_id:
        correlation_id = str(uuid.uuid4())

    return correlation_id


@asynccontextmanager
async def log_request_context(correlation_id: str):
    """
    Context manager for request-scoped logging with correlation ID

    Task: T012
    Spec: NFR-002 (correlation ID for request tracing)
    """
    # Create adapter with correlation ID bound
    extra = {"correlation_id": correlation_id}
    adapter = logging.LoggerAdapter(logger, extra)

    try:
        yield adapter
    finally:
        # Context cleanup happens automatically
        pass


def log_request(
    correlation_id: str,
    user_id: str | None,
    endpoint: str,
    method: str,
    status_code: int,
    duration_ms: float,
    message: str
):
    """
    Log HTTP request with structured data

    Task: T012
    Spec: NFR-002 (structured JSON logging with correlation IDs)

    NEVER logs: passwords, tokens, PII
    """
    logger.info(
        message,
        extra={
            "correlation_id": correlation_id,
            "user_id": user_id,
            "endpoint": endpoint,
            "method": method,
            "status_code": status_code,
            "duration_ms": duration_ms
        }
    )


def log_authentication_event(
    correlation_id: str,
    event_type: str,
    user_id: str | None,
    success: bool,
    details: str | None = None
):
    """
    Log authentication events for audit trails

    Task: T012
    Spec: SEC-010 (log authentication events with correlation IDs)

    Events: login, logout, failed_login, register

    NEVER logs: passwords
    """
    logger.info(
        f"Auth event: {event_type}",
        extra={
            "correlation_id": correlation_id,
            "user_id": user_id,
            "event_type": event_type,
            "success": success,
            "details": details
        }
    )


def log_error(
    correlation_id: str,
    error: Exception,
    context: str | None = None
):
    """
    Log errors with correlation ID and context

    Task: T012
    Spec: NFR-002 (structured JSON logging with correlation IDs)

    NEVER exposes: stack traces, database schema, internal service names
    """
    logger.error(
        f"Error: {str(error)}",
        extra={
            "correlation_id": correlation_id,
            "error_type": type(error).__name__,
            "context": context
        }
    )
