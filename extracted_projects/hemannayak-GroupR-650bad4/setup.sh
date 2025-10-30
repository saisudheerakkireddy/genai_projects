#!/bin/bash

echo "🚀 Setting up DisasterLens AI..."

# Create necessary directories
mkdir -p data/raw
mkdir -p data/chromadb

# Check if initialization is needed
if [ ! -d data/chromadb/chroma.sqlite3 ]; then
    echo "⚙️ Initializing system..."
    python scripts/initialize_system.py
else
    echo "✅ System already initialized"
fi

# Generate initial data if needed
if [ ! -f data/raw/disaster_tweets.csv ]; then
    echo "📊 Generating initial data..."
    python scripts/enhanced_sample.py
fi

# Generate simulated live data
echo "🔄 Generating simulated live data..."
python scripts/generate_live_tweets.py -a

echo "✅ Setup complete!"
