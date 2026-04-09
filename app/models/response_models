from pydantic import BaseModel
from typing import List, Optional


class SourceChunk(BaseModel):
    text: str
    score: Optional[float] = None
    metadata: Optional[dict] = None


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceChunk]
    llm_model: str
    latency_seconds: float
    cached: bool = False


class HealthResponse(BaseModel):
    status: str
    timestamp: str


class UploadResponse(BaseModel):
    message: str
    filename: str
    chunks_created: int
