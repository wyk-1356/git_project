from fastapi import FastAPI
from app.database import engine, Base
from app.api.endpoints import students, groups

# Создание таблиц в БД
Base.metadata.create_all(bind=engine)

# Создание приложения FastAPI
app = FastAPI(
    title="Students API",
    description="API для управления студентами и группами",
    version="1.0.0"
)

# Подключение роутеров
app.include_router(
    students.router,
    prefix="/api/students",
    tags=["Студенты"]
)

app.include_router(
    groups.router,
    prefix="/api/groups",
    tags=["Группы"]
)

@app.get("/")
def read_root():
    """Корневой эндпоинт"""
    return {
        "message": "Добро пожаловать в Students API!",
        "docs": "/docs",
        "redoc": "/redoc"
    }
