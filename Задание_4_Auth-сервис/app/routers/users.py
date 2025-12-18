"""
Роутер для операций с пользователями.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import UserUpdate, UserInDB
from app.schemas.token import TokenData
from app.crud.user import (
    get_user_by_id,
    update_user,
    get_login_history
)
from app.utils.auth import get_current_user

router = APIRouter(prefix="/user", tags=["Пользователи"])


@router.put("/update", response_model=UserInDB)
async def update_user_data(
    user_update: UserUpdate,
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Обновление данных пользователя.
    
    Args:
        user_update (UserUpdate): Новые данные пользователя
        current_user (TokenData): Текущий пользователь
        db (Session): Сессия базы данных
    
    Returns:
        UserInDB: Обновленный пользователь
    
    Raises:
        HTTPException: Если пользователь не найден
    """
    user = get_user_by_id(db, current_user.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    updated_user = update_user(db, current_user.user_id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    
    return updated_user


@router.get("/history")
async def get_user_login_history(
    current_user: TokenData = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10
):
    """
    Получение истории входов пользователя.
    
    Args:
        current_user (TokenData): Текущий пользователь
        db (Session): Сессия базы данных
        limit (int): Максимальное количество записей
    
    Returns:
        List[dict]: Список записей истории входов
    """
    history = get_login_history(db, current_user.user_id, limit)
    
    return [
        {
            "id": record.id,
            "user_agent": record.user_agent,
            "login_time": record.login_time.isoformat()
        }
        for record in history
    ]