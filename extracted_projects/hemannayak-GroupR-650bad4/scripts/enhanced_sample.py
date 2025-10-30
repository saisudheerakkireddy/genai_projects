import pandas as pd
import random
import os
from datetime import datetime, timedelta

os.makedirs('data/raw', exist_ok=True)

# Enhanced disaster tweets with more variety and Hyderabad focus
TWEETS = [
    # Hyderabad specific (25% of data)
    ("BREAKING: Severe flooding in Hyderabad! Hussain Sagar overflowing, roads submerged!", "flood", 1, "Hyderabad", "CRITICAL"),
    ("URGENT: Major fire at industrial area in Hyderabad. Multiple buildings affected!", "fire", 1, "Hyderabad", "CRITICAL"),
    ("Hyderabad: Heavy rains causing flash floods in low-lying areas. Immediate evacuation needed!", "flood", 1, "Hyderabad", "HIGH"),
    ("Storm warning for Hyderabad! Strong winds expected, secure loose objects.", "storm", 1, "Hyderabad", "MEDIUM"),
    ("Earthquake tremors felt in Hyderabad. Magnitude 4.2, no major damage reported yet.", "earthquake", 1, "Hyderabad", "MEDIUM"),
    ("Hyderabad Metro flooded! Services suspended on multiple lines.", "flood", 1, "Hyderabad", "HIGH"),
    ("Fire at Charminar area! Historic monument at risk, firefighters on scene.", "fire", 1, "Hyderabad", "CRITICAL"),
    ("Landslide near Hyderabad outskirts after heavy rains. Highway blocked.", "landslide", 1, "Hyderabad", "HIGH"),
    
    # Mumbai
    ("CRITICAL: Mumbai floods! Marine Drive underwater, trains stopped!", "flood", 1, "Mumbai", "CRITICAL"),
    ("Massive earthquake in Mumbai! Buildings shaking, people evacuating!", "earthquake", 1, "Mumbai", "CRITICAL"),
    ("Fire at Mumbai high-rise! Rescue operations underway, multiple trapped!", "fire", 1, "Mumbai", "CRITICAL"),
    ("Mumbai: Heavy monsoon rains causing severe waterlogging in multiple areas.", "flood", 1, "Mumbai", "HIGH"),
    ("Storm surge hitting Mumbai coastline. Fishing boats advised to return.", "storm", 1, "Mumbai", "MEDIUM"),
    
    # Delhi
    ("Delhi: Earthquake felt across NCR region! Magnitude 5.5, buildings evacuated.", "earthquake", 1, "Delhi", "HIGH"),
    ("Major fire at Delhi market! Hundreds of shops affected, firefighters battling blaze.", "fire", 1, "Delhi", "CRITICAL"),
    ("Delhi: Yamuna river flooding, low-lying areas at risk. Evacuation orders issued.", "flood", 1, "Delhi", "HIGH"),
    ("Dust storm approaching Delhi! Visibility near zero, flights delayed.", "storm", 1, "Delhi", "MEDIUM"),
    
    # Bangalore
    ("Bangalore: Flash floods in tech parks! Employees stranded, rescue teams deployed.", "flood", 1, "Bangalore", "HIGH"),
    ("Fire at Bangalore IT hub! Multiple companies affected, data centers at risk.", "fire", 1, "Bangalore", "CRITICAL"),
    ("Bangalore: Tremors felt, minor earthquake reported. No casualties so far.", "earthquake", 1, "Bangalore", "LOW"),
    ("Heavy rains in Bangalore causing traffic chaos and waterlogging.", "flood", 1, "Bangalore", "MEDIUM"),
    
    # Chennai
    ("Chennai: Cyclone making landfall! Severe winds and rain, stay indoors!", "storm", 1, "Chennai", "CRITICAL"),
    ("Chennai floods: Multiple areas submerged, rescue boats deployed.", "flood", 1, "Chennai", "HIGH"),
    ("Fire at Chennai port! Container yard ablaze, explosions reported.", "fire", 1, "Chennai", "CRITICAL"),
    ("Chennai: Coastal flooding due to high tide and storm surge.", "flood", 1, "Chennai", "HIGH"),
    
    # Kolkata
    ("Kolkata: Severe cyclone warning! Evacuations in coastal areas underway.", "storm", 1, "Kolkata", "CRITICAL"),
    ("Kolkata: Flash floods in multiple districts. Schools closed.", "flood", 1, "Kolkata", "HIGH"),
    ("Fire at Kolkata market! Historic area affected, heritage buildings at risk.", "fire", 1, "Kolkata", "HIGH"),
    
    # Pune
    ("Pune: Dam overflow alert! Downstream areas being evacuated urgently.", "flood", 1, "Pune", "CRITICAL"),
    ("Fire at Pune industrial zone! Chemical plant affected, toxic smoke.", "fire", 1, "Pune", "CRITICAL"),
    ("Pune: Landslide on Mumbai-Pune expressway. Traffic diverted.", "landslide", 1, "Pune", "HIGH"),
    
    # Ahmedabad
    ("Ahmedabad: Earthquake tremors felt! Magnitude 4.8, people rushing out.", "earthquake", 1, "Ahmedabad", "HIGH"),
    ("Fire at Ahmedabad textile market! Massive blaze, multiple casualties feared.", "fire", 1, "Ahmedabad", "CRITICAL"),
    ("Ahmedabad: Flash floods after cloud burst. Low areas submerged.", "flood", 1, "Ahmedabad", "MEDIUM"),
]

# Generate realistic timestamps (last 7 days)
def generate_timestamp():
    days_ago = random.randint(0, 7)
    hours_ago = random.randint(0, 23)
    minutes_ago = random.randint(0, 59)
    return (datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)).isoformat()

# Generate enhanced dataset
data = []
tweet_id = 0

# Add base tweets multiple times with variations
for repeat in range(10):  # 10x repetition = ~320 tweets
    for text, keyword, target, location, severity in TWEETS:
        prefixes = ["", "BREAKING: ", "ALERT: ", "UPDATE: ", "URGENT: ", "⚠️ ", "🚨 "]
        suffixes = ["", " #DisasterAlert", " #Emergency", " Need help!", " Rescue needed!"]
        
        enhanced_text = random.choice(prefixes) + text + random.choice(suffixes)
        
        data.append({
            "id": f"tweet_{tweet_id}",
            "keyword": keyword,
            "location": location,
            "text": enhanced_text,
            "target": target,
            "severity": severity,
            "timestamp": generate_timestamp()
        })
        tweet_id += 1

# Create DataFrame and save
df = pd.DataFrame(data)

# Add some variety in severity distribution
df.loc[df.sample(frac=0.1).index, 'severity'] = 'LOW'

df.to_csv("data/raw/disaster_tweets.csv", index=False)

# Print statistics
print(f"✅ Generated {len(df)} enhanced disaster tweets")
print(f"\n📊 Statistics:")
print(f"  Total tweets: {len(df)}")
print(f"  Disaster tweets: {df['target'].sum()}")
print(f"\n🌍 Location Distribution:")
print(df['location'].value_counts())
print(f"\n⚠️ Severity Distribution:")
print(df['severity'].value_counts())
print(f"\n🔥 Disaster Types:")
print(df['keyword'].value_counts())
print(f"\n🎯 Hyderabad Events: {len(df[df['location'] == 'Hyderabad'])}")
print(f"\n✅ File saved: data/raw/disaster_tweets.csv")
