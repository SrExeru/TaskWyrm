import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services import session_manager
from services.database import Base
from models import all_models
from routes import all_routes
from config import CORS_ORIGINS

@asynccontextmanager
async def lifespan(app: FastAPI):
    session_manager.init_db()
    
    async with session_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield
    
    await session_manager.close()

app = FastAPI(
    lifespan = lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins = CORS_ORIGINS,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

@app.get('/')
async def hello_world ():
    return 'hello world'

for route in all_routes:
    app.include_router(route)