import streamlit as st
import pandas as pd
import subprocess
import os
import sys
from datetime import datetime, timedelta
import time

def fetch_live_tweets(location="Hyderabad", max_results=20, days=1, append=False):
    """Run the fetch_live_tweets.py script to get real-time tweets"""
    try:
        # Build command arguments
        cmd = [
            sys.executable, 
            "scripts/fetch_live_tweets.py",  # Path relative to project root
            "-l", location,
            "-n", str(max_results),
            "-d", str(days),
            "-o", "data/raw/live_tweets.csv"
        ]
        
        # Add append flag if requested
        if append:
            cmd.append("-a")
        
        # Show spinner while fetching
        with st.spinner(f"Fetching live tweets for {location}..."):
            # Run the script
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )
            
            # Capture output
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                st.error(f"Error fetching tweets: {stderr}")
                return None
            
            # Load the fetched tweets
            if os.path.exists("data/raw/live_tweets.csv"):
                return pd.read_csv("data/raw/live_tweets.csv")
            else:
                st.warning("No tweets were fetched")
                return None
    except Exception as e:
        st.error(f"Error running tweet fetcher: {str(e)}")
        return None

def display_live_data_tab():
    """Display the Live Data tab in the Streamlit app"""
    st.markdown("""
    <div style="text-align: center; padding: 1rem 0;">
        <div style="background: linear-gradient(135deg, #ff4444, #ff8800, #667eea);
                padding: 1.5rem; border-radius: 20px; margin: 0 auto; max-width: 800px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.2);">
            <h1 style="color: white; font-size: 2.5rem; margin: 0; text-shadow: 0 2px 4px rgba(0,0,0,0.3);">
                🔴 LIVE Data Integration
            </h1>
            <p style="color: white; font-size: 1.1rem; margin: 0.5rem 0 0 0; opacity: 0.9;">
                Real-Time Disaster Tweets from Hyderabad
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Explanation
    st.markdown("""
    This tab demonstrates real-time data integration with live tweets about disasters in Hyderabad.
    Unlike the generated data in the main dashboard, these tweets are fetched from public sources in real-time.
    """)
    
    # Control panel
    st.markdown("### 🎛️ Live Data Controls")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        location = st.selectbox(
            "📍 Location",
            ["Hyderabad", "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata"],
            index=0
        )
    
    with col2:
        max_results = st.slider("📊 Number of tweets", 5, 50, 20)
    
    with col3:
        days_back = st.slider("🕒 Days to look back", 1, 7, 1)
    
    # Action buttons
    col1, col2 = st.columns(2)
    
    with col1:
        fetch_button = st.button("🔄 Fetch Live Tweets", type="primary", use_container_width=True)
    
    with col2:
        append_button = st.button("➕ Fetch & Add to Main Dataset", type="secondary", use_container_width=True)
    
    # Process button clicks
    if fetch_button:
        df = fetch_live_tweets(location, max_results, days_back, append=False)
        if df is not None and not df.empty:
            st.session_state.live_tweets_df = df
            st.session_state.last_fetch_time = datetime.now()
            st.success(f"✅ Successfully fetched {len(df)} tweets!")
    
    if append_button:
        df = fetch_live_tweets(location, max_results, days_back, append=True)
        if df is not None and not df.empty:
            st.session_state.live_tweets_df = df
            st.session_state.last_fetch_time = datetime.now()
            st.success(f"✅ Successfully fetched and added {len(df)} tweets to the main dataset!")
            st.info("Refresh the main dashboard to see the integrated data.")
    
    # Display fetched tweets if available
    if "live_tweets_df" in st.session_state and not st.session_state.live_tweets_df.empty:
        df = st.session_state.live_tweets_df
        
        # Show fetch time
        if "last_fetch_time" in st.session_state:
            st.caption(f"Last updated: {st.session_state.last_fetch_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Display stats
        st.markdown("### 📊 Live Data Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Tweets", len(df))
        
        with col2:
            severity_counts = df["severity"].value_counts()
            critical_count = severity_counts.get("CRITICAL", 0)
            st.metric("Critical Alerts", critical_count)
        
        with col3:
            keyword_counts = df["keyword"].value_counts()
            most_common = keyword_counts.index[0] if not keyword_counts.empty else "N/A"
            st.metric("Most Common Event", most_common)
        
        # Display keyword distribution
        st.markdown("### 🔍 Event Type Distribution")
        
        if "keyword" in df.columns:
            keyword_df = df["keyword"].value_counts().reset_index()
            keyword_df.columns = ["Event Type", "Count"]
            
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.dataframe(keyword_df, use_container_width=True)
            
            with col2:
                st.bar_chart(keyword_df.set_index("Event Type"))
        
        # Display severity distribution
        st.markdown("### ⚠️ Severity Distribution")
        
        if "severity" in df.columns:
            severity_df = df["severity"].value_counts().reset_index()
            severity_df.columns = ["Severity", "Count"]
            
            # Ensure consistent order
            severity_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW"]
            severity_df["Severity"] = pd.Categorical(severity_df["Severity"], categories=severity_order, ordered=True)
            severity_df = severity_df.sort_values("Severity")
            
            col1, col2 = st.columns([2, 3])
            
            with col1:
                st.dataframe(severity_df, use_container_width=True)
            
            with col2:
                st.bar_chart(severity_df.set_index("Severity"))
        
        # Display the tweets
        st.markdown("### 📱 Live Disaster Tweets")
        
        # Create tabs for different views
        tab1, tab2 = st.tabs(["Card View", "Table View"])
        
        with tab1:
            # Card view of tweets
            for i, row in df.iterrows():
                severity_color = {
                    "CRITICAL": "#ff4444",
                    "HIGH": "#ff8800",
                    "MEDIUM": "#ffbb00",
                    "LOW": "#00cc66"
                }.get(row.get("severity", "LOW"), "#00cc66")
                
                st.markdown(f"""
                <div style="border: 1px solid rgba(0,0,0,0.1); border-left: 5px solid {severity_color}; 
                           border-radius: 10px; padding: 1rem; margin-bottom: 1rem; 
                           background: white; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
                        <span style="font-weight: bold; color: {severity_color};">
                            {row.get("severity", "UNKNOWN")} - {row.get("keyword", "unknown").upper()}
                        </span>
                        <span style="color: #666; font-size: 0.8rem;">
                            {row.get("timestamp", "")[:16].replace("T", " ")}
                        </span>
                    </div>
                    <p style="margin: 0.5rem 0;">{row["text"]}</p>
                    <div style="display: flex; justify-content: space-between; margin-top: 0.5rem;">
                        <span style="color: #666; font-size: 0.8rem;">📍 {row["location"]}</span>
                        <span style="color: #666; font-size: 0.8rem;">ID: {row["id"]}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        with tab2:
            # Table view
            st.dataframe(
                df[["id", "keyword", "location", "text", "severity", "timestamp"]],
                use_container_width=True,
                column_config={
                    "id": "ID",
                    "keyword": "Event Type",
                    "location": "Location",
                    "text": "Tweet Content",
                    "severity": "Severity",
                    "timestamp": "Time"
                }
            )
    else:
        # No tweets fetched yet
        st.info("👆 Click 'Fetch Live Tweets' to get real-time disaster data from Hyderabad")
        
        # Placeholder image
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: rgba(0,0,0,0.03); 
                   border-radius: 10px; margin: 1rem 0;">
            <img src="https://cdn-icons-png.flaticon.com/512/1251/1251681.png" 
                 style="width: 100px; opacity: 0.5;">
            <p style="color: #666; margin-top: 1rem;">No live data available yet</p>
        </div>
        """, unsafe_allow_html=True)

# For testing the module directly
if __name__ == "__main__":
    st.set_page_config(page_title="Live Data Test", layout="wide")
    display_live_data_tab()
