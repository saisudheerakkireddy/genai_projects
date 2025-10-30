#!/bin/bash
# CrisisLens AI - Quick Start Script

echo "🚀 Starting CrisisLens AI..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please create .env with your HF_TOKEN"
    exit 1
fi

echo "✅ .env file found"

# Check if data is initialized
if [ ! -d data/chromadb ]; then
    echo "⚠️  System not initialized. Running initialization..."
    python3 scripts/initialize_system.py
    if [ $? -ne 0 ]; then
        echo "❌ Initialization failed"
        exit 1
    fi
else
    echo "✅ System already initialized (found data/chromadb)"
fi

echo ""
echo "🎯 Starting backend and frontend..."
echo ""
echo "Backend will start at: http://localhost:8000"
echo "Frontend will start at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Start backend in background
echo "Starting backend..."
uvicorn backend.main_simple:app --reload --port 8000 &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start frontend
echo "Starting frontend..."
streamlit run frontend/app_enhanced.py &
FRONTEND_PID=$!

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
