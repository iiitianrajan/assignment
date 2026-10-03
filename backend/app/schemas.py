from pydantic import BaseModel, Field


class KnowledgeDocumentCreate(BaseModel):
    record_id: str = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
    category: str | None = None
    source: str | None = None
    source_url: str | None = None
    version: str | None = None
    language: str = "en"
    contains_pii: bool = False

class KnowledgeSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=5, ge=1, le=20)