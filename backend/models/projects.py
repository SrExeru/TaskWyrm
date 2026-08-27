from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from services.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import User
    
class Project(Base):
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text)
    
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    author: Mapped['User'] = relationship(back_populates = 'projects')
    
    __tablename__ = 'projects'