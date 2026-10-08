from sqlalchemy import select

from app.db.models import Chunk
from app.db.session import SessionLocal


def search_similar_chunks(
        query_embedding: list[float],
        top_k: int = 3
) -> list[tuple[int, str, float]]:
    with SessionLocal() as session:
        distance = Chunk.embedding.cosine_distance(query_embedding)

        statement = (
            select(
                Chunk.chunk_number,
                Chunk.content,
                distance.label("distance"),
            )
            .where(Chunk.embedding.is_not(None))
            .order_by(distance)
            .limit(top_k)
        )

        rows = session.execute(statement).all()

        return [
            (
                chunk_number,
                content,
                1.0 - float(distance_value)
            )
            for chunk_number, content, distance_value in rows
        ]

