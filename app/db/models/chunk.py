from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, Identity, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pgvector.sqlalchemy import VECTOR

from app.core.config import EMBEDDING_DIM
from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.document import Document

class Chunk(Base):
    __tablename__ = "chunks"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(),
        primary_key=True
    )
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    chunk_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    embedding:Mapped[list[float] | None] = mapped_column(
        VECTOR(EMBEDDING_DIM),
        nullable=True
    )

    document: Mapped["Document"] = relationship(
        back_populates="chunks",
    )