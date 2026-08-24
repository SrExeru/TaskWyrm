from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

class UserResponse(BaseModel):
    username: str
    biography: Optional[str]
    email: str
    
    model_config = ConfigDict(from_attributes=True)