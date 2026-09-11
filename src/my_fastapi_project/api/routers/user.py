from fastapi import APIRouter, Depends

from my_fastapi_project.api.deps import (
    ROLE_ADMIN,
    CurrentUserDep,
    PaginationDep,
    UserServiceDep,
    get_caller_role,
    register_rate_limit,
    require_role,
    users_rate_limit,
)
from my_fastapi_project.schemas.user import (
    PasswordUpdate,
    UserCreate,
    UserResponse,
    UserUpdate,
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[
        Depends(users_rate_limit),
        Depends(get_caller_role),
    ],
)


@router.post(
    "/register/",
    response_model=UserResponse,
    status_code=201,
    dependencies=[Depends(register_rate_limit)],
)
async def register_user(user: UserCreate, service: UserServiceDep):
    return service.register(user)


@router.get("/{username}", response_model=UserResponse)
async def get_user(user_data: CurrentUserDep):
    return user_data


@router.get("/", response_model=list[UserResponse])
async def get_users(pagination: PaginationDep, service: UserServiceDep):
    return service.list_users(pagination.offset, pagination.limit)


@router.put("/{username}/password", status_code=204)
async def password_update(
    password_data: PasswordUpdate,
    user_data: CurrentUserDep,
    service: UserServiceDep,
):
    service.change_password(user_data["username"], password_data)


@router.patch("/{username}", response_model=UserResponse)
async def user_update(
    payload: UserUpdate, user_data: CurrentUserDep, service: UserServiceDep
):
    return service.update_user(user_data["username"], payload)


@router.delete(
    "/{username}",
    status_code=204,
    dependencies=[Depends(require_role(ROLE_ADMIN))],
)
async def user_delete(user_data: CurrentUserDep, service: UserServiceDep):
    service.delete_user(user_data["username"])
