"""add vector embeddings

Revision ID: 243b227bc00c
Revises: 22dc824b6861
Create Date: 2026-10-08 19:35:58.135726

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from pgvector.sqlalchemy import VECTOR


# revision identifiers, used by Alembic.
revision: str = '243b227bc00c'
down_revision: Union[str, Sequence[str], None] = '22dc824b6861'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "CREATE EXTENSION IF NOT EXISTS vector"
    )

    op.add_column("chunks", sa.Column(
        "embedding", VECTOR(768), nullable=True
    ))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "chunks",
        "embedding",
    )
