# SafeAI - Intelligent Safety Beyond Boundaries

A comprehensive women's safety application with AI-powered features, real-time location sharing, and emergency response systems.

## 🏗️ Project Structure

```
safeai/
├── safeai-frontend/        # Next.js Frontend Application
│   ├── app/               # Pages and UI components
│   ├── components/        # Reusable React components
│   ├── utils/             # Frontend utilities and API client
│   └── package.json       # Frontend dependencies
├── safeai-backend/         # Node.js Backend API
│   ├── src/               # Server and main files
│   ├── routes/            # API route handlers
│   ├── database/          # Database schemas
│   └── package.json       # Backend dependencies
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Start the Backend API

```bash
cd safeai-backend
npm install
npm run dev
```

The backend will run on [http://localhost:5000](http://localhost:5000)

### 2. Start the Frontend Application

```bash
cd safeai-frontend
npm install
npm run dev
```

The frontend will run on [http://localhost:3000](http://localhost:3000)

## 🎯 Features

### Frontend (React/Next.js)
- **Interactive Dashboard** - Feature overview and navigation
- **AI Chat Assistant** - Natural language safety commands
- **Interactive Map** - Real-time location sharing and safety sessions
- **Emergency System** - SOS alerts and emergency contacts
- **Profile Management** - User settings and contact management
- **Route Planning** - AI-powered safe route recommendations

### Backend (Node.js/Express)
- **RESTful API** - Complete API for all frontend features
- **Authentication** - User login/registration system
- **Emergency Alerts** - Emergency response system
- **Location Services** - Location sharing and tracking
- **Safety Sessions** - Safety monitoring and check-ins
- **User Management** - Profile and contact management

## 🔧 Technology Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **React 18** - UI library
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Beautiful icons
- **Axios** - HTTP client for API calls
- **Leaflet** - Interactive maps

### Backend
- **Node.js** - JavaScript runtime
- **Express.js** - Web application framework
- **CORS** - Cross-origin resource sharing
- **Helmet** - Security middleware
- **Rate Limiting** - API protection
- **Supabase** - Database and authentication

## 📱 Interactive Features

### AI Chat Assistant
- Natural language processing
- Safety command recognition
- Emergency alert triggers
- Location sharing commands
- Safety session management

### Interactive Map
- Real-time GPS location
- Safety session controls
- Location sharing with timers
- Emergency alert system
- Nearby safe places

### Emergency System
- One-click SOS alerts
- Automatic contact notification
- Location sharing with authorities
- Real-time status updates

## 🔗 API Communication

The frontend communicates with the backend through RESTful APIs:

- **Authentication**: `/api/auth/*`
- **Users**: `/api/users/*`
- **Emergency**: `/api/emergency/*`
- **Location**: `/api/location/*`
- **Safety**: `/api/safety/*`

## 🛡️ Security Features

- **CORS Protection** - Configured for frontend domain
- **Rate Limiting** - API protection against abuse
- **Input Validation** - Request validation
- **Error Handling** - Centralized error management
- **Security Headers** - Helmet middleware

## 🚀 Deployment

### Frontend Deployment
```bash
cd safeai-frontend
npm run build
npm start
```

### Backend Deployment
```bash
cd safeai-backend
npm start
```

## 📋 Environment Setup

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:5000/api
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_key
```

### Backend (.env)
```
NODE_ENV=development
PORT=5000
FRONTEND_URL=http://localhost:3000
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_key
```

## 👥 Team MINDSHARK

- **Konam Pranavi**
- **Janigala Vignesh Kumar**
- **Gouroju Shiva Ganesh**
- **Mamidi Indhu**

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

**SafeAI - Empowering women with intelligent safety solutions** 🛡️