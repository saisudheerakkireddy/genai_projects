from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
from typing import List, Optional
import random
from datetime import datetime
import os

app = FastAPI(title="CrisisLens API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data on startup
EVENTS = []

@app.on_event("startup")
async def startup():
    global EVENTS
    
    # City coordinates (lat, lon)
    CITY_COORDS = {
        'Hyderabad': (17.3850, 78.4867),
        'Mumbai': (19.0760, 72.8777),
        'Delhi': (28.6139, 77.2090),
        'Bangalore': (12.9716, 77.5946),
        'Chennai': (13.0827, 80.2707),
        'Kolkata': (22.5726, 88.3639),
        'Pune': (18.5204, 73.8567),
        'Ahmedabad': (23.0225, 72.5714),
    }
    
    try:
        # Try to load from data directory
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'disaster_tweets.csv')
        df = pd.read_csv(data_path)
        df = df[df['target'] == 1].head(200)  # Load more events
        
        for _, row in df.iterrows():
            location = str(row.get('location', 'Mumbai'))
            
            # Get base coordinates for the city
            if location in CITY_COORDS:
                base_lat, base_lon = CITY_COORDS[location]
            else:
                base_lat, base_lon = CITY_COORDS['Mumbai']  # Default to Mumbai
            
            # Add small random offset for variety (within ~5km)
            lat = base_lat + random.uniform(-0.05, 0.05)
            lon = base_lon + random.uniform(-0.05, 0.05)
            
            EVENTS.append({
                'id': str(row['id']),
                'text': str(row['text']),
                'keyword': str(row.get('keyword', 'other')),
                'location': location,
                'severity': str(row.get('severity', random.choice(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']))),
                'type': str(row.get('keyword', 'other')).upper(),
                'timestamp': datetime.now().isoformat(),
                'lat': lat,
                'lon': lon,
            })
        print(f"✅ Loaded {len(EVENTS)} events across {len(set([e['location'] for e in EVENTS]))} cities")
    except Exception as e:
        print(f"⚠️ Error loading data: {e}")
        # Create some dummy data with proper coordinates
        for i in range(40):
            location = random.choice(list(CITY_COORDS.keys()))
            base_lat, base_lon = CITY_COORDS[location]
            
            EVENTS.append({
                'id': f'event_{i}',
                'text': f'Sample disaster event {i} in {location}',
                'keyword': random.choice(['earthquake', 'flood', 'fire']),
                'location': location,
                'severity': random.choice(['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']),
                'type': random.choice(['EARTHQUAKE', 'FLOOD', 'FIRE']),
                'timestamp': datetime.now().isoformat(),
                'lat': base_lat + random.uniform(-0.05, 0.05),
                'lon': base_lon + random.uniform(-0.05, 0.05),
            })
        print(f"✅ Created {len(EVENTS)} dummy events")

@app.get("/health")
def health():
    return {"status": "healthy", "events": len(EVENTS)}

@app.get("/stats")
def get_stats():
    severities = {}
    types = {}
    for event in EVENTS:
        severities[event['severity']] = severities.get(event['severity'], 0) + 1
        types[event['type']] = types.get(event['type'], 0) + 1
    
    return {
        "total_events": len(EVENTS),
        "events_per_minute": random.randint(5, 15),
        "severity_distribution": severities,
        "disaster_types": types,
        "critical": severities.get('CRITICAL', 0),
        "new_last_hour": random.randint(5, 15),
        "critical_change": random.randint(-2, 5)
    }

@app.get("/events")
def get_events(limit: int = 50):
    return EVENTS[:limit]

@app.get("/events/map-data")
def get_map_data():
    return EVENTS

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
def query_events(req: QueryRequest):
    question = req.question
    question_lower = question.lower()
    
    # Advanced query understanding
    query_intent = analyze_query_intent(question_lower)
    query_location = extract_location(question_lower)
    query_severity = extract_severity(question_lower)
    query_disaster_type = extract_disaster_type(question_lower)
    
    # Filter events based on extracted parameters
    filtered_events = EVENTS.copy()
    
    # Apply location filter if specified
    if query_location:
        filtered_events = [e for e in filtered_events if query_location.lower() in e['location'].lower()]
    
    # Apply severity filter if specified
    if query_severity:
        filtered_events = [e for e in filtered_events if e['severity'] == query_severity]
    
    # Apply disaster type filter if specified
    if query_disaster_type:
        filtered_events = [e for e in filtered_events 
                          if query_disaster_type.lower() in e['type'].lower() or 
                             query_disaster_type.lower() in e['keyword'].lower()]
    
    # Semantic matching for remaining events
    relevant = []
    for event in filtered_events:
        relevance_score = calculate_relevance(question_lower, event)
        if relevance_score > 0.3:  # Threshold for relevance
            event['relevance_score'] = relevance_score
            relevant.append(event)
    
    # Sort by relevance and severity
    relevant.sort(key=lambda e: (e.get('relevance_score', 0), severity_score(e['severity'])), reverse=True)
    
    # Limit to top results
    top_relevant = relevant[:5]
    
    # Generate comprehensive response
    if not top_relevant:
        answer = "No relevant disaster events found for your query. Please try a different question or broaden your search criteria."
        confidence = 0.3
    else:
        answer = generate_response(question, query_intent, top_relevant)
        confidence = calculate_confidence(question, top_relevant)
    
    # Generate action items if applicable
    action_items = []
    if query_intent in ['action', 'help', 'response'] and top_relevant:
        action_items = generate_action_items(top_relevant)
    
    return {
        "answer": answer,
        "sources": [e['id'] for e in top_relevant],
        "relevant_events": top_relevant,
        "confidence": confidence,
        "action_items": action_items
    }

# Helper functions for advanced query processing

def analyze_query_intent(question):
    """Determine the intent of the query."""
    if any(word in question for word in ['what', 'where', 'which', 'how many', 'list', 'show']):
        return 'information'
    elif any(word in question for word in ['why', 'how', 'explain', 'reason', 'cause']):
        return 'explanation'
    elif any(word in question for word in ['should', 'need', 'action', 'help', 'respond', 'do']):
        return 'action'
    else:
        return 'information'

def extract_location(question):
    """Extract location from the query."""
    locations = ['Hyderabad', 'Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad']
    for location in locations:
        if location.lower() in question:
            return location
    return None

def extract_severity(question):
    """Extract severity level from the query."""
    if 'critical' in question:
        return 'CRITICAL'
    elif 'high' in question:
        return 'HIGH'
    elif 'medium' in question:
        return 'MEDIUM'
    elif 'low' in question:
        return 'LOW'
    return None

def extract_disaster_type(question):
    """Extract disaster type from the query."""
    disaster_types = ['earthquake', 'flood', 'fire', 'storm', 'cyclone', 'landslide', 'tsunami']
    for disaster in disaster_types:
        if disaster in question:
            return disaster.upper()
    return None

def calculate_relevance(question, event):
    """Calculate relevance score between question and event."""
    # Simple TF-IDF like scoring
    question_words = set(question.split())
    event_text = event['text'].lower() + ' ' + event['type'].lower() + ' ' + event['location'].lower()
    
    # Count matching words
    matching_words = sum(1 for word in question_words if word in event_text)
    
    # Calculate score based on matches and event severity
    base_score = matching_words / max(len(question_words), 1)
    severity_boost = severity_score(event['severity']) * 0.2
    
    return min(base_score + severity_boost, 1.0)

def severity_score(severity):
    """Convert severity to numeric score."""
    return {'CRITICAL': 1.0, 'HIGH': 0.75, 'MEDIUM': 0.5, 'LOW': 0.25}.get(severity, 0)

def calculate_confidence(question, relevant_events):
    """Calculate confidence score based on relevance and number of events."""
    if not relevant_events:
        return 0.3
    
    # Average relevance of top events
    avg_relevance = sum(e.get('relevance_score', 0) for e in relevant_events) / len(relevant_events)
    
    # Boost confidence based on number of relevant events
    count_factor = min(len(relevant_events) / 3, 1.0) * 0.2
    
    return min(avg_relevance + count_factor, 0.95)

def generate_response(question, intent, events):
    """Generate comprehensive response based on intent and events."""
    if not events:
        return "No relevant information found."
    
    # Group events by location and severity
    locations = {}
    severities = {'CRITICAL': [], 'HIGH': [], 'MEDIUM': [], 'LOW': []}
    
    for event in events:
        loc = event['location']
        sev = event['severity']
        
        if loc not in locations:
            locations[loc] = []
        locations[loc].append(event)
        severities[sev].append(event)
    
    # Generate response based on intent
    if intent == 'information':
        response = f"Based on the available data, I found {len(events)} relevant events. "
        
        # Add severity breakdown
        critical_count = len(severities['CRITICAL'])
        high_count = len(severities['HIGH'])
        
        if critical_count > 0:
            response += f"There {'is' if critical_count == 1 else 'are'} {critical_count} critical situation{'s' if critical_count != 1 else ''} "
            if high_count > 0:
                response += f"and {high_count} high-priority event{'s' if high_count != 1 else ''}. "
            else:
                response += ". "
        elif high_count > 0:
            response += f"There {'is' if high_count == 1 else 'are'} {high_count} high-priority event{'s' if high_count != 1 else ''}. "
        
        # Add location breakdown
        if len(locations) > 1:
            response += f"Events are spread across {len(locations)} locations. "
            most_affected = max(locations.items(), key=lambda x: len(x[1]))
            response += f"The most affected area is {most_affected[0]} with {len(most_affected[1])} incidents. "
        elif len(locations) == 1:
            location = list(locations.keys())[0]
            response += f"All events are in {location}. "
        
        # Add specific details about the most critical event
        if critical_count > 0:
            most_critical = severities['CRITICAL'][0]
            response += f"Most critical situation: {most_critical['text']}"
        elif high_count > 0:
            most_urgent = severities['HIGH'][0]
            response += f"Most urgent situation: {most_urgent['text']}"
    
    elif intent == 'explanation':
        response = f"Based on the analysis of {len(events)} events, "
        
        if len(events) > 0:
            event_types = set(e['type'] for e in events)
            if len(event_types) == 1:
                response += f"the situation involves a {list(event_types)[0]} event. "
            else:
                response += f"the situation involves multiple types of events including {', '.join(list(event_types)[:3])}. "
            
            response += "The data suggests that " + events[0]['text'] + " "
            
            if len(events) > 1:
                response += "Additionally, " + events[1]['text']
    
    elif intent == 'action':
        response = "Based on the current situation, the following actions are recommended:\n\n"
        
        if len(severities['CRITICAL']) > 0:
            response += "1. IMMEDIATE RESPONSE REQUIRED for critical situations:\n"
            for i, event in enumerate(severities['CRITICAL'][:2]):
                response += f"   - {event['location']}: {event['text']}\n"
            response += "\n"
        
        if len(severities['HIGH']) > 0:
            response += "2. URGENT ATTENTION needed for high-priority events:\n"
            for i, event in enumerate(severities['HIGH'][:2]):
                response += f"   - {event['location']}: {event['text']}\n"
            response += "\n"
        
        response += "3. Recommended resources to deploy: Emergency response teams, medical personnel, and rescue equipment."
    
    else:  # Default response
        response = f"Found {len(events)} relevant events. Here are the key details:\n\n"
        for i, event in enumerate(events[:3]):
            response += f"{i+1}. {event['severity']} {event['type']} in {event['location']}: {event['text']}\n"
    
    return response

def generate_action_items(events):
    """Generate action items based on events."""
    action_items = []
    
    # Critical events need immediate evacuation
    critical_events = [e for e in events if e['severity'] == 'CRITICAL']
    if critical_events:
        action_items.append({
            "title": "Immediate Evacuation",
            "description": f"Evacuate residents in {', '.join(set(e['location'] for e in critical_events))} due to critical events.",
            "priority": "CRITICAL"
        })
    
    # High severity events need emergency services
    high_events = [e for e in events if e['severity'] == 'HIGH']
    if high_events:
        action_items.append({
            "title": "Deploy Emergency Services",
            "description": f"Send medical and rescue teams to {', '.join(set(e['location'] for e in high_events))}.",
            "priority": "HIGH"
        })
    
    # General action for all events
    if events:
        action_items.append({
            "title": "Establish Command Center",
            "description": "Set up a central command center to coordinate response efforts across all affected areas.",
            "priority": "MEDIUM"
        })
    
    return action_items

@app.get("/resources")
def get_resources():
    return [
        {"id": "R001", "type": "RESCUE_TEAM", "location": "Central Station", "available": True},
        {"id": "R002", "type": "MEDICAL", "location": "City Hospital", "available": True},
        {"id": "R003", "type": "SUPPLIES", "location": "Warehouse A", "available": True},
    ]

@app.get("/agent/decisions")
def get_agent_decisions():
    decisions = []
    critical_events = [e for e in EVENTS if e['severity'] == 'CRITICAL'][:3]
    for event in critical_events:
        decisions.append({
            "timestamp": datetime.now().isoformat(),
            "event_id": event['id'],
            "priority_score": random.randint(80, 100),
            "recommended_action": f"Deploy resources to {event['location']}",
            "assigned_resources": ["R001", "R002"],
            "reasoning": f"High priority {event['type']} event requiring immediate response.",
            "event_text": event['text']
        })
    return decisions

@app.get("/report")
def generate_report():
    critical = [e for e in EVENTS if e['severity'] == 'CRITICAL']
    high = [e for e in EVENTS if e['severity'] == 'HIGH']
    
    report = f"""# Crisis Situation Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary
- Total Events: {len(EVENTS)}
- Critical Situations: {len(critical)}
- High Priority: {len(high)}

## Top Critical Events
"""
    for i, event in enumerate(critical[:5], 1):
        report += f"\n{i}. **{event['type']}** - {event['location']}\n   {event['text'][:100]}...\n"
    
    return report

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
