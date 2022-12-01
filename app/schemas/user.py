from pydantic import BaseModel
from pydantic import EmailStr
from fastapi import status


class UserBase(BaseModel):
   email: EmailStr


class UserCreate(UserBase):
   name: str
   password: str


class UserCreatedResponse(UserBase):
   message: str
