import mimetypes
import os

from google import genai
from google.genai import types

from app.services.vision_provider import VisionProvider
from app.services.vision_schema import VisionMetadata
from app.services.ai_usage_result import AIUsageResult
from app.services.vision_analysis_result import VisionAnalysisResult


class GeminiVisionProvider(VisionProvider):
    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not set"
            )

        self.client = genai.Client(
            api_key=api_key
        )

    def analyze_image(
        self,
        image_path: str,
    ) -> VisionAnalysisResult:
        mime_type, _ = mimetypes.guess_type(image_path)

        if not mime_type or not mime_type.startswith("image/"):
            raise ValueError(
                f"Unsupported image type: {image_path}"
            )

        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type,
                ),
                """
Analyze this image for an image-to-content matching system.

Return:
- 3 or more concise tags describing the main subjects,
  objects, or concepts.
- A factual one-sentence caption.
- A confidence score between 0.0 and 1.0.

Do not guess details that cannot reasonably be determined
from the image.
""",
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=VisionMetadata,
            ),
        )

        usage = AIUsageResult(
            input_units=response.usage_metadata.prompt_token_count,
            output_units=response.usage_metadata.candidates_token_count,
            model_name="gemini-2.5-flash",
        )

        metadata = VisionMetadata.model_validate_json(
        response.text
        )

        return VisionAnalysisResult(
            metadata=metadata,
            usage=usage,
        )