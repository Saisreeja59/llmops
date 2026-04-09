import time
from typing import Any, Optional


class SimpleCache:
    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self.store: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Optional[Any]:
        item = self.store.get(key)
        if not item:
            return None

        value, created_at = item
        if time.time() - created_at > self.ttl_seconds:
            del self.store[key]
            return None

        return value

    def set(self, key: str, value: Any) -> None:
        self.store[key] = (value, time.time())

    def delete(self, key: str) -> None:
        if key in self.store:
            del self.store[key]

    def clear(self) -> None:
        self.store.clear()
