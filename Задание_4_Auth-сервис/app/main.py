"""
Главный модуль приложения FastAPI.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, users
from app.database import engine
from app.models import user

# Создаем таблицы в базе данных
user.Base.metadata.create_all(bind=engine)

# Создаем приложение FastAPI
app = FastAPI(
    title="Auth Service",
    description="Сервис аутентификации и авторизации пользователей с использованием JWT токенов",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене заменить на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router)
app.include_router(users.router)


@app.get("/")
async def root():
    """
    Корневой эндпоинт для проверки работы сервиса.
    
    Returns:
        dict: Приветственное сообщение
    """
    return {
        "message": "Auth Service is running",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """
    Эндпоинт для проверки здоровья сервиса.
    
    Returns:
        dict: Статус сервиса
    """
    return {"status": "healthy"}