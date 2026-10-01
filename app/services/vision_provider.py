from abc import ABC, abstractmethod

from app.services.vision_schema import VisionMetadata


class VisionProvider(ABC):

    @abstractmethod
    def analyze_image(self, image_path: str) -> VisionMetadata:
        """Analyze an image and return validated metadata."""
        raise NotImplementedError