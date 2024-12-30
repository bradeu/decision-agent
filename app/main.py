from fastapi import FastAPI, Request
from app.api.endpoints import agent, health

app = FastAPI()

@app.get("/")
async def root(request: Request):
    return await request.json()

app.include_router(agent.router, prefix="/agent", tags=["agent"])
app.include_router(health.router, prefix="/health", tags=["health"])
