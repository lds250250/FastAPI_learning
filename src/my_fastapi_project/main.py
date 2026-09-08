from fastapi import FastAPI
from my_fastapi_project.routers.user import router as user_router

app = FastAPI()
app.include_router(user_router)
