from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Literal

class TokenPayload(BaseModel):
    sub: str
    type: str
    device: str
    exp: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
class TokenResponse(BaseModel):
    token: str
    type: Literal['access_token', 'refresh_token']
    
    model_config = ConfigDict(from_attributes=True)