from sqlalchemy.orm import Session

from fastapi.testclient import TestClient


def test(db: Session, client: TestClient) -> None:
    data = {
        "name": "test_name",
        "description": "test_description",
    }
    response = client.post("/projects", json=data)
    assert response.status_code == 200

    # get project
    response = client.get("/projects?skip=0&limit=100")
    assert response.status_code == 200
    response_projects = response.json().get("projects")
    assert len(response_projects) == 1
    assert response_projects[0].get("id") == 1
    assert response_projects[0].get("name") == "test_name"
    assert response_projects[0].get("description") == "test_description"

    # post
    data = {
        "name": "test_name2",
        "description": "test_description2",
    }
    response = client.post("/projects", json=data)
    assert response.status_code == 200

    # get projects
    response = client.get("/projects?skip=0&limit=100")
    assert response.status_code == 200
    response_projects = response.json().get("projects")
    assert len(response_projects) == 2

    # put
    data = {
        "name": "test_name_updated",
        "description": "test_description_updated",
    }
    response = client.put("/projects/1", json=data)
    assert response.status_code == 200

    # get project
    response = client.get("/projects/1")
    assert response.status_code == 200
    response_project = response.json()
    assert response_project.get("id") == 1
    assert response_project.get("name") == "test_name_updated"
    assert response_project.get("description") == "test_description_updated"

    # patch
    data = {
        "description": "test_description_updated2",
    }
    response = client.patch("/projects/1", json=data)
    assert response.status_code == 200

    # get project
    response = client.get("/projects/1")
    assert response.status_code == 200
    response_project = response.json()
    assert response_project.get("id") == 1
    assert response_project.get("name") == "test_name_updated"
    assert response_project.get("description") == "test_description_updated2"

    # delete
    response = client.delete("/projects/1")
    assert response.status_code == 204

    # get project
    response = client.get("/projects?skip=0&limit=100")
    assert response.status_code == 200
    response_projects = response.json().get("projects")
    assert len(response_projects) == 1
