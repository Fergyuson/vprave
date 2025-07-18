# ───────────────────────────
# 0. Импорт и подготовка
# ───────────────────────────
import logging
import warnings
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from .config import settings, BASE_DIR


class ColorFormatter(logging.Formatter):
    # ANSI-коды
    COLORS = {
        logging.DEBUG:    "\033[34m",        # синий
        logging.INFO:     "\033[32m",        # зелёный
        logging.WARNING:  "\033[33m",        # жёлтый
        logging.ERROR:    "\033[31m",        # красный
        logging.CRITICAL: "\033[1;31m",      # ярко-красный (bold)
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, self.RESET)
        record.levelname = f"{color}{record.levelname:<8}{self.RESET}"
        return super().format(record)

# ───────────────────────────
# 1. Каталог логов
# ───────────────────────────
LOG_DIR: Path = BASE_DIR / settings.log.dir
LOG_DIR.mkdir(parents=True, exist_ok=True)


# ───────────────────────────
# 2. Формат и уровень
# ───────────────────────────
LOG_LEVEL = getattr(logging, settings.log.level.upper(), logging.INFO)
fmt_file  = logging.Formatter(settings.log.fmt, datefmt="%Y-%m-%d %H:%M:%S")

# цветной формат только для терминала
fmt_console = ColorFormatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# ───────────────────────────
# 3. Консоль
# ───────────────────────────
stream_handler = logging.StreamHandler()
stream_handler.setLevel(LOG_LEVEL)
stream_handler.setFormatter(fmt_console)


# ───────────────────────────
# 4. Файл (ротация)
# ───────────────────────────
file_handler = TimedRotatingFileHandler(
    filename=LOG_DIR / settings.log.filename,
    when=settings.log.rotation_when,
    interval=settings.log.rotation_interval,
    backupCount=settings.log.retention_days,
    encoding="utf-8",
    delay=True
)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(fmt_file)


# ───────────────────────────
# 5. Навешиваем хендлеры на **root**-логгер
# ───────────────────────────
root = logging.getLogger()
root.handlers.clear()
root.setLevel(LOG_LEVEL)
root.addHandler(stream_handler)
root.addHandler(file_handler)

# ваш именованный логгер может наследовать хендлеры
app_logger = logging.getLogger(settings.app_name)
app_logger.propagate = True


# ───────────────────────────
# 6. Глушим ворнинги FastAPI
# ───────────────────────────
warnings.filterwarnings(
    "ignore",
    category=DeprecationWarning,
    module=r"fastapi\.",
)
