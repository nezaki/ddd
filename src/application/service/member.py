from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from fastapi import Depends
from src.domain.model.member import Member
from src.infrastructure.datasource.database import get_db
from src.infrastructure.datasource.member import MemberRepository, MemberRepositoryImpl


class MemberService(ABC):
    @abstractmethod
    def create(self, member: Member) -> Member:
        raise NotImplementedError


class MemberServiceImpl(MemberService):
    def __init__(
        self,
        session: Session = Depends(get_db),
        member_repository: MemberRepository = Depends(MemberRepositoryImpl),
    ):
        self.session: Session = session
        self.member_repository = member_repository

    def create(self, project: Member) -> Member:
        return self.member_repository.create(self.session, project)
