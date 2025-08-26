import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.main import app
from src.utils.database import get_db, create_tables
from src.core.config import settings

@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

@pytest.mark.asyncio
async def test_root_endpoint():
    """Test root endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert "Customer Management System API" in response.json()["message"]

@pytest.mark.asyncio
async def test_docs_endpoint():
    """Test API documentation endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/docs")
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_auth_endpoints_exist():
    """Test that auth endpoints are accessible"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/auth/me")
    assert response.status_code == 401  # Should require authentication

@pytest.mark.asyncio
async def test_clients_endpoints_exist():
    """Test that clients endpoints are accessible"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/clients/search")
    assert response.status_code == 401  # Should require authentication
