from app.services.vision_provider import VisionProvider
from app.services.vision_schema import VisionMetadata


class MockVisionProvider(VisionProvider):

    def analyze_image(self, image_path: str) -> VisionMetadata:
        return VisionMetadata(
            tags=["red fox", "wildlife", "animal"],
            caption="A red fox standing in a forest.",
            confidence=0.94,
        )