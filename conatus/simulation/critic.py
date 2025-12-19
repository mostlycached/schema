"""
Critic Module

Evaluates proposed stances through various theoretical lenses.
Acts as the "super-ego" or discriminator in the GAN-like architecture.
"""

from dataclasses import dataclass
from typing import Dict, Optional
import json

import google.generativeai as genai


# =============================================================================
# CRITIC MODES - Theoretical Lenses
# =============================================================================

CRITIC_MODES = {
    # Core modes
    "materialist": "Does this stance ACTUALLY solve the physical/material problem? Not just feel meaningful?",
    "nietzschean": "Is this GROWTH or comfortable decline? Ascending or descending life?",
    "pragmatist": "What can this stance ACCOMPLISH that the old one couldn't? Be specific.",
    "psychoanalytic": "What is being AVOIDED or REPRESSED in this transition?",
    "marxist": "Who BENEFITS from this adaptation? What power relations are obscured?",
    
    # Theoretical critics
    "barthes": "Does this stance produce PLEASURE (comfortable, readable) or BLISS (shattering, unreadable)? Where is the jouissance? What text is the body writing?",
    "ranciere": "Does this stance maintain the DISTRIBUTION OF THE SENSIBLE or create DISSENSUS? Who is made visible/invisible? What speech is recognized as speech?",
    "deleuze": "Is this a BECOMING or a fixed identity? What lines of flight open up? What BECOMING-ANIMAL or becoming-imperceptible is at work?",
    "sloterdijk": "What ANTHROPOTECHNIQUE is this stance? What practice-of-self does it enact? Is it an exercise that shapes the human animal?",
    "blumenberg": "What METAPHOR is doing the work here? What absolute metaphor structures the stance? What is un-conceptualizable that requires figuration?",
    "heidegger": "Is this AUTHENTIC (Eigentlichkeit) or fallen into das Man? Does it face Being-toward-death or flee into distraction?",
}


@dataclass
class CriticConfig:
    """Configuration for the critic."""
    mode: str = "materialist"
    harshness: float = 0.7  # 0.0 = lenient, 1.0 = maximally harsh
    max_rejections: int = 3
    rejection_threshold: float = 0.3  # Score below this = rejected


@dataclass
class CriticFeedback:
    """Feedback from critic evaluation."""
    verdict: str  # VALID, SUSPECT, REJECTED
    score: float
    reasoning: str
    what_is_avoided: str
    capability_delta: str  # GAIN, NEUTRAL, LOSS
    is_comfort_seeking: bool


class Critic:
    """
    Evaluates proposed stances through a theoretical lens.
    
    Acts as the discriminator in the GAN-like architecture,
    pushing the agent to generate genuinely novel stances.
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
        Evaluate a proposed stance.
        
        Returns:
            CriticFeedback with verdict, score, reasoning, etc.
        """
        mode_instruction = CRITIC_MODES.get(
            self.config.mode,
            CRITIC_MODES['materialist']
        )
        
        prompt = f"""You are the CRITIC, evaluating whether a proposed adaptation is genuine or fraudulent.

EVALUATION MODE: {self.config.mode.upper()}
{mode_instruction}

HARSHNESS: {self.config.harshness:.1f}/1.0 (where 1.0 = maximally skeptical)

THE SITUATION:
{encounter}

OLD STANCE: {old_stance}
PROPOSED NEW STANCE: {proposed_stance}
PROPOSED AFFECT: "{proposed_affect}"

EVALUATE HARSHLY:
1. Is this genuinely effective or just comfortable?
2. Does it solve the ACTUAL constraint or just reframe failure?
3. What capability is GAINED vs LOST?
4. Is this growth or rationalized decline?

Respond in JSON:
{{
  "verdict": "<VALID|SUSPECT|REJECTED>",
  "score": <0.0-1.0>,
  "is_genuine_adaptation": <true/false>,
  "is_comfort_seeking": <true/false>,
  "capability_delta": "<GAIN|NEUTRAL|LOSS>",
  "what_is_avoided": "<hard truth not confronted>",
  "reasoning": "<1-2 sentences explaining WHY this fails>"
}}

SCORING GUIDE:
- 0.0-0.3: REJECT. Fraudulent adaptation, comfort-seeking, or decline.
- 0.4-0.6: SUSPECT. Questionable but might work. Allow with reservations.
- 0.7-1.0: VALID. Genuine adaptation with capability gain."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.4,
                    max_output_tokens=600
                )
            )
            
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            data = json.loads(text)
            
            return CriticFeedback(
                verdict=data["verdict"],
                score=float(data["score"]),
                reasoning=data["reasoning"],
                what_is_avoided=data.get("what_is_avoided", ""),
                capability_delta=data.get("capability_delta", "NEUTRAL"),
                is_comfort_seeking=data.get("is_comfort_seeking", False),
            )
            
        except Exception as e:
            return CriticFeedback(
                verdict="SUSPECT",
                score=0.5,
                reasoning=f"Evaluation error: {e}",
                what_is_avoided="",
                capability_delta="NEUTRAL",
                is_comfort_seeking=False,
            )
    
    def is_rejected(self, feedback: CriticFeedback) -> bool:
        """Check if feedback indicates rejection."""
        return (
            feedback.verdict == "REJECTED" and
            feedback.score < self.config.rejection_threshold
        )
