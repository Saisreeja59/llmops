from fastapi import APIRouter, HTTPException
from app.models.request_models import AskRequest
from app.services.answer_service import AnswerService
from app.workflows.rag_pipeline import RAGPipeline
from app.core.exceptions import GuardrailViolationError, LLMServiceError

router = APIRouter()


@router.post("/")
def ask_question(request: AskRequest):
    try:
        pipeline = RAGPipeline()
        answer_service = AnswerService()

        result = pipeline.run(
            question=request.question,
            use_cache=request.use_cache
        )

        return answer_service.build_response(result)

    except GuardrailViolationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except LLMServiceError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
