from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import KnowledgeDocument
from app.schemas import KnowledgeDocumentCreate, KnowledgeSearchRequest
from app.services.retrieval_service import retrieve_similar_chunks
from app.services.voice_service import process_voice_query

app = FastAPI(
    title="AI Engineer Assessment API",
    version="1.0.0"
)


class VoiceQueryRequest(BaseModel):
    text: str


@app.get("/")
def root():
    return {
        "message": "AI Engineer Assessment API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/health/database")
def database_health(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar()
    }

@app.post("/api/knowledge")
def create_knowledge(
    document: KnowledgeDocumentCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(KnowledgeDocument).filter(
        KnowledgeDocument.record_id == document.record_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=409,
            detail="record_id already exists"
        )

    knowledge = KnowledgeDocument(
        record_id=document.record_id,
        title=document.title,
        content=document.content,
        category=document.category,
        source=document.source,
        source_url=document.source_url,
        version=document.version,
        language=document.language,
        contains_pii=document.contains_pii
    )

    db.add(knowledge)
    db.commit()
    db.refresh(knowledge)

    return {
        "message": "Knowledge document created",
        "record_id": knowledge.record_id,
        "title": knowledge.title
    }

@app.get("/api/knowledge")
def get_knowledge(db: Session = Depends(get_db)):
    documents = (
        db.query(KnowledgeDocument)
        .order_by(KnowledgeDocument.created_at.desc())
        .all()
    )

    return [
        {
            "record_id": document.record_id,
            "title": document.title,
            "content": document.content,
            "category": document.category,
            "source": document.source,
            "source_url": document.source_url,
            "version": document.version,
            "language": document.language,
            "contains_pii": document.contains_pii,
            "created_at": document.created_at,
            "updated_at": document.updated_at,
        }
        for document in documents
    ]

@app.get("/api/knowledge/{record_id}")
def get_knowledge_by_id(
    record_id: str,
    db: Session = Depends(get_db)
):
    document = (
        db.query(KnowledgeDocument)
        .filter(KnowledgeDocument.record_id == record_id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Knowledge document not found"
        )

    return {
        "record_id": document.record_id,
        "title": document.title,
        "content": document.content,
        "category": document.category,
        "source": document.source,
        "source_url": document.source_url,
        "version": document.version,
        "language": document.language,
        "contains_pii": document.contains_pii,
        "created_at": document.created_at,
        "updated_at": document.updated_at,
    }

@app.post("/api/search")
def search_knowledge(
    request: KnowledgeSearchRequest,
    db: Session = Depends(get_db)
):
    results = retrieve_similar_chunks(
        db=db,
        query=request.query,
        top_k=request.top_k
    )

    return [
    {
        "chunk_id": str(row.id),
        "document_id": str(row.document_id),
        "record_id": row.record_id,
        "title": row.title,
        "category": row.category,
        "chunk_index": row.chunk_index,
        "content": row.content,
        "page_number": row.page_number,
        "section_title": row.section_title,
        "distance": row.distance
    }
    for row in results
]

@app.post("/api/voice/chat")
def voice_chat(request: VoiceQueryRequest):

    result = process_voice_query(request.text)

    return {
        "user_text": request.text,
        "answer": result["answer"],
        "escalate": result["escalate"]
    }