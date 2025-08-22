from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager
import uvicorn

from src.api.routes import auth, clients
from src.utils.database import create_tables
from src.core.config import settings
from src.api.services.cache_service import cache_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("Starting up...")
    await create_tables()
    
    # Check Redis connection
    if not await cache_service.health_check():
        print("Warning: Redis connection failed")
    else:
        print("Redis connected successfully")
    
    yield
    
    # Shutdown
    print("Shutting down...")
    await cache_service.redis_client.close()

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Customer Management System API",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)

# Include routers
app.include_router(auth.router)
app.include_router(clients.router)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    redis_health = await cache_service.health_check()
    return {
        "status": "healthy",
        "redis": "connected" if redis_health else "disconnected",
        "version": settings.VERSION
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Customer Management System API",
        "version": settings.VERSION,
        "docs": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
