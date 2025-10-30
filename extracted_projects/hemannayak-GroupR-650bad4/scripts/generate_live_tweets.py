#!/usr/bin/env python3

import pandas as pd
import random
import os
from datetime import datetime, timedelta
import argparse

def generate_simulated_live_tweets(location="Hyderabad", count=30, days_back=1):
    """Generate simulated 'live' tweets for demo purposes when real API access fails"""
    
    print(f"🔄 Generating {count} simulated live tweets for {location}...")
    
    # Templates for realistic disaster tweets
    tweet_templates = [
        "BREAKING: {disaster} reported in {area} area of {location}! {impact}. #DisasterAlert",
        "URGENT: {disaster} situation in {location}! {impact}. Authorities responding. #Emergency",
        "🚨 {location} {disaster} update: {impact}. Stay safe! #DisasterResponse",
        "Alert: {disaster} in {location} {area}. {impact}. Follow official channels for updates.",
        "{location} residents report {disaster} in {area}. {impact}. Emergency services on scene.",
        "Just in: {disaster} affecting {location} {area}. {impact}. #BreakingNews",
        "LIVE: {disaster} situation developing in {location}. {impact}. Updates to follow.",
        "⚠️ {location} {disaster} alert: {impact}. Authorities advise {advice}.",
        "{disaster} in {location} {area} - {impact}. Please {advice} if in affected area.",
        "Confirmed reports of {disaster} in {location}. {impact}. Emergency response underway."
    ]
    
    # Disaster types with impacts and advice
    disasters = {
        "flood": {
            "name": ["flooding", "flash floods", "severe waterlogging", "overflowing drains", "water inundation"],
            "areas": ["low-lying", "riverside", "downtown", "old city", "market", "residential"],
            "impacts": [
                "roads submerged", 
                "vehicles stranded", 
                "homes evacuated",
                "traffic at standstill",
                "public transport suspended",
                "schools closed",
                "power outages reported",
                "rescue operations underway"
            ],
            "advice": [
                "avoid travel", 
                "move to higher ground", 
                "follow evacuation orders",
                "stay indoors"
            ],
            "severity": ["HIGH", "CRITICAL", "MEDIUM", "HIGH", "CRITICAL"]
        },
        "fire": {
            "name": ["fire", "major blaze", "building fire", "industrial fire", "fire outbreak"],
            "areas": ["commercial", "industrial", "residential", "shopping", "market", "historic"],
            "impacts": [
                "multiple buildings affected", 
                "thick smoke visible for miles", 
                "firefighters on scene",
                "nearby buildings evacuated",
                "casualties reported",
                "traffic diverted",
                "air quality deteriorating"
            ],
            "advice": [
                "avoid the area", 
                "keep windows closed", 
                "follow official instructions",
                "check on vulnerable neighbors"
            ],
            "severity": ["CRITICAL", "HIGH", "CRITICAL", "HIGH", "MEDIUM"]
        },
        "earthquake": {
            "name": ["earthquake", "tremors", "seismic activity", "quake", "earth tremors"],
            "areas": ["northern", "central", "entire", "southern", "eastern", "western"],
            "impacts": [
                "buildings shaking", 
                "people rushing outdoors", 
                "minor damage reported",
                "some structures affected",
                "power outages in parts",
                "communication networks congested",
                "aftershocks expected"
            ],
            "advice": [
                "stay away from damaged buildings", 
                "be prepared for aftershocks", 
                "check for gas leaks",
                "follow drop-cover-hold protocol"
            ],
            "severity": ["MEDIUM", "HIGH", "MEDIUM", "LOW", "HIGH"]
        },
        "storm": {
            "name": ["storm", "heavy rainfall", "thunderstorm", "wind damage", "cyclonic conditions"],
            "areas": ["northern", "entire", "coastal", "southern", "central", "outlying"],
            "impacts": [
                "trees uprooted", 
                "power lines down", 
                "flights delayed",
                "roofs damaged",
                "roads blocked",
                "public events canceled",
                "visibility severely reduced"
            ],
            "advice": [
                "stay indoors", 
                "secure loose objects", 
                "avoid travel if possible",
                "park vehicles in safe locations"
            ],
            "severity": ["HIGH", "MEDIUM", "HIGH", "MEDIUM", "LOW"]
        },
        "landslide": {
            "name": ["landslide", "mudslide", "land subsidence", "hillside collapse", "road collapse"],
            "areas": ["hilly", "mountainous", "highway", "construction", "outskirts", "rural"],
            "impacts": [
                "road blocked", 
                "vehicles trapped", 
                "traffic diverted",
                "houses damaged",
                "rescue teams deployed",
                "people missing",
                "communication lines affected"
            ],
            "advice": [
                "use alternative routes", 
                "follow official diversions", 
                "report any cracks in structures",
                "evacuate if in danger zone"
            ],
            "severity": ["HIGH", "CRITICAL", "MEDIUM", "HIGH", "MEDIUM"]
        }
    }
    
    # City-specific areas
    city_areas = {
        "Hyderabad": ["Gachibowli", "Hitech City", "Banjara Hills", "Secunderabad", "Charminar", "Jubilee Hills", "Kukatpally", "Madhapur", "Ameerpet", "Begumpet"],
        "Mumbai": ["Andheri", "Bandra", "Colaba", "Dadar", "Juhu", "Worli", "Marine Drive", "Powai", "Malad", "Goregaon"],
        "Delhi": ["Connaught Place", "Chandni Chowk", "Hauz Khas", "Dwarka", "Saket", "Lajpat Nagar", "Karol Bagh", "Rohini", "Vasant Kunj", "Janakpuri"],
        "Bangalore": ["Koramangala", "Indiranagar", "Whitefield", "MG Road", "Jayanagar", "Electronic City", "HSR Layout", "Malleshwaram", "BTM Layout", "Hebbal"],
        "Chennai": ["T Nagar", "Adyar", "Anna Nagar", "Mylapore", "Velachery", "Besant Nagar", "Porur", "Nungambakkam", "Tambaram", "Guindy"],
        "Kolkata": ["Park Street", "Salt Lake", "Howrah", "New Town", "Ballygunge", "Alipore", "Behala", "Dum Dum", "Gariahat", "Jadavpur"]
    }
    
    # Default to Hyderabad areas if location not in our list
    areas = city_areas.get(location, city_areas["Hyderabad"])
    
    # Generate tweets
    tweets = []
    
    for i in range(count):
        # Pick a random disaster type
        disaster_type = random.choice(list(disasters.keys()))
        disaster_info = disasters[disaster_type]
        
        # Create tweet with random variations
        disaster_name = random.choice(disaster_info["name"])
        area = random.choice(disaster_info["areas"]) + " " + random.choice(areas)
        impact = random.choice(disaster_info["impacts"])
        advice = random.choice(disaster_info["advice"])
        severity = random.choice(disaster_info["severity"])
        
        # Generate a random timestamp within the specified days
        hours_back = random.randint(0, days_back * 24)
        timestamp = datetime.now() - timedelta(hours=hours_back)
        
        # Format the tweet
        template = random.choice(tweet_templates)
        text = template.format(
            disaster=disaster_name,
            location=location,
            area=area,
            impact=impact,
            advice=advice
        )
        
        # Create tweet object
        tweet = {
            "id": f"live_sim_{i}_{int(timestamp.timestamp())}",
            "keyword": disaster_type,
            "location": location,
            "text": text,
            "target": 1,
            "severity": severity,
            "timestamp": timestamp.isoformat(),
            "source": "simulated_live"
        }
        
        tweets.append(tweet)
    
    return tweets

def save_tweets(tweets, output_path="data/raw/live_tweets.csv"):
    """Save the generated tweets to CSV"""
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Convert to DataFrame and save
    df = pd.DataFrame(tweets)
    df.to_csv(output_path, index=False)
    print(f"✅ Saved {len(df)} simulated live tweets to {output_path}")
    return df

def append_to_main_dataset(live_df, main_path="data/raw/disaster_tweets.csv"):
    """Append the simulated live tweets to the main dataset"""
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

def main():
    """Main function"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Generate simulated live disaster tweets")
    parser.add_argument("-l", "--location", type=str, default="Hyderabad", help="Location for tweets (default: Hyderabad)")
    parser.add_argument("-n", "--num", type=int, default=30, help="Number of tweets to generate (default: 30)")
    parser.add_argument("-d", "--days", type=int, default=1, help="Number of days to simulate (default: 1)")
    parser.add_argument("-o", "--output", type=str, default="data/raw/live_tweets.csv", help="Output file path")
    parser.add_argument("-a", "--append", action="store_true", help="Append to main dataset")
    parser.add_argument("-m", "--main", type=str, default="data/raw/disaster_tweets.csv", help="Main dataset path")
    
    args = parser.parse_args()
    
    print("🚨 CrisisLens AI - Simulated Live Tweet Generator")
    print("==================================================")
    
    # Generate tweets
    tweets = generate_simulated_live_tweets(args.location, args.num, args.days)
    
    # Save to file
    live_df = save_tweets(tweets, args.output)
    
    # Append to main dataset if requested
    if args.append:
        print("🔄 Appending to main dataset...")
        append_to_main_dataset(live_df, args.main)
    
    # Print statistics
    print("\n🎯 Tweet Keywords Distribution:")
    print(live_df['keyword'].value_counts())
    
    print("\n⚠️ Severity Distribution:")
    print(live_df['severity'].value_counts())
    
    print("\n✅ All operations completed successfully!")
    print("Run your application to see the simulated live data in action.")

if __name__ == "__main__":
    main()
