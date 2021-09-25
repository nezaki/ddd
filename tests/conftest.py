from typing import Generator

import alembic
import pytest
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.main import verify_token
from src.infrastructure.datasource.database import get_db


async def override_verify_token():
    pass

app.dependency_overrides[verify_token] = override_verify_token


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://user:password@localhost:15432/postgres"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
config = Config("./tests/test_alembic.ini")


def override_get_db():
    db = TestingSessionLocal()
    try:
        schema = config.get_main_option("schema")
        db.execute(f"SET search_path TO {schema}")
        yield db
        db.commit()
    except Exception as e:
        if db:
            db.rollback()
        raise e
    finally:
        if db:
            db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def db(request):
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
