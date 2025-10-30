# 🚀 START YOUR DEMO NOW!

## ✅ Everything is Ready!

Your simplified working version is complete and ready to run.

## 🎯 Two Ways to Start

### Option 1: Automatic (Easiest)
```bash
cd /Users/hemanth/CascadeProjects/DisasterLens
./QUICK_START.sh
```

### Option 2: Manual (Two Terminals)

**Terminal 1 - Backend:**
```bash
cd /Users/hemanth/CascadeProjects/DisasterLens/backend
python3 main_simple.py
```

Wait for: `✅ Loaded 100 events`

**Terminal 2 - Frontend:**
```bash
cd /Users/hemanth/CascadeProjects/DisasterLens/frontend
streamlit run app_simple.py
```

## 📍 Access Your Dashboard

Browser will auto-open to: **http://localhost:8501**

## ✅ What You'll See

1. **Green Banner**: "🟢 Backend Online | 100 events loaded"
2. **Left Sidebar**: Live statistics with pie charts
3. **Five Tabs**:
   - 🗺️ **Live Map**: Interactive map with colored markers
   - 💬 **Query Assistant**: Ask questions, get answers
   - 🤖 **Agent Decisions**: AI resource allocation
   - 📋 **Situation Report**: Auto-generated reports
   - 🔍 **Event Details**: Filterable event table

## 🧪 Quick Test

1. **Tab 1 (Map)**: See 100 markers on map ✅
2. **Tab 2 (Query)**: 
   - Type "critical situations"
   - Click Search
   - See answer with sources ✅
3. **Tab 3 (Agent)**: See resource allocation decisions ✅
4. **Tab 4 (Report)**: Click "Generate Report" ✅
5. **Tab 5 (Events)**: See filterable table ✅

## 🎬 Demo Queries to Try

- "What are the most critical situations?"
- "Show me earthquake events"
- "Where are floods happening?"
- "What kind of help is needed?"

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill it
kill -9 <PID>
# Try again
python3 backend/main_simple.py
```

### Frontend shows "Backend Offline"
```bash
# Verify backend is running
curl http://localhost:8000/health
# Should return: {"status":"healthy","events":100}
```

### No data showing
```bash
# Regenerate data
python3 scripts/quick_sample.py
```

## 🎉 Success Indicators

✅ Backend console shows: "✅ Loaded 100 events"
✅ Frontend shows: "🟢 Backend Online"
✅ Map displays colored markers
✅ Queries return answers
✅ All tabs work

## ⏱️ Timeline

- **Now**: Start services (2 mins)
- **10:05 PM**: Working demo running
- **10:05-11:00 PM**: Test and polish
- **11:00 PM-12:00 AM**: Record demo video
- **12:00 AM onwards**: Final touches

## 🚀 YOU'RE READY!

Just run the commands above and your demo will be live!

**Say "IT'S WORKING!" when you see the dashboard! 🎯**
