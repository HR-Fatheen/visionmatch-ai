from decimal import Decimal


# Gemini 2.5 Flash standard pricing.
# Values are USD per 1 million tokens.
INPUT_COST_PER_MILLION = Decimal("0.30")
OUTPUT_COST_PER_MILLION = Decimal("2.50")
EMBEDDING_INPUT_COST_PER_MILLION = Decimal("0.20")


def estimate_gemini_cost(
    input_units: int,
    output_units: int,
) -> float:
    input_cost = (
        Decimal(input_units)
        / Decimal(1_000_000)
        * INPUT_COST_PER_MILLION
    )

    output_cost = (
        Decimal(output_units)
        / Decimal(1_000_000)
        * OUTPUT_COST_PER_MILLION
    )

    return float(input_cost + output_cost)

def estimate_embedding_cost(input_units: int) -> float:
    input_cost = (
        Decimal(input_units)
        / Decimal(1_000_000)
        * EMBEDDING_INPUT_COST_PER_MILLION
    )

    return float(input_cost)