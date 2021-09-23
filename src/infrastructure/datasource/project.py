from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.schema import Column
from sqlalchemy.orm import relationship, Session

from src.infrastructure.datasource.database import Base
from src.infrastructure.datasource.member_allocation import MemberAllocation  # noqa
from src.domain.model.project import Project as ProjectModel


class Project(Base):
    __tablename__ = "project"

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR)
    description = Column(VARCHAR)

    member_allocation = relationship("MemberAllocation", uselist=True, lazy="joined", innerjoin=False, viewonly=True)

    def to_entity(self) -> ProjectModel:
        return ProjectModel(
            id=self.id,
            name=self.name,
            description=self.description
        )

    @staticmethod
    def from_entity(project: ProjectModel) -> "Project":
        return Project(
            id=project.id,
            name=project.name,
            description=project.description
        )


class ProjectRepository(ABC):

    @abstractmethod
    def find(self, session: Session, skip: int = 0, limit: int = 100) -> List[ProjectModel]:
        raise NotImplementedError

    @abstractmethod
    def create(self, session: Session, project: ProjectModel) -> ProjectModel:
        raise NotImplementedError


class ProjectRepositoryImpl(ProjectRepository):

    def __init__(self):
        pass

    def find(self, session: Session, skip: int = 0, limit: int = 100) \
            -> List[ProjectModel]:
        projects = session.query(Project) \
            .order_by(Project.id) \
            .offset(skip) \
            .limit(limit) \
            .all()
        return [project.to_entity() for project in projects]

    def create(self, session: Session, project: ProjectModel) -> ProjectModel:
        project: Project = Project.from_entity(project)
        session.add(project)
        session.flush()
        return project.to_entity()
