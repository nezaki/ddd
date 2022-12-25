from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy.dialects.postgresql import INTEGER, VARCHAR
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.schema import Column

from src.domain.model.project import Project as ProjectModel
from src.infrastructure.datasource.database import Base
from src.infrastructure.datasource.member_allocation import MemberAllocation  # noqa


class Project(Base):
    __tablename__ = "project"

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR)
    description = Column(VARCHAR)

    # member_allocation = relationship("MemberAllocation", uselist=True, lazy="joined", innerjoin=False, viewonly=True)

    def to_entity(self) -> ProjectModel:
        return ProjectModel(id=self.id, name=self.name, description=self.description)

    @staticmethod
    def from_entity(project: ProjectModel) -> "Project":
        return Project(
            id=project.id, name=project.name, description=project.description
        )


class ProjectRepository(ABC):
    @abstractmethod
    def find(
        self, session: Session, skip: int | None = 0, limit: int | None = 100
    ) -> List[ProjectModel]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, session: Session, project_id: int) -> Optional[ProjectModel]:
        raise NotImplementedError

    @abstractmethod
    def create(self, session: Session, project: ProjectModel) -> ProjectModel:
        raise NotImplementedError

    @abstractmethod
    def update(
        self, session: Session, project: ProjectModel, project_id: int
    ) -> ProjectModel:
        raise NotImplementedError

    @abstractmethod
    def delete(self, session: Session, project_id: int) -> None:
        raise NotImplementedError


class ProjectRepositoryImpl(ProjectRepository):
    def find(
        self, session: Session, skip: int | None = 0, limit: int | None = 100
    ) -> List[ProjectModel]:
        projects = (
            session.query(Project).order_by(Project.id).offset(skip).limit(limit).all()
        )
        return [project.to_entity() for project in projects]

    def find_by_id(self, session: Session, project_id: int) -> Optional[ProjectModel]:
        try:
            project: Project = session.query(Project).filter_by(id=project_id).one()
            return project.to_entity()
        except NoResultFound:
            return None
        except Exception as e:
            raise e

    def create(self, session: Session, project: ProjectModel) -> ProjectModel:
        _project: Project = Project.from_entity(project)
        session.add(_project)
        session.flush()
        return _project.to_entity()

    def update(
        self, session: Session, project: ProjectModel, project_id: int
    ) -> ProjectModel:
        _project: Project = session.query(Project).filter_by(id=project_id).one()
        _project.name = project.name
        _project.description = project.description
        return _project.to_entity()

    def delete(self, session: Session, project_id: int) -> None:
        session.query(Project).filter_by(id=project_id).delete()
