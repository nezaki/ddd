from abc import ABC, abstractmethod
from typing import List, Optional

from fastapi import Depends, Query
from sqlalchemy.orm import Session

from src.infrastructure.datasource.database import get_db
from src.infrastructure.datasource.project import project_repository, Project


class ProjectService(ABC):
    @abstractmethod
    def read_projects(self, skip: Optional[int], limit: Optional[int]) -> List[Project]:
        raise NotImplementedError


class ProjectServiceImpl(ProjectService):
    def __init__(self, session: Session):
        self.session: Session = session

    def read_projects(self, skip: Optional[int], limit: Optional[int]) -> List[Project]:
        projects = project_repository.get_multi(self.session, skip=skip, limit=limit)
        return projects
