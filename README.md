# AI Engineer Assessment

A FastAPI-based AI knowledge retrieval and question-answering system using PostgreSQL, pgvector, Hugging Face embeddings, LangChain, and an LLM.

## Overview

The application implements a Retrieval-Augmented Generation (RAG) workflow:

```text
User Question
      |
      v
FastAPI API
      |
      v
Query Embedding
      |
      v
PostgreSQL + pgvector
      |
      v
Top-K Relevant Chunks
      |
      v
Context Construction
      |
      v
LLM
      |
      v
Context-Aware Answer
```

The system retrieves relevant information from the knowledge base before generating an answer. If the required information is not available, the system responds:

```text
I don't have enough information in the provided knowledge base.
```

## Features

- Knowledge document creation and retrieval
- Semantic/vector similarity search
- PostgreSQL database integration
- pgvector-based retrieval
- Hugging Face embeddings
- LangChain retriever
- RAG question answering
- LLM integration
- Voice/chat query endpoint
- FastAPI REST APIs
- Swagger/OpenAPI documentation
- Basic API and database health checks

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| PostgreSQL | Database |
| pgvector | Vector similarity search |
| SQLAlchemy | Database access/ORM |
| LangChain | Retrieval pipeline |
| Hugging Face | Embeddings |
| Gemini / LLM | Answer generation |
| Pydantic | Data validation |

## Project Structure

```text
ai-engineer-assessment/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   │
│   │   └── services/
│   │       ├── embedding_service.py
│   │       ├── langchain_retriever.py
│   │       ├── llm_service.py
│   │       ├── prompt_service.py
│   │       ├── rag_chain.py
│   │       ├── retrieval_service.py
│   │       └── voice_service.py
│   │
│   ├── migrations/
│   ├── requirements.txt
│   └── .env
│
└── README.md
```

> The exact files/folders may vary depending on the final submitted codebase.

## Prerequisites

- Python 3.10+
- PostgreSQL
- PostgreSQL `pgvector` extension
- Required API credentials

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd ai-engineer-assessment
cd backend
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file inside the `backend` directory.

Example:

```env
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/<database_name>
GEMINI_API_KEY=<your_gemini_api_key>
HF_TOKEN=<your_huggingface_token>
```

Replace the placeholder values with your local credentials.

**Do not commit `.env` or API keys to Git.**

Recommended `.gitignore` entries:

```gitignore
.env
.venv/
__pycache__/
*.pyc
```

## Database Setup

The application uses PostgreSQL with vector similarity search.

Make sure PostgreSQL is running and the required database exists.

Enable pgvector:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Run the database migrations/setup included in the project before starting the application.

## Run the Application

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

OpenAPI specification:

```text
http://127.0.0.1:8000/openapi.json
```

## API Endpoints

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

### Database Health Check

```http
GET /health/database
```

This verifies database connectivity.

### Create Knowledge Document

```http
POST /api/knowledge
```

Example request:

```json
{
  "record_id": "DOC-001",
  "title": "Introduction to AI",
  "content": "Artificial intelligence is the simulation of human intelligence by machines.",
  "category": "AI",
  "source": "Knowledge Base",
  "source_url": null,
  "version": "1.0",
  "language": "en",
  "contains_pii": false
}
```

### Get Knowledge Documents

```http
GET /api/knowledge
```

Returns the stored knowledge documents.

### Get Knowledge Document

```http
GET /api/knowledge/{record_id}
```

Example:

```text
GET /api/knowledge/DOC-001
```

### Semantic Search

```http
POST /api/search
```

Example request:

```json
{
  "query": "What is deep learning used for?",
  "top_k": 3
}
```

The search returns the most relevant knowledge chunks and associated metadata.

### Voice / Chat

```http
POST /api/voice/chat
```

This endpoint processes a user query through the RAG/LLM pipeline.

## RAG Workflow

The RAG implementation follows these steps:

1. Receive the user question.
2. Generate an embedding for the question.
3. Perform vector similarity search in PostgreSQL.
4. Retrieve the top-K relevant chunks.
5. Construct a context from the retrieved chunks.
6. Build a grounded prompt.
7. Send the prompt to the LLM.
8. Return the generated answer.

The prompt instructs the model to use only the retrieved context and avoid unsupported information.

## Example

Question:

```text
What is deep learning used for?
```

Retrieved knowledge may contain:

```text
Deep learning is a specialized area of machine learning that
uses neural networks with multiple layers. Deep learning is
commonly used for computer vision.
```

The system can then answer:

```text
Based on the provided context, deep learning is commonly used
for computer vision.
```

For a question outside the available knowledge base, such as:

```text
What is quantum computing?
```

the expected behavior is:

```text
I don't have enough information in the provided knowledge base.
```

## Testing

LLM test:

```bash
python app/test_llm.py
```

RAG test:

```bash
python app/test_rag_chain.py
```

API testing can also be performed through:

```text
http://127.0.0.1:8000/docs
```

## Verification

The implemented API was verified with successful HTTP responses for:

```text
GET  /health
GET  /health/database
POST /api/search
POST /api/voice/chat
GET  /docs
GET  /openapi.json
```

Successful requests returned HTTP `200 OK`.

## Notes

### Hugging Face Warning

When a Hugging Face token is not configured, the application may display:

```text
Warning: You are sending unauthenticated requests to the HF Hub.
```

This is an authentication/rate-limit warning and does not by itself indicate an application failure.

### Gemini AFC Warning

The Gemini SDK may display a warning recommending use of automatic function calling through the chat interface rather than direct `generate_content` usage.

If the API request still returns `200 OK`, this warning does not indicate that the current request failed.

## Security

Do not include the following in the submitted codebase:

```text
.env
.venv/
__pycache__/
*.pyc
```

Never expose:

- API keys
- Database passwords
- Access tokens
- Other private credentials

## Submission Checklist

Before submitting:

- [ ] Application starts successfully
- [ ] PostgreSQL connection works
- [ ] `/health` returns `200 OK`
- [ ] `/health/database` returns `200 OK`
- [ ] `/api/search` returns search results
- [ ] RAG question answering works
- [ ] `/api/voice/chat` returns `200 OK`
- [ ] `/docs` opens successfully
- [ ] `requirements.txt` is included
- [ ] `README.md` is included
- [ ] `.env` is excluded
- [ ] `.venv` is excluded
- [ ] `__pycache__` is excluded
- [ ] No API keys or passwords are included

## Author

**Rajan Kumar**

B.Tech Computer Science Engineering
