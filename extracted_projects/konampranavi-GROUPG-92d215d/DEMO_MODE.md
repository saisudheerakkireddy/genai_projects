# 🎮 Demo Mode - SafeAI Without Supabase

## Quick Demo Setup

If you want to see the SafeAI application in action without setting up Supabase, you can use demo mode:

### Option 1: View UI Only
1. Open `http://localhost:3000` in your browser
2. You'll see a helpful setup message with instructions
3. The app will show you exactly what to do

### Option 2: Mock Authentication (Advanced)
If you want to test the full UI without Supabase, you can temporarily modify the app:

1. **Edit `utils/supabaseClient.js`**:
   ```javascript
   // Add this at the top after imports
   const DEMO_MODE = true; // Set to true for demo mode
   
   // Replace the hasValidCredentials check with:
   const hasValidCredentials = DEMO_MODE || (supabaseUrl && 
     supabaseAnonKey && 
     supabaseUrl !== 'https://placeholder.supabase.co' && 
     supabaseAnonKey !== 'placeholder-key' &&
     supabaseUrl.startsWith('https://') &&
     supabaseUrl.includes('.supabase.co'))
   ```

2. **Add demo auth functions**:
   ```javascript
   // Add these demo functions
   export const demoSignIn = async (email, password) => {
     return { 
       data: { 
         user: { 
           id: 'demo-user', 
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
           id: 'demo-user', 
           email: email,
           user_metadata: { name: 'Demo User' }
         } 
       }, 
       error: null 
     }
   }
   ```

3. **Update auth functions to use demo mode**:
   ```javascript
   export const signIn = async (email, password) => {
     if (DEMO_MODE) {
       return await demoSignIn(email, password)
     }
     // ... rest of function
   }
   ```

## 🎯 What You Can Demo

Even without Supabase, you can see:
- ✅ Beautiful ASTRA login page
- ✅ Responsive design
- ✅ UI components and layout
- ✅ Navigation between pages
- ✅ Form interactions
- ✅ Loading states and animations

## 🚀 For Full Functionality

To get the complete SafeAI experience with:
- Real user authentication
- Database storage
- AI chat functionality
- Location tracking
- Emergency features

Follow the **SUPABASE_SETUP.md** guide (5 minutes).

## 🛡️ ASTRA - Intelligent Safety Beyond Boundaries

**By Team MINDSHARK**

Your SafeAI project is ready to demonstrate its potential! 🚀
