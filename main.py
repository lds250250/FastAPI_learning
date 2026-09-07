from fastapi import FastAPI, Query
from pydantic import BaseModel, Field, TypeAdapter
from typing import Annotated

app = FastAPI()


PositiveInt = Annotated[int, Field(..., gt=0, description="必须为正整数")]
UsernameType = Annotated[str, Field(..., min_length=2,
                                    max_length=20, description="用户名，2-20个字符")]


class User(BaseModel):
    user_id = PositiveInt
    username = UsernameType
    age = PositiveInt


PageQuery = Annotated[int, Query(ge=1, description="页码，最小为1")]
SizeQuery = Annotated[int, Query(ge=1, le=100, description="每页数量，1-100之间")]


@app.post("/users/")
async def create_user(user: User):
    return user


@app.get("/items")
async def read_items(page: PageQuery, size: SizeQuery):
    return {"page": page, "size": size}

list_adapter = TypeAdapter(list[int])


@app.post("/validate-list/")
async def validate_list(numbers: list[int]):
    validated_list = list_adapter.validate_python(numbers)
    return {"validated_list": validated_list}

EmailType = Annotated[str,
                      Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$', description="邮箱地址，必须符合邮箱格式")]


class Subscriber(BaseModel):
    subscriber_id: PositiveInt
    email: EmailType
    age: PositiveInt


@app.post("/subscribers/")
async def create_subscriber(subscriber: Subscriber):
    return subscriber
