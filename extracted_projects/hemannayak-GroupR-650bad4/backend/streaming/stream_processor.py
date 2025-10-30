import asyncio
from datetime import datetime
from collections import defaultdict
from typing import Dict, List, Optional
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from loguru import logger

from backend.models import DisasterEvent, ExtractedInfo, DisasterType, Severity
from backend.streaming.twitter_stream import TwitterMonitor


class StreamProcessor:
    def __init__(self, extractor, classifier, vector_store):
        self.extractor = extractor
        self.classifier = classifier  # Placeholder for ML classifier
        self.vector_store = vector_store
        self.geocoder = Nominatim(user_agent="crisis_lens")
        self.stats = defaultdict(int)
        self.events_per_minute = []
        self.cache = {}

    async def process_tweet(self, tweet_data: dict) -> DisasterEvent:
        text = tweet_data['text']
        tweet_id = str(tweet_data['id'])
        timestamp = tweet_data.get('created_at', datetime.now())

        # 1. Extract info using extractor
        extracted = self.extractor.extract(text)

        # 2. Classify severity (if needed, fallback to extracted)
        severity, confidence = self.classifier.predict(text) if self.classifier else (extracted.severity, extracted.confidence)

        # 3. Geocode location
        location = extracted.location
        coordinates = None
        if location:
            coordinates = self.geocode_location(location)

        # 4. Create DisasterEvent
        event = DisasterEvent(
            id=tweet_id,
            text=text,
            timestamp=timestamp,
            location=location,
            coordinates=coordinates,
            disaster_type=extracted.disaster_type,
            severity=severity,
            confidence=confidence,
            source="twitter",
            needs=extracted.needs,
            is_verified=False
        )

        # 5. Add to vector store
        if self.vector_store:
            self.vector_store.add_tweets([event])

        # Update stats
        self.stats['total_events'] += 1
        self.stats[severity.value] += 1
        self.stats[extracted.disaster_type.value] += 1

        logger.info(f"Processed event: {event.id} - {event.disaster_type} {event.severity}")
        return event

    def geocode_location(self, location: str) -> Optional[tuple]:
        if location in self.cache:
            return self.cache[location]
        try:
            loc = self.geocoder.geocode(location, timeout=5)
            if loc:
                coords = (loc.latitude, loc.longitude)
                self.cache[location] = coords
                return coords
        except GeocoderTimedOut:
            logger.warning(f"Geocoding timed out for {location}")
        return None

    async def start_monitoring(self, keywords: List[str], bearer_token: Optional[str] = None):
        monitor = TwitterMonitor(bearer_token=bearer_token, callback=self.process_tweet)
        await monitor.start_stream(keywords)

    def get_stats(self) -> Dict:
        current_time = datetime.now()
        events_last_minute = sum(1 for e in self.events_per_minute if (current_time - e).seconds < 60)
        self.events_per_minute.append(current_time)
        self.events_per_minute = [e for e in self.events_per_minute if (current_time - e).seconds < 300]  # Keep last 5 min

        severity_dist = {k: v for k, v in self.stats.items() if k in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']}
        disaster_dist = {k: v for k, v in self.stats.items() if k in ['EARTHQUAKE', 'FLOOD', 'FIRE', 'STORM', 'OTHER']}

        return {
            'total_events': self.stats['total_events'],
            'events_per_minute': events_last_minute,
            'severity_distribution': severity_dist,
            'disaster_types': disaster_dist,
            'top_disaster': max(disaster_dist, key=disaster_dist.get) if disaster_dist else None
        }
