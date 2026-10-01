from app.database import SessionLocal
from app.services.ai_cost_service import estimate_gemini_cost
from app.services.ai_usage_service import record_ai_usage


db = SessionLocal()

usage = None

try:
    input_units = 1000
    output_units = 500

    estimated_cost = estimate_gemini_cost(
        input_units=input_units,
        output_units=output_units,
    )

    usage = record_ai_usage(
        db=db,
        operation="test_vision_analysis",
        model_name="gemini-2.5-flash",
        input_units=input_units,
        output_units=output_units,
        estimated_cost=estimated_cost,
    )

    print("Usage ID:", usage.id)
    print("Operation:", usage.operation)
    print("Model:", usage.model_name)
    print("Input units:", usage.input_units)
    print("Output units:", usage.output_units)
    print("Estimated cost:", usage.estimated_cost)

    assert usage.id is not None
    assert usage.estimated_cost == estimated_cost

    print("AI usage test: PASSED")

finally:
    if usage is not None:
        db.delete(usage)
        db.commit()

    db.close()

    print("Cleanup: done")