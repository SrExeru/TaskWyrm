from sqlalchemy import String, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from services.database import Base
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import User

class Session(Base):
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    device: Mapped[str] = mapped_column(String(100))
    token: Mapped[str] = mapped_column(String(300))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone = True))
    
    user: Mapped['User'] = relationship(back_populates = 'sessions')
    
    __tablename__ = 'session'