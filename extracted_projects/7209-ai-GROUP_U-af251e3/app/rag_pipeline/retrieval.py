def retrieve_relevant_chunks(query: str, collection_name="default_collection"):
    """Mock retrieval function."""
    print(f"[Retrieval] Retrieving chunks for query '{query}' from collection '{collection_name}'")
    return [f"Example chunk for query '{query}'."]
