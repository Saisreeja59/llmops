import os
from app.config import settings


def load_prompt(filename: str) -> str:
    path = os.path.join(settings.PROMPTS_DIR, filename)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Prompt file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return f.read()
