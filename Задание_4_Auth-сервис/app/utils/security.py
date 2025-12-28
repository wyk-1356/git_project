"""
Утилиты для работы с паролями и хэшированием.
"""
from passlib.context import CryptContext
import os
from dotenv import load_dotenv

load_dotenv()

# Контекст для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет соответствие пароля его хэшу.
    
    Args:
        plain_password (str): Обычный пароль
        hashed_password (str): Хэшированный пароль
    
    Returns:
        bool: True если пароль верный, иначе False
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Генерирует хэш пароля.
    
    Args:
        password (str): Пароль для хэширования
    
    Returns:
        str: Хэшированный пароль
    """
    return pwd_context.hash(password)