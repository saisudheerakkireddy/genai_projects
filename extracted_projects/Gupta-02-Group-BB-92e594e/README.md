# 🚀 HireFlow – Intelligent AI-Powered Hiring Platform

> **Revolutionizing recruitment through GenAI automation and intelligent candidate assessment**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Made with React](https://img.shields.io/badge/Frontend-React+TypeScript-blue?logo=react)](https://reactjs.org/)
[![Node.js Backend](https://img.shields.io/badge/Backend-Node.js+Express-green?logo=node.js)](https://nodejs.org/)
[![AI Powered](https://img.shields.io/badge/AI-Google%20Gemini-orange?logo=google)](https://ai.google.dev/)
[![Database](https://img.shields.io/badge/Database-MongoDB-green?logo=mongodb)](https://www.mongodb.com/)

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900"> 

## 📋 Abstract

**HireFlow** is a next-generation recruitment platform that harnesses the power of generative AI to streamline and accelerate the hiring process. Designed for modern HR professionals, recruiters, and organizations of all sizes, HireFlow automates critical hiring workflows—from job posting creation to candidate evaluation, interview scheduling, and AI-powered assessments.

The platform leverages **Google Gemini AI** to intelligently evaluate resumes, generate interview questions, assess candidate responses, and facilitate coding assessments. By combining a responsive React frontend with a robust Node.js/Python backend, HireFlow delivers a seamless experience that reduces hiring cycles from weeks to days while ensuring data-driven hiring decisions.

**Key Innovation**: An intelligent pipeline that automatically scores candidates, conducts AI-powered Q&A interviews, evaluates coding submissions, and provides actionable hiring recommendations—all without manual intervention.

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900"> 

## Video 




https://github.com/user-attachments/assets/3f0ae61d-ce92-43e5-95d0-b4b049f2e0f0


## ✨ Key Features

🎯 **AI-Powered Candidate Scoring** - Automatic resume evaluation and candidate ranking  
🗣️ **Intelligent Interview Agent** - AI-driven Q&A and technical assessments  
📧 **Automated Workflows** - Email notifications, interview invitations, and status updates  
💻 **Coding Assessment** - Real-time code evaluation with AI feedback  
📊 **HR Dashboard** - Comprehensive metrics and candidate pipeline visualization  
🔐 **Secure Resume Handling** - PDF parsing and encrypted data storage  
⚡ **Real-time Updates** - WebSocket-ready architecture for live notifications  
🎨 **Modern UI** - Responsive design with Shadcn UI components  

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900"> 

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     HIREFLOW ECOSYSTEM                          │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────────────┐
                    │   CLIENT LAYER       │
                    │  (React + TypeScript)│
                    │  - HR Dashboard      │
                    │  - Candidate Portal  │
                    │  - Interview Module  │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │  API GATEWAY / CORS  │
                    └──────────┬───────────┘
                               │
            ┌──────────────────┼──────────────────┐
            │                  │                  │
    ┌───────▼────────┐  ┌──────▼────────┐  ┌─────▼──────────┐
    │  NODE.JS API   │  │  PYTHON       │  │  EXTERNAL      │
    │  (Express.js)  │  │  MICROSERVICE │  │  SERVICES      │
    │                │  │  (Flask)      │  │                │
    │ ✓ Job Routes   │  │               │  │ • Google       │
    │ ✓ Application  │  │ ✓ Job         │  │   Gemini API   │
    │   Management   │  │   Processing  │  │ • Gmail SMTP   │
    │ ✓ Interview    │  │ ✓ AI          │  │ • MongoDB      │
    │   Pipeline     │  │   Evaluation  │  │                │
    │ ✓ File Upload  │  │               │  │                │
    └───────┬────────┘  └──────┬────────┘  └─────────────────┘
            │                  │
            └──────────────────┼─────────────────┐
                               │                 │
                    ┌──────────▼──────────┐      │
                    │   MONGODB           │      │
                    │   DATABASE          │      │
                    │                     │      │
                    │ Collections:        │      │
                    │ • Jobs              │      │
                    │ • Applications      │      │
                    │ • Interviews        │      │
                    │ • Responses         │      │
                    └─────────────────────┘      │
                                                 │
                                    ┌────────────▼──────┐
                                    │  NOTIFICATION     │
                                    │  SERVICE          │
                                    │  (Email/SMS)      │
                                    └───────────────────┘
```

---

## 🔄 Workflow & Process Flow

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    RECRUITMENT WORKFLOW                                  │
└──────────────────────────────────────────────────────────────────────────┘

STAGE 1: JOB POSTING
────────────────────
    HR Admin
       │
       ├─→ Log in to HR Dashboard
       │
       ├─→ Fill Job Form
       │   • Title, Description
       │   • Requirements, Salary
       │   • Location, Job Type
       │
       ├─→ Submit Job Posting
       │
       └─→ Job Published ✓
           (Available on Candidate Portal)


STAGE 2: CANDIDATE APPLICATION
───────────────────────────────
    Candidate
       │
       ├─→ Browse Job Listings
       │
       ├─→ Click "Apply Now"
       │
       ├─→ Fill Application Form
       │   • Personal Info (Name, Email, Phone)
       │   • Cover Letter
       │   • Resume Upload (PDF)
       │
       ├─→ System: PDF → Text Extraction
       │
       └─→ Application Submitted ✓


STAGE 3: AI EVALUATION
──────────────────────
    Backend System
       │
       ├─→ Parse Resume (PDF → Text)
       │
       ├─→ Call Google Gemini API
       │   • Analyze Resume Content
       │   • Extract Key Skills
       │   • Match with Job Requirements
       │
       ├─→ Generate AI Score (0-100)
       │   Based on:
       │   • Skill Match
       │   • Experience Level
       │   • Education Background
       │   • Relevance to Role
       │
       ├─→ Store Application + Score in MongoDB
       │
       └─→ Evaluation Complete ✓


STAGE 4: INTERVIEW SCHEDULING
──────────────────────────────
    HR Admin
       │
       ├─→ View Candidate Scores
       │   (in HR Dashboard)
       │
       ├─→ Select Top Candidates
       │
       ├─→ Click "Send Interview Invite"
       │
       ├─→ System Sends Email
       │   • Interview Details
       │   • Calendar Link
       │   • Instructions
       │
       ├─→ Update Status: "invited" ✓
       │
       └─→ Candidate Receives Email


STAGE 5: AI INTERVIEW ASSESSMENT
─────────────────────────────────
    Candidate
       │
       ├─→ Click Interview Link
       │
       ├─→ Start Interview Module
       │
       │   ┌─ Q&A ASSESSMENT ──────────┐
       │   │ • AI generates 5-7         │
       │   │   behavioral questions     │
       │   │ • Candidate answers each   │
       │   │ • AI scores responses      │
       │   │ • Real-time feedback       │
       │   └────────────────────────────┘
       │
       │   ┌─ CODING ASSESSMENT ───────┐
       │   │ • Programming challenge    │
       │   │ • Code editor (Ace.js)     │
       │   │ • Multiple language support│
       │   │ • AI evaluates solution    │
       │   │ • Provides detailed review │
       │   └────────────────────────────┘
       │
       │   ┌─ EVALUATION SUMMARY ──────┐
       │   │ • Overall Interview Score  │
       │   │ • Question-wise Analysis   │
       │   │ • Coding Assessment Result │
       │   │ • Strengths & Weaknesses   │
       │   └────────────────────────────┘
       │
       └─→ Interview Completed ✓


STAGE 6: FINAL DECISION
───────────────────────
    HR Admin
       │
       ├─→ Review Interview Results
       │
       ├─→ Analyze Combined Scores
       │   • Resume Score (Stage 3)
       │   • Interview Score (Stage 5)
       │   • Coding Score (if applicable)
       │
       ├─→ Make Hiring Decision
       │   • Accept / Reject / Hold
       │   • Add Decision Notes
       │
       ├─→ Send Final Email
       │   • Outcome Notification
       │   • Next Steps
       │   • HR Contact Info
       │
       ├─→ Update Status: "completed" ✓
       │
       └─→ Candidate Notified


┌──────────────────────────────────────────────────────────────────────────┐
│  TIMELINE: Job Posted → Candidate Applied → AI Scored → Interviewed     │
│            → Evaluated → Hired (Avg. 3-5 days vs. 3-4 weeks manually)    │
└──────────────────────────────────────────────────────────────────────────┘
```


## WorkFlow Cycle

<img width="660" height="585" alt="image" src="https://github.com/user-attachments/assets/249cf245-39bb-47eb-82ed-c29df677bfb2" />


<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900"> 

## 📁 Project Structure

```
hireflow/
├── 📦 backend-hiring-AI/
│   ├── index.js                    # Express.js main server
│   ├── jobpostingserver.py         # Flask microservice
│   ├── package.json                # Node dependencies
│   ├── env                         # Environment variables
│   └── env-1                       # Backup env config
│
├── 🎨 Frontend/
│   ├── 📂 src/
│   │   ├── 📄 App.tsx              # Main app component with routing
│   │   ├── 📄 main.tsx             # React entry point
│   │   ├── 📄 index.css            # Global styles
│   │   ├── 📂 components/
│   │   │   ├── 📄 JobForm.tsx      # Job creation form
│   │   │   └── 📂 ui/              # Shadcn UI components (20+ components)
│   │   ├── 📂 pages/
│   │   │   ├── 📄 Home.tsx         # Landing page
│   │   │   ├── 📄 HRDashboard.tsx  # HR management dashboard
│   │   │   ├── 📄 ApplyJob.tsx     # Job application page
│   │   │   ├── 📄 Interview.tsx    # AI interview module
│   │   │   ├── 📄 ViewCandidates.tsx  # Candidate list
│   │   │   ├── 📄 CandidatePortal.tsx # Candidate portal
│   │   │   ├── 📄 Support.tsx      # Support page
│   │   │   └── 📄 NotFound.tsx     # 404 page
│   │   ├── 📂 hooks/
│   │   │   ├── 📄 use-toast.ts     # Toast notifications
│   │   │   └── 📄 use-mobile.tsx   # Responsive design
│   │   └── 📂 lib/
│   │       └── 📄 utils.ts         # Utility functions
│   │
│   ├── vite.config.ts              # Vite configuration
│   ├── tailwind.config.ts          # Tailwind CSS config
│   ├── tsconfig.json               # TypeScript config
│   ├── package.json                # React dependencies
│   └── index.html                  # HTML entry point
│
├── 📄 README.md                    # This file
└── 📄 hacktoday.code-workspace     # VS Code workspace
```

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900"> 

## 🛠️ Technology Stack

### **Frontend**
- ⚛️ **React 18** - UI library with hooks
- 🎯 **TypeScript** - Type-safe development
- ⚡ **Vite** - Lightning-fast build tool & dev server
- 🎨 **Tailwind CSS** - Utility-first CSS framework
- 🧩 **Shadcn UI** - Beautiful, accessible component library
- 🪝 **React Router** - Client-side routing
- 📡 **TanStack Query** - Server state management
- 💬 **React Hook Form** - Efficient form handling
- ✏️ **Ace Editor** - Code editing (for coding assessments)

### **Backend**
- 🟢 **Node.js + Express.js** - HTTP API server
- 🐍 **Python + Flask** - AI processing microservice
- 📦 **MongoDB** - NoSQL document database
- 🤖 **Google Generative AI (Gemini 1.5 Flash)** - AI model for evaluations
- 📧 **Nodemailer** - Email sending service
- 📑 **pdf-parse** - PDF text extraction
- 🔐 **CORS** - Cross-origin resource sharing
- 📤 **Multer** - File upload handling
- 🔑 **UUID** - Unique identifier generation
- 🔐 **Dotenv** - Environment variable management

### **Deployment & DevOps**
- 🐳 **Docker** - Containerization (optional)
- 🗄️ **MongoDB Atlas** - Cloud database
- ☁️ **Vercel/Netlify** - Frontend hosting
- ☁️ **Render/Railway** - Backend hosting

---

## ⚙️ Getting Started

### Prerequisites
- **Node.js** (v16 or higher)
- **Python** (v3.8 or higher)
- **MongoDB** (local or Atlas cloud instance)
- **Google Gemini API Key** (free tier available)
- **Gmail Account** (for email notifications)

### 1. Clone the Repository

```bash
git clone https://github.com/shravankumar8/hireflow.git
cd hireflow
```

### 2. Backend Setup

```bash
cd backend-hiring-AI

# Install Node dependencies
npm install

# Create .env file
cp env .env

# Add your credentials
echo "GEMINI_API_KEY=your_gemini_api_key_here" >> .env
echo "EMAIL_USER=your_gmail@gmail.com" >> .env
echo "EMAIL_PASS=your_app_password_here" >> .env
echo "MONGO_URI=mongodb://localhost:27017/recruiter_db" >> .env

# Install Python dependencies
pip install flask pymongo

# Start backend servers
node index.js          # Terminal 1
python jobpostingserver.py  # Terminal 2
```

### 3. Frontend Setup

```bash
cd Frontend

# Install React dependencies
npm install

# Create .env file (if needed)
echo "VITE_API_URL=http://localhost:5000" >> .env

# Start development server
npm run dev
```

### 4. Access the Application

- 🏠 **Home**: http://localhost:8080
- 👨‍💼 **HR Dashboard**: http://localhost:8080/hr
- 👤 **Candidate Portal**: http://localhost:8080/candidates
- 💼 **Job Application**: http://localhost:8080/apply/:jobId
- 🎤 **Interview Module**: http://localhost:8080/interview/:candidateId/:jobId

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900"> 

## 📚 API Documentation

### **Job Management**

#### Create Job
```http
POST /jobs
Content-Type: application/json

{
  "title": "Senior React Developer",
  "company": "TechCorp",
  "location": "San Francisco, CA",
  "type": "full-time",
  "salary": "$120,000 - $150,000",
  "description": "...",
  "requirements": "..."
}

Response: { "jobId": "uuid", "status": "created" }
```

#### Get All Jobs
```http
GET /jobs
Response: { "jobs": [...] }
```

#### Get Single Job
```http
GET /jobs/:jobId
Response: { "job": {...} }
```

### **Application Management**

#### Submit Application
```http
POST /jobs/:jobId/apply
Content-Type: multipart/form-data

name=John&email=john@example.com&resume=<file>&coverLetter=...

Response: { "score": 85, "candidateId": "uuid" }
```

#### Get Candidates for Job
```http
GET /jobs/:jobId/applications
Response: { "candidates": [...], "metrics": {...} }
```

### **Interview Management**

#### Send Interview Invite
```http
POST /jobs/:jobId/applications/:candidateId/invite
Content-Type: application/json

{
  "interviewDate": "2025-01-15T10:00:00Z",
  "method": "email"
}

Response: { "status": "invite_sent" }
```

#### Submit Interview Response
```http
POST /jobs/:jobId/applications/:candidateId/submit-interview
Content-Type: application/json

{
  "responses": [
    { "question": "...", "answer": "..." },
    { "question": "...", "answer": "..." }
  ],
  "codingSubmission": { "code": "...", "language": "javascript" }
}

Response: { "score": 88, "feedback": "..." }
```

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900"> 

## 🤖 AI Features

### **Resume Evaluation**
- **Automatic Parsing**: Extracts text from PDF resumes
- **Skill Extraction**: Identifies technical and soft skills
- **Job Matching**: Compares candidate skills with job requirements
- **Scoring**: Generates 0-100 score based on relevance

### **Interview Generation**
- **Dynamic Questions**: AI generates 5-7 behavioral/technical questions
- **Context-Aware**: Questions tailored to job requirements
- **Progressive Difficulty**: Questions increase in complexity
- **Real-time Feedback**: Immediate AI scoring of responses

### **Coding Assessment**
- **Challenge Generation**: AI creates programming problems
- **Code Evaluation**: Analyzes solution correctness, efficiency, code quality
- **Language Support**: JavaScript, Python, Java, C++, etc.
- **Detailed Feedback**: Suggestions for improvement

### **Hiring Recommendation**
- **Multi-Factor Analysis**: Combines resume, interview, and coding scores
- **Decision Support**: Provides recommendations (Strong Accept/Accept/Hold/Reject)
- **Reasoning**: Explains the decision based on collected data
- **Calendar Integration**: Links to HR scheduling tools

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900"> 

## 🔐 Environment Variables

```env
# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Email Configuration (Gmail)
EMAIL_USER=your_gmail@gmail.com
EMAIL_PASS=your_app_password_here

# Database
MONGO_URI=mongodb://username:password@localhost:27017/recruiter_db

# Server Configuration (Optional)
NODE_PORT=5000
PYTHON_PORT=5000
FRONTEND_PORT=8080
```

### How to Get These Credentials

**Google Gemini API Key**:
1. Go to https://ai.google.dev/
2. Click "Get started" → "Get API key in Google Cloud Console"
3. Create a new project, enable Gemini API
4. Copy your API key

**Gmail App Password**:
1. Enable 2-Factor Authentication on your Google Account
2. Go to myaccount.google.com → Security
3. Find "App passwords" and generate one
4. Use this password (not your regular password)

**MongoDB Connection**:


<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900"> 

## 🚀 Features Showcase

### 📊 HR Dashboard
- **Job Analytics**: Overview of all active job postings
- **Candidate Metrics**: Application count, average scores
- **Pipeline Visualization**: See candidates at each stage
- **Quick Actions**: Create jobs, send invites, view candidates
- **Search & Filter**: Find candidates by skills, scores, or status

### 🎤 Interview Module
- **Multi-Stage Assessment**:
  - ✅ Resume Review
  - ✅ AI Q&A Interview
  - ✅ Coding Challenge
  - ✅ Final Evaluation
- **Live Code Editor**: Syntax highlighting, multiple languages
- **Real-time Scoring**: Instant feedback on submissions
- **Interview Recording**: Store responses for HR review

### 💼 Candidate Experience
- **Simple Application**: Intuitive form with resume upload
- **Interview Preparation**: Clear instructions and guidelines
- **Progress Tracking**: See application status at each stage
- **Feedback**: Receive detailed evaluation results


<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900"> 

## 📈 Performance Metrics

| Metric | Before HireFlow | With HireFlow |
|--------|-----------------|---------------|
| Time to Hire | 21-28 days | 3-5 days |
| Resume Screening | 2-3 hours per job | <5 minutes |
| Interview Scheduling | 1-2 days | Instant |
| Evaluation Time | 1-2 weeks | Real-time |
| Cost per Hire | $3,000-$5,000 | <$500 |
| Candidate Quality | Manual bias | Data-driven |

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900"> 

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Style
- Use **TypeScript** for type safety
- Follow **ESLint** rules
- Write meaningful commit messages
- Add comments for complex logic
- Test before submitting PR

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900"> 

## 🐛 Troubleshooting

### MongoDB Connection Issues
```bash
# Check if MongoDB is running
mongosh

# If not installed, use MongoDB Atlas (cloud)
# Update MONGO_URI in .env
```

### Gemini API Errors
```
Error: GEMINI_API_KEY not found
→ Make sure API key is added to .env file
→ Verify key is active in Google Cloud Console
```

### Email Not Sending
```
Error: Failed to send email
→ Enable 2FA on Google Account
→ Use App Password (not regular password)
→ Check if Gmail SMTP is enabled
```

### Port Already in Use
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9

# Or use different port
NODE_PORT=5001 npm start
```

---

## 📝 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

---

## 👥 Team & Attribution

**Created by**: Gupta-02  
**Inspired by**: Modern recruitment industry challenges  
**Built with**: Open-source technologies and community support

---

## 📞 Support & Contact

- 📧 **Email**: support@hireflow.io
- 💬 **Discord**: [Join Community](https://discord.gg/hireflow)
- 🐙 **GitHub Issues**: [Report Bugs](https://github.com/Gupta-02/hireflow/issues)
- 📖 **Documentation**: [Full Docs](https://docs.hireflow.io)


<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900"> 

## 🎯 Roadmap (Future Enhancements)

- 🎙️ **Voice Interview**: Real-time voice Q&A with AI
- 📹 **Video Recording**: Video interview capabilities
- 🔗 **ATS Integration**: Connect with existing ATS systems
- 📊 **Analytics Dashboard**: Advanced reporting and insights
- 🌐 **Multi-Language**: Support for 20+ languages
- 🤖 **Advanced ML Models**: Predictive hiring analytics
- ⚡ **WebSocket**: Real-time notifications
- 🔐 **2FA & SSO**: Enhanced security features
- 📱 **Mobile App**: Native iOS/Android applications

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900"> 

## ⭐ Show Your Support

If you find HireFlow useful, please consider:
- ⭐ Starring the repository
- 🔀 Sharing with your network
- 💬 Providing feedback and suggestions
- 🤝 Contributing to the project

<img src="https://user-images.githubusercontent.com/74038190/212284100-561aa473-3905-4a80-b561-0d28506553ee.gif" width="900"> 

<div align="center">

**Transform Your Hiring Process Today!**

[🌐 Website](https://hireflow.io) • [📖 Docs](https://docs.hireflow.io) • [💼 LinkedIn](https://linkedin.com) • [🐙 GitHub](https://github.com/Gupta-02/hireflow)

</div>
