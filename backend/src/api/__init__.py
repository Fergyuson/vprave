from src.api.send.router import router as send_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(send_router)
