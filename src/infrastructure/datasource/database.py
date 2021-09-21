from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://user:password@localhost:15432/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=20, max_overflow=40, echo=False)
engine.execute("SET search_path TO ddd")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        db.execute(f"SET search_path TO ddd")
        yield db
        db.commit()
    except Exception as e:
        if db:
            db.rollback()
        raise e
    finally:
        if db:
            db.close()
