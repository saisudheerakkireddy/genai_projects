"""Main agent orchestrator that routes requests to the appropriate agent."""
from langchain_groq import ChatGroq
from config.settings import settings
from src.agents.triage_agent import TriageAgent
from src.agents.business_agent import BusinessAgent
from src.agents.task_agent import TaskAgent
from src.utils.logger import setup_logger

logger = setup_logger()

class TelecomAIAgent:
    """The main orchestrator for the multi-agent RAG system."""
    def __init__(self):
        logger.info("Initializing Telecom AI Agent...")
        self.llm = ChatGroq(temperature=0, groq_api_key=settings.GROQ_API_KEY, model_name=settings.LLM_MODEL_NAME)
        self.triage_agent = TriageAgent(self.llm)
        self.business_agent = BusinessAgent(self.llm)
        self.task_agent = TaskAgent(self.llm)
        logger.info("Telecom AI Agent initialized successfully.")

    def process(self, user_input: str, conversation_history: list) -> dict:
        """Processes a user query by routing it to the correct agent."""
        logger.info(f"Processing user input: {user_input}")
        
        # 1. Classify intent
        intent = self.triage_agent.classify_intent(user_input)
        logger.info(f"Classified intent as: {intent}")

        # 2. Route to the appropriate agent
        if intent == "telecom_support":
            result = self.business_agent.handle_query(user_input)
            result["intent"] = "telecom_support"
            return result
        elif intent == "task_automation":
            # For task automation, we need to manage conversation state
            # This is a simplified example of state management
            collected_info = conversation_history[-1].get("collected_info", {}) if conversation_history else {}
            result = self.task_agent.handle_task(user_input, conversation_history, collected_info)
            result["intent"] = "task_automation"
            return result
        else: # general intent
            response = self.llm.invoke(user_input).content
            return {
                "response": response,
                "intent": "general",
                "should_escalate": False,
                "citations": [],
                "context": ""
            }

# Create a singleton instance of the agent
agent = TelecomAIAgent()
