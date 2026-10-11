from dataclasses import dataclass


@dataclass
class EmbeddingResult:
    vector: list[float]
    model_name: str
    input_units: int