from app.core.config import TOP_K, EMBEDDING_MODEL
from app.rag.sample_data import DOCUMENT_TEXT
from app.rag.chunking import split_into_sentences, create_chunks
from app.rag.embeddings import load_embedding_model, embed_chunks, embed_query
from app.llm.client import ask_llm
from app.rag.context import build_context
from app.db.session import check_connection
from app.db.services import save_document, search_similar_chunks


def main() -> None:
    check_connection()

    sentences = split_into_sentences(
        DOCUMENT_TEXT
    )


    chunks = create_chunks(
        sentences,
        max_chars=300,
        overlap_sentences=1,
    )

    model = load_embedding_model(EMBEDDING_MODEL)

    # chunk_vectors = embed_chunks(model, chunks)
    #
    # created_embeddings = chunk_vectors.tolist()
    #
    # document_id = save_document(
    #     title="Текстовый документ",
    #     chunks=chunks,
    #     embeddings=created_embeddings,
    # )

    print()

    question = input('Введите вопрос: ').strip()


    if not question:
        print('Вопрос не введён.')

        return


    query_vector = embed_query(model, question)

    retrieved = search_similar_chunks(
        query_vector.tolist(),
        TOP_K
    )

    print()
    print('=== RETRIEVAL ===')

    for position, (
        chunk_index,
        chunk_text,
        score,
    ) in enumerate(retrieved, start=1):
        print()

        print(
            f'{position}. '
            f'chunk={chunk_index + 1}, '
            f'score={score:.4f}'
        )

        print(
            chunk_text
        )


    context = build_context(retrieved)

    print()
    print(
        '=== КОНТЕКСТ ДЛЯ LLM ==='
    )

    print()
    print(context)


    print()
    print(
        '=== ОТВЕТ LLM ==='
    )

    print()


    answer = ask_llm(
        question=question,
        context=context,
    )

    print(answer)

if __name__ == '__main__':
    main()