from pydantic import BaseModel, field_validator
from typing import Optional

class RegisterUserForm(BaseModel):
    username: str
    biography: Optional[str] = None
    email: str
    password: str
    
    device: str
    
class LoginUserForm(BaseModel):
    email: str
    password: str
    
    device: str