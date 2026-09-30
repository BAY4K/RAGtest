import numpy as np


def retrieve_chunks(
        query_vector: np.ndarray,
        chunks: list[str],
        chunk_vectors: np.ndarray,
        top_k: int = 3,
) -> list[tuple[int, str, float]]:
    """
    Ищет наиболее релевантные chunks.

    Возвращает список:

    (
        индекс chunk,
        текст chunk,
        similarity score
    )
    """

    scores = chunk_vectors @ query_vector

    ranking = np.argsort(scores)[::-1]


    results: list[tuple[int, str, float]] = []

    for index in ranking[:top_k]:
        chunk_index = int(index)

        score = float(scores[chunk_index])

        results.append(
            (
                chunk_index,
                chunks[chunk_index],
                score,
            )
        )

    return results