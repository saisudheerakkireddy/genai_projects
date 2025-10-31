# GenAI Hackathon 2025 - Automated Evaluation Framework

This repository contains a fully automated evaluation framework for the GenAI Hackathon 2025. It is designed to process, analyze, and score all 44 team submissions based on a comprehensive set of criteria.

## Prerequisites

Before you begin, ensure you have the following installed on your macOS device:

- **Homebrew**: [Installation Guide](https://brew.sh/)
- **Python 3.8+**: `brew install python`
- **Git**: `brew install git`
- **Docker**: [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/)
- **Gitleaks**: `brew install gitleaks`
- **Bandit**: `brew install bandit`

## Setup

1.  **Clone the Repository**
    ```bash
    git clone <your-repository-url>
    cd genai_hackathon_25
    ```

2.  **Install Dependencies**
    The start script will handle this automatically, but you can also install them manually:
    ```bash
    pip3 install -r requirements.txt
    ```

## Execution

To start the evaluation, simply run the provided start script. This will handle dependency installation and execute the main evaluation pipeline.

```bash
./start_evaluation.sh
```

The script will process all 44 repositories sequentially. Upon completion, a new `evaluation_reports` directory will be created with detailed reports, summaries, and logs.
