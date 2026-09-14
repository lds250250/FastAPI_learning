def test_response_has_request_id(client):
    response = client.get("/health")

    assert "x-request-id" in response.headers


def test_client_supplied_request_id_is_reused(client):
    response = client.get("/health", headers={"x-request-id": "my-test-id"})

    assert response.headers["x-request-id"] == "my-test-id"


def test_request_id_is_added_even_on_404(client):
    response = client.get("/this-path-does-not-exist")

    assert response.status_code == 404
    assert "x-request-id" in response.headers
