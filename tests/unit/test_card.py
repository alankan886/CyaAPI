from _pytest.monkeypatch import MonkeyPatch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app import schemas, models


def test_read_card(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = {"id": 1, "name": "card1", "board_id": 1}

    def mock_get_card_by_id(db: Session, card_id: int):
        return test_data

    monkeypatch.setattr(crud, "get_card_by_id", mock_get_card_by_id)
    response = test_client.get("/cards/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_card_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_get_card_by_id(db: Session, card_id: int):
        return

    monkeypatch.setattr(crud, "get_card_by_id", mock_get_card_by_id)
    response = test_client.get("/cards/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Card with id=1 not found"


def test_read_cards(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = [
        {
            "id": 1,
            "name": "card1",
            "board_id": 1
        },
        {
            "id": 2,
            "name": "card2",
            "board_id": 1
        },
        {
            "id": 3,
            "name": "card3",
            "board_id": 2
        }
    ]

    def mock_get_cards(db: Session):
        return test_data

    monkeypatch.setattr(crud, "get_cards", mock_get_cards)
    response = test_client.get("/cards")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_cards_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_get_cards(db: Session):
        return

    monkeypatch.setattr(crud, "get_cards", mock_get_cards)
    response = test_client.get("/cards")
    assert response.status_code == 404
    assert response.json()["detail"] == "No cards are found"


def test_create_card(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_request_data = {
        "name": "card1",
        "board_id": 1
    }
    test_response_data = {
        "id": 1,
        "name": "card1",
        "board_id": 1
    }

    def mock_create_card(db: Session, card: schemas.CardCreate):
        return test_response_data

    def mock_get_card_by_name(db: Session, card_name: str):
        return

    monkeypatch.setattr(crud, "create_card", mock_create_card)
    monkeypatch.setattr(crud, "get_card_by_name", mock_get_card_by_name)
    response = test_client.post("/cards", json=test_request_data)
    assert response.status_code == 200
    assert response.json() == test_response_data


def test_create_card_already_exists(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_request_data = {
        "name": "card1",
        "board_id": 1
    }

    card_exists = {
        "id": 1,
        "name": "card1",
        "board_id": 1
    }

    def mock_get_card_by_name(db: Session, card_name: str):
        return card_exists

    monkeypatch.setattr(crud, "get_card_by_name", mock_get_card_by_name)
    response = test_client.post("/cards", json=test_request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Card with the name card1 has already exists"


def test_delete_card(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = {
        "id": 1,
        "name": "card1",
        "board_id": 1
    }

    def mock_get_card_by_id(db: Session, card_id: int):
        return test_data

    def mock_delete_card(db: Session, card: schemas.Card):
        return test_data

    monkeypatch.setattr(crud, "get_card_by_id", mock_get_card_by_id)
    monkeypatch.setattr(crud, "delete_card", mock_delete_card)
    response = test_client.delete("/cards/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_delete_card_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_get_card_by_id(db: Session, card_id: int):
        return

    monkeypatch.setattr(crud, "get_card_by_id", mock_get_card_by_id)
    response = test_client.delete("/cards/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Card with id=1 is not found"
