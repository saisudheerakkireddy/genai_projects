# 🔧 SafeAI Setup Guide - Get Your App Fully Working!

## 🎯 Your App is Running at: http://localhost:3000

**Current Status:** ✅ Development server running  
**Next Step:** Configure Supabase to make it fully functional

---

## 📋 Step-by-Step Setup (5 minutes)

### **Step 1: Create Supabase Project**

1. **Go to [supabase.com](https://supabase.com)**
2. **Click "Start your project"**
3. **Sign up/Login with GitHub**
4. **Click "New Project"**
5. **Choose organization and enter project details:**
   - Name: `safeai`
   - Database Password: (create a strong password)
   - Region: Choose closest to you
6. **Click "Create new project"**
7. **Wait 2-3 minutes for setup to complete**

### **Step 2: Get Your Credentials**

1. **In your Supabase dashboard, go to Settings → API**
2. **Copy these two values:**
   - **Project URL** (looks like: `https://xyz.supabase.co`)
   - **anon public** key (long string starting with `eyJ...`)

### **Step 3: Update Environment Variables**

1. **Create a file called `.env.local` in your project root**
2. **Add this content:**
   ```env
   NEXT_PUBLIC_SUPABASE_URL=https://your-project-id.supabase.co
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key_here
   ```
3. **Replace the placeholder values with your actual Supabase credentials**

### **Step 4: Set Up Database**

1. **In Supabase dashboard, go to SQL Editor**
2. **Click "New query"**
3. **Copy the entire contents of `database/schema.sql`**
4. **Paste it in the SQL Editor**
5. **Click "Run" to execute**

### **Step 5: Enable Authentication**

1. **Go to Authentication → Settings**
2. **Enable "Email" provider**
3. **Set Site URL to: `http://localhost:3000`**
4. **Save settings**

### **Step 6: Test Your App**

1. **Refresh your browser at http://localhost:3000**
2. **Click "Create Account"**
3. **Enter email and password**
4. **Check your email for verification link**
5. **Click the verification link**
6. **Login to your app!**

---

## 🎉 What You'll See After Setup

### **✅ Working Features:**
- **Login/Signup** - Create accounts and authenticate
- **Dashboard** - ASTRA branding with feature cards
- **Emergency Button** - SOS functionality
- **Interactive Map** - Real-time location tracking
- **AI Chat** - Safety assistant conversation
- **Profile** - Manage emergency contacts
- **Database** - All data stored securely

### **✅ Pages Available:**
- **Home** (`/`) - Login/signup page
- **Dashboard** (`/dashboard`) - Main features overview
- **Map** (`/map`) - Interactive safety map
- **Chat** (`/chat`) - AI safety agent
- **Profile** (`/profile`) - User settings

---

## 🚀 Quick Test Checklist

After setup, test these features:

- [ ] **Create account** - Sign up with email
- [ ] **Login** - Access dashboard
- [ ] **Emergency button** - Click SOS (shows countdown)
- [ ] **Map** - View interactive map
- [ ] **Chat** - Talk to AI assistant
- [ ] **Profile** - Add emergency contacts
- [ ] **Navigation** - Use navbar to switch pages

---

## 🛠️ Troubleshooting

### **"Missing Supabase environment variables"**
- Check your `.env.local` file exists
- Ensure variables start with `NEXT_PUBLIC_`
- Restart the dev server: `npm run dev`

### **"Authentication failed"**
- Verify Supabase project is active
- Check Site URL in Supabase settings
- Ensure email provider is enabled

### **"Database error"**
- Run the schema.sql in Supabase SQL Editor
- Check RLS policies are enabled

### **"Map not loading"**
- Check browser console for errors
- Ensure location permissions are granted

---

## 📱 Mobile Testing

Your app is fully responsive! Test on:
- **Desktop** - Full feature experience
- **Mobile** - Touch-friendly interface
- **Tablet** - Optimized layout

---

## 🎨 Customization Options

### **Branding:**
- Update team name in `app/layout.js`
- Modify colors in `tailwind.config.js`
- Change logo/watermark

### **Features:**
- Add more emergency contact fields
- Customize AI chat responses
- Add real emergency service integration

---

## 🚀 Ready to Deploy?

Once everything works locally:

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "SafeAI project ready"
   git push origin main
   ```

2. **Deploy to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Import your GitHub repo
   - Add environment variables
   - Deploy!

---

## 🎯 Success Indicators

You'll know everything is working when:
- ✅ Can create and login to accounts
- ✅ Dashboard shows all features
- ✅ Map loads with location
- ✅ Chat responds to messages
- ✅ Profile saves emergency contacts
- ✅ Emergency button works

---

## 📞 Need Help?

- 📖 **Documentation:** README.md
- 🚀 **Deployment:** DEPLOYMENT.md
- 🎯 **Quick Start:** QUICK_START.md
- 📋 **Project Brief:** SafeAI_Project_Brief.txt

---

**ASTRA - Intelligent Safety Beyond Boundaries** 🛡️  
**By Team MINDSHARK**

**Your SafeAI app is ready to save lives! 🚀**
