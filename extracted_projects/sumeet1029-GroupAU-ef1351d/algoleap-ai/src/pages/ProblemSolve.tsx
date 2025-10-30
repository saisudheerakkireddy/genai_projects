import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Separator } from "@/components/ui/separator";
import Editor from "@monaco-editor/react";
import {
  ArrowLeft,
  Code2,
  Play,
  Lightbulb,
  Target,
  CheckCircle2,
  XCircle,
  Sparkles,
} from "lucide-react";
import { useToast } from "@/hooks/use-toast";

interface TestCase {
  input: string;
  expectedOutput: string;
  passed?: boolean;
  actualOutput?: string;
  runtime?: string;
  memory?: string;
}

interface TestResult {
  passed: boolean;
  totalTests: number;
  passedTests: number;
  failedTests: number;
  runtime: string;
  memory: string;
  testCases: TestCase[];
}

const problemData: Record<string, any> = {
  "1": {
    title: "Two Sum",
    difficulty: "Easy",
    description:
      "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
    examples: [
      {
        input: "nums = [2,7,11,15], target = 9",
        output: "[0,1]",
        explanation: "Because nums[0] + nums[1] == 9, we return [0, 1].",
      },
    ],
    constraints: [
      "2 <= nums.length <= 10^4",
      "-10^9 <= nums[i] <= 10^9",
      "-10^9 <= target <= 10^9",
      "Only one valid answer exists.",
    ],
    starterCode: `function twoSum(nums: number[], target: number): number[] {
    // Your code here
    
}`,
    testCases: [
      {
        input: "nums = [2,7,11,15], target = 9",
        expectedOutput: "[0,1]",
      },
      {
        input: "nums = [3,2,4], target = 6",
        expectedOutput: "[1,2]",
      },
      {
        input: "nums = [3,3], target = 6",
        expectedOutput: "[0,1]",
      },
      {
        input: "nums = [-1,-2,-3,-4,-5], target = -8",
        expectedOutput: "[2,4]",
      },
    ],
  },
};

export default function ProblemSolve() {
  const { problemId } = useParams();
  const navigate = useNavigate();
  const { toast } = useToast();

  const problem = problemData[problemId || "1"];
  const [code, setCode] = useState(problem?.starterCode || "");
  const [isRunning, setIsRunning] = useState(false);
  const [testResults, setTestResults] = useState<TestResult | null>(null);
  const [showHint, setShowHint] = useState(false);

  const simulateCodeExecution = (): TestResult => {
    // Simulate different scenarios
    const scenarios = [
      // All tests pass
      {
        passed: true,
        totalTests: 4,
        passedTests: 4,
        failedTests: 0,
        runtime: "52 ms",
        memory: "42.1 MB",
        testCases: problem.testCases.map((tc: TestCase) => ({
          ...tc,
          passed: true,
          actualOutput: tc.expectedOutput,
          runtime: `${Math.floor(Math.random() * 20 + 10)} ms`,
          memory: `${(Math.random() * 5 + 40).toFixed(1)} MB`,
        })),
      },
      // Some tests fail
      {
        passed: false,
        totalTests: 4,
        passedTests: 2,
        failedTests: 2,
        runtime: "N/A",
        memory: "N/A",
        testCases: problem.testCases.map((tc: TestCase, idx: number) => ({
          ...tc,
          passed: idx < 2,
          actualOutput: idx < 2 ? tc.expectedOutput : "[]",
          runtime: `${Math.floor(Math.random() * 20 + 10)} ms`,
          memory: `${(Math.random() * 5 + 40).toFixed(1)} MB`,
        })),
      },
    ];

    // For demo, randomly choose a scenario (70% success rate)
    const result = Math.random() > 0.3 ? scenarios[0] : scenarios[1];
    return result;
  };

  const handleRunCode = () => {
    setIsRunning(true);
    setTestResults(null);
    
    // Simulate code execution
    setTimeout(() => {
      const result = simulateCodeExecution();
      setTestResults(result);
      setIsRunning(false);
      
      if (result.passed) {
        toast({
          title: "Success! 🎉",
          description: `All ${result.totalTests} test cases passed!`,
        });
      } else {
        toast({
          title: "Some tests failed",
          description: `${result.passedTests}/${result.totalTests} test cases passed`,
          variant: "destructive",
        });
      }
    }, 1500);
  };

  const handleGetHint = () => {
    setShowHint(true);
    toast({
      title: "AI Hint Generated",
      description: "Check the hints panel for guidance",
    });
  };

  return (
    <div className="h-screen flex flex-col bg-background">
      <header className="border-b border-border bg-card/50 backdrop-blur-sm z-50 flex-shrink-0">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Button variant="ghost" size="sm" onClick={() => navigate("/dashboard")}>
              <ArrowLeft className="h-4 w-4 mr-2" />
              Back
            </Button>
            <div className="flex items-center gap-2">
              <Code2 className="h-8 w-8 text-primary" />
              <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                AlgoLeap AI
              </h1>
            </div>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm" onClick={handleGetHint}>
              <Lightbulb className="h-4 w-4 mr-2" />
              Get AI Hint
            </Button>
            <Button variant="hero" size="sm" onClick={handleRunCode} disabled={isRunning}>
              <Play className="h-4 w-4 mr-2" />
              {isRunning ? "Running..." : "Run Code"}
            </Button>
          </div>
        </div>
      </header>

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 overflow-hidden">
        {/* Problem Description */}
        <div className="overflow-y-auto border-r border-border">
          <div className="p-6 space-y-6">
            <div>
              <div className="flex items-center gap-3 mb-4">
                <h2 className="text-2xl font-bold">{problem?.title}</h2>
                <Badge variant={problem?.difficulty === "Easy" ? "success" : "default"}>
                  {problem?.difficulty}
                </Badge>
              </div>
              <p className="text-muted-foreground">{problem?.description}</p>
            </div>

            <Separator />

            <div>
              <h3 className="font-semibold mb-3 flex items-center gap-2">
                <Target className="h-4 w-4 text-primary" />
                Examples
              </h3>
              {problem?.examples?.map((example: any, idx: number) => (
                <Card key={idx} className="mb-3">
                  <CardContent className="pt-4">
                    <div className="space-y-2 text-sm font-mono">
                      <div>
                        <span className="text-muted-foreground">Input:</span> {example.input}
                      </div>
                      <div>
                        <span className="text-muted-foreground">Output:</span> {example.output}
                      </div>
                      {example.explanation && (
                        <div>
                          <span className="text-muted-foreground">Explanation:</span> {example.explanation}
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              ))}
            </div>

            <Separator />

            <div>
              <h3 className="font-semibold mb-3">Constraints</h3>
              <ul className="space-y-1 text-sm text-muted-foreground">
                {problem?.constraints?.map((constraint: string, idx: number) => (
                  <li key={idx}>• {constraint}</li>
                ))}
              </ul>
            </div>

            {showHint && (
              <>
                <Separator />
                <Card className="border-accent bg-accent/5">
                  <CardHeader>
                    <CardTitle className="text-lg flex items-center gap-2">
                      <Sparkles className="h-5 w-5 text-accent" />
                      AI Hint
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <p className="text-sm">
                      <strong>💡 Strategic Approach:</strong> This problem can be solved efficiently using a Hash Map
                      (object in JavaScript/TypeScript).
                    </p>
                    <p className="text-sm text-muted-foreground">
                      Instead of using nested loops which would be O(n²), try storing each number in a hash map as you
                      iterate. For each number, check if (target - current number) exists in your hash map. This
                      reduces time complexity to O(n).
                    </p>
                  </CardContent>
                </Card>
              </>
            )}
          </div>
        </div>

        {/* Code Editor */}
        <div className="flex flex-col overflow-hidden">
          <Tabs defaultValue="code" className="flex-1 flex flex-col">
            <div className="px-4 pt-4">
              <TabsList>
                <TabsTrigger value="code">Code</TabsTrigger>
                <TabsTrigger value="test">Test Results</TabsTrigger>
              </TabsList>
            </div>

            <TabsContent value="code" className="flex-1 overflow-hidden mt-0">
              <div className="h-full">
                <Editor
                  height="100%"
                  defaultLanguage="typescript"
                  value={code}
                  onChange={(value) => setCode(value || "")}
                  theme="vs-dark"
                  options={{
                    minimap: { enabled: false },
                    fontSize: 14,
                    lineNumbers: "on",
                    scrollBeyondLastLine: false,
                    automaticLayout: true,
                    tabSize: 2,
                  }}
                />
              </div>
            </TabsContent>

            <TabsContent value="test" className="flex-1 overflow-auto px-4 pb-4">
              {testResults ? (
                <div className="space-y-4">
                  {/* Summary Card */}
                  <Card className={testResults.passed ? "border-success bg-success/5" : "border-destructive bg-destructive/5"}>
                    <CardHeader>
                      <CardTitle className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          {testResults.passed ? (
                            <>
                              <CheckCircle2 className="h-6 w-6 text-success" />
                              <span>All Tests Passed!</span>
                            </>
                          ) : (
                            <>
                              <XCircle className="h-6 w-6 text-destructive" />
                              <span>Tests Failed</span>
                            </>
                          )}
                        </div>
                        <Badge variant={testResults.passed ? "success" : "destructive"}>
                          {testResults.passedTests}/{testResults.totalTests}
                        </Badge>
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <p className="text-sm text-muted-foreground">Runtime</p>
                          <p className="text-lg font-semibold">{testResults.runtime}</p>
                        </div>
                        <div>
                          <p className="text-sm text-muted-foreground">Memory</p>
                          <p className="text-lg font-semibold">{testResults.memory}</p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>

                  {/* Individual Test Cases */}
                  <div className="space-y-3">
                    <h3 className="font-semibold text-sm text-muted-foreground">Test Case Results</h3>
                    {testResults.testCases.map((testCase: TestCase, idx: number) => (
                      <Card
                        key={idx}
                        className={
                          testCase.passed
                            ? "border-success/50 bg-success/5"
                            : "border-destructive/50 bg-destructive/5"
                        }
                      >
                        <CardHeader className="pb-3">
                          <div className="flex items-start justify-between">
                            <div className="flex items-center gap-2">
                              {testCase.passed ? (
                                <CheckCircle2 className="h-5 w-5 text-success flex-shrink-0" />
                              ) : (
                                <XCircle className="h-5 w-5 text-destructive flex-shrink-0" />
                              )}
                              <CardTitle className="text-base">Test Case {idx + 1}</CardTitle>
                            </div>
                            <div className="flex gap-2 text-xs text-muted-foreground">
                              <span>{testCase.runtime}</span>
                              <span>•</span>
                              <span>{testCase.memory}</span>
                            </div>
                          </div>
                        </CardHeader>
                        <CardContent className="space-y-3">
                          <div>
                            <p className="text-xs font-semibold text-muted-foreground mb-1">Input:</p>
                            <code className="text-sm bg-muted px-2 py-1 rounded block">
                              {testCase.input}
                            </code>
                          </div>
                          
                          <div className="grid grid-cols-2 gap-3">
                            <div>
                              <p className="text-xs font-semibold text-muted-foreground mb-1">Expected:</p>
                              <code className="text-sm bg-muted px-2 py-1 rounded block">
                                {testCase.expectedOutput}
                              </code>
                            </div>
                            <div>
                              <p className="text-xs font-semibold text-muted-foreground mb-1">Your Output:</p>
                              <code
                                className={`text-sm px-2 py-1 rounded block ${
                                  testCase.passed ? "bg-success/10" : "bg-destructive/10"
                                }`}
                              >
                                {testCase.actualOutput}
                              </code>
                            </div>
                          </div>

                          {!testCase.passed && (
                            <div className="pt-2 border-t border-destructive/20">
                              <p className="text-xs text-destructive font-medium">
                                ❌ Output does not match expected result
                              </p>
                            </div>
                          )}
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                </div>
              ) : (
                <div className="text-center text-muted-foreground py-12">
                  <Play className="h-12 w-12 mx-auto mb-4 opacity-50" />
                  <p className="text-lg font-medium mb-2">Ready to test your solution?</p>
                  <p className="text-sm">Click "Run Code" to execute your code against test cases</p>
                </div>
              )}
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}
