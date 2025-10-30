import json
import os
from functools import lru_cache
from typing import List
from tenacity import retry, stop_after_attempt, wait_exponential
from loguru import logger
from huggingface_hub import InferenceClient

from backend.models import ExtractedInfo, DisasterType, Severity


class DisasterInfoExtractor:
    def __init__(self, hf_token: str = None):
        if not hf_token:
            hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            logger.warning("No HF_TOKEN found, using fallback extraction")
            self.client = None
        else:
            self.client = InferenceClient(token=hf_token)
        self.model = "mistralai/Mistral-7B-Instruct-v0.2"

    def extract(self, text: str) -> ExtractedInfo:
        if not self.client:
            return self._fallback_extraction(text)
        
        prompt = f"""<s>[INST] Extract disaster information from this text as JSON.

Text: "{text}"

Respond with ONLY valid JSON (no markdown, no explanation):
{{
  "disaster_type": "EARTHQUAKE|FLOOD|FIRE|STORM|LANDSLIDE|OTHER",
  "severity": "LOW|MEDIUM|HIGH|CRITICAL",
  "location": "location if mentioned else null",
  "needs": ["list of needs"],
  "confidence": 0.85
}}

Rules:
- CRITICAL: trapped, dying, urgent
- HIGH: emergency, help needed
- MEDIUM: damage, need assistance
- LOW: update, information
[/INST]</s>"""

        try:
            response = self.client.text_generation(
                prompt,
                model=self.model,
                max_new_tokens=200,
                temperature=0.1
            )
            
            # Extract JSON from response
            json_str = response.strip()
            if "```json" in json_str:
                json_str = json_str.split("```json")[1].split("```")[0]
            elif "```" in json_str:
                json_str = json_str.split("```")[1].split("```")[0]
            
            data = json.loads(json_str)
            
            return ExtractedInfo(
                disaster_type=DisasterType[data["disaster_type"]],
                severity=Severity[data["severity"]],
                location=data.get("location"),
                needs=data.get("needs", []),
                confidence=data.get("confidence", 0.7)
            )
        except Exception as e:
            logger.warning(f"LLM extraction failed: {e}. Using fallback.")
            return self._fallback_extraction(text)
    
    def _fallback_extraction(self, text: str) -> ExtractedInfo:
        """Keyword-based fallback if LLM fails"""
        text_lower = text.lower()
        
        # Detect type
        if any(kw in text_lower for kw in ["earthquake", "quake", "tremor"]):
            dtype = DisasterType.EARTHQUAKE
        elif any(kw in text_lower for kw in ["flood", "flooding", "water"]):
            dtype = DisasterType.FLOOD
        elif any(kw in text_lower for kw in ["fire", "wildfire", "burning"]):
            dtype = DisasterType.FIRE
        elif any(kw in text_lower for kw in ["storm", "hurricane", "cyclone"]):
            dtype = DisasterType.STORM
        else:
            dtype = DisasterType.OTHER
        
        # Detect severity
        if any(kw in text_lower for kw in ["trapped", "dying", "urgent", "critical"]):
            severity = Severity.CRITICAL
        elif any(kw in text_lower for kw in ["emergency", "help", "rescue"]):
            severity = Severity.HIGH
        elif any(kw in text_lower for kw in ["damage", "need", "injured"]):
            severity = Severity.MEDIUM
        else:
            severity = Severity.LOW
        
        return ExtractedInfo(
            disaster_type=dtype,
            severity=severity,
            location=None,
            needs=[],
            confidence=0.5
        )

    def batch_extract(self, texts: List[str]) -> List[ExtractedInfo]:
        return [self.extract(text) for text in texts]
