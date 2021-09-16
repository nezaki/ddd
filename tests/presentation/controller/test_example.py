from fastapi.testclient import TestClient


def test_multiple_body_parameters(client: TestClient) -> None:
    data = {
        "example1": {"name1": "test1"},
        "example2": {"name2": "test2"},
    }
    response = client.post("/example", json=data)
    assert response.status_code == 200
    content = response.json()
    assert content == data
