from app.services.langchain_retriever import retriever
from app.services.prompt_service import build_prompt
from app.services.llm_service import llm


def answer_question(question: str) -> str:
    # Retrieve relevant documents
    documents = retriever.invoke(question)

    # If nothing was retrieved
    if not documents:
        return "I don't have enough information in the provided knowledge base."

    # Build context from retrieved documents
    context_parts = []

    for doc in documents:
        context_parts.append(
            f"""
Source: {doc.metadata.get("title")}
Record ID: {doc.metadata.get("record_id")}

Content:
{doc.page_content}
"""
        )

    context = "\n---\n".join(context_parts)

    # Build grounded prompt
    prompt = build_prompt(
        context=context,
        question=question
    )

    # Call LLM
    response = llm.invoke(prompt)

    # Handle LangChain/Gemini response
    if hasattr(response, "content"):
        content = response.content

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    return item.get("text", "")

    return str(response)