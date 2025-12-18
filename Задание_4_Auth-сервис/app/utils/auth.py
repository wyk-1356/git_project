"""
Утилиты для работы с JWT токенами и аутентификацией.
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import redis
import os
from dotenv import load_dotenv

from app.schemas.token import TokenData
from app.utils.security import verify_password

load_dotenv()

# Настройки JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

# Настройки Redis
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))

# Создание Redis клиента
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True
)

# Схема аутентификации HTTP Bearer
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создает JWT access токен.
    
    Args:
        data (dict): Данные для кодирования в токене
        expires_delta (Optional[timedelta]): Время жизни токена
    
    Returns:
        str: JWT токен
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Создает JWT refresh токен.
    
    Args:
        data (dict): Данные для кодирования в токене
    
    Returns:
        str: JWT refresh токен
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """
    Проверяет и декодирует JWT токен.
    
    Args:
        token (str): JWT токен
    
    Returns:
        TokenData: Данные из токена
    
    Raises:
        HTTPException: Если токен невалидный
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невалидные учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Проверяем, не отозван ли токен
        if redis_client.get(f"blacklist:{token}"):
            raise credentials_exception
            
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if email is None or user_id is None:
            raise credentials_exception
        
        token_type = payload.get("type")
        if token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный тип токена",
            )
            
        return TokenData(email=email, user_id=user_id)
    except JWTError:
        raise credentials_exception


def verify_refresh_token(token: str) -> TokenData:
    """
    Проверяет и декодирует refresh токен.
    
    Args:
        token (str): JWT refresh токен
    
    Returns:
        TokenData: Данные из токена
    
    Raises:
        HTTPException: Если токен невалидный
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Невалидный refresh токен",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Проверяем, не отозван ли токен
        if redis_client.get(f"blacklist:{token}"):
            raise credentials_exception
            
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        user_id: int = payload.get("user_id")
        
        if email is None or user_id is None:
            raise credentials_exception
        
        token_type = payload.get("type")
        if token_type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный тип токена",
            )
            
        return TokenData(email=email, user_id=user_id)
    except JWTError:
        raise credentials_exception


def add_to_blacklist(token: str, expires_in: int) -> None:
    """
    Добавляет токен в черный список в Redis.
    
    Args:
        token (str): Токен для добавления в черный список
        expires_in (int): Время жизни в секундах
    """
    redis_client.setex(f"blacklist:{token}", expires_in, "blacklisted")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Получает текущего пользователя из токена.
    
    Args:
        credentials (HTTPAuthorizationCredentials): Учетные данные из заголовка
    
    Returns:
        TokenData: Данные пользователя из токена
    """
    token = credentials.credentials
    return verify_token(token)


def authenticate_user(email: str, password: str, db) -> Optional[dict]:
    """
    Аутентифицирует пользователя по email и паролю.
    
    Args:
        email (str): Email пользователя
        password (str): Пароль пользователя
        db: Сессия базы данных
    
    Returns:
        Optional[dict]: Данные пользователя или None
    """
    from app.crud.user import get_user_by_email
    
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    
    return {"id": user.id, "email": user.email}