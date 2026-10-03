from app.services.rag_chain import answer_question


def process_voice_query(user_text: str) -> dict:

    user_text = user_text.strip()

    if not user_text:
        return {
            "answer": "I didn't hear anything. Could you please repeat that?",
            "escalate": False
        }

    escalation_words = [
        "human",
        "agent",
        "representative",
        "talk to someone",
        "customer service",
        "support agent"
    ]

    lower_text = user_text.lower()

    if any(word in lower_text for word in escalation_words):
        return {
            "answer": (
                "Sure. I can connect you with a human representative "
                "for further assistance."
            ),
            "escalate": True
        }

    answer = answer_question(user_text)

    return {
        "answer": answer,
        "escalate": False
    }