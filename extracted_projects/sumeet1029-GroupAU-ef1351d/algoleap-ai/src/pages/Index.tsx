import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Code2, Sparkles, Brain, Target, TrendingUp, Zap, CheckCircle } from "lucide-react";
import heroBackground from "@/assets/hero-background.jpg";
import { useEffect } from "react";

export default function Index() {
  const navigate = useNavigate();
  const { user } = useAuth();

  useEffect(() => {
    if (user) {
      navigate("/dashboard");
    }
  }, [user, navigate]);

  const features = [
    {
      icon: <Brain className="h-8 w-8 text-primary" />,
      title: "AI-Powered Hints",
      description: "Get actionable, contextual hints when you're stuck - just like a senior developer would provide.",
    },
    {
      icon: <Target className="h-8 w-8 text-accent" />,
      title: "Adaptive Learning",
      description: "AI generates custom problems at your skill level to help you build confidence and master concepts.",
    },
    {
      icon: <TrendingUp className="h-8 w-8 text-success" />,
      title: "Strategic Guidance",
      description: "Learn problem-solving patterns and techniques, not just memorize solutions.",
    },
  ];

  const benefits = [
    "Personalized feedback on your code",
    "Step-by-step hints without spoiling solutions",
    "Adaptive difficulty based on your progress",
    "Real interview-style problems",
    "Track your improvement over time",
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Code2 className="h-8 w-8 text-primary" />
            <span className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              AlgoLeap AI
            </span>
          </div>
          <div className="flex gap-3">
            <Button variant="ghost" onClick={() => navigate("/auth")}>
              Login
            </Button>
            <Button variant="hero" onClick={() => navigate("/auth")}>
              Get Started
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section
        className="relative py-24 px-4 overflow-hidden"
        style={{
          backgroundImage: `url(${heroBackground})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-r from-background/95 via-background/80 to-background/95" />
        <div className="container mx-auto relative z-10">
          <div className="max-w-4xl mx-auto text-center space-y-8">
            <div className="inline-flex items-center gap-2 bg-primary/10 text-primary px-4 py-2 rounded-full text-sm font-medium">
              <Sparkles className="h-4 w-4" />
              Your Personal AI Advisor for DSA Mastery
            </div>
            <h1 className="text-5xl md:text-7xl font-bold leading-tight">
              Master{" "}
              <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                Technical Interviews
              </span>{" "}
              with AI Guidance
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Stop grinding blindly. AlgoLeap AI provides personalized hints, adaptive problems, and strategic advice
              to make you interview-ready faster.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button variant="hero" size="lg" onClick={() => navigate("/auth")} className="group">
                <Zap className="mr-2 h-5 w-5 group-hover:animate-pulse" />
                Start Learning Free
              </Button>
              <Button variant="outline" size="lg">
                Watch Demo
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-muted/30">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">Why AlgoLeap AI?</h2>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Traditional platforms tell you if you're wrong. We teach you how to get it right.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {features.map((feature, idx) => (
              <Card key={idx} className="border-2 hover:border-primary transition-colors">
                <CardHeader>
                  <div className="mb-4">{feature.icon}</div>
                  <CardTitle>{feature.title}</CardTitle>
                  <CardDescription className="text-base">{feature.description}</CardDescription>
                </CardHeader>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <h2 className="text-3xl md:text-4xl font-bold mb-6">
                Transform Your Interview Prep Journey
              </h2>
              <p className="text-lg text-muted-foreground mb-8">
                AlgoLeap AI combines the structure of traditional coding platforms with the personalized guidance of a
                1-on-1 mentor. No more frustration, no more memorization - just effective learning.
              </p>
              <ul className="space-y-4">
                {benefits.map((benefit, idx) => (
                  <li key={idx} className="flex items-start gap-3">
                    <CheckCircle className="h-6 w-6 text-success flex-shrink-0 mt-0.5" />
                    <span className="text-lg">{benefit}</span>
                  </li>
                ))}
              </ul>
            </div>
            <Card className="p-8 bg-gradient-to-br from-primary/5 to-accent/5 border-2">
              <CardHeader>
                <CardTitle className="text-2xl">Example: Getting Stuck?</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="bg-destructive/10 border-l-4 border-destructive p-4 rounded">
                  <p className="text-sm font-mono">
                    ❌ Traditional Platform: "Wrong Answer"
                  </p>
                </div>
                <div className="bg-success/10 border-l-4 border-success p-4 rounded">
                  <p className="text-sm font-semibold mb-2">✅ AlgoLeap AI:</p>
                  <p className="text-sm">
                    "Your solution is timing out. Your nested loop is O(n²). Hint: Try using a Hash Map to check for
                    duplicates in a single pass, reducing complexity to O(n)."
                  </p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-primary/10 via-accent/10 to-primary/10">
        <div className="container mx-auto text-center">
          <h2 className="text-3xl md:text-5xl font-bold mb-6">
            Ready to Ace Your Next Interview?
          </h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Join thousands of developers who've transformed their interview prep with AI-powered guidance.
          </p>
          <Button variant="hero" size="lg" onClick={() => navigate("/auth")} className="text-lg px-8 py-6">
            Start Your Journey Today
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8 px-4">
        <div className="container mx-auto text-center text-muted-foreground">
          <p>&copy; 2025 AlgoLeap AI. Your personal advisor for technical interview success.</p>
        </div>
      </footer>
    </div>
  );
}
