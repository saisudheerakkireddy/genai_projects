"use client"
import { SignIn } from '@clerk/nextjs'
import { Logo } from "@/components/common/logo"
import { LanguageToggle } from "@/components/language/language-toggle"
import { useRouter } from "next/navigation"
import { useLanguage } from "@/components/language/language-provider"

export default function AuthPage() {
  const router = useRouter()
  const { t } = useLanguage()

  return (
    <div className="min-h-screen relative overflow-hidden bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-slate-800 dark:to-indigo-900">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden">
        {/* Floating gradient orbs */}
        <div className="absolute top-1/4 left-1/4 w-72 h-72 bg-gradient-to-r from-blue-400/20 to-indigo-400/20 rounded-full filter blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-gradient-to-r from-purple-400/20 to-pink-400/20 rounded-full filter blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-gradient-to-r from-cyan-400/20 to-blue-400/20 rounded-full filter blur-3xl animate-pulse delay-500"></div>
        
        {/* Subtle grid pattern */}
        <div className="absolute inset-0 opacity-[0.02]">
          <svg width="100%" height="100%" className="absolute inset-0">
            <defs>
              <pattern id="grid" width="60" height="60" patternUnits="userSpaceOnUse">
                <path d="M 60 0 L 0 0 0 60" fill="none" stroke="currentColor" strokeWidth="1"/>
              </pattern>
            </defs>
            <rect width="100%" height="100%" fill="url(#grid)" className="text-blue-600" />
          </svg>
        </div>
        
        {/* Floating particles */}
        <div className="absolute inset-0">
          {[...Array(6)].map((_, i) => (
            <div
              key={i}
              className="absolute w-2 h-2 bg-blue-400/30 rounded-full animate-bounce"
              style={{
                left: `${10 + (i * 15)}%`,
                top: `${20 + (i * 10)}%`,
                animationDelay: `${i * 0.5}s`,
                animationDuration: `${2 + (i * 0.5)}s`
              }}
            />
          ))}
        </div>
      </div>
      {/* Back Button */}
      <button
        onClick={() => router.push("/")}
        className="absolute top-4 left-4 z-20 flex items-center px-3 py-1.5 rounded-md bg-white/80 dark:bg-slate-800/80 border border-gray-200 dark:border-gray-700 shadow hover:bg-blue-50 dark:hover:bg-blue-900/30 transition-colors"
      >
        <svg className="h-5 w-5 mr-2" fill="none" stroke="currentColor" strokeWidth="2" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        <span className="font-medium text-gray-700 dark:text-gray-200">Back</span>
      </button>
      
      {/* Header */}
      <div className="relative z-10 text-center pt-8 mb-8">
        <div className="flex justify-between items-center mx-4 sm:mx-20 mb-8">
          <Logo size="lg" className="text-gray-900 dark:text-white" isLanding={false} />
          <LanguageToggle />
        </div>
        <div className="max-w-2xl mx-auto px-4">
          <h1 className="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-gray-900 via-blue-900 to-indigo-900 dark:from-white dark:via-blue-100 dark:to-indigo-100 bg-clip-text text-transparent mb-4">
            Welcome to CareConnect
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400 leading-relaxed">
            Sign in to access your personalized healthcare dashboard
          </p>
          <div className="mt-4 flex items-center justify-center space-x-2">
            <div className="w-12 h-0.5 bg-gradient-to-r from-transparent to-blue-500"></div>
            <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
            <div className="w-12 h-0.5 bg-gradient-to-l from-transparent to-blue-500"></div>
          </div>
        </div>
      </div>

      {/* Clerk Sign In Component */}
      <div className="relative z-10 flex justify-center items-center min-h-[50vh] px-4">
        <div className="relative">
          {/* Glow effect behind the card */}
          <div className="absolute inset-0 bg-gradient-to-r from-blue-600/20 via-indigo-600/20 to-purple-600/20 rounded-3xl blur-2xl scale-105"></div>
          
          <SignIn 
          appearance={{
            baseTheme: undefined,
            variables: {
              colorPrimary: '#3b82f6',
              colorBackground: 'transparent',
              colorInputBackground: 'rgba(255, 255, 255, 0.9)',
              colorInputText: '#1f2937',
              colorText: '#374151',
              colorTextSecondary: '#6b7280',
              colorDanger: '#ef4444',
              colorSuccess: '#10b981',
              colorWarning: '#f59e0b',
              borderRadius: '1rem',
              fontFamily: 'Inter, system-ui, sans-serif',
              fontSize: '0.875rem',
              spacingUnit: '0.75rem'
            },
            elements: {
              // Enhanced glassmorphism card design
              card: 'relative bg-white/10 backdrop-blur-2xl border border-white/20 shadow-2xl shadow-black/5 rounded-3xl p-6 max-w-md w-full overflow-hidden before:absolute before:inset-0 before:rounded-3xl before:bg-gradient-to-br before:from-white/20 before:to-white/5 before:border before:border-white/20 before:-z-10',
              
              // Header with better contrast and logo styling
              headerTitle: 'hidden',
              headerSubtitle: 'hidden',
              logoImage: 'h-24 w-auto mx-auto mb-2 relative z-10 rounded-full mt-4 border border-white/30 shadow-lg',
              logoBox: 'text-center mb-2 relative z-10',
              
              // Form elements with glassmorphism
              formFieldLabel: 'text-sm font-semibold text-gray-700 mb-1 block relative z-10',
              formFieldInput: 'w-full px-4 py-3 bg-white/80 backdrop-blur-sm border border-white/30 rounded-2xl text-gray-900 placeholder:text-gray-500 focus:border-blue-400 focus:ring-4 focus:ring-blue-400/20 transition-all duration-300 shadow-lg focus:shadow-xl focus:bg-white/90 hover:bg-white/85 relative z-10',
              formFieldInputShowPasswordButton: 'text-gray-500 hover:text-gray-700 relative z-10',
              
              // Enhanced primary button
              formButtonPrimary: 'w-full relative overflow-hidden bg-gradient-to-r from-blue-600 via-blue-600 to-indigo-600 hover:from-blue-700 hover:via-blue-700 hover:to-indigo-700 text-white font-semibold py-3 px-6 rounded-2xl shadow-2xl hover:shadow-blue-500/25 transition-all duration-300 transform hover:scale-[1.02] hover:-translate-y-0.5 focus:outline-none focus:ring-4 focus:ring-blue-500/50 mt-4 relative z-10',
              
              // Secondary actions
              formButtonReset: 'text-blue-600 hover:text-blue-700 font-medium text-sm transition-colors duration-200 relative z-10',
              
              // Glassmorphism social buttons
              socialButtonsBlockButton: 'flex-1 relative bg-white/60 backdrop-blur-sm border border-white/40 text-gray-700 hover:bg-white/80 hover:border-white/60 font-medium py-3 px-3 rounded-2xl transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-[1.01] hover:-translate-y-0.5 relative z-10',
              socialButtonsBlockButtonText: 'font-medium text-gray-700 text-xs relative z-10 hidden sm:block',
              socialButtonsProviderIcon: 'w-5 h-5 relative z-10 mx-auto sm:mx-0',
              
              // Enhanced divider
              dividerLine: 'h-px bg-gradient-to-r from-transparent via-white/40 to-transparent',
              dividerText: 'text-gray-500 bg-white/20 backdrop-blur-sm px-4 py-1 text-sm font-medium rounded-full border border-white/30 relative z-10',
              
              // Footer styling - custom signup text
              footerActionLink: 'text-blue-600 hover:text-blue-700 font-medium transition-colors duration-200 underline-offset-4 hover:underline relative z-10',
              footerActionText: 'text-gray-600 text-sm relative z-10',
              footerActions: 'hidden',
              footer: 'relative z-10',
              
              // Hide Clerk branding and extra elements
              footer__legal: 'hidden',
              footer__links: 'hidden',
              footer__poweredBy: 'hidden',
              
              // Error styling
              formFieldErrorText: 'text-red-500 text-sm mt-1 font-medium relative z-10',
              globalError: 'bg-red-500/10 backdrop-blur-sm border border-red-500/20 text-red-600 rounded-2xl p-3 text-sm mb-4 relative z-10',
              
              // Loading states
              spinner: 'text-blue-600 relative z-10',
              
              // Form layout
              form: 'space-y-4 relative z-10',
              main: 'space-y-0 relative z-10',
              headerBox: 'text-center mb-6 relative z-10',
              socialButtons: 'flex gap-2 mb-6 relative z-10',
              formFieldRow: 'space-y-1 relative z-10',
              
              // Identity preview
              identityPreview: 'bg-white/50 backdrop-blur-sm border border-white/30 rounded-2xl p-2 relative z-10',
              identityPreviewText: 'text-gray-700 text-sm relative z-10',
              identityPreviewEditButton: 'text-blue-600 hover:text-blue-700 text-sm font-medium relative z-10',
              
              // Alternative methods
              alternativeMethods: 'space-y-3 relative z-10'
            },
            layout: {
              logoImageUrl: "/images/careconnect-logo.png",
              showOptionalFields: false,
              privacyPageUrl: '/privacy',
              termsPageUrl: '/terms',
              helpPageUrl: '/support',
              socialButtonsPlacement: 'top',
              logoPlacement: 'inside',
              logoLinkUrl: undefined
            },
          }}
          redirectUrl="/role-select"
          signUpUrl="/auth"
          forceRedirectUrl="/role-select"
        />
        </div>
      </div>
    </div>
  )
}