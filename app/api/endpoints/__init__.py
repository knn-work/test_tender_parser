from fastapi import APIRouter

from app.api.endpoints import trends

app_router = APIRouter()

# Подключение маршрутов
app_router.include_router(trends.router, prefix="/trends", tags=["trends"])