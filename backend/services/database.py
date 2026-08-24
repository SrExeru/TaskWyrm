from typing import AsyncGenerator, Optional, TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import AsyncAdaptedQueuePool
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.expression import ColumnElement
from sqlalchemy import insert, select, Result
from fastapi import HTTPException
from config import database_config

class Base(DeclarativeBase):
    pass

# Session tools

ModelType = TypeVar("ModelType", bound = Base)

class QueryBuilder(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: type[ModelType]) -> None:
        self._session: AsyncSession = session
        self._model: type[ModelType] = model
        self._conditions: list[ColumnElement[bool]] = []
        
    def where (self, *criteria: ColumnElement[bool]) -> 'QueryBuilder[ModelType]':
        self._conditions.extend(criteria)
        return self
    
    async def first (self) -> Optional[ModelType]:
        result = await self._build_query()
        return result.first()
    
    async def all (self) -> list[ModelType]:
        result = await self._build_query()
        return list(result.all())
    
    async def _build_query (self):
        query = await self._session.execute(
            select(self._model).where(*self._conditions)
        )
        
        return query.scalars()

class DatabaseManager:
    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session
        
    async def add (self, entity: Base) -> None:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        
    def select (self, model: type[ModelType]) -> QueryBuilder[ModelType]:
        return QueryBuilder(self.session, model)
        
# Session generator

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
            
    async def get_session (self) -> AsyncGenerator[DatabaseManager, None]:
        if not self.session_factory:
            raise RuntimeError('Database session is not initialized.') 
        
        async with self.session_factory() as session:
            try:
                yield DatabaseManager(session)
            except HTTPException:
                raise
            except Exception as e:
                await session.rollback()
                raise RuntimeError(f"Database session error: {e!r}") from e  
    
session_manager = SessionManager()