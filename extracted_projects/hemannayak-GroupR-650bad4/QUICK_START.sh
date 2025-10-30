#!/bin/bash
# Quick Start Script for DisasterLens AI

echo "🚀 DisasterLens AI - Quick Start"
echo "================================"
echo ""

# Check if data exists
if [ ! -f "data/raw/disaster_tweets.csv" ]; then
    echo "📊 Generating sample data..."
    python3 scripts/quick_sample.py
    echo ""
fi

echo "✅ Data ready!"
echo ""
echo "🎯 Starting services..."
echo ""
echo "Backend will start at: http://localhost:8000"
echo "Frontend will start at: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Start backend in background
echo "Starting backend..."
cd backend
python3 main_simple.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting frontend..."
cd frontend
streamlit run app_simple.py &
FRONTEND_PID=$!
cd ..

# Wait for user to stop
echo ""
echo "✅ Both services started!"
echo "   Backend PID: $BACKEND_PID"
echo "   Frontend PID: $FRONTEND_PID"
echo ""
echo "Open your browser to: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop..."

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
