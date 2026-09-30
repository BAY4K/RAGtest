from sentence_transformers import SentenceTransformer


def load_embedding_model(model) -> SentenceTransformer:
    print('Загрузка embedding-модели...')

    embedding_model = SentenceTransformer(model)

    return embedding_model

def embed_chunks(
        model: SentenceTransformer,
        chunks: list,
):
    chunk_inputs = [
        f'passage: {chunk}'
        for chunk in chunks
    ]

    chunk_vectors = model.encode(
        chunk_inputs,
        normalize_embeddings=True,
    )

    return chunk_vectors

def embed_query(model: SentenceTransformer, question: str):
    query_vector = model.encode(
        f'query: {question}',
        normalize_embeddings=True,
    )

    return query_vector