"""Dependency injection for routes."""
from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config import get_settings
from app.database import get_db
from app.models import User

settings = get_settings()


async def get_current_user(
    token: Annotated[str, Depends(lambda: None)],
    db: AsyncSession = Depends(get_db),
) -> User:
    """Get current authenticated user from JWT token.

    Args:
        token: JWT token from Authorization header
        db: Database session

    Returns:
        User object

    Raises:
        HTTPException: If token is invalid or user not found
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current user and verify admin role.

    Args:
        current_user: Current authenticated user

    Returns:
        User object if admin

    Raises:
        HTTPException: If user is not admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token.

    Args:
        data: Data to encode in token
        expires_delta: Token expiration time delta

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt
