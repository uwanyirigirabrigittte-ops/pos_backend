from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..repositories.user_repo import user_repository
from ..schemas.user import UserCreate, UserUpdate
from ..core.security import hash_password, verify_password

def get_user(db: Session, user_id: int):
    user = user_repository.get(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Employee user record not found"
        )
    return user

def list_users(db: Session):
    return user_repository.get_all(db)

def create_user(db: Session, data: UserCreate):
    data_dict = data.model_dump()
    data_dict["password"] = hash_password(data_dict["password"])
    return user_repository.create(db, data_dict)

def authenticate_user(db: Session, username: str, password: str):
    user = user_repository.get_by_username(db, username)
    if not user:
        return None
    if not user.is_active:
        return None
    if not verify_password(password, user.password):
        return None
    return user

def update_user(db: Session, user_id: int, data: UserUpdate):
    user = get_user(db, user_id)
    update_dict = data.model_dump(exclude_unset=True)
    if "password" in update_dict and update_dict["password"]:
        update_dict["password"] = hash_password(update_dict["password"])
    return user_repository.update(db, user, update_dict)

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    user_repository.delete(db, user)
