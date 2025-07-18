from fastapi import APIRouter

from src.api.send.routers import send

router = APIRouter()
router.include_router(send.router)
