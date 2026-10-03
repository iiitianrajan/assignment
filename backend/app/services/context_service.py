def build_context(results):
    context_parts = []

    for result in results:
        context_parts.append(
            f"""Source: {result['title']}
Record ID: {result['record_id']}
Chunk: {result['chunk_index']}

Content:
{result['content']}
"""
        )

    return "\n---\n".join(context_parts)