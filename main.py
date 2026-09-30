from rag.config import TOP_K, embedding_model
from rag.sample_data import DOCUMENT_TEXT
from rag.chuncking import split_into_sentences, create_chunks
from rag.embeddings import load_embedding_model, embed_chunks, embed_query
from rag.retrieval import retrieve_chunks
from rag.llm import ask_llm
from rag.context import build_context


def main() -> None:

    sentences = split_into_sentences(
        DOCUMENT_TEXT
    )


    chunks = create_chunks(
        sentences,
        max_chars=300,
        overlap_sentences=1,
    )


    print(
        f'Создано chunks: {len(chunks)}'
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