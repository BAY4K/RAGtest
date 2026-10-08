from sqlalchemy import select

from app.db.session import SessionLocal
from app.db.models import Chunk, Document

def save_document(
        title: str,
        chunks: list[str],
        embeddings: list[list[float]],
) -> int:
    if len(chunks) != len(embeddings):
        raise ValueError(
            "Количество chunks и embeddings должно совпадать."
        )

    with SessionLocal.begin() as session:
        document = Document(title=title)
        session.add(document)
        session.flush()

        for chunk_number, (content, embedding) in enumerate(
                zip(chunks, embeddings, strict=True)):
            chunk = Chunk(
                document_id=document.id,
                chunk_number=chunk_number,
                content=content,
                embedding=embedding,
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