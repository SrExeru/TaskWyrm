from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from services import Base

class User(Base):
    id: Mapped[int] = mapped_column(primary_key = True)
    username: Mapped[str] = mapped_column(String(50))
    biography: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(String(80))
    password: Mapped[str] = mapped_column(String(100))
    
    __tablename__ = 'users'