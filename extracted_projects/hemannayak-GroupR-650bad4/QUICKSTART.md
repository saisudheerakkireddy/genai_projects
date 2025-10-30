# 🚀 Quick Start Guide

## Step 1: Get HuggingFace Token (2 mins)

1. Go to: https://huggingface.co/settings/tokens
2. Click "New token"
3. Name: "CrisisLens"
4. Type: Read
5. Copy token: `hf_xxxxxxxxxxxxxxxxxxxxx`

## Step 2: Setup Environment (5 mins)

```bash
cd /Users/hemanth/CascadeProjects/DisasterLens

# Create .env file
cat > .env << EOF
HF_TOKEN=hf_YOUR_TOKEN_HERE
ENVIRONMENT=development
LOG_LEVEL=INFO
EOF

# Create virtual environment (if not done)
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Generate Sample Data (1 min)

```bash
# Generate sample disaster tweets
python scripts/generate_sample_data.py
```

## Step 4: Initialize System (3 mins)

```bash
# Process data and create vector database
python scripts/initialize_system.py
```

## Step 5: Run Backend (1 min)

```bash
# Start FastAPI server
uvicorn backend.main:app --reload --port 8000
```

## Step 6: Run Frontend (1 min)

Open a NEW terminal:

```bash
cd /Users/hemanth/CascadeProjects/DisasterLens
source venv/bin/activate
streamlit run frontend/app.py
```

## Step 7: Access Dashboard

Open browser: http://localhost:8501

---

## Troubleshooting

### Backend won't start
- Check .env file has HF_TOKEN
- Run: `python scripts/initialize_system.py` first

### No data showing
- Make sure you ran `python scripts/generate_sample_data.py`
- Check `data/raw/disaster_tweets.csv` exists

### Import errors
- Make sure you're in the project root directory
- Activate venv: `source venv/bin/activate`

---

## What You'll See

1. **Live Map**: Interactive map with disaster events
2. **Query Assistant**: Ask questions about disasters
3. **Agent Decisions**: AI resource allocation
4. **Situation Report**: Auto-generated reports
5. **Event Feed**: Filterable event list

---

## Demo Queries to Try

- "What are the most critical situations?"
- "Where are floods happening?"
- "Show me earthquake events"
- "What kind of help is needed?"
