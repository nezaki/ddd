from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, NUMERIC
from sqlalchemy.schema import Column, ForeignKey

from src.infrastructure.datasource.database import Base


class Estimate(Base):
    __tablename__ = "estimate"

    id = Column(INTEGER, primary_key=True)
    project_id = Column(INTEGER, ForeignKey('project.id'))
    member_id = Column(INTEGER, ForeignKey('member.id'))
    year_month = Column(TIMESTAMP)
    quantity = Column(NUMERIC)
