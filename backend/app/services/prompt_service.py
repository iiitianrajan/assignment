def build_prompt(context: str, question: str) -> str:
    return f"""
You are a helpful AI assistant.

Answer the user's question using ONLY the information provided
in the context below.

If the answer cannot be found in the context, say:
"I don't have enough information in the provided knowledge base."

Do not invent facts.
Do not use outside knowledge.

Context:
----------------
{context}
----------------

Question:
{question}

Answer:
"""