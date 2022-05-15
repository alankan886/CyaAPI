from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.tests.utils.queue import create_random_queue
from app.crud import read_queue_by_id


def test_read_queues(
    test_client: TestClient, test_db: Session
) -> None:
    item = create_random_queue(test_db)
    response = test_client.get(
        "/queues/",
    )
    assert response.status_code == 200
    content = response.json()

    assert len(content) == 1
    response_item = content[0]
    assert response_item["name"] == item.name
    assert response_item["description"] == item.description
    assert response_item["id"] == item.id
    assert response_item["created_at"] == str(item.created_at)


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


def test_update_queue(
    test_client: TestClient, test_db: Session
) -> None:
    new_name = "New Name"
    new_description = "New description."
    item = create_random_queue(test_db)
    response = test_client.put(
        f"/queues/{item.id}", json={"name": new_name, "description": new_description}
    )
    assert response.status_code == 200
    content = response.json()

    assert content["name"] == new_name
    assert content["description"] == new_description


# TODO: maybe make test_session into test_db, and test_db into test_db_clean_up and maybe just make it autouse
def test_delete_queue(
    test_client: TestClient, test_db: Session
) -> None:
    item = create_random_queue(test_db)
    item_id = item.id
    response = test_client.delete(f"/queues/{item.id}")
    assert response.status_code == 204
    content = response.json()

    assert content == None
    assert read_queue_by_id(test_db, item_id) == None
