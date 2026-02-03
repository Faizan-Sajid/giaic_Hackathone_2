# Task: T034
# Spec: Implementation Plan - Phase 2.2 Authentication Implementation
# Spec: Authentication Endpoints (contracts/auth-endpoints.md)
# Implementation: User ID validation middleware checking token.sub == request.path.user_id

from fastapi import Depends, HTTPException, status
from typing import Annotated


def get_token_user_id(token_user_id: str) -> str:
    """
    FastAPI dependency to extract user_id from JWT token

    Task: T034 (part of user ID validation)
    Spec: FR-005 (extract and validate user_id from JWT)
    """
    return token_user_id


def validate_user_id(
    token_user_id: Annotated[str, Depends(get_token_user_id)],
    url_user_id: str
) -> str:
    """
    Validate that token user_id matches URL user_id

    Task: T034
    Spec: FR-007 (enforce user_id matching)
    FR-014 (token user_id matches request URL user_id)

    Args:
        token_user_id: User ID extracted from JWT token
        url_user_id: User ID from request URL path

    Returns:
        user_id string if validation passes

    Raises:
        HTTPException(403 Forbidden) if user_id mismatch
    """
    # Compare token user_id with URL user_id
    # This prevents User A from accessing User B's resources
    if token_user_id != url_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user_id mismatch"
        )

    return url_user_id
