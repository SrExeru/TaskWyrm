from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import text, insert
from sqlalchemy.ext.asyncio import AsyncSession
from models import User
from schemas import RegisterUserForm, LoginUserForm, UserResponse
from services import session_manager, DatabaseManager

auth_router = APIRouter(
    prefix = '/auth',
    tags = ['Auth']
)

@auth_router.post('/register')
async def register_user (register_form: RegisterUserForm, db: DatabaseManager = Depends(session_manager.get_session)):
    new_user = User(**register_form.model_dump())
    
    await db.add(new_user)
    
    return {
        'id': new_user.id
        }

@auth_router.post('/login')
async def login_user (login_form: LoginUserForm, db: DatabaseManager = Depends(session_manager.get_session)):
    user = await db.select(User).where(
        User.email == login_form.email
    ).first()
    
    if not user:
        raise HTTPException(
            status_code = 401,
            detail = 'Incorrect email or password.'
        )
        
    if not user.verify_password(login_form.password):
        raise HTTPException(
            status_code = 401,
            detail = 'Incorrect email or password.'
        )
        
    return UserResponse.model_validate(user)

@auth_router.post('/logout')
async def finish_session ():
    return 'logout'

@auth_router.post('/refresh')
async def refresh_session ():
    return 'refresh'