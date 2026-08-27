from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models import Session, User
from schemas import TokenPayload, TokenResponse, LoginUserForm
from services import DatabaseManager, session_manager, encode_jwt, decode_jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone, timedelta
from config import auth_settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "auth/login")

create_expiration_date = lambda **duration: datetime.now(timezone.utc) + timedelta(**duration)

# Global validations

def proccess_token (access_token: str) -> TokenPayload:
    try:
        payload = decode_jwt(access_token)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code = 401, detail = 'Expired token.'
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code = 401, detail = 'Invalid token.'
        )
        
    return TokenPayload(**payload)

async def validate_access (access_token: str, db: DatabaseManager) -> bool:
    payload = proccess_token(access_token)
    
    if payload.type != 'access':
        raise HTTPException(
            status_code = 401, detail = 'Invalid token.'
        )
        
    session = await db.select(Session).where(Session.user_id == int(payload.sub), Session.device == payload.device).first()
    
    if not session:
        raise HTTPException(
            status_code = 401, detail = 'Invalid token.'
        )
    
    return payload.exp < session.expires_at
    
async def validate_refresh (refresh_token: str, db: DatabaseManager) -> tuple[int, str]:
    payload = proccess_token(refresh_token)
    
    
    if payload.type != 'refresh':
        raise HTTPException(
            status_code = 401, detail = 'Invalid token.'
        )
        
        
    print(payload.sub)
    print(refresh_token)
    session = await db.select(Session).where(Session.user_id == int(payload.sub), Session.token == refresh_token).first()
    
    print(session)
    
    if not session:
        raise HTTPException(
            status_code = 401, detail = 'Invalid token.'
        )
    
    if datetime.now(timezone.utc) > session.expires_at:
        
        raise HTTPException(
            status_code = 401, detail = 'Expired token.'
        )
        
    return session.user_id, session.device
    
# Create and refresh authorization

async def get_new_session (user_id: int, device: str, db: DatabaseManager) -> tuple[TokenResponse, TokenResponse]:
    access_expiration_date = create_expiration_date(**auth_settings.access_token_lifespan)
    refresh_expiration_date = create_expiration_date(**auth_settings.refresh_token_lifespan)
    
    access_payload = TokenPayload(
        sub = str(user_id),
        type = 'access',
        device = device,
        exp = access_expiration_date
    )
    
    refresh_payload = TokenPayload(
        sub = str(user_id),
        type = 'refresh',
        device = device,
        exp = refresh_expiration_date
    )
    
    access_token = encode_jwt(access_payload.model_dump())
    refresh_token = encode_jwt(refresh_payload.model_dump())
    
    previous_session = await db.select(Session).where(Session.user_id == user_id, Session.device == device).first()
    
    if not previous_session:
        session = Session(
            user_id = user_id,
            device = device,
            token = refresh_token,
            expires_at = refresh_expiration_date
        )
        
        await db.add(session)
    else:
        previous_session.token = refresh_token
        previous_session.expires_at = refresh_expiration_date
        
        await db.save(previous_session)
        
    return TokenResponse(token = access_token, type = 'access_token'), TokenResponse(token = refresh_token, type = 'refresh_token') 
    
# Get authorization

async def get_session (access_token: str = Depends(oauth2_scheme), db: DatabaseManager = Depends(session_manager.get_session)) -> Session:
    payload = proccess_token(access_token)
    
    is_valid = await validate_access(
        access_token = access_token,
        db = db
        )
    
    if not is_valid:
        raise HTTPException(
            status_code = 401, detail = 'Invalid token.'
        )
            
    session = await db.select(Session).where(Session.user_id == int(payload.sub)).first()
    
    if not session:
        raise HTTPException(
            status_code = 404, detail = 'Session not found.'
        )
            
    return session


async def get_user (access_token = Depends(oauth2_scheme), db: DatabaseManager = Depends(session_manager.get_session)) -> User:
    payload = proccess_token(access_token)
    
    is_valid = await validate_access(
        access_token = access_token,
        db = db
        )
    
    if not is_valid:
        raise HTTPException(
            status_code = 401, detail = 'Invalid token.'
        )
        
    user = await db.select(User).where(User.id == int(payload.sub)).first()
    
    if not user:
        raise HTTPException(
            status_code = 404, detail = 'User not found.'
        )
        
    return user
            
    