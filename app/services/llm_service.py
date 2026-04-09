from google import genai
from app.config import settings
from app.core.logger import get_logger
from app.core.exceptions import LLMServiceError

logger = get_logger(__name__)


class LLMService:
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY is missing in .env")

        self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        self.model_name = settings.LLM_MODEL

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )

            if not response or not getattr(response, "text", None):
                raise LLMServiceError("No text returned from LLM.")

            return response.text.strip()
        except Exception as e:
            logger.exception("Error while generating response from Gemini.")
            raise LLMServiceError(f"LLM generation failed: {str(e)}")
