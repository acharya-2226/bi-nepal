"""
logger.py  -  Logging: console + rotating file at logs/app.log
Usage in any module:
    from logger import get_logger
    logger = get_logger(__name__)
"""
import logging
import logging.handlers
from pathlib import Path

_READY = False
FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE   = "%Y-%m-%d %H:%M:%S"
BASE_DIR = Path(__file__).resolve().parent


def setup_logging(level: str = "INFO") -> None:
    global _READY
    if _READY:
        return
    log_level = getattr(logging, level.upper(), logging.INFO)
    root = logging.getLogger()
    root.setLevel(log_level)
    fmt = logging.Formatter(FORMAT, datefmt=DATE)

    ch = logging.StreamHandler()
    ch.setFormatter(fmt)
    root.addHandler(ch)

    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)
    fh = logging.handlers.RotatingFileHandler(
        str(log_dir / "app.log"), maxBytes=5_000_000, backupCount=3, encoding="utf-8"
    )
    fh.setFormatter(fmt)
    root.addHandler(fh)
    _READY = True


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
