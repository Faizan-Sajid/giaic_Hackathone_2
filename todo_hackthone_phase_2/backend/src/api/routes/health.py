# Task: T057
# Spec: Implementation Plan - Phase 6: Health Check & API Documentation
# Spec: API Contracts - Health Check Endpoint (implied in spec.md)
# Implementation: Health check endpoint returning status, database connectivity, environment info

import asyncio
import os
from datetime import datetime
from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from src.core.database import engine
from src.core.logging import get_correlation_id


router = APIRouter(prefix="", tags=["Health Check"])


@router.get("/health")
async def health_check(request: Request):
    """
    Health check endpoint for service monitoring

    Task: T057
    Spec: Health Check & API Documentation (plan.md lines 566-569)
    Spec: API Contracts - Health Check Endpoint (implied in spec.md)
    Spec: Quick Start (quickstart.md lines 164-174)

    Returns:
        - 200 OK: Service is healthy
        - 503 Service Unavailable: Database disconnected

    No authentication required
    Monitoring endpoint for deployment verification
    """
    correlation_id = get_correlation_id(request)

    # Check database connectivity with retry (T053)
    db_status = "connected"
    db_connection_attempts = 0
    max_retries = 3

    while db_connection_attempts < max_retries:
        try:
            # Simple query to test connection
            async with engine.connect() as conn:
                await conn.execute("SELECT 1")
            break  # Connection successful
        except Exception as e:
            db_connection_attempts += 1
            if db_connection_attempts < max_retries:
                # Wait 1 second before retrying
                await asyncio.sleep(1)
            else:
                db_status = "disconnected"
                print(f"Database connection failed after {max_retries} attempts: {e}")

    # Determine overall status based on database health
    overall_status = "healthy" if db_status == "connected" else "unhealthy"

    # Get environment info
    environment = os.getenv("ENVIRONMENT", "development")

    # Return appropriate status code
    http_status = status.HTTP_200_OK if db_status == "connected" else status.HTTP_503_SERVICE_UNAVAILABLE

    from fastapi.responses import JSONResponse
    return JSONResponse(
        status_code=http_status,
        content={
            "status": overall_status,
            "database": db_status,
            "environment": environment,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "correlation_id": correlation_id
        }
    )
