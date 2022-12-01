
from db import SessionLocal
from schemas.user import UserBase,UserCreate
from models.user import User
from core.security import get_password_hash, verify_password

def get_user_by_email(db: SessionLocal, email: UserBase):
    return db.query(User).filter(User.email == email).first()


def create_user(db: SessionLocal, user: UserCreate):
    create_data = user.dict()
    create_data.pop("password")
    created_user = User(**create_data)
    created_user.hashed_password = get_password_hash(user.password)
    db.add(created_user)
    db.commit()

    return created_user

def authenticate_user(db, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
