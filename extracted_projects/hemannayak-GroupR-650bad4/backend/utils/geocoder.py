from typing import Optional, Tuple
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from loguru import logger


class LocationGeocoder:
    def __init__(self):
        self.geocoder = Nominatim(user_agent="crisis_lens")
        self.cache = {}  # Cache results

    def geocode(self, location_text: str) -> Optional[Tuple[float, float]]:
        """
        Convert location text to coordinates.

        Examples:
        "Mumbai Central Station" → (19.0760, 72.8777)
        "Bandra West, Mumbai" → (19.0596, 72.8295)

        Returns: (latitude, longitude) or None
        """
        if location_text in self.cache:
            return self.cache[location_text]

        try:
            location = self.geocoder.geocode(location_text, timeout=5)
            if location:
                coords = (location.latitude, location.longitude)
                self.cache[location_text] = coords
                logger.info(f"Geocoded {location_text} to {coords}")
                return coords
        except GeocoderTimedOut:
            logger.warning(f"Geocoding timed out for {location_text}")
        except Exception as e:
            logger.error(f"Geocoding error for {location_text}: {e}")
        return None

    def reverse_geocode(self, lat: float, lon: float) -> str:
        """Get address from coordinates."""
        try:
            location = self.geocoder.reverse((lat, lon), timeout=5)
            if location:
                return location.address
            else:
                return ""
        except GeocoderTimedOut:
            logger.warning(f"Reverse geocoding timed out for {lat}, {lon}")
            return ""
        except Exception as e:
            logger.error(f"Reverse geocoding error for {lat}, {lon}: {e}")
            return ""
