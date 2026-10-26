"""Initial database schema.

Revision ID: 778833e818e7
Revises:
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


revision: str = "778833e818e7"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the original database schema."""

    # Required before creating pgvector embedding columns.
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "ai_usage",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("operation", sa.String(length=100), nullable=False),
        sa.Column("model_name", sa.String(length=100), nullable=False),
        sa.Column("input_units", sa.Integer(), nullable=False),
        sa.Column("output_units", sa.Integer(), nullable=False),
        sa.Column("estimated_cost", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "images",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("filepath", sa.String(length=500), nullable=False),
        sa.Column("caption", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_table(
        "image_vectors",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("image_id", sa.Integer(), nullable=False),
        sa.Column("embedding", Vector(768), nullable=False),
        sa.ForeignKeyConstraint(["image_id"], ["images.id"]),
        sa.UniqueConstraint("image_id"),
    )

    op.create_table(
        "post_vectors",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("embedding", Vector(768), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"]),
        sa.UniqueConstraint("post_id"),
    )

    op.create_table(
        "match_results",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.Column("image_id", sa.Integer(), nullable=False),
        sa.Column("similarity_score", sa.Float(), nullable=False),
        sa.Column("accepted", sa.Boolean(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"]),
        sa.ForeignKeyConstraint(["image_id"], ["images.id"]),
    )

    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("match_result_id", sa.Integer(), nullable=False),
        sa.Column("reviewer_decision", sa.Boolean(), nullable=False),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("reviewed_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["match_result_id"],
            ["match_results.id"],
        ),
    )


def downgrade() -> None:
    """Drop the original database tables."""

    op.drop_table("reviews")
    op.drop_table("match_results")
    op.drop_table("post_vectors")
    op.drop_table("image_vectors")
    op.drop_table("posts")
    op.drop_table("images")
    op.drop_table("ai_usage")