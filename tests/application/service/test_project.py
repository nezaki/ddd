from pytest_mock import MockerFixture
from sqlalchemy.orm import Session

from src.application.service.project import ProjectServiceImpl
from src.domain.model.project import Project as ProjectModel


def test_project_service(db: Session, mocker: MockerFixture) -> None:
    test_project = ProjectModel(
        id=100, name="name service test", description="desc service test"
    )

    mocker.patch(
        "src.infrastructure.datasource.repository.project.create",
        return_value=test_project,
    )

    service = ProjectServiceImpl()

    created_project = service.create(test_project)
    assert created_project.id == 100
    assert created_project.name == "name service test"
    assert created_project.description == "desc service test"
