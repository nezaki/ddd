from abc import ABC, abstractmethod
from typing import Dict, List, NoReturn, Optional

from sqlalchemy.orm import Session

from fastapi import Depends
from src.domain.model.project import Project
from src.infrastructure.datasource.database import get_db
from src.infrastructure.datasource.project import ProjectRepository, ProjectRepositoryImpl


class ProjectService(ABC):
    @abstractmethod
    def read_projects(self, skip: Optional[int], limit: Optional[int]) -> List[Project]:
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
    def delete(self, project_id: int) -> NoReturn:
        raise NotImplementedError


class ProjectServiceImpl(ProjectService):
    def __init__(
            self,
            session: Session = Depends(get_db),
            project_repository: ProjectRepository = Depends(ProjectRepositoryImpl)):
        self.session: Session = session
        self.project_repository = project_repository

    def read_projects(self, skip: Optional[int], limit: Optional[int]) -> List[Project]:
        return self.project_repository.find(self.session, skip, limit)

    def read(self, project_id: int) -> Optional[Project]:
        return self.project_repository.find_by_id(self.session, project_id)

    def create(self, project: Project) -> Project:
        return self.project_repository.create(self.session, project)

    def replace(self, project: Project, project_id: int) -> Project:
        return self.project_repository.update(self.session, project, project_id)

    def update(self, project: Dict, project_id: int) -> Project:
        stored_project = self.project_repository.find_by_id(self.session, project_id)
        return self.project_repository.update(self.session, stored_project.copy(update=project), project_id)

    def delete(self, project_id: int) -> NoReturn:
        self.project_repository.delete(self.session, project_id)
