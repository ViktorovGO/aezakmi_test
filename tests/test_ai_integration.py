import pytest
import asyncio
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_ai_categorization(client: AsyncClient):
    response = await client.post(
        "/api/v1/notifications/",
        json={
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
            "title": "Critical Alert",
            "text": "ERROR in system",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["processing_status"] == "pending"
    check_data = {"processing_status": "pending"}
 
    timeout = 10  
    interval = 0.5  # интервал между проверками
    elapsed_time = 0
    while elapsed_time < timeout:
        await asyncio.sleep(interval)
        elapsed_time += interval
        response = await client.get(f"/api/v1/notifications/check/{data['id']}")
        check_data = response.json()
        if check_data["processing_status"] == "completed":
            break
    else:
        pytest.fail("AI обработка не завершилась за отведенное время")

    response = await client.get(f"/api/v1/notifications/{data['id']}")
    data = response.json()
    assert data["processing_status"] == "completed"
    assert data["category"] == "critical"

    response = await client.delete(f"/api/v1/notifications/{data['id']}")
    assert response.status_code == 200
