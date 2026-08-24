from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models import Session, User
from schemas import TokenPayload, TokenResponse, LoginUserForm
from services import DatabaseManager, session_manager, encode_jwt, decode_jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone, timedelta

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
        
    session = await db.select(Session).where(Session.user_id == int(payload.sub), Session.decive == payload.decive).first()
    
    if not session:
        raise HTTPException(
            status_code = 401, detail = 'Invalid token.'
        )
    
    return payload.exp < session.expires_at
    
async def validate_refresh (refresh_token: str, db: DatabaseManager) -> bool:
    payload = proccess_token(refresh_token)
    
    if payload.type != 'refresh':
        raise HTTPException(
            status_code = 401, detail = 'Invalid token.'
        )
        
    session = await db.select(Session).where(Session.user_id == int(payload.sub), Session.token == refresh_token, Session.decive == payload.decive).first()
    
    if not session:
        raise HTTPException(
            status_code = 401, detail = 'Invalid token.'
        )
    
    return payload.exp < session.expires_at
    
# Create and refresh authorization

async def get_new_session (user_id: int, decive: str, db: DatabaseManager) -> TokenResponse:
    access_expiration_date = create_expiration_date(minutes = 15)
    refresh_expiration_date = create_expiration_date(days = 30)
    
    access_payload = TokenPayload(
        sub = str(user_id),
        type = 'access',
        decive = decive,
        exp = access_expiration_date
    )
    
    refresh_payload = TokenPayload(
        sub = str(user_id),
        type = 'refresh',
        decive = decive,
        exp = refresh_expiration_date
    )
    
    access_token = encode_jwt(access_payload.model_dump())
    refresh_token = encode_jwt(refresh_payload.model_dump())
    
    previous_session = await db.select(Session).where(Session.user_id == user_id, Session.decive == decive).first()
    
    if not previous_session:
        session = Session(
            user_id = user_id,
            decive = decive,
            token = refresh_token,
            expires_at = refresh_expiration_date
        )
        
        await db.add(session)
    else:
        previous_session.token = refresh_token
        previous_session.expires_at = refresh_expiration_date
        
        await db.save(previous_session)
        
    return TokenResponse(
        access_token = access_token
    )
    
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
            
    