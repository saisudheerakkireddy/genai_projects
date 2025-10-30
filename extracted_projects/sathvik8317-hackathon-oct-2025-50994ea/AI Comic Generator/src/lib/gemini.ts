import "dotenv/config";
import { GoogleGenAI } from "@google/genai";

const GEMINI_MODEL = process.env.GEMINI_MODEL ?? "gemini-2.5-flash";

export async function generateText(prompt: string): Promise<string> {
  const apiKey = process.env.GEMINI_API_KEY;
  if (!apiKey) throw new Error("Missing GEMINI_API_KEY in .env");

  const ai = new GoogleGenAI({ apiKey });

  const res = await ai.models.generateContent({
    model: GEMINI_MODEL,
    contents: prompt
  });

  // SDK provides .text convenience getter
  // @ts-expect-error: .text exists at runtime per SDK
  const text: string = res.text ?? "";
  if (!text.trim()) throw new Error("Gemini returned empty text.");
  return text.trim();
}
