from dataclasses import dataclass

from app.services.ai_usage_result import AIUsageResult
from app.services.vision_schema import VisionMetadata


@dataclass
class VisionAnalysisResult:
    metadata: VisionMetadata
    usage: AIUsageResult | None = None