import logging
import logging.handlers
import re
from contextvars import ContextVar
from pathlib import Path

from my_fastapi_project.core.config import get_settings

LOG_DIR = Path("logs")

LOG_FORMAT = "%(asctime)s [%(levelname)s] [%(request_id)s] %(name)s: %(message)s"
LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"

TOKEN_PATTERN = re.compile(r"(token=)[^&\s]+")

request_id_var: ContextVar[str] = ContextVar("request_id", default="-")

_record_factory_installed = False


def _install_record_factory() -> None:
    global _record_factory_installed
    if _record_factory_installed:
        return

    original = logging.getLogRecordFactory()

    def factory(*args, **kwargs):
        record = original(*args, **kwargs)
        record.request_id = request_id_var.get()
        return record

    logging.setLogRecordFactory(factory)
    _record_factory_installed = True


class RedactingFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return TOKEN_PATTERN.sub(r"\1***", super().format(record))


def setup_logging(level: int = logging.INFO) -> None:
    _install_record_factory()

    settings = get_settings()

    formatter = RedactingFormatter(LOG_FORMAT, datefmt=LOG_DATEFMT)

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(console)

    if settings.LOG_TO_FILE:
        LOG_DIR.mkdir(exist_ok=True)

        file_handler = logging.handlers.TimedRotatingFileHandler(
            LOG_DIR / "app.log",
            when="midnight",
            backupCount=7,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        root.addHandler(file_handler)
