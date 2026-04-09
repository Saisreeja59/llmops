from fastapi import FastAPI
from app.config import settings
from app.api.routes.health import router as health_router
from app.api.routes.upload import router as upload_router
from app.api.routes.ask import router as ask_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

app.include_router(health_router, prefix="/health", tags=["Health"])
app.include_router(upload_router, prefix="/upload", tags=["Upload"])
app.include_router(ask_router, prefix="/ask", tags=["Ask"])


@app.get("/")
def root():
    return {
        "message": "Welcome to the LLMOps RAG System",
        "version": settings.APP_VERSION
    }
