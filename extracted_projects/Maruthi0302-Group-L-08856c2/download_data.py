"""This script downloads the required Kaggle datasets."""
import os
import sys

# Load environment variables BEFORE importing anything else
from dotenv import load_dotenv
load_dotenv()

from config.settings import settings
from src.utils.logger import setup_logger
from kaggle.api.kaggle_api_extended import KaggleApi

logger = setup_logger()

def download_kaggle_dataset(dataset_id: str, destination: str):
    """Downloads a dataset from Kaggle and extracts it."""
    try:
        api = KaggleApi()
        api.authenticate()
        logger.info(f"Downloading dataset: {dataset_id} to {destination}")
        api.dataset_download_files(dataset_id, path=destination, unzip=True)
        logger.info(f"Successfully downloaded and extracted {dataset_id}.")
    except Exception as e:
        logger.error(f"Failed to download dataset {dataset_id}. Error: {e}")
        logger.error("Please ensure your Kaggle API credentials (kaggle.json) are correctly set up.")
        logger.error("You can create a kaggle.json file by creating an API token in your Kaggle account settings.")
        sys.exit(1)

def main():
    """Main function to download all required datasets."""
    # Ensure data directories exist
    telecom_path = os.path.join(settings.RAW_DATA_DIR, "telecom")
    support_path = os.path.join(settings.RAW_DATA_DIR, "support")
    os.makedirs(telecom_path, exist_ok=True)
    os.makedirs(support_path, exist_ok=True)

    # Dataset IDs
    telecom_dataset = "avinashok/telecomagentcustomerinteractiontext"
    support_dataset = "suraj520/customer-support-ticket-dataset"

    # Download datasets
    logger.info("Starting data download process...")
    download_kaggle_dataset(telecom_dataset, telecom_path)
    download_kaggle_dataset(support_dataset, support_path)
    logger.info("All datasets have been downloaded.")

if __name__ == "__main__":
    # Set Kaggle credentials from environment/settings
    if not os.getenv('KAGGLE_USERNAME'):
        os.environ['KAGGLE_USERNAME'] = settings.KAGGLE_USERNAME
    if not os.getenv('KAGGLE_KEY'):
        os.environ['KAGGLE_KEY'] = settings.KAGGLE_KEY
    
    logger.info(f"Using Kaggle user: {os.getenv('KAGGLE_USERNAME')}")
    main()
