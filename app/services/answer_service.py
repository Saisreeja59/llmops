from app.models.response_models import AskResponse, SourceChunk


class AnswerService:
    def build_response(self, result: dict) -> AskResponse:
        source_chunks = [
            SourceChunk(
                text=item["text"],
                score=item.get("score"),
                metadata=item.get("metadata")
            )
            for item in result["sources"]
        ]

        return AskResponse(
            question=result["question"],
            answer=result["answer"],
            sources=source_chunks,
            llm_model=result["model_used"],
            latency_seconds=result["latency_seconds"],
            cached=result["cached"]
        )
