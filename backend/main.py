import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from services import session_manager, Base
from models import all_models
from routes import all_routes

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

@app.get('/')
async def hello_world ():
    return 'hello world'

for route in all_routes:
    app.include_router(route)