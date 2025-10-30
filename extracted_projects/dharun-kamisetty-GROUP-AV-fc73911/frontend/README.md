# Arovia Health Desk - Frontend

A beautiful, responsive React frontend for the Arovia Health Desk medical triage application.

## Features

- 🎨 **Modern UI/UX** - Clean, minimalistic design with Tailwind CSS
- 📱 **Responsive Design** - Mobile-first approach, works on all devices
- 🎤 **Voice Input** - Record symptoms in 22 languages
- 📝 **Text Triage** - Detailed symptom analysis
- 🏥 **Facility Search** - Find nearby healthcare centers
- 🤖 **AI Integration** - Real-time medical triage with FastAPI backend
- 🌐 **Multi-language** - Support for major Indian languages

## Tech Stack

- **React 19** - Latest React with TypeScript
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Heroicons** - Beautiful SVG icons
- **Axios** - HTTP client for API calls

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn
- FastAPI backend running on http://localhost:8000

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Open http://localhost:5173 in your browser

### Building for Production

```bash
npm run build
```

## Project Structure

```
src/
├── components/          # React components
│   ├── Header.tsx      # Navigation header
│   ├── Dashboard.tsx   # Main dashboard
│   ├── TriageForm.tsx  # Text input form
│   ├── VoiceInput.tsx  # Voice recording
│   ├── Results.tsx     # Triage results
│   └── Facilities.tsx  # Healthcare facilities
├── types.ts           # TypeScript interfaces
├── App.tsx            # Main app component
├── main.tsx           # App entry point
└── index.css          # Global styles
```

## API Integration

The frontend connects to the FastAPI backend with the following endpoints:

- `POST /triage/text` - Text-based symptom analysis
- `POST /triage/voice` - Voice input processing
- `POST /facilities` - Healthcare facility search
- `GET /languages` - Supported languages
- `GET /health` - System health check

## Features Overview

### Dashboard
- Quick symptom assessment form
- Navigation to different input methods
- Feature highlights and instructions

### Text Triage
- Detailed symptom description
- Location input for facility recommendations
- Example symptom templates

### Voice Input
- Real-time audio recording
- 22 language support
- Recording tips and instructions

### Results
- AI-powered triage analysis
- Urgency scoring and recommendations
- Red flags and potential risks
- Nearby healthcare facilities

### Facilities
- Interactive facility search
- Distance-based sorting
- Contact information and maps
- Service availability

## Styling

The app uses Tailwind CSS with custom components:

- **Primary colors** - Medical blue theme
- **Responsive grid** - Mobile-first design
- **Custom components** - Reusable UI elements
- **Animations** - Smooth transitions and loading states

## Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Code Style

- TypeScript for type safety
- Functional components with hooks
- Custom CSS classes for consistency
- Responsive design patterns

## Deployment

The frontend can be deployed to any static hosting service:

- **Vercel** - Recommended for React apps
- **Netlify** - Easy deployment with Git integration
- **GitHub Pages** - Free hosting for public repos
- **AWS S3** - Scalable static hosting

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details