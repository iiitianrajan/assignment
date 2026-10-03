from sqlalchemy import text
from sqlalchemy.orm import Session

from services.chunking_service import chunk_text
from services.embedding_service import generate_embedding


def ingest_document(
    db: Session,
    document_id,
    content: str
):
    chunks = chunk_text(
        content,
        chunk_size=500,
        overlap=50
    )

    created_count = 0

    for index, chunk in enumerate(chunks):

        existing = db.execute(
            text("""
                SELECT id
                FROM knowledge_chunks
                WHERE document_id = :document_id
                  AND chunk_index = :chunk_index
            """),
            {
                "document_id": document_id,
                "chunk_index": index
            }
        ).first()

        if existing:
            continue

        embedding = generate_embedding(chunk)

        embedding_string = "[" + ",".join(
            str(value) for value in embedding
        ) + "]"

        db.execute(
            text("""
                INSERT INTO knowledge_chunks (
                    document_id,
                    chunk_index,
                    content,
                    embedding
                )
                VALUES (
                    :document_id,
                    :chunk_index,
                    :content,
                    CAST(:embedding AS vector)
                )
            """),
            {
                "document_id": document_id,
                "chunk_index": index,
                "content": chunk,
                "embedding": embedding_string,
            }
        )

        created_count += 1

    db.commit()

    return created_count