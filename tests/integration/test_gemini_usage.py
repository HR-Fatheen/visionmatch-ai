import os

from dotenv import load_dotenv

from app.database import SessionLocal
from app.models.ai_usage import AIUsage
from app.services.ai_cost_service import estimate_gemini_cost
from app.services.gemini_vision_provider import GeminiVisionProvider

load_dotenv()

image_path = "data/images/gemini-test.jpg"

db = SessionLocal()

try:
    provider = GeminiVisionProvider()

    result = provider.analyze_image(image_path)

    assert result.usage is not None

    usage = result.usage

    estimated_cost = estimate_gemini_cost(
        input_units=usage.input_units,
        output_units=usage.output_units,
    )

    record = AIUsage(
        operation="test_vision_analysis",
        model_name=usage.model_name,
        input_units=usage.input_units,
        output_units=usage.output_units,
        estimated_cost=estimated_cost,
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    print("Usage ID:", record.id)
    print("Operation:", record.operation)
    print("Model:", record.model_name)
    print("Input units:", record.input_units)
    print("Output units:", record.output_units)
    print("Estimated cost:", record.estimated_cost)

    assert record.input_units > 0
    assert record.output_units > 0
    assert record.estimated_cost > 0

    print("Gemini usage persistence test: PASSED")

finally:
    if "record" in locals():
        db.delete(record)
        db.commit()

    db.close()

    print("Cleanup: done")