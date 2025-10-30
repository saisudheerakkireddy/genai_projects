import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Code2, LogOut, Zap, Target, TrendingUp, Brain } from "lucide-react";
import heroBackground from "@/assets/hero-background.jpg";

const problemCategories = [
  {
    id: "arrays",
    name: "Arrays & Hashing",
    description: "Master array manipulation and hash table techniques",
    problemCount: 24,
    completed: 8,
    difficulty: "Easy to Hard",
    icon: "📊",
  },
  {
    id: "two-pointers",
    name: "Two Pointers",
    description: "Learn efficient two-pointer patterns for arrays and strings",
    problemCount: 18,
    completed: 5,
    difficulty: "Easy to Medium",
    icon: "👉",
  },
  {
    id: "sliding-window",
    name: "Sliding Window",
    description: "Optimize solutions with sliding window technique",
    problemCount: 15,
    completed: 3,
    difficulty: "Medium",
    icon: "🪟",
  },
  {
    id: "trees",
    name: "Trees & Graphs",
    description: "Navigate complex tree and graph data structures",
    problemCount: 32,
    completed: 12,
    difficulty: "Medium to Hard",
    icon: "🌳",
  },
  {
    id: "dynamic-programming",
    name: "Dynamic Programming",
    description: "Break down complex problems with DP strategies",
    problemCount: 28,
    completed: 4,
    difficulty: "Hard",
    icon: "🧮",
  },
  {
    id: "backtracking",
    name: "Backtracking",
    description: "Explore solution spaces with backtracking algorithms",
    problemCount: 20,
    completed: 6,
    difficulty: "Medium to Hard",
    icon: "🔄",
  },
];

export default function Dashboard() {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    navigate("/auth");
  };

  const totalProblems = problemCategories.reduce((acc, cat) => acc + cat.problemCount, 0);
  const totalCompleted = problemCategories.reduce((acc, cat) => acc + cat.completed, 0);
  const overallProgress = (totalCompleted / totalProblems) * 100;

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Code2 className="h-8 w-8 text-primary" />
            <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              AlgoLeap AI
            </h1>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-sm text-muted-foreground hidden sm:inline">{user?.email}</span>
            <Button variant="ghost" size="sm" onClick={handleLogout}>
              <LogOut className="h-4 w-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section
        className="relative py-20 px-4 overflow-hidden"
        style={{
          backgroundImage: `url(${heroBackground})`,
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      >
        <div className="absolute inset-0 bg-gradient-to-r from-background/95 via-background/80 to-background/95" />
        <div className="container mx-auto relative z-10">
          <div className="max-w-3xl mx-auto text-center space-y-6">
            <h2 className="text-4xl md:text-5xl font-bold">
              Welcome back, <span className="bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">Champion</span>!
            </h2>
            <p className="text-lg text-muted-foreground">
              Your AI advisor is ready to guide you through today's challenges
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button variant="hero" size="lg" className="group">
                <Zap className="mr-2 h-5 w-5 group-hover:animate-pulse" />
                Continue Learning
              </Button>
              <Button variant="outline" size="lg">
                <Brain className="mr-2 h-5 w-5" />
                AI Practice Session
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-8 px-4 border-b border-border">
        <div className="container mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Overall Progress</CardTitle>
                <Target className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{Math.round(overallProgress)}%</div>
                <Progress value={overallProgress} className="mt-2" />
                <p className="text-xs text-muted-foreground mt-2">
                  {totalCompleted} of {totalProblems} problems solved
                </p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">Current Streak</CardTitle>
                <TrendingUp className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">7 days</div>
                <p className="text-xs text-muted-foreground mt-2">Keep it up! You're on fire 🔥</p>
              </CardContent>
            </Card>

            <Card>
              <CardHeader className="flex flex-row items-center justify-between pb-2">
                <CardTitle className="text-sm font-medium">AI Hints Used</CardTitle>
                <Brain className="h-4 w-4 text-muted-foreground" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">23</div>
                <p className="text-xs text-muted-foreground mt-2">Strategic guidance this week</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Problem Categories */}
      <section className="py-12 px-4">
        <div className="container mx-auto">
          <div className="mb-8">
            <h3 className="text-2xl font-bold mb-2">Problem Categories</h3>
            <p className="text-muted-foreground">Choose a category to start practicing</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {problemCategories.map((category) => {
              const progress = (category.completed / category.problemCount) * 100;
              return (
                <Card
                  key={category.id}
                  className="hover:shadow-lg transition-all duration-300 cursor-pointer group"
                  onClick={() => navigate(`/category/${category.id}`)}
                >
                  <CardHeader>
                    <div className="flex items-start justify-between">
                      <div className="text-4xl mb-2">{category.icon}</div>
                      <Badge variant="secondary">{category.difficulty}</Badge>
                    </div>
                    <CardTitle className="group-hover:text-primary transition-colors">{category.name}</CardTitle>
                    <CardDescription>{category.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-2">
                      <div className="flex justify-between text-sm">
                        <span className="text-muted-foreground">Progress</span>
                        <span className="font-medium">
                          {category.completed}/{category.problemCount}
                        </span>
                      </div>
                      <Progress value={progress} />
                    </div>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>
    </div>
  );
}
