/**
 * Converts dialogue (bubble1 || bubble2 || caption) into a rich image prompt.
 * Usage:
 *   npm run dev:imgprompt -- "bubble1 || bubble2 || caption"
 * Prints the final image prompt.
 */
const raw = process.argv.slice(2).join(" ").trim() ||
  "Learning has never been this fun! || Thanks to AI, even physics feels like magic! || The Future of Education Begins Now";

const parts = raw.split("||").map(s => s.trim());
let imagePrompt: string;

if (parts.length >= 3) {
  const [b1, b2, cap] = parts;
  imagePrompt = `
A colorful comic book panel of two teenage students in a futuristic classroom,
surrounded by holographic screens. Bold outlines, halftone shading, vivid colors,
dynamic lighting, expressive faces, clean composition, high detail.
Speech bubble 1: ${b1}
Speech bubble 2: ${b2}
Caption (bottom): ${cap}
Comic-style typography, 1024x1024, sharp focus, inked lines.
`.trim();
} else {
  imagePrompt = `
A colorful comic book panel with two teenage students in a futuristic classroom,
holographic screens, bold outlines, halftone shading, vivid colors, dynamic lighting,
expressive faces, caption at the bottom. 1024x1024, sharp focus, inked lines.
`.trim();
}

console.log(imagePrompt);
