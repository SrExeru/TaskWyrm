from fastapi import APIRouter, Depends, HTTPException
from models import User
from schemas import UserResponse
from services.auth import get_user

user_router = APIRouter(
    prefix = '/user',
    tags = ['User']
)

@user_router.get('/me', response_model = UserResponse)
def get_user_data (user: User = Depends(get_user)):
    return user