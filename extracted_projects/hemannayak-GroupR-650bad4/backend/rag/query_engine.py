import os
from typing import List
from huggingface_hub import InferenceClient
from loguru import logger

from backend.models import QueryResponse, DisasterEvent
from backend.rag.vector_store import DisasterVectorStore


class DisasterQueryEngine:
    def __init__(self, vector_store: DisasterVectorStore):
        hf_token = os.getenv("HF_TOKEN")
        self.client = InferenceClient(token=hf_token) if hf_token else None
        self.model = "mistralai/Mistral-7B-Instruct-v0.2"
        self.vector_store = vector_store

    async def query(self, question: str) -> QueryResponse:
        """Query with RAG"""
        # Retrieve relevant events
        results = self.vector_store.query(question, k=5)
        
        if not results:
            return QueryResponse(
                answer="No relevant disaster events found.",
                sources=[],
                relevant_events=[],
                confidence=0.0
            )
        
        # Build context
        context = "\n\n".join([
            f"[{i+1}] {evt.text}" 
            for i, evt in enumerate(results)
        ])
        
        # Generate answer
        if self.client:
            prompt = f"""Based on these disaster reports:

{context}

Question: {question}

Provide a specific answer citing source numbers [1], [2], etc."""

            try:
                answer = self.client.text_generation(
                    prompt,
                    model=self.model,
                    max_new_tokens=200,
                    temperature=0.3
                )
            except Exception as e:
                logger.warning(f"LLM generation failed: {e}")
                answer = f"Found {len(results)} relevant events. " + results[0].text[:100]
        else:
            answer = f"Found {len(results)} relevant events. " + results[0].text[:100]
        
        return QueryResponse(
            answer=answer.strip(),
            sources=[evt.id for evt in results],
            relevant_events=results,
            confidence=0.8 if len(results) > 0 else 0.3
        )

    async def generate_situation_report(self) -> str:
        """Generate situation report"""
        stats = self.vector_store.get_stats()
        results = self.vector_store.query("critical emergency situations", k=10)
        
        report = f"""# Disaster Situation Report

## Summary
- Total Events: {stats.get('total_documents', 0)}
- Critical Events: {len([e for e in results if e.severity.value == 'CRITICAL'])}

## Recent Critical Events
"""
        for i, event in enumerate(results[:5], 1):
            report += f"\n{i}. **{event.disaster_type.value}** - {event.severity.value}\n"
            report += f"   Location: {event.location}\n"
            report += f"   {event.text[:100]}...\n"
        
        return report
