from dotenv import load_dotenv

from app.database import SessionLocal
from app.services.embedding_service import generate_embedding
from app.services.gemini_embedding_provider import GeminiEmbeddingProvider


load_dotenv()

db = SessionLocal()

try:
    provider = GeminiEmbeddingProvider()

    text = "A red fox standing in a forest."

    result = generate_embedding(
        db=db,
        text=text,
        embedding_provider=provider,
    )

    print("Model:", result.model_name)
    print("Vector dimensions:", len(result.vector))
    print("Input units:", result.input_units)
    print("First 5 values:", result.vector[:5])

    assert result.model_name == "gemini-embedding-2"
    assert len(result.vector) == 3072
    assert result.input_units > 0
    assert all(isinstance(value, float) for value in result.vector)

    print("Embedding service test: PASSED")

finally:
    db.close()