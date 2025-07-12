from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import ops, client
from app.db import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(ops.router, prefix="/ops")
app.include_router(client.router, prefix="/client")