"""
Инициализация моделей базы данных.
"""
from app.models.user import User, LoginHistory

__all__ = ["User", "LoginHistory"]