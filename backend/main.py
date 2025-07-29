import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, Request
from fastapi.exceptions import RequestValidationError
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse, FileResponse

from src.api import router as all_routers
from src.core.config import settings
from src.core.logger import logging  # ваш logger

# ────────────────────────────────────────
# Lifespan (startup / shutdown)
# ────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("▶️ Application startup")
    yield
    logging.info("⏹ Application shutdown")


# ────────────────────────────────────────
# Основной объект приложения
# ────────────────────────────────────────
app = FastAPI(
    title=settings.app_name,
    lifespan=lifespan,
    docs_url="/api/docs",
    redoc_url=None,
    openapi_url="/api/openapi.json"
)

# ────────────────────────────────────────
# Middleware для settings и CORS
# ────────────────────────────────────────
class SettingsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.settings = settings
        return await call_next(request)

app.add_middleware(SettingsMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://списать-долги-удаленно.рф",
        "https://www.списать-долги-удаленно.рф",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Set-Cookie"],
    max_age=3600,
)

# ────────────────────────────────────────
# Обработчик валидации
# ────────────────────────────────────────
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    details = [
        {"loc": e["loc"], "msg": e["msg"], "type": e["type"]}
        for e in exc.errors()
    ]
    logging.error("Validation error: %s", details)

    if not request.headers.get("content-type", "").startswith("multipart/form-data"):
        body = await request.body()
        try:
            logging.error("Request body: %s", body.decode())
        except UnicodeDecodeError:
            logging.error("Request body as bytes (non-UTF8)")

    return JSONResponse(
        status_code=422,
        content={"detail": details, "message": "Validation error."},
    )

# ────────────────────────────────────────
# Роутеры API (ВАЖНО: должны быть до статических файлов!)
# ────────────────────────────────────────
api_router = APIRouter(prefix="/api")
api_router.include_router(all_routers)
app.include_router(api_router)

# ────────────────────────────────────────
# Монтируем статические ресурсы
# ────────────────────────────────────────
app.mount(
    "/assets",
    StaticFiles(directory="static/assets"),
    name="assets"
)

# Монтируем папку docs для PDF файлов
app.mount(
    "/docs",
    StaticFiles(directory="static/docs"),
    name="docs"
)

# ────────────────────────────────────────
# SPA Fallback - все остальные роуты отдают index.html
# ────────────────────────────────────────
@app.get("/{full_path:path}")
async def spa_handler(request: Request, full_path: str):
    """
    Обрабатываем все остальные роуты и отдаем index.html для SPA.
    Исключаем API роуты, которые уже обработаны выше.
    """
    # Если это запрос к статическому файлу, пытаемся его найти
    if "." in full_path:
        file_path = f"static/{full_path}"
        if os.path.exists(file_path):
            return FileResponse(file_path)

    # Для всех остальных роутов отдаем index.html (SPA)
    return FileResponse("static/index.html")


# ────────────────────────────────────────
# Точка входа Uvicorn
# ────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("BACKEND_PORT", settings.server.port)),
        reload=settings.server.reload,
        log_level=settings.log.level.lower(),
        log_config=None,
    )
