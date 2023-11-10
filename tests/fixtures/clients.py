from dataclasses import dataclass
from typing import Optional

import aiohttp
import aioredis
import pytest
from multidict import CIMultiDictProxy

import json
from settings import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture
async def redis_client():
    redis = await aioredis.create_redis_pool((settings.REDIS_HOST, settings.REDIS_PORT), minsize=10, maxsize=20)
    yield redis
    redis.close()
    await redis.wait_closed()


@pytest.fixture
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = f'{settings.SERVICE_URL}:{settings.SERVICE_PORT}' + '/api/v1' + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner


@pytest.fixture
def make_post_request(session):
    async def inner(method: str, data: Optional[dict] = None) -> HTTPResponse:
        url = f'{settings.SERVICE_URL}:{settings.SERVICE_PORT}' + '/api/v1' + method
        async with session.post(url, data=data) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )
    return inner


@pytest.fixture
async def session_db():
    engine = create_async_engine("postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}".format(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        db_name=settings.DB_NAME,
    ), echo=True, future=True)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False,
    )
    yield async_session
    async_session.close_all()
