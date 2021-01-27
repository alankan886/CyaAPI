from _pytest.monkeypatch import MonkeyPatch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app import schemas, models


def test_read_card(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = {"id": 1, "name": "card1", "stack_id": 1}

    def mock_read_card_by_id(db: Session, card_id: int):
        return test_data

    monkeypatch.setattr(crud, "read_card_by_id", mock_read_card_by_id)
    response = test_client.get("/cards/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_card_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_read_card_by_id(db: Session, card_id: int):
        return

    monkeypatch.setattr(crud, "read_card_by_id", mock_read_card_by_id)
    response = test_client.get("/cards/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Card with id=1 not found"


def test_read_cards(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = [
        {
            "id": 1,
            "name": "card1",
            "stack_id": 1,
        },
        {
            "id": 2,
            "name": "card2",
            "stack_id": 1,
        },
        {
            "id": 3,
            "name": "card3",
            "stack_id": 2,
        }
    ]

    def mock_read_cards(db: Session):
        return test_data

    monkeypatch.setattr(crud, "read_cards", mock_read_cards)
    response = test_client.get("/cards")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_cards_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_read_cards(db: Session):
        return

    monkeypatch.setattr(crud, "read_cards", mock_read_cards)
    response = test_client.get("/cards")
    assert response.status_code == 200
    assert response.json() == []


def test_get_card_details_of_card(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = {
        "id": 1,
        "quality": 3,
        "easiness": 2.5,
        "interval": 1,
        "repetitions": 1,
        "last_review": "2021-01-01",
        "next_review": "2021-01-02"
    }

    def mock_read_card_details_of_card(db: Session, card_id: int):
        return test_data

    monkeypatch.setattr(crud, "read_card_details_of_card", mock_read_card_details_of_card)
    response = test_client.get("/cards/1/card_details")
    assert response.status_code == 200
    assert response.json() == test_data


def test_get_card_details_of_card_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_read_card_details_of_card(db: Session, card_id: int):
        return []

    monkeypatch.setattr(crud, "read_card_details_of_card", mock_read_card_details_of_card)
    response = test_client.get("/cards/1/card_details")
    assert response.status_code == 200
    assert response.json() == []

import pytest
@pytest.mark.skip
def test_get_cards_due_today(test_client: TestClient, monkeypatch: MonkeyPatch):
    request_data = {
        "filter": "today"
    }
    response_data = [
        {
            "id": 1,
            "name": "card1",
            "stack_id": 1,
        }
    ]

    def mock_read_card_due(db: Session, card_id: int):
        return response_data

    monkeypatch.setattr(crud, "read_card_due", mock_read_card_due)
    response = test_client.get("/cards/1/card_details", json=request_data)
    assert response.status_code == 200
    assert response.json() == response_data


def test_create_card(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_request_data = {
        "name": "card1",
        "stack_id": 1,
    }
    test_response_data = {
        "id": 1,
        "name": "card1",
        "stack_ids": 1
    }

    def mock_create_card(db: Session, card: schemas.CardCreate):
        return test_response_data

    def mock_read_card_by_name(db: Session, card_name: str):
        return

    monkeypatch.setattr(crud, "create_card", mock_create_card)
    monkeypatch.setattr(crud, "read_card_by_name", mock_read_card_by_name)
    response = test_client.post("/cards", json=test_request_data)
    assert response.status_code == 201
    assert response.json() == test_response_data


def test_create_card_already_exists(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_request_data = {
        "name": "card1",
        "stack_id": 1
    }

    card_exists = {
        "id": 1,
        "name": "card1",
        "stack_id": 1
    }

    def mock_read_card_by_name(db: Session, card_name: str):
        return card_exists

    monkeypatch.setattr(crud, "read_card_by_name", mock_read_card_by_name)
    response = test_client.post("/cards", json=test_request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Card with the name card1 has already exists"


def test_put_card(test_client: TestClient, monkeypatch: MonkeyPatch):
    before_udpate = {
        "id": 1,
        "name": "oldname",
        "stack_id": 1
    }
    test_request_data = {
        "name": "newname",
        "stack_id": 2
    }
    after_update = {
        "id": 1,
        "name": "newname",
        "stack_id": 2
    }

    def mock_read_card_by_id(db: Session, card_id: int):
        return before_udpate

    def mock_update_card(db: Session, old_card: schemas.Card, new_card: schemas.CardCreate):
        return after_update

    monkeypatch.setattr(crud, "read_card_by_id", mock_read_card_by_id)
    monkeypatch.setattr(crud, "update_card", mock_update_card)
    response = test_client.put("/cards/1", json=test_request_data)
    assert response.status_code == 200
    assert response.json() == after_update
    assert response.json() != before_udpate


def test_put_card_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = {
        "id": 1,
        "name": "newname",
        "stack_id": 2
    }

    def mock_read_card_by_id(db: Session, card_id: int):
        return

    def mock_create_card(db: Session, card: schemas.StackCreate):
        return test_data

    monkeypatch.setattr(crud, "read_card_by_id", mock_read_card_by_id)
    monkeypatch.setattr(crud, "create_card", mock_create_card)
    response = test_client.put("/cards/1", json=test_data)
    assert response.status_code == 201
    assert response.json() == test_data


def test_delete_card(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = {
        "id": 1,
        "name": "card1",
        "stack_id": 1
    }

    def mock_read_card_by_id(db: Session, card_id: int):
        return test_data

    def mock_delete_card(db: Session, card: schemas.Card):
        return

    monkeypatch.setattr(crud, "read_card_by_id", mock_read_card_by_id)
    monkeypatch.setattr(crud, "delete_card", mock_delete_card)
    response = test_client.delete("/cards/1")
    assert response.status_code == 204
    assert response.json() is None


def test_delete_card_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_read_card_by_id(db: Session, card_id: int):
        return

    monkeypatch.setattr(crud, "read_card_by_id", mock_read_card_by_id)
    response = test_client.delete("/cards/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Card with id=1 is not found"
