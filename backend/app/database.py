"""Database configuration and session management."""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_settings

settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    future=True,
    pool_pre_ping=True,
)

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    future=True,
)


async def get_db() -> AsyncSession:
    """Dependency to get database session."""
    async with AsyncSessionLocal() as session:
        yield session
