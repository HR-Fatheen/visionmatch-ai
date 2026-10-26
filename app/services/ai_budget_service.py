import os
from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.ai_usage import AIUsage


class AIBudgetExceededError(RuntimeError):
    """Raised when the configured daily AI budget would be exceeded."""


def ensure_ai_budget_available(
    db: Session,
    estimated_next_cost: float = 0.05,
) -> None:
    """Check today's recorded AI spending before making another request."""

    try:
        daily_budget = float(os.getenv("AI_DAILY_BUDGET_USD", "5.00"))
    except ValueError as exc:
        raise ValueError(
            "AI_DAILY_BUDGET_USD must be a valid number."
        ) from exc

    if daily_budget <= 0:
        raise ValueError("AI_DAILY_BUDGET_USD must be greater than zero.")

    if estimated_next_cost < 0:
        raise ValueError("estimated_next_cost cannot be negative.")

    now = datetime.now(timezone.utc)
    utc_midnight = now.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
        tzinfo=None,
    )

    spent_today = (
        db.query(func.coalesce(func.sum(AIUsage.estimated_cost), 0.0))
        .filter(AIUsage.created_at >= utc_midnight)
        .scalar()
    )

    spent_today = float(spent_today or 0.0)

    if spent_today + estimated_next_cost > daily_budget:
        raise AIBudgetExceededError(
            "Daily AI budget limit reached. "
            f"Recorded spending: ${spent_today:.4f}; "
            f"daily limit: ${daily_budget:.2f}. "
            "No new AI request should be started."
        )
