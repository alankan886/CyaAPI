def test_read_all_boards(test_client):
    test_response_payload = [{"id": 1, "name": "board1"}]

    def mock_get_board_by_id(id):
        return test_response_payload

    # monkeypatch.setattr(crud, "get", mock_get_board_by_id)

    response = test_client.get("/boards")
    assert response.status_code == 200


def test_bad_read_all_boards(test_client):
    response = test_client.get("/boards")
    assert response.status_code == 404
    assert response.json() == {"detail": "No boards are found"}
