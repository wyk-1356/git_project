"""
Роутер для аутентификации пользователей.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserCreate, TokenPair, RefreshToken
from app.schemas.user import UserLogin
from app.crud.user import create_user, get_user_by_email, add_login_history
from app.utils.auth import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    authenticate_user,
    get_current_user,
    add_to_blacklist
)
from app.schemas.token import TokenData

router = APIRouter(prefix="", tags=["Аутентификация"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация нового пользователя.
    
    Args:
        user (UserCreate): Данные нового пользователя
        db (Session): Сессия базы данных
    
    Returns:
        dict: Сообщение об успешной регистрации
    
    Raises:
        HTTPException: Если пользователь уже существует
    """
    # Проверяем, существует ли пользователь с таким email
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже зарегистрирован"
        )
    
    # Создаем пользователя
    create_user(db=db, user=user)
    
    return {"message": "Пользователь успешно зарегистрирован"}


@router.post("/login", response_model=TokenPair)
async def login(
    request: Request,
    user_login: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Вход пользователя в систему.
    
    Args:
        request (Request): Запрос
        user_login (UserLogin): Данные для входа
        db (Session): Сессия базы данных
    
    Returns:
        TokenPair: Пара токенов (access и refresh)
    
    Raises:
        HTTPException: Если email или пароль неверные
    """
    # Аутентифицируем пользователя
    user = authenticate_user(user_login.email, user_login.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Создаем токены
    access_token = create_access_token(
        data={"sub": user["email"], "user_id": user["id"]}
    )
    refresh_token = create_refresh_token(
        data={"sub": user["email"], "user_id": user["id"]}
    )
    
    # Добавляем запись в историю входов
    user_agent = request.headers.get("User-Agent")
    add_login_history(db, user["id"], user_agent)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=TokenPair)
async def refresh_token(refresh_token_data: RefreshToken):
    """
    Обновление access токена с помощью refresh токена.
    
    Args:
        refresh_token_data (RefreshToken): Refresh токен
    
    Returns:
        TokenPair: Новая пара токенов
    
    Raises:
        HTTPException: Если refresh токен невалидный
    """
    # Проверяем refresh токен
    token_data = verify_refresh_token(refresh_token_data.refresh_token)
    
    # Добавляем старый refresh токен в черный список
    add_to_blacklist(refresh_token_data.refresh_token, 7 * 24 * 60 * 60)  # 7 дней
    
    # Создаем новые токены
    access_token = create_access_token(
        data={"sub": token_data.email, "user_id": token_data.user_id}
    )
    refresh_token = create_refresh_token(
        data={"sub": token_data.email, "user_id": token_data.user_id}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(
    current_user: TokenData = Depends(get_current_user)
):
    """
    Выход из системы.
    
    Args:
        current_user (TokenData): Текущий пользователь
    
    Returns:
        dict: Сообщение об успешном выходе
    """
    # В реальном приложении здесь бы мы получали токен из заголовка
    # и добавляли его в черный список
    return {"message": "Успешный выход из системы"}