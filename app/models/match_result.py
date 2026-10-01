from sqlalchemy import Boolean, Float, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MatchResult(Base):
    __tablename__ = "match_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"),
        nullable=False,
    )

    image_id: Mapped[int] = mapped_column(
        ForeignKey("images.id"),
        nullable=False,
    )

    similarity_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    accepted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
    )

    explanation: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )