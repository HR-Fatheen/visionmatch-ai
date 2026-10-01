from sqlalchemy.orm import Session

from app.models.ai_usage import AIUsage


def record_ai_usage(
    db: Session,
    operation: str,
    model_name: str,
    input_units: int,
    output_units: int,
    estimated_cost: float,
) -> AIUsage:
    usage = AIUsage(
        operation=operation,
        model_name=model_name,
        input_units=input_units,
        output_units=output_units,
        estimated_cost=estimated_cost,
    )

    db.add(usage)
    db.commit()
    db.refresh(usage)

    return usage