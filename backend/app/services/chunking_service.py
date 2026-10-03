import re


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50
) -> list[str]:

    if not text.strip():
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    chunks = []
    current_sentences = []
    current_length = 0

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        additional_length = len(sentence) + (
            1 if current_sentences else 0
        )

        if (
            current_sentences
            and current_length + additional_length > chunk_size
        ):
            chunks.append(" ".join(current_sentences))

            # Keep complete previous sentences for overlap
            overlap_sentences = []
            overlap_length = 0

            for previous_sentence in reversed(current_sentences):
                sentence_length = len(previous_sentence) + (
                    1 if overlap_sentences else 0
                )

                if overlap_length + sentence_length > overlap:
                    break

                overlap_sentences.insert(0, previous_sentence)
                overlap_length += sentence_length

            current_sentences = overlap_sentences
            current_length = len(" ".join(current_sentences))

        current_sentences.append(sentence)
        current_length = len(" ".join(current_sentences))

    if current_sentences:
        chunks.append(" ".join(current_sentences))

    return chunks