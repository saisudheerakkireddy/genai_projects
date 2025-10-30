# Problem statement
In many organisations, handling customer support tickets is a resource‑intensive task: manual categorisation, routing, response generation and feedback collection all require human intervention. This leads to slower resolution times, inconsistent responses, and high operational costs.  
Our goal is to build an *AI-powered customer service agent* that can:  
- Automatically ingest support ticket text (voice or text) and understand the customer issue.  
- Retrieve the most relevant past tickets or knowledge documents to ground its response.  
- Generate a context-aware, professional answer to the customer query, and optionally escalate complex cases.  
- Provide insights on customer sentiment, common issues, and resolution efficiency.

# Telecom AI Agent with Multi-Agent Architecture

This project is a complete multi-agent RAG (Retrieval-Augmented Generation) system designed for a 24-hour hackathon. It provides a REST API for interacting with a telecom AI that can handle support queries and automate tasks.

## Project Overview

The system features a triage agent that routes user queries to one of two specialized agents:

1.  **Business Service Agent**: A RAG-based agent that answers telecom support questions using a knowledge base built from Kaggle datasets. It can cite sources and detect when a conversation needs to be escalated to a human.
2.  **Task Automation Agent**: A conversational agent that assists users with tasks, such as booking a flight, by collecting necessary information.

# Telecom AI Business Service Agent with RAG

Complete RAG system for telecom customer support using Groq LLM + ChromaDB.

## Setup
1. Copy `.env.example` to `.env` and add your API keys
2. `pip install -r requirements.txt`
3. `python download_data.py`
4. `python build_rag.py`
5. `uvicorn api:app --reload`

See `BUSINESS_AGENT_COMPLETE.md` for full documentation.

## Architecture

The architecture uses a pipeline of agents, orchestrated by a main controller. All components are built with a free and open-source tech stack.

```
      +--------------------+
      |       User         |
      +--------------------+
              |
              v
      +--------------------+
      |   FastAPI Server   |
      |      (/chat)       |
      +--------------------+
              |
              v
      +--------------------+
      |  TelecomAIAgent    |
      |   (Orchestrator)   |
      +--------------------+
              |
              v
      +--------------------+
      |   Triage Agent     |
      | (Intent Classifier)|
      +--------------------+
              |
+-----------------------------+-----------------------------+
| (telecom_support)           | (task_automation)           | (general)
|                             |                             | 
v                             v                             v
+-----------------+     +-----------------+     +-----------------+
| Business Agent  |     |  Task Agent     |     |      LLM        |
| (RAG)           |     | (Info Collector)|
+-----------------+     +-----------------+     +-----------------+
        |
        v
+-----------------+
|    ChromaDB     |
| (Vector Store)  |
+-----------------+
```

## Tech Stack

-   **LLM**: Groq API (`llama-3.2-90b-text-preview`)
-   **Vector DB**: ChromaDB
-   **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
-   **Framework**: LangChain, LangGraph, FastAPI
-   **Data**: Kaggle datasets

## Setup Instructions

**Prerequisites**: Python 3.10+, `pip`, and `venv`.

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Run the setup script**:
    This script will create a virtual environment, install dependencies, create directories, and set up the `.env` file.
    ```bash
    # On Linux/macOS
    chmod +x setup.sh
    ./setup.sh

    # On Windows (using Git Bash or WSL)
    ./setup.sh
    ```

3.  **Activate the virtual environment**:
    ```bash
    # On Linux/macOS
    source venv/bin/activate

    # On Windows
    .\venv\Scripts\activate
    ```

4.  **Configure Environment Variables**:
    Open the `.env` file and add your API keys for Groq and Kaggle.
    ```
    GROQ_API_KEY="YOUR_GROQ_API_KEY"
    KAGGLE_USERNAME="YOUR_KAGGLE_USERNAME"
    KAGGLE_KEY="YOUR_KAGGLE_KEY"
    ```

5.  **Download Data**:
    Run the script to download the datasets from Kaggle.
    ```bash
    python 1_download_data.py
    ```

6.  **Build the RAG Vector Store**:
    Process the raw data and build the ChromaDB vector store.
    ```bash
    python 2_build_rag.py
    ```

7.  **Start the API Server**:
    Launch the FastAPI server with Uvicorn.
    ```bash
    uvicorn 4_api:app --reload
    ```
    The API will be available at `http://127.0.0.1:8000`.

## API Usage

You can interact with the API using any HTTP client, such as `curl` or Postman.

### Health Check

```bash
curl -X GET http://127.0.0.1:8000/
```

### Chat Endpoint

**Request (Telecom Support)**:
```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{
  "user_input": "Why is my internet so slow?",
  "conversation_history": []
}'
```

**Request (Task Automation)**:
```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{
  "user_input": "I want to book a flight",
  "conversation_history": []
}'
```

### Testing

After starting the API server, open a new terminal, activate the virtual environment, and run the test script:

```bash
python 5_test.py
```

## Hackathon Timeline Suggestions

-   **Hours 1-2**: Setup, data download, and environment configuration.
-   **Hours 3-6**: Build the RAG pipeline (`2_build_rag.py`). Experiment with chunking and embeddings.
-   **Hours 7-12**: Develop the core agents (`triage`, `business`, `task`). Focus on prompt engineering.
-   **Hours 13-16**: Build the orchestrator (`3_agent.py`) and the FastAPI server (`4_api.py`).
-   **Hours 17-20**: Write tests (`5_test.py`) and debug the end-to-end flow.
-   **Hours 21-24**: Refine the README, prepare the presentation, and add any last-minute polish.

## Troubleshooting

-   **Kaggle Download Issues**: Ensure your `KAGGLE_USERNAME` and `KAGGLE_KEY` in `.env` are correct. You can also place a `kaggle.json` file in `~/.kaggle/`.
-   **`ModuleNotFoundError`**: Make sure you have activated the virtual environment (`source venv/bin/activate`) before running any Python scripts.
-   **Vector Store Errors**: If you have issues with ChromaDB, try deleting the `database/chroma_db` directory and re-running `2_build_rag.py`.
