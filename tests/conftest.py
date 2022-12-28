from typing import AsyncGenerator

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.config import get_settings
from src.infrastructure.datasource.database import get_db
from src.main import app, verify_token


async def override_verify_token() -> None:
    pass


app.dependency_overrides[verify_token] = override_verify_token


# async def override_get_db():  # noqa
#     db = async_session()
#     try:
#         schema = config.get_main_option("schema")
#         db.execute(f"SET search_path TO {schema}")
#         yield db
#         db.commit()
#     except Exception as e:
#         if db:
#             db.rollback()
#         raise e
#     finally:
#         if db:
#             db.close()

app.dependency_overrides[get_db] = lambda: None


@pytest_asyncio.fixture(scope="function")
async def session() -> AsyncGenerator:
    async_engine = create_async_engine(get_settings().DATABASE_URL, echo=False)

    AsyncSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession,
        future=True,
    )

    async with AsyncSessionLocal.begin() as async_session:
        yield async_session
        await async_session.commit()
        await async_session.close()


@pytest_asyncio.fixture
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="https://test") as async_client:
        yield async_client
