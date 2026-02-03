# Task: T021
# Spec: Research Document (research.md R-001: Better Auth Integration Pattern)
# Spec: Security Standards (constitution)
# Spec: Implementation Plan - Phase 2.2 Authentication Implementation
# Implementation: Password hashing and JWT generation functions

from src.core.security import hash_password, verify_password, create_jwt


# Task: T021
# Spec: Security Standards (constitution)
# Spec: Implementation Plan - Phase 2.2 Authentication Implementation
# Spec: Research Document (research.md R-001: Better Auth Integration Pattern)
# Implementation: AuthService with password hashing and JWT generation

import os
from jwt import InvalidTokenError, ExpiredSignatureError, decode, encode
from fastapi import HTTPException, status
from datetime import datetime, timedelta


# Task: T021
# Spec: Security Standards (constitution)
# Spec: SEC-001 (bcrypt minimum 12 rounds)
# Spec: Implementation Plan - Phase 2.2 Authentication Implementation
# Spec: Research Document (research.md R-001: Better Auth Integration Pattern)
# Implementation: Password hashing with bcrypt 12+ rounds

class PasswordService:
    """
    Password hashing and verification service

    Task: T021
    Spec: SEC-001 (bcrypt minimum 12 rounds)
    DINT-001 (password hashing before storage)

    Security:
        - NEVER logs passwords (even hashed)
        - Minimum 12 bcrypt rounds
        - Salt included in hash automatically
    """

    @staticmethod
    def hash_password(password: str, rounds: int = None) -> str:
        """
        Hash password using bcrypt with 12+ rounds

        Task: T021
        Spec: SEC-001 (bcrypt minimum 12 rounds)
        DINT-001 (password hashing before storage)

        Args:
            password: Plain text password to hash
            rounds: Number of bcrypt rounds (default 12 from env)

        Returns:
            Hashed password string (60 characters for bcrypt)

        Raises:
            ValueError: If rounds < 12
        """
        # Use default 12 rounds from environment or override
        bcrypt_rounds = rounds or int(os.getenv("BCRYPT_ROUNDS", "12"))

        if bcrypt_rounds < 12:
            raise ValueError("BCrypt rounds must be at least 12")

        # Hash password using bcrypt with specified rounds
        hashed = hash_password(password, rounds=bcrypt_rounds)

        return hashed

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify password against bcrypt hash

        Task: T021
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
        # Verify password using bcrypt
        is_valid = verify_password(plain_password, hashed_password)

        return is_valid


# Task: T022
# Spec: Security Standards (constitution)
# Spec: SEC-002 (JWT 7-day max expiration)
# Spec: SEC-004 (JWT contains user_id claim)
# Spec: FR-004 (JWT token with max 7-day expiration)
# Spec: Implementation Plan - Phase 2.2 Authentication Implementation
# Spec: Research Document (research.md R-003: User ID Storage in JWT)
# Implementation: JWT generation with user_id, email, expiration

class TokenService:
    """
    JWT token generation and verification service

    Task: T022
    Spec: SEC-002 (JWT 7-day max expiration)
    SEC-004 (JWT contains user_id claim)
    FR-004 (JWT token issuance on successful auth)
    FR-005 (extract and validate user_id from JWT)

    Security:
        - JWT secret stored in environment variable
        - HS256 algorithm with shared secret
        - 7-day maximum expiration
        - user_id in standard 'sub' claim
    """

    @staticmethod
    def create_jwt(user_id: str, email: str) -> str:
        """
        Create JWT token with user_id, email, expiration

        Task: T022
        Spec: FR-004 (JWT token with max 7-day expiration)
        SEC-002 (JWT 7-day max expiration)

        Args:
            user_id: User UUID for 'sub' claim
            email: User email (included in token)

        Returns:
            JWT token string

        Security:
            - 7-day maximum expiration
            - Standard 'sub' claim for user_id
            - HS256 algorithm with shared secret
        """
        # Get JWT secret and algorithm from environment
        secret = os.getenv("JWT_SECRET")
        algorithm = os.getenv("JWT_ALGORITHM", "HS256")

        if not secret:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="JWT secret not configured"
            )

        # Create JWT payload with 7-day expiration
        payload = {
            "sub": user_id,  # Subject: User UUID (standard JWT practice)
            "email": email,
            "iat": datetime.utcnow(),  # Issued at
            "exp": datetime.utcnow() + timedelta(days=7)  # Expires in 7 days
        }

        # Encode JWT token
        token = encode(
            payload,
            secret,
            algorithm=algorithm
        )

        return token

    @staticmethod
    def verify_token(token: str) -> dict:
        """
        Verify and decode JWT token, extract claims

        Task: T022
        Spec: SEC-002 (JWT 7-day max expiration)
        SEC-004 (JWT contains user_id claim)
        FR-006 (require valid JWT for protected endpoints)

        Args:
            token: JWT token string

        Returns:
            Dictionary with 'user_id', 'email', 'exp'

        Raises:
            HTTPException(401) if token is invalid/expired/missing user_id
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
            # Decode JWT token with expiration verification
            payload = decode(
                token,
                secret,
                algorithms=[algorithm],
                options={"verify_exp": True}
            )

            # Extract user_id from 'sub' claim (standard JWT practice)
            user_id = payload.get("sub")

            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token: missing user_id claim"
                )

            return {
                "user_id": user_id,
                "email": payload.get("email"),
                "exp": payload.get("exp")
            }

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
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
