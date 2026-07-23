"""Refactored vehicle CRUD routes using service layer."""
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_admin_user, get_current_user
from app.models import User
from app.schemas import (
    VehicleCreate,
    VehicleListResponse,
    VehicleResponse,
    VehicleUpdate,
)
from app.services.vehicle_service import VehicleService

router = APIRouter(prefix="/api/vehicles", tags=["vehicles"])


def get_vehicle_service(db: AsyncSession = Depends(get_db)) -> VehicleService:
    """Dependency injection for vehicle service.

    Args:
        db: Database session

    Returns:
        VehicleService instance
    """
    return VehicleService(db)


@router.post("", response_model=VehicleResponse, status_code=201)
async def create_vehicle(
    vehicle_data: VehicleCreate,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    service: VehicleService = Depends(get_vehicle_service),
) -> VehicleResponse:
    """Create a new vehicle.

    Args:
        vehicle_data: Vehicle creation data
        current_user: Current authenticated admin user
        service: Vehicle service

    Returns:
        Created vehicle

    Raises:
        HTTPException: If validation fails or user is not admin
    """
    try:
        return await service.create_vehicle(vehicle_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.get("", response_model=VehicleListResponse)
async def list_vehicles(
    skip: int = 0,
    limit: int = 10,
    current_user: Annotated[User, Depends(get_current_user)] = None,
    service: VehicleService = Depends(get_vehicle_service),
) -> VehicleListResponse:
    """List all vehicles with pagination.

    Args:
        skip: Number of items to skip (default: 0)
        limit: Maximum items to return (default: 10)
        current_user: Current authenticated user
        service: Vehicle service

    Returns:
        Paginated list of vehicles
    """
    return await service.list_vehicles(skip=skip, limit=limit)


@router.get("/search", response_model=list[VehicleResponse])
async def search_vehicles(
    make: Optional[str] = Query(None, description="Filter by make"),
    model: Optional[str] = Query(None, description="Filter by model"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_price: Optional[str] = Query(None, description="Minimum price"),
    max_price: Optional[str] = Query(None, description="Maximum price"),
    current_user: Annotated[User, Depends(get_current_user)] = None,
    service: VehicleService = Depends(get_vehicle_service),
) -> list[VehicleResponse]:
    """Search and filter vehicles based on optional criteria.

    All parameters are optional. When multiple filters are provided,
    they are combined with AND logic (all must match).

    Query Parameters:
        make: Filter by vehicle manufacturer (case-insensitive partial match)
        model: Filter by vehicle model (case-insensitive partial match)
        category: Filter by vehicle category (case-insensitive partial match)
        min_price: Minimum price filter (inclusive)
        max_price: Maximum price filter (inclusive)

    Args:
        make: Vehicle make filter
        model: Vehicle model filter
        category: Vehicle category filter
        min_price: Minimum price filter
        max_price: Maximum price filter
        current_user: Current authenticated user
        service: Vehicle service

    Returns:
        List of vehicles matching all filter criteria

    Raises:
        HTTPException: If price parameters are invalid
    """
    try:
        return await service.search_vehicles(
            make=make,
            model=model,
            category=category,
            min_price=min_price,
            max_price=max_price,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.get("/{vehicle_id}", response_model=VehicleResponse)
async def get_vehicle(
    vehicle_id: int,
    current_user: Annotated[User, Depends(get_current_user)] = None,
    service: VehicleService = Depends(get_vehicle_service),
) -> VehicleResponse:
    """Get a specific vehicle by ID.

    Args:
        vehicle_id: Vehicle ID
        current_user: Current authenticated user
        service: Vehicle service

    Returns:
        Vehicle details

    Raises:
        HTTPException: If vehicle not found
    """
    vehicle = await service.get_vehicle(vehicle_id)
    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found",
        )
    return VehicleResponse.model_validate(vehicle)


@router.put("/{vehicle_id}", response_model=VehicleResponse)
async def update_vehicle(
    vehicle_id: int,
    vehicle_data: VehicleUpdate,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    service: VehicleService = Depends(get_vehicle_service),
) -> VehicleResponse:
    """Update a vehicle.

    Args:
        vehicle_id: Vehicle ID
        vehicle_data: Updated vehicle data
        current_user: Current authenticated admin user
        service: Vehicle service

    Returns:
        Updated vehicle

    Raises:
        HTTPException: If vehicle not found, validation fails, or user is not admin
    """
    try:
        vehicle = await service.update_vehicle(vehicle_id, vehicle_data)
        if not vehicle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vehicle not found",
            )
        return VehicleResponse.model_validate(vehicle)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )


@router.delete("/{vehicle_id}", status_code=204)
async def delete_vehicle(
    vehicle_id: int,
    current_user: Annotated[User, Depends(get_current_admin_user)],
    service: VehicleService = Depends(get_vehicle_service),
) -> None:
    """Delete a vehicle.

    Args:
        vehicle_id: Vehicle ID
        current_user: Current authenticated admin user
        service: Vehicle service

    Raises:
        HTTPException: If vehicle not found or user is not admin
    """
    deleted = await service.delete_vehicle(vehicle_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vehicle not found",
        )
