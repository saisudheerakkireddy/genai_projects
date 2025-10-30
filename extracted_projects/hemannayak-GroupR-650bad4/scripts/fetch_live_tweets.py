#!/usr/bin/env python3

import subprocess
import sys
import os
import json
import pandas as pd
import random
from datetime import datetime, timedelta
import argparse

# Check if snscrape is installed, if not install it
def check_snscrape():
    try:
        import snscrape.modules.twitter as sntwitter
        print("✅ snscrape is already installed")
        return True
    except ImportError:
        print("⚠️ snscrape not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "snscrape"])
            print("✅ snscrape installed successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to install snscrape: {e}")
            print("Please install manually: pip install snscrape")
            return False

# Function to extract disaster keyword from tweet text
def extract_keyword(text):
    keywords = {
        "flood": ["flood", "water", "submerged", "drowning", "overflow"],
        "fire": ["fire", "blaze", "burning", "flames", "smoke"],
        "earthquake": ["earthquake", "tremor", "seismic", "quake", "shaking"],
        "storm": ["storm", "cyclone", "hurricane", "winds", "tornado"],
        "landslide": ["landslide", "mudslide", "rockfall", "debris flow"]
    }
    
    text_lower = text.lower()
    for keyword, terms in keywords.items():
        for term in terms:
            if term in text_lower:
                return keyword
    return "other"

# Function to determine severity based on text content
def determine_severity(text):
    text_lower = text.lower()
    
    # Critical indicators
    critical_terms = ["urgent", "emergency", "critical", "evacuate", "death", "casualties", 
                     "trapped", "danger", "severe", "destroyed", "devastated"]
    
    # High severity indicators
    high_terms = ["warning", "alert", "heavy", "major", "significant", "damaged", 
                 "injured", "rescue", "help needed"]
    
    # Medium severity indicators
    medium_terms = ["caution", "attention", "moderate", "affected", "impact", "disruption"]
    
    # Check for critical indicators
    for term in critical_terms:
        if term in text_lower:
            return "CRITICAL"
    
    # Check for high severity indicators
    for term in high_terms:
        if term in text_lower:
            return "HIGH"
    
    # Check for medium severity indicators
    for term in medium_terms:
        if term in text_lower:
            return "MEDIUM"
    
    # Default to LOW if no indicators found
    return "LOW"

# Function to fetch tweets using snscrape
def fetch_disaster_tweets(location="Hyderabad", max_results=30, days=1):
    print(f"🔍 Searching for {location} disaster tweets from the last {days} days...")
    
    # Calculate the date for the search query
    since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    # Build search query
    query = f"(disaster OR flood OR fire OR earthquake OR storm OR emergency OR rescue OR evacuate) {location} since:{since_date}"
    print(f"🔎 Query: {query}")
    
    try:
        import snscrape.modules.twitter as sntwitter
        tweets = []
        
        # Create a generator for tweet scraping
        scraper = sntwitter.TwitterSearchScraper(query)
        
        # Fetch tweets
        print(f"⏳ Fetching up to {max_results} tweets...")
        for i, tweet in enumerate(scraper.get_items()):
            if i >= max_results:
                break
                
            # Extract the tweet data
            tweets.append({
                "id": f"live_{tweet.id}",
                "text": tweet.content,
                "raw_content": tweet.content,
                "username": tweet.user.username,
                "created_at": tweet.date,
                "url": f"https://twitter.com/{tweet.user.username}/status/{tweet.id}"
            })
            
            if (i + 1) % 10 == 0:
                print(f"  ✓ Fetched {i + 1} tweets")
        
        print(f"✅ Successfully fetched {len(tweets)} tweets")
        return tweets
    
    except Exception as e:
        print(f"❌ Error fetching tweets: {e}")
        return []

# Process tweets into the format needed for the application
def process_tweets(tweets, location="Hyderabad"):
    processed_data = []
    
    for tweet in tweets:
        # Extract keyword from tweet text
        keyword = extract_keyword(tweet["text"])
        
        # Determine severity
        severity = determine_severity(tweet["text"])
        
        # Create entry in the required format
        processed_data.append({
            "id": tweet["id"],
            "keyword": keyword,
            "location": location,
            "text": tweet["text"],
            "target": 1,  # Assuming all fetched tweets are about disasters
            "severity": severity,
            "timestamp": tweet["created_at"].isoformat(),
            "source_url": tweet.get("url", ""),
            "username": tweet.get("username", "")
        })
    
    return processed_data

# Save tweets to CSV file
def save_tweets(tweets_data, output_path="data/raw/live_tweets.csv"):
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Convert to DataFrame and save
    df = pd.DataFrame(tweets_data)
    
    # Select only columns that match the existing dataset format
    columns_to_keep = ["id", "keyword", "location", "text", "target", "severity", "timestamp"]
    df_filtered = df[[col for col in columns_to_keep if col in df.columns]]
    
    df_filtered.to_csv(output_path, index=False)
    print(f"✅ Saved {len(df_filtered)} tweets to {output_path}")
    return df_filtered

# Append live tweets to existing dataset
def append_to_main_dataset(live_df, main_path="data/raw/disaster_tweets.csv"):
    try:
        # Read existing dataset
        main_df = pd.read_csv(main_path)
        print(f"📊 Existing dataset: {len(main_df)} entries")
        
        # Combine datasets and remove duplicates
        combined = pd.concat([main_df, live_df]).drop_duplicates('id')
        
        # Save combined dataset
        combined.to_csv(main_path, index=False)
        print(f"✅ Combined dataset saved with {len(combined)} entries")
        print(f"  Added {len(combined) - len(main_df)} new entries")
        return True
    except Exception as e:
        print(f"❌ Error appending to main dataset: {e}")
        return False

# Main function
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Fetch live disaster tweets")
    parser.add_argument("-l", "--location", type=str, default="Hyderabad", help="Location to search for (default: Hyderabad)")
    parser.add_argument("-n", "--num", type=int, default=30, help="Number of tweets to fetch (default: 30)")
    parser.add_argument("-d", "--days", type=int, default=1, help="Number of days to look back (default: 1)")
    parser.add_argument("-o", "--output", type=str, default="data/raw/live_tweets.csv", help="Output file path")
    parser.add_argument("-a", "--append", action="store_true", help="Append to main dataset")
    parser.add_argument("-m", "--main", type=str, default="data/raw/disaster_tweets.csv", help="Main dataset path")
    
    args = parser.parse_args()
    
    print("🚨 CrisisLens AI - Live Tweet Fetcher")
    print("==================================================")
    
    # Check if snscrape is installed
    if not check_snscrape():
        return
    
    # Fetch tweets
    tweets = fetch_disaster_tweets(location=args.location, max_results=args.num, days=args.days)
    
    if not tweets:
        print("❌ No tweets found. Try increasing the number of days or check your internet connection.")
        return
    
    # Process tweets
    print("🔄 Processing tweets...")
    processed_tweets = process_tweets(tweets, location=args.location)
    
    # Save to separate file
    live_df = save_tweets(processed_tweets, args.output)
    
    # Append to main dataset if requested
    if args.append:
        print("🔄 Appending to main dataset...")
        append_to_main_dataset(live_df, args.main)
    
    print("\n🎯 Tweet Keywords Distribution:")
    print(live_df['keyword'].value_counts())
    
    print("\n⚠️ Severity Distribution:")
    print(live_df['severity'].value_counts())
    
    print("\n✅ All operations completed successfully!")
    print("Run your application to see the live data in action.")

if __name__ == "__main__":
    main()
