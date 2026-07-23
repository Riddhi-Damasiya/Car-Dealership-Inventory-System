"""Updated FastAPI application with auth routes."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.routers import auth

settings = get_settings()

app = FastAPI(
    title="Car Dealership Inventory System",
    description="A TDD-driven car dealership inventory management API",
    version="0.1.0",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
