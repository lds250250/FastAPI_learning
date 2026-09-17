def test_book_detail_still_works_when_redis_is_down(
    dead_redis, auth_client, sample_book
):
    response = auth_client.get(f"/books/{sample_book}")

    assert response.status_code == 200
    assert response.json()["title"] == "流畅的Python"


def test_rate_limit_is_bypassed_when_redis_is_down(dead_redis, auth_client):
    for _ in range(10):
        assert auth_client.get("/books/").status_code == 200
