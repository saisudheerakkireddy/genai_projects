import time
from typing import List, Callable, Optional
import tweepy
from loguru import logger
import snscrape.modules.twitter as sntwitter


class TwitterStreamMonitor:
    def __init__(self, bearer_token: str, callback: Callable):
        self.client = tweepy.Client(bearer_token=bearer_token)
        self.callback = callback
        self.streaming = False

    def start_stream(self, keywords: List[str], location_box: Optional[List[float]] = None):
        """
        Stream tweets matching disaster keywords.

        Keywords: ["earthquake", "flood", "fire", "emergency",
                   "help needed", "rescue", "disaster", "trapped"]

        Uses Twitter API v2 filtered stream.
        Calls callback(tweet_data) for each matching tweet.
        """
        try:
            # Add rules for filtered stream
            rule = " OR ".join(keywords)
            self.client.create_tweet_filter(rule=rule)
            self.streaming = True

            # Start streaming (simplified; in real, use async stream)
            while self.streaming:
                tweets = self.client.search_recent_tweets(query=rule, max_results=10)
                for tweet in tweets.data or []:
                    tweet_data = {
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'location': tweet.geo if hasattr(tweet, 'geo') else None
                    }
                    self.callback(tweet_data)
                time.sleep(60)  # Rate limiting
        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            self.streaming = False

    def stop_stream(self):
        """Gracefully stop streaming."""
        self.streaming = False
        logger.info("Streaming stopped.")


class TwitterScraper:
    def __init__(self):
        pass

    def search_recent(self, query: str, max_results: int = 100) -> List[dict]:
        """
        Scrape recent tweets (no API key needed).
        Use for demo if Twitter API unavailable.
        """
        tweets = []
        try:
            for tweet in sntwitter.TwitterSearchScraper(query).get_items():
                if len(tweets) >= max_results:
                    break
                tweets.append({
                    'id': tweet.id,
                    'text': tweet.content,
                    'created_at': tweet.date,
                    'user': tweet.user.username
                })
        except Exception as e:
            logger.error(f"Scraping failed: {e}")
        return tweets


# Fallback class that tries API first, then scraper
class TwitterMonitor:
    def __init__(self, bearer_token: Optional[str] = None, callback: Optional[Callable] = None):
        self.bearer_token = bearer_token
        self.callback = callback
        self.api_monitor = None
        self.scraper = TwitterScraper()

    def start_stream(self, keywords: List[str], location_box: Optional[List[float]] = None):
        if self.bearer_token and self.callback:
            logger.info("Using Twitter API for streaming.")
            self.api_monitor = TwitterStreamMonitor(self.bearer_token, self.callback)
            self.api_monitor.start_stream(keywords, location_box)
        else:
            logger.info("Using Twitter scraper (no API key).")
            # Simulate streaming with periodic scraping
            while True:
                query = " OR ".join(keywords)
                tweets = self.scraper.search_recent(query, max_results=10)
                for tweet in tweets:
                    if self.callback:
                        tweet_data = {
                            'id': tweet['id'],
                            'text': tweet['text'],
                            'created_at': tweet['created_at'],
                            'location': None  # Scraper doesn't provide location easily
                        }
                        self.callback(tweet_data)
                time.sleep(60)  # Poll every minute

    def stop_stream(self):
        if self.api_monitor:
            self.api_monitor.stop_stream()
