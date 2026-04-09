import time
from app.config import settings
from app.core.prompts import load_prompt
from app.core.cache import SimpleCache
from app.core.logger import get_logger
from app.services.retriever_service import RetrieverService
from app.services.llm_service import LLMService
from app.services.guardrail_service import GuardrailService

logger = get_logger(__name__)

cache = SimpleCache(ttl_seconds=settings.CACHE_TTL_SECONDS)


class RAGPipeline:
    def __init__(self):
        self.retriever = RetrieverService()
        self.llm_service = LLMService()
        self.guardrail_service = GuardrailService()

    def run(self, question: str, use_cache: bool = True) -> dict:
        start_time = time.time()

        self.guardrail_service.validate_question(question)

        cache_key = question.strip().lower()

        if settings.CACHE_ENABLED and use_cache:
            cached_result = cache.get(cache_key)
            if cached_result:
                logger.info("Cache hit for question: %s", question)
                cached_result["cached"] = True
                return cached_result

        retrieved_chunks = self.retriever.retrieve(question)

        if not retrieved_chunks:
            raise RuntimeError("No relevant chunks found for the given question.")

        context = "\n\n".join([item["text"] for item in retrieved_chunks])

        prompt_template = load_prompt("qa_prompt.txt")
        final_prompt = prompt_template.format(
            context=context,
            question=question
        )

        answer = self.llm_service.generate_response(final_prompt)
        answer = self.guardrail_service.validate_answer(answer)

        latency = round(time.time() - start_time, 3)

        result = {
            "question": question,
            "answer": answer,
            "sources": retrieved_chunks,
            "model_used": self.llm_service.model_name,
            "latency_seconds": latency,
            "cached": False
        }

        if settings.CACHE_ENABLED and use_cache:
            cache.set(cache_key, result.copy())
            logger.info("Cached result for question: %s", question)

        logger.info("RAG pipeline completed successfully for question: %s", question)
        return result
