from fastapi import APIRouter, HTTPException, status
from my_fastapi_project.schemas.user import UserCreate, UserResponse, UserUpdate, PasswordUpdate
from my_fastapi_project.api.deps import UserDependency, get_user_by_username, fake_users_db


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register/", response_model=UserResponse, status_code=201)
async def register_user(user: UserCreate):
    hashed_password = f'hashed_{user.password}'
    fake_users_db[user.username] = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "profile": user.profile.model_dump() if user.profile else None
    }
    return fake_users_db[user.username]


@router.get("/{username}", response_model=UserResponse)
async def get_user(user_data: UserDependency):
    return user_data


@router.get("/", response_model=list[UserResponse])
async def get_users():
    return list(fake_users_db.values())


@router.put("/{username}/password", status_code=204)
async def password_update(password_data: PasswordUpdate, user_data: UserDependency):
    hashed_oldpassword = f'hashed_{password_data.old_password}'
    if user_data["password"] != hashed_oldpassword:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    hashed_newpassword = f'hashed_{password_data.new_password}'
    user_data["password"] = hashed_newpassword


@router.patch("/{username}", response_model=UserResponse)
async def user_update(user_update: UserUpdate, user_data: UserDependency):
    update_data = user_update.model_dump(exclude_unset=True)
    if "email" in update_data:
        user_data["email"] = update_data["email"]
    if "profile" in update_data:
        user_data["profile"] = update_data["profile"]


@router.delete("/{username}", status_code=204)
async def user_delete(user_data: UserDependency):
    del fake_users_db[user_data["username"]]
