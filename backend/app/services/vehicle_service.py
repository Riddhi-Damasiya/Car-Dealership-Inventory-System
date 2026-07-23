"""Vehicle service layer for business logic."""
from decimal import Decimal, InvalidOperation

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_

from app.models import Vehicle
from app.schemas import (
    VehicleCreate,
    VehicleListResponse,
    VehicleResponse,
    VehicleUpdate,
    PurchaseRequest,
    RestockRequest,
    PurchaseResponse,
    RestockResponse,
)


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

    async def search_vehicles(
        self,
        make: str | None = None,
        model: str | None = None,
        category: str | None = None,
        min_price: str | None = None,
        max_price: str | None = None,
    ) -> list[VehicleResponse]:
        """Search and filter vehicles based on criteria.

        All parameters are optional. When multiple filters are provided,
        they are combined with AND logic (all must match).

        Args:
            make: Filter by vehicle manufacturer (case-insensitive partial match)
            model: Filter by vehicle model (case-insensitive partial match)
            category: Filter by vehicle category (case-insensitive partial match)
            min_price: Filter by minimum price (inclusive)
            max_price: Filter by maximum price (inclusive)

        Returns:
            List of vehicles matching all filter criteria

        Raises:
            ValueError: If price parameters are invalid
        """
        # Build dynamic WHERE clause with all filters
        filters = []

        if make:
            filters.append(func.lower(Vehicle.make).contains(make.lower()))

        if model:
            filters.append(func.lower(Vehicle.model).contains(model.lower()))

        if category:
            filters.append(func.lower(Vehicle.category).contains(category.lower()))

        # Validate and apply price filters
        if min_price is not None:
            try:
                min_price_decimal = Decimal(min_price)
                if min_price_decimal < 0:
                    raise ValueError("Minimum price must be non-negative")
                filters.append(Vehicle.price >= min_price_decimal)
            except (InvalidOperation, ValueError) as e:
                raise ValueError(f"Invalid minimum price: {e}")

        if max_price is not None:
            try:
                max_price_decimal = Decimal(max_price)
                if max_price_decimal < 0:
                    raise ValueError("Maximum price must be non-negative")
                filters.append(Vehicle.price <= max_price_decimal)
            except (InvalidOperation, ValueError) as e:
                raise ValueError(f"Invalid maximum price: {e}")

        # Execute query with combined filters
        query = select(Vehicle).order_by(Vehicle.id)
        if filters:
            query = query.where(and_(*filters))

        result = await self.db.execute(query)
        vehicles = result.scalars().all()

        return [VehicleResponse.model_validate(v) for v in vehicles]

    async def purchase_vehicle(
        self, vehicle_id: int, purchase_data: PurchaseRequest
    ) -> PurchaseResponse:
        """Purchase a vehicle by decrementing its quantity.

        Args:
            vehicle_id: Vehicle ID
            purchase_data: Purchase request with quantity

        Returns:
            Purchase confirmation response

        Raises:
            ValueError: If vehicle not found or insufficient stock
        """
        vehicle = await self.get_vehicle(vehicle_id)
        if not vehicle:
            raise ValueError(f"Vehicle with ID {vehicle_id} not found")

        if vehicle.quantity < purchase_data.quantity:
            raise ValueError(
                f"Insufficient stock. Available: {vehicle.quantity}, "
                f"Requested: {purchase_data.quantity}"
            )

        # Calculate total price
        total_price = Decimal(vehicle.price) * Decimal(purchase_data.quantity)

        # Decrement quantity
        vehicle.quantity -= purchase_data.quantity

        await self.db.commit()
        await self.db.refresh(vehicle)

        return PurchaseResponse(
            vehicle_id=vehicle.id,
            quantity_purchased=purchase_data.quantity,
            total_price=str(total_price),
            remaining_quantity=vehicle.quantity,
            message=f"Successfully purchased {purchase_data.quantity} "
            f"{vehicle.make} {vehicle.model}(s). Total: ${total_price}",
        )

    async def restock_vehicle(
        self, vehicle_id: int, restock_data: RestockRequest
    ) -> RestockResponse:
        """Restock a vehicle by incrementing its quantity.

        Args:
            vehicle_id: Vehicle ID
            restock_data: Restock request with quantity

        Returns:
            Restock confirmation response

        Raises:
            ValueError: If vehicle not found
        """
        vehicle = await self.get_vehicle(vehicle_id)
        if not vehicle:
            raise ValueError(f"Vehicle with ID {vehicle_id} not found")

        # Increment quantity
        vehicle.quantity += restock_data.quantity

        await self.db.commit()
        await self.db.refresh(vehicle)

        return RestockResponse(
            vehicle_id=vehicle.id,
            quantity_added=restock_data.quantity,
            new_quantity=vehicle.quantity,
            message=f"Successfully restocked {restock_data.quantity} "
            f"{vehicle.make} {vehicle.model}(s). New quantity: {vehicle.quantity}",
        )
