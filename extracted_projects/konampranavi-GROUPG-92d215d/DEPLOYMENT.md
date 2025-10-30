# 🚀 SafeAI Deployment Guide

## Quick Start (5 minutes)

### 1. Supabase Setup
1. Go to [supabase.com](https://supabase.com) and create a new project
2. Wait for the project to be ready (2-3 minutes)
3. Go to **Settings → API**
4. Copy your **Project URL** and **anon public** key
5. Update `.env.local` with these values

### 2. Database Setup
1. In your Supabase dashboard, go to **SQL Editor**
2. Copy the entire contents of `database/schema.sql`
3. Paste it in the SQL Editor
4. Click **Run** to execute the schema

### 3. Authentication Setup
1. Go to **Authentication → Settings**
2. Enable **Email** provider
3. Set **Site URL** to `http://localhost:3000` (for development)
4. Save settings

### 4. Run the Application
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) 🎉

---

## Production Deployment

### Option 1: Vercel (Recommended)

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial SafeAI project"
   git push origin main
   ```

2. **Deploy to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repository
   - Add environment variables:
     - `NEXT_PUBLIC_SUPABASE_URL`
     - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - Deploy!

3. **Update Supabase Settings:**
   - Go to Supabase → Authentication → Settings
   - Add your Vercel domain to **Site URL**
   - Add to **Redirect URLs**

### Option 2: Netlify

1. **Build the project:**
   ```bash
   npm run build
   ```

2. **Deploy to Netlify:**
   - Drag the `.next` folder to [netlify.com](https://netlify.com)
   - Or connect your GitHub repository
   - Add environment variables in Netlify dashboard

---

## Environment Variables

### Required
```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### Optional (for email alerts)
```env
EMAILJS_SERVICE_ID=your_emailjs_service_id
EMAILJS_TEMPLATE_ID=your_emailjs_template_id
EMAILJS_PUBLIC_KEY=your_emailjs_public_key
```

---

## Database Schema

The `database/schema.sql` file contains:
- ✅ User management tables
- ✅ Emergency contacts system
- ✅ Safety sessions tracking
- ✅ Chat logs storage
- ✅ Alert system
- ✅ Location tracking
- ✅ Safe places database
- ✅ Row Level Security (RLS) policies
- ✅ Database functions and triggers

---

## Features Checklist

- ✅ **Authentication** - Login/signup with Supabase Auth
- ✅ **Dashboard** - ASTRA branding with feature overview
- ✅ **Profile Management** - User settings and emergency contacts
- ✅ **AI Chat Agent** - Intelligent safety assistant
- ✅ **Interactive Map** - Real-time location with safety zones
- ✅ **Emergency System** - SOS button and alert system
- ✅ **Responsive Design** - Mobile-first approach
- ✅ **Security** - RLS policies and data encryption

---

## Troubleshooting

### Common Issues

1. **"Missing Supabase environment variables"**
   - Check your `.env.local` file
   - Ensure variables start with `NEXT_PUBLIC_`

2. **"Authentication failed"**
   - Verify Supabase project is active
   - Check Site URL in Supabase settings
   - Ensure email provider is enabled

3. **"Database error"**
   - Run the schema.sql in Supabase SQL Editor
   - Check RLS policies are enabled

4. **"Map not loading"**
   - Ensure you're using HTTPS in production
   - Check browser console for errors

### Support

- 📧 Email: support@safeai.com
- 🐛 Issues: Create GitHub issue
- 📖 Docs: Check README.md

---

**ASTRA - Intelligent Safety Beyond Boundaries** 🛡️
**By Team MINDSHARK**
