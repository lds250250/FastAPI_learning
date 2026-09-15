from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from my_fastapi_project.api.deps import UserServiceDep, login_rate_limit
from my_fastapi_project.core.security import create_access_token
from my_fastapi_project.schemas.token import Token
from my_fastapi_project.api.deps import CallerDep, UserServiceDep, login_rate_limit

router = APIRouter(tags=["auth"])


@router.post("/token", response_model=Token, dependencies=[Depends(login_rate_limit)])
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: UserServiceDep,
):
    user = service.authenticate(form_data.username, form_data.password)
    return Token(access_token=create_access_token(user["username"]))


@router.post("/token/refresh", response_model=Token)
async def refresh_token(caller: CallerDep):
    return Token(access_token=create_access_token(caller["username"]))
