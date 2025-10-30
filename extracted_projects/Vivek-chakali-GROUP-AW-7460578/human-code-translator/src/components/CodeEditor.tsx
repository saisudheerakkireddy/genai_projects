import { Textarea } from "@/components/ui/textarea";
import { Code2 } from "lucide-react";

interface CodeEditorProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}

const CodeEditor = ({ value, onChange, placeholder }: CodeEditorProps) => {
  return (
    <div className="flex flex-col h-full bg-[hsl(var(--code-bg))] rounded-lg border border-border overflow-hidden shadow-card">
      <div className="flex items-center gap-2 px-4 py-3 border-b border-border bg-card">
        <Code2 className="w-4 h-4 text-primary" />
        <span className="text-sm font-medium text-foreground">Code Editor</span>
      </div>
      <Textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder || "Paste your code here..."}
        className="flex-1 resize-none border-0 bg-transparent font-mono text-sm p-4 focus-visible:ring-0 focus-visible:ring-offset-0 rounded-none"
        spellCheck={false}
      />
    </div>
  );
};

export default CodeEditor;
