from datetime import date, timedelta

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Stack, Card
import pytest


def verify_resp_data_against_req_data(request_data, resp_data):
    for k, v in request_data.items():
        assert resp_data[k] == v


def test_create_card(test_client: TestClient, test_db_session: Session):
    new_stack = Stack(name="stack1")
    test_db_session.add(new_stack)
    test_db_session.commit()
    test_db_session.refresh(new_stack)
    test_request_data = {
        "name": "card1",
        "stack_id": new_stack.id,
        "quality": 4,
        "prev_easiness": 2.36,
        "prev_interval": 1,
        "prev_repetitions": 2,
        "prev_review_date": "2021-01-01"
    }

    response = test_client.post("/cards", json=test_request_data)
    assert response.status_code == 201
    data = response.json()
    verify_resp_data_against_req_data(test_request_data, data)

    assert data["easiness"] == 2.36
    assert data["interval"] == 6
    assert data["repetitions"] == 3
    assert data["review_date"] == "2021-01-07"
    assert "id" in data
    card_id = data["id"]

    response = test_client.get(f"/cards/{card_id}")
    assert response.status_code == 200
    data = response.json()
    verify_resp_data_against_req_data(test_request_data, data)

    assert data["easiness"] == 2.36
    assert data["interval"] == 6
    assert data["repetitions"] == 3
    assert data["review_date"] == "2021-01-07"
    assert data["id"] == card_id


def test_create_first_review_card(test_client: TestClient, test_db_session: Session):
    new_stack = Stack(name="stack1")
    test_db_session.add(new_stack)
    test_db_session.commit()
    test_db_session.refresh(new_stack)
    test_request_data = {
        "name": "card1",
        "stack_id": new_stack.id,
        "quality": 4,
        "prev_review_date": "2021-01-01"
    }

    response = test_client.post("/cards/first", json=test_request_data)
    assert response.status_code == 201
    data = response.json()
    verify_resp_data_against_req_data(test_request_data, data)

    assert data["prev_easiness"] == 2.5
    assert data["prev_interval"] == 1
    assert data["prev_repetitions"] == 1
    assert data["prev_review_date"] == "2021-01-01"
    assert data["easiness"] == 2.5000000000000004
    assert data["interval"] == 1
    assert data["repetitions"] == 2
    assert data["review_date"] == "2021-01-02"
    assert "id" in data
    card_id = data["id"]

    response = test_client.get(f"/cards/{card_id}")
    assert response.status_code == 200
    data = response.json()
    verify_resp_data_against_req_data(test_request_data, data)

    assert data["prev_easiness"] == 2.5
    assert data["prev_interval"] == 1
    assert data["prev_repetitions"] == 1
    assert data["prev_review_date"] == "2021-01-01"
    assert data["easiness"] == 2.5000000000000004
    assert data["interval"] == 1
    assert data["repetitions"] == 2
    assert data["review_date"] == "2021-01-02"
    assert data["id"] == card_id


def test_create_first_review_card_without_prev_review_date(test_client: TestClient, test_db_session: Session):
    new_stack = Stack(name="stack1")
    test_db_session.add(new_stack)
    test_db_session.commit()
    test_db_session.refresh(new_stack)
    test_request_data = {
        "name": "card1",
        "stack_id": new_stack.id,
        "quality": 4
    }

    response = test_client.post("/cards/first", json=test_request_data)
    assert response.status_code == 201
    data = response.json()
    verify_resp_data_against_req_data(test_request_data, data)

    assert data["prev_easiness"] == 2.5
    assert data["prev_interval"] == 1
    assert data["prev_repetitions"] == 1
    assert data["prev_review_date"] == str(date.today())
    assert data["easiness"] == 2.5000000000000004
    assert data["interval"] == 1
    assert data["repetitions"] == 2
    assert data["review_date"] == str(date.today() + timedelta(days=1))
    assert "id" in data
    card_id = data["id"]

    response = test_client.get(f"/cards/{card_id}")
    assert response.status_code == 200
    data = response.json()
    verify_resp_data_against_req_data(test_request_data, data)

    assert data["prev_easiness"] == 2.5
    assert data["prev_interval"] == 1
    assert data["prev_repetitions"] == 1
    assert data["prev_review_date"] == str(date.today())
    assert data["easiness"] == 2.5000000000000004
    assert data["interval"] == 1
    assert data["repetitions"] == 2
    assert data["review_date"] == str(date.today() + timedelta(days=1))
    assert data["id"] == card_id


def test_update_card(test_client: TestClient, test_db_session: Session):
    new_stack = Stack(name="stack1")
    test_db_session.add(new_stack)
    test_db_session.commit()
    test_db_session.refresh(new_stack)

    new_card = {
        "name": "card1",
        "stack_id": new_stack.id,
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
    new_card = Card(**new_card)
    test_db_session.add(new_card)
    test_db_session.commit()
    test_db_session.refresh(new_card)
    test_request_data = {
        "name": "new_card",
        "quality": 5,
        "prev_review_date": "2021-01-02"
    } 

    response = test_client.patch(f"/cards/{new_card.id}", json=test_request_data)
    assert response.status_code == 200
    data = response.json()
    verify_resp_data_against_req_data(test_request_data, data)

    assert data["prev_easiness"] == 2.5
    assert data["prev_interval"] == 1
    assert data["prev_repetitions"] == 1
    assert data["prev_review_date"] == "2021-01-02"
    assert data["easiness"] == 2.6
    assert data["interval"] == 1
    assert data["repetitions"] == 2
    assert data["review_date"] == "2021-01-03"
    assert "id" in data
    card_id = data["id"]

    response = test_client.get(f"/cards/{card_id}")
    assert response.status_code == 200
    data = response.json()
    verify_resp_data_against_req_data(test_request_data, data)

    assert data["prev_easiness"] == 2.5
    assert data["prev_interval"] == 1
    assert data["prev_repetitions"] == 1
    assert data["prev_review_date"] == "2021-01-02"
    assert data["easiness"] == 2.6
    assert data["interval"] == 1
    assert data["repetitions"] == 2
    assert data["review_date"] == "2021-01-03"
    assert data["id"] == card_id
