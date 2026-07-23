"""SQLAlchemy ORM models."""
from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """User model for authentication."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email}, is_admin={self.is_admin})>"


class Vehicle(Base):
    """Vehicle model for inventory management."""

    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<Vehicle(id={self.id}, make={self.make}, model={self.model}, quantity={self.quantity})>"
