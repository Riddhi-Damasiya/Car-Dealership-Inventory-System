"""Vehicle CRUD routes."""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.database import get_db
from app.dependencies import get_current_admin_user, get_current_user
from app.models import User, Vehicle
from app.schemas import (
    VehicleCreate,
    VehicleListResponse,
    VehicleResponse,
    VehicleUpdate,
)

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])


@router.post("", response_model=VehicleResponse, status_code=201)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    db: AsyncSession = Depends(get_db),
):
    """Create a new vehicle.

    Args:
        vehicle_data: Vehicle creation data
        current_user: Current authenticated admin user
        db: Database session

    Returns:
        Created vehicle

    Raises:
        HTTPException: If user is not admin
    """
    # Validate price is non-negative
    try:
        price_float = float(vehicle_data.price)
        if price_float < 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Price must be non-negative",
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Price must be a valid decimal number",
        )

    new_vehicle = Vehicle(
        make=vehicle_data.make,
        model=vehicle_data.model,
        category=vehicle_data.category,
        price=vehicle_data.price,
        quantity=vehicle_data.quantity,
    )
    db.add(new_vehicle)
    await db.commit()
    await db.refresh(new_vehicle)
    return new_vehicle


@router.get("", response_model=VehicleListResponse)
async def list_vehicles(
    skip: int = 0,
    limit: int = 10,
    current_user: Annotated[User, Depends(get_current_user)] = None,
    db: AsyncSession = Depends(get_db),
):
    """List all vehicles with pagination.

    Args:
        skip: Number of items to skip
        limit: Maximum items to return
        current_user: Current authenticated user
        db: Database session

    Returns:
        Paginated list of vehicles
    """
    # Get total count
    count_result = await db.execute(select(func.count(Vehicle.id)))
    total = count_result.scalar() or 0

    # Get vehicles with pagination
    result = await db.execute(
        select(Vehicle).offset(skip).limit(limit).order_by(Vehicle.id)
    )
    vehicles = result.scalars().all()

    return VehicleListResponse(
        items=vehicles,
        total=total,
        skip=skip,
        limit=limit,
    )


@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: int,
    current_user: Annotated[User, Depends(get_current_user)] = None,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific vehicle by ID.

    Args:
        vehicle_id: Vehicle ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Vehicle details

    Raises:
        HTTPException: If vehicle not found
    """
    result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
    vehicle = result.scalars().first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found",
        )

    return vehicle


@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    db: AsyncSession = Depends(get_db),
):
    """Update a vehicle.

    Args:
        vehicle_id: Vehicle ID
        vehicle_data: Updated vehicle data
        current_user: Current authenticated admin user
        db: Database session

    Returns:
        Updated vehicle

    Raises:
        HTTPException: If vehicle not found or user is not admin
    """
    # Validate price is non-negative
    try:
        price_float = float(vehicle_data.price)
        if price_float < 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Price must be non-negative",
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Price must be a valid decimal number",
        )

    result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
    vehicle = result.scalars().first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found",
        )

    vehicle.make = vehicle_data.make
    vehicle.model = vehicle_data.model
    vehicle.category = vehicle_data.category
    vehicle.price = vehicle_data.price
    vehicle.quantity = vehicle_data.quantity

    await db.commit()
    await db.refresh(vehicle)
    return vehicle


@router.delete("/{vehicle_id}", status_code=204)
async def delete_vehicle(
    vehicle_id: int,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    db: AsyncSession = Depends(get_db),
):
    """Delete a vehicle.

    Args:
        vehicle_id: Vehicle ID
        current_user: Current authenticated admin user
        db: Database session

    Raises:
        HTTPException: If vehicle not found or user is not admin
    """
    result = await db.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
    vehicle = result.scalars().first()

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found",
        )

    await db.delete(vehicle)
    await db.commit()
