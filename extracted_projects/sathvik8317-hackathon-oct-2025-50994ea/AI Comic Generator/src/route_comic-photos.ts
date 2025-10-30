/**
 * Multi-image run: generate N image prompts from one topic and render each.
 * Usage:
 *   npm run dev:photos -- "topic text" 3
 * Saves output/comic_1.png ... comic_N.png
 */
import { generateText } from "./lib/gemini.js";
import { generateImage } from "./lib/hf.js";

const [topicArg, countArg] = (() => {
  const args = process.argv.slice(2);
  return [args[0] || "Basics of circuits", args[1] || "3"];
})();

const N = Math.max(1, Math.min(10, parseInt(countArg, 10) || 3));

const basePrompt = (topic: string) => `
You will produce ${N} variations of single-panel comic dialogue for this topic: ${topic}.
Format each line exactly as: bubble1 || bubble2 || caption
- Tone: bright, fun, concise.
- Each bubble 6-12 words; caption <= 12 words.
- No quotes; one variation per line.
`;

function toImagePrompt(line: string, idx: number): string {
  const [b1, b2, cap] = line.split("||").map(s => s.trim());
  return `
Comic panel #${idx}: two teenage students in a futuristic classroom, holographic screens.
Bold outlines, halftone shading, vivid colors, dynamic lighting, expressive faces, high detail.
Speech bubble 1: ${b1}
Speech bubble 2: ${b2}
Caption (bottom): ${cap}
Comic-style typography, 1024x1024, sharp focus, inked lines.
`.trim();
}

const main = async () => {
  console.log(`Topic: ${topicArg} | Count: ${N}`);
  const raw = await generateText(basePrompt(topicArg));

  const lines = raw
    .split("\n")
    .map(l => l.trim())
    .filter(Boolean)
    .slice(0, N);

  if (lines.length === 0) throw new Error("Gemini returned no lines.");

  let i = 1;
  for (const line of lines) {
    const prompt = toImagePrompt(line, i);
    const outPath = await generateImage(prompt, `comic_${i}.png`);
    console.log(`Saved [${i}/${lines.length}]: ${outPath}`);
    i++;
  }
};

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
  