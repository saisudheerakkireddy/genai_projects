"""Builds the RAG vector store from the raw data."""
import os
import pandas as pd
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from config.settings import settings
from src.utils.logger import setup_logger

logger = setup_logger()

def load_documents_from_csv(file_path: str, text_column: str, metadata_columns: list) -> list[Document]:
    """Loads documents from a CSV file."""
    logger.info(f"Loading data from {file_path}")
    df = pd.read_csv(file_path)
    documents = []
    for _, row in df.iterrows():
        content = row[text_column]
        metadata = {col: row[col] for col in metadata_columns}
        metadata["source"] = os.path.basename(file_path)
        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)
    logger.info(f"Loaded {len(documents)} documents.")
    return documents

def main():
    """Builds and persists the ChromaDB vector store."""
    logger.info("Starting RAG build process...")

    # Define data paths
    telecom_path = os.path.join(settings.RAW_DATA_DIR, "telecom", "CustomerInteractionData.csv")
    support_path = os.path.join(settings.RAW_DATA_DIR, "support", "customer_support_tickets.csv")

    # Load documents
    telecom_docs = load_documents_from_csv(
        telecom_path,
        text_column="CustomerInteractionRawText",
        metadata_columns=["RecordID", "AgentAssignedTopic"]
    )
    support_docs = load_documents_from_csv(
        support_path,
        text_column="Ticket Description",
        metadata_columns=["Ticket ID", "Ticket Type", "Ticket Subject"]
    )
    all_docs = telecom_docs + support_docs

    # Split documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.CHUNK_SIZE,
        chunk_overlap=settings.CHUNK_OVERLAP
    )
    splits = text_splitter.split_documents(all_docs)
    logger.info(f"Split documents into {len(splits)} chunks.")

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)

    # Build ChromaDB
    logger.info("Building ChromaDB vector store...")
    vectorstore = Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=settings.CHROMA_DB_PATH
    )
    logger.info(f"Vector store created with {vectorstore._collection.count()} vectors.")
    logger.info(f"Persisting vector store to {settings.CHROMA_DB_PATH}")
    vectorstore.persist()
    logger.info("RAG build process completed successfully.")

if __name__ == "__main__":
    main()
