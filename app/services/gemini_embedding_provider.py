import os

from google import genai

from app.services.embedding_provider import EmbeddingProvider
from app.services.embedding_result import EmbeddingResult


class GeminiEmbeddingProvider(EmbeddingProvider):
    MODEL_NAME = "gemini-embedding-2"

    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set"
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def embed_text(self, text: str) -> EmbeddingResult:
        if not text.strip():
            raise ValueError("Text cannot be empty")

        token_count = self.client.models.count_tokens(
            model=self.MODEL_NAME,
            contents=text,
        )

        response = self.client.models.embed_content(
            model=self.MODEL_NAME,
            contents=text,
        )

        if not response.embeddings:
            raise ValueError("Gemini returned no embedding")

        embedding = response.embeddings[0]

        if embedding.values is None:
            raise ValueError("Gemini returned an embedding without values")

        return EmbeddingResult(
            vector=list(embedding.values),
            model_name=self.MODEL_NAME,
            input_units=token_count.total_tokens,
        )