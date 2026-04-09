import os
import pickle
import numpy as np
import faiss
from app.config import settings
from app.core.logger import get_logger

logger = get_logger(__name__)


class VectorStoreService:
    def __init__(self):
        os.makedirs(settings.VECTORSTORE_DIR, exist_ok=True)
        self.index_path = os.path.join(settings.VECTORSTORE_DIR, "faiss.index")
        self.metadata_path = os.path.join(settings.VECTORSTORE_DIR, "metadata.pkl")

    def save_index(self, embeddings: list[list[float]], metadata: list[dict]) -> None:
        if not embeddings:
            raise ValueError("No embeddings provided to save.")

        vectors = np.array(embeddings).astype("float32")
        dimension = vectors.shape[1]

        index = faiss.IndexFlatL2(dimension)
        index.add(vectors)

        faiss.write_index(index, self.index_path)

        with open(self.metadata_path, "wb") as f:
            pickle.dump(metadata, f)

        logger.info("FAISS index and metadata saved successfully.")

    def load_index(self):
        if not os.path.exists(self.index_path) or not os.path.exists(self.metadata_path):
            return None, None

        index = faiss.read_index(self.index_path)

        with open(self.metadata_path, "rb") as f:
            metadata = pickle.load(f)

        return index, metadata
