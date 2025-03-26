import pytest
import pytest_asyncio
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_notifications(client: AsyncClient):
    response = await client.get("/api/v1/notifications/")
    assert response.status_code == 200


@pytest_asyncio.fixture
async def created_notification(client: AsyncClient) -> str:
    """Создаёт тестовое уведомление и возвращает его ID."""
    response = await client.post(
        "/api/v1/notifications/",
        json={
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
            "title": "INFO",
            "text": "ERROR in the system",
        },
    )
    assert response.status_code == 200
    return response.json()["id"]


@pytest.mark.asyncio
async def test_get_notification(client: AsyncClient, created_notification: str):
    response = await client.get(f"/api/v1/notifications/{created_notification}")
    assert response.status_code == 200
