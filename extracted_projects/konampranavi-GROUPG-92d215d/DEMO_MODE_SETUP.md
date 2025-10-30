# 🎮 Demo Mode Setup - Test Your App Without Supabase

## 🚨 **Current Issue: Supabase Connection Failed**

Your Supabase project might be paused or there's a network issue. Let's set up a demo mode so you can test your app!

---

## 🎯 **Option 1: Quick Demo Mode (2 minutes)**

### **Step 1: Enable Demo Mode**
1. Open `utils/supabaseClient.js`
2. Find this line: `const hasValidCredentials = supabaseUrl &&`
3. Replace it with: `const hasValidCredentials = true // DEMO MODE`

### **Step 2: Add Demo Auth Functions**
Add these functions to `utils/supabaseClient.js`:

```javascript
// Demo mode functions
export const demoSignIn = async (email, password) => {
  return { 
    data: { 
      user: { 
        id: 'demo-user-123', 
        email: email,
        user_metadata: { name: 'Demo User' }
      } 
    }, 
    error: null 
  }
}

export const demoSignUp = async (email, password) => {
  return { 
    data: { 
      user: { 
        id: 'demo-user-123', 
        email: email,
        user_metadata: { name: 'Demo User' }
      } 
    }, 
    error: null 
  }
}
```

### **Step 3: Update Auth Functions**
Replace the signIn and signUp functions with:

```javascript
export const signIn = async (email, password) => {
  return await demoSignIn(email, password)
}

export const signUp = async (email, password) => {
  return await demoSignUp(email, password)
}
```

---

## 🎯 **Option 2: Create New Supabase Project (5 minutes)**

### **Step 1: Create New Project**
1. Go to https://supabase.com
2. Create a new project
3. Get new URL and anon key
4. Update `.env.local` with new credentials

### **Step 2: Run Database Schema**
1. Copy the schema from `database/schema_simple.sql`
2. Run it in the new project
3. Enable authentication

---

## 🎯 **Option 3: Use Mock Data (1 minute)**

I can create a version that works with mock data for testing.

---

## ✅ **What You'll Get in Demo Mode**

- ✅ Login/signup forms work
- ✅ Dashboard loads
- ✅ All UI components work
- ✅ Navigation between pages
- ❌ No real database (mock data only)
- ❌ No real authentication

---

## 🎉 **Recommendation**

**Try Option 1 (Demo Mode) first** - it's the quickest way to see your app working!

Then we can fix the Supabase issue separately.

**Which option would you like to try?**

