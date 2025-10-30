# filepath: app/rag_pipeline/llm_integration.py

import os
import google.generativeai as genai
from dotenv import load_dotenv
from .model_manager import GeminiManager

# Load environment variables from .env (project root)
load_dotenv()

# Read Gemini API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing! Set it in a .env file in the project root.")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the model manager
model_manager = GeminiManager()


def list_models():
    '''models = gemini.list_models()
    #print("Available Models:")
    for model in models:
          (model.name)
    """Return a list of available model names from the model manager."""'''
    models = model_manager.list_available_models()
    return [model["name"] for model in models]


def summarize_text(text: str, model_name: str = None) -> str:
    """Summarize text using the specified Gemini model name.
    
    If model_name is provided, switches to that model before generating.
    """
    if model_name:
        model_manager.set_model(model_name)
        
    prompt = f"Summarize this educational content clearly and concisely:\n\n{text}"
    return model_manager.generate_content(prompt)


def generate_question(topic: str, model_name: str = None) -> str:
    """Generate an educational quiz question using Gemini.
    
    If model_name is provided, switches to that model before generating.
    """
    if model_name:
        model_manager.set_model(model_name)
        
    prompt = f"Create one challenging multiple-choice question about: {topic}. Include 4 options and mark the correct answer."
    return model_manager.generate_content(prompt)
