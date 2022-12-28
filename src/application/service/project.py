from abc import ABC, abstractmethod
from typing import Dict, List

from src.domain.model.project import Project as ProjectModel
from src.infrastructure.datasource.database import get_db
from src.infrastructure.datasource.repository import project as project_repository


class ProjectService(ABC):
    @abstractmethod
    def read_projects(
        self, skip: int | None = 0, limit: int | None = 100
    ) -> List[ProjectModel]:
        raise NotImplementedError

    @abstractmethod
    def read(self, project_id: int) -> ProjectModel | None:
        raise NotImplementedError

    @abstractmethod
    def create(self, project: ProjectModel) -> ProjectModel:
        raise NotImplementedError

    @abstractmethod
    def replace(self, project: ProjectModel, project_id: int) -> ProjectModel:
        raise NotImplementedError

    @abstractmethod
    def update(self, project: Dict, project_id: int) -> ProjectModel:
        raise NotImplementedError

    @abstractmethod
    def delete(self, project_id: int) -> None:
        raise NotImplementedError


class ProjectServiceImpl(ProjectService):
    def __init__(self):
        self.session = get_db()

    def read_projects(
        self, skip: int | None = 0, limit: int | None = 100
    ) -> List[ProjectModel]:
        return project_repository.find(self.session, skip, limit)

    def read(self, project_id: int) -> ProjectModel | None:
        return project_repository.find_by_id(self.session, project_id)

    def create(self, project: ProjectModel) -> ProjectModel:
        return project_repository.create(self.session, project)

    def replace(self, project: ProjectModel, project_id: int) -> ProjectModel:
        return project_repository.update(self.session, project, project_id)

    def update(self, project: Dict, project_id: int) -> ProjectModel:
        stored_project = project_repository.find_by_id(self.session, project_id)
        assert stored_project is not None
        return project_repository.update(
            self.session, stored_project.copy(update=project), project_id
        )

    def delete(self, project_id: int) -> None:
        project_repository.delete(self.session, project_id)
