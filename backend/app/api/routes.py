from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def home():
    return {
        "app": "RED AI",
        "status": "running",
        "version": "0.1.0"
    }

@router.get("/health")
async def health():
    return {
        "status": "healthy"
    }