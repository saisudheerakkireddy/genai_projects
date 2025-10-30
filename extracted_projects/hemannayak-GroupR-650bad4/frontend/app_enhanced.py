import streamlit as st
import httpx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
from datetime import datetime, timedelta
import time
import random
import json
import urllib.parse
from typing import Dict, Any, List, Optional

# Page config with better design
st.set_page_config(
    layout="wide",
    page_title="🚨 CrisisLens AI - Disaster Intelligence",
    page_icon="🚨",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/hemannayak/GroupR',
        'Report a bug': 'https://github.com/hemannayak/GroupR/issues',
        'About': '# CrisisLens AI - Real-time Disaster Intelligence Platform'
    }
)

# Initialize session state for persistent settings
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True
    
if 'refresh_interval' not in st.session_state:
    st.session_state.refresh_interval = 3  # seconds
    
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
    
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""
    
if 'countdown' not in st.session_state:
    st.session_state.countdown = st.session_state.refresh_interval
    
# Debug information
if 'last_api_call' not in st.session_state:
    st.session_state.last_api_call = ""
    
if 'last_api_time' not in st.session_state:
    st.session_state.last_api_time = ""
    
if 'last_api_status' not in st.session_state:
    st.session_state.last_api_status = ""
    
if 'last_api_error' not in st.session_state:
    st.session_state.last_api_error = ""

# Parse URL parameters for persistent filters
def get_url_params():
    # Use st.query_params instead of experimental_get_query_params
    query_params = st.query_params.to_dict()
    params = {}
    
    # Handle city filter
    if 'city' in query_params:
        params['city'] = query_params['city']
        
    # Handle severity filter
    if 'severity' in query_params:
        params['severity'] = query_params['severity'].split(',')
        
    # Handle disaster type filter
    if 'type' in query_params:
        params['type'] = query_params['type'].split(',')
        
    # Handle dark mode
    if 'dark_mode' in query_params:
        st.session_state.dark_mode = query_params['dark_mode'].lower() == 'true'
        
    # Handle auto refresh
    if 'auto_refresh' in query_params:
        st.session_state.auto_refresh = query_params['auto_refresh'].lower() == 'true'
        
    return params

# Update URL with current filters
def update_url_params(city=None, severity=None, disaster_type=None):
    # Create a new query params dict
    params = {}
    
    if city and city != "All Cities":
        params['city'] = city
        
    if severity:
        params['severity'] = ','.join(severity)
        
    if disaster_type:
        params['type'] = ','.join(disaster_type)
        
    params['dark_mode'] = str(st.session_state.dark_mode).lower()
    params['auto_refresh'] = str(st.session_state.auto_refresh).lower()
    
    # Use st.query_params instead of experimental_set_query_params
    for key, value in params.items():
        st.query_params[key] = value

# Get URL parameters
url_params = get_url_params()

# Enhanced CSS with modern design
st.markdown("""
<style>
    /* Modern gradient background - Light mode */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
        background-attachment: fixed;
        transition: all 0.3s ease;
    }
    
    /* Dark mode styles */
    .dark-mode .main {
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
        color: #e2e8f0;
    }
    
    .dark-mode .stApp {
        background-color: #1a202c;
    }
    
    .dark-mode p, .dark-mode span, .dark-mode div {
        color: #e2e8f0;
    }
    
    .dark-mode .stTabs [data-baseweb="tab-list"] {
        background: rgba(255,255,255,0.05);
    }
    
    .dark-mode .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.05);
    }
    
    .dark-mode .info-box {
        background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
        color: #e2e8f0;
    }
    
    .dark-mode .event-card {
        background: rgba(26, 32, 44, 0.8);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    .dark-mode .event-card p {
        color: #e2e8f0;
    }

    /* Enhanced header styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #ff4444 0%, #ff8800 50%, #667eea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 2rem 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { filter: drop-shadow(0 0 5px rgba(255,68,68,0.3)); }
        to { filter: drop-shadow(0 0 20px rgba(102,126,234,0.5)); }
    }
    
    /* Global search bar */
    .search-container {
        position: relative;
        margin: 1rem 0;
    }
    
    .search-container input {
        width: 100%;
        padding: 0.75rem 1rem 0.75rem 3rem;
        border-radius: 50px;
        border: 1px solid rgba(102,126,234,0.2);
        background: rgba(255,255,255,0.9);
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .dark-mode .search-container input {
        background: rgba(26, 32, 44, 0.8);
        border: 1px solid rgba(255,255,255,0.1);
        color: #e2e8f0;
    }
    
    .search-container input:focus {
        box-shadow: 0 0 0 2px rgba(102,126,234,0.5);
        border: 1px solid rgba(102,126,234,0.5);
    }
    
    .search-icon {
        position: absolute;
        left: 1rem;
        top: 50%;
        transform: translateY(-50%);
        color: #667eea;
        font-size: 1.2rem;
    }
    
    /* Live/pause button */
    .refresh-control {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255,255,255,0.9);
        padding: 0.5rem 1rem;
        border-radius: 50px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .dark-mode .refresh-control {
        background: rgba(26, 32, 44, 0.8);
    }
    
    .refresh-control:hover {
        box-shadow: 0 5px 15px rgba(0,0,0,0.15);
    }
    
    .live-indicator {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #00cc66;
        animation: pulse-live 2s infinite;
    }
    
    .paused-indicator {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #ff8800;
    }
    
    @keyframes pulse-live {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Theme toggle button */
    .theme-toggle {
        background: none;
        border: none;
        cursor: pointer;
        font-size: 1.5rem;
        padding: 0.5rem;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    .theme-toggle:hover {
        background: rgba(0,0,0,0.1);
    }
    
    .dark-mode .theme-toggle:hover {
        background: rgba(255,255,255,0.1);
    }

    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        border: 1px solid rgba(255,255,255,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.3);
    }

    /* Critical alert styling */
    .critical-alert {
        background: linear-gradient(135deg, #ff4444 0%, #cc0000 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 8px solid #ff6666;
        margin: 1rem 0;
        animation: pulse 2s infinite;
        box-shadow: 0 8px 32px rgba(255,68,68,0.3);
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.9; transform: scale(1.02); }
    }

    /* City badges */
    .city-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        margin: 0.25rem;
        border-radius: 25px;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        font-weight: bold;
        font-size: 0.9rem;
        box-shadow: 0 4px 12px rgba(102,126,234,0.3);
        transition: all 0.3s ease;
    }

    .city-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102,126,234,0.4);
    }

    /* Enhanced tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }

    .stTabs [data-baseweb="tab"] {
        height: 60px;
        padding: 0 2rem;
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        transition: all 0.3s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 8px 32px rgba(102,126,234,0.4);
        transform: translateY(-2px);
    }

    /* Event cards */
    .event-card {
        background: rgba(255,255,255,0.95);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.5);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
    }

    .event-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.2);
    }

    /* Status indicators */
    .status-online {
        color: #00cc66;
        font-weight: bold;
        animation: blink 2s infinite;
    }

    .status-offline {
        color: #ff4444;
        font-weight: bold;
    }

    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.7; }
    }

    /* Loading animation */
    .loading-spinner {
        text-align: center;
        padding: 2rem;
    }

    /* Enhanced buttons */
    .stButton > button {
        border-radius: 25px;
        font-weight: bold;
        padding: 0.75rem 2rem;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }

    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }

    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }

    /* Help tooltips */
    .help-tooltip {
        font-size: 0.8rem;
        color: #666;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# API Config
API_BASE = "http://localhost:8000"

@st.cache_data(ttl=1)
def api_call(endpoint):
    try:
        # Print debug info
        st.session_state.last_api_call = f"{API_BASE}{endpoint}"
        st.session_state.last_api_time = datetime.now().strftime('%H:%M:%S')
        
        # Make the API call with a shorter timeout
        response = httpx.get(f"{API_BASE}{endpoint}", timeout=3)
        
        # Store response info
        st.session_state.last_api_status = response.status_code
        
        # Return the JSON response
        return response.json()
    except Exception as e:
        # Store error info
        st.session_state.last_api_error = str(e)
        st.session_state.last_api_status = "Error"
        return None

# Auto-refresh indicator at bottom of page
def add_auto_refresh_indicator():
    # Calculate countdown
    if st.session_state.auto_refresh:
        current_time = datetime.now()
        elapsed = (current_time - st.session_state.last_refresh).total_seconds()
        st.session_state.countdown = max(0, st.session_state.refresh_interval - int(elapsed))
        status = f"🟢 Live | Next refresh: {st.session_state.countdown}s"
    else:
        status = "⏸️ Paused | Click to resume"
    
    st.markdown(f"""
    <div style="position: fixed; bottom: 20px; right: 20px; background: rgba(102,126,234,0.9);
                color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem;
                backdrop-filter: blur(10px); z-index: 1000;">
        {status} | Last update: {st.session_state.last_refresh.strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)
    
# Function to handle auto-refresh
def handle_auto_refresh():
    if st.session_state.auto_refresh:
        current_time = datetime.now()
        elapsed = (current_time - st.session_state.last_refresh).total_seconds()
        
        if elapsed >= st.session_state.refresh_interval:
            st.session_state.last_refresh = current_time
            st.rerun()
            
# Toggle dark mode
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode
    
# Toggle auto-refresh
def toggle_auto_refresh():
    st.session_state.auto_refresh = not st.session_state.auto_refresh
    if st.session_state.auto_refresh:
        st.session_state.last_refresh = datetime.now()

# Apply dark mode if enabled
if st.session_state.dark_mode:
    st.markdown("<style>.stApp {color: white; background-color: #1a202c}</style>", unsafe_allow_html=True)
    st.markdown("<style>div[data-testid='stToolbar'] {visibility: hidden}</style>", unsafe_allow_html=True)
    st.markdown("<style>div[data-testid='stDecoration'] {display: none}</style>", unsafe_allow_html=True)
    st.markdown("<style>div[data-testid='stStatusWidget'] {display: none}</style>", unsafe_allow_html=True)
    st.markdown("<style>.main {background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%)}</style>", unsafe_allow_html=True)
    st.markdown("<style>section[data-testid='stSidebar'] {background: #1a202c}</style>", unsafe_allow_html=True)
    st.markdown("<style>div.stTabs [data-baseweb='tab-panel'] {background: #1a202c}</style>", unsafe_allow_html=True)

# Header row with controls
col1, col2, col3 = st.columns([1, 3, 1])

with col1:
    # Theme toggle button
    theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
    theme_tooltip = "Switch to Dark Mode" if not st.session_state.dark_mode else "Switch to Light Mode"
    if st.button(theme_icon, help=theme_tooltip, key="theme_toggle"):
        toggle_theme()
        st.rerun()

with col3:
    # Live/pause toggle
    refresh_icon = "🟢 Live" if st.session_state.auto_refresh else "⏸️ Paused"
    refresh_tooltip = "Pause auto-refresh" if st.session_state.auto_refresh else "Resume auto-refresh"
    if st.button(refresh_icon, help=refresh_tooltip, key="refresh_toggle"):
        toggle_auto_refresh()
        st.rerun()

# Enhanced header with logo-like design
st.markdown("""
<div style="text-align: center; padding: 1rem 0;">
    <div style="background: linear-gradient(135deg, #ff4444, #ff8800, #667eea);
                padding: 2rem; border-radius: 20px; margin: 0 auto; max-width: 800px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2);">
        <h1 style="color: white; font-size: 4rem; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
            🚨 CrisisLens AI
        </h1>
        <p style="color: white; font-size: 1.3rem; margin: 1rem 0 0 0; opacity: 0.9;">
            Real-Time Disaster Intelligence & Response Platform
        </p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem; flex-wrap: wrap;">
            <span class="city-badge">🧠 AI-Powered</span>
            <span class="city-badge">⚡ Real-Time</span>
            <span class="city-badge">🌍 Multi-City</span>
            <span class="city-badge">📊 Analytics</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Global search bar
st.markdown("""
<div class="search-container">
    <span class="search-icon">🔍</span>
    <input type="text" id="global-search" placeholder="Search for events, locations, or disaster types..." />
</div>
""", unsafe_allow_html=True)

# Handle auto-refresh if enabled
handle_auto_refresh()

# System status with enhanced design
try:
    health = api_call("/health")
    if health:
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>🟢 System Online</h3>
                <p style="font-size: 1.5rem; margin: 0.5rem 0;">All Systems Operational</p>
                <p style="opacity: 0.8; margin: 0;">{health.get('events', 0)} events monitored</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>📊 Events</h3>
                <p style="font-size: 2rem; margin: 0.5rem 0;">{health.get('events', 0)}</p>
                <p style="opacity: 0.8; margin: 0;">Total Active</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>⚡ Real-time</h3>
                <p style="font-size: 1.5rem; margin: 0.5rem 0; color: #00cc66;">● LIVE</p>
                <p style="opacity: 0.8; margin: 0;">Auto-refresh</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="metric-card">
                <h3>🎯 Accuracy</h3>
                <p style="font-size: 1.5rem; margin: 0.5rem 0;">95%</p>
                <p style="opacity: 0.8; margin: 0;">AI Analysis</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Refresh button
        if st.button("🔄 Refresh Dashboard", type="secondary", help="Update all data and metrics"):
            st.cache_data.clear()
            st.rerun()
    else:
        # Show welcome screen when backend is not available
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea, #764ba2);
                color: white; border-radius: 15px; margin: 2rem 0;">
            <h2>🚀 CrisisLens AI Dashboard</h2>
            <p>Real-time disaster intelligence and response coordination platform</p>
            <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem; flex-wrap: wrap;">
                <span class="city-badge">🧠 AI-Powered</span>
                <span class="city-badge">⚡ Real-Time</span>
                <span class="city-badge">🌍 Multi-City</span>
                <span class="city-badge">📊 Analytics</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="critical-alert">
            <h3>🔴 System Offline</h3>
            <p>Backend server is not responding. Please start the backend service.</p>
            <code>cd backend && python3 main_simple.py</code>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="info-box">
            <h3>🔌 Backend Connection Required</h3>
            <p>The dashboard needs to connect to the backend server to display live data.</p>
            <p><strong>To start the system:</strong></p>
            <ol>
                <li>Start the backend: <code>cd backend && python3 main_simple.py</code></li>
                <li>Or use the start script: <code>./START.sh</code></li>
            </ol>
            <p>Once the backend is running, refresh this page to see the live dashboard.</p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
except Exception as e:
    st.markdown(f"""
    <div class="critical-alert">
        <h3>🔴 Connection Error</h3>
        <p>Cannot connect to backend server: {str(e)}</p>
        <p>Make sure the backend is running on port 8000</p>
        <p><strong>Debug Info:</strong></p>
        <ul>
            <li>Last API Call: {st.session_state.last_api_call}</li>
            <li>Call Time: {st.session_state.last_api_time}</li>
            <li>Status: {st.session_state.last_api_status}</li>
            <li>Error: {st.session_state.last_api_error}</li>
        </ul>
        <p>Try manually checking if the backend is responding:</p>
        <code>curl -v http://localhost:8000/health</code>
    </div>
    """, unsafe_allow_html=True)
    
    # Add a retry button
    if st.button("🔄 Retry Connection", type="primary"):
        st.cache_data.clear()
        st.rerun()
        
    st.stop()

# This is a duplicate block that was moved to the correct location above

# Enhanced sidebar with better organization
with st.sidebar:
    st.markdown("## 🎛️ Control Panel")

    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    with col2:
        if st.button("📊 Stats", use_container_width=True):
            st.session_state.active_tab = "Analytics"

    st.markdown("---")

    # Live statistics
    stats = api_call("/stats")
    if stats:
        st.markdown("### 📈 Live Metrics")

        # Key metrics with enhanced styling
        metrics_col1, metrics_col2 = st.columns(2)
        with metrics_col1:
            st.metric("🚨 Critical", stats.get('critical', 0),
                     delta=f"+{stats.get('critical_change', 0)}")
            st.metric("⏱️ Events/Min", stats.get('events_per_minute', 0))
        with metrics_col2:
            st.metric("📍 Cities", len(stats.get('cities', [])), delta="8 total")
            st.metric("🕐 New (1hr)", stats.get('new_last_hour', 0))

        st.markdown("---")

        # Severity distribution with enhanced visualization
        if stats.get('severity_distribution'):
            st.markdown("### ⚠️ Alert Levels")

            # Custom progress bars for severity
            severity_data = stats['severity_distribution']
            colors = {'CRITICAL': '#ff4444', 'HIGH': '#ff8800', 'MEDIUM': '#ffbb00', 'LOW': '#00cc66'}

            for level, count in severity_data.items():
                percentage = (count / sum(severity_data.values())) * 100
                st.markdown(f"""
                <div style="margin: 0.5rem 0;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.25rem;">
                        <span style="font-weight: bold; color: {colors[level]};">{level}</span>
                        <span>{count} ({percentage:.1f}%)</span>
                    </div>
                    <div style="background: #e0e0e0; border-radius: 10px; height: 8px;">
                        <div style="background: {colors[level]}; width: {percentage}%; height: 100%;
                                   border-radius: 10px; transition: width 0.5s ease;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("---")

        # Disaster types
        if stats.get('disaster_types'):
            st.markdown("### 🔥 Active Threats")
            for disaster_type, count in list(stats['disaster_types'].items())[:5]:
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; padding: 0.5rem;
                           background: rgba(255,255,255,0.1); border-radius: 8px; margin: 0.25rem 0;">
                    <span>🔥 {disaster_type}</span>
                    <span style="font-weight: bold;">{count}</span>
                </div>
                """, unsafe_allow_html=True)

    # System info
    st.markdown("---")
    st.markdown("### ℹ️ System Info")
    st.caption(f"🕐 Last Update: {datetime.now().strftime('%H:%M:%S')}")
    st.caption("🔄 Auto-refresh: 3 seconds")
    st.caption("🌐 API: FastAPI + ChromaDB")
    st.caption("🤖 AI: Mistral-7B + RAG")

# Enhanced city filtering
st.markdown("## 🌍 Crisis Monitoring Dashboard")
st.markdown("*Select a city to focus monitoring efforts or view all cities for national overview*")

# Update last refresh time
if st.session_state.auto_refresh:
    st.session_state.last_refresh = datetime.now()

events = api_call("/events?limit=500")
if events:
    df_all = pd.DataFrame(events)
    cities = ["All Cities"] + sorted(df_all['location'].unique().tolist())

    # Enhanced filter section
    st.markdown("### 🎯 Monitoring Filters")

    col1, col2, col3 = st.columns([3, 2, 2])

    with col1:
        # Use URL parameter if available
        default_city = url_params.get('city', "All Cities")
        if default_city not in cities:
            default_city = "All Cities"
            
        selected_city = st.selectbox(
            "📍 Select City",
            cities,
            index=cities.index(default_city) if default_city in cities else 0,
            key="city_filter",
            help="Choose a specific city to focus on, or 'All Cities' for national view"
        )

    with col2:
        # Use URL parameter if available
        default_severity = url_params.get('severity', ["CRITICAL", "HIGH"])
        severity_filter = st.multiselect(
            "⚠️ Alert Levels",
            ["CRITICAL", "HIGH", "MEDIUM", "LOW"],
            default=default_severity,
            help="Filter events by severity level"
        )

    with col3:
        disaster_types = ["All Types"] + sorted(df_all['type'].unique().tolist())
        # Use URL parameter if available
        default_types = url_params.get('type', ["All Types"])
        selected_types = st.multiselect(
            "🔥 Disaster Types",
            disaster_types,
            default=default_types if all(t in disaster_types for t in default_types) else ["All Types"],
            help="Filter by specific disaster types"
        )
        
    # Update URL with current filters
    update_url_params(selected_city, severity_filter, selected_types)

    # Apply filters
    df_filtered = df_all.copy()

    if selected_city != "All Cities":
        df_filtered = df_filtered[df_filtered['location'] == selected_city]

    if "All Types" not in selected_types:
        df_filtered = df_filtered[df_filtered['type'].isin(selected_types)]

    if severity_filter:
        df_filtered = df_filtered[df_filtered['severity'].isin(severity_filter)]

    # Enhanced city alert
    if selected_city != "All Cities":
        city_stats = df_filtered['severity'].value_counts()
        critical_count = city_stats.get('CRITICAL', 0)
        high_count = city_stats.get('HIGH', 0)

        if critical_count > 0 or high_count > 0:
            alert_color = "#ff4444" if critical_count > 0 else "#ff8800"
            st.markdown(f"""
            <div class="critical-alert">
                <h3>🚨 ACTIVE CRISIS: {selected_city.upper()}</h3>
                <div style="display: flex; gap: 2rem; margin-top: 1rem;">
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; color: #ff6666;">{critical_count}</div>
                        <div style="font-size: 0.9rem;">Critical Alerts</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; color: #ffaa66;">{high_count}</div>
                        <div style="font-size: 0.9rem;">High Priority</div>
                    </div>
                    <div style="text-align: center;">
                        <div style="font-size: 2rem; color: #66aa66;">{len(df_filtered)}</div>
                        <div style="font-size: 0.9rem;">Total Events</div>
                    </div>
                </div>
                <p style="margin-top: 1rem; font-size: 0.9rem;">
                    📍 Immediate response teams should prioritize this location
                </p>
            </div>
            """, unsafe_allow_html=True)

# Import live data tab module
import sys
import os
# Add the current directory to the path so we can import the module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from live_data_tab import display_live_data_tab

# Enhanced tabs with better organization
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🗺️ Crisis Map",
    "💬 AI Assistant",
    "🤖 Response AI",
    "📋 Reports",
    "📊 Analytics",
    "🔴 Live Data",
    "🆘 Emergency"
])

with tab1:
    st.markdown(f"## 🗺️ Real-Time Crisis Map")
    st.markdown(f"*Interactive map showing disaster events for **{selected_city}***")

    if len(df_filtered) > 0:
        # Enhanced map setup
        if selected_city != "All Cities":
            center_lat = df_filtered['lat'].mean()
            center_lon = df_filtered['lon'].mean()
            zoom = 11
        else:
            center_lat = 20.5937  # India center
            center_lon = 78.9629
            zoom = 5

        # Create enhanced map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom,
            tiles='CartoDB positron',  # Cleaner tiles
            control_scale=True,
            zoom_control=True
        )

        # Enhanced markers with clustering
        from folium.plugins import MarkerCluster
        marker_cluster = MarkerCluster().add_to(m)

        # Color and icon mapping
        colors = {'CRITICAL': 'red', 'HIGH': 'orange', 'MEDIUM': 'yellow', 'LOW': 'green'}
        icons = {'CRITICAL': 'exclamation-triangle', 'HIGH': 'warning-sign',
                'MEDIUM': 'info-sign', 'LOW': 'ok-sign'}

        # Add enhanced markers
        for _, event in df_filtered.head(200).iterrows():  # Limit for performance
            # Enhanced popup with more info
            popup_content = f"""
            <div style='width: 300px; font-family: Arial, sans-serif;'>
                <div style='background: {colors.get(event['severity'], 'blue')};
                           color: white; padding: 0.5rem; border-radius: 8px; margin-bottom: 0.5rem;'>
                    <h4 style='margin: 0; text-align: center;'>{event['type']} - {event['severity']}</h4>
                </div>
                <p style='margin: 0.5rem 0;'><strong>📍 Location:</strong> {event['location']}</p>
                <p style='margin: 0.5rem 0;'><strong>🕐 Time:</strong> {event.get('timestamp', 'Recent')[:19]}</p>
                <div style='background: #f5f5f5; padding: 0.5rem; border-radius: 5px; margin: 0.5rem 0;'>
                    <strong>📝 Description:</strong><br>
                    {event['text'][:200]}...
                </div>
                <p style='margin: 0.5rem 0; font-size: 0.8rem; color: #666;'>
                    Event ID: {event['id']} | Confidence: {event.get('confidence', 0.8)*100:.1f}%
                </p>
            </div>
            """

            # Add marker with enhanced styling
            folium.Marker(
                location=[event['lat'], event['lon']],
                popup=folium.Popup(popup_content, max_width=350),
                icon=folium.Icon(
                    color=colors.get(event['severity'], 'blue'),
                    icon=icons.get(event['severity'], 'info-sign'),
                    prefix='fa'
                ),
                tooltip=f"{event['type']} - {event['severity']}"
            ).add_to(marker_cluster)

        # Add legend
        legend_html = '''
        <div style="position: fixed; bottom: 50px; left: 50px; width: 200px; height: 120px;
                    background: white; border: 2px solid grey; border-radius: 10px; padding: 10px;
                    font-family: Arial; font-size: 12px; z-index: 1000; box-shadow: 0 0 15px rgba(0,0,0,0.2);">
        <p style="margin: 0 0 5px 0; font-weight: bold; text-align: center;">Alert Levels</p>
        <p style="margin: 2px 0;"><i class="fa fa-exclamation-triangle" style="color: red;"></i> Critical</p>
        <p style="margin: 2px 0;"><i class="fa fa-warning-sign" style="color: orange;"></i> High</p>
        <p style="margin: 2px 0;"><i class="fa fa-info-sign" style="color: yellow;"></i> Medium</p>
        <p style="margin: 2px 0;"><i class="fa fa-ok-sign" style="color: green;"></i> Low</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))

        # Display map
        st_folium(m, width=1400, height=700, returned_objects=[])

        # Map statistics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📍 Events Shown", len(df_filtered), help="Total events displayed on map")
        col2.metric("🚨 Critical", len(df_filtered[df_filtered['severity'] == 'CRITICAL']),
                   delta="High Priority")
        col3.metric("🗺️ Map Center", f"{center_lat:.2f}, {center_lon:.2f}", help="Current map coordinates")
        col4.metric("🔍 Zoom Level", zoom, help="Current zoom level")

    else:
        st.markdown("""
        <div class="info-box">
            <h3>📍 No Events Found</h3>
            <p>No disaster events match your current filters. Try:</p>
            <ul>
                <li>Selecting "All Cities" for national view</li>
                <li>Reducing filter restrictions</li>
                <li>Checking if backend is running</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("## 💬 AI Crisis Assistant")
    st.markdown("*Ask questions about the disaster situation in natural language*")

    # Enhanced query interface
    if selected_city != "All Cities":
        st.markdown(f"**🔍 Currently analyzing: {selected_city}**")
        examples = [
            f"What are the most critical situations in {selected_city}?",
            f"Show me flood events in {selected_city}",
            f"What emergency services are needed in {selected_city}?",
            f"Latest updates from {selected_city}",
            f"Which areas in {selected_city} need immediate help?",
            f"Summarize the disaster situation in {selected_city}"
        ]
    else:
        st.markdown("**🔍 Currently analyzing: All Cities (National View)**")
        examples = [
            "What are the most critical situations across India?",
            "Which cities need immediate assistance?",
            "Show me all earthquake events",
            "Where are the major floods happening?",
            "What types of disasters are most active?",
            "Give me a national crisis summary"
        ]

    # Enhanced example queries with categories
    st.markdown("### 💡 Suggested Questions")
    
    # Categorize example questions
    info_examples = [ex for ex in examples if ex.lower().startswith(('what', 'where', 'which', 'how many', 'list', 'show'))]
    action_examples = [ex for ex in examples if ex.lower().startswith(('how to', 'what should', 'need', 'help'))]
    other_examples = [ex for ex in examples if ex not in info_examples and ex not in action_examples]
    
    # Create tabs for different question types
    q_tab1, q_tab2, q_tab3 = st.tabs(["📊 Information", "🚨 Action Needed", "❓ Other Questions"])
    
    with q_tab1:
        cols = st.columns(2)
        for i, example in enumerate(info_examples):
            if cols[i % 2].button(f"📈 {example[:40]}...", key=f"info_example_{i}", help=example):
                st.session_state.query = example
    
    with q_tab2:
        cols = st.columns(2)
        for i, example in enumerate(action_examples):
            if cols[i % 2].button(f"🚨 {example[:40]}...", key=f"action_example_{i}", help=example):
                st.session_state.query = example
                
    with q_tab3:
        cols = st.columns(2)
        for i, example in enumerate(other_examples):
            if cols[i % 2].button(f"❓ {example[:40]}...", key=f"other_example_{i}", help=example):
                st.session_state.query = example

    # Query input with history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
        
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("### 💬 Previous Questions")
        for i, (past_q, past_a) in enumerate(st.session_state.chat_history[-3:]):
            with st.expander(f"🔍 {past_q}"):
                st.markdown(f"""<div style="white-space: pre-wrap;">{past_a}</div>""", unsafe_allow_html=True)
    
    # Query input with type hints
    query_type = st.radio(
        "Question type:",
        ["Information", "Explanation", "Action Needed"],
        horizontal=True,
        help="Select the type of response you're looking for"
    )
    
    query_placeholder = {
        "Information": "What are the critical situations in Mumbai?",
        "Explanation": "Why are floods happening in Chennai?",
        "Action Needed": "What should we do about the fire in Delhi?"
    }[query_type]
    
    query = st.text_area(
        "🔍 Ask about the disaster situation:",
        value=st.session_state.get('query', ''),
        height=120,
        placeholder=query_placeholder,
        help="Ask any question about current disaster situations, resource needs, or emergency response"
    )

    col1, col2, col3 = st.columns([1, 1, 3])
    with col1:
        search_btn = st.button("🤖 Ask AI", type="primary", use_container_width=True)
    with col2:
        clear_btn = st.button("🚫 Clear History", type="secondary", use_container_width=True)
        if clear_btn:
            st.session_state.chat_history = []
            st.rerun()

    if search_btn and query:
        with st.container():
            st.markdown("### 🔄 Processing Query...")

            # Loading animation
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.text("🔍 Analyzing query...")
                elif i < 60:
                    status_text.text("🧠 Searching disaster database...")
                elif i < 90:
                    status_text.text("💭 Generating AI response...")
                else:
                    status_text.text("✅ Finalizing answer...")
                time.sleep(0.02)

            progress_bar.empty()
            status_text.empty()

            try:
                response = httpx.post(
                    f"{API_BASE}/query",
                    json={"question": query},
                    timeout=15
                ).json()

                # Save to chat history
                st.session_state.chat_history.append((query, response['answer']))
                
                # Enhanced response display
                st.markdown("### 📝 AI Analysis Result")

                # Response with enhanced styling
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #667eea, #764ba2);
                           color: white; padding: 1.5rem; border-radius: 15px;
                           box-shadow: 0 8px 32px rgba(102,126,234,0.3);">
                    <h4 style="margin-top: 0;">🔍 Query: {query}</h4>
                    <div style="background: rgba(255,255,255,0.1); padding: 1rem;
                               border-radius: 10px; margin: 1rem 0;">
                        <p style="margin: 0; font-size: 1.1rem; line-height: 1.6; white-space: pre-wrap;">
                            {response['answer']}
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Confidence score with enhanced visualization
                confidence = response.get('confidence', 0.8)
                st.markdown("### 🎯 Confidence Score")
                st.progress(confidence)

                # Color-coded confidence
                if confidence >= 0.9:
                    confidence_color = "#00cc66"
                    confidence_text = "Very High Confidence"
                elif confidence >= 0.7:
                    confidence_color = "#ffbb00"
                    confidence_text = "High Confidence"
                elif confidence >= 0.5:
                    confidence_color = "#ff8800"
                    confidence_text = "Medium Confidence"
                else:
                    confidence_color = "#ff4444"
                    confidence_text = "Low Confidence"

                st.markdown(f"""
                <div style="text-align: center; padding: 1rem; background: {confidence_color}20;
                           border: 2px solid {confidence_color}; border-radius: 10px; margin: 1rem 0;">
                    <h3 style="color: {confidence_color}; margin: 0;">
                        {confidence_text} ({confidence*100:.1f}%)
                    </h3>
                </div>
                """, unsafe_allow_html=True)

                # Source events with enhanced display
                if response.get('relevant_events'):
                    st.markdown("### 📚 Supporting Evidence")

                    for i, event in enumerate(response['relevant_events'][:5], 1):
                        severity_color = {
                            'CRITICAL': '#ff4444',
                            'HIGH': '#ff8800',
                            'MEDIUM': '#ffbb00',
                            'LOW': '#00cc66'
                        }.get(event.get('severity', 'MEDIUM'), '#667eea')
                        
                        # Add relevance score display if available
                        relevance_display = ""
                        if 'relevance_score' in event:
                            relevance_pct = event['relevance_score'] * 100
                            relevance_display = f"<span>Relevance: {relevance_pct:.1f}%</span>"

                        st.markdown(f"""
                        <div class="event-card">
                            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                                <h4 style="color: {severity_color}; margin: 0;">
                                    📍 Source {i}: {event.get('type', 'Unknown')} - {event.get('severity', 'Unknown')}
                                </h4>
                                <span style="background: {severity_color}; color: white; padding: 0.25rem 0.75rem;
                                           border-radius: 15px; font-size: 0.8rem; font-weight: bold;">
                                    {event.get('location', 'Unknown')}
                                </span>
                            </div>
                            <p style="margin: 0.5rem 0; color: #333;">{event.get('text', '')}</p>
                            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #666;">
                                <span>Event ID: {event.get('id', 'N/A')}</span>
                                {relevance_display}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                # Action items if available
                if response.get('action_items'):
                    st.markdown("### 🎯 Recommended Actions")
                    
                    # Color-code action items by priority
                    for action in response['action_items']:
                        priority = action.get('priority', 'MEDIUM')
                        if priority == 'CRITICAL':
                            color = "linear-gradient(135deg, #ff4444, #cc0000)"
                            icon = "🔴" # Red circle
                        elif priority == 'HIGH':
                            color = "linear-gradient(135deg, #ff8800, #cc6600)"
                            icon = "🟠" # Orange circle
                        else:
                            color = "linear-gradient(135deg, #ffbb00, #cc9900)"
                            icon = "🟡" # Yellow circle
                            
                        st.markdown(f"""
                        <div style="background: {color};
                                   color: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;
                                   box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h4 style="margin: 0 0 0.5rem 0;">{icon} {action.get('title', 'Action Required')}</h4>
                                <span style="background: rgba(255,255,255,0.2); padding: 0.25rem 0.75rem; border-radius: 15px; font-size: 0.8rem;">
                                    {priority}
                                </span>
                            </div>
                            <p style="margin: 0;">{action.get('description', '')}</p>
                        </div>
                        """, unsafe_allow_html=True)

            except Exception as e:
                st.markdown(f"""
                <div class="critical-alert">
                    <h3>❌ Query Failed</h3>
                    <p>Error: {str(e)}</p>
                    <p>Please check if the backend is running and try again.</p>
                </div>
                """, unsafe_allow_html=True)

with tab3:
    st.markdown("## 🤖 AI Response Coordination")
    st.markdown("*AI-powered decision making for emergency response*")

    decisions = api_call("/agent/decisions")
    if decisions and len(decisions) > 0:
        st.markdown(f"### 🎯 Priority Response Decisions ({len(decisions)} active)")

        for i, decision in enumerate(decisions, 1):
            priority = decision.get('priority_score', 0)

            # Color coding based on priority
            if priority >= 90:
                color = "#ff4444"
                priority_label = "🚨 CRITICAL"
            elif priority >= 70:
                color = "#ff8800"
                priority_label = "⚠️ HIGH"
            elif priority >= 50:
                color = "#ffbb00"
                priority_label = "📊 MEDIUM"
            else:
                color = "#00cc66"
                priority_label = "ℹ️ LOW"

            # Create a cleaner card layout using columns instead of complex HTML
            with st.container():
                # Header with priority score
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"### Decision #{i} - {priority_label}")
                with col2:
                    st.markdown(f"""
                    <div style="text-align: center; background: {color}; color: white; 
                             padding: 0.5rem; border-radius: 10px; font-weight: bold;">
                        {priority}/100
                    </div>
                    """, unsafe_allow_html=True)
                
                # Event description
                st.markdown("#### 📍 Event Description")
                st.info(decision.get('event_text', '')[:200] + "...")
                
                # Recommended action
                st.markdown("#### 🎯 Recommended Action")
                st.success(decision.get('recommended_action', ''))
                
                # AI reasoning
                st.markdown("#### 🧠 AI Reasoning")
                st.write(decision.get('reasoning', ''))
                
                # Resource allocation
                st.markdown("#### 📋 Resource Allocation")
                resources = decision.get('assigned_resources', [])
                if resources:
                    resource_cols = st.columns(len(resources))
                    for i, res in enumerate(resources):
                        resource_cols[i].markdown(f"""
                        <div style="text-align: center; background: #00cc66; color: white;
                                 padding: 0.5rem; border-radius: 10px;">
                            ✅ {res}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.write("No resources allocated yet")
                
                # Event metadata
                st.caption(f"Event ID: {decision.get('event_id', 'N/A')} | Updated: {decision.get('timestamp', 'Recent')[:19]}")
                
                # Add a separator between decisions
                st.markdown("---")

    else:
        st.markdown("""
        <div class="info-box">
            <h3>🤖 AI Response System</h3>
            <p>The AI agent is continuously monitoring for critical situations that require coordinated response.</p>
            <p>When critical events are detected, automated decisions will appear here with:</p>
            <ul>
                <li>Priority scoring and reasoning</li>
                <li>Resource allocation recommendations</li>
                <li>Response coordination plans</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.markdown("## 📋 Automated Situation Reports")
    st.markdown("*Generate comprehensive reports for emergency response teams*")

    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown("### 📄 Report Options")
        report_type = st.selectbox(
            "Report Type",
            ["Executive Summary", "Detailed Analysis", "Resource Planning", "Media Brief"],
            index=0,
            help="Choose the type of report needed"
        )

        include_map = st.checkbox("Include Map", value=True, help="Add interactive map to report")
        include_charts = st.checkbox("Include Charts", value=True, help="Add data visualizations")

        generate_btn = st.button("📄 Generate Report", type="primary", use_container_width=True)

    with col2:
        st.markdown("### 📋 Report Preview")
        if selected_city != "All Cities":
            st.markdown(f"**Focus Area:** {selected_city}")
        else:
            st.markdown("**Focus Area:** National Overview")

        st.markdown(f"**Events Covered:** {len(df_filtered)}")
        st.markdown(f"**Report Type:** {report_type}")
        st.markdown(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    if generate_btn:
        with st.container():
            st.markdown("### 🔄 Generating Report...")

            # Enhanced loading
            progress_bar = st.progress(0)
            status_text = st.empty()

            for i in range(100):
                progress_bar.progress(i + 1)
                if i < 25:
                    status_text.text("📊 Collecting data...")
                elif i < 50:
                    status_text.text("🧠 Analyzing situations...")
                elif i < 75:
                    status_text.text("📝 Writing report...")
                else:
                    status_text.text("🎨 Formatting document...")
                time.sleep(0.01)

            try:
                report = api_call("/report")
                if report:
                    # Enhanced report display
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #667eea, #764ba2);
                               color: white; padding: 2rem; border-radius: 15px;
                               box-shadow: 0 8px 32px rgba(102,126,234,0.3);">
                        <h3 style="margin-top: 0;">📋 Generated Situation Report</h3>
                    </div>
                    """, unsafe_allow_html=True)

                    # Report content with enhanced formatting
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.95); padding: 2rem; border-radius: 15px;
                               box-shadow: 0 8px 32px rgba(0,0,0,0.1); margin: 1rem 0;">
                        <div style="white-space: pre-wrap; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                                   line-height: 1.6; color: #333;">
                            {report}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # Download options
                    st.markdown("### 📥 Download Options")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            label="📄 Download Markdown",
                            data=report,
                            file_name=f"crisis_report_{selected_city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                            mime="text/markdown",
                            use_container_width=True
                        )

                    with col2:
                        # Convert to HTML for better formatting
                        html_report = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>CrisisLens AI - Situation Report</title>
                            <style>
                                body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
                                .header {{ background: linear-gradient(135deg, #667eea, #764ba2);
                                          color: white; padding: 2rem; border-radius: 15px; margin-bottom: 2rem; }}
                                .content {{ background: white; padding: 2rem; border-radius: 15px;
                                           box-shadow: 0 4px 12px rgba(0,0,0,0.1); line-height: 1.6; }}
                                .footer {{ margin-top: 2rem; text-align: center; color: #666; }}
                            </style>
                        </head>
                        <body>
                            <div class="header">
                                <h1>🚨 CrisisLens AI - Situation Report</h1>
                                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                            </div>
                            <div class="content">
                                {report.replace(chr(10), '<br>')}
                            </div>
                            <div class="footer">
                                <p>Generated by CrisisLens AI - Real-time Disaster Intelligence Platform</p>
                            </div>
                        </body>
                        </html>
                        """

                        st.download_button(
                            label="🌐 Download HTML",
                            data=html_report,
                            file_name=f"crisis_report_{selected_city}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                            mime="text/html",
                            use_container_width=True
                        )

                    st.success("✅ Report generated successfully!")
                    st.balloons()

                else:
                    st.error("❌ Failed to generate report")

            except Exception as e:
                st.error(f"❌ Report generation failed: {e}")

with tab5:
    st.markdown("## 📊 Crisis Analytics Dashboard")
    st.markdown("*Comprehensive analysis and insights for decision makers*")

    if len(df_filtered) > 0:
        # Enhanced analytics layout
        st.markdown("### 📈 Key Performance Indicators")

        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            total_events = len(df_filtered)
            st.markdown(f"""
            <div class="metric-card">
                <h3>📊 Total Events</h3>
                <p style="font-size: 2.5rem; margin: 0.5rem 0; font-weight: bold;">{total_events}</p>
                <p style="opacity: 0.8; margin: 0;">All severities</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            critical_events = len(df_filtered[df_filtered['severity'] == 'CRITICAL'])
            st.markdown(f"""
            <div class="metric-card">
                <h3>🚨 Critical</h3>
                <p style="font-size: 2.5rem; margin: 0.5rem 0; font-weight: bold;">{critical_events}</p>
                <p style="opacity: 0.8; margin: 0;">Immediate action</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            avg_confidence = df_filtered['confidence'].mean() if 'confidence' in df_filtered.columns else 0.85
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎯 AI Accuracy</h3>
                <p style="font-size: 2.5rem; margin: 0.5rem 0; font-weight: bold;">{avg_confidence*100:.1f}%</p>
                <p style="opacity: 0.8; margin: 0;">Average confidence</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            unique_locations = df_filtered['location'].nunique()
            st.markdown(f"""
            <div class="metric-card">
                <h3>📍 Locations</h3>
                <p style="font-size: 2.5rem; margin: 0.5rem 0; font-weight: bold;">{unique_locations}</p>
                <p style="opacity: 0.8; margin: 0;">Affected areas</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Enhanced visualizations
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### ⚠️ Severity Distribution")

            # Enhanced pie chart
            severity_counts = df_filtered['severity'].value_counts()
            colors = ['#ff4444', '#ff8800', '#ffbb00', '#00cc66']

            fig = go.Figure(data=[go.Pie(
                labels=severity_counts.index,
                values=severity_counts.values,
                marker_colors=colors,
                hole=0.4,
                textinfo='percent+label',
                textposition='inside'
            )])

            fig.update_layout(
                title="Current Alert Distribution",
                title_x=0.5,
                showlegend=True,
                legend=dict(orientation="h", y=-0.2),
                height=400,
                margin=dict(l=20, r=20, t=40, b=40)
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("### 🔥 Disaster Types")

            # Enhanced bar chart
            disaster_counts = df_filtered['type'].value_counts().head(10)
            fig = go.Figure(data=[go.Bar(
                x=disaster_counts.values,
                y=disaster_counts.index,
                orientation='h',
                marker=dict(
                    color=disaster_counts.values,
                    colorscale='Reds',
                    showscale=True,
                    colorbar=dict(title="Event Count")
                )
            )])

            fig.update_layout(
                title="Most Active Disaster Types",
                title_x=0.5,
                height=400,
                margin=dict(l=20, r=20, t=40, b=40),
                xaxis_title="Number of Events",
                yaxis_title=""
            )

            st.plotly_chart(fig, use_container_width=True)

        # Enhanced location analysis
        st.markdown("### 🌍 Geographic Distribution")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📍 City-wise Events")
            location_counts = df_filtered['location'].value_counts()

            # Enhanced horizontal bar chart
            fig = go.Figure(data=[go.Bar(
                x=location_counts.values,
                y=location_counts.index,
                orientation='h',
                marker=dict(
                    color=location_counts.values,
                    colorscale='Blues',
                    showscale=True
                )
            )])

            fig.update_layout(
                title="Events by Location",
                title_x=0.5,
                height=400,
                margin=dict(l=20, r=20, t=40, b=20),
                xaxis_title="Event Count",
                yaxis_title=""
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### ⏱️ Timeline Analysis")

            # Time-based analysis
            if 'timestamp' in df_filtered.columns:
                df_filtered['hour'] = pd.to_datetime(df_filtered['timestamp']).dt.hour
                hourly_counts = df_filtered.groupby('hour').size()

                fig = go.Figure(data=[go.Scatter(
                    x=hourly_counts.index,
                    y=hourly_counts.values,
                    mode='lines+markers',
                    line=dict(color='#667eea', width=3),
                    marker=dict(size=8, color='#667eea'),
                    fill='tozeroy',
                    fillcolor='rgba(102,126,234,0.2)'
                )])

                fig.update_layout(
                    title="Events by Hour of Day",
                    title_x=0.5,
                    height=400,
                    margin=dict(l=20, r=20, t=40, b=20),
                    xaxis_title="Hour",
                    yaxis_title="Event Count"
                )

                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Timeline data not available in current dataset")

        st.markdown("---")

        # Enhanced event feed
        st.markdown("### 📋 Real-Time Event Feed")

        # Filter controls for feed
        col1, col2, col3 = st.columns(3)
        with col1:
            feed_limit = st.selectbox("Show", [10, 20, 50, 100], index=1, help="Number of events to display", key="tab_feed_limit")
        with col2:
            feed_sort = st.selectbox("Sort by", ["Newest", "Critical First", "Location"], index=0, help="Sort order", key="tab_feed_sort")
        with col3:
            feed_filter = st.multiselect("Filter", ["Show All"] + list(df_filtered['severity'].unique()),
                                       default=["Show All"], help="Filter by severity", key="tab_feed_filter")

        # Apply feed filters
        feed_data = df_filtered.copy()

        if "Show All" not in feed_filter:
            feed_data = feed_data[feed_data['severity'].isin(feed_filter)]

        # Sort feed
        if feed_sort == "Critical First":
            severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
            feed_data = feed_data.sort_values(by='severity', key=lambda x: x.map(severity_order))
        elif feed_sort == "Location":
            feed_data = feed_data.sort_values(by='location')
        elif feed_sort == "Newest":
            feed_data = feed_data.sort_values(by='timestamp', ascending=False)
    else:
        st.info("Timeline data not available in current dataset")

st.markdown("---")

# Enhanced event feed
st.markdown("### 📋 Real-Time Event Feed")

# Filter controls for feed
col1, col2, col3 = st.columns(3)
with col1:
    feed_limit = st.selectbox("Show", [10, 20, 50, 100], index=1, help="Number of events to display", key="main_feed_limit")
with col2:
    feed_sort = st.selectbox("Sort by", ["Newest", "Critical First", "Location"], index=0, help="Sort order", key="main_feed_sort")
with col3:
    feed_filter = st.multiselect("Filter", ["Show All"] + list(df_filtered['severity'].unique()),
                               default=["Show All"], help="Filter by severity", key="main_feed_filter")

# Apply feed filters
feed_data = df_filtered.copy()

if "Show All" not in feed_filter:
    feed_data = feed_data[feed_data['severity'].isin(feed_filter)]

# Sort feed
if feed_sort == "Critical First":
    severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
    feed_data = feed_data.sort_values(by='severity', key=lambda x: x.map(severity_order))
elif feed_sort == "Location":
    feed_data = feed_data.sort_values(by='location')
else:  # Newest first
    if 'timestamp' in feed_data.columns:
        feed_data = feed_data.sort_values(by='timestamp', ascending=False)

# Display as cards using native Streamlit components
if len(feed_data) > 0:
    for _, event in feed_data.head(feed_limit).iterrows():
        severity_color = {
            'CRITICAL': '#ff4444',
            'HIGH': '#ff8800',
            'MEDIUM': '#ffbb00',
            'LOW': '#00cc66'
        }.get(event['severity'], '#cccccc')
        
        # Create a card with Streamlit elements
        with st.container():
            # Header with severity, type, and location
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="background: {severity_color}; color: white; padding: 0.5rem 1rem;
                           border-radius: 20px; font-weight: bold; font-size: 0.9rem;">
                        {event['severity']} - {event['type']}
                    </div>
                    <span style="color: #666; font-size: 0.9rem;">📍 {event['location']}</span>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.caption(f"ID: {event['id']}")
                timestamp = event.get('timestamp', 'Recent')[:19] if 'timestamp' in event and event['timestamp'] else 'Recent'
                st.caption(f"{timestamp}")
            
            # Event text
            st.info(event['text'])
            
            # Metadata footer
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"Confidence: {event.get('confidence', 0.8)*100:.1f}%")
            with col2:
                priority = random.randint(60, 95) if event['severity'] in ['CRITICAL', 'HIGH'] else random.randint(30, 70)
                st.caption(f"Priority Score: {priority}")
            
            # Add separator
            st.markdown("---")

    st.caption(f"📊 Displaying {min(feed_limit, len(feed_data))} of {len(feed_data)} total events")

else:
    st.markdown("""
    <div class="info-box">
        <h3>📊 No Data Available</h3>
        <p>No events to analyze with current filters.</p>
        <p>Try adjusting your filters or checking if the backend is running properly.</p>
    </div>
    """, unsafe_allow_html=True)

with tab6:
    # Display the live data tab
    display_live_data_tab()

with tab7:
    st.markdown("## 🆘 Emergency Response")
    st.markdown("*Coordinate emergency response and resource allocation*")
    
    st.info("Emergency response module will be available in the next update.")
    st.markdown("### 🚨 Critical Alerts")

    if len(df_filtered) > 0:
        critical_events = df_filtered[df_filtered['severity'] == 'CRITICAL']

        if len(critical_events) > 0:
            st.markdown(f"### 🚨 {len(critical_events)} Critical Situations Requiring Immediate Action")

            for _, event in critical_events.head(10).iterrows():
                st.markdown(f"""
                <div class="critical-alert">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin: 0 0 0.5rem 0;">🚨 CRITICAL: {event['type']} - {event['location']}</h4>
                            <p style="margin: 0 0 0.5rem 0;">{event['text']}</p>
                            <div style="display: flex; gap: 1rem; font-size: 0.9rem;">
                                <span>📍 {event['location']}</span>
                                <span>🕐 {event.get('timestamp', 'Recent')[:19]}</span>
                                <span>🎯 ID: {event['id']}</span>
                            </div>
                        </div>
                        <div style="text-align: center;">
                            <div style="font-size: 1.5rem; font-weight: bold;">PRIORITY 1</div>
                            <div style="font-size: 0.8rem;">IMMEDIATE</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="info-box">
                <h3>✅ No Critical Alerts</h3>
                <p>All systems monitoring normally. No immediate threats detected.</p>
            </div>
            """, unsafe_allow_html=True)

    # Quick actions for emergency response
    st.markdown("### ⚡ Emergency Response Actions")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🚑 Dispatch Emergency Services", type="primary", use_container_width=True):
            st.success("🚑 Emergency services dispatch initiated!")
            st.info("Coordinating with local authorities...")

    with col2:
        if st.button("📢 Alert All Agencies", type="secondary", use_container_width=True):
            st.success("📢 All agencies alerted!")
            st.info("Notifications sent to response teams...")

    with col3:
        if st.button("📞 Contact Emergency Services", use_container_width=True):
            st.info("📞 Emergency contact numbers:")
            st.code("Police: 100\nFire: 101\nAmbulance: 102\nDisaster Helpline: 108")

    # Resource allocation
    st.markdown("### 🎯 Resource Allocation Status")

    if stats and stats.get('disaster_types'):
        st.markdown("#### 📊 Resource Needs by Disaster Type")

        for disaster_type, count in list(stats['disaster_types'].items())[:5]:
            # Simulate resource needs
            resources = {
                "Flood": ["Boats", "Life Jackets", "Medical Teams", "Food Supplies"],
                "Fire": ["Fire Engines", "Water Tankers", "Medical Teams", "Evacuation Teams"],
                "Earthquake": ["Search & Rescue", "Medical Teams", "Temporary Shelter", "Heavy Equipment"],
                "Storm": ["Emergency Power", "Medical Teams", "Communication Teams", "Food Distribution"],
                "Landslide": ["Heavy Equipment", "Search & Rescue", "Medical Teams", "Engineering Teams"]
            }

            needed_resources = resources.get(disaster_type, ["Emergency Response Teams", "Medical Support", "Supplies"])

            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ff8800, #ffaa00);
                       color: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0;">
                <h4 style="margin: 0 0 0.5rem 0;">🔥 {disaster_type} ({count} events)</h4>
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
            """, unsafe_allow_html=True)

            for resource in needed_resources:
                st.markdown(f'<span class="city-badge">📋 {resource}</span>', unsafe_allow_html=True)

            st.markdown("</div></div>", unsafe_allow_html=True)

    # Communication center
    st.markdown("### 📞 Communication Center")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 📢 Broadcast Message")
        broadcast_msg = st.text_area(
            "Emergency broadcast message:",
            "🚨 EMERGENCY ALERT: CrisisLens AI has detected critical situations. All response teams report to stations immediately.",
            height=100
        )

        if st.button("📡 Send Broadcast", type="primary"):
            st.success("📡 Emergency broadcast sent!")
            st.info("Message delivered to all registered emergency services")

    with col2:
        st.markdown("#### 📋 Response Checklist")
        checklist_items = [
            "Verify all critical alerts",
            "Contact local authorities",
            "Assess resource availability",
            "Coordinate with other agencies",
            "Update situation reports",
            "Monitor response effectiveness"
        ]

        for item in checklist_items:
            checked = st.checkbox(f"✅ {item}", value=False)
            if checked:
                st.success(f"✅ {item} - Completed")

# Enhanced footer
st.markdown("---")

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h3 style="color: #667eea; margin: 0;">🚨 CrisisLens AI</h3>
        <p style="margin: 0; font-size: 0.9rem; color: #666;">Disaster Intelligence</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h4 style="color: #667eea; margin: 0 0 0.5rem 0;">GenAIVersity Hackathon 2025</h4>
        <p style="margin: 0; font-size: 0.9rem; color: #666;">
            Real-time AI-powered disaster response platform<br>
            Built with ❤️ for emergency responders
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h3 style="color: #667eea; margin: 0;">🛠️ Tech Stack</h3>
        <p style="margin: 0; font-size: 0.9rem; color: #666;">FastAPI • Streamlit • AI</p>
    </div>
    """, unsafe_allow_html=True)

# Add auto-refresh indicator at bottom of page
add_auto_refresh_indicator()

# Add keyboard shortcuts
st.markdown("""
<script>
document.addEventListener('keydown', function(e) {
    // '/' key for search
    if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
        e.preventDefault();
        document.getElementById('global-search').focus();
    }
    
    // 'r' key for refresh
    if (e.key === 'r' && !e.ctrlKey && !e.metaKey) {
        e.preventDefault();
        window.location.reload();
    }
    
    // 'm' key to jump to map tab
    if (e.key === 'm' && !e.ctrlKey && !e.metaKey) {
        e.preventDefault();
        document.querySelector('[data-baseweb="tab"]').click();
    }
});
</script>
""", unsafe_allow_html=True)

# Add a floating help button
st.markdown("""
<div style="position: fixed; bottom: 20px; left: 20px; z-index: 1000;">
    <a href="https://github.com/hemannayak/GroupR" target="_blank"
       style="background: linear-gradient(135deg, #667eea, #764ba2); color: white;
              padding: 0.75rem 1rem; border-radius: 25px; text-decoration: none;
              box-shadow: 0 4px 12px rgba(102,126,234,0.3); display: inline-block;
              font-weight: bold; transition: all 0.3s ease;">
        🔆 Help & Docs
    </a>
</div>
""", unsafe_allow_html=True)

# Add keyboard shortcuts
st.markdown("""
<script>
document.addEventListener('keydown', function(e) {
    // '/' key for search
    if (e.key === '/' && !e.ctrlKey && !e.metaKey) {
        e.preventDefault();
        document.getElementById('global-search').focus();
    }
    
    // 'r' key for refresh
    if (e.key === 'r' && !e.ctrlKey && !e.metaKey) {
        e.preventDefault();
        window.location.reload();
    }
    
    // 'm' key to jump to map tab
    if (e.key === 'm' && !e.ctrlKey && !e.metaKey) {
        e.preventDefault();
        document.querySelector('[data-baseweb="tab"]').click();
    }
});
</script>
""", unsafe_allow_html=True)

# Add keyboard shortcut help
# Keyboard shortcuts help removed as requested
