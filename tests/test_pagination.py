from my_fastapi_project.api.deps import Pagination


def test_offset_of_first_page_is_zero():
    pagination = Pagination(page=1, size=10)
    assert pagination.offset == 0


def test_offset_of_second_page_skips_one_page():
    pagination = Pagination(page=2, size=10)
    assert pagination.offset == 10


def test_limit_equals_size():
    pagination = Pagination(page=3, size=25)
    assert pagination.limit == 25
    assert pagination.offset == 50
