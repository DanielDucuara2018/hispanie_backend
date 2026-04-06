import logging
from unittest import mock

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
async def mock_session():
    from hispanie.model.base import Base

    engine = create_async_engine(
        "postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/hispanie_test"
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)

    with mock.patch("hispanie.db.async_session_factory", session_factory):
        yield session_factory

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest.fixture
@mock.patch("hispanie.db.initialize")
async def client(func_initialize):
    def mock_initialize(value):
        return value

    func_initialize.side_effect = mock_initialize

    from hispanie.api.api import app

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
