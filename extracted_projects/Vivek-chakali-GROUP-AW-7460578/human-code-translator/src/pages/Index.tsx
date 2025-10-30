import { useState } from "react";
import CodeEditor from "@/components/CodeEditor";
import ChatInterface from "@/components/ChatInterface";
import { Code2 } from "lucide-react";

const Index = () => {
  const [code, setCode] = useState(`// Paste your code here
function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}

console.log(fibonacci(10));`);

  return (
    <div className="h-screen w-screen overflow-hidden bg-background">
      {/* Header */}
      <header className="h-16 border-b border-border bg-card shadow-sm">
        <div className="h-full px-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg gradient-primary flex items-center justify-center shadow-glow">
              <Code2 className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold">AI Code Analyzer</h1>
              <p className="text-xs text-muted-foreground">Add features with plain English</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="h-[calc(100vh-4rem)] p-4">
        <div className="h-full grid grid-cols-1 lg:grid-cols-2 gap-4">
          <CodeEditor value={code} onChange={setCode} />
          <ChatInterface code={code} />
        </div>
      </main>
    </div>
  );
};

export default Index;
