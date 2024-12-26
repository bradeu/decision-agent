from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def agent():
    return {"test": "hello world"}

@router.get("/plan")
async def planner():
    return {"test": "hello world"}

@router.get("/revise")
async def revise():
    return {"test": "hello world"}