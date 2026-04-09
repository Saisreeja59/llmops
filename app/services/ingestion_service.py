import os
from fastapi import UploadFile
from app.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class IngestionService:
    def __init__(self):
        os.makedirs(settings.RAW_DATA_DIR, exist_ok=True)

    async def save_uploaded_file(self, file: UploadFile) -> str:
        file_path = os.path.join(settings.RAW_DATA_DIR, file.filename)

        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)

        logger.info("Saved uploaded file: %s", file_path)
        return file_path

    def load_text_file(self, file_path: str) -> str:
        if not file_path.endswith(".txt"):
            raise ValueError("Currently only .txt files are supported.")

        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
