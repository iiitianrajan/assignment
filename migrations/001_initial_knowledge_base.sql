CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE knowledge_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    record_id VARCHAR(100) UNIQUE NOT NULL,

    title VARCHAR(255) NOT NULL,

    content TEXT NOT NULL,

    category VARCHAR(100),

    source VARCHAR(255),

    source_url TEXT,

    version VARCHAR(50),

    language VARCHAR(50) DEFAULT 'en',

    contains_pii BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    updated_at TIMESTAMPTZ DEFAULT NOW()
);