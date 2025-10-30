#!/bin/bash

echo "🚨 CrisisLens AI - Live Data Integration"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    exit 1
fi

# Ensure we're in the project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "🔄 Activating virtual environment..."
    source venv/bin/activate
fi

# Set parameters
LOCATION="Hyderabad"
COUNT=30
DAYS=3
APPEND=true

# First try to fetch real tweets
echo ""
echo "🔍 Attempting to fetch real disaster tweets from $LOCATION..."
echo ""

# Install snscrape if not already installed
pip install snscrape

# Try to run the real fetch script
python3 scripts/fetch_live_tweets.py -l "$LOCATION" -n $COUNT -d $DAYS -a

# Check if the fetch was successful by looking for the output file
if [ -f "data/raw/live_tweets.csv" ] && [ $(wc -l < "data/raw/live_tweets.csv") -gt 1 ]; then
    echo "✅ Successfully fetched real tweets!"
else
    echo ""
    echo "⚠️ Could not fetch real tweets. Using simulated live data instead..."
    echo ""
    
    # Run the simulated data generator as fallback
    python3 scripts/generate_live_tweets.py -l "$LOCATION" -n $COUNT -d $DAYS -a
fi

echo ""
echo "✅ Done! You can now run the application to see the live data."
echo "   Run: ./START.sh"
echo ""
