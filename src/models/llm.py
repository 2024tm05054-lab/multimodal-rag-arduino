def generate_answer(query, context):
    # simple response generator
    combined_context = " ".join(context)

    return f"Answer based on document: {combined_context[:300]}"
