import asyncio
from datetime import datetime, timedelta
from typing import List, Dict
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from loguru import logger

from ..models import DisasterEvent, AgentDecision, Resource, ResourceType


class CoordinatorAgent:
    def __init__(self, vector_store, resource_db: List[Resource]):
        self.vector_store = vector_store
        self.resource_db = resource_db
        self.llm = self._load_llm()

        # Define tools
        self.tools = [
            Tool(
                name="query_database",
                description="Query the database for recent events.",
                func=self.query_database
            ),
            Tool(
                name="calculate_priority",
                description="Calculate priority score for an event.",
                func=self.calculate_priority
            ),
            Tool(
                name="find_resources",
                description="Find available resources near a location.",
                func=self.find_resources
            ),
            Tool(
                name="generate_report",
                description="Generate a situation report.",
                func=self.generate_report
            )
        ]

        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def _load_llm(self):
        model_name = "google/flan-t5-large"  # Local model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        hf_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=200,
            temperature=0.7
        )
        return HuggingFacePipeline(pipeline=hf_pipeline)

    def query_database(self, query: str) -> List[DisasterEvent]:
        # Simplified query to vector store
        results = self.vector_store.query(query, k=10)
        return results  # Assuming returns list of DisasterEvent

    def calculate_priority(self, event: DisasterEvent) -> float:
        """
        Multi-factor priority scoring:
        - Severity weight: 40%
        - Time urgency: 30% (newer = higher)
        - Resource availability: 20%
        - Location clustering: 10% (multiple reports = higher)

        Returns 0-100 score.
        """
        severity_scores = {"CRITICAL": 100, "HIGH": 75, "MEDIUM": 50, "LOW": 25}
        base_score = severity_scores.get(event.severity.value, 0)

        # Time urgency: newer events higher
        time_diff = (datetime.now() - event.timestamp).total_seconds() / 3600
        time_score = max(0, 100 - time_diff * 10)  # Decrease 10 per hour

        # Resource availability: lower availability higher score
        available_resources = len([r for r in self.resource_db if r.available])
        availability_score = (len(self.resource_db) - available_resources) / len(self.resource_db) * 100

        # Location clustering: count nearby events (simplified)
        clustering_score = 10  # Placeholder

        priority = 0.4 * base_score + 0.3 * time_score + 0.2 * availability_score + 0.1 * clustering_score
        return min(100, priority)

    def find_resources(self, location: str, res_type: str) -> List[Resource]:
        # Filter resources by type and availability
        type_enum = ResourceType(res_type)
        return [r for r in self.resource_db if r.type == type_enum and r.available]

    def generate_report(self, time_window_hours: int) -> str:
        # Generate a simple report
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=time_window_hours)
        events = self.query_database(f"events after {start_time}")
        report = f"Situation report for last {time_window_hours} hours:\n"
        report += f"Total events: {len(events)}\n"
        for event in events:
            report += f"- {event.disaster_type} in {event.location}: {event.severity}\n"
        return report

    async def analyze_situation(self) -> AgentDecision:
        """
        Agent workflow:
        1. Query database for events in last hour
        2. For each CRITICAL/HIGH event:
           - Calculate priority score
           - Find nearest available resources
           - Make assignment decision
           - Generate reasoning
        3. Return structured decisions
        """
        prompt = """You are a disaster response coordinator AI.
Analyze current events and assign resources to highest priority needs.

Available tools: query_database, calculate_priority, find_resources

Current situation: [inject recent events]

Your task: Identify top 3 critical situations and recommend resource allocation."""

        # Get recent events
        recent_events = self.query_database("events in last hour")

        # Use agent to analyze
        response = self.agent.run(prompt + f" Recent events: {[e.text for e in recent_events]}")

        # Parse response to create AgentDecision (simplified)
        # In reality, parse the response
        decision = AgentDecision(
            timestamp=datetime.now(),
            event_id=recent_events[0].id if recent_events else "none",
            priority_score=90.0,
            recommended_action="Deploy resources to critical areas",
            assigned_resources=["R001"],
            reasoning=response
        )

        logger.info(f"Agent decision: {decision}")
        return decision
