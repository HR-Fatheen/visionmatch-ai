from sqlalchemy.orm import Session

from app.services.ai_cost_service import estimate_embedding_cost
from app.services.ai_usage_service import record_ai_usage
from app.services.embedding_provider import EmbeddingProvider


def generate_embedding(
    db: Session,
    text: str,
    embedding_provider: EmbeddingProvider,
):
    result = embedding_provider.embed_text(text)

    estimated_cost = estimate_embedding_cost(
        input_units=result.input_units,
    )

    record_ai_usage(
        db=db,
        operation="text_embedding",
        model_name=result.model_name,
        input_units=result.input_units,
        output_units=0,
        estimated_cost=estimated_cost,
    )

    return result