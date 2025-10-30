"""Triage agent to classify user intent."""
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from config.prompts import TRIAGE_PROMPT

class TriageAgent:
    """Agent to classify user intent."""
    def __init__(self, llm: ChatGroq):
        self.llm = llm
        self.prompt_template = PromptTemplate.from_template(TRIAGE_PROMPT)
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def classify_intent(self, user_input: str) -> str:
        """Classifies the user's intent."""
        raw_intent = self.chain.invoke({"user_input": user_input}).strip().lower()
        
        if "telecom_support" in raw_intent:
            return "telecom_support"
        elif "task_automation" in raw_intent:
            return "task_automation"
        else:
            return "general"
