import re

def split_into_sentences(
        text: str,
) -> list[str]:
    """
    Разбивает текст на предложения.

    Пока используем простой regex.
    В production позже сделаем обработку умнее.
    """

    return re.split(
        r'(?<=[.!?])\s+',
        text,
    )


def create_chunks(
        sentences: list[str],
        max_chars: int = 300,
        overlap_sentences: int = 1,
) -> list[str]:
    """
    Собирает предложения в chunks.

    Если chunk становится слишком большим,
    он сохраняется.

    Несколько последних предложений
    переносятся в следующий chunk как overlap.
    """

    chunks: list[str] = []

    current_sentences: list[str] = []
    current_length = 0


    for sentence in sentences:
        sentence = sentence.strip()

        if not sentence:
            continue


        new_length = (current_length + len(sentence) + 1)

        if current_sentences and new_length > max_chars:
            chunks.append(
                ' '.join(current_sentences)
            )


            if overlap_sentences > 0:
                current_sentences = current_sentences[-overlap_sentences:]
            else:
                current_sentences = []


            current_length = sum(
                len(value) + 1
                for value
                in current_sentences
            )


        current_sentences.append(sentence)

        current_length += len(sentence) + 1


    if current_sentences:
        chunks.append(' '.join(current_sentences))


    return chunks
