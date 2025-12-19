"""
Critic Module

Evaluates proposed stances through multiple analytical dimensions.
Uses a hybrid approach that illuminates rather than judges.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, List
import json

import google.generativeai as genai


# =============================================================================
# CRITIQUE DIMENSIONS - Multi-Perspective Analysis
# =============================================================================

CRITIQUE_DIMENSIONS = {
    "diagnostic": {
        "name": "Diagnostic",
        "question": "What is this stance DOING phenomenologically? What mode of being does it enact?",
        "focus": "Describes without judgment - illuminates the mechanism"
    },
    "generative": {
        "name": "Generative",
        "question": "What might EMERGE from this stance? What possibilities does it open or foreclose?",
        "focus": "Future-oriented - what could this become"
    },
    "archetypal": {
        "name": "Archetypal",
        "question": "What PATTERN or archetype is being enacted? What mythic/structural role does this fulfill?",
        "focus": "Maps to universal human patterns"
    },
    "relational": {
        "name": "Relational",
        "question": "How does this stance change the COUPLING between agent and environment? What new affordances appear?",
        "focus": "Considers the relation, not just the agent"
    },
    "temporal": {
        "name": "Temporal",
        "question": "What is this stance ON THE WAY TO? Is it a transition, a settling, a preparation?",
        "focus": "Becoming rather than being - the trajectory"
    },
    "phenomenological": {
        "name": "Phenomenological",
        "question": "What does this FEEL LIKE from inside? What is the lived texture of this stance?",
        "focus": "First-person experiential description"
    },
}


@dataclass
class DimensionAnalysis:
    """Analysis from a single dimension."""
    dimension: str
    insight: str


@dataclass
class CriticConfig:
    """Configuration for the critic."""
    mode: str = "hybrid"  # "hybrid" uses all dimensions
    harshness: float = 0.5  # 0.0 = generous, 1.0 = demanding
    max_rejections: int = 3
    rejection_threshold: float = 0.3


@dataclass
class CriticFeedback:
    """Multi-dimensional feedback from critic evaluation."""
    verdict: str  # VALID, SUSPECT, REJECTED
    score: float
    reasoning: str  # Synthesis across dimensions
    dimensions: List[DimensionAnalysis] = field(default_factory=list)
    
    # Legacy fields for compatibility
    what_is_avoided: str = ""
    capability_delta: str = "NEUTRAL"
    is_comfort_seeking: bool = False


class Critic:
    """
    Evaluates proposed stances through multiple analytical dimensions.
    
    Rather than judging from a single theoretical perspective,
    illuminates the stance from multiple angles simultaneously.
    """
    
    def __init__(
        self,
        config: CriticConfig = None,
        model_name: str = "gemini-2.0-flash",
    ):
        self.config = config or CriticConfig()
        self.model = genai.GenerativeModel(model_name)
    
    def evaluate(
        self,
        encounter: str,
        proposed_stance: str,
        proposed_affect: str,
        old_stance: str,
    ) -> CriticFeedback:
        """
        Evaluate a proposed stance through all dimensions.
        
        Returns:
            CriticFeedback with multi-dimensional analysis.
        """
        
        # Build dimension prompts
        dimension_questions = "\n".join([
            f"- **{d['name']}**: {d['question']}"
            for d in CRITIQUE_DIMENSIONS.values()
        ])
        
        prompt = f"""You are a multi-dimensional analyst examining a proposed stance adaptation.

THE SITUATION:
{encounter}

TRANSITION:
From: {old_stance}
To: {proposed_stance}
Affect: "{proposed_affect}"

Analyze this transition through SIX dimensions. For each, provide a specific insight (1-2 sentences):

{dimension_questions}

After analyzing all dimensions, synthesize:
1. What is the OVERALL QUALITY of this adaptation? (considering all dimensions)
2. What is most NOTABLE or interesting about this stance?
3. What TENSION or unresolved dynamic exists?

Respond in JSON:
{{
  "dimensions": {{
    "diagnostic": "<what this stance is doing>",
    "generative": "<what might emerge>",
    "archetypal": "<pattern being enacted>",
    "relational": "<how coupling changes>",
    "temporal": "<what this is on the way to>",
    "phenomenological": "<lived experience>"
  }},
  "synthesis": {{
    "overall_quality": "<RICH|ADEQUATE|THIN|COLLAPSED>",
    "notable": "<most interesting aspect>",
    "tension": "<unresolved dynamic>",
    "trajectory": "<where this seems to be heading>"
  }},
  "score": <0.0-1.0>,
  "verdict": "<VALID|SUSPECT|REJECTED>"
}}

SCORING:
- 0.0-0.3: THIN/COLLAPSED - stance lacks dimensionality, collapses complexity
- 0.4-0.6: ADEQUATE - functional but not fully alive
- 0.7-0.9: RICH - multi-dimensional, alive, generative
- 1.0: Exceptional - rare, deeply coherent across all dimensions"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.4,
                    max_output_tokens=1200
                )
            )
            
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            # Basic JSON repair
            text = self._repair_json(text)
            data = json.loads(text)
            
            # Build dimension analyses
            dimensions = []
            dim_data = data.get("dimensions", {})
            for key, value in dim_data.items():
                if key in CRITIQUE_DIMENSIONS:
                    dimensions.append(DimensionAnalysis(
                        dimension=CRITIQUE_DIMENSIONS[key]["name"],
                        insight=value
                    ))
            
            # Build synthesis reasoning
            synthesis = data.get("synthesis", {})
            reasoning_parts = []
            if synthesis.get("notable"):
                reasoning_parts.append(f"Notable: {synthesis['notable']}")
            if synthesis.get("tension"):
                reasoning_parts.append(f"Tension: {synthesis['tension']}")
            if synthesis.get("trajectory"):
                reasoning_parts.append(f"Trajectory: {synthesis['trajectory']}")
            
            reasoning = " | ".join(reasoning_parts) if reasoning_parts else "Multi-dimensional analysis complete."
            
            return CriticFeedback(
                verdict=data.get("verdict", "SUSPECT"),
                score=float(data.get("score", 0.5)),
                reasoning=reasoning,
                dimensions=dimensions,
                what_is_avoided=synthesis.get("tension", ""),
                capability_delta=synthesis.get("overall_quality", "ADEQUATE"),
                is_comfort_seeking=False,
            )
            
        except Exception as e:
            return CriticFeedback(
                verdict="SUSPECT",
                score=0.5,
                reasoning=f"Evaluation error: {e}",
                dimensions=[],
                what_is_avoided="",
                capability_delta="NEUTRAL",
                is_comfort_seeking=False,
            )
    
    def _repair_json(self, text: str) -> str:
        """Repair common JSON malformations from LLM output."""
        import re
        
        text = text.strip()
        
        # Remove trailing commas before closing brackets
        text = re.sub(r',\s*}', '}', text)
        text = re.sub(r',\s*]', ']', text)
        
        # Balance brackets
        open_braces = text.count('{')
        close_braces = text.count('}')
        text += '}' * (open_braces - close_braces)
        
        open_brackets = text.count('[')
        close_brackets = text.count(']')
        text += ']' * (open_brackets - close_brackets)
        
        # Fix unterminated strings
        quote_count = text.count('"')
        if quote_count % 2 == 1:
            last_brace = text.rfind('}')
            if last_brace > 0:
                text = text[:last_brace] + '"' + text[last_brace:]
        
        return text
    
    def is_rejected(self, feedback: CriticFeedback) -> bool:
        """Check if feedback indicates rejection."""
        return (
            feedback.verdict == "REJECTED" and
            feedback.score < self.config.rejection_threshold
        )


# Keep old constant for backward compatibility
CRITIC_MODES = {
    "hybrid": "Multi-dimensional analysis through diagnostic, generative, archetypal, relational, temporal, and phenomenological lenses.",
    "materialist": "Legacy mode - defaults to hybrid.",
    "nietzschean": "Legacy mode - defaults to hybrid.",
}
