from google import genai
from app.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class EmbeddingService:
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing in .env")

        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.model_name = settings.EMBEDDING_MODEL

    def embed_text(self, text: str) -> list[float]:
        try:
            response = self.client.models.embed_content(
                model=self.model_name,
                contents=[text]
            )

            if hasattr(response, "embeddings") and response.embeddings:
                return response.embeddings[0].values

            raise RuntimeError("No embeddings returned from Gemini.")
        except Exception as e:
            logger.exception("Error while generating embeddings.")
            raise RuntimeError(f"Embedding generation failed: {str(e)}")

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        try:
            response = self.client.models.embed_content(
                model=self.model_name,
                contents=texts
            )

            if hasattr(response, "embeddings") and response.embeddings:
                return [item.values for item in response.embeddings]

            raise RuntimeError("No embeddings returned from Gemini.")
        except Exception as e:
            logger.exception("Error while generating batch embeddings.")
            raise RuntimeError(f"Batch embedding generation failed: {str(e)}")
