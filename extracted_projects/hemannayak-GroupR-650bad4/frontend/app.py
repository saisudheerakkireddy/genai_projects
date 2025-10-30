import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
import requests
import json
from datetime import datetime
import time

st.set_page_config(layout="wide", page_title="CrisisLens AI", page_icon="🚨")

# Custom CSS
st.markdown("""
<style>
.big-font {font-size:20px !important; font-weight: bold;}
.critical {background-color: #ff4444; color: white; padding: 10px; border-radius: 5px;}
.high {background-color: #ff8800; color: white; padding: 10px; border-radius: 5px;}
</style>
""", unsafe_allow_html=True)

# API base URL
API_BASE = "http://localhost:8000"

# API functions
def fetch_stats():
    try:
        response = requests.get(f"{API_BASE}/stats")
        return response.json()
    except:
        return {"total_events": 0, "events_per_minute": 0}

def fetch_events(severity=None, disaster_type=None, hours=24):
    params = {"hours": hours}
    if severity:
        params["severity"] = severity
    if disaster_type:
        params["disaster_type"] = disaster_type
    try:
        response = requests.get(f"{API_BASE}/events", params=params)
        return response.json()
    except:
        return []

def fetch_map_data():
    try:
        response = requests.get(f"{API_BASE}/events/map-data")
        return response.json()
    except:
        return []

def fetch_resources():
    try:
        response = requests.get(f"{API_BASE}/resources")
        return response.json()
    except:
        return []

def fetch_agent_decisions():
    try:
        response = requests.get(f"{API_BASE}/agent/decisions")
        return response.json()
    except:
        return []

def query_api(question):
    try:
        response = requests.post(f"{API_BASE}/query", json={"question": question})
        return response.json()
    except:
        return {"answer": "Error", "confidence": 0.0, "sources": []}

def generate_report():
    try:
        response = requests.get(f"{API_BASE}/report")
        return response.text
    except:
        return "Error generating report"

def start_stream(keywords):
    try:
        requests.post(f"{API_BASE}/stream/start", params={"keywords": keywords})
    except:
        pass

def stop_stream():
    try:
        requests.post(f"{API_BASE}/stream/stop")
    except:
        pass

def create_severity_pie(stats):
    data = stats.get('severity_distribution', {})
    return px.pie(values=list(data.values()), names=list(data.keys()))

def create_type_bar(stats):
    data = stats.get('disaster_types', {})
    return px.bar(x=list(data.keys()), y=list(data.values()))

# Header
st.title("🚨 CrisisLens AI - Real-Time Disaster Intelligence")
st.markdown("*AI-Powered Crisis Response Coordination System*")

# Sidebar
with st.sidebar:
    st.header("📊 Live Statistics")
    stats = fetch_stats()
    col1, col2 = st.columns(2)
    col1.metric("Total Events", stats.get('total_events', 0))
    col2.metric("Events/Min", stats.get('events_per_minute', 0))
    st.plotly_chart(create_severity_pie(stats), use_container_width=True)
    st.plotly_chart(create_type_bar(stats), use_container_width=True)
    st.markdown("---")
    st.header("🔴 Stream Control")
    keywords = st.text_input("Keywords (comma-separated)", "earthquake,flood,fire")
    if st.button("▶️ Start Monitoring"):
        start_stream(keywords.split(","))
        st.success("Monitoring started!")
    if st.button("⏸️ Stop Monitoring"):
        stop_stream()
        st.info("Monitoring stopped")
    auto_refresh = st.checkbox("Auto-refresh (30s)")
    if auto_refresh:
        time.sleep(30)
        st.rerun()

# Main Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ Live Map", 
    "💬 Query Assistant", 
    "🤖 Agent Decisions",
    "📋 Situation Report", 
    "🔍 Event Details"
])

with tab1:  # LIVE MAP
    st.header("Real-Time Crisis Map")
    events = fetch_map_data()
    if events:
        m = folium.Map(location=[19.0760, 72.8777], zoom_start=11)
        for event in events:
            color = {
                'CRITICAL': 'red',
                'HIGH': 'orange',
                'MEDIUM': 'yellow',
                'LOW': 'green'
            }.get(event['severity'], 'blue')
            folium.Marker(
                location=[event['lat'], event['lon']],
                popup=f"{event['type']} - {event['severity']}: {event['text']}",
                icon=folium.Icon(color=color)
            ).add_to(m)
        st_folium(m, width=1400, height=600)
    else:
        st.info("No map data available.")

with tab2:  # QUERY ASSISTANT
    st.header("AI Query Assistant")
    examples = st.selectbox("Try examples:", [
        "What are the most critical situations?",
        "Where are floods happening?",
        "Which areas need rescue teams?",
        "What resources are available?",
        "Show me recent earthquakes"
    ])
    query = st.text_input("Ask about the situation:", value=examples)
    if st.button("🔍 Search"):
        with st.spinner("Analyzing..."):
            response = query_api(query)
            st.markdown("### 📝 Answer")
            st.info(response.get('answer', 'No answer'))
            st.progress(response.get('confidence', 0.0))
            st.caption(f"Confidence: {response.get('confidence', 0.0)*100:.1f}%")
            st.markdown("### 📚 Sources")
            for source in response.get('sources', []):
                st.caption(f"Source: {source}")

with tab3:  # AGENT DECISIONS
    st.header("🤖 AI Agent Decisions & Resource Allocation")
    decisions = fetch_agent_decisions()
    for decision in decisions:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f'<div class="critical">Priority: {decision.get("priority_score", 0)}/100</div>', unsafe_allow_html=True)
                st.markdown(f"**Reasoning:** {decision.get('reasoning', '')}")
            with col2:
                st.metric("Resources", len(decision.get('assigned_resources', [])))

with tab4:  # SITUATION REPORT
    st.header("📋 Automated Situation Report")
    if st.button("Generate Report"):
        with st.spinner("Generating..."):
            report = generate_report()
            st.markdown(report)
            st.download_button("📥 Download", report, "report.md")

with tab5:  # EVENT DETAILS
    st.header("🔍 Event Feed")
    col1, col2, col3 = st.columns(3)
    severity_filter = col1.multiselect("Severity", ["CRITICAL", "HIGH", "MEDIUM", "LOW"])
    type_filter = col2.multiselect("Type", ["EARTHQUAKE", "FLOOD", "FIRE", "STORM", "OTHER"])
    hours_filter = col3.slider("Last N hours", 1, 24, 6)
    events = fetch_events(severity=severity_filter, disaster_type=type_filter, hours=hours_filter)
    df = pd.DataFrame([{
        'timestamp': e['timestamp'],
        'severity': e['severity'],
        'type': e['disaster_type'],
        'location': e['location'],
        'text': e['text']
    } for e in events])
    st.dataframe(df, use_container_width=True, height=400)
