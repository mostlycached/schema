"""
Biography Module: Longitudinal Life Simulation

Extends the Conatus simulation from single-moment stances to life trajectories
spanning years and decades. Tracks the accumulation of:
- Habitus: Dispositions formed through repeated stance patterns
- Commitments: Bindings to institutions, relationships, projects
- Repertoire: All stances successfully deployed
- Wounds: Marks left by failures and limit-situations

Temporal structure:
- Biography (decades) → Phase (years) → Encounters (current granularity)
"""

import os
import json
import random
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from datetime import datetime
from enum import Enum

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))


# =============================================================================
# TEMPORAL ARC PATTERNS
# =============================================================================

class PhaseArc(Enum):
    """How a life phase unfolds."""
    ASCENT = "ascent"           # Building, growing, accumulating
    PLATEAU = "plateau"         # Maintaining, consolidating
    DESCENT = "descent"         # Declining, losing ground
    CRISIS = "crisis"           # Acute rupture, limit-situation
    DRIFT = "drift"             # Slow, unnoticed change
    REBIRTH = "rebirth"         # Discovery of new mode after crisis


# =============================================================================
# ACCUMULATING STRUCTURES
# =============================================================================

@dataclass
class Habitus:
    """
    Accumulated dispositions from repeated stance patterns.
    
    This is Bourdieu's concept: structured structuring structures.
    What stances have become second nature? What affects come easily
    or are avoided?
    """
    # Stances that have become default dispositions
    default_stances: Dict[str, float] = field(default_factory=dict)  # name → strength
    
    # Affects that have become skilled (come easily)
    skilled_affects: List[str] = field(default_factory=list)
    
    # Affects that are charged (difficult, avoided, trigger wounds)
    charged_affects: List[str] = field(default_factory=list)
    
    # Components that have been heavily trained
    trained_components: Dict[str, int] = field(default_factory=dict)  # name → activation count
    
    def record_stance(self, stance_name: str, affect: str, components: List[str]) -> None:
        """Record a stance usage, strengthening dispositions."""
        # Strengthen this stance as a disposition
        self.default_stances[stance_name] = self.default_stances.get(stance_name, 0) + 0.1
        
        # After 5+ uses, affect becomes skilled
        if self.default_stances.get(stance_name, 0) >= 0.5 and affect not in self.skilled_affects:
            self.skilled_affects.append(affect)
        
        # Track component training
        for comp in components:
            self.trained_components[comp] = self.trained_components.get(comp, 0) + 1
    
    def record_wound(self, affect: str) -> None:
        """Mark an affect as charged due to failure/trauma."""
        if affect not in self.charged_affects:
            self.charged_affects.append(affect)
    
    def get_disposition_strength(self, stance_name: str) -> float:
        """How strongly is this stance a disposition?"""
        return min(1.0, self.default_stances.get(stance_name, 0))


@dataclass
class Commitment:
    """
    A binding to an institution, relationship, or project.
    
    Commitments constrain what encounters are available and what
    stances are appropriate. They have duration and exit conditions.
    """
    name: str
    institution: str
    started_age: float
    expected_duration_years: float
    constraints: List[str] = field(default_factory=list)
    benefits: List[str] = field(default_factory=list)
    exit_triggers: List[str] = field(default_factory=list)
    is_active: bool = True
    ended_age: Optional[float] = None
    exit_reason: Optional[str] = None


@dataclass
class Wound:
    """
    A mark left by failure or limit-situation.
    
    Not just a record but an active influence: wounds make certain
    affects charged, certain stances harder to access.
    """
    description: str
    age_incurred: float
    phase: str
    charged_affects: List[str] = field(default_factory=list)
    inhibited_components: List[str] = field(default_factory=list)
    healed: bool = False
    healing_narrative: Optional[str] = None


# =============================================================================
# LIFE PHASE
# =============================================================================

@dataclass
class LifePhase:
    """
    A distinct period in a biography.
    
    Phases are the mid-level temporal unit: graduate school, first job,
    marriage, midlife crisis, late career, etc.
    """
    name: str
    institution: str
    age_start: float
    age_end: Optional[float] = None  # None if ongoing
    arc: PhaseArc = PhaseArc.PLATEAU
    
    # What commitments define this phase
    central_commitments: List[str] = field(default_factory=list)
    
    # Encounter patterns typical of this phase
    encounter_types: List[str] = field(default_factory=list)
    
    # How the phase ended (if it did)
    exit_trigger: Optional[str] = None
    exit_narrative: Optional[str] = None


# =============================================================================
# BIOGRAPHY STATE
# =============================================================================

@dataclass 
class BiographyState:
    """
    The accumulated state across an entire life trajectory.
    
    This is passed between phases and modified by each.
    Now includes relational identity (Others) and internalized voices.
    """
    name: str
    current_age: float
    habitus: Habitus
    active_commitments: List[Commitment]
    repertoire: List[str]  # Names of all stances ever successfully used
    wounds: List[Wound]
    current_phase: Optional[LifePhase] = None
    phase_history: List[LifePhase] = field(default_factory=list)
    
    # Relational identity (the Other)
    relationships: Dict[str, 'Relationship'] = field(default_factory=dict)  # name -> Relationship
    recognition_events: List['RecognitionEvent'] = field(default_factory=list)
    internalized_voices: List['InternalizedVoice'] = field(default_factory=list)
    
    # Fortuna events that occurred
    fortuna_events: List['FortunaEvent'] = field(default_factory=list)
    
    def enter_phase(self, phase: LifePhase) -> None:
        """Begin a new life phase."""
        if self.current_phase:
            self.current_phase.age_end = self.current_age
            self.phase_history.append(self.current_phase)
        self.current_phase = phase
    
    def add_wound(self, description: str, phase: str, charged_affects: List[str]) -> None:
        """Record a wound from failure or trauma."""
        wound = Wound(
            description=description,
            age_incurred=self.current_age,
            phase=phase,
            charged_affects=charged_affects
        )
        self.wounds.append(wound)
        for affect in charged_affects:
            self.habitus.record_wound(affect)
    
    def age_years(self, years: float) -> None:
        """Advance time."""
        self.current_age += years


# =============================================================================
# PHASE RECORD
# =============================================================================

@dataclass
class EncounterDetail:
    """Detailed record of a single encounter within a phase."""
    encounter: str
    stance_name: str
    stance_description: str
    affect_register: str
    affect_description: str
    embodiment: str
    components: List[str]
    outcome: str  # SUCCESS, PARTIAL, FAILURE
    viability: float
    muse: Optional[str] = None
    
    # The Other in this encounter
    other_involved: Optional[str] = None  # Name of Other
    recognition_event: Optional[str] = None  # What recognition occurred


@dataclass
class PhaseRecord:
    """Record of a complete life phase."""
    phase: LifePhase
    encounters_faced: int
    stances_generated: int
    successes: int
    failures: int
    dispositions_formed: List[str]
    wounds_incurred: List[str]
    commitments_made: List[str]
    commitments_ended: List[str]
    key_moments: List[str]  # Narrative highlights
    encounter_details: List[EncounterDetail] = field(default_factory=list)  # Full encounter records


# =============================================================================
# BIOGRAPHY SIMULATION
# =============================================================================

class Biography:
    """
    Orchestrates a life trajectory through multiple phases.
    
    Uses the existing Simulation infrastructure for encounter-level
    processing, but adds accumulation, phase transitions, and
    longitudinal coherence.
    
    Now includes Ricoeurian emplotment and the Other.
    """
    
    def __init__(
        self,
        name: str,
        starting_age: float = 22.0,
        context: str = "career",
        model_name: str = "gemini-2.0-flash",
        muse: Optional[str] = None,
        narrative_mode: Optional[str] = None,  # "tragedy", "comedy", etc.
    ):
        self.name = name
        self.model = genai.GenerativeModel(model_name)
        self.muse = muse
        self.context = context
        
        # Narrative configuration
        self.narrative_mode = narrative_mode
        self.narrative_config = None
        if narrative_mode:
            from conatus.simulation.narrative import EmplotmentMode, NARRATIVE_CONFIGS
            try:
                mode = EmplotmentMode(narrative_mode)
                self.narrative_config = NARRATIVE_CONFIGS.get(mode)
            except ValueError:
                pass  # Use default if invalid mode
        
        # Initialize biography state
        self.state = BiographyState(
            name=name,
            current_age=starting_age,
            habitus=Habitus(),
            active_commitments=[],
            repertoire=[],
            wounds=[],
            relationships={},
            recognition_events=[],
            internalized_voices=[],
            fortuna_events=[],
        )
        
        # Track simulation
        self.phase_records: List[PhaseRecord] = []
        
        # The Others in this biography
        self.others: Dict[str, 'Other'] = {}
    
    def _introduce_others_for_phase(self, phase: LifePhase) -> None:
        """Introduce archetypal Others when entering a new phase."""
        from conatus.simulation.narrative import (
            get_others_for_institution, Relationship, InternalizedVoice
        )
        
        others = get_others_for_institution(phase.institution)
        
        for other in others:
            if other.name not in self.others:
                self.others[other.name] = other
                
                # Create relationship
                from conatus.simulation.narrative import Relationship as Rel
                relationship = Rel(
                    other=other,
                    began_at_age=self.state.current_age,
                    phase_introduced=phase.name,
                    intensity=0.5,
                    mode="I-It" if other.recognition_status.value == "withholding" else "I-Thou",
                )
                self.state.relationships[other.name] = relationship
                
                # If internalized, add voice
                if other.internalized and other.internalized_voice:
                    from conatus.simulation.narrative import InternalizedVoice as Voice
                    voice = Voice(
                        source_other=other.name,
                        tone="critical" if "wrong" in other.internalized_voice.lower() else "supportive",
                        typical_message=other.internalized_voice,
                        intensity=0.3,
                    )
                    self.state.internalized_voices.append(voice)
    
    def _generate_relational_encounter(
        self,
        phase: LifePhase,
        other_name: str,
    ) -> str:
        """Generate an encounter specifically involving an Other."""
        other = self.others.get(other_name)
        if not other:
            return f"An encounter with {other_name}"
        
        prompt = f"""Generate a SPECIFIC encounter involving this significant Other.

SUBJECT: {self.name}, age {self.state.current_age:.0f}
PHASE: {phase.name}

THE OTHER:
- Name: {other.name}
- Role: {other.role.value}
- Description: {other.description}
- Their Recognition Status: {other.recognition_status.value}
- Their Ethical Demand: {other.ethical_demand or "None explicit"}

SUBJECT'S ACCUMULATED STATE:
- Skilled affects: {', '.join(self.state.habitus.skilled_affects) or 'None yet'}
- Wounds: {len(self.state.wounds)} carried
- Relationship history so far: {self.state.relationships.get(other_name).encounters_shared if other_name in self.state.relationships else 0} shared encounters

Generate a vivid, specific encounter where:
1. The Other is NAMED and PRESENT (not just mentioned)
2. Recognition dynamics are central (do they see the subject? how?)
3. The Other's ethical demand is felt
4. There is potential for relationship change

Respond with JUST the encounter description (2-3 sentences), no JSON."""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=200
                )
            )
            return response.text.strip()
        except Exception:
            return f"{other.name} confronts {self.name} about their shared history"
    
    def _check_fortuna(self, phase_progress: float) -> Optional['FortunaEvent']:
        """Check if a Fortuna event should occur based on narrative mode."""
        if not self.narrative_config:
            return None
        
        from conatus.simulation.narrative import get_fortuna_for_mode, EmplotmentMode
        
        try:
            mode = EmplotmentMode(self.narrative_mode)
            event = get_fortuna_for_mode(mode, phase_progress)
            if event:
                # Fill in the age and phase
                event.age = self.state.current_age
                event.phase = self.state.current_phase.name if self.state.current_phase else ""
                return event
        except:
            pass
        
        return None
    
    def _apply_fortuna(self, event: 'FortunaEvent') -> str:
        """Apply a Fortuna event and return a narrative description."""
        self.state.fortuna_events.append(event)
        
        # Create wound if specified
        if event.wound_created:
            self.state.add_wound(
                description=event.wound_created,
                phase=event.phase,
                charged_affects=[]
            )
        
        # Affect relationship if specified
        if event.affects_other and event.affects_other in self.state.relationships:
            rel = self.state.relationships[event.affects_other]
            if event.fortuna_type.value in ["betrayal", "loss"]:
                rel.ended = True
                rel.ended_at_age = self.state.current_age
                rel.ending_narrative = event.description
        
        return f"FORTUNA: {event.fortuna_type.value.upper()} — {event.description}"

    def _generate_phase_encounters(
        self,
        phase: LifePhase,
        count: int = 5,
    ) -> List[str]:
        """Generate encounters appropriate for a life phase."""
        
        # Build context from accumulated state
        habitus_context = ""
        if self.state.habitus.skilled_affects:
            habitus_context = f"Their skilled affects are: {', '.join(self.state.habitus.skilled_affects)}. "
        if self.state.habitus.charged_affects:
            habitus_context += f"They avoid or struggle with: {', '.join(self.state.habitus.charged_affects)}. "
        
        wounds_context = ""
        if self.state.wounds:
            wounds_context = f"They carry wounds from: {'; '.join([w.description for w in self.state.wounds[-3:]])}. "
        
        prompt = f"""Generate {count} specific encounters for this life phase.

SUBJECT: {self.name}, age {self.state.current_age:.0f}
PHASE: {phase.name} ({phase.arc.value})
INSTITUTION: {phase.institution}

ACCUMULATED DISPOSITIONS:
{habitus_context}

WOUNDS:
{wounds_context}

CURRENT COMMITMENTS: {', '.join([c.name for c in self.state.active_commitments]) or 'None yet'}

Generate encounters that:
1. Are typical for this phase and institution
2. Might activate wounds or require the subject's skilled affects
3. Include at least one that challenges their habitual patterns
4. Progress across the phase (early → middle → late phase)

Respond in JSON:
{{
  "encounters": [
    {{"description": "<specific, vivid encounter>", "phase_timing": "<early/middle/late>"}},
    ...
  ]
}}"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=1000
                )
            )
            
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            data = json.loads(text)
            return [e["description"] for e in data.get("encounters", [])]
            
        except Exception as e:
            # Fallback encounters
            return [
                f"A routine challenge in {phase.institution}",
                f"An unexpected complication arises",
                f"A relationship at work becomes strained",
                f"An opportunity appears that requires commitment",
                f"A moment of doubt about the current path",
            ][:count]
    
    def _generate_phase_transition(
        self,
        from_phase: LifePhase,
        trigger: str,
    ) -> LifePhase:
        """Generate the next life phase based on how the previous one ended."""
        
        prompt = f"""Generate the next life phase after this transition.

SUBJECT: {self.name}, age {self.state.current_age:.0f}
EXITING PHASE: {from_phase.name} ({from_phase.institution})

EXIT TRIGGER: {trigger}

SUBJECT'S ACCUMULATED STATE:
- Skilled affects: {', '.join(self.state.habitus.skilled_affects) or 'None developed yet'}
- Wounds: {len(self.state.wounds)} accumulated
- Repertoire: {len(self.state.repertoire)} stances mastered
- Career years: {self.state.current_age - 22:.0f}

What life phase comes next? Consider:
- Natural progressions (promotion, graduation, retirement)
- Crisis responses (career change, breakdown, reinvention)
- Life events (marriage, children, loss)
- Institutional changes (new job, new field, new location)

Respond in JSON:
{{
  "phase_name": "<name of the new phase>",
  "institution": "<the new institutional context>",
  "arc": "<ascent/plateau/descent/crisis/drift/rebirth>",
  "duration_years": <estimated years>,
  "central_commitments": ["<commitment 1>", ...],
  "encounter_types": ["<type 1>", ...],
  "transition_narrative": "<1-2 sentence description of the transition>"
}}"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.6,
                    max_output_tokens=600
                )
            )
            
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            data = json.loads(text)
            
            return LifePhase(
                name=data["phase_name"],
                institution=data["institution"],
                age_start=self.state.current_age,
                arc=PhaseArc(data.get("arc", "plateau")),
                central_commitments=data.get("central_commitments", []),
                encounter_types=data.get("encounter_types", []),
            )
            
        except Exception:
            # Fallback: generic next phase
            return LifePhase(
                name="New Chapter",
                institution="undefined",
                age_start=self.state.current_age,
                arc=PhaseArc.PLATEAU,
            )
    
    def run_phase(
        self,
        phase: LifePhase,
        encounters_per_year: int = 3,
    ) -> PhaseRecord:
        """
        Run a complete life phase.
        
        This creates encounters, processes them through the simulation,
        and accumulates results into the biography state.
        """
        from conatus.simulation import ConatusAgent, Simulation, EnvironmentConfig
        from conatus.simulation.experiments import create_agent
        
        # Enter the phase
        self.state.enter_phase(phase)
        
        # Introduce Others for this phase
        self._introduce_others_for_phase(phase)
        
        # Estimate phase duration based on arc (or narrative config if present)
        arc_durations = {
            PhaseArc.ASCENT: (3, 7),
            PhaseArc.PLATEAU: (4, 10),
            PhaseArc.DESCENT: (2, 5),
            PhaseArc.CRISIS: (0.5, 2),
            PhaseArc.DRIFT: (3, 8),
            PhaseArc.REBIRTH: (2, 5),
        }
        min_years, max_years = arc_durations.get(phase.arc, (3, 6))
        phase_years = random.uniform(min_years, max_years)
        encounter_count = max(3, int(phase_years * encounters_per_year))
        
        # Generate phase-appropriate encounters (mix of general and relational)
        general_encounters = self._generate_phase_encounters(phase, count=max(1, encounter_count - 2))
        
        # Add relational encounters with specific Others
        relational_encounters = []
        active_others = [name for name, rel in self.state.relationships.items() if not rel.ended]
        if active_others and encounter_count > 2:
            # Pick 1-2 Others to feature
            featured_others = random.sample(active_others, min(2, len(active_others)))
            for other_name in featured_others:
                rel_encounter = self._generate_relational_encounter(phase, other_name)
                relational_encounters.append((rel_encounter, other_name))
        
        # Interleave encounters with relational ones and possible Fortuna
        all_encounters = []
        general_idx = 0
        rel_idx = 0
        
        for i in range(encounter_count):
            progress = i / encounter_count if encounter_count > 0 else 0
            
            # Check for Fortuna event at narrative turning points
            fortuna = self._check_fortuna(progress)
            if fortuna:
                all_encounters.append((self._apply_fortuna(fortuna), None))
            
            # Alternate between general and relational encounters
            if rel_idx < len(relational_encounters) and (i == 1 or i == encounter_count - 2):
                enc, other = relational_encounters[rel_idx]
                all_encounters.append((enc, other))
                rel_idx += 1
            elif general_idx < len(general_encounters):
                all_encounters.append((general_encounters[general_idx], None))
                general_idx += 1
        
        encounters = [enc for enc, _ in all_encounters]
        encounter_other_map = {enc: other for enc, other in all_encounters}
        
        # Create agent with biography-informed components
        agent = create_agent(
            name=self.name,
            context=phase.institution,
            use_vector_store=True,
        )
        
        # Inject habitus into agent (bias toward trained components)
        if self.state.habitus.trained_components:
            for comp_name, comp in agent.components.items():
                if comp_name in self.state.habitus.trained_components:
                    comp.activation_weight = min(1.0, 
                        0.5 + 0.1 * self.state.habitus.trained_components[comp_name])
        
        # Run simulation
        sim = Simulation(
            agent=agent,
            env_config=EnvironmentConfig.for_context(phase.institution) 
                if phase.institution in ["forge", "arena", "dojo", "dance", "campfire", "wilderness"]
                else EnvironmentConfig(),
            force_novelty=True,
            use_vector_store=True,
            muse=self.muse,
        )
        
        records = sim.run(encounters)
        
        # Process results and accumulate into biography state
        successes = 0
        failures = 0
        key_moments = []
        dispositions_formed = []
        wounds_incurred = []
        encounter_details = []
        
        for record in records:
            # Track outcomes
            if record.environment_outcome == "SUCCESS":
                successes += 1
            elif record.environment_outcome == "FAILURE":
                failures += 1
                # Failures may create wounds
                if random.random() < 0.3:  # 30% chance of wound
                    wound_desc = f"Failed at {record.encounter[:50]}..."
                    wounds_incurred.append(wound_desc)
                    self.state.add_wound(
                        description=wound_desc,
                        phase=phase.name,
                        charged_affects=[record.final_affect] if record.final_affect else []
                    )
            
            # Accumulate into habitus
            final_proposal = None
            if record.proposals:
                final_proposal = record.proposals[-1]
                self.state.habitus.record_stance(
                    record.final_stance,
                    record.final_affect,
                    final_proposal.get("components", [])
                )
                
                # Add to repertoire if new
                if record.final_stance not in self.state.repertoire:
                    self.state.repertoire.append(record.final_stance)
            
            # Check for disposition formation
            if self.state.habitus.get_disposition_strength(record.final_stance) >= 0.5:
                if record.final_stance not in dispositions_formed:
                    dispositions_formed.append(record.final_stance)
                    key_moments.append(
                        f"The stance '{record.final_stance}' crystallized into a disposition"
                    )
            
            # Determine if an Other was involved in this encounter
            other_involved = encounter_other_map.get(record.encounter, None)
            recognition_event_desc = None
            
            if other_involved and other_involved in self.state.relationships:
                rel = self.state.relationships[other_involved]
                rel.encounters_shared += 1
                
                # Generate recognition event based on outcome
                if record.environment_outcome == "SUCCESS":
                    recognition_event_desc = f"{other_involved}'s recognition was earned"
                    # Potentially upgrade recognition status
                    if other_involved in self.others:
                        other = self.others[other_involved]
                        if other.recognition_status.value == "withholding":
                            recognition_event_desc = f"{other_involved} began to see {self.name}"
                elif record.environment_outcome == "FAILURE":
                    recognition_event_desc = f"{other_involved} witnessed the failure"
                
                key_moments.append(f"Encounter with {other_involved}: {recognition_event_desc}")
            
            # Store detailed encounter record
            encounter_details.append(EncounterDetail(
                encounter=record.encounter,
                stance_name=record.final_stance,
                stance_description=final_proposal.get("description", "") if final_proposal else "",
                affect_register=record.final_affect or "",
                affect_description=final_proposal.get("affect_description", "") if final_proposal else "",
                embodiment=final_proposal.get("embodiment", "") if final_proposal else "",
                components=final_proposal.get("components", []) if final_proposal else [],
                outcome=record.environment_outcome,
                viability=record.environment_viability,
                muse=record.muse,
                other_involved=other_involved,
                recognition_event=recognition_event_desc,
            ))
        
        # Age through the phase
        self.state.age_years(phase_years)
        phase.age_end = self.state.current_age
        
        # Create phase record
        phase_record = PhaseRecord(
            phase=phase,
            encounters_faced=len(encounters),
            stances_generated=len(set(r.final_stance for r in records)),
            successes=successes,
            failures=failures,
            dispositions_formed=dispositions_formed,
            wounds_incurred=wounds_incurred,
            commitments_made=phase.central_commitments if isinstance(phase.central_commitments, list) else [],
            commitments_ended=[],
            key_moments=key_moments,
            encounter_details=encounter_details,
        )
        
        self.phase_records.append(phase_record)
        return phase_record
    
    def run_biography(
        self,
        initial_phase: LifePhase,
        num_phases: int = 5,
    ) -> List[PhaseRecord]:
        """
        Run an entire biography across multiple phases.
        """
        current_phase = initial_phase
        
        for i in range(num_phases):
            print(f"\n{'='*60}")
            print(f"PHASE {i+1}: {current_phase.name} (Age {self.state.current_age:.0f})")
            print(f"{'='*60}")
            
            # Run the phase
            record = self.run_phase(current_phase)
            
            print(f"  Encounters: {record.encounters_faced}")
            print(f"  Successes: {record.successes}, Failures: {record.failures}")
            print(f"  Dispositions formed: {len(record.dispositions_formed)}")
            print(f"  Wounds incurred: {len(record.wounds_incurred)}")
            
            # Generate transition to next phase (if not last)
            if i < num_phases - 1:
                # Determine exit trigger
                if record.failures > record.successes:
                    trigger = "accumulated failures led to crisis"
                elif len(record.dispositions_formed) > 2:
                    trigger = "mastery achieved, ready for new challenge"
                else:
                    trigger = "natural progression of time"
                
                current_phase.exit_trigger = trigger
                current_phase = self._generate_phase_transition(current_phase, trigger)
        
        return self.phase_records


# =============================================================================
# BIOGRAPHY REPORT GENERATION
# =============================================================================

def generate_biography_report(
    biography: Biography,
    output_path: str = None,
) -> str:
    """Generate a rich narrative report of the biography."""
    
    outcome_icons = {"SUCCESS": "✅", "PARTIAL": "⚠️", "FAILURE": "❌"}
    arc_icons = {
        PhaseArc.ASCENT: "📈",
        PhaseArc.PLATEAU: "➡️",
        PhaseArc.DESCENT: "📉",
        PhaseArc.CRISIS: "💥",
        PhaseArc.DRIFT: "🌊",
        PhaseArc.REBIRTH: "🌱",
    }
    
    lines = [
        f"# Biography: {biography.name}",
        "",
        f"> A life simulation spanning ages {biography.phase_records[0].phase.age_start:.0f} to {biography.state.current_age:.0f}",
        "",
    ]
    
    # Executive summary
    total_encounters = sum(r.encounters_faced for r in biography.phase_records)
    total_successes = sum(r.successes for r in biography.phase_records)
    total_failures = sum(r.failures for r in biography.phase_records)
    
    lines.extend([
        "## Summary",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| Lifespan Simulated | {biography.state.current_age - biography.phase_records[0].phase.age_start:.0f} years |",
        f"| Phases | {len(biography.phase_records)} |",
        f"| Total Encounters | {total_encounters} |",
        f"| Overall Success Rate | {total_successes}/{total_successes + total_failures} ({total_successes/(total_successes + total_failures)*100:.0f}%) |" if (total_successes + total_failures) > 0 else "",
        f"| Stances Mastered | {len(biography.state.repertoire)} |",
        f"| Wounds Carried | {len(biography.state.wounds)} |",
        "",
        "---",
        "",
    ])
    
    # Detailed phase-by-phase narrative
    lines.append("## Life Trajectory")
    lines.append("")
    
    for i, record in enumerate(biography.phase_records):
        phase = record.phase
        icon = arc_icons.get(phase.arc, "•")
        
        lines.extend([
            f"### Phase {i+1}: {icon} {phase.name}",
            "",
            f"**Ages {phase.age_start:.0f} - {phase.age_end:.0f}** | {phase.institution} | Arc: *{phase.arc.value}*",
            "",
        ])
        
        # Phase statistics
        total = record.successes + record.failures
        if total > 0:
            success_rate = record.successes / total * 100
            lines.extend([
                f"**Phase Outcomes**: {record.successes} successes, {record.failures} failures ({success_rate:.0f}% success rate)",
                "",
            ])
        
        # Detailed encounters
        if record.encounter_details:
            lines.append("#### Encounters")
            lines.append("")
            
            for j, detail in enumerate(record.encounter_details):
                outcome_icon = outcome_icons.get(detail.outcome, "❓")
                
                # Check if this involves an Other
                other_marker = ""
                if detail.other_involved:
                    other_marker = f" 👤 [{detail.other_involved}]"
                
                lines.extend([
                    f"##### {j+1}. {outcome_icon}{other_marker} {detail.encounter[:70]}{'...' if len(detail.encounter) > 70 else ''}",
                    "",
                ])
                
                # If Other is involved, show recognition dynamics
                if detail.other_involved and detail.recognition_event:
                    lines.extend([
                        f"**The Other**: *{detail.other_involved}*",
                        f"> {detail.recognition_event}",
                        "",
                    ])
                
                # Stance adopted
                lines.extend([
                    f"**Stance**: *{detail.stance_name}*",
                    "",
                ])
                
                if detail.stance_description:
                    lines.extend([
                        f"> {detail.stance_description}",
                        "",
                    ])
                
                # Affect
                if detail.affect_register:
                    lines.append(f"**Affect Register**: \"{detail.affect_register}\"")
                    if detail.affect_description:
                        lines.extend([
                            "",
                            f"*{detail.affect_description}*",
                        ])
                    lines.append("")
                
                # Embodiment instructions
                if detail.embodiment:
                    lines.extend([
                        "**Embodiment**:",
                        "",
                        f"> {detail.embodiment}",
                        "",
                    ])
                
                # Components activated
                if detail.components:
                    lines.append(f"**Active Components**: {', '.join(detail.components[:5])}{'...' if len(detail.components) > 5 else ''}")
                    lines.append("")
                
                # Outcome and viability
                lines.extend([
                    f"**Outcome**: {detail.outcome} (viability: {detail.viability:.2f})",
                    "",
                ])
                
                if detail.muse:
                    lines.append(f"*Muse: {detail.muse.title()}*")
                    lines.append("")
        
        # Key moments and transitions
        if record.key_moments:
            lines.extend([
                "#### Key Moments",
                "",
            ])
            for moment in record.key_moments:
                lines.append(f"- {moment}")
            lines.append("")
        
        # Dispositions crystallized
        if record.dispositions_formed:
            lines.extend([
                "#### Dispositions Crystallized",
                "",
                f"{', '.join(record.dispositions_formed)}",
                "",
            ])
        
        # Wounds incurred
        if record.wounds_incurred:
            lines.extend([
                "#### Wounds Incurred",
                "",
            ])
            for wound in record.wounds_incurred:
                lines.append(f"- 🩸 {wound}")
            lines.append("")
        
        # Phase exit
        if phase.exit_trigger:
            lines.extend([
                f"**Exit Trigger**: *{phase.exit_trigger}*",
                "",
            ])
        
        lines.extend(["---", ""])
    
    # Accumulated Self - The Final State
    lines.extend([
        "## The Accumulated Self",
        "",
        f"> At age {biography.state.current_age:.0f}, after {len(biography.phase_records)} life phases",
        "",
    ])
    
    # Habitus section
    lines.extend([
        "### Habitus",
        "",
    ])
    
    if biography.state.habitus.skilled_affects:
        lines.extend([
            "**Skilled Affects** (come easily):",
            "",
        ])
        for affect in biography.state.habitus.skilled_affects:
            lines.append(f"- *{affect}*")
        lines.append("")
    
    if biography.state.habitus.charged_affects:
        lines.extend([
            "**Charged Affects** (difficult, avoided):",
            "",
        ])
        for affect in biography.state.habitus.charged_affects:
            lines.append(f"- ⚡ *{affect}*")
        lines.append("")
    
    # Top dispositions with visual bars
    top_dispositions = sorted(
        biography.state.habitus.default_stances.items(),
        key=lambda x: x[1],
        reverse=True
    )[:8]
    
    if top_dispositions:
        lines.extend([
            "### Strongest Dispositions",
            "",
        ])
        for name, strength in top_dispositions:
            bar = "█" * int(strength * 10) + "░" * (10 - int(strength * 10))
            lines.append(f"| {bar} | **{name}** ({strength:.2f}) |")
        lines.append("")
    
    # Relationships (the Others)
    if biography.state.relationships:
        lines.extend([
            "### Significant Others",
            "",
            "| Other | Role | Encounters | Status |",
            "|-------|------|------------|--------|",
        ])
        for name, rel in biography.state.relationships.items():
            other = biography.others.get(name)
            role = other.role.value if other else "unknown"
            status = other.recognition_status.value if other else "unknown"
            ended = " (ended)" if rel.ended else ""
            lines.append(f"| {name} | {role} | {rel.encounters_shared} | {status}{ended} |")
        lines.append("")
        
        # Internalized voices
        if biography.state.internalized_voices:
            lines.extend([
                "### Internalized Voices",
                "",
            ])
            for voice in biography.state.internalized_voices:
                lines.append(f"- **{voice.source_other}** ({voice.tone}): *\"{voice.typical_message}\"*")
            lines.append("")
    
    # Fortuna events
    if biography.state.fortuna_events:
        lines.extend([
            "### Fortuna (Contingent Events)",
            "",
        ])
        for event in biography.state.fortuna_events:
            lines.append(f"- **Age {event.age:.0f}** ({event.fortuna_type.value}): {event.description}")
        lines.append("")
    
    # Full repertoire
    if biography.state.repertoire:
        lines.extend([
            "### Full Repertoire",
            "",
            f"*{len(biography.state.repertoire)} stances mastered:*",
            "",
        ])
        # Group into rows of 3
        for k in range(0, len(biography.state.repertoire), 3):
            chunk = biography.state.repertoire[k:k+3]
            lines.append("- " + " • ".join(chunk))
        lines.append("")
    
    # Wounds section
    if biography.state.wounds:
        lines.extend([
            "### Wounds Carried",
            "",
        ])
        for wound in biography.state.wounds:
            healed_str = "(healed)" if wound.healed else ""
            lines.append(f"- **Age {wound.age_incurred:.0f}** ({wound.phase}): {wound.description} {healed_str}")
            if wound.charged_affects:
                lines.append(f"  - Charged affects: {', '.join(wound.charged_affects)}")
        lines.append("")
    
    # Most trained components
    if biography.state.habitus.trained_components:
        top_components = sorted(
            biography.state.habitus.trained_components.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        
        lines.extend([
            "### Most Trained Components",
            "",
            "| Component | Activations |",
            "|-----------|-------------|",
        ])
        for comp, count in top_components:
            lines.append(f"| {comp} | {count} |")
        lines.append("")
    
    lines.extend([
        "---",
        "",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
    ])
    
    report = "\n".join(lines)
    
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            f.write(report)
        print(f"✓ Biography report saved to {output_path}")
    
    return report
