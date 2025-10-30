import pandas as pd
import re
from datetime import datetime
from typing import List
from loguru import logger

from backend.models import DisasterTweet


def load_disaster_tweets(filepath: str) -> List[DisasterTweet]:
    """Load and process disaster tweets from CSV."""
    try:
        df = pd.read_csv(filepath)
        tweets = []
        for _, row in df.iterrows():
            # Clean text
            text = clean_text(row['text'])
            if len(text) < 10:
                continue
            # Parse date
            try:
                timestamp = datetime.fromisoformat(row['timestamp']) if 'timestamp' in row else datetime.now()
            except:
                timestamp = datetime.now()
            
            # Handle NaN location
            location = row.get('location', None)
            if pd.isna(location):
                location = None
            
            tweet = DisasterTweet(
                id=str(row['id']),
                text=text,
                timestamp=timestamp,
                location=location,
                disaster_type=None,
                severity=None,
                is_real_disaster=bool(row.get('target', 0))
            )
            tweets.append(tweet)
        logger.info(f"Loaded {len(tweets)} tweets from {filepath}")
        return tweets
    except Exception as e:
        logger.error(f"Failed to load tweets: {e}")
        return []


def clean_text(text: str) -> str:
    """Clean tweet text."""
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove mentions
    text = re.sub(r'@\w+', '', text)
    # Remove special chars but keep meaning
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()
