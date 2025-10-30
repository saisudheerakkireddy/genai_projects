def load_and_prepare_text(content: str):
    """Split text into chunks (for RAG)."""
    chunk_size = 500  # characters
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    print(f"[Preprocessing] Created {len(chunks)} chunks.")
    return chunks
