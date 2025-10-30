"""Load environment variables and provide configuration settings."""
import os
from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Configuration settings for the application."""
    # API Keys
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    KAGGLE_USERNAME: str = os.getenv("KAGGLE_USERNAME", "")
    KAGGLE_KEY: str = os.getenv("KAGGLE_KEY", "")

    # Paths
    CHROMA_DB_PATH: str = os.getenv("CHROMA_DB_PATH", "database/chroma_db")
    RAW_DATA_DIR: str = os.getenv("RAW_DATA_DIR", "data/raw")
    LOGS_DIR: str = os.getenv("LOGS_DIR", "logs")

    # Model Names
    LLM_MODEL_NAME: str = os.getenv("LLM_MODEL_NAME", "llama-3.3-70b-versatile")
    EMBEDDING_MODEL_NAME: str = os.getenv("EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2")

    # RAG Parameters
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", 500))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", 50))
    VECTOR_COUNT: int = int(os.getenv("VECTOR_COUNT", 3))

# Instantiate settings
settings = Settings()

# Validate that essential settings are configured
if not settings.GROQ_API_KEY:
    logger.error("GROQ_API_KEY is not set in the environment variables.")
    raise ValueError("GROQ_API_KEY is not set.")

if not (settings.KAGGLE_USERNAME and settings.KAGGLE_KEY):
    logger.warning("Kaggle credentials are not set. Data download will fail.")
