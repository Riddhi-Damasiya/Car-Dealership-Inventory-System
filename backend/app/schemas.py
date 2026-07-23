"""Pydantic schemas for authentication request/response."""
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """User registration schema.

    Attributes:
        email: Valid email address
        password: Password, minimum 6 characters
    """

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(
        ..., min_length=6, description="Password, minimum 6 characters"
    )


class UserLogin(BaseModel):
    """User login schema.

    Attributes:
        email: User email address
        password: User password
    """

    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., description="User password")


class TokenResponse(BaseModel):
    """JWT token response schema.

    Attributes:
        access_token: JWT token string
        token_type: Token type (usually 'bearer')
    """

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")


class UserResponse(BaseModel):
    """User response schema (without password).

    Attributes:
        id: User ID
        email: User email
        is_admin: Whether user is admin
    """

    id: int = Field(..., description="User ID")
    email: str = Field(..., description="User email")
    is_admin: bool = Field(..., description="Whether user is admin")

    class Config:
        """Pydantic config."""

        from_attributes = True
