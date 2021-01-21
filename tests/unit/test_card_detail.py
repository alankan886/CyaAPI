from _pytest.monkeypatch import MonkeyPatch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import crud
from app import schemas, models

import pytest


@pytest.mark.skip
def test_create_card_detail():
    pass


@pytest.mark.skip
def test_delete_card_detail():
    pass


# I need to rethink how I want to read card_details for just one card or read all card_details.
@pytest.mark.skip
def test_read_card_details(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = [
        {
            "id": 1,
            "card_id": 1,
            "quality": 3,
            "easiness": 2.36,
            "interval": 1,
            "repetitions": 2,
            "last_review": "2021-01-01",
            "next_review": "2021-01-02"
        },
        {
            "id": 2,
            "card_id": 1,
            "quality": 4,
            "easiness": 2.67,
            "interval": 10,
            "repetitions": 3,
            "last_review": "2021-01-08",
            "next_review": "2021-01-18"
        }
    ]

    def mock_get_card_details_by_id(db: Session, card_id: int):
        return test_data

    monkeypatch.setattr(crud, "get_card_details_by_id", mock_get_card_details_by_id)
    response = test_client.get("/card_details/1")
    assert response.status_code == 200
    assert response.json() == test_data


@pytest.mark.skip
def test_read_card_details_not_found(test_client: TestClient, monkeypatch: MonkeyPatch):
    def mock_get_card_details_by_id(db: Session, card_id: int):
        return

    monkeypatch.setattr(crud, "get_card_details_by_id", mock_get_card_details_by_id)
    response = test_client.get("/card_details/1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Card details with id=1 not found"


@pytest.mark.skip
def test_read_card_detail(test_client: TestClient, monkeypatch: MonkeyPatch):
    test_data = {
        "id": 2,
        "card_id": 1,
        "quality": 4,
        "easiness": 2.67,
        "interval": 10,
        "repetitions": 3,
        "last_review": "2021-01-08",
        "next_review": "2021-01-18"
    }

    def mock_get_card_detail_by_id(db: Session, card_id: int, card_detail_id: int):
        return test_data

    monkeypatch.setattr(crud, "get_card_detail_by_id", mock_get_card_detail_by_id)
    response = test_client.get("/card_details/1?card_detail_id=2")
    assert response.status_code == 200
    assert response.json() == test_data
