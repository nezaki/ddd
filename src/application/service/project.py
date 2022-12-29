from abc import ABC, abstractmethod
from typing import Dict, List

from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends
from src.domain.model.project import Project as ProjectModel
from src.infrastructure.datasource.database import get_db_async
from src.infrastructure.datasource.repository import project as project_repository


class ProjectService(ABC):
    @abstractmethod
    async def read_projects(
        self, skip: int | None = 0, limit: int | None = 100
    ) -> List[ProjectModel]:
        raise NotImplementedError

    @abstractmethod
    async def read(self, project_id: int) -> ProjectModel | None:
        raise NotImplementedError

    @abstractmethod
    async def create(self, project: ProjectModel) -> ProjectModel:
        raise NotImplementedError

    @abstractmethod
    async def replace(self, project: ProjectModel, project_id: int) -> ProjectModel:
        raise NotImplementedError

    @abstractmethod
    async def update(self, project: Dict, project_id: int) -> ProjectModel:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, project_id: int) -> None:
        raise NotImplementedError


class ProjectServiceImpl(ProjectService):
    def __init__(self, session: AsyncSession = Depends(get_db_async)):
        self.session = session

    async def read_projects(
        self, skip: int | None = 0, limit: int | None = 100
    ) -> List[ProjectModel]:
        return await project_repository.find(self.session, skip, limit)

    async def read(self, project_id: int) -> ProjectModel | None:
        return await project_repository.find_by_id(self.session, project_id)

    async def create(self, project: ProjectModel) -> ProjectModel:
        return await project_repository.create(self.session, project)

    async def replace(self, project: ProjectModel, project_id: int) -> ProjectModel:
        return await project_repository.update(self.session, project, project_id)

    async def update(self, project: Dict, project_id: int) -> ProjectModel:
        stored_project = await project_repository.find_by_id(self.session, project_id)
        assert stored_project is not None
        return await project_repository.update(
            self.session, stored_project.copy(update=project), project_id
        )

    async def delete(self, project_id: int) -> None:
        await project_repository.delete(self.session, project_id)
