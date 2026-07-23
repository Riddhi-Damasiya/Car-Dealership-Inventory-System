"""Integration tests for vehicle CRUD endpoints."""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import User, Vehicle


class TestVehicleCreate:
    """Tests for POST /api/vehicles endpoint."""

    @pytest.mark.asyncio
    async def test_create_vehicle_success(self, client: AsyncClient, admin_token: str):
        """Test successful vehicle creation by admin."""
        response = await client.post(
            "/api/vehicles",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "make": "Toyota",
                "model": "Camry",
                "category": "Sedan",
                "price": "25000.00",
                "quantity": 5,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["make"] == "Toyota"
        assert data["model"] == "Camry"
        assert data["category"] == "Sedan"
        assert data["price"] == "25000.00"
        assert data["quantity"] == 5
        assert "id" in data
        assert "created_at" in data

    @pytest.mark.asyncio
    async def test_create_vehicle_requires_admin(self, client: AsyncClient, user_token: str):
        """Test that non-admin users cannot create vehicles."""
        response = await client.post(
            "/api/vehicles",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "make": "Honda",
                "model": "Civic",
                "category": "Sedan",
                "price": "20000.00",
                "quantity": 3,
            },
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_create_vehicle_requires_auth(self, client: AsyncClient):
        """Test that unauthenticated requests cannot create vehicles."""
        response = await client.post(
            "/api/vehicles",
            json={
                "make": "Ford",
                "model": "Mustang",
                "category": "Sports",
                "price": "35000.00",
                "quantity": 2,
            },
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_create_vehicle_missing_field(self, client: AsyncClient, admin_token: str):
        """Test vehicle creation with missing required field."""
        response = await client.post(
            "/api/vehicles",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "make": "Tesla",
                "model": "Model 3",
                # missing category
                "price": "45000.00",
                "quantity": 1,
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_vehicle_negative_price(self, client: AsyncClient, admin_token: str):
        """Test vehicle creation with negative price."""
        response = await client.post(
            "/api/vehicles",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "make": "BMW",
                "model": "X5",
                "category": "SUV",
                "price": "-10000.00",
                "quantity": 1,
            },
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_vehicle_negative_quantity(self, client: AsyncClient, admin_token: str):
        """Test vehicle creation with negative quantity."""
        response = await client.post(
            "/api/vehicles",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "make": "Audi",
                "model": "A4",
                "category": "Sedan",
                "price": "30000.00",
                "quantity": -5,
            },
        )
        assert response.status_code == 422


class TestVehicleRead:
    """Tests for GET /api/vehicles endpoints."""

    @pytest.mark.asyncio
    async def test_list_vehicles_success(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test listing all vehicles."""
        # Create some test vehicles
        for i in range(3):
            vehicle = Vehicle(
                make="Make",
                model=f"Model{i}",
                category="Sedan",
                price="25000.00",
                quantity=i + 1,
            )
            test_db.add(vehicle)
        await test_db.commit()

        response = await client.get(
            "/api/vehicles",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) >= 3

    @pytest.mark.asyncio
    async def test_list_vehicles_requires_auth(self, client: AsyncClient):
        """Test that listing vehicles requires authentication."""
        response = await client.get("/api/vehicles")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_list_vehicles_pagination(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test vehicle listing with pagination."""
        # Create 15 vehicles
        for i in range(15):
            vehicle = Vehicle(
                make="Make",
                model=f"Model{i}",
                category="Sedan",
                price="25000.00",
                quantity=1,
            )
            test_db.add(vehicle)
        await test_db.commit()

        response = await client.get(
            "/api/vehicles?skip=0&limit=10",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data["items"]) <= 10

    @pytest.mark.asyncio
    async def test_get_vehicle_by_id_success(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test retrieving a specific vehicle by ID."""
        # Create a vehicle
        vehicle = Vehicle(
            make="Toyota",
            model="Corolla",
            category="Sedan",
            price="20000.00",
            quantity=5,
        )
        test_db.add(vehicle)
        await test_db.commit()
        await test_db.refresh(vehicle)

        response = await client.get(
            f"/api/vehicles/{vehicle.id}",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == vehicle.id
        assert data["make"] == "Toyota"
        assert data["model"] == "Corolla"

    @pytest.mark.asyncio
    async def test_get_vehicle_not_found(self, client: AsyncClient, user_token: str):
        """Test retrieving a non-existent vehicle."""
        response = await client.get(
            "/api/vehicles/99999",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 404


class TestVehicleUpdate:
    """Tests for PUT /api/vehicles/{id} endpoint."""

    @pytest.mark.asyncio
    async def test_update_vehicle_success(self, client: AsyncClient, admin_token: str, test_db: AsyncSession):
        """Test successful vehicle update by admin."""
        # Create a vehicle
        vehicle = Vehicle(
            make="Honda",
            model="Accord",
            category="Sedan",
            price="24000.00",
            quantity=3,
        )
        test_db.add(vehicle)
        await test_db.commit()
        await test_db.refresh(vehicle)

        response = await client.put(
            f"/api/vehicles/{vehicle.id}",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "make": "Honda",
                "model": "Accord",
                "category": "Sedan",
                "price": "26000.00",
                "quantity": 5,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["price"] == "26000.00"
        assert data["quantity"] == 5

    @pytest.mark.asyncio
    async def test_update_vehicle_requires_admin(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test that non-admin users cannot update vehicles."""
        # Create a vehicle
        vehicle = Vehicle(
            make="Ford",
            model="Focus",
            category="Sedan",
            price="18000.00",
            quantity=2,
        )
        test_db.add(vehicle)
        await test_db.commit()
        await test_db.refresh(vehicle)

        response = await client.put(
            f"/api/vehicles/{vehicle.id}",
            headers={"Authorization": f"Bearer {user_token}"},
            json={
                "make": "Ford",
                "model": "Focus",
                "category": "Sedan",
                "price": "19000.00",
                "quantity": 3,
            },
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_update_vehicle_not_found(self, client: AsyncClient, admin_token: str):
        """Test updating a non-existent vehicle."""
        response = await client.put(
            "/api/vehicles/99999",
            headers={"Authorization": f"Bearer {admin_token}"},
            json={
                "make": "Toyota",
                "model": "Camry",
                "category": "Sedan",
                "price": "25000.00",
                "quantity": 5,
            },
        )
        assert response.status_code == 404


class TestVehicleDelete:
    """Tests for DELETE /api/vehicles/{id} endpoint."""

    @pytest.mark.asyncio
    async def test_delete_vehicle_success(self, client: AsyncClient, admin_token: str, test_db: AsyncSession):
        """Test successful vehicle deletion by admin."""
        # Create a vehicle
        vehicle = Vehicle(
            make="Chevrolet",
            model="Cruze",
            category="Sedan",
            price="20000.00",
            quantity=2,
        )
        test_db.add(vehicle)
        await test_db.commit()
        await test_db.refresh(vehicle)
        vehicle_id = vehicle.id

        response = await client.delete(
            f"/api/vehicles/{vehicle_id}",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 204

        # Verify vehicle is deleted
        result = await test_db.execute(
            select(Vehicle).where(Vehicle.id == vehicle_id)
        )
        assert result.scalars().first() is None

    @pytest.mark.asyncio
    async def test_delete_vehicle_requires_admin(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test that non-admin users cannot delete vehicles."""
        # Create a vehicle
        vehicle = Vehicle(
            make="Nissan",
            model="Altima",
            category="Sedan",
            price="22000.00",
            quantity=3,
        )
        test_db.add(vehicle)
        await test_db.commit()
        await test_db.refresh(vehicle)

        response = await client.delete(
            f"/api/vehicles/{vehicle.id}",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 403

    @pytest.mark.asyncio
    async def test_delete_vehicle_not_found(self, client: AsyncClient, admin_token: str):
        """Test deleting a non-existent vehicle."""
        response = await client.delete(
            "/api/vehicles/99999",
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert response.status_code == 404
