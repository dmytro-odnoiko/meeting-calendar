from datetime import timedelta
from os import environ


from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm 

from db import SessionLocal, get_db
from schemas.token import Token
from crud.user import authenticate_user
from core.token import create_access_token


router = APIRouter()

@router.post("/api/token", response_model=Token)
def login_for_access_token(db: SessionLocal = Depends(get_db),
                      	   form_data: OAuth2PasswordRequestForm = Depends()):
    """generate access token for valid credentials"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(
        minutes=environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 30)
    )
    access_token = create_access_token(data={"sub": user.email},
                                       expires_delta=access_token_expires)

    return {"access_token": access_token, "token_type": "bearer"}