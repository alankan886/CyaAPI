from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models import Stack, Card, CardDetail
from app import crud


def test_create_card_detail(test_client: TestClient, test_db_session: Session):
    new_stack = Stack(name="stack1")
    new_card = Card(name="card1", stack_id=1)
    test_db_session.add(new_stack)
    test_db_session.add(new_card)
    test_db_session.commit()
    test_db_session.refresh(new_stack)
    test_db_session.refresh(new_card)

    test_request_data = {
        "card_id": 1,
        "quality": 3,
        "easiness": 2.5,
        "interval": 1,
        "repetitions": 1,
        "last_review": "2021-01-01"
    }
    response = test_client.post("/card_details", json=test_request_data)
    assert response.status_code == 201
    data = response.json()

    for k, v in test_request_data.items():
        assert data[k] == v

    assert "id" in data
    assert data["next_review"] == "2021-01-02"
    assert data["latest"] is True
    card_detail_id = data["id"]

    response = test_client.get(f"/card_details/{card_detail_id}")
    assert response.status_code == 200
    data = response.json()
    for k, v in test_request_data.items():
        assert data[k] == v

    assert data["next_review"] == "2021-01-02"
    assert data["latest"] is True
    assert data["id"] == card_detail_id


def test_update_card_detail(test_client: TestClient, test_db_session: Session):
    # TODO: I need to check when values are changed, new values are being updated
    # The key here is when you update a card_detail, it should update the next card_detail, an that would go recursively??
    new_stack = Stack(name="stack1")
    test_db_session.add(new_stack)
    stack = crud.read_stack_by_name(test_db_session, "stack1")
    new_card = Card(name="card1", stack_id=stack.id)
    test_db_session.add(new_card)
    card = crud.read_card_by_name(test_db_session, "card1")
    test_data = {
        "card_id": card.id,
        "quality": 3,
        "easiness": 2.56,
        "interval": 27,
        "repetitions": 4,
        "last_review": "2021-01-01",
        "next_review": "2021-01-28",
        "latest": True
    }
    new_card_detail = CardDetail(**test_data)
    test_db_session.add(new_card_detail)
    test_db_session.commit()
    test_db_session.refresh(new_stack)
    test_db_session.refresh(new_card)
    test_db_session.refresh(new_card_detail)
    test_request_data = {
        "card_id": card.id,
        "quality": 5,
        "easiness": 2.56,
        "interval": 27,
        "repetitions": 4,
        "last_review": "2021-01-01"
    }
    test_response_data = {
        "id": new_card_detail.id,
        "card_id": card.id,
        "quality": 5,
        "easiness": 2.8000000000000003,
        "interval": 27,
        "repetitions": 4,
        "last_review": "2021-01-01",
        "next_review": "2021-01-28",
        "latest": True
    }
    response = test_client.put(f"/card_details/{new_card_detail.id}", json=test_request_data)
    assert response.status_code == 200
    data = response.json()
    assert data == test_response_data
