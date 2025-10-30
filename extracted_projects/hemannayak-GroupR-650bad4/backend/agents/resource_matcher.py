import math
from typing import List, Tuple
from geopy.distance import geodesic

from ..models import Resource, ResourceMatch, DisasterEvent, ResourceType


MOCK_RESOURCES = [
    Resource(id="R001", type=ResourceType.RESCUE_TEAM, location="Central Station",
             coordinates=(19.0760, 72.8777), capacity=10, available=True, status="active"),
    Resource(id="R002", type=ResourceType.MEDICAL, location="City Hospital",
             coordinates=(19.0896, 72.8656), capacity=50, available=True, status="active"),
    Resource(id="R003", type=ResourceType.SUPPLIES, location="Warehouse A",
             coordinates=(19.1000, 72.9000), capacity=100, available=True, status="active"),
    Resource(id="R004", type=ResourceType.SHELTER, location="Community Center",
             coordinates=(19.0500, 72.8500), capacity=200, available=True, status="active"),
    Resource(id="R005", type=ResourceType.RESCUE_TEAM, location="North Station",
             coordinates=(19.1200, 72.8800), capacity=15, available=True, status="active"),
    # Add more for variety
    Resource(id="R006", type=ResourceType.MEDICAL, location="South Clinic",
             coordinates=(19.0400, 72.8700), capacity=30, available=True, status="active"),
    Resource(id="R007", type=ResourceType.SUPPLIES, location="Warehouse B",
             coordinates=(19.1100, 72.8600), capacity=80, available=True, status="active"),
    Resource(id="R008", type=ResourceType.SHELTER, location="School Hall",
             coordinates=(19.0600, 72.8900), capacity=150, available=True, status="active"),
    Resource(id="R009", type=ResourceType.RESCUE_TEAM, location="East Base",
             coordinates=(19.0800, 72.9200), capacity=12, available=True, status="active"),
    Resource(id="R010", type=ResourceType.MEDICAL, location="East Hospital",
             coordinates=(19.0900, 72.9300), capacity=60, available=True, status="active"),
    Resource(id="R011", type=ResourceType.SUPPLIES, location="Warehouse C",
             coordinates=(19.0700, 72.8400), capacity=90, available=True, status="active"),
    Resource(id="R012", type=ResourceType.SHELTER, location="Church Hall",
             coordinates=(19.0500, 72.9100), capacity=120, available=True, status="active"),
    Resource(id="R013", type=ResourceType.RESCUE_TEAM, location="West Base",
             coordinates=(19.0800, 72.8200), capacity=8, available=True, status="active"),
    Resource(id="R014", type=ResourceType.MEDICAL, location="West Clinic",
             coordinates=(19.0600, 72.8100), capacity=25, available=True, status="active"),
    Resource(id="R015", type=ResourceType.SUPPLIES, location="Warehouse D",
             coordinates=(19.1000, 72.8000), capacity=70, available=True, status="active"),
]


class ResourceMatcher:
    def __init__(self, resources: List[Resource] = None):
        self.resources = resources or MOCK_RESOURCES

    def match_resources(self, event: DisasterEvent, k: int = 3) -> List[ResourceMatch]:
        """
        Find k best resource matches for event.

        Algorithm:
        1. Filter by resource type needed
        2. Calculate distance (haversine formula)
        3. Check availability
        4. Score = f(distance, capacity, availability)
        5. Return top k matches with reasoning
        """
        matches = []
        for resource in self.resources:
            if resource.available:
                # Assume needs map to resource types
                needed_types = self.map_needs_to_types(event.needs)
                if resource.type in needed_types:
                    distance = self.calculate_distance(event.coordinates, resource.coordinates) if event.coordinates else 100
                    eta = self.calculate_eta(distance)
                    score = self.calculate_score(distance, resource.capacity, resource.available)
                    reasoning = self.generate_reasoning(event, resource, distance, eta)
                    matches.append(ResourceMatch(
                        event_id=event.id,
                        resource_id=resource.id,
                        distance_km=distance,
                        eta_minutes=eta,
                        priority_score=score,
                        reasoning=reasoning
                    ))
        # Sort by score descending
        matches.sort(key=lambda x: x.priority_score, reverse=True)
        return matches[:k]

    def map_needs_to_types(self, needs: List[str]) -> List[ResourceType]:
        mapping = {
            "rescue": ResourceType.RESCUE_TEAM,
            "medical": ResourceType.MEDICAL,
            "food": ResourceType.SUPPLIES,
            "water": ResourceType.SUPPLIES,
            "shelter": ResourceType.SHELTER,
            "help": ResourceType.RESCUE_TEAM
        }
        return [mapping.get(need.lower(), ResourceType.SUPPLIES) for need in needs]

    def calculate_distance(self, coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        """Haversine formula for lat/lon distance in km."""
        if not coord1 or not coord2:
            return 100  # Default large distance
        return geodesic(coord1, coord2).km

    def calculate_eta(self, distance_km: float) -> int:
        """Assume 40 km/h average speed in emergency."""
        speed_kmh = 40
        time_hours = distance_km / speed_kmh
        return int(time_hours * 60)

    def calculate_score(self, distance: float, capacity: int, available: bool) -> float:
        """Score based on distance, capacity, availability."""
        distance_score = max(0, 100 - distance * 2)  # Penalty for distance
        capacity_score = min(100, capacity * 2)  # Bonus for capacity
        availability_score = 100 if available else 0
        return (distance_score + capacity_score + availability_score) / 3

    def generate_reasoning(self, event: DisasterEvent, resource: Resource, distance: float, eta: int) -> str:
        """Generate natural language explanation."""
        return f"Assigned {resource.type.value} {resource.id} ({distance:.1f}km away, ETA {eta}min) because event requires {event.needs} and resource is available."
