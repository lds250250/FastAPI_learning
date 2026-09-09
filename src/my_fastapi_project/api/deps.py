from fastapi import HTTPException, status, Depends
from typing import Annotated

fake_users_db = {}


async def get_user_by_username(username: str):
    if username not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户'{username}'不存在"
        )
    return fake_users_db[username]

UserDependency = Annotated[dict, Depends(get_user_by_username)]
