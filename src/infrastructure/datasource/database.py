from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import settings

engine = create_engine(settings.DATABASE_URL, pool_size=20, max_overflow=40, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():  # noqa
    db = SessionLocal()
    try:
        db.execute(f"SET search_path TO {settings.DATABASE_SCHEMA}")
        yield db
        db.commit()
    except Exception as e:
        if db:
            db.rollback()
        raise e
    finally:
        if db:
            db.close()
