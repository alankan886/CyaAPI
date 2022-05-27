from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests.utils.utils import format_datetime
from app.tests.utils.queue import create_random_queue
from app.crud import read_queue_by_id


def test_read_queues(test_client: TestClient, test_db: Session) -> None:
    queue = create_random_queue(test_db)
    response = test_client.get(
        "/queues/",
    )
    assert response.status_code == 200
    content = response.json()

    assert len(content) == 1
    response_queue = content[0]
    assert response_queue["name"] == queue.name
    assert response_queue["description"] == queue.description
    assert response_queue["id"] == queue.id
    assert response_queue["created_at"] == format_datetime(queue.created_at)


def test_create_queue(test_client: TestClient) -> None:
    test_name = "Test Name"
    test_description = "Test description."
    response = test_client.post(
        "/queues/", json={"name": test_name, "description": test_description}
    )
    assert response.status_code == 201
    content = response.json()

    assert content["name"] == test_name
    assert content["description"] == test_description


def test_create_queue_name_already_exists(test_client: TestClient, test_db: Session):
    queue = create_random_queue(test_db)
    response = test_client.post("/queues/", json={"name": queue.name})
    assert response.status_code == 400
    content = response.json()

    assert content["detail"] == f"Queue with the name '{queue.name}' has already exists"


def test_update_queue(test_client: TestClient, test_db: Session) -> None:
    new_name = "New Name"
    new_description = "New description."
    queue = create_random_queue(test_db)
    response = test_client.patch(
        f"/queues/{queue.id}/", json={"name": new_name, "description": new_description}
    )
    assert response.status_code == 200
    content = response.json()

    assert content["name"] == new_name
    assert content["description"] == new_description


def test_update_non_existing_queue(test_client: TestClient, test_db: Session) -> None:
    new_name = "New Name"
    new_description = "New description."
    response = test_client.patch(
        f"/queues/123/", json={"name": new_name, "description": new_description}
    )
    assert response.status_code == 404
    content = response.json()

    assert content["detail"] == "Queue with the id='123' is not found"


def test_delete_queue(test_client: TestClient, test_db: Session) -> None:
    queue = create_random_queue(test_db)
    queue_id = queue.id
    response = test_client.delete(f"/queues/{queue.id}/")
    assert response.status_code == 204
    content = response.json()

    assert content == None
    assert read_queue_by_id(test_db, queue_id) == None


def test_delete_non_existing_queue(test_client: TestClient, test_db: Session) -> None:
    response = test_client.delete(f"/queues/123/")
    assert response.status_code == 404
    content = response.json()

    assert content["detail"] == "Queue with the id='123' is not found"
