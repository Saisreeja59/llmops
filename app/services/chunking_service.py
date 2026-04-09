from app.config import settings


class ChunkingService:
    def __init__(self):
        self.chunk_size = settings.MAX_CHUNK_SIZE
        self.chunk_overlap = settings.CHUNK_OVERLAP

    def chunk_text(self, text: str) -> list[str]:
        text = text.strip()
        if not text:
            return []

        chunks = []
        start = 0
        text_length = len(text)

        while start < text_length:
            end = start + self.chunk_size
            chunk = text[start:end]
            chunks.append(chunk)

            if end >= text_length:
                break

            start = end - self.chunk_overlap

        return chunks
