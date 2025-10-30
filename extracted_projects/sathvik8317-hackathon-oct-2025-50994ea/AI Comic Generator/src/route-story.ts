/**
 * Generates comic dialogue/caption text with Gemini.
 * Usage:
 *   npm run dev:story -- "topic about physics basics"
 * Output: prints bubble1 || bubble2 || caption
 */
import { generateText } from "./lib/gemini.js";

const input = process.argv.slice(2).join(" ").trim() || "Explain Newton's first law for teens";
const prompt = `
You are writing comic dialogue for a single panel. 
Return EXACTLY this format: bubble1 || bubble2 || caption
- Tone: bright, fun, concise.
- Topic: ${input}
- 6-12 words per bubble. Caption up to 12 words.
- No quotes around text.
`;

const main = async () => {
  const text = await generateText(prompt);
  console.log(text);
};

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
