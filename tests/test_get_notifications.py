import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient


@pytest_asyncio.fixture()
async def created_notification(client: AsyncClient):
    response = await client.post(
        "/api/v1/notifications/",
        json={
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
            "title": "INFO",
            "text": "ERROR in the system",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["processing_status"] == "pending"

    timeout = 10
    interval = 0.5  # интервал между проверками
    elapsed_time = 0
    while elapsed_time < timeout:
        await asyncio.sleep(interval)
        elapsed_time += interval
        response = await client.get(f"/api/v1/notifications/check/{data["id"]}")
        check_data = response.json()
        if check_data["processing_status"] == "completed":
            break
    else:
        pytest.fail("AI обработка не завершилась за отведенное время")

    yield data["id"]

    response = await client.delete(f"/api/v1/notifications/{data['id']}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_notifications(client: AsyncClient, created_notification: str):
    response = await client.get("/api/v1/notifications/")
    assert response.status_code == 200
    data = response.json()
    assert any(
        notific["id"] == created_notification for notific in data["notifications"]
    )


@pytest.mark.asyncio
async def test_get_notification(client: AsyncClient, created_notification: str):
    response = await client.get(f"/api/v1/notifications/{created_notification}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_create_invalid_notification(client: AsyncClient):
    response = await client.post(
        "/api/v1/notifications/",
        json={
            "user_id": "123",
            "title": "INFO",
            "text": "ERROR in the system",
        },
    )
    assert response.status_code == 422

    response = await client.post(
        "/api/v1/notifications/",
        json={
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
            "text": "ERROR in the system",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_paginating_notification(client: AsyncClient):
    response = await client.get(
        "/api/v1/notifications/", params={"limit": 3, "offset": 0}
    )
    assert response.status_code == 200
    assert len(response.json()["notifications"]) <= 3

    response = await client.get(
        "/api/v1/notifications/", params={"limit": -5, "offset": 0}
    )
    assert response.status_code == 422
