from typing import Dict, List

import pytest
from httpx import AsyncClient

from src.application.service.project import ProjectService, ProjectServiceImpl
from src.domain.model.project import Project as ProjectModel
from tests.conftest import app

test_project01 = ProjectModel(
    id=100, name="name presentation test", description="desc presentation test"
)
test_project02 = ProjectModel(
    id=101, name="name presentation test02", description="desc presentation test02"
)


class ProjectServiceMock(ProjectService):
    async def read_projects(
        self, skip: int | None = 0, limit: int | None = 100
    ) -> List[ProjectModel]:
        return [test_project01, test_project02]

    async def read(self, project_id: int) -> ProjectModel | None:
        return test_project01

    async def create(self, project: ProjectModel) -> ProjectModel:
        return test_project01

    async def replace(self, project: ProjectModel, project_id: int) -> ProjectModel:
        return test_project01

    async def update(self, project: Dict, project_id: int) -> ProjectModel:
        return test_project01

    async def delete(self, project_id: int) -> None:
        pass


app.dependency_overrides[ProjectServiceImpl] = ProjectServiceMock


@pytest.mark.asyncio
async def test_project(client: AsyncClient) -> None:

    # get list
    response = await client.get("/projects")
    assert response.status_code == 200
    response_projects = response.json().get("projects")
    assert len(response_projects) == 2
    assert response_projects[0].get("id") == 100
    assert response_projects[0].get("name") == "name presentation test"
    assert response_projects[0].get("description") == "desc presentation test"
    assert response_projects[1].get("id") == 101
    assert response_projects[1].get("name") == "name presentation test02"
    assert response_projects[1].get("description") == "desc presentation test02"

    # get
    response = await client.get("/projects/1")
    assert response.status_code == 200
    response_project = response.json()
    assert response_project.get("id") == 100
    assert response_project.get("name") == "name presentation test"
    assert response_project.get("description") == "desc presentation test"

    # post
    response = await client.post(
        "/projects",
        json={
            "name": "name",
            "description": "description",
        },
    )
    assert response.status_code == 200
    response_project_post = response.json()
    assert response_project_post.get("id") == 100
    assert response_project_post.get("name") == "name presentation test"
    assert response_project_post.get("description") == "desc presentation test"

    # put
    response = await client.put(
        "/projects/2",
        json={
            "name": "name",
            "description": "description",
        },
    )
    assert response.status_code == 200
    response_project_put = response.json()
    assert response_project_put.get("id") == 100
    assert response_project_put.get("name") == "name presentation test"
    assert response_project_put.get("description") == "desc presentation test"

    # patch
    response = await client.patch(
        "/projects/3",
        json={
            "name": "name",
        },
    )
    assert response.status_code == 200
    response_project_patch = response.json()
    assert response_project_patch.get("id") == 100
    assert response_project_patch.get("name") == "name presentation test"
    assert response_project_patch.get("description") == "desc presentation test"

    # delete
    response = await client.delete("/projects/4")
    assert response.status_code == 204
