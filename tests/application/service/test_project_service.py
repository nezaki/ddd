from pytest_mock import MockerFixture
from sqlalchemy.orm import Session

from src.application.service.project import ProjectServiceImpl
from src.domain.model.project import Project as ProjectModel

_test_project = ProjectModel(
    id=100, name="name service test", description="desc service test"
)


def test_project_service(db: Session, mocker: MockerFixture) -> None:
    mocker.patch(
        "src.infrastructure.datasource.project.ProjectRepositoryImpl.create",
        return_value=_test_project,
    )
    service = ProjectServiceImpl(db)

    created_project = service.create(_test_project)
    assert created_project.id == 100
    assert created_project.name == "name service test"
    assert created_project.description == "desc service test"
