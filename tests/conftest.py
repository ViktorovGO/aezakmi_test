import pytest
import asyncio
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.core import settings
from app.core import db_helper as db
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture()
async def client() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=app), base_url="https://testserver")


@pytest.fixture(autouse=True)
def fastapi_cache():
    redis = aioredis.from_url(settings.redis.redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
