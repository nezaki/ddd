from fastapi.testclient import TestClient


def test_create(db, client: TestClient) -> None:
    data = {
        "name": "test_name",
        "description": "test_description",
    }
    response = client.post("/projects", json=data)
    assert response.status_code == 200


def test_reads_project(db, client: TestClient) -> None:
    response = client.get("/projects?skip=0&limit=100")
    assert response.status_code == 200
    response_projects = response.json().get("projects")
    assert len(response_projects) == 1
    assert response_projects[0].get("id") == 1
    assert response_projects[0].get("name") == "test_name"
    assert response_projects[0].get("description") == "test_description"


def test_update(db, client: TestClient) -> None:
    # update
    data = {
        "name": "test_name_updated",
        "description": "test_description_updated",
    }
    response = client.put("/projects/1", json=data)
    assert response.status_code == 200

    # read
    response = client.get("/projects/1")
    assert response.status_code == 200
    response_project = response.json()
    assert response_project.get("id") == 1
    assert response_project.get("name") == "test_name_updated"
    assert response_project.get("description") == "test_description_updated"


def test_delete(db, client: TestClient) -> None:
    # delete
    response = client.delete("/projects/1")
    assert response.status_code == 204

    # reads_project
    response = client.get("/projects?skip=0&limit=100")
    assert response.status_code == 200
    response_projects = response.json().get("projects")
    assert len(response_projects) == 0
