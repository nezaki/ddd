import os
from typing import AsyncGenerator

import pytest_asyncio
from alembic.config import Config
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from alembic import command
from src.config import get_settings
from src.infrastructure.datasource.database import get_db_async
from src.main import app, verify_token

app.dependency_overrides[verify_token] = lambda: None
app.dependency_overrides[get_db_async] = lambda: None


_path = os.path.dirname(__file__)
__config_path__ = _path + "/alembic-test.ini"
__migration_path__ = _path + "/../alembic/dev/"

cfg = Config(__config_path__)
cfg.set_main_option("script_location", __migration_path__)


def __execute_downgrade(connection: AsyncSession) -> None:
    cfg.attributes["connection"] = connection
    command.downgrade(cfg, "base")


def __execute_upgrade(connection: AsyncSession) -> None:
    cfg.attributes["connection"] = connection
    command.upgrade(cfg, "head")


async def migrate_db(conn_url: str) -> None:
    async_engine = create_async_engine(conn_url, echo=False)
    async with async_engine.begin() as conn:
        await conn.execute(
            text(f"CREATE SCHEMA IF NOT EXISTS {get_settings().DATABASE_SCHEMA}")
        )
        await conn.execute(text(f"SET search_path TO {get_settings().DATABASE_SCHEMA}"))
        await conn.run_sync(__execute_downgrade)
        await conn.run_sync(__execute_upgrade)


@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncGenerator:
    await migrate_db(get_settings().DATABASE_URL)

    async_engine = create_async_engine(get_settings().DATABASE_URL, echo=False)

    AsyncSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
        future=True,
    )

    async with AsyncSessionLocal.begin() as async_session:
        await async_session.execute(
            f"SET search_path TO {get_settings().DATABASE_SCHEMA}"
        )
        yield async_session
        await async_session.commit()
        await async_session.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="https://test") as async_client:
        yield async_client
