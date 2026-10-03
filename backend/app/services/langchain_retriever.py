from typing import List

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import ConfigDict
from sqlalchemy import text

from app.database import SessionLocal
from app.services.embedding_service import generate_embedding


class KnowledgeRetriever(BaseRetriever):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    top_k: int = 3

    def _get_relevant_documents(self, query: str) -> List[Document]:

        db = SessionLocal()

        try:
            embedding = generate_embedding(query)

            results = db.execute(
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
                    "embedding": str(embedding),
                    "top_k": self.top_k
                }
            ).mappings().all()

            documents = []

            for row in results:

                documents.append(
                    Document(
                        page_content=row["content"],
                        metadata={
                            "chunk_id": str(row["id"]),
                            "document_id": str(row["document_id"]),
                            "record_id": row["record_id"],
                            "title": row["title"],
                            "category": row["category"],
                            "chunk_index": row["chunk_index"],
                            "distance": float(row["distance"])
                        }
                    )
                )

            return documents

        finally:
            db.close()


retriever = KnowledgeRetriever(top_k=3)

def retrieve_documents(query: str) -> List[Document]:
    return retriever.invoke(query)