from typing import Optional

from fastapi.testclient import TestClient

from src.domain.model.project import Project
from src.main import app
from src.presentation.controller.project import verify_token
from src.application.service.project import ProjectServiceImpl


async def override_verify_token():
    pass

app.dependency_overrides[verify_token] = override_verify_token


def test_project(db, client: TestClient) -> None:
    # create
    data = {
        "name": "test_name",
        "description": "test_description",
    }
    response = client.post("/projects", json=data)
    assert response.status_code == 200

    # reads_project
    response = client.get("/projects?skip=0&limit=100")
    assert response.status_code == 200
    response_projects = response.json().get("projects")
    assert len(response_projects) == 1
    assert response_projects[0].get("id") == 1
    assert response_projects[0].get("name") == "test_name"
    assert response_projects[0].get("description") == "test_description"
