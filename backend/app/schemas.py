"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr


class UserRegister(UserBase):
    """User registration schema."""

    password: str = Field(..., min_length=6)


class UserLogin(UserBase):
    """User login schema."""

    password: str


class TokenResponse(BaseModel):
    """Token response schema."""

    access_token: str
    token_type: str = "bearer"


class VehicleBase(BaseModel):
    """Base vehicle schema."""

    make: str
    model: str
    category: str
    price: float = Field(..., gt=0)
    quantity: int = Field(default=0, ge=0)


class VehicleCreate(VehicleBase):
    """Vehicle creation schema."""

    pass


class VehicleUpdate(BaseModel):
    """Vehicle update schema."""

    make: str | None = None
    model: str | None = None
    category: str | None = None
    price: float | None = Field(None, gt=0)
    quantity: int | None = Field(None, ge=0)


class VehicleResponse(VehicleBase):
    """Vehicle response schema."""

    id: int

    class Config:
        from_attributes = True
