import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { 
  DocumentTextIcon, 
  MicrophoneIcon, 
  MapPinIcon, 
  HeartIcon,
  ClockIcon,
  ShieldCheckIcon
} from '@heroicons/react/24/outline';

interface DashboardProps {
  onTriageSubmit: (symptoms: string, location?: string) => void;
  onVoiceSubmit: (audioBlob: Blob, language: string) => void;
  loading: boolean;
  error: string | null;
}

const Dashboard: React.FC<DashboardProps> = ({ onTriageSubmit, onVoiceSubmit, loading, error }) => {
  const [symptoms, setSymptoms] = useState('');
  const [location, setLocation] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (symptoms.trim()) {
      onTriageSubmit(symptoms.trim(), location.trim() || undefined);
    }
  };

  const quickActions = [
    {
      title: 'Text Triage',
      description: 'Describe your symptoms in text',
      icon: DocumentTextIcon,
      href: '/triage',
      color: 'bg-blue-500',
    },
    {
      title: 'Voice Input',
      description: 'Speak your symptoms in 22 languages',
      icon: MicrophoneIcon,
      href: '/voice',
      color: 'bg-green-500',
    },
    {
      title: 'Find Facilities',
      description: 'Locate nearby healthcare centers',
      icon: MapPinIcon,
      href: '/facilities',
      color: 'bg-purple-500',
    },
  ];

  return (
    <div className="max-w-6xl mx-auto">
      {/* Hero Section */}
      <div className="text-center mb-12">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-6">
          <HeartIcon className="w-8 h-8 text-primary-600" />
        </div>
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          AI-Powered Health Triage
        </h1>
        <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
          Get instant medical assessment and find nearby healthcare facilities. 
          Our AI analyzes your symptoms and provides personalized recommendations.
        </p>
      </div>

      {/* Quick Assessment Form */}
      <div className="card mb-12">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6">Quick Assessment</h2>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label htmlFor="symptoms" className="block text-sm font-medium text-gray-700 mb-2">
              Describe your symptoms
            </label>
            <textarea
              id="symptoms"
              value={symptoms}
              onChange={(e) => setSymptoms(e.target.value)}
              placeholder="Example: I have chest pain and shortness of breath for the past hour..."
              className="input-field h-32 resize-none"
              required
            />
          </div>
          
          <div>
            <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
              Your location (optional)
            </label>
            <input
              type="text"
              id="location"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
              placeholder="City, State (e.g., Mumbai, Maharashtra)"
              className="input-field"
            />
          </div>

          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <p className="text-red-800">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={loading || !symptoms.trim()}
            className="btn-primary w-full disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="flex items-center justify-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Analyzing...
              </div>
            ) : (
              'Analyze Symptoms'
            )}
          </button>
        </form>
      </div>

      {/* Quick Actions */}
      <div className="grid md:grid-cols-3 gap-6 mb-12">
        {quickActions.map((action) => (
          <Link
            key={action.title}
            to={action.href}
            className="card hover:shadow-md transition-shadow duration-200 group"
          >
            <div className={`w-12 h-12 ${action.color} rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-200`}>
              <action.icon className="w-6 h-6 text-white" />
            </div>
            <h3 className="text-lg font-semibold text-gray-900 mb-2">{action.title}</h3>
            <p className="text-gray-600">{action.description}</p>
          </Link>
        ))}
      </div>

      {/* Features */}
      <div className="grid md:grid-cols-3 gap-8">
        <div className="text-center">
          <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <ClockIcon className="w-6 h-6 text-green-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Instant Analysis</h3>
          <p className="text-gray-600">Get AI-powered medical triage in seconds</p>
        </div>
        
        <div className="text-center">
          <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <MicrophoneIcon className="w-6 h-6 text-blue-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">22 Languages</h3>
          <p className="text-gray-600">Voice input in major Indian languages</p>
        </div>
        
        <div className="text-center">
          <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mx-auto mb-4">
            <ShieldCheckIcon className="w-6 h-6 text-purple-600" />
          </div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Secure & Private</h3>
          <p className="text-gray-600">Your health data is protected and secure</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
