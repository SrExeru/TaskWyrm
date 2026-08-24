from pwdlib import PasswordHash
from pwdlib.hashers.argon2 import Argon2Hasher
from config import jwt_config
import jwt

# JWT

def encode_jwt (payload: dict) -> str:    
    return jwt.encode(
        payload,
        jwt_config.JWT_SECRET_KEY,
        algorithm = jwt_config.JWT_ALGORITHM
    )
    
def decode_jwt (encoded_jwt: str) -> dict:
    return jwt.decode(
        encoded_jwt,
        jwt_config.JWT_SECRET_KEY,
        algorithms = [jwt_config.JWT_ALGORITHM]
    )
    
# Password hashing

password_hash = PasswordHash((Argon2Hasher(),))

def hash_password (raw_password: str) -> str:
    return password_hash.hash(raw_password)

def verify_password (raw_password: str, hashed_password: str) -> bool:
    return password_hash.verify(raw_password, hashed_password)