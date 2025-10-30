import pandas as pd
import random
import os

os.makedirs('data/raw', exist_ok=True)

TWEETS = [
    ("URGENT: Massive earthquake! Buildings collapsed, people trapped!", "earthquake", 1, "Mumbai"),
    ("Severe flooding downtown. Water rising fast!", "flood", 1, "Delhi"),
    ("Wildfire spreading! Evacuate immediately!", "fire", 1, "Bangalore"),
    ("Hurricane winds destroying homes!", "storm", 1, "Chennai"),
    ("Building collapsed after earthquake, need rescue teams!", "earthquake", 1, "Mumbai"),
    ("Flash flood, cars underwater, help needed!", "flood", 1, "Kolkata"),
    ("Forest fire out of control!", "fire", 1, "Pune"),
    ("Cyclone causing massive damage!", "storm", 1, "Visakhapatnam"),
    ("Tremors felt, some damage reported", "earthquake", 1, "Delhi"),
    ("Heavy rain causing floods", "flood", 1, "Mumbai"),
    ("Small fire contained", "fire", 1, "Bangalore"),
    ("Storm passed, cleanup needed", "storm", 1, "Chennai"),
] * 25  # Repeat for 300 tweets

data = []
for i, (text, keyword, target, location) in enumerate(TWEETS):
    prefixes = ["", "BREAKING: ", "ALERT: ", "UPDATE: "]
    data.append({
        "id": f"tweet_{i}",
        "keyword": keyword,
        "location": location,
        "text": random.choice(prefixes) + text,
        "target": target
    })

df = pd.DataFrame(data)
df.to_csv("data/raw/disaster_tweets.csv", index=False)
print(f"✅ Created {len(df)} sample tweets")
print(f"   Disaster tweets: {len(df)}")
print(f"   File: data/raw/disaster_tweets.csv")
