from fastapi import HTTPException, status, Depends
from typing import Annotated

from my_fastapi_project.repositories.user_repo import UserRepository


_repo = UserRepository()


async def get_user_by_username(username: str):
    user = _repo.get(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户'{username}'不存在"
        )
    return user

UserDependency = Annotated[dict, Depends(get_user_by_username)]
