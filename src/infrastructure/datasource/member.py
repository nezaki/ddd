from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.schema import Column

from src.infrastructure.datasource.database import Base


class Member(Base):
    __tablename__ = "member"

    id = Column(INTEGER, primary_key=True)
    cost = Column(INTEGER)
    calculation_type = Column(VARCHAR)
