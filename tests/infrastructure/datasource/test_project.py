import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.model.project import Project
from src.infrastructure.datasource.repository import project as project_repository


@pytest.mark.asyncio
async def test_project_repository(session: AsyncSession) -> None:
    test_value = {
        "name": "name test",
        "description": "test description",
    }

    created_project = await project_repository.create(
        session, Project(name=test_value["name"], description=test_value["description"])
    )
    assert created_project.name == test_value["name"]
    assert created_project.description == test_value["description"]

    assert created_project.id is not None
    project = await project_repository.find_by_id(session, created_project.id)
    assert project is not None
    assert project.id == created_project.id
    assert project.name == test_value["name"]
    assert project.description == test_value["description"]

    project.name = "update test name"
    updated_project = await project_repository.update(session, project, project.id)
    assert updated_project.id == project.id
    assert updated_project.name == project.name
    assert updated_project.description == project.description

    await project_repository.delete(session, project.id)

    assert await project_repository.find_by_id(session, project.id) is None

    test_values = [
        {"name": "name1", "description": "description1"},
        {"name": "name2", "description": "description2"},
    ]
    for value in test_values:
        await project_repository.create(
            session, Project(name=value["name"], description=value["description"])
        )
    projects = await project_repository.find(session)
    assert len(projects) == 2
    assert projects[0].name == "name1"
    assert projects[0].description == "description1"
    assert projects[1].name == "name2"
    assert projects[1].description == "description2"
