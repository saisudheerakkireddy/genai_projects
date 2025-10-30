"""Task automation agent for handling booking tasks."""
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from config.prompts import TASK_AGENT_PROMPT
from src.utils.logger import setup_logger

logger = setup_logger()

class TaskAgent:
    """Agent for handling booking tasks."""
    def __init__(self, llm: ChatGroq):
        self.llm = llm
        self.prompt_template = PromptTemplate.from_template(TASK_AGENT_PROMPT)
        self.chain = self.prompt_template | self.llm

    def handle_task(self, user_input: str, conversation_history: list, collected_info: dict) -> dict:
        """Handles a booking task by collecting information."""
        try:
            # Format conversation history for the prompt
            # Handle both dict with 'role'/'content' and other formats
            history_str = ""
            if conversation_history:
                try:
                    history_str = "\n".join([f"{msg.get('role', 'User')}: {msg.get('content', str(msg))}" for msg in conversation_history])
                except:
                    history_str = "\n".join([str(msg) for msg in conversation_history])

            # Invoke the LLM to get the next response
            response_content = self.chain.invoke({
                "conversation_history": history_str,
                "collected_info": str(collected_info),
                "user_input": user_input
            }).content

            # This is a simplified simulation of extracting info.
            # A more robust solution would use function calling or a structured output parser.
            self._update_collected_info(response_content, collected_info)
            
            status = self._get_status(collected_info)

            return {
                "response": response_content,
                "intent": "task_automation",
                "should_escalate": False,
                "citations": [],
                "context": f"Task Status: {status}. Collected Info: {str(collected_info)}"
            }
        except Exception as e:
            logger.error(f"Error in task agent: {e}")
            return {
                "response": "I'm having trouble with this task. Let's try again.",
                "intent": "task_automation",
                "should_escalate": False,
                "citations": [],
                "context": "Error in task processing"
            }
            
    def _update_collected_info(self, response: str, collected_info: dict):
        """A simple heuristic to update collected info. Not robust."""
        # This is a placeholder for a more sophisticated info extraction logic.
        # For a hackathon, this might be all you have time for!
        pass

    def _get_status(self, collected_info: dict) -> str:
        """Determines the collection status."""
        required_fields = ["from", "to", "date", "class", "passengers"]
        if all(collected_info.get(field) for field in required_fields):
            return "completed"
        elif any(collected_info.get(field) for field in required_fields):
            return "collecting_info"
        else:
            return "ready_to_execute"
