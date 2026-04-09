import logging
import os
from app.config import settings


def get_logger(name: str) -> logging.Logger:
    os.makedirs(settings.LOG_DIR, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        app_file_handler = logging.FileHandler(
            os.path.join(settings.LOG_DIR, "app.log"),
            encoding="utf-8"
        )
        app_file_handler.setLevel(logging.INFO)
        app_file_handler.setFormatter(formatter)

        error_file_handler = logging.FileHandler(
            os.path.join(settings.LOG_DIR, "error.log"),
            encoding="utf-8"
        )
        error_file_handler.setLevel(logging.ERROR)
        error_file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        stream_handler.setFormatter(formatter)

        logger.addHandler(app_file_handler)
        logger.addHandler(error_file_handler)
        logger.addHandler(stream_handler)

    return logger
