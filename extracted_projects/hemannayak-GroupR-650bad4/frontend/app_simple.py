import streamlit as st
import httpx
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from datetime import datetime

st.set_page_config(layout="wide", page_title="🚨 CrisisLens AI", page_icon="🚨")

# API Config
API_BASE = "http://localhost:8000"

def api_call(endpoint):
    try:
        response = httpx.get(f"{API_BASE}{endpoint}", timeout=5)
        return response.json()
    except Exception as e:
        return None

# Header
st.title("🚨 CrisisLens AI - Real-Time Disaster Intelligence")
st.markdown("*AI-Powered Crisis Response Coordination System*")

# Check backend
try:
    health = api_call("/health")
    if health:
        st.success(f"🟢 Backend Online | {health.get('events', 0)} events loaded")
    else:
        st.error("🔴 Backend Offline")
        st.info("Start backend: `cd backend && python main_simple.py`")
        st.stop()
except:
    st.error("🔴 Cannot connect to backend")
    st.info("Start backend: `cd backend && python main_simple.py`")
    st.stop()

# Sidebar Stats
with st.sidebar:
    st.header("📊 Live Statistics")
    
    stats = api_call("/stats")
    if stats:
        col1, col2 = st.columns(2)
        col1.metric("Total Events", stats.get('total_events', 0))
        col2.metric("Critical", stats.get('critical', 0), delta=stats.get('critical_change', 0))
        
        # Severity pie chart
        if stats.get('severity_distribution'):
            fig = px.pie(
                values=list(stats['severity_distribution'].values()),
                names=list(stats['severity_distribution'].keys()),
                title="Severity Distribution",
                color_discrete_map={'CRITICAL': 'red', 'HIGH': 'orange', 'MEDIUM': 'yellow', 'LOW': 'green'}
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Type bar chart
        if stats.get('disaster_types'):
            fig = px.bar(
                x=list(stats['disaster_types'].keys()),
                y=list(stats['disaster_types'].values()),
                title="Disaster Types",
                labels={'x': 'Type', 'y': 'Count'},
                color=list(stats['disaster_types'].values()),
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)

# Main Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🗺️ Live Map", "💬 Query Assistant", "🤖 Agent Decisions", "📋 Situation Report", "🔍 Event Details"])

with tab1:
    st.header("Real-Time Crisis Map")
    
    events = api_call("/events/map-data")
    if events:
        # Create map
        m = folium.Map(location=[19.0760, 72.8777], zoom_start=8)
        
        # Color map for severity
        colors = {
            'CRITICAL': 'red',
            'HIGH': 'orange',
            'MEDIUM': 'yellow',
            'LOW': 'green'
        }
        
        # Add markers
        for event in events[:50]:  # Show first 50
            folium.Marker(
                location=[event['lat'], event['lon']],
                popup=f"<b>{event['type']}</b><br>Severity: {event['severity']}<br>{event['text'][:100]}...",
                icon=folium.Icon(color=colors.get(event['severity'], 'blue'), icon='info-sign')
            ).add_to(m)
        
        # Display map
        st_folium(m, width=1400, height=600)
        
        st.markdown("**Legend:** 🔴 Critical | 🟠 High | 🟡 Medium | 🟢 Low")
    else:
        st.warning("No map data available")

with tab2:
    st.header("AI Query Assistant")
    
    examples = st.selectbox("Try examples:", [
        "Custom query...",
        "What are the most critical situations?",
        "Show me earthquake events",
        "Where are floods happening?",
        "What kind of help is needed?"
    ])
    
    query = st.text_input("Ask about the situation:", 
                          value="" if examples == "Custom query..." else examples)
    
    if st.button("🔍 Search", type="primary"):
        if query:
            with st.spinner("Analyzing..."):
                try:
                    response = httpx.post(
                        f"{API_BASE}/query",
                        json={"question": query},
                        timeout=10
                    ).json()
                    
                    # Display answer
                    st.markdown("### 📝 Answer")
                    st.info(response['answer'])
                    
                    # Confidence
                    st.progress(response['confidence'])
                    st.caption(f"Confidence: {response['confidence']*100:.1f}%")
                    
                    # Sources
                    if response.get('relevant_events'):
                        st.markdown("### 📚 Sources")
                        for i, tweet in enumerate(response['relevant_events'][:3], 1):
                            with st.expander(f"Source {i}: {tweet['type']} - {tweet['severity']}"):
                                st.write(tweet['text'])
                                st.caption(f"Location: {tweet['location']}")
                except Exception as e:
                    st.error(f"Query failed: {e}")

with tab3:
    st.header("🤖 AI Agent Decisions & Resource Allocation")
    
    decisions = api_call("/agent/decisions")
    if decisions:
        for decision in decisions:
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f'<div style="background-color: #ff4444; color: white; padding: 10px; border-radius: 5px;">', unsafe_allow_html=True)
                    st.markdown(f"**Priority Score: {decision.get('priority_score', 0)}/100**")
                    st.markdown(f"Event: {decision.get('event_text', '')[:100]}...")
                    st.markdown(f"**Reasoning:** {decision.get('reasoning', '')}")
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col2:
                    st.metric("Resources Assigned", len(decision.get('assigned_resources', [])))
                    for res in decision.get('assigned_resources', []):
                        st.caption(f"✓ {res}")
                
                st.markdown("---")
    else:
        st.info("No agent decisions available")

with tab4:
    st.header("📋 Automated Situation Report")
    
    if st.button("Generate Report", type="primary"):
        with st.spinner("Generating comprehensive report..."):
            try:
                report = api_call("/report")
                if report:
                    st.markdown(report)
                    
                    # Download button
                    st.download_button(
                        label="📥 Download Report",
                        data=report,
                        file_name=f"crisis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
            except Exception as e:
                st.error(f"Report generation failed: {e}")

with tab5:
    st.header("🔍 Recent Events")
    
    events = api_call("/events?limit=50")
    if events:
        # Create DataFrame
        df = pd.DataFrame(events)
        
        # Filters
        col1, col2 = st.columns(2)
        severity_filter = col1.multiselect("Filter by Severity", 
                                          df['severity'].unique(),
                                          default=list(df['severity'].unique()))
        type_filter = col2.multiselect("Filter by Type",
                                       df['type'].unique(),
                                       default=list(df['type'].unique()))
        
        # Apply filters
        filtered_df = df[
            (df['severity'].isin(severity_filter)) &
            (df['type'].isin(type_filter))
        ]
        
        # Display
        st.dataframe(
            filtered_df[['timestamp', 'severity', 'type', 'location', 'text']],
            use_container_width=True,
            height=400
        )
        
        st.caption(f"Showing {len(filtered_df)} of {len(df)} events")
    else:
        st.warning("No events available")

# Footer
st.markdown("---")
st.markdown("**CrisisLens AI** | Built for GenAIVersity Hackathon 2025 | Powered by HuggingFace")
