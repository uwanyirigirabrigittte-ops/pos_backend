from typing import Any

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from ..repositories.user_repo import user_repository
from ..schemas.user import UserCreate


def register(db: Session, data: UserCreate) -> Any:
    existing = user_repository.get_by_username(db, data.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    user_data = data.model_dump()
    user_data["password"] = hash_password(user_data["password"])
    return user_repository.create(db, user_data)


def authenticate(db: Session, username: str, password: str) -> Any:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if not isinstance(username, str) or not username.strip():
        raise credentials_exception
    if not isinstance(password, str) or not password:
        raise credentials_exception
    user = user_repository.get_by_username(db, username)
    if not user or not verify_password(password, user.password):
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is inactive",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user.id <= 0:
        raise credentials_exception
    return {
        "access_token": create_access_token({"sub": str(user.id)}),
        "token_type": "bearer",
    }
