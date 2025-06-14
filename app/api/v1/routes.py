from fastapi import APIRouter

router = APIRouter()

@router.get("/health", summary="Health Check")
async def health_check():
    return {"status": "ok"}