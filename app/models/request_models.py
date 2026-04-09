from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, description="User question")
    use_cache: bool = Field(default=True, description="Whether to use cache")


class UploadResponseRequest(BaseModel):
    filename: str
