from _pytest.monkeypatch import MonkeyPatch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app import schemas, models


def test_get_card_detail(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = {
        "id": 1,
        "card_id": 1,
        "quality": 3,
        "easiness": 2.36,
        "interval": 1,
        "repetitions": 2,
        "last_review": "2021-01-01",
        "next_review": "2021-01-02",
        "latest": True
    }

    def mock_read_card_detail_by_id(db: Session, card_detail_id: int):
        return test_data

    monkeypatch.setattr(crud, "read_card_detail_by_id",
                        mock_read_card_detail_by_id)
    response = test_client.get("/card_details/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_get_card_detail_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_read_card_detail_by_id(db: Session, card_detail_id: int):
        return

    monkeypatch.setattr(crud, "read_card_detail_by_id", mock_read_card_detail_by_id)
    response = test_client.get("/card_details/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Card detail with id=1 not found"


def test_get_card_details(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = [
        {
            "id": 1,
            "card_id": 1,
            "quality": 3,
            "easiness": 2.36,
            "interval": 1,
            "repetitions": 2,
            "last_review": "2021-01-01",
            "next_review": "2021-01-02",
            "latest": False
        },
        {
            "id": 2,
            "card_id": 1,
            "quality": 4,
            "easiness": 2.67,
            "interval": 10,
            "repetitions": 3,
            "last_review": "2021-01-08",
            "next_review": "2021-01-18",
            "latest": True
        }
    ]

    def mock_read_card_details(db: Session):
        return test_data

    monkeypatch.setattr(crud, "read_card_details", mock_read_card_details)
    response = test_client.get("/card_details")
    assert response.status_code == 200
    assert response.json() == test_data


def test_get_card_details_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_read_card_details(db: Session):
        return []

    monkeypatch.setattr(crud, "read_card_details", mock_read_card_details)
    response = test_client.get("/card_details")
    assert response.status_code == 200
    assert response.json() == []


def test_post_card_detail(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_request_data = {
        "card_id": 1,
        "quality": 3,
        "easiness": 2.36,
        "interval": 1,
        "repetitions": 2,
        "last_review": "2021-01-01"
    }
    test_response_data = {
        "id": 1,
        "card_id": 1,
        "quality": 3,
        "easiness": 2.36,
        "interval": 1,
        "repetitions": 2,
        "last_review": "2021-01-01",
        "next_review": "2021-01-02",
        "latest": True
    }

    def mock_create_card_detail(db: Session, card_detail: schemas.CardDetailCreate):
        return test_response_data

    def mock_read_card_detail_by_card_id_and_review(db: Session, card_detail: schemas.CardDetailCreate):
        return

    monkeypatch.setattr(crud, "create_card_detail", mock_create_card_detail)
    monkeypatch.setattr(
        crud,
        "read_card_detail_by_card_id_and_review",
        mock_read_card_detail_by_card_id_and_review
    )
    response = test_client.post("/card_details", json=test_request_data)
    assert response.status_code == 201
    assert response.json() == test_response_data


def test_post_card_detail_already_exists(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_request_data = {
        "card_id": 1,
        "quality": 3,
        "easiness": 2.36,
        "interval": 1,
        "repetitions": 2,
        "last_review": "2021-01-01"
    }

    card_exists = {
        "id": 1,
        "card_id": 1,
        "quality": 3,
        "easiness": 2.36,
        "interval": 1,
        "repetitions": 2,
        "last_review": "2021-01-01",
        "next_review": "2021-01-02",
        "latest": True
    }

    def mock_read_card_detail_by_card_id_and_review(db: Session, card_detail: schemas.CardDetailCreate):
        return card_exists

    monkeypatch.setattr(
        crud,
        "read_card_detail_by_card_id_and_review",
        mock_read_card_detail_by_card_id_and_review
    )
    response = test_client.post("/card_details", json=test_request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Card detail with card_id=1 and last_review date='2021-01-01' has already exists"


def test_put_card_detail(test_client: TestClient, monkeypatch: MonkeyPatch):
    before_update = {
        "id": 1,
        "card_id": 1,
        "quality": 3,
        "easiness": 2.36,
        "interval": 1,
        "repetitions": 2,
        "last_review": "2021-01-01",
        "next_review": "2021-01-02",
        "latest": True
    }
    test_request_data = {
        "card_id": 2,
        "quality": 4,
        "easiness": 2.99,
        "interval": 1,
        "repetitions": 2,
        "last_review": "2021-01-01",
    }
    after_update = {
        "id": 1,
        "card_id": 2,
        "quality": 4,
        "easiness": 2.99,
        "interval": 1,
        "repetitions": 2,
        "last_review": "2021-01-01",
        "next_review": "2021-01-02",
        "latest": True
    }

    def mock_read_card_detail_by_id(db: Session, card_detail_id: int):
        return before_update

    def mock_update_card_detail(db: Session, old_card_detail: schemas.CardDetail, new_card_detail: schemas.CardDetailCreate):
        return after_update

    monkeypatch.setattr(crud, "read_card_detail_by_id", mock_read_card_detail_by_id)
    monkeypatch.setattr(crud, "update_card_detail", mock_update_card_detail)
    response = test_client.put("/card_details/1", json=test_request_data)
    assert response.status_code == 200
    assert response.json() == after_update
    assert response.json() != before_update


def test_put_card_detail_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = {
        "id": 1,
        "card_id": 2,
        "quality": 4,
        "easiness": 2.99,
        "interval": 1,
        "repetitions": 2,
        "last_review": "2021-01-01"
    }

    def mock_read_card_detail_by_id(db: Session, card_detail_id: int):
        return

    def mock_create_card_detail(db: Session, card: schemas.StackCreate):
        return test_data

    monkeypatch.setattr(crud, "read_card_detail_by_id", mock_read_card_detail_by_id)
    monkeypatch.setattr(crud, "create_card_detail", mock_create_card_detail)
    response = test_client.put("/card_details/1", json=test_data)
    assert response.status_code == 201
    assert response.json() == test_data


def test_delete_card_detail(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = {
        "id": 1,
        "card_id": 2,
        "quality": 4,
        "easiness": 2.99,
        "interval": 1,
        "repetitions": 2,
        "last_review": "2021-01-01",
        "next_review": "2021-01-02",
        "latest": True
    }

    def mock_read_card_detail_by_id(db: Session, card_detail_id: int):
        return test_data

    def mock_delete_card_detail(db: Session, card_detail_id):
        return

    monkeypatch.setattr(crud, "read_card_detail_by_id", mock_read_card_detail_by_id)
    monkeypatch.setattr(crud, "delete_card_detail", mock_delete_card_detail)
    response = test_client.delete("/card_details/1")
    assert response.status_code == 204
    assert response.json() is None


def test_delete_card_detail_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_read_card_detail_by_id(db: Session, card_detail_id: int):
        return

    monkeypatch.setattr(crud, "read_card_detail_by_id", mock_read_card_detail_by_id)
    response = test_client.delete("/card_details/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Card detail with id=1 is not found"
