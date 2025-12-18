"""
CRUD операции для работы с пользователями.
"""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List

from app.models.user import User, LoginHistory
from app.schemas.user import UserCreate, UserUpdate
from app.utils.security import get_password_hash


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Получает пользователя по email.
    
    Args:
        db (Session): Сессия базы данных
        email (str): Email пользователя
    
    Returns:
        Optional[User]: Пользователь или None
    """
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """
    Получает пользователя по ID.
    
    Args:
        db (Session): Сессия базы данных
        user_id (int): ID пользователя
    
    Returns:
        Optional[User]: Пользователь или None
    """
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate) -> User:
    """
    Создает нового пользователя.
    
    Args:
        db (Session): Сессия базы данных
        user (UserCreate): Данные нового пользователя
    
    Returns:
        User: Созданный пользователь
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """
    Обновляет данные пользователя.
    
    Args:
        db (Session): Сессия базы данных
        user_id (int): ID пользователя
        user_update (UserUpdate): Новые данные пользователя
    
    Returns:
        Optional[User]: Обновленный пользователь или None
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    
    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(update_data.pop("password"))
    
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def add_login_history(db: Session, user_id: int, user_agent: Optional[str] = None) -> LoginHistory:
    """
    Добавляет запись в историю входов.
    
    Args:
        db (Session): Сессия базы данных
        user_id (int): ID пользователя
        user_agent (Optional[str]): User-Agent браузера
    
    Returns:
        LoginHistory: Созданная запись истории
    """
    login_history = LoginHistory(user_id=user_id, user_agent=user_agent)
    db.add(login_history)
    db.commit()
    db.refresh(login_history)
    return login_history


def get_login_history(db: Session, user_id: int, limit: int = 10) -> List[LoginHistory]:
    """
    Получает историю входов пользователя.
    
    Args:
        db (Session): Сессия базы данных
        user_id (int): ID пользователя
        limit (int): Максимальное количество записей
    
    Returns:
        List[LoginHistory]: Список записей истории входов
    """
    return (
        db.query(LoginHistory)
        .filter(LoginHistory.user_id == user_id)
        .order_by(desc(LoginHistory.login_time))
        .limit(limit)
        .all()
    )