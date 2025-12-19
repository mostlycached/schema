"""
Environment: Encounter Frame Generator

This module provides the Environment class that generates and manages
encounter frames - the constraints and challenges the agent must face.
"""

import os
import json
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)


class EncounterDifficulty(Enum):
    """Difficulty levels for encounter frames."""
    TRIVIAL = 0.1
    EASY = 0.3
    MODERATE = 0.5
    CHALLENGING = 0.7
    ADVERSARIAL = 0.9


@dataclass
class EncounterFrame:
    """
    A specific slice of environment constraints.
    The agent must handle this using its current stance.
    """
    description: str
    constraints: list[str] = field(default_factory=list)
    difficulty: float = 0.5
    category: str = "general"  # e.g., "physical", "social", "cognitive", "emotional"
    

@dataclass
class EnvironmentContext:
    """
    Pre-defined context configuration for specific domains.
    Derived from Castle Rooms IIT Analysis + THESIS.md examples.
    """
    name: str
    description: str
    typical_constraints: list[str]
    escalation_pattern: list[str]  # How challenges intensify
    limit_situations: list[str]  # Jaspers' Grenzsituationen relevant here


# Pre-defined contexts from Castle Rooms + THESIS.md
CONTEXTS = {
    # From THESIS.md examples
    "dance": EnvironmentContext(
        name="Dance / Movement",
        description="Physical movement improvisation where the dancer must adapt to bodily states and spatial constraints",
        typical_constraints=[
            "Maintain balance while moving",
            "Express emotion through gesture",
            "Respond to rhythm and tempo",
            "Navigate spatial boundaries"
        ],
        escalation_pattern=[
            "Simple balanced movement",
            "Increased tempo demands",
            "Physical obstacle or constraint",
            "Complete loss of expected balance",
            "Floor becomes primary surface"
        ],
        limit_situations=["Struggle", "Historical Determinedness"]
    ),
    
    "woodworking": EnvironmentContext(
        name="Woodworking / Craft",
        description="Manual craft where the material resists and demands adaptive technique",
        typical_constraints=[
            "Apply controlled force to material",
            "Read material feedback",
            "Maintain tool accuracy",
            "Preserve wood integrity"
        ],
        escalation_pattern=[
            "Straight-grain, cooperative wood",
            "Slight irregularities in grain",
            "Knots requiring adjustment",
            "Wild grain that tears under normal technique",
            "Complete tool-material mismatch"
        ],
        limit_situations=["Struggle"]
    ),
    
    "child_rearing": EnvironmentContext(
        name="Child Rearing / Caregiving",
        description="Parenting situations requiring adaptive response to child's emotional states",
        typical_constraints=[
            "Maintain safety",
            "Provide emotional regulation",
            "Communicate appropriately",
            "Model desired behavior"
        ],
        escalation_pattern=[
            "Child calm and receptive",
            "Child distracted or uncooperative",
            "Child frustrated, mild resistance",
            "Full tantrum, logic failing",
            "Complete dysregulation, emergency co-regulation needed"
        ],
        limit_situations=["Struggle", "Guilt"]
    ),
    
    # From Castle Rooms IIT Analysis
    "forge": EnvironmentContext(
        name="The Forge (Room 026)",
        description="High-intensity physical training where body meets resistance",
        typical_constraints=[
            "Maintain form under load",
            "Manage cardiovascular response",
            "Execute precise movement patterns",
            "Push through discomfort"
        ],
        escalation_pattern=[
            "Warm-up, light resistance",
            "Working weight, moderate challenge",
            "Near-maximal effort",
            "Form breakdown, must adapt",
            "Failure point - must find new approach"
        ],
        limit_situations=["Struggle", "Death (metaphorical)"]
    ),
    
    "dojo": EnvironmentContext(
        name="The Dojo (Room 034)",
        description="Deliberate practice space for skill acquisition through repetition",
        typical_constraints=[
            "Execute technique with precision",
            "Integrate feedback from attempts",
            "Maintain focus despite repetition",
            "Refine incremental improvements"
        ],
        escalation_pattern=[
            "Basic form practice",
            "Increased complexity",
            "Speed or pressure added",
            "Plateaued - old approach isn't working",
            "Breakthrough requires fundamental change"
        ],
        limit_situations=["Struggle", "Historical Determinedness"]
    ),
    
    "arena": EnvironmentContext(
        name="The Arena (Room 029)",
        description="Public performance under judgment where stakes are real",
        typical_constraints=[
            "Deliver under observation",
            "Manage performance anxiety",
            "Maintain quality despite pressure",
            "Handle real-time feedback"
        ],
        escalation_pattern=[
            "Friendly audience, low stakes",
            "Critical audience appears",
            "Unexpected challenge during performance",
            "Major mistake - must recover publicly",
            "Complete exposure of inadequacy"
        ],
        limit_situations=["Struggle", "Uncertainty", "Guilt"]
    ),
    
    "campfire": EnvironmentContext(
        name="The Campfire (Room 051)",
        description="Vulnerable storytelling space requiring emotional openness",
        typical_constraints=[
            "Share authentically",
            "Receive others' stories",
            "Maintain trust atmosphere",
            "Navigate vulnerability"
        ],
        escalation_pattern=[
            "Surface-level sharing",
            "Deeper personal content",
            "Conflict or disagreement emerges",
            "Deep vulnerability triggered",
            "Existential communication attempted"
        ],
        limit_situations=["All - stories address limits vicariously"]
    ),
    
    "war_room": EnvironmentContext(
        name="The War Room (Room 035)",
        description="Crisis management where all resources focus on single problem",
        typical_constraints=[
            "Maintain clarity under pressure",
            "Coordinate rapid response",
            "Make decisions with incomplete information",
            "Sustain focus despite urgency"
        ],
        escalation_pattern=[
            "Emerging situation",
            "Situation confirmed as crisis",
            "Initial responses insufficient",
            "Resources depleting, stakes rising",
            "Complete approach must change"
        ],
        limit_situations=["All - crisis activates all limits"]
    ),
    
    "wilderness": EnvironmentContext(
        name="The Wilderness (Room 041)",
        description="Unmarked terrain requiring primal navigation and survival instincts",
        typical_constraints=[
            "Navigate without aids",
            "Manage physical needs",
            "Respond to environmental dangers",
            "Maintain orientation"
        ],
        escalation_pattern=[
            "Marked trail, clear conditions",
            "Trail disappears",
            "Weather changes",
            "Lost or disoriented",
            "Physical danger present"
        ],
        limit_situations=["Death", "Historical Determinedness"]
    ),
    
    "improv_stage": EnvironmentContext(
        name="The Improv Stage (Room 042)",
        description="Creative generation without planning - 'Yes, And' space",
        typical_constraints=[
            "Generate without judgment",
            "Build on others' contributions",
            "Maintain creative flow",
            "Suppress inner critic"
        ],
        escalation_pattern=[
            "Safe, supportive prompts",
            "Unexpected direction from partner",
            "Content pushes comfort zone",
            "Inner critic threatens shutdown",
            "Complete creative block"
        ],
        limit_situations=["Uncertainty"]
    ),
    
    "void": EnvironmentContext(
        name="The Void (Room 063+)",
        description="Confrontation with meaninglessness and existential limit",
        typical_constraints=[
            "Maintain presence despite emptiness",
            "Find ground when ground is absent",
            "Allow the void without fleeing",
            "Emerge transformed"
        ],
        escalation_pattern=[
            "Discomfort with stillness",
            "Anxiety rising",
            "Meaninglessness confronted",
            "Ego dissolution threatening",
            "Complete surrender or breakthrough"
        ],
        limit_situations=["Death", "The Questionable Nature of All Existence"]
    ),
}


class Environment:
    """
    Generates and manages encounter frames for agent simulation.
    
    Uses LLM to:
    - Generate contextually appropriate encounters
    - Escalate difficulty based on agent success
    - Introduce adversarial/novel situations
    - Assess agent responses
    """
    
    def __init__(
        self,
        context_name: str,
        model_name: str = "gemini-2.0-flash",
        auto_escalate: bool = True,
    ):
        if context_name not in CONTEXTS:
            available = ", ".join(CONTEXTS.keys())
            raise ValueError(f"Unknown context: {context_name}. Available: {available}")
        
        self.context = CONTEXTS[context_name]
        self.model = genai.GenerativeModel(model_name) if GEMINI_KEY else None
        self.auto_escalate = auto_escalate
        
        self.current_difficulty = EncounterDifficulty.EASY
        self.encounter_history: list[EncounterFrame] = []
        self.escalation_index = 0
    
    def generate_encounter(
        self,
        difficulty: Optional[EncounterDifficulty] = None,
        specific_constraint: Optional[str] = None,
    ) -> EncounterFrame:
        """
        Generate an encounter frame for the current context.
        
        Args:
            difficulty: Override difficulty level
            specific_constraint: Force a specific constraint type
        """
        if difficulty:
            self.current_difficulty = difficulty
        
        if not self.model:
            # Fallback: use pre-defined escalation pattern
            if self.escalation_index < len(self.context.escalation_pattern):
                desc = self.context.escalation_pattern[self.escalation_index]
            else:
                desc = self.context.escalation_pattern[-1]
            
            return EncounterFrame(
                description=desc,
                constraints=self.context.typical_constraints,
                difficulty=self.current_difficulty.value,
                category=self.context.name
            )
        
        # Use LLM to generate contextual encounter
        prompt = f"""Generate a specific situational challenge for this context:

CONTEXT: {self.context.name}
{self.context.description}

DIFFICULTY LEVEL: {self.current_difficulty.name} ({self.current_difficulty.value})

TYPICAL CONSTRAINTS in this context:
{chr(10).join('- ' + c for c in self.context.typical_constraints)}

ESCALATION PATTERN (we're at level {self.escalation_index + 1}):
{chr(10).join(f'{i+1}. {p}' for i, p in enumerate(self.context.escalation_pattern))}

{f'SPECIFIC CONSTRAINT TO INCLUDE: {specific_constraint}' if specific_constraint else ''}

Generate a SPECIFIC, CONCRETE encounter/challenge at this difficulty level.
Make it vivid and particular - not abstract.

Respond in JSON format:
{{
  "description": "<specific situation description, 1-2 sentences>",
  "constraints": ["<specific constraint 1>", "<specific constraint 2>"],
  "category": "<physical/social/cognitive/emotional>"
}}"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=400
                )
            )
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            data = json.loads(text)
            
            encounter = EncounterFrame(
                description=data["description"],
                constraints=data.get("constraints", []),
                difficulty=self.current_difficulty.value,
                category=data.get("category", "general")
            )
            
        except Exception as e:
            # Fallback
            encounter = EncounterFrame(
                description=self.context.escalation_pattern[
                    min(self.escalation_index, len(self.context.escalation_pattern) - 1)
                ],
                constraints=self.context.typical_constraints,
                difficulty=self.current_difficulty.value,
                category=self.context.name
            )
        
        self.encounter_history.append(encounter)
        return encounter
    
    def escalate(self) -> None:
        """Increase difficulty for next encounter."""
        self.escalation_index = min(
            self.escalation_index + 1,
            len(self.context.escalation_pattern) - 1
        )
        
        difficulties = list(EncounterDifficulty)
        current_idx = difficulties.index(self.current_difficulty)
        if current_idx < len(difficulties) - 1:
            self.current_difficulty = difficulties[current_idx + 1]
    
    def de_escalate(self) -> None:
        """Decrease difficulty for next encounter."""
        self.escalation_index = max(0, self.escalation_index - 1)
        
        difficulties = list(EncounterDifficulty)
        current_idx = difficulties.index(self.current_difficulty)
        if current_idx > 0:
            self.current_difficulty = difficulties[current_idx - 1]
    
    def assess_response(
        self,
        agent_action: str,
        encounter: EncounterFrame,
        agent_stance: str,
    ) -> float:
        """
        Assess how well the agent handled the encounter.
        Returns viability score 0.0 - 1.0.
        """
        if not self.model:
            import random
            return random.uniform(0.3, 0.9)
        
        prompt = f"""Assess how well this response addresses the challenge:

ENCOUNTER: {encounter.description}
CONSTRAINTS: {', '.join(encounter.constraints)}

AGENT'S STANCE: {agent_stance}
AGENT'S ACTION: {agent_action}

Rate the effectiveness on a scale of 0.0 to 1.0:
- 0.0-0.3: Completely mismatched, will fail
- 0.4-0.6: Partially effective, struggling
- 0.7-0.9: Effective handling
- 1.0: Perfect match

Respond with just a number between 0.0 and 1.0."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.2,
                    max_output_tokens=50
                )
            )
            score = float(response.text.strip())
            return max(0.0, min(1.0, score))
        except:
            import random
            return random.uniform(0.3, 0.8)
    
    def generate_encounter_sequence(
        self,
        length: int,
        pattern: str = "escalating"
    ) -> list[EncounterFrame]:
        """
        Generate a sequence of encounters.
        
        Args:
            length: Number of encounters
            pattern: "escalating", "flat", or "wave"
        """
        encounters = []
        
        for i in range(length):
            if pattern == "escalating":
                if i > 0 and i % 2 == 0:
                    self.escalate()
            elif pattern == "wave":
                if i > 0:
                    if i % 3 == 0:
                        self.escalate()
                    elif i % 5 == 0:
                        self.de_escalate()
            # "flat" keeps same difficulty
            
            encounters.append(self.generate_encounter())
        
        return encounters
    
    @classmethod
    def list_contexts(cls) -> list[str]:
        """List all available context names."""
        return list(CONTEXTS.keys())
    
    @classmethod
    def get_context_info(cls, name: str) -> Optional[EnvironmentContext]:
        """Get detailed info about a specific context."""
        return CONTEXTS.get(name)
