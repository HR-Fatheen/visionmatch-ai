from abc import ABC, abstractmethod

from app.services.embedding_result import EmbeddingResult


class EmbeddingProvider(ABC):
    @abstractmethod
    def embed_text(
        self,
        text: str,
    ) -> EmbeddingResult:
        raise NotImplementedError