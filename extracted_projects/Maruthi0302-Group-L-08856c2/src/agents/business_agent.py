"""Business agent for handling telecom support queries using RAG."""
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from config.settings import settings
from config.prompts import BUSINESS_AGENT_PROMPT
from src.utils.logger import setup_logger

logger = setup_logger()

class BusinessAgent:
    """Agent for handling telecom support queries."""
    def __init__(self, llm: ChatGroq):
        self.llm = llm
        self.prompt_template = PromptTemplate.from_template(BUSINESS_AGENT_PROMPT)
        self.chain = self.prompt_template | self.llm

        try:
            logger.info("Loading ChromaDB vector store...")
            embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL_NAME)
            self.vectorstore = Chroma(
                persist_directory=settings.CHROMA_DB_PATH,
                embedding_function=embeddings
            )
            logger.info("Vector store loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load vector store: {e}")
            self.vectorstore = None

    def handle_query(self, user_input: str) -> dict:
        """Handles a user query using RAG."""
        if not self.vectorstore:
            return {
                "response": "I am currently unable to access my knowledge base. Please try again later.",
                "should_escalate": False,
                "citations": [],
                "context": ""
            }

        try:
            # 1. Similarity search
            logger.info(f"Performing similarity search for: {user_input}")
            results = self.vectorstore.similarity_search(
                user_input,
                k=settings.VECTOR_COUNT
            )

            # 2. Extract context and ticket IDs
            context = "\n".join([doc.page_content for doc in results])
            ticket_ids = [doc.metadata.get("Ticket ID", doc.metadata.get("id")) for doc in results]
            citations = list(set(filter(None, ticket_ids)))

            # 3. Invoke LLM with context
            response_content = self.chain.invoke({
                "context": context,
                "user_input": user_input
            }).content

            # 4. Parse response for escalation
            should_escalate = "escalate: yes" in response_content.lower()
            response_text = response_content.split("Escalation Flag:")[0].strip()

            return {
                "response": response_text,
                "should_escalate": should_escalate,
                "citations": citations,
                "context": context
            }
        except Exception as e:
            logger.error(f"Error handling business query: {e}")
            return {
                "response": "I encountered an error while processing your request. Please try again.",
                "should_escalate": True, # Escalate on error
                "citations": [],
                "context": ""
            }
