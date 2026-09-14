# create / get / exists / list_all / update / delete
def test_create_get(empty_book_repo):
    empty_book_repo.create("12345", {"isbn": "12345", "title": "流畅的Python"})
    assert empty_book_repo.get("12345")["title"] == "流畅的Python"


def test_exists(empty_book_repo):
    assert empty_book_repo.exists("12345") is False
    empty_book_repo.create("12345", {"isbn": "12345"})
    assert empty_book_repo.exists("12345") is True


def test_list_all(empty_book_repo):
    empty_book_repo.create("12345", {"isbn": "12345", "title": "流畅的Python"})
    assert empty_book_repo.list_all() == [{"isbn": "12345", "title": "流畅的Python"}]


def test_update(empty_book_repo):
    empty_book_repo.create("12345", {"isbn": "12345", "title": "流畅的Python"})
    empty_book_repo.update("12345", {"title": "game start"})
    assert empty_book_repo.get("12345")["title"] == "game start"


def test_delete(empty_book_repo):
    empty_book_repo.create("12345", {"isbn": "12345"})
    assert empty_book_repo.delete("12345") is True
    assert empty_book_repo.delete("12345") is False
