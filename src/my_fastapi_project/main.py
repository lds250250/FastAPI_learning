from fastapi import FastAPI
from my_fastapi_project.config import get_settings 
from my_fastapi_project.routers.user import router as user_router

settings = get_settings() 

app = FastAPI(title=settings.APP_NAME, debug=settings.DEBUG)  
app.include_router(user_router)  
