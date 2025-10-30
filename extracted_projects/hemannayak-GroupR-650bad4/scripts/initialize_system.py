import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from backend.utils.data_loader import load_disaster_tweets
from backend.processing.extractor import DisasterInfoExtractor
from backend.rag.vector_store import DisasterVectorStore
from backend.models import DisasterEvent, DisasterType, Severity
from backend.utils.geocoder import LocationGeocoder
from datetime import datetime
import random

def convert_tweet_to_event(tweet, extracted_info, geocoder) -> DisasterEvent:
    """Convert DisasterTweet to DisasterEvent"""
    
    # Geocode location
    coords = None
    if tweet.location:
        coords = geocoder.geocode(tweet.location)
    
    # Default to Mumbai with random offset if no coords
    if not coords:
        coords = (
            19.0760 + random.uniform(-0.05, 0.05),
            72.8777 + random.uniform(-0.05, 0.05)
        )
    
    return DisasterEvent(
        id=tweet.id,
        text=tweet.text,
        timestamp=tweet.timestamp or datetime.now(),
        location=tweet.location or "Unknown",
        coordinates=coords,
        disaster_type=extracted_info.disaster_type,
        severity=extracted_info.severity,
        confidence=extracted_info.confidence,
        source="twitter",
        needs=extracted_info.needs,
        is_verified=False
    )

def main():
    print("🚀 Initializing CrisisLens System...")
    
    # Load data
    print("\n📊 Loading disaster tweets...")
    tweets = load_disaster_tweets('data/raw/disaster_tweets.csv')
    print(f"✅ Loaded {len(tweets)} tweets")
    
    # Filter only disaster tweets (target=1)
    disaster_tweets = [t for t in tweets if t.is_real_disaster]
    print(f"✅ Found {len(disaster_tweets)} disaster tweets")
    
    # Limit to first 100 for speed
    disaster_tweets = disaster_tweets[:100]
    
    # Initialize components
    print("\n🔧 Initializing components...")
    extractor = DisasterInfoExtractor()
    geocoder = LocationGeocoder()
    vector_store = DisasterVectorStore('data/chromadb')
    
    # Process tweets
    print("\n⚙️ Processing tweets...")
    events = []
    for i, tweet in enumerate(disaster_tweets):
        if i % 10 == 0:
            print(f"  Processed {i}/{len(disaster_tweets)}...")
        
        try:
            # Extract info
            extracted = extractor.extract(tweet.text)
            
            # Convert to event
            event = convert_tweet_to_event(tweet, extracted, geocoder)
            events.append(event)
            
        except Exception as e:
            print(f"  ⚠️ Error processing tweet {tweet.id}: {e}")
            continue
    
    print(f"✅ Processed {len(events)} events")
    
    # Add to vector store
    print("\n💾 Adding to vector database...")
    vector_store.add_events(events)
    
    # Get stats
    stats = vector_store.get_stats()
    print(f"\n📊 Vector Store Stats:")
    print(f"  Total documents: {stats.get('total_documents', 0)}")
    
    # Test query
    print("\n🔍 Testing query...")
    results = vector_store.query("earthquake emergency", k=3)
    print(f"  Found {len(results)} results")
    if results:
        print(f"  Sample: {results[0].text[:100]}...")
    
    print("\n✅ System initialized successfully!")
    print(f"\n📈 Summary:")
    print(f"  - Loaded: {len(tweets)} tweets")
    print(f"  - Processed: {len(events)} events")
    print(f"  - Indexed: {stats.get('total_documents', 0)} documents")
    print(f"  - Ready for queries!")

if __name__ == "__main__":
    main()
