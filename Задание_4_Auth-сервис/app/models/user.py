"""
Модель пользователя для базы данных.
"""
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """
    Модель пользователя.
    
    Attributes:
        id (int): Уникальный идентификатор пользователя
        email (str): Email пользователя (уникальный)
        hashed_password (str): Хэшированный пароль
        created_at (datetime): Дата создания
        updated_at (datetime): Дата обновления
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    # Связь с историей входов
    login_history = relationship("LoginHistory", back_populates="user", cascade="all, delete-orphan")


class LoginHistory(Base):
    """
    Модель истории входов пользователя.
    
    Attributes:
        id (int): Уникальный идентификатор записи
        user_id (int): ID пользователя
        user_agent (str): User-Agent браузера
        login_time (datetime): Время входа
    """
    __tablename__ = "login_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_agent = Column(String)
    login_time = Column(DateTime, server_default=func.now())

    # Связь с пользователем
    user = relationship("User", back_populates="login_history")