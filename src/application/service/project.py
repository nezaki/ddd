from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from sqlalchemy.orm import Session

from fastapi import Depends
from src.domain.model.project import Project
from src.infrastructure.datasource.database import get_db
from src.infrastructure.datasource.project import ProjectRepository, ProjectRepositoryImpl


class ProjectService(ABC):
    @abstractmethod
    def read_projects(
        self, skip: int | None = 0, limit: int | None = 100
    ) -> List[Project]:
        raise NotImplementedError

    @abstractmethod
    def read(self, project_id: int) -> Optional[Project]:
        raise NotImplementedError

    @abstractmethod
    def create(self, project: Project) -> Project:
        raise NotImplementedError

    @abstractmethod
    def replace(self, project: Project, project_id: int) -> Project:
        raise NotImplementedError

    @abstractmethod
    def update(self, project: Dict, project_id: int) -> Project:
        raise NotImplementedError

    @abstractmethod
    def delete(self, project_id: int) -> None:
        raise NotImplementedError


class ProjectServiceImpl(ProjectService):
    def __init__(
        self,
        session: Session = Depends(get_db),
    ):
        self.session = session
        self.project_repository: ProjectRepository = ProjectRepositoryImpl()

    def read_projects(
        self, skip: int | None = 0, limit: int | None = 100
    ) -> List[Project]:
        return self.project_repository.find(self.session, skip, limit)

    def read(self, project_id: int) -> Optional[Project]:
        return self.project_repository.find_by_id(self.session, project_id)

    def create(self, project: Project) -> Project:
        return self.project_repository.create(self.session, project)

    def replace(self, project: Project, project_id: int) -> Project:
        return self.project_repository.update(self.session, project, project_id)

    def update(self, project: Dict, project_id: int) -> Project:
        stored_project = self.project_repository.find_by_id(self.session, project_id)
        assert stored_project is not None
        return self.project_repository.update(
            self.session, stored_project.copy(update=project), project_id
        )

    def delete(self, project_id: int) -> None:
        self.project_repository.delete(self.session, project_id)
