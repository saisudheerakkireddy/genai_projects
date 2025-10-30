"""FastAPI server to expose the Telecom AI Agent."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any

from telecom_agent import agent
from src.utils.logger import setup_logger

logger = setup_logger()

app = FastAPI(
    title="Telecom AI Agent API",
    description="A multi-agent RAG system for telecom support and task automation.",
    version="1.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Pydantic Models
class ChatRequest(BaseModel):
    user_input: str
    conversation_history: List[Dict[str, Any]] = Field(default_factory=list)

class ChatResponse(BaseModel):
    response: str
    intent: str
    should_escalate: bool
    citations: List[str]
    context: str

@app.get("/", summary="Health Check")
def read_root():
    """Health check endpoint to ensure the server is running."""
    return {"status": "ok", "message": "Welcome to the Telecom AI Agent API"}

@app.post("/chat", response_model=ChatResponse, summary="Process a user query")
def chat(request: ChatRequest):
    """Main endpoint to interact with the AI agent."""
    try:
        logger.info(f"Received chat request: {request.user_input}")
        result = agent.process(request.user_input, request.conversation_history)
        logger.info(f"Sending response: {result['response']}")
        
        # Ensure all required fields are present with defaults
        citations = [str(c) for c in result.get('citations', [])]
        should_escalate = result.get('should_escalate', False)
        intent = result.get('intent', 'general')
        context = result.get('context', '')
        response_text = result.get('response', '')
        
        return ChatResponse(
            response=response_text,
            intent=intent,
            should_escalate=should_escalate,
            citations=citations,
            context=context
        )
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
