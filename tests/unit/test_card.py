from _pytest.monkeypatch import MonkeyPatch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app import schemas, models


def test_read_card(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = {
        "id": 1,
        "name": "card1",
        "stack_id": 1,
        "quality": 3,
        "prev_easiness": 2.5,
        "easiness": 2.36,
        "prev_interval": 1,
        "interval": 1,
        "prev_repetitions": 1,
        "repetitions": 2,
        "prev_review_date": "2021-01-01",
        "review_date": "2021-01-02",
    }

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
            "quality": 3,
            "prev_easiness": 2.5,
            "easiness": 2.36,
            "prev_interval": 1,
            "interval": 1,
            "prev_repetitions": 1,
            "repetitions": 2,
            "prev_review_date": "2021-01-01",
            "review_date": "2021-01-02",
        },
        {
            "id": 2,
            "name": "card2",
            "stack_id": 1,
            "quality": 5,
            "prev_easiness": 2.36,
            "easiness": 2.46,
            "prev_interval": 1,
            "interval": 6,
            "prev_repetitions": 2,
            "repetitions": 3,
            "prev_review_date": "2021-01-02",
            "review_date": "2021-01-08",
        },
        {
            "id": 3,
            "name": "card3",
            "stack_id": 2,
            "quality": 3,
            "prev_easiness": 2.5,
            "easiness": 2.36,
            "prev_interval": 1,
            "interval": 1,
            "prev_repetitions": 1,
            "repetitions": 2,
            "prev_review_date": "2021-01-01",
            "review_date": "2021-01-02",
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


def test_get_cards_due_today(test_client: TestClient, monkeypatch: MonkeyPatch):
    response_data = [
        {
            "id": 1,
            "name": "card1",
            "stack_id": 1,
            "quality": 3,
            "prev_easiness": 2.5,
            "easiness": 2.36,
            "prev_interval": 1,
            "interval": 1,
            "prev_repetitions": 1,
            "repetitions": 2,
            "prev_review_date": "2021-01-01",
            "review_date": "2021-01-02",
        }
    ]

    def mock_read_cards_due(db: Session, card_id: int):
        return response_data

    monkeypatch.setattr(crud, "read_cards_due", mock_read_cards_due)
    response = test_client.get("/cards/?filter=today")
    assert response.status_code == 200
    assert response.json() == response_data


def test_create_card(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_request_data = {
        "name": "card1",
        "stack_id": 1,
        "quality": 4,
        "prev_easiness": 2.36,
        "prev_interval": 1,
        "prev_repetitions": 2,
        "prev_review_date": "2021-01-01",
    }
    test_response_data = {
        "id": 1,
        "name": "card1",
        "stack_ids": 1,
        "quality": 3,
        "prev_easiness": 2.5,
        "easiness": 2.36,
        "prev_interval": 1,
        "interval": 1,
        "prev_repetitions": 1,
        "repetitions": 2,
        "prev_review_date": "2021-01-01",
        "review_date": "2021-01-02"
    }

    def mock_create_card(db: Session, card: schemas.CardCreate, is_first_review: bool):
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
        "stack_id": 1,
        "quality": 4,
        "prev_easiness": 2.36,
        "prev_interval": 1,
        "prev_repetitions": 2,
        "prev_review_date": "2021-01-01"
    }

    card_exists = {
        "id": 1,
        "name": "card1",
        "stack_id": 1,
        "quality": 3,
        "prev_easiness": 2.5,
        "easiness": 2.36,
        "prev_interval": 1,
        "interval": 1,
        "prev_repetitions": 1,
        "repetitions": 2,
        "prev_review_date": "2021-01-01",
        "review_date": "2021-01-02",
    }

    def mock_read_card_by_name(db: Session, card_name: str):
        return card_exists

    monkeypatch.setattr(crud, "read_card_by_name", mock_read_card_by_name)
    response = test_client.post("/cards", json=test_request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Card with the name card1 has already exists"


def test_create_first_card(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_request_data = {
        "name": "card1",
        "stack_id": 1,
        "quality": 4,
        "prev_review_date": "2021-01-01"
    }
    test_response_data = {
        "id": 1,
        "name": "card1",
        "stack_id": 1,
        "quality": 3,
        "prev_easiness": 2.5,
        "easiness": 2.36,
        "prev_interval": 1,
        "interval": 1,
        "prev_repetitions": 1,
        "repetitions": 2,
        "prev_review_date": "2021-01-01",
        "review_date": "2021-01-02",
    }

    def mock_create_card(db: Session, card: schemas.CardCreate, is_first_review: bool):
        return test_response_data

    def mock_read_card_by_name(db: Session, card_name: str):
        return

    monkeypatch.setattr(crud, "create_card", mock_create_card)
    monkeypatch.setattr(crud, "read_card_by_name", mock_read_card_by_name)
    response = test_client.post("/cards/first", json=test_request_data)
    assert response.status_code == 201
    assert response.json() == test_response_data


def test_create_first_card_already_exists(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_request_data = {
        "name": "card1",
        "stack_id": 1,
        "quality": 4,
        "prev_review_date": "2021-01-01"
    }

    card_exists = {
        "id": 1,
        "name": "card1",
        "stack_id": 1,
        "quality": 3,
        "prev_easiness": 2.5,
        "easiness": 2.36,
        "prev_interval": 1,
        "interval": 1,
        "prev_repetitions": 1,
        "repetitions": 2,
        "prev_review_date": "2021-01-01",
        "review_date": "2021-01-02",
    }

    def mock_read_card_by_name(db: Session, card_name: str):
        return card_exists

    monkeypatch.setattr(crud, "read_card_by_name", mock_read_card_by_name)
    response = test_client.post("/cards/first", json=test_request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Card with the name card1 has already exists"


def test_patch_card(test_client: TestClient, monkeypatch: MonkeyPatch):
    before_udpate = {
        "id": 1,
        "name": "oldname",
        "stack_id": 1,
        "quality": 3,
        "prev_easiness": 2.5,
        "easiness": 2.36,
        "prev_interval": 1,
        "interval": 1,
        "prev_repetitions": 1,
        "repetitions": 2,
        "prev_review_date": "2021-01-01",
        "review_date": "2021-01-02",
    }
    # you should only be able to modify name, stack_id, quality and the prev_ values,
    # the rest should be calculated by the api.
    test_request_data = {
        "name": "newname",
        "stack_id": 2,
        "quality": 5
    }
    after_update = {
        "id": 1,
        "name": "newname",
        "stack_id": 2,
        "quality": 5,
        "prev_easiness": 2.5,
        "easiness": 2.6,
        "prev_interval": 1,
        "interval": 1,
        "prev_repetitions": 1,
        "repetitions": 2,
        "prev_review_date": "2021-01-01",
        "review_date": "2021-01-02"
    }

    def mock_read_card_by_id(db: Session, card_id: int):
        return before_udpate

    def mock_update_card(db: Session, card: schemas.Card, new_info: schemas.CardOptionalAttrs):
        return after_update

    monkeypatch.setattr(crud, "read_card_by_id", mock_read_card_by_id)
    monkeypatch.setattr(crud, "update_card", mock_update_card)
    response = test_client.patch("/cards/1", json=test_request_data)
    assert response.status_code == 200
    assert response.json() == after_update
    assert response.json() != before_udpate


def test_patch_card_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_request_data = {
        "id": 1,
        "name": "newname",
        "stack_id": 2,
        "quality": 5
    }
    test_response_data = {
        "id": 1,
        "name": "newname",
        "stack_id": 2,
        "quality": 5,
        "prev_easiness": 2.5,
        "easiness": 2.6,
        "prev_interval": 1,
        "interval": 1,
        "prev_repetitions": 1,
        "repetitions": 2,
        "prev_review_date": "2021-01-01",
        "review_date": "2021-01-02"
    }

    def mock_read_card_by_id(db: Session, card_id: int):
        return

    def mock_create_card(db: Session, card: schemas.StackCreate):
        return test_response_data

    monkeypatch.setattr(crud, "read_card_by_id", mock_read_card_by_id)
    monkeypatch.setattr(crud, "create_card", mock_create_card)
    response = test_client.patch("/cards/1", json=test_request_data)
    assert response.status_code == 201
    assert response.json() == test_response_data


def test_patch_next_card(test_client: TestClient, monkeypatch: MonkeyPatch):
    before_update = {
        "id": 1,
        "name": "card1",
        "stack_id": 1,
        "quality": 5,
        "prev_easiness": 2.5,
        "easiness": 2.6,
        "prev_interval": 1,
        "interval": 1,
        "prev_repetitions": 1,
        "repetitions": 2,
        "prev_review_date": "2021-01-01",
        "review_date": "2021-01-02"
    }
    test_request_data = {
        "quality": 4,
        "prev_review_date": "2021-01-02"
    }
    after_update = {
        "id": 1,
        "name": "card1",
        "stack_id": 1,
        "quality": 4,
        "prev_easiness": 2.6,
        "easiness": 2.6,
        "prev_interval": 1,
        "interval": 6,
        "prev_repetitions": 2,
        "repetitions": 3,
        "prev_review_date": "2021-01-02",
        "review_date": "2021-01-08"
    }

    def mock_read_card_by_id(db: Session, card_id: int):
        return before_update

    def mock_update_card(db: Session, card: schemas.Card, new_info: schemas.CardOptionalAttrs):
        return after_update

    monkeypatch.setattr(crud, "read_card_by_id", mock_read_card_by_id)
    monkeypatch.setattr(crud, "update_card", mock_update_card)
    response = test_client.patch("/cards/1/next", json=test_request_data)
    assert response.status_code == 200
    assert response.json() == after_update


def test_patch_next_card_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_read_card_by_id(db: Session, card_id: int):
        return

    test_request_data = {
        "quality": 4,
        "prev_review_date": "2021-01-02"
    }
    monkeypatch.setattr(crud, "read_card_by_id", mock_read_card_by_id)
    response = test_client.patch("/cards/1/next", json=test_request_data)
    assert response.status_code == 200
    assert response.json()["detail"] == "Card with id=1 not found"


def test_delete_card(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = {
        "id": 1,
        "name": "card1",
        "stack_id": 1,
        "quality": 5,
        "prev_easiness": 2.5,
        "easiness": 2.6,
        "prev_interval": 1,
        "interval": 1,
        "prev_repetitions": 1,
        "repetitions": 2,
        "prev_review_date": "2021-01-01",
        "review_date": "2021-01-02"
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
    assert response.json()["detail"] == "Card with id=1 not found"
