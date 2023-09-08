from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.model.project import Project as ProjectModel
from src.infrastructure.datasource.entity.project import Project as ProjectEntity


async def find(
    session: AsyncSession, skip: int | None = 0, limit: int | None = 100
) -> List[ProjectModel]:
    statement = (
        select(ProjectEntity).order_by(ProjectEntity.id).offset(skip).limit(limit)
    )
    result = await session.execute(statement)
    projects = result.fetchall()
    return [
        ProjectModel(
            id=project[0].id,
            name=project[0].name,
            description=project[0].description,
        )
        for project in projects
    ]


async def _find_by_id(session: AsyncSession, project_id: int) -> ProjectEntity | None:
    statement = select(ProjectEntity).filter_by(id=project_id)
    result = (await session.execute(statement)).fetchone()
    if result is not None:
        return result.Project  # type: ignore
    else:
        return None


async def find_by_id(session: AsyncSession, project_id: int) -> ProjectModel | None:
    project = await _find_by_id(session, project_id)
    if project is not None:
        return ProjectModel.model_validate(project)
    else:
        return None


async def create(session: AsyncSession, project: ProjectModel) -> ProjectModel:
    _project: ProjectEntity = ProjectEntity.from_model(project)
    session.add(_project)
    await session.flush()
    return ProjectModel(
        id=_project.id,
        name=_project.name,  # type: ignore
        description=_project.description,
    )


async def update(
    session: AsyncSession, project: ProjectModel, project_id: int
) -> ProjectModel:
    _project = await _find_by_id(session, project_id)
    assert _project is not None
    _project.name = "update test name"
    _project.description = project.description
    await session.flush()
    return ProjectModel.model_validate(_project)


async def delete(session: AsyncSession, project_id: int) -> None:
    _project = await _find_by_id(session, project_id)
    await session.delete(_project)
    await session.flush()
