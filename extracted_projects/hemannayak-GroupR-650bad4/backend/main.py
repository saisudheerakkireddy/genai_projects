from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import asyncio
import json
import os
from datetime import datetime, timedelta
from loguru import logger

from backend.models import DisasterEvent, QueryResponse, AgentDecision, Resource, ResourceMatch, DisasterType, Severity
from backend.rag.vector_store import DisasterVectorStore
from backend.rag.query_engine import DisasterQueryEngine
from backend.agents.resource_matcher import ResourceMatcher, MOCK_RESOURCES
from backend.processing.extractor import DisasterInfoExtractor

app = FastAPI(title="CrisisLens AI API")

# CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Global stores
events_store: List[DisasterEvent] = []
resources_store = MOCK_RESOURCES
agent_decisions: List[AgentDecision] = []

# Initialize components
vector_store = DisasterVectorStore('data/chromadb')
extractor = DisasterInfoExtractor()
matcher = ResourceMatcher(resources_store)
query_engine = DisasterQueryEngine(vector_store)

@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    logger.info("Initializing CrisisLens API...")
    logger.info(f"HF_TOKEN present: {bool(os.getenv('HF_TOKEN'))}")
    # Load existing events from vector store
    global events_store
    try:
        results = vector_store.query("disaster", k=100)
        events_store = results
        logger.info(f"Loaded {len(events_store)} events from vector store")
    except Exception as e:
        logger.warning(f"Could not load events: {e}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}

@app.post("/stream/start")
async def start_stream(keywords: List[str] = Query(...)):
    """Start Twitter monitoring (placeholder)."""
    return {"status": "streaming", "keywords": keywords, "note": "Streaming not implemented in demo"}

@app.post("/stream/stop")
async def stop_stream():
    """Stop streaming."""
    return {"status": "stopped"}

@app.get("/events")
async def get_events(
    limit: int = Query(10),
    severity: Optional[Severity] = None,
    disaster_type: Optional[DisasterType] = None,
    hours: int = Query(24)
) -> List[DisasterEvent]:
    """Get paginated events."""
    filtered = events_store
    if severity:
        filtered = [e for e in filtered if e.severity == severity]
    if disaster_type:
        filtered = [e for e in filtered if e.disaster_type == disaster_type]
    # Filter by hours
    cutoff = datetime.now() - timedelta(hours=hours)
    filtered = [e for e in filtered if e.timestamp > cutoff]
    return filtered[-limit:]  # Last limit

@app.get("/events/map-data")
async def get_map_data() -> List[Dict]:
    """Return events for map."""
    return [
        {
            "lat": e.coordinates[0] if e.coordinates else 0,
            "lon": e.coordinates[1] if e.coordinates else 0,
            "severity": e.severity.value,
            "text": e.text[:100],
            "type": e.disaster_type.value
        }
        for e in events_store if e.coordinates
    ]

@app.post("/query")
async def query_api(question: str) -> QueryResponse:
    """Query the system."""
    return await query_engine.query(question)

@app.get("/agent/decisions")
async def get_agent_decisions() -> List[AgentDecision]:
    """Get recent agent decisions."""
    return agent_decisions[-10:]  # Last 10

@app.get("/resources")
async def get_resources() -> List[Resource]:
    """Get available resources."""
    return [r for r in resources_store if r.available]

@app.post("/resources/match")
async def match_resources(event_id: str) -> List[ResourceMatch]:
    """Match resources for event."""
    event = next((e for e in events_store if e.id == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    matches = matcher.match_resources(event)
    return matches

@app.get("/report")
async def generate_report() -> str:
    """Generate situation report."""
    return await query_engine.generate_situation_report()

@app.get("/stats")
async def get_stats() -> Dict:
    """Get real-time stats."""
    severity_dist = {}
    disaster_types = {}
    
    for event in events_store:
        severity_dist[event.severity.value] = severity_dist.get(event.severity.value, 0) + 1
        disaster_types[event.disaster_type.value] = disaster_types.get(event.disaster_type.value, 0) + 1
    
    return {
        "total_events": len(events_store),
        "events_per_minute": 0,
        "severity_distribution": severity_dist,
        "disaster_types": disaster_types,
        "critical": severity_dist.get("CRITICAL", 0),
        "new_last_hour": 0,
        "critical_change": 0
    }

# WebSocket for real-time events
@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Send new events (simplified)
            if events_store:
                data = json.dumps([
                    {
                        "id": e.id,
                        "text": e.text,
                        "severity": e.severity.value,
                        "type": e.disaster_type.value
                    }
                    for e in events_store[-5:]  # Last 5
                ])
                await websocket.send_text(data)
            await asyncio.sleep(10)  # Poll every 10s
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
