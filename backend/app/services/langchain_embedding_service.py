from langchain_huggingface import HuggingFaceEmbeddings


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def generate_embedding(text: str) -> list[float]:
    return embeddings.embed_query(text)


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    return embeddings.embed_documents(texts)