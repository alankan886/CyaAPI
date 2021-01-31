from _pytest.monkeypatch import MonkeyPatch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app import schemas, models


def test_get_stack(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = {
        "id": 1,
        "name": "stack1",
        "cards": []
    }

    def mock_read_stack_by_id(db: Session, stack_id: int):
        return test_data

    monkeypatch.setattr(crud, "read_stack_by_id", mock_read_stack_by_id)
    response = test_client.get("/stacks/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_get_stack_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_read_stack_by_id(db: Session, stack_id: int):
        return None

    monkeypatch.setattr(crud, "read_stack_by_id", mock_read_stack_by_id)
    response = test_client.get("/stacks/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Stack with id=1 not found"


def test_get_boards(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = [
        {
            "id": 1,
            "name": "stack1",
            "cards": []
        },
        {
            "id": 2,
            "name": "stack2",
            "cards": [
                {
                    "id": 1,
                    "name": "card1",
                    "stack_id": 2
                }
            ]
        }
    ]

    def mock_read_stacks(db: Session):
        return test_data

    monkeypatch.setattr(crud, "read_stacks", mock_read_stacks)
    response = test_client.get("/stacks")
    assert response.status_code == 200
    assert response.json() == test_data


def test_get_stacks_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_read_stacks(db: Session):
        return None

    monkeypatch.setattr(crud, "read_stacks", mock_read_stacks)
    response = test_client.get("/stacks")
    assert response.status_code == 200
    assert response.json() == []


def test_get_cards_in_stack(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = [
        {
            "id": 1,
            "name": "card1",
            "stack_id": 2
        },
        {
            "id": 2,
            "name": "card2",
            "stack_id": 2
        }
    ]

    def mock_read_cards_in_stacks(db: Session, stack_id: int):
        return test_data

    monkeypatch.setattr(crud, "read_cards_in_stacks", mock_read_cards_in_stacks)
    response = test_client.get("/stacks/2/cards")
    assert response.status_code == 200
    assert response.json() == test_data


def test_get_cards_in_stack_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_read_cards_in_stacks(db: Session, stack_id: int):
        return []

    monkeypatch.setattr(crud, "read_cards_in_stacks", mock_read_cards_in_stacks)
    response = test_client.get("/stacks/2/cards")
    assert response.status_code == 200
    assert response.json() == []


def test_post_stack(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_request_data = {
        "name": "stack1"
    }

    test_response_data = {
        "id": 1,
        "name": "stack1",
        "cards": []
    }

    def mock_create_stack(db: Session, stack: schemas.StackCreate):
        return test_response_data

    def mock_read_stack_by_name(db: Session, stack_name: str):
        return

    monkeypatch.setattr(crud, "create_stack", mock_create_stack)
    monkeypatch.setattr(crud, "read_stack_by_name", mock_read_stack_by_name)
    response = test_client.post("/stacks", json=test_request_data)
    assert response.status_code == 201
    assert response.json() == test_response_data


def test_post_stack_already_exists(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_request_data = {
        "name": "stack1"
    }

    stack_exists = {
        "id": 1,
        "name": "stack1",
        "cards": []
    }

    def mock_read_stack_by_name(db: Session, stack_name: str):
        return stack_exists

    monkeypatch.setattr(crud, "read_stack_by_name", mock_read_stack_by_name)
    response = test_client.post("/stacks", json=test_request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Stack with the name stack1 has already exists"


def test_put_stack(test_client: TestClient, monkeypatch: MonkeyPatch):
    before_udpate = {
        "id": 1,
        "name": "oldname",
        "cards": []
    }

    after_update = {
        "id": 1,
        "name": "newname",
        "cards": []
    }

    def mock_read_stack_by_id(db: Session, stack_id: int):
        return before_udpate

    def mock_update_stack(db: Session, old_stack: schemas.Stack, new_stack: schemas.StackCreate):
        return after_update

    monkeypatch.setattr(crud, "read_stack_by_id", mock_read_stack_by_id)
    monkeypatch.setattr(crud, "update_stack", mock_update_stack)
    response = test_client.put("/stacks/1", json=after_update)
    assert response.status_code == 200
    assert response.json() == after_update
    assert response.json() != before_udpate


def test_put_stack_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = {
        "id": 1,
        "name": "newname",
        "cards": []
    }

    def mock_read_stack_by_id(db: Session, stack_id: int):
        return []

    def mock_create_stack(db: Session, stack: schemas.StackCreate):
        return test_data

    monkeypatch.setattr(crud, "read_stack_by_id", mock_read_stack_by_id)
    monkeypatch.setattr(crud, "create_stack", mock_create_stack)
    response = test_client.put("/stacks/1", json=test_data)
    assert response.status_code == 201
    assert response.json() == test_data


def test_delete_stack(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = {
        "id": 1,
        "name": "stack1",
        "cards": []
    }

    def mock_read_stack_by_id(db: Session, stack_id: int):
        return test_data

    def mock_delete_stack(db: Session, stack: schemas.Stack):
        return

    monkeypatch.setattr(crud, "read_stack_by_id", mock_read_stack_by_id)
    monkeypatch.setattr(crud, "delete_stack", mock_delete_stack)
    response = test_client.delete("/stacks/1")
    assert response.status_code == 204
    assert response.json() is None


def test_delete_stack_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_read_stack_by_id(db: Session, stack_id: int):
        return

    monkeypatch.setattr(crud, "read_stack_by_id", mock_read_stack_by_id)
    response = test_client.delete("/stacks/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Stack with id=1 is not found"
