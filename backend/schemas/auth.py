from pydantic import BaseModel, field_validator
from typing import Optional

class RegisterUserForm(BaseModel):
    username: str
    biography: Optional[str]
    email: str
    password: str
    
    decive: str
    
class LoginUserForm(BaseModel):
    email: str
    password: str
    
    decive: str