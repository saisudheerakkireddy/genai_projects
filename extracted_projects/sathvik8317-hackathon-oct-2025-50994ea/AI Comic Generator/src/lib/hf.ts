import "dotenv/config";
import { HfInference } from "@huggingface/inference";
import { createWriteStream } from "node:fs";
import { mkdirSync } from "node:fs";
import { join } from "node:path";

const HF_MODEL = process.env.HF_IMAGE_MODEL ?? "stabilityai/stable-diffusion-2-1";

export async function generateImage(
  prompt: string,
  outName = "image.png",
  model = HF_MODEL
): Promise<string> {
  const token = process.env.HF_API_KEY;
  if (!token) throw new Error("Missing HF_API_KEY in .env");

  const hf = new HfInference(token);
  mkdirSync("output", { recursive: true });

  // text-to-image returns ArrayBuffer
  const result = await hf.textToImage({
    model,
    inputs: prompt
  });

  const outPath = join("output", outName);
  const buf = Buffer.from(await result.arrayBuffer());
  await new Promise<void>((resolve, reject) => {
    const ws = createWriteStream(outPath);
    ws.on("finish", () => resolve());
    ws.on("error", reject);
    ws.end(buf);
  });
  return outPath;
}
