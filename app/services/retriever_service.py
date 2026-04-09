import numpy as np
from app.config import settings
from app.services.embedding_service import EmbeddingService
from app.services.vectorstore_service import VectorStoreService
from app.core.logger import get_logger

logger = get_logger(__name__)


class RetrieverService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vectorstore_service = VectorStoreService()
        self.top_k = settings.TOP_K_RETRIEVAL

    def retrieve(self, query: str) -> list[dict]:
        index, metadata = self.vectorstore_service.load_index()

        if index is None or metadata is None:
            raise RuntimeError(
                "Vector store not found. Please upload and index documents first."
            )

        if not metadata:
            raise RuntimeError("No metadata found in vector store.")

        query_embedding = self.embedding_service.embed_text(query)
        query_vector = np.array([query_embedding], dtype="float32")

        valid_k = min(self.top_k, len(metadata))
        distances, indices = index.search(query_vector, valid_k)

        results = []
        seen_indices = set()

        for score, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue

            if idx in seen_indices:
                continue

            if score > 1e10:
                continue

            if idx >= len(metadata):
                continue

            item = metadata[idx].copy()
            item["score"] = float(score)
            results.append(item)
            seen_indices.add(idx)

        results = sorted(results, key=lambda x: x["score"])

        logger.info(
            "Retrieved %d valid chunk(s) for query: %s",
            len(results),
            query
        )

        return results
