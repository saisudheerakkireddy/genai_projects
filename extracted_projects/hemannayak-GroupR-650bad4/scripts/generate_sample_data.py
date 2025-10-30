import pandas as pd
import random
from datetime import datetime, timedelta

# Sample disaster tweets
SAMPLE_TWEETS = [
    # Earthquakes
    ("Massive earthquake just hit! Buildings shaking, people running outside. Need help!", "earthquake", 1),
    ("Felt strong tremors, some damage to buildings. Everyone safe so far.", "earthquake", 1),
    ("URGENT: Building collapsed after earthquake, people trapped inside!", "earthquake", 1),
    ("Earthquake reported in downtown area, magnitude 6.5", "earthquake", 1),
    ("Aftershocks continue, people scared to go back inside", "earthquake", 1),
    
    # Floods
    ("Severe flooding in downtown area. Water level rising fast, need rescue teams!", "flood", 1),
    ("Roads completely flooded, cars stuck. Emergency services needed.", "flood", 1),
    ("Trapped on second floor, water still rising. Help needed at Main Street!", "flood", 1),
    ("Flash flood warning! River overflowing, evacuate immediately", "flood", 1),
    ("Water reached first floor, need boats for rescue", "flood", 1),
    
    # Fires
    ("Wildfire spreading rapidly! Multiple homes at risk. Evacuate now!", "fire", 1),
    ("Building on fire, smoke everywhere. Fire department on scene.", "fire", 1),
    ("CRITICAL: Fire out of control, need more firefighters immediately!", "fire", 1),
    ("Forest fire approaching residential area, evacuations underway", "fire", 1),
    ("Smoke filling the air, visibility near zero", "fire", 1),
    
    # Storms
    ("Hurricane approaching, strong winds already causing damage.", "storm", 1),
    ("Severe storm, trees down, power lines damaged. Stay indoors!", "storm", 1),
    ("Storm destroyed several houses, people need shelter and supplies.", "storm", 1),
    ("Tornado warning issued, take shelter immediately", "storm", 1),
    ("Heavy rain and winds, flooding expected", "storm", 1),
    
    # Landslides
    ("Landslide blocked the highway, multiple vehicles trapped", "landslide", 1),
    ("URGENT: Mudslide destroyed homes, people missing", "landslide", 1),
    ("Heavy rains causing landslides in hilly areas", "landslide", 1),
    
    # Regular tweets (not disasters)
    ("Beautiful day today! Weather is perfect.", "weather", 0),
    ("Just had an amazing meal at the new restaurant.", "food", 0),
    ("Excited about the upcoming concert next week!", "entertainment", 0),
    ("Traffic is heavy today but moving smoothly", "traffic", 0),
    ("Great weather for a picnic this weekend", "weather", 0),
    ("New movie release this Friday, can't wait!", "entertainment", 0),
    ("Morning coffee tastes extra good today", "food", 0),
    ("Finished my project on time, feeling accomplished", "work", 0),
]

def generate_sample_dataset(n_samples=200):
    """Generate sample disaster tweets dataset"""
    
    data = []
    locations = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Ahmedabad"]
    
    for i in range(n_samples):
        # Pick random sample
        text, keyword, target = random.choice(SAMPLE_TWEETS)
        
        # Add variation
        if target == 1:
            prefixes = ["", "BREAKING: ", "UPDATE: ", "ALERT: ", "URGENT: ", ""]
            text = random.choice(prefixes) + text
        
        # Random timestamp in last 30 days
        days_ago = random.randint(0, 30)
        timestamp = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))
        
        data.append({
            "id": f"tweet_{i}",
            "keyword": keyword,
            "location": random.choice(locations) if random.random() > 0.3 else "",
            "text": text,
            "target": target,
            "timestamp": timestamp.isoformat()
        })
    
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("🔧 Generating sample disaster dataset...")
    df = generate_sample_dataset(200)
    
    output_path = "data/raw/disaster_tweets.csv"
    df.to_csv(output_path, index=False)
    
    print(f"✅ Generated {len(df)} samples")
    print(f"✅ Saved to: {output_path}")
    print(f"\n📊 Statistics:")
    print(f"  Disaster tweets: {df['target'].sum()}")
    print(f"  Normal tweets: {(1-df['target']).sum()}")
    print(f"\n🎯 Disaster types:")
    disaster_df = df[df['target'] == 1]
    print(disaster_df['keyword'].value_counts())
