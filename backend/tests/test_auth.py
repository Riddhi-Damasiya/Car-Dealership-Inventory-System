"""Integration tests for authentication endpoints."""
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models import User
from app.services.auth_service import verify_password


class TestUserRegistration:
    """Tests for POST /api/auth/register endpoint."""

    @pytest.mark.asyncio
    async def test_register_success(self, client: AsyncClient):
        """Test successful user registration."""
        response = await client.post(
            "/api/auth/register",
            json={"email": "newuser@example.com", "password": "password123"},
        )
        assert response.status_code == 201
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, client: AsyncClient, test_db: AsyncSession):
        """Test registration with duplicate email fails."""
        # Create a user first
        await client.post(
            "/api/auth/register",
            json={"email": "duplicate@example.com", "password": "password123"},
        )

        # Try to register with same email
        response = await client.post(
            "/api/auth/register",
            json={"email": "duplicate@example.com", "password": "password456"},
        )
        assert response.status_code in (400, 409)

    @pytest.mark.asyncio
    async def test_register_invalid_email(self, client: AsyncClient):
        """Test registration with invalid email format."""
        response = await client.post(
            "/api/auth/register",
            json={"email": "not-an-email", "password": "password123"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_password_too_short(self, client: AsyncClient):
        """Test registration with password shorter than 6 characters."""
        response = await client.post(
            "/api/auth/register",
            json={"email": "user@example.com", "password": "short"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_missing_email(self, client: AsyncClient):
        """Test registration without email."""
        response = await client.post(
            "/api/auth/register",
            json={"password": "password123"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_missing_password(self, client: AsyncClient):
        """Test registration without password."""
        response = await client.post(
            "/api/auth/register",
            json={"email": "user@example.com"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_register_user_is_not_admin_by_default(self, client: AsyncClient, test_db: AsyncSession):
        """Test that registered user is not admin by default."""
        await client.post(
            "/api/auth/register",
            json={"email": "regular@example.com", "password": "password123"},
        )

        # Query the database to verify is_admin is False
        result = await test_db.execute(
            select(User).where(User.email == "regular@example.com")
        )
        user = result.scalars().first()
        assert user is not None
        assert user.is_admin is False


class TestUserLogin:
    """Tests for POST /api/auth/login endpoint."""

    @pytest.mark.asyncio
    async def test_login_success(self, client: AsyncClient):
        """Test successful login."""
        # Register first
        await client.post(
            "/api/auth/register",
            json={"email": "login@example.com", "password": "password123"},
        )

        # Login
        response = await client.post(
            "/api/auth/login",
            json={"email": "login@example.com", "password": "password123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_invalid_email(self, client: AsyncClient):
        """Test login with non-existent email."""
        response = await client.post(
            "/api/auth/login",
            json={"email": "nonexistent@example.com", "password": "password123"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, client: AsyncClient):
        """Test login with wrong password."""
        # Register
        await client.post(
            "/api/auth/register",
            json={"email": "wrongpass@example.com", "password": "correct_password"},
        )

        # Try to login with wrong password
        response = await client.post(
            "/api/auth/login",
            json={"email": "wrongpass@example.com", "password": "wrong_password"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_login_missing_email(self, client: AsyncClient):
        """Test login without email."""
        response = await client.post(
            "/api/auth/login",
            json={"password": "password123"},
        )
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_login_missing_password(self, client: AsyncClient):
        """Test login without password."""
        response = await client.post(
            "/api/auth/login",
            json={"email": "user@example.com"},
        )
        assert response.status_code == 422


class TestProtectedRoutes:
    """Tests for protected route access control."""

    @pytest.mark.asyncio
    async def test_protected_route_requires_token(self, client: AsyncClient):
        """Test that protected routes require authentication token."""
        response = await client.get("/api/vehicles")
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_protected_route_with_invalid_token(self, client: AsyncClient):
        """Test that protected routes reject invalid tokens."""
        response = await client.get(
            "/api/vehicles",
            headers={"Authorization": "Bearer invalid_token_xyz"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_protected_route_with_valid_token(self, client: AsyncClient):
        """Test that protected routes accept valid tokens."""
        # Register and login
        register_response = await client.post(
            "/api/auth/register",
            json={"email": "protected@example.com", "password": "password123"},
        )
        token = register_response.json()["access_token"]

        # Access protected route
        response = await client.get(
            "/api/vehicles",
            headers={"Authorization": f"Bearer {token}"},
        )
        # Should not be 401 (may be 200 or other depending on implementation)
        assert response.status_code != 401


class TestPasswordHashing:
    """Tests for password hashing and verification."""

    @pytest.mark.asyncio
    async def test_password_is_hashed_not_plaintext(self, client: AsyncClient, test_db: AsyncSession):
        """Test that registered passwords are hashed, not stored as plaintext."""
        password = "my_secret_password"
        await client.post(
            "/api/auth/register",
            json={"email": "hashed@example.com", "password": password},
        )

        # Query database
        result = await test_db.execute(
            select(User).where(User.email == "hashed@example.com")
        )
        user = result.scalars().first()
        assert user is not None
        assert user.hashed_password != password
        assert len(user.hashed_password) > len(password)  # Hash is longer

    def test_verify_password_correct(self):
        """Test that verify_password returns True for correct password."""
        from app.services.auth_service import hash_password

        password = "test_password_123"
        hashed = hash_password(password)
        assert verify_password(password, hashed) is True

    def test_verify_password_incorrect(self):
        """Test that verify_password returns False for incorrect password."""
        from app.services.auth_service import hash_password

        password = "test_password_123"
        hashed = hash_password(password)
        assert verify_password("wrong_password", hashed) is False
