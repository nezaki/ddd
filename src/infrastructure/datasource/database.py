from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import get_settings

engine = create_async_engine(
    get_settings().DATABASE_URL, pool_size=2, max_overflow=4, echo=False
)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

Base = declarative_base()


async def get_db():  # noqa
    db = SessionLocal()
    try:
        db.execute(f"SET search_path TO {get_settings().DATABASE_SCHEMA}")
        yield db
        db.commit()
    except Exception as e:
        if db:
            db.rollback()
        raise e
    finally:
        if db:
            db.close()
