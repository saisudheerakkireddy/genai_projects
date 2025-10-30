# Firebase Setup Guide for AlgoLeap AI

## Quick Setup Steps

### 1. Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" or select an existing project
3. Follow the setup wizard

### 2. Enable Authentication

1. In your Firebase project, go to **Build** > **Authentication**
2. Click "Get Started"
3. Enable **Email/Password** authentication
4. Click "Save"

### 3. Get Your Firebase Configuration

1. In Firebase Console, click the **gear icon** ⚙️ next to "Project Overview"
2. Select **Project settings**
3. Scroll down to "Your apps" section
4. Click the **Web** icon `</>` to add a web app
5. Register your app (give it a name like "AlgoLeap AI")
6. Copy the configuration values

### 4. Configure Environment Variables

1. Create a `.env` file in your project root (copy from `.env.example`)
2. Fill in your Firebase configuration values:

```env
VITE_FIREBASE_API_KEY=your_api_key_here
VITE_FIREBASE_AUTH_DOMAIN=your_project_id.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project_id.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your_messaging_sender_id
VITE_FIREBASE_APP_ID=your_app_id
```

### 5. Start Your App

```bash
npm install
npm run dev
```

## Features Enabled

✅ Email/Password Authentication
✅ User Sign Up
✅ User Login
✅ Protected Routes
✅ Session Persistence

## Next Steps

To enable AI-powered hints, you'll need to set up Lovable Cloud:
1. Click the Cloud icon in the Lovable editor
2. Enable Lovable Cloud
3. The AI hint system will be ready to use!

## Troubleshooting

**Issue: "Firebase configuration not found"**
- Make sure your `.env` file exists in the project root
- Verify all environment variables are set correctly
- Restart your development server

**Issue: "Cannot sign up users"**
- Check that Email/Password authentication is enabled in Firebase Console
- Verify your Firebase project settings

**Issue: "Unauthorized domain"**
- In Firebase Console, go to Authentication > Settings > Authorized domains
- Add your development domain (e.g., `localhost`)
