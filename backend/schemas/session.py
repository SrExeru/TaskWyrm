from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TokenPayload(BaseModel):
    sub: str
    type: str
    decive: str
    exp: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    model_config = ConfigDict(from_attributes=True)