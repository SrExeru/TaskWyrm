from fastapi import APIRouter, HTTPException, Depends, Response, Cookie
from models import User
from schemas import RegisterUserForm, LoginUserForm, TokenResponse
from services import session_manager, DatabaseManager
from services.auth import get_new_session, validate_refresh
from typing import Optional

auth_router = APIRouter(
    prefix = '/auth',
    tags = ['Auth']
)

@auth_router.post('/register', response_model = TokenResponse)
async def register_user (response: Response, register_form: RegisterUserForm, db: DatabaseManager = Depends(session_manager.get_session)):
    new_user = User(**register_form.model_dump(exclude = {'device'}))
    
    await db.add(new_user)
    
    access_session, refresh_session = await get_new_session(
        new_user.id,
        register_form.device,
        db
    )
    
    response.set_cookie(
        key = 'refresh_token',
        value = refresh_session.token
    )
    
    return TokenResponse(
        token = access_session.token,
        type = 'access_token'
    )

@auth_router.post('/login', response_model = TokenResponse)
async def login_user (response: Response, login_form: LoginUserForm, db: DatabaseManager = Depends(session_manager.get_session)):
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
        
    access_session, refresh_session = await get_new_session(
        user.id,
        login_form.device,
        db
    )
        
    response.set_cookie(
        key = 'refresh_token',
        value = refresh_session.token
    )
        
    return TokenResponse(
        token = access_session.token,
        type = 'access_token'
    )

@auth_router.post('/logout')
async def finish_session ():
    return 'logout'

@auth_router.get('/refresh', response_model = TokenResponse)
async def refresh_session (response: Response, refresh_token: Optional[str] = Cookie(default = None), db: DatabaseManager = Depends(session_manager.get_session)):
    print(refresh_token)
    
    if not (refresh_token):
        return HTTPException(
            status_code = 404,
            detail = 'Inexistent token.'
        )
        
    user_id, device = await validate_refresh(refresh_token, db)
    
    access_session, refresh_session = await get_new_session(
        user_id,
        device,
        db
    )

    response.set_cookie(
            key = 'refresh_token',
            value = refresh_session.token
        )
            
    return TokenResponse(
        token = access_session.token,
        type = 'access_token'
    )