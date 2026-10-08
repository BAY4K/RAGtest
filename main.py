from app.core.config import TOP_K, embedding_model
from app.rag import DOCUMENT_TEXT
from app.rag import split_into_sentences, create_chunks
from app.rag.embeddings import load_embedding_model, embed_chunks, embed_query
from app.rag import retrieve_chunks
from app.rag import ask_llm
from app.rag import build_context
from app.rag import check_connection
from app.rag import save_document, get_document, get_document_chunks


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

    document_id = save_document(
        title="Текстовый документ",
        chunks=chunks,
    )

    print(f'Документ сохранён, id = : {document_id}')

    document = get_document(document_id)

    print("\nДокумент:")
    print(document.id, document.title)

    saved_chunks = get_document_chunks(document_id)

    print("\nЧанки из PostgreSQL:")

    for chunk in saved_chunks:
        print(
            chunk.id,
            chunk.chunk_number,
            chunk.content,
        )

    model = load_embedding_model(embedding_model)

    chunk_vectors = embed_chunks(model, chunks)

    print()

    question = input('Введите вопрос: ').strip()


    if not question:
        print('Вопрос не введён.')

        return


    query_vector = embed_query(model, question)

    retrieved = retrieve_chunks(
        query_vector=query_vector,
        chunks=chunks,
        chunk_vectors=chunk_vectors,
        top_k=TOP_K,
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