"""
Схемы Pydantic для работы с токенами.
"""
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """
    Схема access токена.
    
    Attributes:
        access_token (str): Access токен
        token_type (str): Тип токена (bearer)
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Данные, закодированные в токене.
    
    Attributes:
        email (Optional[str]): Email пользователя
        user_id (Optional[int]): ID пользователя
    """
    email: Optional[str] = None
    user_id: Optional[int] = None


class RefreshToken(BaseModel):
    """
    Схема для обновления токена.
    
    Attributes:
        refresh_token (str): Refresh токен
    """
    refresh_token: str


class TokenPair(BaseModel):
    """
    Пара токенов (access и refresh).
    
    Attributes:
        access_token (str): Access токен
        refresh_token (str): Refresh токен
        token_type (str): Тип токена
    """
    access_token: str
    refresh_token: str
    token_type: str