from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from services.database import Base
from services.security import hash_password, verify_password
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from models.session import Session

class User(Base):
    id: Mapped[int] = mapped_column(primary_key = True)
    username: Mapped[str] = mapped_column(String(50), unique = True)
    email: Mapped[str] = mapped_column(String(80), unique = True)
    biography: Mapped[str | None] = mapped_column(Text)
    password: Mapped[str] = mapped_column(String(300))
    
    
    sessions: Mapped[list['Session']] = relationship(back_populates = 'user')
    
    __tablename__ = 'users'
    
    def verify_password (self, password: str) -> bool:
        return verify_password(password, self.password)
    
    # Validations
    
    @validates('password')
    def validate_password (self, key, value: str) -> str:
        # Password validations
        
        return hash_password(value)
    
    @validates('biography')
    def validate_biography (self, key, value: Optional[str]) -> Optional[str]:
        if not value:
            return None
        
        clean_bio = value.strip()
        
        if clean_bio == '':
            return None
        
        return clean_bio
