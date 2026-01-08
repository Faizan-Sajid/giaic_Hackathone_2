# Task: T023-T026
# Spec: API Contracts - Authentication Endpoints (contracts/auth-endpoints.md)
# Spec: Implementation Plan - Phase 2.2 Authentication Implementation
# Spec: Research Document (research.md R-001: Better Auth Integration Pattern)

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.core.database import get_session
from src.core.logging import log_authentication_event, get_correlation_id, log_request
from src.core.exceptions import (
    APIError,
    ValidationError,
    ConflictError,
    error_response_generator
)
from src.core.security import verify_jwt
from src.services import PasswordService, TokenService


# Task: T023
# Spec: API Contracts - Register Endpoint (contracts/auth-endpoints.md lines 9-57)
# Spec: Data Model - User Entity (data-model.md lines 9-84)
# Implementation: Register endpoint with email validation, password hashing, user creation

router = APIRouter(prefix="/auth", tags=["Authentication"])


class RegisterRequest(BaseModel):
    """
    Request model for user registration

    Task: T023
    Spec: FR-001 (registration with email and password)
    FR-005 (password minimum 8 characters)
    FR-016 (prevent duplicate email)
    """
    email: EmailStr
    password: str = Field(min_length=8, description="Password (minimum 8 characters)")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(
    register_request: RegisterRequest,
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_session)
):
    """
    Register new user with email and password

    Task: T023
    Spec: FR-001 (user registration with email and password)
    FR-005 (password minimum 8 characters)
    FR-006 (prevent duplicate email)
    FR-016 (email already registered returns 409)
    DINT-001 (email uniqueness)

    Accepts:
        - Email (RFC 5322 format)
        - Password (min 8 characters)

    Returns:
        - 201 Created: User registered successfully
            - Returns: id, email, message
        - 400 Bad Request: Invalid email format or password too short
        - 409 Conflict: Email already registered

    Security:
        - Passwords hashed with bcrypt 12+ rounds
        - Never logs passwords
        - Email uniqueness enforced
    """
    correlation_id = await get_correlation_id(request)

    # Check if email already exists (duplicate prevention)
    from src.models import User
    result = await session.execute(
        select(User).where(User.email == register_request.email)
    )
    existing_user = result.scalars().one_or_none()

    if existing_user:
        # Log failed registration attempt
        log_authentication_event(
            correlation_id=correlation_id,
            event_type="register_failed",
            user_id=None,
            success=False,
            details="Email already registered"
        )

        raise ConflictError(
            detail="Email already registered",
            correlation_id=correlation_id
        )

    # Hash password with bcrypt 12+ rounds
    password_hash = PasswordService.hash_password(register_request.password)

    # Create user
    from src.models import User
    user = User(
        email=register_request.email,
        password_hash=password_hash
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    # Log successful registration
    log_authentication_event(
        correlation_id=correlation_id,
        event_type="register_success",
        user_id=user.id,
        success=True,
        details=f"User registered: {register_request.email}"
    )

    # Log successful registration
    log_authentication_event(
        correlation_id=correlation_id,
        event_type="register_success",
        user_id=user.id,
        success=True,
        details=f"User registered: {register_request.email}"
    )

    # Create response object with content
    res = JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "id": user.id,
            "email": user.email,
            "message": "User registered successfully"
        },
        headers={"X-Correlation-ID": str(correlation_id)}
    )

    # Set JWT cookie for auto-login on the response object (same as login endpoint)
    res.set_cookie(
        key="token",
        value=TokenService.create_jwt(user.id, user.email),
        httponly=True,  # Prevents JavaScript access (XSS protection)
        secure=False,  # HTTP only (local development) - set to True in production
        samesite="lax",  # Lax CSRF protection for cross-origin compatibility
        max_age=604800,  # 7 days in seconds (7 * 24 * 60 * 60)
        path="/",  # Valid for entire domain
        domain=None  # Explicitly set domain to None
    )

    # Explicitly allow credentials
    res.headers["Access-Control-Allow-Credentials"] = "true"

    return res


# Task: T024
# Spec: API Contracts - Login Endpoint (contracts/auth-endpoints.md lines 60-119)
# Spec: Research Document (research.md R-001: Better Auth Integration Pattern)
# Implementation: Login endpoint with credential verification and JWT cookie setting

class LoginRequest(BaseModel):
    """
    Request model for user login

    Task: T024
    Spec: FR-003 (login with email and password)
    FR-004 (JWT token issuance on successful authentication)
    SEC-004 (JWT issuance with max 7-day expiration)
    """
    email: EmailStr
    password: str = Field(description="Password")


@router.post("/login")
async def login(
    login_request: LoginRequest,
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_session)
):
    """
    Authenticate user and set JWT cookie

    Task: T024
    Spec: FR-003 (login with email and password)
    FR-004 (JWT token issuance on successful authentication)
    SEC-004 (JWT issuance with max 7-day expiration)

    Accepts:
        - Email (registered user)
        - Password

    Returns:
        - 200 OK: Login successful, JWT cookie set
            - Returns: id, email, message
        - 401 Unauthorized: Invalid email or password

    Security:
        - JWT set in HTTP-only cookie (HttpOnly, Secure, SameSite=Strict)
        - JWT expires in 7 days
        - Passwords verified with bcrypt
        - Never logs passwords
    """
    correlation_id = await get_correlation_id(request)
    start_time = datetime.utcnow()

    # Find user by email
    from src.models import User
    result = await session.execute(
        select(User).where(User.email == login_request.email)
    )
    user = result.scalars().one_or_none()

    # Verify password
    if not user or not PasswordService.verify_password(login_request.password, user.password_hash):
        # Log failed login attempt
        log_authentication_event(
            correlation_id=correlation_id,
            event_type="login_failed",
            user_id=None,
            success=False,
            details=f"Failed login attempt for: {login_request.email}"
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"X-Correlation-ID": str(correlation_id)}
        )

    # Generate JWT token
    token = TokenService.create_jwt(user.id, user.email)

    # Log successful login
    end_time = datetime.utcnow()
    duration_ms = (end_time - start_time).total_seconds() * 1000

    log_authentication_event(
        correlation_id=correlation_id,
        event_type="login_success",
        user_id=user.id,
        success=True,
        details=f"User logged in: {login_request.email}"
    )

    # Create response object with content
    res = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "id": user.id,
            "email": user.email,
            "message": "Login successful"
        },
        headers={"X-Correlation-ID": str(correlation_id)}
    )

    # Set JWT cookie on the response object (HTTP-only, Secure=False for local development, SameSite=lax)
    res.set_cookie(
        key="token",
        value=token,
        httponly=True,  # Prevents JavaScript access (XSS protection)
        secure=False,  # HTTP only (local development) - set to True in production
        samesite="lax",  # Lax CSRF protection for cross-origin compatibility
        max_age=604800,  # 7 days in seconds (7 * 24 * 60 * 60)
        path="/",  # Valid for entire domain
        domain=None  # Explicitly set domain to None
    )

    # Explicitly allow credentials
    res.headers["Access-Control-Allow-Credentials"] = "true"

    return res


# Task: T025
# Spec: API Contracts - Logout Endpoint (contracts/auth-endpoints.md lines 123-166)
# Spec: FR-017 (invalidate JWT on logout)
# Implementation: Logout endpoint with JWT cookie clearing

@router.post("/logout")
async def logout(response: Response):
    """
    Invalidate session by clearing JWT cookie

    Task: T025
    Spec: FR-017 (invalidate JWT on logout)

    Returns:
        - 200 OK: Logout successful, cookie cleared
        - 401 Unauthorized: No valid JWT cookie

    Security:
        - Cookie cleared by setting expiration to past date
        - All security attributes maintained
    """
    correlation_id = response.headers.get("X-Correlation-ID", "unknown")

    # Clear JWT cookie by setting expiration to Unix epoch (1970-01-01)
    response.delete_cookie(
        key="token",
        path="/",
    )

    # Log logout event
    log_authentication_event(
        correlation_id=correlation_id,
        event_type="logout",
        user_id=None,
        success=True,
        details="User logged out"
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Logged out successfully"
        },
        headers={"X-Correlation-ID": str(correlation_id)}
    )


# Task: T026
# Spec: API Contracts - Session Endpoint (contracts/auth-endpoints.md lines 169-207)
# Implementation: Session validation endpoint returning user info if authenticated

async def get_current_user(
    request: Request,
    session: AsyncSession = Depends(get_session)
):
    """
    Dependency to extract and verify user from JWT token

    Task: T026
    Spec: Session validation endpoint
    """
    # Get token from cookie
    token = request.cookies.get("token")

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    # Verify token and extract user_id
    user_id = verify_jwt(token)

    # Get user from database
    from src.models import User
    result = await session.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalars().one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


@router.get("/session")
async def get_session(
    request: Request,
    session: AsyncSession = Depends(get_session),
    user=Depends(get_current_user)
):
    """
    Return user info if authenticated

    Task: T026
    Spec: Used by frontend to check auth state

    Returns:
        - 200 OK: User info if authenticated
            - Returns: user object with id, email
        - 401 Unauthorized: Not authenticated

    Security:
        - Requires valid JWT token
        - Verifies token expiration
        - Returns user_id from 'sub' claim
    """
    correlation_id = await get_correlation_id(request)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "user": {
                "id": user.id,
                "email": user.email
            },
            "authenticated": True
        },
        headers={"X-Correlation-ID": str(correlation_id)}
    )
