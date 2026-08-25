from fastapi import APIRouter, Depends, HTTPException
from models import User
from services.auth import get_user

user_router = APIRouter(
    prefix = '/user',
    tags = ['User']
)

@user_router.get('/me')
def get_user_data (user: User = Depends(get_user)):
    return user