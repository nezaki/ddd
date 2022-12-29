from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import get_settings

Base = declarative_base()

async_engine = create_async_engine(get_settings().DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession,
    future=True,
)


async def get_db_async() -> AsyncGenerator:
    async with AsyncSessionLocal.begin() as async_session:
        try:
            await async_session.execute(
                f"SET search_path TO {get_settings().DATABASE_SCHEMA}"
            )
            yield async_session
            await async_session.commit()
        except Exception:
            await async_session.rollback()
        finally:
            await async_session.close()
