from _pytest.monkeypatch import MonkeyPatch
from fastapi.testclient import TestClient

from app import crud
from app import schemas, models
from sqlalchemy.orm import Session


def test_read_board(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = {
        "id": 1,
        "name": "board1",
        "size": 0,
        "cards": []
    }

    def mock_get_board_by_id(db: Session, board_id: int):
        return test_data

    monkeypatch.setattr(crud, "get_board_by_id", mock_get_board_by_id)

    response = test_client.get("/boards/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_board_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_get_board_by_id(db: Session, board_id: int):
        return None

    monkeypatch.setattr(crud, "get_board_by_id", mock_get_board_by_id)

    response = test_client.get("/boards/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Board not found"


def test_read_all_boards(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = [
        {
            "id": 1,
            "name": "board1",
            "size": 0,
            "cards": []
        },
        {
            "id": 2,
            "name": "board2",
            "size": 1,
            "cards": [
                {
                    "id": 1,
                    "name": "card1",
                    "board_id": 2
                }
            ]
        }
    ]

    def mock_get_boards(db: Session):
        return test_data

    monkeypatch.setattr(crud, "get_boards", mock_get_boards)

    response = test_client.get("/boards")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_all_boards_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_get_boards(db: Session):
        return None

    monkeypatch.setattr(crud, "get_boards", mock_get_boards)

    response = test_client.get("/boards")
    assert response.status_code == 404
    assert response.json()["detail"] == "No boards are found"


def test_create_board(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_request_data = {
        "name": "board1"
    }

    test_response_data = {
        "id": 1,
        "name": "board1",
        "size": 0,
        "cards": []
    }

    def mock_create_board(db: Session, board: schemas.BoardCreate):
        return test_response_data

    def mock_get_board_by_name(db: Session, board_name: str):
        return None

    monkeypatch.setattr(crud, "create_board", mock_create_board)
    monkeypatch.setattr(crud, "get_board_by_name", mock_get_board_by_name)

    response = test_client.post("/boards", json=test_request_data)
    assert response.status_code == 200
    assert response.json() == test_response_data


def test_reate_board_board_already_exists(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_request_data = {
        "name": "board1"
    }

    board_exists = {
        "id": 1,
        "name": "board1",
        "size": 0,
        "cards": []
    }

    def mock_get_board_by_name(db: Session, board_name: str):
        return board_exists

    monkeypatch.setattr(crud, "get_board_by_name", mock_get_board_by_name)

    response = test_client.post("/boards", json=test_request_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Board with the name board1 has already exists"


def test_delete_board(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_request_data = models.Board(id=1, name="board1", size=0, cards=[])
    test_response_data = {
        "id": 1,
        "name": "board1",
        "size": 0,
        "cards": []
    }

    def mock_get_board_by_id(db: Session, board_id: int):
        return test_request_data

    def mock_remove_board(db: Session, board: schemas.Board):
        return None

    monkeypatch.setattr(crud, "get_board_by_id", mock_get_board_by_id)
    monkeypatch.setattr(crud, "remove_board", mock_remove_board)

    response = test_client.delete("/boards/1")
    assert response.status_code == 200
    assert response.json() == test_response_data


def test_delete_board_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_get_board_by_id(db: Session, board_id: int):
        return None

    monkeypatch.setattr(crud, "get_board_by_id", mock_get_board_by_id)

    response = test_client.delete("/boards/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Board with id 1 is not found"
