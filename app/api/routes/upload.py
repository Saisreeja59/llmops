from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.response_models import UploadResponse
from app.services.ingestion_service import IngestionService
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.vectorstore_service import VectorStoreService
from app.core.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post("/", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".txt"):
            raise HTTPException(
                status_code=400,
                detail="Only .txt files are supported for now."
            )

        ingestion_service = IngestionService()
        chunking_service = ChunkingService()
        embedding_service = EmbeddingService()
        vectorstore_service = VectorStoreService()

        file_path = await ingestion_service.save_uploaded_file(file)
        text = ingestion_service.load_text_file(file_path)

        chunks = chunking_service.chunk_text(text)
        if not chunks:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        embeddings = embedding_service.embed_texts(chunks)

        metadata = [
            {
                "text": chunk,
                "metadata": {"filename": file.filename}
            }
            for chunk in chunks
        ]

        vectorstore_service.save_index(embeddings, metadata)

        logger.info(
            "File uploaded and indexed successfully: %s | chunks=%d",
            file.filename,
            len(chunks)
        )

        return UploadResponse(
            message="File uploaded and indexed successfully.",
            filename=file.filename,
            chunks_created=len(chunks)
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Upload failed.")
        raise HTTPException(status_code=500, detail=str(e))
