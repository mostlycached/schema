"""
ConatusAgent: The Dynamic Stance-Component Agent

This module implements the agent architecture from THESIS.md, using an LLM
to model semantic relationships, viability assessments, and affect generation.
"""

import os
import json
from dataclasses import dataclass, field
from typing import Optional, Callable
from enum import Enum
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)


class AgentMode(Enum):
    """The two dynamic modes from the thesis."""
    ADOPTION = "adoption"          # Optimization, refining current stance
    NOVELTY_SEARCH = "novelty_search"  # Trauma/discovery, seeking new stance


@dataclass
class FunctionalComponent:
    """
    An atomic unit of capability (motor, sensory, cognitive).
    These are the raw resources available to the system.
    """
    name: str
    description: str
    category: str  # "motor", "sensory", "cognitive", "affective"
    is_active: bool = False
    activation_weight: float = 0.0
    activation_history: list[float] = field(default_factory=list)
    
    def activate(self, weight: float = 1.0) -> None:
        self.is_active = True
        self.activation_weight = weight
        self.activation_history.append(weight)
    
    def deactivate(self) -> None:
        self.is_active = False
        self.activation_weight = 0.0
        self.activation_history.append(0.0)


@dataclass
class Stance:
    """
    A Higher Order Complex - a specific configuration/binding of Functional Components.
    Determines which FCs are active, which are inhibited, and how they coordinate.
    """
    name: str
    description: str
    core_components: list[str]      # Component names that define this stance
    active_weights: dict[str, float] = field(default_factory=dict)
    affect_register: str = ""       # The felt-sense name of this stance
    viability_history: list[float] = field(default_factory=list)
    
    def get_component_config(self) -> dict[str, float]:
        """Return the full component weight configuration."""
        return self.active_weights.copy()


@dataclass
class SimulationEvent:
    """A single event in the simulation log."""
    timestep: int
    mode: AgentMode
    encounter: str
    stance_name: str
    viability: float
    action_taken: str
    affect_register: str
    transition_occurred: bool = False
    new_stance_name: Optional[str] = None
    

class InterventionLevel(Enum):
    """Levels of human intervention in the simulation."""
    FULL_AUTO = "full_auto"           # No human input
    OBSERVE = "observe"               # Human sees output, no input
    ENCOUNTER_INJECT = "encounter_inject"  # Human can inject encounters
    STANCE_GUIDE = "stance_guide"     # Human can suggest stance changes
    FULL_CONTROL = "full_control"     # Human approves all transitions


class AssessmentMode(Enum):
    """How to evaluate viability."""
    THERAPEUTIC = "therapeutic"  # Default, tends toward feel-good
    REALISTIC = "realistic"      # Harsh, materialist assessment
    ADVERSARIAL = "adversarial"  # Maximally critical


# =============================================================================
# MUSES - Inspirational Generators
# =============================================================================

MUSES = {
    "whitman": "Speak as Walt Whitman: Expand to contain multitudes. Celebrate the body electric. Affirm contradiction. Use cataloging and expansive breath.",
    "nietzsche": "Speak as Nietzsche: Seek self-overcoming. Despise comfort. Affirm the dangerous perhaps. Use aphoristic, hammer-like intensity.",
    "bataille": "Speak as Bataille: Seek the limit-experience. Expend energy without reserve. Embrace heterology and waste. Focus on the sacred and profane body.",
    "sloterdijk": "Speak as Sloterdijk: Analyze the sphere of immunity. Describe the anthropotechnic exercise. Focus on vertical tension and spatial containment.",
    "deleuze": "Speak as Deleuze: Create concepts. Seek the body without organs. Trace lines of flight. Avoid arborescent structures; be rhizomatic.",
    "rilke": "Speak as Rilke: Turn inward to the open. Praise the fragile thing. Seek the transformation of the visible into the invisible.",
    "barthes": "Speak as Barthes: Distinguish pleasure from bliss (jouissance). Seek the neutral. Focus on the grain of the voice and the eroticism of the text.",
    "serres": "Speak as Michel Serres: Mix the senses. Follow the parasite. Bridge the hard and soft. Use topological metaphors and fluid dynamics.",
    "von_foerster": "Speak as Heinz von Foerster: Act to increase choices. Construct reality through recursion. Focus on the observer observing.",
    "goffman": "Speak as Erving Goffman: Analyze the performance. Expose the backstage. Focus on impression management and face-work.",
    "shakira": "Speak as Shakira: The hips don't lie. Trust the primal rhythm. Ground truth in the moving body. Be wolf-like and unapologetic.",
    "malabou": "Speak as Catherine Malabou: Seek plasticity (destructible transformability). Explore the accident. Focus on brain-like adaptability without central command.",
}


class ConatusAgent:
    """
    The Dynamic Stance-Component Agent.
    
    Uses LLM for:
    - Viability assessment of stance against encounter
    - Detection of stance failure (trauma trigger)
    - Generation of new stances and affect registers
    - Semantic understanding of component coordination
    """
    
    def __init__(
        self,
        name: str,
        context: str,
        functional_components: list[FunctionalComponent],
        initial_stance: Stance,
        viability_threshold: float = 0.4,
        model_name: str = "gemini-2.0-flash",
        intervention_level: InterventionLevel = InterventionLevel.FULL_AUTO,
        human_input_callback: Optional[Callable[[str], str]] = None,
        assessment_mode: AssessmentMode = AssessmentMode.REALISTIC,
        harshness: float = 0.7,
    ):
        self.name = name
        self.context = context
        self.components = {fc.name: fc for fc in functional_components}
        self.current_stance = initial_stance
        self.available_stances = [initial_stance]
        self.viability_threshold = viability_threshold
        self.mode = AgentMode.ADOPTION
        self.intervention_level = intervention_level
        self.human_input_callback = human_input_callback
        self.assessment_mode = assessment_mode
        self.harshness = harshness
        
        self.model = genai.GenerativeModel(model_name) if GEMINI_KEY else None
        self.history: list[SimulationEvent] = []
        self.timestep = 0
        
        # Apply initial stance
        self._apply_stance(initial_stance)
    
    def _apply_stance(self, stance: Stance) -> None:
        """Activate/deactivate components according to stance configuration."""
        for name, component in self.components.items():
            if name in stance.active_weights:
                component.activate(stance.active_weights[name])
            else:
                component.deactivate()
        self.current_stance = stance
    
    def _get_active_components(self) -> list[FunctionalComponent]:
        """Get currently active components."""
        return [c for c in self.components.values() if c.is_active]
    
    def _get_dormant_components(self) -> list[FunctionalComponent]:
        """Get currently inactive (dormant) components."""
        return [c for c in self.components.values() if not c.is_active]
    
    def _llm_assess_viability(self, encounter: str) -> tuple[float, str]:
        """
        Use LLM to assess how well the current stance handles the encounter.
        Returns (viability_score, reasoning).
        """
        if not self.model:
            import random
            return random.uniform(0.2, 0.8), "No LLM available"
        
        active_components = self._get_active_components()
        component_desc = "\n".join([
            f"- {c.name} ({c.category}): {c.description}"
            for c in active_components
        ])
        
        # Different prompts based on assessment mode
        if self.assessment_mode == AssessmentMode.THERAPEUTIC:
            critique_instruction = ""
            scoring_guide = ""
        else:
            harshness_str = f"{self.harshness:.1f}/1.0"
            critique_instruction = f"""

CRITICAL EVALUATION MODE (harshness: {harshness_str}):
- Do NOT reward stances for "feeling" right. Evaluate ACTUAL capability.
- A stance that "accepts" failure or "finds peace" with incapacity is still FAILING.
- Material problems require material solutions, not reframes.
- Don't confuse comfort-seeking with genuine adaptation.
- Ask: Does this stance ACCOMPLISH the task, or just feel meaningful while failing?"""
            
            scoring_guide = """

SCORING (BE HARSH):
- 0.0-0.3: Cannot solve the problem. Fails the material constraint.
- 0.4-0.5: Partial. Some elements work, core problem unsolved.
- 0.6-0.7: Mostly works but with gaps. Functional, not optimal.
- 0.8-1.0: Actually solves the problem. Demonstrable effectiveness.

Do NOT inflate scores. The therapeutic default is too generous. Correct for this."""
        
        prompt = f"""You are evaluating an agent's ability to handle a situation.

CONTEXT: {self.context}

CURRENT STANCE: {self.current_stance.name}
Description: {self.current_stance.description}
Affect Register: {self.current_stance.affect_register}

ACTIVE FUNCTIONAL COMPONENTS:
{component_desc}

ENCOUNTER/CHALLENGE:
{encounter}{critique_instruction}

Assess how well this stance can handle this encounter.
Consider:
1. Do the active components ACTUALLY address the constraints?
2. Is there a mismatch between what's needed and what's available?
3. Would different components be more effective?
4. Is this stance genuinely capable or just comfortable?{scoring_guide}

Respond in JSON format:
{{
  "viability_score": <float between 0.0 and 1.0>,
  "reasoning": "<brief explanation>",
  "constraint_met": <true/false>,
  "is_genuine_solution": <true/false>,
  "what_remains_unsolved": "<if applicable>"
}}"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=500
                )
            )
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            data = json.loads(text)
            return float(data["viability_score"]), data["reasoning"]
        except Exception as e:
            import random
            return random.uniform(0.3, 0.7), f"LLM error: {e}"
    
    def _llm_generate_new_stance(
        self, 
        encounter: str,
        muse: Optional[str] = None
    ) -> Stance:
        """
        Use LLM to generate a new stance after trauma/failure.
        Optionally inspired by a Muse (Inspirational Generator).
        """
        if not self.model:
            # Fallback: create a generic new stance
            dormant = self._get_dormant_components()
            if dormant:
                new_weights = {c.name: 0.8 for c in dormant[:3]}
                return Stance(
                    name="Emergent Stance",
                    description="Automatically generated stance",
                    core_components=list(new_weights.keys()),
                    active_weights=new_weights,
                    affect_register="novel sensation"
                )
            return self.current_stance
        
        active = self._get_active_components()
        dormant = self._get_dormant_components()
        
        active_desc = "\n".join([f"- {c.name}: {c.description}" for c in active])
        dormant_desc = "\n".join([f"- {c.name}: {c.description}" for c in dormant])
        
        # Muse injection
        muse_prompt = ""
        if muse and muse.lower() in MUSES:
            muse_prompt = f"""
INSPIRATION:
{MUSES[muse.lower()]}
Let this voice guide the naming, description, and affect of the new stance.
Make it stylistically distinct but functionally grounded."""
        
        prompt = f"""You are helping an agent discover a new mode of being after its current approach failed.

CONTEXT: {self.context}

FAILED STANCE: {self.current_stance.name}
- It could not handle: {encounter}

CORE COMPONENTS (to be inhibited/reduced):
{active_desc}

DORMANT COMPONENTS (available for activation):
{dormant_desc}
{muse_prompt}

Following the Novelty Search process:
1. Identify which core components should be inhibited
2. Identify which dormant components should be activated
3. Synthesize a NEW stance configuration
4. Name the new AFFECT REGISTER (the felt-sense of this new coordination)

The affect register should be evocative - like "grounded fluidity" or "shearing awareness".

Respond in JSON format:
{{
  "new_stance_name": "<evocative name for the new stance>",
  "description": "<what this stance enables>",
  "components_to_inhibit": ["<component names>"],
  "components_to_activate": ["<component names>"],
  "weights": {{"<component_name>": <weight 0.0-1.0>}},
  "affect_register": "<evocative name for the new felt-sense>",
  "rationale": "<why this configuration might work>"
}}"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.5,  # Lower for consistency
                    max_output_tokens=600
                )
            )
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            data = json.loads(text)
            
            new_stance = Stance(
                name=data["new_stance_name"],
                description=data["description"],
                core_components=data["components_to_activate"],
                active_weights=data.get("weights", {}),
                affect_register=data["affect_register"]
            )
            return new_stance
            
        except Exception as e:
            # Fallback
            dormant = self._get_dormant_components()
            if dormant:
                new_weights = {c.name: 0.7 for c in dormant[:2]}
                return Stance(
                    name="Emergency Adaptation",
                    description=f"Fallback stance after failure: {e}",
                    core_components=list(new_weights.keys()),
                    active_weights=new_weights,
                    affect_register="uncertain groping"
                )
            return self.current_stance
    
    def _request_human_input(self, prompt_type: str, context: str) -> Optional[str]:
        """Request input from human if intervention level allows."""
        if self.human_input_callback is None:
            return None
            
        if self.intervention_level == InterventionLevel.FULL_AUTO:
            return None
        elif self.intervention_level == InterventionLevel.OBSERVE:
            return None
        elif self.intervention_level == InterventionLevel.ENCOUNTER_INJECT:
            if prompt_type == "encounter":
                return self.human_input_callback(context)
        elif self.intervention_level == InterventionLevel.STANCE_GUIDE:
            if prompt_type in ["encounter", "stance_suggestion"]:
                return self.human_input_callback(context)
        elif self.intervention_level == InterventionLevel.FULL_CONTROL:
            return self.human_input_callback(context)
        
        return None
    
    def step(self, encounter: str) -> SimulationEvent:
        """
        Execute one step of the agent simulation.
        
        1. Sense the encounter
        2. Assess viability of current stance
        3. If viable: ADOPTION mode (refine)
        4. If not viable: NOVELTY SEARCH (trauma/discovery)
        """
        self.timestep += 1
        
        # Check for human encounter injection
        human_encounter = self._request_human_input(
            "encounter",
            f"Current encounter: {encounter}\nProvide alternative encounter or press Enter:"
        )
        if human_encounter:
            encounter = human_encounter
        
        # Assess viability
        viability, reasoning = self._llm_assess_viability(encounter)
        self.current_stance.viability_history.append(viability)
        
        transition_occurred = False
        new_stance_name = None
        action_taken = ""
        
        if viability >= self.viability_threshold:
            # ADOPTION MODE: stance is working, refine it
            self.mode = AgentMode.ADOPTION
            action_taken = f"Adoption: {reasoning}"
        else:
            # NOVELTY SEARCH MODE: stance has failed (trauma)
            self.mode = AgentMode.NOVELTY_SEARCH
            
            # Check if human wants to guide stance change
            if self.intervention_level in [
                InterventionLevel.STANCE_GUIDE,
                InterventionLevel.FULL_CONTROL
            ]:
                guidance = self._request_human_input(
                    "stance_suggestion",
                    f"Stance '{self.current_stance.name}' failed (viability: {viability:.2f}).\n"
                    f"Reason: {reasoning}\n"
                    f"Suggest new stance approach or press Enter for auto:"
                )
                # Could incorporate guidance into stance generation
            
            # Generate new stance
            new_stance = self._llm_generate_new_stance(encounter)
            
            if self.intervention_level == InterventionLevel.FULL_CONTROL:
                approval = self._request_human_input(
                    "approval",
                    f"Proposed new stance: {new_stance.name}\n"
                    f"Affect: {new_stance.affect_register}\n"
                    f"Approve? (y/n):"
                )
                if approval and approval.lower() != 'y':
                    new_stance = self.current_stance  # Keep old stance
            
            if new_stance.name != self.current_stance.name:
                transition_occurred = True
                new_stance_name = new_stance.name
                self._apply_stance(new_stance)
                self.available_stances.append(new_stance)
                action_taken = f"Novelty Search: Transitioned to '{new_stance.name}' ({new_stance.affect_register})"
            else:
                action_taken = f"Novelty Search attempted but retained stance"
        
        # Log the event
        event = SimulationEvent(
            timestep=self.timestep,
            mode=self.mode,
            encounter=encounter,
            stance_name=self.current_stance.name,
            viability=viability,
            action_taken=action_taken,
            affect_register=self.current_stance.affect_register,
            transition_occurred=transition_occurred,
            new_stance_name=new_stance_name
        )
        self.history.append(event)
        
        return event
    
    def run(self, encounters: list[str], verbose: bool = True) -> list[SimulationEvent]:
        """Run the agent through a series of encounters."""
        events = []
        for encounter in encounters:
            event = self.step(encounter)
            events.append(event)
            
            if verbose:
                mode_str = "🔄 ADOPTION" if event.mode == AgentMode.ADOPTION else "⚡ NOVELTY"
                trans_str = " → TRANSITION!" if event.transition_occurred else ""
                print(f"\n[{event.timestep}] {mode_str}{trans_str}")
                print(f"  Encounter: {encounter[:60]}...")
                print(f"  Stance: {event.stance_name}")
                print(f"  Viability: {event.viability:.2f}")
                print(f"  Action: {event.action_taken}")
                if event.transition_occurred:
                    print(f"  New Affect: {event.affect_register}")
        
        return events
    
    def get_summary(self) -> dict:
        """Get a summary of the simulation run."""
        transitions = [e for e in self.history if e.transition_occurred]
        viabilities = [e.viability for e in self.history]
        
        return {
            "total_steps": len(self.history),
            "transitions": len(transitions),
            "stances_discovered": len(self.available_stances),
            "avg_viability": sum(viabilities) / len(viabilities) if viabilities else 0,
            "final_stance": self.current_stance.name,
            "final_affect": self.current_stance.affect_register,
            "stance_history": [e.stance_name for e in self.history],
            "all_affect_registers": [s.affect_register for s in self.available_stances]
        }
