# 🚀 Supabase Setup Guide for SafeAI

## Quick Setup (5 minutes)

### Step 1: Create Supabase Project
1. Go to [https://supabase.com](https://supabase.com)
2. Sign up/Login with your account
3. Click **"New Project"**
4. Fill in project details:
   - **Name**: `safeai-astra`
   - **Database Password**: Generate a strong password (save this!)
   - **Region**: Choose closest to your location
5. Click **"Create new project"**
6. Wait for project to be ready (2-3 minutes)

### Step 2: Get API Credentials
1. In your Supabase dashboard, go to **Settings** → **API**
2. Copy these values:
   - **Project URL** (looks like: `https://abcdefgh.supabase.co`)
   - **anon public** key (long string starting with `eyJ...`)

### Step 3: Update Environment File
1. Open `.env.local` in your project root
2. Replace the placeholder values:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your-actual-anon-key
   ```

### Step 4: Set Up Database
1. In Supabase, go to **SQL Editor**
2. Click **"New Query"**
3. Copy the entire contents of `database/schema.sql`
4. Paste it in the SQL Editor
5. Click **"Run"** to execute the schema

### Step 5: Enable Authentication
1. Go to **Authentication** → **Settings**
2. Under **Auth Providers**, enable **Email**
3. Set **Site URL** to: `http://localhost:3000`
4. Save changes

### Step 6: Test Your App
1. Refresh your browser at `http://localhost:3000`
2. You should now see the login form
3. Try creating an account!

## ✅ What You'll Get

After setup, your SafeAI app will have:
- ✅ User registration and login
- ✅ Dashboard with all features
- ✅ Interactive map with location tracking
- ✅ AI chat agent
- ✅ Profile management
- ✅ Emergency contact system
- ✅ Database integration

## 🆘 Troubleshooting

**"Invalid supabaseUrl" error:**
- Check your `.env.local` file has correct Supabase URL
- Make sure URL starts with `https://` and ends with `.supabase.co`

**"Failed to fetch" error:**
- Verify your Supabase project is active
- Check your anon key is correct
- Restart the development server

**Database errors:**
- Make sure you ran the schema.sql file
- Check all tables were created successfully

## 🎉 Success!

Once configured, you'll have a fully functional SafeAI application ready to save lives!

**ASTRA - Intelligent Safety Beyond Boundaries** 🛡️
