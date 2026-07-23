"""Vehicle Pydantic schemas for request/response validation."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class VehicleCreate(BaseModel):
    """Vehicle creation schema.

    Attributes:
        make: Vehicle manufacturer (e.g., Toyota, Honda)
        model: Vehicle model name
        category: Vehicle category (e.g., Sedan, SUV, Truck)
        price: Vehicle price as decimal string
        quantity: Number of vehicles in stock
    """

    make: str = Field(..., min_length=1, description="Vehicle manufacturer")
    model: str = Field(..., min_length=1, description="Vehicle model")
    category: str = Field(..., min_length=1, description="Vehicle category")
    price: str = Field(..., description="Vehicle price (decimal string)")
    quantity: int = Field(..., ge=0, description="Quantity in stock (non-negative)")


class VehicleUpdate(BaseModel):
    """Vehicle update schema.

    Attributes:
        make: Vehicle manufacturer
        model: Vehicle model name
        category: Vehicle category
        price: Vehicle price as decimal string
        quantity: Number of vehicles in stock
    """

    make: str = Field(..., min_length=1, description="Vehicle manufacturer")
    model: str = Field(..., min_length=1, description="Vehicle model")
    category: str = Field(..., min_length=1, description="Vehicle category")
    price: str = Field(..., description="Vehicle price (decimal string)")
    quantity: int = Field(..., ge=0, description="Quantity in stock (non-negative)")


class VehicleResponse(BaseModel):
    """Vehicle response schema.

    Attributes:
        id: Vehicle ID
        make: Vehicle manufacturer
        model: Vehicle model name
        category: Vehicle category
        price: Vehicle price as decimal string
        quantity: Number of vehicles in stock
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: int = Field(..., description="Vehicle ID")
    make: str = Field(..., description="Vehicle manufacturer")
    model: str = Field(..., description="Vehicle model")
    category: str = Field(..., description="Vehicle category")
    price: str = Field(..., description="Vehicle price")
    quantity: int = Field(..., description="Quantity in stock")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        """Pydantic config."""

        from_attributes = True


class VehicleListResponse(BaseModel):
    """Paginated vehicle list response.

    Attributes:
        items: List of vehicles
        total: Total number of vehicles
        skip: Number of items skipped
        limit: Maximum items returned
    """

    items: list[VehicleResponse] = Field(..., description="List of vehicles")
    total: int = Field(..., description="Total number of vehicles")
    skip: int = Field(..., description="Items skipped")
    limit: int = Field(..., description="Items limit")


class SearchParams(BaseModel):
    """Search and filter parameters for vehicles.

    Attributes:
        make: Filter by vehicle manufacturer (optional)
        model: Filter by vehicle model (optional)
        category: Filter by vehicle category (optional)
        min_price: Filter by minimum price (optional)
        max_price: Filter by maximum price (optional)
    """

    make: Optional[str] = Field(None, description="Filter by make")
    model: Optional[str] = Field(None, description="Filter by model")
    category: Optional[str] = Field(None, description="Filter by category")
    min_price: Optional[str] = Field(None, description="Filter by minimum price")
    max_price: Optional[str] = Field(None, description="Filter by maximum price")


class PurchaseRequest(BaseModel):
    """Purchase request schema for buying vehicles.

    Attributes:
        quantity: Number of vehicles to purchase (must be positive)
    """

    quantity: int = Field(..., gt=0, description="Quantity to purchase (positive)")


class RestockRequest(BaseModel):
    """Restock request schema for adding inventory.

    Attributes:
        quantity: Number of vehicles to add to stock (must be positive)
    """

    quantity: int = Field(..., gt=0, description="Quantity to restock (positive)")


class PurchaseResponse(BaseModel):
    """Purchase confirmation response.

    Attributes:
        vehicle_id: ID of purchased vehicle
        quantity_purchased: Number of vehicles purchased
        total_price: Total purchase price
        remaining_quantity: Quantity remaining in stock
        message: Confirmation message
    """

    vehicle_id: int = Field(..., description="Vehicle ID")
    quantity_purchased: int = Field(..., description="Quantity purchased")
    total_price: str = Field(..., description="Total purchase price")
    remaining_quantity: int = Field(..., description="Remaining quantity in stock")
    message: str = Field(..., description="Confirmation message")


class RestockResponse(BaseModel):
    """Restock confirmation response.

    Attributes:
        vehicle_id: ID of restocked vehicle
        quantity_added: Number of vehicles added
        new_quantity: New total quantity in stock
        message: Confirmation message
    """

    vehicle_id: int = Field(..., description="Vehicle ID")
    quantity_added: int = Field(..., description="Quantity added")
    new_quantity: int = Field(..., description="New quantity in stock")
    message: str = Field(..., description="Confirmation message")


class UserLogin(BaseModel):
    """User login schema.

    Attributes:
        email: User email
        password: User password
    """

    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")


class UserRegister(BaseModel):
    """User registration schema.

    Attributes:
        email: User email
        password: User password
    """

    email: str = Field(..., description="User email")
    password: str = Field(..., description="User password")


class TokenResponse(BaseModel):
    """Token response schema.

    Attributes:
        access_token: JWT access token
        token_type: Type of token (e.g., bearer)
    """

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Token type")
