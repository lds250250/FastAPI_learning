from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI()

"""
任务 1（订单模型）：
定义一个 Order 模型，包含 order_id（整数）、customer_name（字符串）和 total_amount（浮点数）。
要求：前端传参和返回时，字段名必须是驼峰命名（orderId, customerName, totalAmount）。
每个字段都要加上 Field 校验和 description。
写一个 GET /orders/1 接口返回该订单。
任务 2（动态排除）：
定义一个 Article 模型，包含 title（字符串）和 content（字符串）。
每个字段加上 Field 校验和 description。
写一个 GET /articles/1 接口，不使用 exclude=True，而是在 return 的时候，使用 model_dump() 的参数，临时排除掉 content 字段（模拟列表页只展示标题，不展示正文）。
"""


class User(BaseModel):
    username: str = Field(..., min_length=1, max_length=20, description="用户名字")
    email: str = Field(..., description="用户邮箱")
    password: str = Field(..., min_length=6,
                          description="用户密码，至少6位", exclude=True)


class Product(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    product_name: str = Field(..., alias="productName",
                              min_length=1, max_length=50, description="商品名称")
    unit_price: float = Field(..., alias="unitPrice",
                              gt=0, description="商品单价，必须大于0")


@app.post("/users/me", response_model=User)
async def get_product():
    return Product(product_name="机械键盘", unit_price=299.99)


class Order(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    order_id: int = Field(..., alias="orderId", description="订单ID")
    customer_name: str = Field(..., alias="customerName", description="客户名称")
    total_amount: float = Field(..., alias="totalAmount",
                                gt=0, description="订单总金额")


@app.get("/orders/1", response_model=Order)
async def get_order():
    return Order(order_id=1, customer_name="张三", total_amount=100.50)
