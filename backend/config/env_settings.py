from os import getenv
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import TypeVar, cast, Optional

load_dotenv()

T = TypeVar('T')

def parse_setting (value: str, value_type: type[T]) -> T:
    if value_type == str:
        return cast(T, value)
    if value_type == bool:
        clean_value = value.strip().lower()
        if clean_value not in ['true', 'false', '1', '0', 't', 'f']:
            raise RuntimeError(f'value {value} should be a {value_type}.')
            
        return cast(T, clean_value in ['true', '1', 't'])
    if value_type in (int, float):
        return cast(T, value_type(value))
    if value_type in (list, set):
        values = [x.strip() for x in value.split(',')]
        return cast(T, value_type(values))
    
    raise NotImplementedError(f'Invalid env variable type: {value_type}.')

def required_env_setting (key: str, value_type: type[T] = str) -> T:
    value = getenv(key)
    
    if value is None:
        raise RuntimeError(f'Inexistent environment variable: {key}.')
    
    try:
        return parse_setting(value, value_type)
    except Exception as e:
        raise RuntimeError(f'Env setting error {key}: {e}')
    
def optional_env_setting (key: str, value_type: type[T] = str, default: Optional[T] = None) -> T:
    value = getenv(key)
        
    if value is None:
        return cast(T, default)
    
    try:
        return parse_setting(value, value_type)
    except Exception as e:
        raise RuntimeError(f'Env setting error {key}: {e}')

JWT_SECRET_KEY = required_env_setting('JWT_SECRET_KEY')
JWT_ALGORITHM = required_env_setting('JWT_ALGORITHM')

@dataclass
class DBConfig:
    DATABASE_URL: str = required_env_setting('DATABASE_URL')
    DATABASE_DEBUG: bool = optional_env_setting('DATABASE_DEBUG', value_type = bool, default = False)
    
database_config = DBConfig()