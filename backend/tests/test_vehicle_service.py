"""Service layer tests for vehicle operations."""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Vehicle
from app.schemas import VehicleCreate, VehicleUpdate
from app.services.vehicle_service import VehicleService


class TestVehicleService:
    """Tests for VehicleService business logic."""

    @pytest.mark.asyncio
    async def test_create_vehicle(self, vehicle_service: VehicleService):
        """Test creating a vehicle through service."""
        vehicle_data = VehicleCreate(
            make="Toyota",
            model="Camry",
            category="Sedan",
            price="25000.00",
            quantity=5,
        )
        result = await vehicle_service.create_vehicle(vehicle_data)
        assert result.make == "Toyota"
        assert result.model == "Camry"
        assert result.price == "25000.00"
        assert result.quantity == 5

    @pytest.mark.asyncio
    async def test_create_vehicle_invalid_price(self, vehicle_service: VehicleService):
        """Test creating a vehicle with invalid price."""
        vehicle_data = VehicleCreate(
            make="Honda",
            model="Civic",
            category="Sedan",
            price="invalid",
            quantity=3,
        )
        with pytest.raises(ValueError):
            await vehicle_service.create_vehicle(vehicle_data)

    @pytest.mark.asyncio
    async def test_create_vehicle_negative_price(self, vehicle_service: VehicleService):
        """Test creating a vehicle with negative price."""
        vehicle_data = VehicleCreate(
            make="Ford",
            model="Mustang",
            category="Sports",
            price="-5000.00",
            quantity=1,
        )
        with pytest.raises(ValueError):
            await vehicle_service.create_vehicle(vehicle_data)

    @pytest.mark.asyncio
    async def test_list_vehicles(
        self, vehicle_service: VehicleService, test_db: AsyncSession
    ):
        """Test listing vehicles with pagination."""
        # Create test vehicles
        for i in range(5):
            vehicle = Vehicle(
                make="Make",
                model=f"Model{i}",
                category="Sedan",
                price="25000.00",
                quantity=i + 1,
            )
            test_db.add(vehicle)
        await test_db.commit()

        result = await vehicle_service.list_vehicles(skip=0, limit=3)
        assert len(result.items) == 3
        assert result.total >= 5
        assert result.skip == 0
        assert result.limit == 3

    @pytest.mark.asyncio
    async def test_get_vehicle(
        self, vehicle_service: VehicleService, test_db: AsyncSession
    ):
        """Test getting a specific vehicle."""
        vehicle = Vehicle(
            make="Tesla",
            model="Model 3",
            category="Electric",
            price="45000.00",
            quantity=2,
        )
        test_db.add(vehicle)
        await test_db.commit()
        await test_db.refresh(vehicle)

        result = await vehicle_service.get_vehicle(vehicle.id)
        assert result is not None
        assert result.make == "Tesla"

    @pytest.mark.asyncio
    async def test_get_vehicle_not_found(self, vehicle_service: VehicleService):
        """Test getting non-existent vehicle."""
        result = await vehicle_service.get_vehicle(99999)
        assert result is None

    @pytest.mark.asyncio
    async def test_update_vehicle(
        self, vehicle_service: VehicleService, test_db: AsyncSession
    ):
        """Test updating a vehicle."""
        vehicle = Vehicle(
            make="BMW",
            model="X5",
            category="SUV",
            price="50000.00",
            quantity=1,
        )
        test_db.add(vehicle)
        await test_db.commit()
        await test_db.refresh(vehicle)

        update_data = VehicleUpdate(
            make="BMW",
            model="X5",
            category="SUV",
            price="52000.00",
            quantity=2,
        )
        result = await vehicle_service.update_vehicle(vehicle.id, update_data)
        assert result is not None
        assert result.price == "52000.00"
        assert result.quantity == 2

    @pytest.mark.asyncio
    async def test_update_vehicle_not_found(self, vehicle_service: VehicleService):
        """Test updating non-existent vehicle."""
        update_data = VehicleUpdate(
            make="Toyota",
            model="Camry",
            category="Sedan",
            price="25000.00",
            quantity=5,
        )
        result = await vehicle_service.update_vehicle(99999, update_data)
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_vehicle(
        self, vehicle_service: VehicleService, test_db: AsyncSession
    ):
        """Test deleting a vehicle."""
        vehicle = Vehicle(
            make="Audi",
            model="A4",
            category="Sedan",
            price="40000.00",
            quantity=1,
        )
        test_db.add(vehicle)
        await test_db.commit()
        await test_db.refresh(vehicle)
        vehicle_id = vehicle.id

        result = await vehicle_service.delete_vehicle(vehicle_id)
        assert result is True

        # Verify deletion
        deleted = await vehicle_service.get_vehicle(vehicle_id)
        assert deleted is None

    @pytest.mark.asyncio
    async def test_delete_vehicle_not_found(self, vehicle_service: VehicleService):
        """Test deleting non-existent vehicle."""
        result = await vehicle_service.delete_vehicle(99999)
        assert result is False
