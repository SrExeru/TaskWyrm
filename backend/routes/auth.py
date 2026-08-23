from fastapi import APIRouter, Depends
from sqlalchemy import text, insert
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from services import session_manager

auth_router = APIRouter(
    prefix = '/auth',
    tags = ['Auth']
)

@auth_router.post('/register')
async def register_user (db: AsyncSession = Depends(session_manager.get_session)):
    return 'register'

@auth_router.post('/login')
async def login_user ():
    return 'login'

@auth_router.post('/logout')
async def finish_session ():
    return 'logout'

@auth_router.post('/refresh')
async def refresh_session ():
    return 'refresh'