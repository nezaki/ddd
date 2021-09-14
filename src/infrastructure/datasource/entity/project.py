from sqlalchemy import Column, Integer, String

from src.infrastructure.datasource.database import Base


class Project(Base):
    __tablename__ = "project"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
