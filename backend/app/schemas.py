"""Vehicle Pydantic schemas for request/response validation."""
from datetime import datetime

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
