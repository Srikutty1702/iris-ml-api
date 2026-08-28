import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("ml_api")
logger.setLevel(logging.INFO)
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