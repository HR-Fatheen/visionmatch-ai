from dataclasses import dataclass

from app.models.image import Image


@dataclass
class RankedImage:
    image: Image
    similarity_score: float