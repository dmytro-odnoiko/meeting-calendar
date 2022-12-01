from fastapi import Depends, HTTPException, status, APIRouter
from db import SessionLocal, get_db
from schemas.user import UserCreate, UserCreatedResponse
from crud.user import get_user_by_email, create_user

router = APIRouter()

@router.post('/users', response_model=UserCreatedResponse, status_code=201)
async def signup(user_data: UserCreate, db: SessionLocal = Depends(get_db)):
	"""add new user"""
	user = get_user_by_email(db, user_data.email)
	if user:
		raise HTTPException(status_code=status.HTTP_409_CONFLICT,
							detail="Email already registered.")
	
	signedup_user = create_user(db, user_data)
	return {
		'email': signedup_user.email,
		'message': 'User successfully created.',
	}