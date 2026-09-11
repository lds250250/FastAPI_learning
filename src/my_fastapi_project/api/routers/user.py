from fastapi import APIRouter, HTTPException, status, Depends

from my_fastapi_project.schemas.user import UserCreate, UserResponse, UserUpdate, PasswordUpdate
from my_fastapi_project.api.deps import (
    UserServiceDep,
    CurrentUserDep,
    PaginationDep,
    get_caller_role,
    log_request,
    users_rate_limit,
    register_rate_limit,
    require_role,
    ROLE_ADMIN
)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[
        Depends(users_rate_limit),
        Depends(get_caller_role),
        Depends(log_request)
    ],
)


@router.post("/register/",
             response_model=UserResponse,
             status_code=201,
             dependencies=[Depends(register_rate_limit)],
             )
async def register_user(user: UserCreate, service: UserServiceDep):
    created = service.register(user)
    if created is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="用户名已存在"
        )
    return created


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
    service: UserServiceDep
):
    if not service.change_password(user_data["username"], password_data):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="旧密码不正确",
        )


@router.patch("/{username}", response_model=UserResponse)
async def user_update(
    payload: UserUpdate,
    user_data: CurrentUserDep,
    service: UserServiceDep
):
    return service.update_user(user_data["username"], payload)


@router.delete(
    "/{username}",
    status_code=204,
    dependencies=[Depends(require_role(ROLE_ADMIN))],
)
async def user_delete(user_data: CurrentUserDep, service: UserServiceDep):
    service.delete_user(user_data["username"])
