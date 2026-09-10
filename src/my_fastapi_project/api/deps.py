from fastapi import HTTPException, status, Depends
from typing import Annotated

from my_fastapi_project.repositories.user_repo import UserRepository
from my_fastapi_project.services.user_service import UserService


def get_user_repo() -> UserRepository:
    return UserRepository()


def get_user_service(
        repo: Annotated[UserRepository, Depends(get_user_repo)],
) -> UserService:
    return UserService(repo)


UserServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_current_user(
        username: str,
        service: UserServiceDep,
) -> dict:
    user = service.get_user(username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户'{username}'不存在"
        )
    return user

CurrentUserDep = Annotated[dict, Depends(get_current_user)]
