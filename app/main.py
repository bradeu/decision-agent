from fastapi import FastAPI
from app.api.endpoints import agent, health

app = FastAPI()

app.include_router(agent.router, prefix="/agent", tags=["agent"])
app.include_router(health.router, prefix="/health", tags=["health"])
