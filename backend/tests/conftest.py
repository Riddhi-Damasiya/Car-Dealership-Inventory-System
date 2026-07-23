"""Pytest configuration and fixtures."""
import asyncio
import os
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import get_db
from app.main import app
from app.models import Base


# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """Create test database and return session."""
    engine = create_async_engine(
        SQLALCHEMY_TEST_DATABASE_URL,
        echo=False,
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    TestingSessionLocal = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        future=True,
    )

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create test client with test database."""

    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
