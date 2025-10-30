/**
 * Quick smoke test for Hugging Face image generation.
 * Usage:
 *   npm run dev:testimg -- "a cheerful robot reading a book, comic style"
 * Saves output/image.png
 */
import { generateImage } from "./lib/hf.js";

const prompt = process.argv.slice(2).join(" ").trim() ||
  "A colorful comic panel of a friendly robot giving a thumbs up, halftone, bold outlines, vivid colors";

const main = async () => {
  const path = await generateImage(prompt, "test-image.png");
  console.log("Saved:", path);
};

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
