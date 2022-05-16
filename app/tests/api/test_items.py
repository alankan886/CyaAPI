import pytest
from datetime import date, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from supermemo2 import SMTwo

from app.crud.crud_item import read_item_by_id
from app.tests.utils.utils import format_datetime
from app.tests.utils.item import create_random_queue, create_random_item


def test_read_items(test_client: TestClient, test_db: Session) -> None:
    item = create_random_item(test_db)
    response = test_client.get(
        "/items/",
    )
    assert response.status_code == 200
    content = response.json()

    assert len(content) == 1
    response_item = content[0]
    assert response_item["name"] == item.name
    assert response_item["easiness"] == item.easiness
    assert response_item["interval"] == item.interval
    assert response_item["repetitions"] == item.repetitions
    assert response_item["review_date"] == str(item.review_date)
    assert response_item["id"] == item.id
    assert response_item["created_at"] == format_datetime(item.created_at)


@pytest.mark.skip()
def test_read_items_filter_review_date_today():
    # TODO
    pass


def test_create_item(test_client: TestClient, test_db: Session) -> None:
    queue = create_random_queue(test_db)
    queue_id = queue.id
    test_name = "Test Name"
    test_quality = 5
    test_easiness = 2.5
    test_interval = 10
    test_repetitions = 2
    test_review_date = str(date.today())

    response = test_client.post(
        "/items/",
        json={
            "name": test_name,
            "quality": test_quality,
            "easiness": test_easiness,
            "interval": test_interval,
            "repetitions": test_repetitions,
            "review_date": test_review_date,
            "queue_id": queue.id,
        },
    )
    assert response.status_code == 201
    content = response.json()

    assert content["name"] == test_name
    assert content["quality"] == test_quality
    assert content["easiness"] == test_easiness
    assert content["interval"] == test_interval
    assert content["repetitions"] == test_repetitions
    assert content["review_date"] == str(test_review_date)
    assert content["queue_id"] == queue_id


def test_create_item_name_already_exists_in_queue(
    test_client: TestClient, test_db: Session
):
    item = create_random_item(test_db)
    response = test_client.post(
        "/items/",
        json={
            "name": item.name,
            "quality": 5,
            "easiness": 2.5,
            "interval": 10,
            "repetitions": 2,
            "review_date": str(date.today()),
            "queue_id": item.queue_id,
        },
    )
    assert response.status_code == 400
    content = response.json()

    assert (
        content["detail"]
        == f"Item with the name '{item.name}' has already exists in Queue '{item.queue_id}'"
    )


def test_create_item_name_already_exists_in_different_queue(
    test_client: TestClient, test_db: Session
):
    queue = create_random_queue(test_db)
    item = create_random_item(test_db)
    queue_id = queue.id
    item_name = item.name
    test_quality = 5
    test_easiness = 2.5
    test_interval = 10
    test_repetitions = 2
    test_review_date = str(date.today())

    response = test_client.post(
        "/items/",
        json={
            "name": item.name,
            "quality": test_quality,
            "easiness": test_easiness,
            "interval": test_interval,
            "repetitions": test_repetitions,
            "review_date": test_review_date,
            "queue_id": queue.id,
        },
    )
    assert response.status_code == 201
    content = response.json()

    assert content["name"] == item_name
    assert content["quality"] == test_quality
    assert content["easiness"] == test_easiness
    assert content["interval"] == test_interval
    assert content["repetitions"] == test_repetitions
    assert content["review_date"] == str(test_review_date)
    assert content["queue_id"] == queue_id


def test_update_item(test_client: TestClient, test_db: Session) -> None:
    different_queue = create_random_queue(test_db)
    item = create_random_item(test_db)

    new_name = "New Name"
    new_quality = 5
    new_easiness = 2.0
    new_interval = 40
    new_repetitions = 3
    new_review_date = str(date.today() + timedelta(days=10))
    different_queue_id = different_queue.id

    response = test_client.patch(
        f"/items/{item.id}/",
        json={
            "name": new_name,
            "quality": new_quality,
            "easiness": new_easiness,
            "interval": new_interval,
            "repetitions": new_repetitions,
            "review_date": new_review_date,
            "queue_id": different_queue_id,
        },
    )
    assert response.status_code == 200
    content = response.json()

    assert content["name"] == new_name
    assert content["quality"] == new_quality
    assert content["easiness"] == new_easiness
    assert content["interval"] == new_interval
    assert content["repetitions"] == new_repetitions
    assert content["review_date"] == new_review_date
    assert content["queue_id"] == different_queue_id


def test_update_non_existing_item(test_client: TestClient, test_db: Session) -> None:
    different_queue = create_random_queue(test_db)

    new_name = "New Name"
    new_quality = 5
    new_easiness = 2.0
    new_interval = 40
    new_repetitions = 3
    new_review_date = str(date.today() + timedelta(days=10))
    different_queue_id = different_queue.id

    response = test_client.patch(
        "/items/123/",
        json={
            "name": new_name,
            "quality": new_quality,
            "easiness": new_easiness,
            "interval": new_interval,
            "repetitions": new_repetitions,
            "review_date": new_review_date,
            "queue_id": different_queue_id,
        },
    )
    assert response.status_code == 404
    content = response.json()

    assert content["detail"] == f"Item with the id='123' is not found"


def test_review_item(test_client: TestClient, test_db: Session) -> None:
    item = create_random_item(test_db)

    new_quality = 5
    item_easiness = item.easiness
    item_interval = item.interval
    item_repetitions = item.repetitions

    response = test_client.patch(
        f"/items/{item.id}/review/",
        json={
            "quality": new_quality,
        },
    )
    assert response.status_code == 200
    content = response.json()

    review_info = SMTwo(item_easiness, item_interval, item_repetitions).review(
        new_quality
    )
    assert content["quality"] == new_quality
    assert content["easiness"] == review_info.easiness
    assert content["interval"] == review_info.interval
    assert content["repetitions"] == review_info.repetitions
    assert content["review_date"] == str(review_info.review_date)


def test_review_non_existing_item(test_client: TestClient, test_db: Session) -> None:
    new_quality = 5

    response = test_client.patch(
        f"/items/123/review/",
        json={
            "quality": new_quality,
        },
    )
    assert response.status_code == 404
    content = response.json()

    assert content["detail"] == f"Item with the id='123' is not found"


def test_delete_item(test_client: TestClient, test_db: Session) -> None:
    item = create_random_item(test_db)
    item_id = item.id
    response = test_client.delete(f"/items/{item_id}/")
    assert response.status_code == 204
    content = response.json()

    assert content == None
    assert read_item_by_id(test_db, item_id) == None


def test_delete_non_existing_item(test_client: TestClient, test_db: Session) -> None:
    response = test_client.delete(f"/items/123/")
    assert response.status_code == 404
    content = response.json()

    assert content["detail"] == "Item with the id='123' is not found"
