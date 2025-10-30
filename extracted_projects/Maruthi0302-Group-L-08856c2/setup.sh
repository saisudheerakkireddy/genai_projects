#!/bin/bash

# This script automates the setup process for the Telecom AI Agent project.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "--- Starting Project Setup ---"

# 1. Create a virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
else
    echo "Virtual environment already exists."
fi

# 2. Activate the virtual environment
# Note: Activation is for the current script session. You need to activate it manually in your shell.
# On Linux/macOS: source venv/bin/activate
# On Windows: .\venv\Scripts\activate
source venv/bin/activate
echo "Virtual environment activated for this script session."

# 3. Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# 4. Create necessary directories
echo "Creating data, database, and logs directories..."
mkdir -p data/raw/telecom
mkdir -p data/raw/support
mkdir -p database/chroma_db
mkdir -p logs

# 5. Copy .env.example to .env
if [ ! -f ".env" ]; then
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo "IMPORTANT: Please fill in your API keys and credentials in the .env file."
else
    echo ".env file already exists. Skipping copy."
fi

echo "--- Setup Complete! ---"
echo "
Next Steps:
1.  Activate the virtual environment in your terminal:
    - On Linux/macOS: source venv/bin/activate
    - On Windows: .\venv\Scripts\activate
2.  Add your API keys to the .env file.
3.  Run the data download script: python 1_download_data.py
4.  Build the RAG vector store: python 2_build_rag.py
5.  Start the API server: uvicorn 4_api:app --reload
6.  Run the tests in a separate terminal: python 5_test.py
"
