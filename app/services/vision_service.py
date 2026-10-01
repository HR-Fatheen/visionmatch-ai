from app.services.vision_schema import VisionMetadata


LOW_CONFIDENCE_THRESHOLD = 0.70


def is_low_confidence(metadata: VisionMetadata) -> bool:
    return metadata.confidence < LOW_CONFIDENCE_THRESHOLD