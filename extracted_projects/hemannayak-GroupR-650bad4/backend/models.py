from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
from typing import List, Optional, Tuple


class DisasterType(str, Enum):
    EARTHQUAKE = "EARTHQUAKE"
    FLOOD = "FLOOD"
    FIRE = "FIRE"
    STORM = "STORM"
    LANDSLIDE = "LANDSLIDE"
    OTHER = "OTHER"


class Severity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class ResourceType(str, Enum):
    RESCUE_TEAM = "RESCUE_TEAM"
    MEDICAL = "MEDICAL"
    SUPPLIES = "SUPPLIES"
    SHELTER = "SHELTER"


class DisasterEvent(BaseModel):
    id: str = Field(..., description="Unique identifier for the event")
    text: str = Field(..., description="Original text of the event report")
    timestamp: datetime = Field(..., description="Timestamp of the event")
    location: Optional[str] = Field(None, description="Location description")
    coordinates: Optional[Tuple[float, float]] = Field(None, description="Latitude and longitude")
    disaster_type: DisasterType = Field(..., description="Type of disaster")
    severity: Severity = Field(..., description="Severity level")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    source: str = Field(..., description="Source of the event (twitter, news, manual)")
    needs: List[str] = Field(default_factory=list, description="List of needs mentioned")
    is_verified: bool = Field(default=False, description="Whether the event is verified")

    class Config:
        schema_extra = {
            "example": {
                "id": "event_123",
                "text": "Building collapsed in downtown",
                "timestamp": "2023-10-01T12:00:00Z",
                "location": "Downtown",
                "coordinates": (19.0760, 72.8777),
                "disaster_type": "EARTHQUAKE",
                "severity": "CRITICAL",
                "confidence": 0.95,
                "source": "twitter",
                "needs": ["rescue", "medical"],
                "is_verified": True
            }
        }


class Resource(BaseModel):
    id: str = Field(..., description="Unique identifier for the resource")
    type: ResourceType = Field(..., description="Type of resource")
    location: str = Field(..., description="Location of the resource")
    coordinates: Tuple[float, float] = Field(..., description="Latitude and longitude")
    capacity: int = Field(..., gt=0, description="Capacity of the resource")
    available: bool = Field(default=True, description="Whether the resource is available")
    status: str = Field(default="active", description="Status of the resource")

    class Config:
        schema_extra = {
            "example": {
                "id": "R001",
                "type": "RESCUE_TEAM",
                "location": "Central Station",
                "coordinates": (19.0760, 72.8777),
                "capacity": 10,
                "available": True,
                "status": "active"
            }
        }


class ResourceMatch(BaseModel):
    event_id: str = Field(..., description="ID of the matched event")
    resource_id: str = Field(..., description="ID of the matched resource")
    distance_km: float = Field(..., ge=0.0, description="Distance in kilometers")
    eta_minutes: int = Field(..., gt=0, description="Estimated time of arrival in minutes")
    priority_score: float = Field(..., ge=0.0, le=100.0, description="Priority score")
    reasoning: str = Field(..., description="Explanation for the match")

    class Config:
        schema_extra = {
            "example": {
                "event_id": "event_123",
                "resource_id": "R001",
                "distance_km": 5.2,
                "eta_minutes": 8,
                "priority_score": 95.0,
                "reasoning": "Assigned Rescue Team R001 (5km away, ETA 8min) because event is critical."
            }
        }


class ExtractedInfo(BaseModel):
    disaster_type: DisasterType = Field(..., description="Type of disaster")
    severity: Severity = Field(..., description="Severity level")
    location: Optional[str] = Field(None, description="Specific location if mentioned")
    needs: List[str] = Field(default_factory=list, description="List of needs")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")

    class Config:
        schema_extra = {
            "example": {
                "disaster_type": "FLOOD",
                "severity": "CRITICAL",
                "location": "Main St Bridge",
                "needs": ["rescue", "medical"],
                "confidence": 0.95
            }
        }


class QueryResponse(BaseModel):
    answer: str = Field(..., description="Generated answer")
    sources: List[str] = Field(default_factory=list, description="List of source tweet IDs")
    relevant_events: List[DisasterEvent] = Field(default_factory=list, description="Relevant events")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")

    class Config:
        schema_extra = {
            "example": {
                "answer": "Multiple floods reported in Mumbai.",
                "sources": ["123456"],
                "relevant_events": [],
                "confidence": 0.95
            }
        }


class DisasterTweet(BaseModel):
    id: str = Field(..., description="Tweet ID")
    text: str = Field(..., description="Tweet text")
    timestamp: datetime = Field(..., description="Timestamp")
    location: Optional[str] = Field(None, description="Location")
    disaster_type: Optional[str] = Field(None, description="Disaster type")
    severity: Optional[str] = Field(None, description="Severity")
    is_real_disaster: bool = Field(..., description="Whether it's a real disaster")

    class Config:
        schema_extra = {
            "example": {
                "id": "123456",
                "text": "Earthquake in Mumbai",
                "timestamp": "2023-10-01T12:00:00Z",
                "location": "Mumbai",
                "disaster_type": "EARTHQUAKE",
                "severity": "HIGH",
                "is_real_disaster": True
            }
        }
