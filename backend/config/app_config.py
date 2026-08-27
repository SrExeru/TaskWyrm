from dataclasses import dataclass
import json

@dataclass
class AuthSettings:
    access_token_lifespan: dict[str, int]
    refresh_token_lifespan: dict[str, int]
    
@dataclass
class AppConfig:
    auth_settings: AuthSettings
    
with open('config/app_config.json', 'r') as raw_data:
    data = json.load(raw_data)
    
auth_settings = AuthSettings(**data['auth'])
