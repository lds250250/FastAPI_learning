from typing import Any

from my_fastapi_project.repositories.borrow_repo import BorrowRecordRepository


class BorrowService:
    def __init__(self, repo: BorrowRecordRepository):
        self.repo = repo

    async def list_mine(self, username: str) -> list[dict[str, Any]]:
        return await self.repo.list_by_username(username)
