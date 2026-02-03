# Task: T015
# Spec: Research Document (research.md R-003: User ID Storage in JWT)
# Spec: Security Standards (constitution)
# Implementation: JWT verification utility extracting user_id from sub claim

import os
from jwt import DecodeError, InvalidTokenError, ExpiredSignatureError, decode, encode
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def verify_jwt(token: str) -> str:
    """
    Verify and decode JWT token, extract user_id from sub claim

    Task: T015
    Spec: SEC-002 (JWT 7-day max expiration)
    SEC-004 (JWT contains user_id claim)
    FR-005 (extract and validate user_id from JWT)
    FR-006 (require valid JWT for protected endpoints)

    Returns:
        user_id (string) if token is valid

    Raises:
        HTTPException(status_code=401) if token is invalid/expired/missing
    """
    # Get JWT secret and algorithm from environment
    secret = os.getenv("JWT_SECRET")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    if not secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT secret not configured"
        )

    try:
        # Decode JWT token
        payload = decode(
            token,
            secret,
            algorithms=[algorithm],
            options={"verify_exp": True}  # Verify expiration
        )

        # Extract user_id from 'sub' claim (standard JWT practice)
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id claim"
            )

        # Optional: Verify expiration explicitly
        # JWT library handles exp claim with options={"verify_exp": True}
        # But we can add explicit check for safety
        if "exp" in payload:
            exp_time = payload["exp"]
            # Handle both datetime objects and timestamp formats
            if isinstance(exp_time, int):
                if datetime.utcnow().timestamp() > exp_time:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token expired"
                    )
            elif isinstance(exp_time, datetime):
                if datetime.utcnow() > exp_time:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Token expired"
                    )

        return user_id

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except DecodeError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )


# Task: T016
# Spec: Security Standards (constitution)
# Spec: Data Model - User Entity (data-model.md lines 9-84)
# Implementation: Password hashing utility with bcrypt 12+ rounds

import os
from bcrypt import hashpw, gensalt, checkpw
from typing import Optional


def hash_password(password: str, rounds: int = None) -> str:
    """
    Hash password using bcrypt with 12+ rounds

    Task: T016
    Spec: SEC-001 (bcrypt password hashing with 12+ rounds)
    DINT-001 (password hashing before storage)

    Args:
        password: Plain text password to hash
        rounds: Number of bcrypt rounds (default 12 from environment)

    Returns:
        Hashed password string (60 characters for bcrypt)

    Security:
        - NEVER logs passwords (even hashed)
        - Minimum 12 rounds for security
        - Salt is included in bcrypt hash automatically
    """
    # Use rounds from environment or default to 12
    bcrypt_rounds = rounds or int(os.getenv("BCRYPT_ROUNDS", "12"))

    if bcrypt_rounds < 12:
        raise ValueError("BCrypt rounds must be at least 12")

    # Generate salt and hash password
    # Bcrypt includes salt in the hash automatically
    salt = gensalt(rounds=bcrypt_rounds)
    hashed = hashpw(password.encode('utf-8'), salt)

    # Return as string (not bytes)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against bcrypt hash

    Task: T016
    Spec: FR-003 (password verification)
    DINT-001 (password verification)

    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hash from database

    Returns:
        True if password matches hash
        False if password doesn't match

    Security:
        - Uses constant-time comparison (bcrypt)
        - Never exposes timing attacks
    """
    # Encode strings to bytes for bcrypt
    plain_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')

    # Check password against hash
    return checkpw(plain_bytes, hashed_bytes)


# Task: T015
# Spec: Security Standards (constitution)
# Spec: Data Model - User Entity (data-model.md lines 9-84)
# Implementation: JWT creation utility with 7-day expiration


def create_jwt(user_id: str, email: str = None) -> str:
    """
    Create JWT token with user_id in sub claim and 7-day expiration

    Task: T015
    Spec: SEC-002 (JWT 7-day max expiration)
    SEC-004 (JWT contains user_id claim)
    FR-004 (JWT token issuance on successful authentication)

    Args:
        user_id: User ID to embed in token
        email: User email to include in token (optional)

    Returns:
        JWT token string

    Security:
        - NEVER logs JWT tokens (security requirement)
        - 7-day max expiration (configurable but max 7 days)
        - User ID in 'sub' claim (standard JWT practice)
        - HS256 algorithm (configurable from environment)
    """
    # Get JWT secret and algorithm from environment
    secret = os.getenv("JWT_SECRET")
    algorithm = os.getenv("JWT_ALGORITHM", "HS256")

    if not secret:
        raise ValueError("JWT secret not configured")

    # Create payload with user_id in 'sub' claim (standard JWT practice)
    # and expiration in 7 days
    now = datetime.utcnow()
    payload = {
        "sub": user_id,  # Standard claim for subject (user ID)
        "iat": now,  # Issued at time (datetime object)
        "exp": now + timedelta(days=7)  # Expires in 7 days (datetime object)
    }

    # Include email if provided
    if email:
        payload["email"] = email

    # Create and return JWT token
    # NEVER log the token itself (security requirement)
    token = encode(payload, secret, algorithm=algorithm)

    return token
