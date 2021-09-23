from abc import ABC, abstractmethod
from typing import List, Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from src.domain.model.project import Project
from src.infrastructure.datasource.database import get_db
from src.infrastructure.datasource.project import ProjectRepository, ProjectRepositoryImpl


class ProjectService(ABC):
    @abstractmethod
    def read_projects(self, skip: Optional[int], limit: Optional[int]) -> List[Project]:
        raise NotImplementedError

    @abstractmethod
    def create(self, project: Project) -> Project:
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

    def create(self, project: Project) -> Project:
        return self.project_repository.create(self.session, project)
