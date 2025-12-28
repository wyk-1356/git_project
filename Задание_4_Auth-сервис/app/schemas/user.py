"""
Схемы Pydantic для валидации данных пользователя.
"""
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """
    Базовая схема пользователя.
    
    Attributes:
        email (EmailStr): Email пользователя
    """
    email: EmailStr


class UserCreate(UserBase):
    """
    Схема для создания пользователя.
    
    Attributes:
        password (str): Пароль пользователя
    """
    password: str


class UserUpdate(BaseModel):
    """
    Схема для обновления данных пользователя.
    
    Attributes:
        email (Optional[EmailStr]): Новый email
        password (Optional[str]): Новый пароль
    """
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserInDB(UserBase):
    """
    Схема пользователя в базе данных.
    
    Attributes:
        id (int): ID пользователя
        created_at (datetime): Дата создания
        updated_at (datetime): Дата обновления
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """
    Схема для входа пользователя.
    
    Attributes:
        email (EmailStr): Email пользователя
        password (str): Пароль пользователя
    """
    email: EmailStr
    password: str