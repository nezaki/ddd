from abc import ABC, abstractmethod

from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship, Session

from src.infrastructure.datasource.database import Base
from src.domain.model.member import Member as MemberModel


class Member(Base):
    __tablename__ = "member"

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR)
    cost = Column(INTEGER)
    cost_type = Column(VARCHAR)

    def to_entity(self) -> MemberModel:
        return MemberModel(
            id=self.id,
            name=self.name,
            cost=self.cost,
            cost_type=self.cost_type,
        )

    @staticmethod
    def from_entity(member: MemberModel) -> "Member":
        return Member(
            id=member.id,
            name=member.name,
            cost=member.cost,
            cost_type=member.cost_type.value,
        )


class MemberRepository(ABC):
    @abstractmethod
    def create(self, session: Session, member: MemberModel) -> MemberModel:
        raise NotImplementedError


class MemberRepositoryImpl(MemberRepository):
    def __init__(self):
        pass

    def create(self, session: Session, member: MemberModel) -> MemberModel:
        member: Member = Member.from_entity(member)
        session.add(member)
        session.flush()
        return member.to_entity()
