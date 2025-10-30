# 🔧 Fix Authentication - Step by Step Guide

## 🚨 **Current Issue: "Failed to fetch" Error**

This means Supabase authentication isn't properly configured yet. Follow these steps:

---

## 🎯 **Step 1: Enable Authentication in Supabase**

### **1.1 Go to Your Supabase Project**
1. Open: https://supabase.com/dashboard/project/xvzacfnsitcgxhpyflfu
2. Make sure you're logged into your Supabase account

### **1.2 Enable Email Authentication**
1. Click **"Authentication"** in the left sidebar
2. Click **"Settings"** tab
3. Scroll down to **"Auth Providers"**
4. Find **"Email"** and **toggle it ON**
5. Set **"Site URL"** to: `http://localhost:3000`
6. Click **"Save"**

### **1.3 Verify Project is Active**
1. Go to **"Settings"** → **"General"**
2. Make sure your project status shows **"Active"**
3. If it shows "Paused" or "Inactive", click **"Resume"**

---

## 🎯 **Step 2: Test Your App**

### **2.1 Refresh Your App**
1. Go to http://localhost:3000
2. Refresh the page (Ctrl+F5)
3. You should now see the login form working

### **2.2 Test Registration**
1. Click **"Create Account"**
2. Enter your email and password
3. Click **"Create Account"**
4. Check your email for verification link

---

## 🎯 **Step 3: If Still Not Working**

### **3.1 Check Project Status**
- Make sure your Supabase project is **Active**
- If it's paused, resume it first

### **3.2 Verify Credentials**
- Double-check your `.env.local` file has the correct URL and key
- Restart your development server: `npm run dev`

### **3.3 Check Browser Console**
- Open browser developer tools (F12)
- Look for any error messages in the Console tab

---

## ✅ **Expected Result**

After enabling authentication, you should see:
- ✅ Login form works without "Failed to fetch" error
- ✅ Can create new accounts
- ✅ Can sign in and out
- ✅ Dashboard loads after login

---

## 🆘 **Still Having Issues?**

If you're still getting errors:

1. **Check Supabase Project Status**: Make sure it's active
2. **Verify Email Provider**: Make sure it's enabled
3. **Check Site URL**: Should be `http://localhost:3000`
4. **Restart Server**: Stop and start `npm run dev`

---

## 🎉 **Once Working**

Your SafeAI app will have:
- ✅ Full user authentication
- ✅ Database integration
- ✅ All safety features
- ✅ Emergency SOS system
- ✅ AI chat agent
- ✅ Location tracking

**ASTRA - Intelligent Safety Beyond Boundaries** 🛡️

