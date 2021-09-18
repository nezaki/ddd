from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.schema import Column

from src.infrastructure.datasource.database import Base
from src.infrastructure.datasource._crud_base import CRUDBase
from src.presentation.schema.member import MemberCreate, MemberUpdate


class Member(Base):
    __tablename__ = "member"

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR)
    cost = Column(INTEGER)
    cost_type = Column(VARCHAR)


class MemberRepository(CRUDBase[Member, MemberCreate, MemberUpdate]):
    pass


member_repository = MemberRepository(Member)
