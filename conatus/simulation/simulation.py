"""
Simulation Module

Orchestrates the agent, environment, and critic in a unified loop.
Supports both THESIS modes:
- Adoption (viability >= threshold): refine current stance
- Novelty Search (viability < threshold): generate new stance

Also supports force_novelty mode for maximum stance diversity.
"""

import os
import json
import random
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))

from conatus.simulation.critic import Critic, CriticConfig, CriticFeedback
from conatus.simulation.agent import MUSES


# =============================================================================
# ENVIRONMENT CONFIGURATION
# =============================================================================

@dataclass
class EnvironmentConfig:
    """
    Environment parameters that exist OUTSIDE the agent's model.
    """
    stability: float = 0.5  # 0.0 = chaotic, 1.0 = predictable
    hidden_volatility: float = 0.0  # Unmodeled perturbation
    escalation_rate: float = 0.1  # How quickly difficulty increases
    
    @classmethod
    def for_context(cls, context: str) -> 'EnvironmentConfig':
        """Get default config for a context."""
        configs = {
            # High-pressure physical
            "forge": cls(stability=0.2, hidden_volatility=0.4, escalation_rate=0.2),
            "arena": cls(stability=0.3, hidden_volatility=0.3, escalation_rate=0.15),
            
            # Performance/creative
            "dance": cls(stability=0.4, hidden_volatility=0.3, escalation_rate=0.1),
            "improv_stage": cls(stability=0.3, hidden_volatility=0.4, escalation_rate=0.15),
            
            # Social/relational
            "campfire": cls(stability=0.7, hidden_volatility=0.2, escalation_rate=0.05),
            "child_rearing": cls(stability=0.5, hidden_volatility=0.4, escalation_rate=0.1),
            
            # Hostile/survival
            "wilderness": cls(stability=0.2, hidden_volatility=0.5, escalation_rate=0.2),
            "war_room": cls(stability=0.2, hidden_volatility=0.5, escalation_rate=0.25),
            "void": cls(stability=0.1, hidden_volatility=0.6, escalation_rate=0.3),
            
            # Craft
            "woodworking": cls(stability=0.6, hidden_volatility=0.2, escalation_rate=0.08),
            "dojo": cls(stability=0.5, hidden_volatility=0.3, escalation_rate=0.12),
        }
        return configs.get(context, cls())


# =============================================================================
# SIMULATION STEP RECORD
# =============================================================================

@dataclass
class StepRecord:
    """Record of a single simulation step."""
    step: int
    encounter: str
    initial_stance: str
    final_stance: str
    final_affect: str
    mode: str  # ADOPTION or NOVELTY_SEARCH
    proposals: List[dict] = field(default_factory=list)
    critic_feedback: Optional[CriticFeedback] = None
    environment_viability: float = 0.0
    environment_outcome: str = ""
    muse: Optional[str] = None


# =============================================================================
# SIMULATION
# =============================================================================

class Simulation:
    """
    Unified simulation orchestrator.
    
    Supports two modes from THESIS.md:
    - Adoption Mode (viability >= threshold): refine current stance
    - Novelty Search Mode (viability < threshold): generate new stance
    
    Also supports force_novelty for maximum stance diversity.
    """
    
    def __init__(
        self,
        agent,  # ConatusAgent
        env_config: EnvironmentConfig = None,
        model_name: str = "gemini-2.0-flash",
        force_novelty: bool = False,  # Always generate new stances
        use_vector_store: bool = False,  # Per-encounter component retrieval
        component_count: int = 30,
        muse: str = None,  # Configurable muse for stance generation
    ):
        self.agent = agent
        self.env_config = env_config or EnvironmentConfig()
        self.critic = Critic(CriticConfig(), model_name)
        self.model = genai.GenerativeModel(model_name)
        
        self.force_novelty = force_novelty
        self.use_vector_store = use_vector_store
        self.component_count = component_count
        self.muse = muse  # Store configured muse
        
        # Vector store (lazy loaded)
        self._vector_store = None
        
        self.history: List[StepRecord] = []
        self.timestep = 0
    
    def _get_vector_store(self):
        """Lazy-load vector store."""
        if self._vector_store is None and self.use_vector_store:
            from conatus.simulation.components import ComponentVectorStore
            self._vector_store = ComponentVectorStore(
                persist_path=os.path.join(os.path.dirname(__file__), "component_db")
            )
        return self._vector_store
    
    def _retrieve_components_for_encounter(self, encounter: str):
        """Retrieve components specific to this encounter."""
        store = self._get_vector_store()
        if store is None:
            return
        
        from conatus.simulation.agent import FunctionalComponent
        
        retrieved = store.search_for_encounter(
            encounter,
            context=self.agent.context,
            limit=self.component_count
        )
        
        components = [
            FunctionalComponent(
                name=c.name,
                description=c.description,
                category=c.modality
            )
            for c in retrieved
        ]
        
        self.agent.functional_components = components
    
    def _apply_hidden_perturbation(self, base_viability: float) -> float:
        """Apply environment's hidden volatility."""
        perturbation = random.gauss(0, self.env_config.hidden_volatility)
        return max(0.0, min(1.0, base_viability + perturbation))
    
    def _environment_assess(
        self,
        encounter: str,
        stance: str,
        components: List[str],
    ) -> tuple:
        """Environment's independent assessment of stance viability."""
        
        prompt = f"""You are the ENVIRONMENT, an independent assessor of whether an agent's stance actually works.

Environment stability: {self.env_config.stability:.1f} (lower = harder to predict)

THE CHALLENGE:
{encounter}

AGENT'S STANCE: {stance}
ACTIVE COMPONENTS: {', '.join(components)}

ASSESS OBJECTIVELY:
1. Can this stance handle the MATERIAL demands of the encounter?
2. Are there aspects of the situation the agent hasn't accounted for?
3. What could go wrong that the agent isn't anticipating?

Respond in JSON:
{{
  "viability": <0.0-1.0>,
  "outcome": "<SUCCESS|PARTIAL|FAILURE>",
  "reasoning": "<brief explanation>"
}}"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    max_output_tokens=300
                )
            )
            
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            data = json.loads(text)
            base_viability = float(data["viability"])
            final_viability = self._apply_hidden_perturbation(base_viability)
            
            if final_viability < 0.3:
                outcome = "FAILURE"
            elif final_viability < 0.6:
                outcome = "PARTIAL"
            else:
                outcome = "SUCCESS"
            
            return final_viability, outcome
            
        except Exception:
            return random.uniform(0.2, 0.5), "PARTIAL"
    
    def _generate_with_feedback(
        self,
        encounter: str,
        rejection_history: List[dict],
        muse: Optional[str] = None,
    ):
        """Generate new stance informed by rejection feedback."""
        active = self.agent._get_active_components()
        dormant = self.agent._get_dormant_components()
        
        active_desc = "\n".join([f"- {c.name}: {c.description}" for c in active])
        dormant_desc = "\n".join([f"- {c.name}: {c.description}" for c in dormant])
        
        rejection_context = ""
        if rejection_history:
            rejection_context = "\n\nPREVIOUS REJECTED PROPOSALS:\n"
            for i, rej in enumerate(rejection_history, 1):
                rejection_context += f"\n{i}. {rej['name']}: {rej['feedback'].reasoning}\n"
            rejection_context += "\nYou MUST address this feedback."
        
        # Muse injection
        muse_prompt = ""
        if muse and muse.lower() in MUSES:
            muse_prompt = f"""
INSPIRATION:
{MUSES[muse.lower()]}
Let this voice guide the naming, description, and affect of the new stance.
Make it stylistically distinct but functionally grounded."""

        prompt = f"""Generate a GENUINELY EFFECTIVE stance after previous approaches were rejected.

CONTEXT: {self.agent.context}
ENCOUNTER: {encounter}

ACTIVE COMPONENTS:
{active_desc}

DORMANT COMPONENTS:
{dormant_desc}
{rejection_context}
{muse_prompt}

Respond in JSON:
{{
  "name": "<stance name>",
  "description": "<what this stance enables>",
  "components_to_activate": ["<component names>"],
  "affect_register": "<2-3 word evocative name for the felt-sense>",
  "affect_description": "<what this affect FEELS LIKE from inside - sensations, textures, emotional qualities>",
  "embodiment": "<HOW to enact: body (breath, posture), equipment/tools, environment/space/others, and attention>"
}}"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.6,
                    max_output_tokens=1000
                )
            )
            
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            data = json.loads(text)
            
            from conatus.simulation.agent import Stance
            return Stance(
                name=data["name"],
                description=data["description"],
                core_components=data["components_to_activate"],
                active_weights={c: 0.8 for c in data["components_to_activate"]},
                affect_register=data["affect_register"],
                affect_description=data.get("affect_description", ""),
                embodiment=data.get("embodiment", "")
            )
            
        except Exception:
            return self.agent._llm_generate_new_stance(encounter)
    
    def step(self, encounter: str) -> StepRecord:
        """
        Execute one simulation step.
        
        1. Optionally retrieve encounter-specific components
        2. Assess viability OR force novelty search
        3. Generate stance if needed
        4. Submit to critic
        5. Environment assesses outcome
        """
        self.timestep += 1
        old_stance = self.agent.current_stance.name
        
        # Per-encounter component retrieval
        if self.use_vector_store:
            self._retrieve_components_for_encounter(encounter)
        
        proposals = []
        rejection_history = []
        
        # Decide mode
        # Use configured muse or select randomly
        if self.muse:
            current_muse = self.muse
        else:
            import random
            from conatus.simulation.agent import MUSES
            current_muse = random.choice(list(MUSES.keys()))
        
        if self.force_novelty:
            mode = "NOVELTY_SEARCH"
            should_generate = True
        else:
            viability, _ = self.agent._llm_assess_viability(encounter)
            if viability >= self.agent.viability_threshold:
                mode = "ADOPTION"
                should_generate = False
            else:
                mode = "NOVELTY_SEARCH"
                should_generate = True
        
        # Generate or adopt
        accepted = False
        proposed = self.agent.current_stance
        feedback = None
        
        if should_generate:
            max_attempts = self.critic.config.max_rejections + 1
            
            for attempt in range(max_attempts):
                # Generate new stance
                if rejection_history:
                    proposed = self._generate_with_feedback(encounter, rejection_history, muse=current_muse)
                else:
                    proposed = self.agent._llm_generate_new_stance(encounter, muse=current_muse)
                
                proposed_desc = f"{proposed.name}: {proposed.description}"
                
                # Critic evaluation
                feedback = self.critic.evaluate(
                    encounter=encounter,
                    proposed_stance=proposed_desc,
                    proposed_affect=proposed.affect_register,
                    old_stance=old_stance,
                )
                
                proposals.append({
                    "attempt": attempt + 1,
                    "name": proposed.name,
                    "description": proposed.description,
                    "affect": proposed.affect_register,
                    "affect_description": proposed.affect_description,
                    "components": proposed.core_components,
                    "embodiment": proposed.embodiment,
                    "feedback": feedback,
                })
                
                if not self.critic.is_rejected(feedback):
                    accepted = True
                    break
                else:
                    rejection_history.append({
                        "name": proposed.name,
                        "feedback": feedback,
                    })
            
            # Apply the stance
            self.agent._apply_stance(proposed)
        
        # Environment assessment
        active_components = list(self.agent.current_stance.active_weights.keys())
        env_viability, env_outcome = self._environment_assess(
            encounter=encounter,
            stance=f"{self.agent.current_stance.name}: {self.agent.current_stance.description}",
            components=active_components,
        )
        
        record = StepRecord(
            step=self.timestep,
            encounter=encounter,
            initial_stance=old_stance,
            final_stance=self.agent.current_stance.name,
            final_affect=self.agent.current_stance.affect_register,
            mode=mode,
            proposals=proposals,
            critic_feedback=feedback,
            environment_viability=env_viability,
            environment_outcome=env_outcome,
            muse=current_muse,
        )
        
        self.history.append(record)
        return record
    
    def run(self, encounters: List[str]) -> List[StepRecord]:
        """Run simulation for all encounters."""
        records = []
        for encounter in encounters:
            record = self.step(encounter)
            records.append(record)
        return records
    
    def get_summary(self) -> dict:
        """Get simulation summary."""
        successes = sum(1 for r in self.history if r.environment_outcome == "SUCCESS")
        partials = sum(1 for r in self.history if r.environment_outcome == "PARTIAL")
        failures = sum(1 for r in self.history if r.environment_outcome == "FAILURE")
        
        total_proposals = sum(len(r.proposals) for r in self.history)
        total_rejections = sum(
            sum(1 for p in r.proposals if self.critic.is_rejected(p.get("feedback", CriticFeedback("VALID", 1.0, "", "", "NEUTRAL", False))))
            for r in self.history
        )
        
        return {
            "total_steps": len(self.history),
            "successes": successes,
            "partials": partials,
            "failures": failures,
            "total_proposals": total_proposals,
            "total_rejections": total_rejections,
            "rejection_rate": total_rejections / total_proposals if total_proposals > 0 else 0,
        }


# =============================================================================
# REPORT GENERATION
# =============================================================================

def generate_report(
    sim: Simulation,
    experiment_name: str,
    description: str,
    output_path: str = None,
) -> str:
    """Generate markdown report from simulation history."""
    
    lines = [
        f"# {experiment_name}",
        "",
        f"> {description}",
        "",
        "---",
        "",
        "## Configuration",
        "",
        "| Parameter | Value |",
        "|-----------|-------|",
        f"| Muse | {sim.muse or 'random'} |",
        f"| Environment Stability | {sim.env_config.stability} |",
        f"| Force Novelty | {sim.force_novelty} |",
        f"| Per-Encounter Components | {sim.use_vector_store} |",
        "",
        "---",
        "",
        "## Simulation Trace",
        "",
    ]
    
    outcome_icons = {"SUCCESS": "✅", "PARTIAL": "⚠️", "FAILURE": "❌"}
    
    for record in sim.history:
        icon = outcome_icons.get(record.environment_outcome, "❓")
        lines.extend([
            f"### Step {record.step}: {icon} {record.environment_outcome}",
            "",
            f"**Encounter**: {record.encounter}",
            "",
            f"**Mode**: {record.mode}",
            "",
        ])
        
        if record.muse:
            lines.extend([
                f"**Muse**: {record.muse.title()}",
                "",
            ])
            
        lines.extend([
            f"**Initial Stance**: {record.initial_stance}",
            "",
        ])
        
        if record.proposals:
            lines.append("#### Proposals")
            for p in record.proposals:
                verdict = p["feedback"].verdict if p["feedback"] else "N/A"
                score = p["feedback"].score if p["feedback"] else 0
                lines.extend([
                    "",
                    f"**{p['name']}** ({verdict}, {score:.2f})",
                    "",
                    f"*{p['description']}*",
                    "",
                ])
                # Add components if available
                if p.get("components"):
                    component_list = ", ".join(p["components"])
                    lines.extend([
                        f"**Components**: {component_list}",
                        "",
                    ])
                # Add embodiment instructions if available
                if p.get("embodiment"):
                    lines.extend([
                        "**How to Embody**:",
                        f"> {p['embodiment']}",
                        "",
                    ])
                # Add affect with description
                affect_line = f"**Affect**: \"{p['affect']}\""
                if p.get("affect_description"):
                    lines.extend([
                        affect_line,
                        f"> {p['affect_description']}",
                        "",
                    ])
                else:
                    lines.extend([affect_line, ""])
                # Add dimensional analysis if available
                if p["feedback"] and hasattr(p["feedback"], 'dimensions') and p["feedback"].dimensions:
                    lines.append("##### Dimensional Analysis")
                    lines.append("")
                    for dim in p["feedback"].dimensions:
                        lines.append(f"- **{dim.dimension}**: {dim.insight}")
                    lines.append("")
                # Add synthesis
                if p["feedback"] and p["feedback"].reasoning:
                    lines.append(f"> **Synthesis**: {p['feedback'].reasoning}")
                    lines.append("")
        
        lines.extend([
            f"**Final Stance**: {record.final_stance}",
            "",
            f"**Environment Viability**: {record.environment_viability:.2f}",
            "",
            "---",
            "",
        ])
    
    # Summary
    summary = sim.get_summary()
    lines.extend([
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Total Steps | {summary['total_steps']} |",
        f"| Successes | {summary['successes']} |",
        f"| Partials | {summary['partials']} |",
        f"| Failures | {summary['failures']} |",
        f"| Total Proposals | {summary['total_proposals']} |",
        f"| Rejection Rate | {summary['rejection_rate']:.0%} |",
        "",
        "---",
        "",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
    ])
    
    report = "\n".join(lines)
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"✓ Report saved to {output_path}")
    
    return report
