from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def agent():
    return {"test": "hello world"}

@router.get("/plan")
async def planner():
    return {"plan": "hello world"}

@router.get("/feedback")
async def feedback():
    return {"feedback": "hello world"}