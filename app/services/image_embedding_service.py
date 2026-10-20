import mimetypes
from pathlib import Path

from google.genai import types
from sqlalchemy.orm import Session

from app.services.ai_cost_service import estimate_embedding_cost
from app.services.ai_usage_service import record_ai_usage
from app.services.gemini_embedding_provider import GeminiEmbeddingProvider
from app.services.vector_service import save_image_vector


def generate_and_save_image_embedding(
    db: Session,
    image_id: int,
    image_path: str,
    embedding_provider: GeminiEmbeddingProvider,
):
    path = Path(image_path)

    if not path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")

    mime_type, _ = mimetypes.guess_type(str(path))

    if mime_type not in {"image/jpeg", "image/png"}:
        raise ValueError(f"Unsupported image type: {image_path}")

    image_bytes = path.read_bytes()

    image_part = types.Part.from_bytes(
        data=image_bytes,
        mime_type=mime_type,
    )

    token_count = embedding_provider.client.models.count_tokens(
        model=embedding_provider.MODEL_NAME,
        contents=[image_part],
    )

    input_units = token_count.total_tokens

    response = embedding_provider.client.models.embed_content(
        model=embedding_provider.MODEL_NAME,
        contents=[image_part],
    )

    if not response.embeddings:
        raise ValueError("Gemini returned no image embedding")

    values = response.embeddings[0].values

    if values is None:
        raise ValueError("Gemini returned an empty image embedding")

    vector = list(values)

    if len(vector) != 3072:
        raise ValueError(
            f"Expected 3072 embedding dimensions, received {len(vector)}"
        )

    estimated_cost = estimate_embedding_cost(input_units=input_units)

    record_ai_usage(
        db=db,
        operation="image_embedding",
        model_name=embedding_provider.MODEL_NAME,
        input_units=input_units,
        output_units=0,
        estimated_cost=estimated_cost,
    )

    return save_image_vector(
        db=db,
        image_id=image_id,
        vector=vector,
    )