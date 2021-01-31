from fastapi.testclient import TestClient


def test_create_stack(test_client: TestClient):
    test_request_data = {
        "name": "stack1"
    }
    response = test_client.post("/stacks", json=test_request_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "stack1"
    assert "id" in data
    stack_id = data["id"]

    response = test_client.get(f"/stacks/{stack_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "stack1"
    assert data["id"] == stack_id
