from sqlalchemy import select

from app.db.database import SessionLocal
from app.db.models.models import Chunk, Document

def save_document(
        title: str,
        chunks: list[str],
) -> int:
    with SessionLocal.begin() as session:
        document = Document(
            title=title,
        )
        session.add(document)
        session.flush()
        for chunk_number, content in enumerate(chunks):
            chunk = Chunk(
                document_id=document.id,
                chunk_number=chunk_number,
                content=content,
            )
            session.add(chunk)

        return document.id

def get_document(document_id: int) -> Document | None:
    with SessionLocal() as session:
        return session.get(Document, document_id)

def get_document_chunks(document_id: int) -> list[Chunk]:
    with SessionLocal() as session:
        statement = (
            select(Chunk)
            .where(Chunk.document_id == document_id)
            .order_by(Chunk.chunk_number)
        )

        result = session.execute(statement)

        return list(result.scalars().all())