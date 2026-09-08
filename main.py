from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from fastapi import HTTPException, Depends, status
from typing import Annotated

app = FastAPI()


class UserProfile(BaseModel):
    age: int = Field(..., gt=0, description="用户年龄")
    bio: str | None = Field(None, max_length=200, description="个人简历")


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="用户名")
    email: EmailStr = Field(..., description="用户邮箱")
    password: str = Field(..., min_length=8, description="用户密码")
    profile: UserProfile | None = Field(None, description="个人简介信息")


class UserResponse(BaseModel):
    username: str = Field(..., min_length=3, max_length=20, description="用户名")
    email: EmailStr = Field(..., description="用户邮箱")
    profile: UserProfile | None = Field(None, description="个人简介信息")


class UserUpdate(BaseModel):
    email: EmailStr | None = Field(None, description="用户邮箱")
    profile: UserProfile | None = Field(None, description="个人简介信息")


class PasswordUpdate(BaseModel):
    old_password: str = Field(..., min_length=8, description="用户密码")
    new_password: str = Field(..., min_length=8, description="用户密码")


fake_users_db = {}


async def get_user_by_username(username: str):
    if username not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"用户'{username}'不存在"
        )
    return fake_users_db[username]


@app.post("/users/register/", response_model=UserResponse, status_code=201)
async def register_user(user: UserCreate):
    hashed_password = f'hashed_{user.password}'

    fake_users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "profile": user.profile.model_dump() if user.profile else None
    }

    return fake_users_db[user.username]


@app.get("/users/{username}", response_model=UserResponse)
async def get_user(user_data: dict = Depends(get_user_by_username)):

    return user_data


@app.get("/users/", response_model=list[UserResponse])
async def get_users():
    return list(fake_users_db.values())


@app.put("/users/{username}/password", status_code=204)
async def password_update(password_data: PasswordUpdate, user_data: dict = Depends(get_user_by_username)):

    hashed_oldpassword = f'hashed_{password_data.old_password}'
    if user_data["password"] != hashed_oldpassword:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    hashed_newpassword = f'hashed_{password_data.new_password}'
    user_data["password"] = hashed_newpassword


@app.patch("/users/{username}", response_model=UserResponse)
async def user_update(user_update: UserUpdate, user_data: dict = Depends(get_user_by_username)):
    update_data = user_update.model_dump(exclude_unset=True)
    if "email" in update_data:
        user_data["email"] = update_data["email"]
    if "profile" in update_data:
        user_data["profile"] = update_data["profile"]


@app.delete("/users/{username}", status_code=204)
async def user_delete(user_data: dict = Depends(get_user_by_username)):
    del fake_users_db[user_data["username"]]
