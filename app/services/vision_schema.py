from pydantic import BaseModel, Field


class VisionMetadata(BaseModel):
    tags: list[str] = Field(min_length=1)
    caption: str = Field(min_length=1)
    confidence: float = Field(ge=0.0, le=1.0)