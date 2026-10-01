from dataclasses import dataclass


@dataclass
class AIUsageResult:
    input_units: int
    output_units: int
    model_name: str