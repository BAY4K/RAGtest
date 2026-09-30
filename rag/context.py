def build_context(
        retrieved_chunks: list[
            tuple[int, str, float]
        ],
) -> str:
    """
    Превращает найденные chunks
    в контекст, понятный LLM.

    Каждый источник получает номер:

    [1]
    [2]
    [3]

    Позже эти номера можно использовать
    как citations.
    """

    context_parts: list[str] = []


    for source_number, (
        chunk_index,
        chunk_text,
        score,
    ) in enumerate(retrieved_chunks, start=1):
        context_parts.append(
            (
                f'[Источник {source_number}]\n'
                f'Фрагмент документа №{chunk_index + 1}\n'
                f'{chunk_text}'
            )
        )


    return '\n\n'.join(
        context_parts
    )
