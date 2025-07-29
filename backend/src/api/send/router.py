from fastapi import APIRouter

router = APIRouter(prefix="/send", tags=["send"])

@router.get("/health")
async def health():
    return {"status": "ok"}
