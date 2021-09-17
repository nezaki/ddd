from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP
from sqlalchemy.schema import Column, ForeignKey

from src.infrastructure.datasource.database import Base


class Revenue(Base):
    __tablename__ = "revenue"

    id = Column(INTEGER, primary_key=True)
    project_id = Column(INTEGER, ForeignKey('project.id'))
    year_month = Column(TIMESTAMP)
    revenue = Column(INTEGER)
