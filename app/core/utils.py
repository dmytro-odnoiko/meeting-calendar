from enum import Enum

from fastapi import Depends
from db import SessionLocal, get_db

from core.token import decode_access_token


def get_current_user(token: str, db: SessionLocal = Depends(get_db)):
   return decode_access_token(db, token)
