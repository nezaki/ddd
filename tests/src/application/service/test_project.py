import pytest
from pytest_mock import MockerFixture

from src.application.service.project import ProjectServiceImpl
from src.domain.model.project import Project as ProjectModel


@pytest.mark.asyncio
async def test_project_service(mocker: MockerFixture) -> None:
    test_project = [
        ProjectModel(id=100, name="name service test", description="desc service test"),
        ProjectModel(
            id=101, name="name service test02", description="desc service test02"
        ),
    ]

    service = ProjectServiceImpl()

    # read_projects
    mocker.patch(
        "src.infrastructure.datasource.repository.project.find",
        return_value=test_project,
    )
    read_projects = await service.read_projects(test_project[0].id)
    assert read_projects[0].id == 100
    assert read_projects[0].name == "name service test"
    assert read_projects[0].description == "desc service test"
    assert read_projects[1].id == 101
    assert read_projects[1].name == "name service test02"
    assert read_projects[1].description == "desc service test02"

    # read
    mocker.patch(
        "src.infrastructure.datasource.repository.project.find_by_id",
        return_value=test_project[0],
    )
    reed_project = await service.read(100)
    assert reed_project is not None
    assert reed_project.id == 100
    assert reed_project.name == "name service test"
    assert reed_project.description == "desc service test"

    # create
    mocker.patch(
        "src.infrastructure.datasource.repository.project.create",
        return_value=test_project[0],
    )
    created_project = await service.create(test_project[0])
    assert created_project.id == 100
    assert created_project.name == "name service test"
    assert created_project.description == "desc service test"

    # replace
    mocker.patch(
        "src.infrastructure.datasource.repository.project.update",
        return_value=test_project[0],
    )
    replaced_project = await service.replace(test_project[0], 100)
    assert replaced_project.id == 100
    assert replaced_project.name == "name service test"
    assert replaced_project.description == "desc service test"

    # update
    mocker.patch(
        "src.infrastructure.datasource.repository.project.find_by_id",
        return_value=test_project[0],
    )
    mocker.patch(
        "src.infrastructure.datasource.repository.project.update",
        return_value=ProjectModel(
            id=test_project[0].id,
            name="update test",
            description=test_project[0].description,
        ),
    )
    updated_project = await service.update({"name": "update test"}, 100)
    assert updated_project.id == 100
    assert updated_project.name == "update test"
    assert updated_project.description == "desc service test"

    # delete
    mocker.patch(
        "src.infrastructure.datasource.repository.project.delete",
        return_value=None,
    )
    await service.delete(100)
