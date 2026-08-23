from typing import AsyncGenerator, Optional
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.orm import DeclarativeBase
from config import database_config

class Base(DeclarativeBase):
    pass

class SessionManager:
    def __init__(self) -> None:
        self.engine: AsyncEngine
        self.session_factory: async_sessionmaker[AsyncSession]
        
    def init_db (self) -> None:
        self.engine = create_async_engine(
            database_config.DATABASE_URL,
            poolclass = AsyncAdaptedQueuePool,
            echo = database_config.DATABASE_DEBUG
        )
        
        self.session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit = False,
            autoflush = False,
            class_ = AsyncSession
        )
        
    async def close (self) -> None:
        if self.engine:
            await self.engine.dispose()
            
    async def get_session (self) -> AsyncGenerator[AsyncSession, None]:
        if not self.session_factory:
            raise RuntimeError('Database session is not initialized.')      
        
        async with self.session_factory() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                raise RuntimeError(f"Database session error: {e!r}") from e  
    
session_manager = SessionManager()