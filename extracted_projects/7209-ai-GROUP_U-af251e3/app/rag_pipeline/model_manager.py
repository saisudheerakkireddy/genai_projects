import google.generativeai as genai
from typing import Dict, List, Optional

class GeminiManager:
    """Manages Gemini model initialization and selection."""
    
    def __init__(self):
        """Initialize with default model but allow changing."""
        self.current_model = None
        self.list_available_models()  # This will populate self.available_models
        
        # Start with gemini-1.5-flash as default
        self.set_model("gemini-1.5-flash")
    
    def list_available_models(self) -> List[Dict[str, str]]:
        """Get list of available Gemini models with their types."""
        try:
            models = genai.list_models()
            self.available_models = [
                {"name": model.name, "type": getattr(model, "type", "unknown")}
                for model in models
                if "gemini" in model.name.lower()  # Filter to only Gemini models
            ]
            return self.available_models
        except Exception as e:
            print(f"Error listing models: {e}")
            # Fallback to known models if API call fails
            self.available_models = [
                {"name": "gemini-1.5-flash", "type": "language"},
                {"name": "gemini-1.5", "type": "language"}
            ]
            return self.available_models
    
    def set_model(self, model_name: str) -> None:
        """Set the active model by name."""
        try:
            self.current_model = genai.GenerativeModel(model_name)
        except Exception as e:
            print(f"Error setting model {model_name}: {e}")
            if not self.current_model:
                # Fallback to gemini-1.5-flash if no model is set
                self.current_model = genai.GenerativeModel("gemini-1.5-flash")
    
    def generate_content(self, prompt: str) -> Optional[str]:
        """Generate content using the current model."""
        try:
            response = self.current_model.generate_content(prompt)
            return getattr(response, "text", str(response))
        except Exception as e:
            return f"Error generating content: {e}"

    def get_current_model(self) -> str:
        """Get the name of the currently active model."""
        return self.current_model.model_name if self.current_model else "unknown"