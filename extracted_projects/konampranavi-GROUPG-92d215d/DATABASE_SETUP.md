# 🗄️ Database Setup for SafeAI

## Quick Database Setup (2 minutes)

Your Supabase credentials are now configured! Now you need to set up the database tables.

### Step 1: Open Supabase SQL Editor
1. Go to your Supabase project: https://supabase.com/dashboard/project/xvzacfnsitcgxhpyflfu
2. Click on **"SQL Editor"** in the left sidebar
3. Click **"New Query"**

### Step 2: Run Database Schema
1. Copy the entire contents of `database/schema.sql` from your project
2. Paste it into the SQL Editor
3. Click **"Run"** to execute the schema

### Step 3: Verify Tables Created
You should see these tables created:
- ✅ `users` - User profiles
- ✅ `emergency_contacts` - Emergency contacts
- ✅ `safety_sessions` - Safety tracking sessions
- ✅ `chat_logs` - AI chat history
- ✅ `alerts` - Emergency alerts
- ✅ `location_tracking` - Location data
- ✅ `safe_places` - Nearby safe locations

### Step 4: Enable Authentication
1. Go to **Authentication** → **Settings**
2. Under **Auth Providers**, enable **Email**
3. Set **Site URL** to: `http://localhost:3000`
4. Save changes

### Step 5: Test Your App
1. Go to http://localhost:3000
2. You should now see the login form (no more setup message!)
3. Try creating an account!

## 🎉 Success!

After completing these steps, your SafeAI application will be fully functional with:
- ✅ User registration and login
- ✅ Dashboard with all features
- ✅ Interactive map with location tracking
- ✅ AI chat agent
- ✅ Profile management
- ✅ Emergency contact system
- ✅ Database integration

## 🆘 Need Help?

If you encounter any issues:
1. Make sure you copied the entire `database/schema.sql` file
2. Check that all tables were created successfully
3. Verify authentication is enabled in Supabase
4. Restart your development server if needed

**ASTRA - Intelligent Safety Beyond Boundaries** 🛡️
