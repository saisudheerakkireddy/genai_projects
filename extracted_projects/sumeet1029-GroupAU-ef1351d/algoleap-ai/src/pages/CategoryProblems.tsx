import { useParams, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Code2, CheckCircle2, Circle } from "lucide-react";

const problemsByCategory: Record<string, any[]> = {
  arrays: [
    {
      id: 1,
      title: "Two Sum",
      difficulty: "Easy",
      completed: true,
      description: "Find two numbers that add up to a target value",
      acceptanceRate: 47,
    },
    {
      id: 2,
      title: "Container With Most Water",
      difficulty: "Medium",
      completed: true,
      description: "Find the maximum area between vertical lines",
      acceptanceRate: 54,
    },
    {
      id: 3,
      title: "3Sum",
      difficulty: "Medium",
      completed: false,
      description: "Find all unique triplets that sum to zero",
      acceptanceRate: 31,
    },
    {
      id: 4,
      title: "Trapping Rain Water",
      difficulty: "Hard",
      completed: false,
      description: "Calculate how much water can be trapped after raining",
      acceptanceRate: 56,
    },
  ],
};

const difficultyColors = {
  Easy: "success",
  Medium: "warning",
  Hard: "destructive",
} as const;

export default function CategoryProblems() {
  const { categoryId } = useParams();
  const navigate = useNavigate();

  const problems = problemsByCategory[categoryId || ""] || [];

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="sm" onClick={() => navigate("/dashboard")}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back
            </Button>
            <div className="flex items-center gap-2">
              <Code2 className="h-8 w-8 text-primary" />
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                AlgoLeap AI
              </h1>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-12">
        <div className="mb-8">
          <h2 className="text-3xl font-bold mb-2 capitalize">{categoryId?.replace("-", " ")}</h2>
          <p className="text-muted-foreground">Select a problem to start practicing</p>
        </div>

        <div className="grid gap-4">
          {problems.map((problem) => (
            <Card
              key={problem.id}
              className="hover:shadow-lg transition-all duration-300 cursor-pointer group"
              onClick={() => navigate(`/problem/${problem.id}`)}
            >
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3 flex-1">
                    {problem.completed ? (
                      <CheckCircle2 className="h-6 w-6 text-success mt-1 flex-shrink-0" />
                    ) : (
                      <Circle className="h-6 w-6 text-muted-foreground mt-1 flex-shrink-0" />
                    )}
                    <div className="space-y-1 flex-1">
                      <CardTitle className="group-hover:text-primary transition-colors">
                        {problem.title}
                      </CardTitle>
                      <CardDescription>{problem.description}</CardDescription>
                    </div>
                  </div>
                  <div className="flex flex-col gap-2 items-end">
                    <Badge variant={difficultyColors[problem.difficulty as keyof typeof difficultyColors]}>
                      {problem.difficulty}
                    </Badge>
                    <span className="text-xs text-muted-foreground">{problem.acceptanceRate}% acceptance</span>
                  </div>
                </div>
              </CardHeader>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
}
