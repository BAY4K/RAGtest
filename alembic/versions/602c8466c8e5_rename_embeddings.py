"""rename embeddings

Revision ID: 602c8466c8e5
Revises: 243b227bc00c
Create Date: 2026-10-08 20:28:28.531792

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '602c8466c8e5'
down_revision: Union[str, Sequence[str], None] = '243b227bc00c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "chunks",
        "embeddings",
        new_column_name="embedding",
    )


def downgrade() -> None:
    op.alter_column(
        "chunks",
        "embedding",
        new_column_name="embeddings",
    )
