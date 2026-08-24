from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from schemas import TokenPayload, TokenResponse
from services import DatabaseManager, session_manager, encode_jwt, decode_jwt
from jwt import ExpiredSignatureError, InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "auth/login")

async def validate_access_token (access_token: str) -> TokenPayload:
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

async def get_session (access_token: str = Depends(oauth2_scheme), db: DatabaseManager = Depends(session_manager.get_session)):
    payload = validate_access_token(access_token)


async def get_user (access_token = Depends(oauth2_scheme), db: DatabaseManager = Depends(session_manager.get_session)):
    payload = validate_access_token(access_token)