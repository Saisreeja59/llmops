from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "LLMOps RAG System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    LLM_PROVIDER: str = "gemini"
    GOOGLE_API_KEY: str = ""
    LLM_MODEL: str = "models/gemini-2.5-flash"
    EMBEDDING_MODEL: str = "models/gemini-embedding-001"

    DATA_DIR: str = "data"
    RAW_DATA_DIR: str = "data/raw"
    PROCESSED_DATA_DIR: str = "data/processed"
    LOG_DIR: str = "logs"
    PROMPTS_DIR: str = "prompts"
    VECTORSTORE_DIR: str = "vectorstore"

    CACHE_ENABLED: bool = True
    CACHE_TTL_SECONDS: int = 300

    TOP_K_RETRIEVAL: int = 3
    MAX_CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    MAX_QUESTION_LENGTH: int = 1000
    BLOCKED_TERMS: str = "hack,exploit,malware"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


settings = Settings()
