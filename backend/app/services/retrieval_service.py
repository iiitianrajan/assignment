from sqlalchemy import text
from sqlalchemy.orm import Session

from app.services.embedding_service import generate_embedding


def retrieve_similar_chunks(
    db: Session,
    query: str,
    top_k: int = 5
):
    query_embedding = generate_embedding(query)

    embedding_string = "[" + ",".join(
        str(value) for value in query_embedding
    ) + "]"

    result = db.execute(
    text("""
        SELECT
            kc.id,
            kc.document_id,
            kd.record_id,
            kd.title,
            kd.category,
            kc.chunk_index,
            kc.content,
            kc.page_number,
            kc.section_title,
            kc.embedding <=> CAST(:embedding AS vector) AS distance
        FROM knowledge_chunks kc
        JOIN knowledge_documents kd
            ON kd.id = kc.document_id
        ORDER BY kc.embedding <=> CAST(:embedding AS vector)
        LIMIT :top_k
    """),
    {
        "embedding": embedding_string,
        "top_k": top_k
    }
)

    return result.fetchall()