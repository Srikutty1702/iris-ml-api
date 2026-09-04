import logging

from logging.handlers import RotatingFileHandler

from app.config import settings


logger = logging.getLogger("ml_api")

logger.setLevel(settings.LOG_LEVEL)

file_handler = RotatingFileHandler(
    "app.log",
    maxBytes=1_000_000,
    backupCount=3
)

console_handler = logging.StreamHandler()

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

file_handler.setFormatter(formatter)

console_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.addHandler(console_handler)