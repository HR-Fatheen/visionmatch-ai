from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from app.database import Base


class PostVector(Base):
    __tablename__ = "post_vectors"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"),
        nullable=False,
        unique=True,
    )
    embedding: Mapped[list[float]] = mapped_column(
        Vector(768),
        nullable=False,
    )