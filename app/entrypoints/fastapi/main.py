from fastapi import FastAPI
from app.entrypoints.fastapi.api.endpoints import v1

app = FastAPI(title="Trading Gateway", version="1.0.0")
app.include_router(v1.router, prefix="/api/v1")
