/**
 * End-to-end: topic -> dialogue via Gemini -> image prompt -> image via HF.
 * Usage:
 *   npm run dev:comic -- "intro to gravity"
 * Saves output/comic_panel.png and prints all steps.
 */
import { generateText } from "./lib/gemini.js";
import { generateImage } from "./lib/hf.js";

const topic = process.argv.slice(2).join(" ").trim() || "Intro to gravity for teens";

const dialoguePrompt = `
Return EXACTLY this format: bubble1 || bubble2 || caption
- Bright, fun, concise; 6-12 words per bubble; caption <= 12 words.
- Topic: ${topic}
- No quotes around text.
`;

function toImagePrompt(dialogue: string): string {
  const parts = dialogue.split("||").map(s => s.trim());
  if (parts.length < 3) {
    return `
A colorful comic book panel with two teenage students in a futuristic classroom,
holographic screens, bold outlines, halftone shading, vivid colors, dynamic lighting,
expressive faces, caption at the bottom. 1024x1024, sharp focus, inked lines.
`.trim();
  }
  const [b1, b2, cap] = parts;
  return `
A colorful comic panel of two teenage students in a futuristic classroom with holographic screens.
Bold outlines, halftone shading, vivid colors, dynamic angles, expressive faces, high detail.
Speech bubble 1: ${b1}
Speech bubble 2: ${b2}
Caption (bottom): ${cap}
Comic-style typography, 1024x1024, sharp focus, inked lines.
`.trim();
}

const main = async () => {
  console.log("Topic:", topic);

  const dialogue = await generateText(dialoguePrompt);
  console.log("\nDialogue:", dialogue);

  const imgPrompt = toImagePrompt(dialogue);
  console.log("\nImage Prompt:\n", imgPrompt);

  const path = await generateImage(imgPrompt, "comic_panel.png");
  console.log("\nSaved:", path);
};

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
