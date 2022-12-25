from sqlalchemy.dialects.postgresql import INTEGER, NUMERIC, TIMESTAMP, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey

from src.infrastructure.datasource.database import Base


class MemberAllocation(Base):
    __tablename__ = "member_allocation"

    id = Column(INTEGER, primary_key=True)
    project_id = Column(INTEGER, ForeignKey("project.id"))
    member_id = Column(INTEGER, ForeignKey("member.id"))
    year_month = Column(TIMESTAMP)
    quantity = Column(NUMERIC)
    status = Column(VARCHAR)

    project = relationship(
        "Project", uselist=False, lazy="joined", innerjoin=True, viewonly=True
    )
