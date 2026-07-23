"""Vehicle service layer for business logic."""
from decimal import Decimal, InvalidOperation

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func

from app.models import Vehicle
from app.schemas import VehicleCreate, VehicleListResponse, VehicleResponse, VehicleUpdate


class VehicleService:
    """Service class for vehicle operations."""

    def __init__(self, db: AsyncSession):
        """Initialize vehicle service.

        Args:
            db: AsyncSession database instance
        """
        self.db = db

    @staticmethod
    def _validate_price(price: str) -> None:
        """Validate price is a valid positive decimal.

        Args:
            price: Price string to validate

        Raises:
            ValueError: If price is invalid or negative
        """
        try:
            price_decimal = Decimal(price)
            if price_decimal < 0:
                raise ValueError("Price must be non-negative")
        except (InvalidOperation, ValueError) as e:
            raise ValueError(f"Invalid price: {e}")

    async def create_vehicle(self, vehicle_data: VehicleCreate) -> VehicleResponse:
        """Create a new vehicle.

        Args:
            vehicle_data: Vehicle creation data

        Returns:
            Created vehicle response

        Raises:
            ValueError: If validation fails
        """
        self._validate_price(vehicle_data.price)

        new_vehicle = Vehicle(
            make=vehicle_data.make,
            model=vehicle_data.model,
            category=vehicle_data.category,
            price=vehicle_data.price,
            quantity=vehicle_data.quantity,
        )
        self.db.add(new_vehicle)
        await self.db.commit()
        await self.db.refresh(new_vehicle)
        return VehicleResponse.model_validate(new_vehicle)

    async def list_vehicles(
        self, skip: int = 0, limit: int = 10
    ) -> VehicleListResponse:
        """List all vehicles with pagination.

        Args:
            skip: Number of items to skip
            limit: Maximum items to return

        Returns:
            Paginated list of vehicles
        """
        # Get total count
        count_result = await self.db.execute(select(func.count(Vehicle.id)))
        total = count_result.scalar() or 0

        # Get vehicles with pagination
        result = await self.db.execute(
            select(Vehicle).offset(skip).limit(limit).order_by(Vehicle.id)
        )
        vehicles = result.scalars().all()

        return VehicleListResponse(
            items=[VehicleResponse.model_validate(v) for v in vehicles],
            total=total,
            skip=skip,
            limit=limit,
        )

    async def get_vehicle(self, vehicle_id: int) -> Vehicle | None:
        """Get a vehicle by ID.

        Args:
            vehicle_id: Vehicle ID

        Returns:
            Vehicle or None if not found
        """
        result = await self.db.execute(
            select(Vehicle).where(Vehicle.id == vehicle_id)
        )
        return result.scalars().first()

    async def update_vehicle(
        self, vehicle_id: int, vehicle_data: VehicleUpdate
    ) -> Vehicle | None:
        """Update a vehicle.

        Args:
            vehicle_id: Vehicle ID
            vehicle_data: Updated vehicle data

        Returns:
            Updated vehicle or None if not found

        Raises:
            ValueError: If validation fails
        """
        self._validate_price(vehicle_data.price)

        vehicle = await self.get_vehicle(vehicle_id)
        if not vehicle:
            return None

        vehicle.make = vehicle_data.make
        vehicle.model = vehicle_data.model
        vehicle.category = vehicle_data.category
        vehicle.price = vehicle_data.price
        vehicle.quantity = vehicle_data.quantity

        await self.db.commit()
        await self.db.refresh(vehicle)
        return vehicle

    async def delete_vehicle(self, vehicle_id: int) -> bool:
        """Delete a vehicle.

        Args:
            vehicle_id: Vehicle ID

        Returns:
            True if deleted, False if not found
        """
        vehicle = await self.get_vehicle(vehicle_id)
        if not vehicle:
            return False

        await self.db.delete(vehicle)
        await self.db.commit()
        return True
