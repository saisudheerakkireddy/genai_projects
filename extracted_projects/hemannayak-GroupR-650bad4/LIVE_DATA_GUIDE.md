# 🔴 Live Data Integration Guide

This guide explains how to integrate real-time disaster tweets into your DisasterLens dashboard.

## 🚀 Quick Start

Run the following command to fetch live disaster tweets from Hyderabad and add them to your dataset:

```bash
./FETCH_LIVE_DATA.sh
```

Then start the application as usual:

```bash
./START.sh
```

## 🔍 What This Does

1. Fetches real public tweets about disasters in Hyderabad from the last 3 days
2. Processes them to extract disaster type and severity
3. Adds them to your existing dataset
4. Makes them available in the dashboard

## 🎛️ Advanced Usage

For more control, you can run the fetch script directly with custom parameters:

```bash
python scripts/fetch_live_tweets.py -l "Mumbai" -n 50 -d 7 -a
```

Parameters:
- `-l, --location`: Location to search for (default: "Hyderabad")
- `-n, --num`: Number of tweets to fetch (default: 30)
- `-d, --days`: Number of days to look back (default: 1)
- `-o, --output`: Output file path (default: "data/raw/live_tweets.csv")
- `-a, --append`: Append to main dataset (flag, no value needed)
- `-m, --main`: Main dataset path (default: "data/raw/disaster_tweets.csv")

## 🌟 Live Data Tab

The application now includes a dedicated "Live Data" tab where you can:

1. Fetch real-time disaster tweets on demand
2. Choose different locations (Hyderabad, Mumbai, Delhi, etc.)
3. View detailed statistics about the live data
4. Add the live data to your main dataset with one click

## ⚙️ How It Works

The integration uses `snscrape`, a Python library that can fetch public tweets without requiring API keys. This makes it perfect for hackathons and demos where you might not have access to official API credentials.

## 🔄 Hybrid Approach

This implementation follows the recommended hybrid approach:
- Generated data provides reliability and consistent demo experience
- Real-time data adds authenticity and "wow factor"
- You control when to fetch new data, avoiding rate limits and API issues

## 🚨 Important Notes

1. Internet connection is required to fetch live data
2. Results depend on recent tweets matching your search criteria
3. For the best demo experience, fetch data shortly before your presentation

## 🏆 Hackathon Tip

During your presentation, mention:
"Our system works with both generated data for reliability AND real-time data streams. Let me show you the LIVE data we just fetched from Hyderabad a few minutes ago..."
