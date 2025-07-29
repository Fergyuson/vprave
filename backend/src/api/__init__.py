from fastapi import APIRouter
from .send.router import router as send_router
from .leads      import router as leads_router

router = APIRouter()
router.include_router(send_router, prefix="/send", tags=["send"])
router.include_router(leads_router, prefix="/leads", tags=["leads"])
