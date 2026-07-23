"""Integration tests for vehicle search endpoint."""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Vehicle


class TestVehicleSearch:
    """Tests for GET /api/vehicles/search endpoint."""

    @pytest.mark.asyncio
    async def test_search_by_make(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test searching vehicles by make."""
        # Create test vehicles
        vehicles = [
            Vehicle(make="Toyota", model="Camry", category="Sedan", price="25000.00", quantity=5),
            Vehicle(make="Toyota", model="Corolla", category="Sedan", price="20000.00", quantity=3),
            Vehicle(make="Honda", model="Civic", category="Sedan", price="22000.00", quantity=2),
        ]
        for vehicle in vehicles:
            test_db.add(vehicle)
        await test_db.commit()

        response = await client.get(
            "/api/vehicles/search?make=Toyota",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(v["make"] == "Toyota" for v in data)

    @pytest.mark.asyncio
    async def test_search_by_model(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test searching vehicles by model."""
        vehicles = [
            Vehicle(make="Toyota", model="Camry", category="Sedan", price="25000.00", quantity=5),
            Vehicle(make="Honda", model="Camry", category="Sedan", price="24000.00", quantity=2),
            Vehicle(make="Toyota", model="Corolla", category="Sedan", price="20000.00", quantity=3),
        ]
        for vehicle in vehicles:
            test_db.add(vehicle)
        await test_db.commit()

        response = await client.get(
            "/api/vehicles/search?model=Camry",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(v["model"] == "Camry" for v in data)

    @pytest.mark.asyncio
    async def test_search_by_category(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test searching vehicles by category."""
        vehicles = [
            Vehicle(make="Toyota", model="Camry", category="Sedan", price="25000.00", quantity=5),
            Vehicle(make="Honda", model="Civic", category="Sedan", price="22000.00", quantity=2),
            Vehicle(make="Ford", model="Mustang", category="Sports", price="35000.00", quantity=1),
        ]
        for vehicle in vehicles:
            test_db.add(vehicle)
        await test_db.commit()

        response = await client.get(
            "/api/vehicles/search?category=Sedan",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(v["category"] == "Sedan" for v in data)

    @pytest.mark.asyncio
    async def test_search_by_price_range(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test searching vehicles by price range."""
        vehicles = [
            Vehicle(make="Toyota", model="Camry", category="Sedan", price="25000.00", quantity=5),
            Vehicle(make="Honda", model="Civic", category="Sedan", price="22000.00", quantity=2),
            Vehicle(make="Ford", model="Mustang", category="Sports", price="35000.00", quantity=1),
        ]
        for vehicle in vehicles:
            test_db.add(vehicle)
        await test_db.commit()

        response = await client.get(
            "/api/vehicles/search?min_price=23000.00&max_price=30000.00",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["make"] == "Toyota"
        assert data[0]["price"] == "25000.00"

    @pytest.mark.asyncio
    async def test_search_multiple_filters(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test searching vehicles with multiple filters combined."""
        vehicles = [
            Vehicle(make="Toyota", model="Camry", category="Sedan", price="25000.00", quantity=5),
            Vehicle(make="Toyota", model="Corolla", category="Sedan", price="20000.00", quantity=3),
            Vehicle(make="Honda", model="Civic", category="Sedan", price="22000.00", quantity=2),
        ]
        for vehicle in vehicles:
            test_db.add(vehicle)
        await test_db.commit()

        response = await client.get(
            "/api/vehicles/search?make=Toyota&category=Sedan&min_price=20000.00",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(v["make"] == "Toyota" and v["category"] == "Sedan" for v in data)

    @pytest.mark.asyncio
    async def test_search_empty_result(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test search returning no results."""
        vehicles = [
            Vehicle(make="Toyota", model="Camry", category="Sedan", price="25000.00", quantity=5),
        ]
        for vehicle in vehicles:
            test_db.add(vehicle)
        await test_db.commit()

        response = await client.get(
            "/api/vehicles/search?make=NonExistent",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data == []

    @pytest.mark.asyncio
    async def test_search_no_filters_returns_all(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test search with no filters returns all vehicles."""
        vehicles = [
            Vehicle(make="Toyota", model="Camry", category="Sedan", price="25000.00", quantity=5),
            Vehicle(make="Honda", model="Civic", category="Sedan", price="22000.00", quantity=2),
            Vehicle(make="Ford", model="Mustang", category="Sports", price="35000.00", quantity=1),
        ]
        for vehicle in vehicles:
            test_db.add(vehicle)
        await test_db.commit()

        response = await client.get(
            "/api/vehicles/search",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    @pytest.mark.asyncio
    async def test_search_requires_auth(self, client: AsyncClient):
        """Test that search endpoint requires authentication."""
        response = await client.get("/api/vehicles/search")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_search_case_insensitive_make(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test that search is case-insensitive for make."""
        vehicle = Vehicle(make="Toyota", model="Camry", category="Sedan", price="25000.00", quantity=5)
        test_db.add(vehicle)
        await test_db.commit()

        response = await client.get(
            "/api/vehicles/search?make=toyota",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["make"] == "Toyota"

    @pytest.mark.asyncio
    async def test_search_case_insensitive_model(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test that search is case-insensitive for model."""
        vehicle = Vehicle(make="Toyota", model="Camry", category="Sedan", price="25000.00", quantity=5)
        test_db.add(vehicle)
        await test_db.commit()

        response = await client.get(
            "/api/vehicles/search?model=CAMRY",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["model"] == "Camry"

    @pytest.mark.asyncio
    async def test_search_partial_match_make(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test that search supports partial matching for make."""
        vehicles = [
            Vehicle(make="Toyota", model="Camry", category="Sedan", price="25000.00", quantity=5),
            Vehicle(make="Toyotas", model="Corolla", category="Sedan", price="20000.00", quantity=3),
            Vehicle(make="Honda", model="Civic", category="Sedan", price="22000.00", quantity=2),
        ]
        for vehicle in vehicles:
            test_db.add(vehicle)
        await test_db.commit()

        response = await client.get(
            "/api/vehicles/search?make=oyot",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

    @pytest.mark.asyncio
    async def test_search_invalid_min_price(self, client: AsyncClient, user_token: str):
        """Test search with invalid minimum price."""
        response = await client.get(
            "/api/vehicles/search?min_price=invalid",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_search_invalid_max_price(self, client: AsyncClient, user_token: str):
        """Test search with invalid maximum price."""
        response = await client.get(
            "/api/vehicles/search?max_price=invalid",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_search_negative_min_price(self, client: AsyncClient, user_token: str):
        """Test search with negative minimum price."""
        response = await client.get(
            "/api/vehicles/search?min_price=-1000.00",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_search_negative_max_price(self, client: AsyncClient, user_token: str):
        """Test search with negative maximum price."""
        response = await client.get(
            "/api/vehicles/search?max_price=-1000.00",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_search_min_price_only(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test search with only minimum price filter."""
        vehicles = [
            Vehicle(make="Toyota", model="Camry", category="Sedan", price="25000.00", quantity=5),
            Vehicle(make="Honda", model="Civic", category="Sedan", price="22000.00", quantity=2),
            Vehicle(make="Ford", model="Mustang", category="Sports", price="35000.00", quantity=1),
        ]
        for vehicle in vehicles:
            test_db.add(vehicle)
        await test_db.commit()

        response = await client.get(
            "/api/vehicles/search?min_price=23000.00",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(float(v["price"]) >= 23000.00 for v in data)

    @pytest.mark.asyncio
    async def test_search_max_price_only(self, client: AsyncClient, user_token: str, test_db: AsyncSession):
        """Test search with only maximum price filter."""
        vehicles = [
            Vehicle(make="Toyota", model="Camry", category="Sedan", price="25000.00", quantity=5),
            Vehicle(make="Honda", model="Civic", category="Sedan", price="22000.00", quantity=2),
            Vehicle(make="Ford", model="Mustang", category="Sports", price="35000.00", quantity=1),
        ]
        for vehicle in vehicles:
            test_db.add(vehicle)
        await test_db.commit()

        response = await client.get(
            "/api/vehicles/search?max_price=25000.00",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(float(v["price"]) <= 25000.00 for v in data)
