import os

from dotenv import load_dotenv

from app.services.gemini_vision_provider import GeminiVisionProvider

load_dotenv()

image_path = "data/images/gemini-test.jpg"

if not os.path.exists(image_path):
    raise FileNotFoundError(
        f"Test image not found: {image_path}"
    )

provider = GeminiVisionProvider()

result = provider.analyze_image(image_path)

metadata = result.metadata
usage = result.usage

print("Tags:", metadata.tags)
print("Caption:", metadata.caption)
print("Confidence:", metadata.confidence)
print("Input units:", usage.input_units)
print("Output units:", usage.output_units)
print("Model:", usage.model_name)

assert len(metadata.tags) >= 3
assert metadata.caption
assert 0.0 <= metadata.confidence <= 1.0

print("Gemini vision test: PASSED")