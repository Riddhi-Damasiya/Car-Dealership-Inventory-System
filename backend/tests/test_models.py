"""Unit tests for SQLAlchemy models."""
import pytest
from app.models import User, Vehicle


class TestUserModel:
    """Tests for User model."""

    def test_user_creation_with_all_fields(self):
        """Test creating a user with all fields."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_pwd_123",
            is_admin=False,
        )
        assert user.email == "test@example.com"
        assert user.hashed_password == "hashed_pwd_123"
        assert user.is_admin is False

    def test_user_is_admin_default_false(self):
        """Test that is_admin defaults to False."""
        user = User(
            email="user@example.com",
            hashed_password="hashed_pwd",
        )
        assert user.is_admin is False

    def test_user_can_be_admin(self):
        """Test creating an admin user."""
        user = User(
            email="admin@example.com",
            hashed_password="hashed_pwd",
            is_admin=True,
        )
        assert user.is_admin is True

    def test_user_repr(self):
        """Test user __repr__ method."""
        user = User(
            id=1,
            email="test@example.com",
            hashed_password="hashed_pwd",
            is_admin=False,
        )
        repr_str = repr(user)
        assert "User" in repr_str
        assert "test@example.com" in repr_str
        assert "is_admin=False" in repr_str

    def test_user_has_created_at_field(self):
        """Test that user has created_at field."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_pwd",
        )
        assert hasattr(user, "created_at")


class TestVehicleModel:
    """Tests for Vehicle model."""

    def test_vehicle_creation_with_all_fields(self):
        """Test creating a vehicle with all fields."""
        vehicle = Vehicle(
            make="Toyota",
            model="Camry",
            category="Sedan",
            price=25000.00,
            quantity=5,
        )
        assert vehicle.make == "Toyota"
        assert vehicle.model == "Camry"
        assert vehicle.category == "Sedan"
        assert vehicle.price == 25000.00
        assert vehicle.quantity == 5

    def test_vehicle_quantity_default_zero(self):
        """Test that quantity defaults to 0."""
        vehicle = Vehicle(
            make="Honda",
            model="Civic",
            category="Sedan",
            price=22000.00,
        )
        assert vehicle.quantity == 0

    def test_vehicle_price_as_decimal(self):
        """Test that price is stored as decimal."""
        vehicle = Vehicle(
            make="Ford",
            model="Mustang",
            category="Sports",
            price=45999.99,
            quantity=3,
        )
        assert vehicle.price == 45999.99

    def test_vehicle_repr(self):
        """Test vehicle __repr__ method."""
        vehicle = Vehicle(
            id=1,
            make="Tesla",
            model="Model 3",
            category="Electric",
            price=45000.00,
            quantity=10,
        )
        repr_str = repr(vehicle)
        assert "Vehicle" in repr_str
        assert "Tesla" in repr_str
        assert "Model 3" in repr_str
        assert "quantity=10" in repr_str

    def test_vehicle_has_timestamps(self):
        """Test that vehicle has created_at and updated_at fields."""
        vehicle = Vehicle(
            make="BMW",
            model="X5",
            category="SUV",
            price=60000.00,
            quantity=2,
        )
        assert hasattr(vehicle, "created_at")
        assert hasattr(vehicle, "updated_at")

    def test_vehicle_with_minimum_quantity(self):
        """Test vehicle with zero quantity."""
        vehicle = Vehicle(
            make="Audi",
            model="A4",
            category="Sedan",
            price=40000.00,
            quantity=0,
        )
        assert vehicle.quantity == 0

    def test_vehicle_with_large_quantity(self):
        """Test vehicle with large quantity."""
        vehicle = Vehicle(
            make="Mazda",
            model="CX-5",
            category="SUV",
            price=35000.00,
            quantity=999,
        )
        assert vehicle.quantity == 999

    def test_vehicle_with_high_price(self):
        """Test vehicle with high price."""
        vehicle = Vehicle(
            make="Lamborghini",
            model="Huracan",
            category="Sports",
            price=250000.00,
            quantity=1,
        )
        assert vehicle.price == 250000.00

    def test_vehicle_with_low_price(self):
        """Test vehicle with low price."""
        vehicle = Vehicle(
            make="Hyundai",
            model="Elantra",
            category="Sedan",
            price=18999.99,
            quantity=8,
        )
        assert vehicle.price == 18999.99
