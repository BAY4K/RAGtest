from sqlalchemy import select

from app.db.models import Chunk
from app.db.session import SessionLocal


def search_similar_chunks(
        query_embedding: list[float],
        top_k: int
) -> list[tuple[Chunk, float]]:
    with SessionLocal() as session:
        distance = Chunk.embedding.cosine_distance(query_embedding)

        statement = (
            select(
                Chunk,
                distance.label("distance"),
            )
            .where(Chunk.embedding.is_not(None))
            .order_by(distance)
            .limit(top_k)
        )

        rows = session.execute(statement).all()

        return [
            (
                chunk,
                1.0 - float(distance_value)
            )
            for chunk, distance_value in rows
        ]

