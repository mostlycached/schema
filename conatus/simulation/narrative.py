"""
Narrative Module: Ricoeurian Emplotment and The Other

This module extends the biography simulation with:
1. Ricoeurian narrative structure (triple mimesis, emplotment)
2. The Other (relational identity, recognition, intersubjectivity)
3. Fortuna (luck, contingency, reversals)

Based on:
- Ricoeur's "Time and Narrative" (emplotment, mimesis₁/₂/₃)
- Ricoeur's "Oneself as Another" (ipse/idem, attestation)
- Levinas (the face of the Other, ethical demand)
- Hegel (recognition, Anerkennung)
"""

import random
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum


# =============================================================================
# NARRATIVE ARCS (Emplotment Modes)
# =============================================================================

class EmplotmentMode(Enum):
    """
    How the biography configures events into a unified plot.
    Based on Northrop Frye's archetypal modes, filtered through Ricoeur.
    """
    TRAGEDY = "tragedy"       # Hubris → peripeteia → catastrophe
    COMEDY = "comedy"         # Obstacles → complications → integration
    ROMANCE = "romance"       # Quest → trials → achievement
    SATIRE = "satire"         # Entropy → dissolution → irony
    BILDUNGSROMAN = "bildung" # Innocence → trial → growth → maturity
    REDEMPTION = "redemption" # Fall → suffering → transformation


@dataclass
class NarrativeConfiguration:
    """
    Mimesis₂: The emplotment configuration.
    
    This determines how phases are structured and what kinds
    of events (peripeteia, anagnorisis, etc.) occur when.
    """
    mode: EmplotmentMode
    
    # At what percentage through the biography do key events occur?
    # Values are 0.0 to 1.0 representing progress through phases
    inciting_incident: float = 0.1    # What sets the plot in motion
    rising_action_peak: float = 0.4   # Complications intensify
    turning_point: float = 0.5        # Peripeteia - reversal of fortune
    climax: float = 0.8               # Maximum crisis/resolution
    denouement: float = 0.95          # Falling action, new equilibrium
    
    # How much does chance intervene? 0.0 = fully determined, 1.0 = random
    concordant_discordance: float = 0.3
    
    # Does this arc trend toward success or failure at key points?
    fortune_trajectory: List[str] = field(default_factory=list)


# Pre-defined narrative configurations
NARRATIVE_CONFIGS = {
    EmplotmentMode.TRAGEDY: NarrativeConfiguration(
        mode=EmplotmentMode.TRAGEDY,
        turning_point=0.6,  # Late turning point
        fortune_trajectory=["ascent", "ascent", "peak", "descent", "catastrophe"]
    ),
    EmplotmentMode.COMEDY: NarrativeConfiguration(
        mode=EmplotmentMode.COMEDY,
        turning_point=0.7,  # Late resolution
        fortune_trajectory=["obstacle", "complication", "crisis", "resolution", "integration"]
    ),
    EmplotmentMode.ROMANCE: NarrativeConfiguration(
        mode=EmplotmentMode.ROMANCE,
        fortune_trajectory=["call", "trial", "ordeal", "reward", "return"]
    ),
    EmplotmentMode.SATIRE: NarrativeConfiguration(
        mode=EmplotmentMode.SATIRE,
        concordant_discordance=0.6,  # More chaos
        fortune_trajectory=["pretension", "exposure", "entropy", "dissolution", "irony"]
    ),
    EmplotmentMode.BILDUNGSROMAN: NarrativeConfiguration(
        mode=EmplotmentMode.BILDUNGSROMAN,
        fortune_trajectory=["innocence", "departure", "trial", "growth", "maturity"]
    ),
    EmplotmentMode.REDEMPTION: NarrativeConfiguration(
        mode=EmplotmentMode.REDEMPTION,
        turning_point=0.4,  # Early fall
        fortune_trajectory=["fall", "suffering", "crisis", "transformation", "redemption"]
    ),
}


# =============================================================================
# THE OTHER
# =============================================================================

class RecognitionStatus(Enum):
    """Hegelian recognition states."""
    AFFIRMING = "affirming"       # The Other sees and acknowledges the subject
    WITHHOLDING = "withholding"   # The Other refuses to recognize
    AMBIVALENT = "ambivalent"     # Mixed or uncertain recognition
    CONTESTED = "contested"       # Active struggle for recognition
    MUTUAL = "mutual"             # Full I-Thou recognition (Buber)


class RelationshipRole(Enum):
    """Archetypal roles the Other can play in a life trajectory."""
    MENTOR = "mentor"           # Guides, bestows recognition
    RIVAL = "rival"             # Competes for same recognition
    PARTNER = "partner"         # Intimate, mutual recognition
    CHILD = "child"             # Dependent, calls forth responsibility
    ADVERSARY = "adversary"     # Opposes, withholds recognition
    ALLY = "ally"               # Supports without deep intimacy
    STRANGER = "stranger"       # Levinasian face - ethical demand
    SHADOW = "shadow"           # Represents rejected aspects of self


@dataclass
class Other:
    """
    A significant Other in the subject's trajectory.
    
    Others have their own (simplified) habitus, their own wounds,
    and a history of recognition events with the subject.
    """
    name: str
    role: RelationshipRole
    description: str = ""
    
    # The Other's own dispositions (simplified)
    their_dominant_stances: List[str] = field(default_factory=list)
    their_wounds: List[str] = field(default_factory=list)
    
    # Recognition dynamics
    recognition_status: RecognitionStatus = RecognitionStatus.AMBIVALENT
    recognition_history: List[str] = field(default_factory=list)
    
    # Levinas: what does the Other's face demand?
    ethical_demand: Optional[str] = None
    
    # Does this Other appear in the subject's internal voice?
    internalized: bool = False
    internalized_voice: Optional[str] = None  # What does their voice say?


@dataclass
class Relationship:
    """
    An ongoing bond with an Other across time.
    
    Relationships have their own trajectory, intensity, and mode.
    """
    other: Other
    began_at_age: float
    phase_introduced: str
    
    # Current state
    intensity: float = 0.5  # How central to identity (0.0-1.0)
    mode: str = "I-It"      # "I-Thou" (genuine encounter) vs "I-It" (instrumental)
    
    # History
    encounters_shared: int = 0
    key_moments: List[str] = field(default_factory=list)
    
    # Has this relationship ended?
    ended: bool = False
    ended_at_age: Optional[float] = None
    ending_narrative: Optional[str] = None


@dataclass
class RecognitionEvent:
    """
    A specific moment of recognition or its refusal.
    
    These are crucial identity-forming moments where the Other's
    gaze confirms, denies, or transforms the subject's self-understanding.
    """
    other_name: str
    age: float
    event_type: str  # "affirmation", "rejection", "withdrawal", "mutual", "demand"
    description: str
    impact_on_identity: str  # How this changed the subject
    
    # What disposition or wound resulted?
    disposition_gained: Optional[str] = None
    wound_incurred: Optional[str] = None


# =============================================================================
# FORTUNA (Luck and Contingency)
# =============================================================================

class FortunaType(Enum):
    """Types of contingent events that bypass normal encounter logic."""
    WINDFALL = "windfall"           # Unexpected good fortune
    SERENDIPITY = "serendipity"     # Happy accident, lucky meeting
    CATASTROPHE = "catastrophe"     # Sudden disaster
    BETRAYAL = "betrayal"           # Trust violated
    LOSS = "loss"                   # Death or departure of Other
    ILLNESS = "illness"             # Bodily limitation
    REVELATION = "revelation"       # Anagnorisis - sudden understanding


@dataclass
class FortunaEvent:
    """
    A contingent event that intervenes from outside.
    
    Ricoeur's "concordant discordance" - the heterogeneous that
    emplotment must integrate into narrative coherence.
    """
    fortuna_type: FortunaType
    description: str
    age: float
    phase: str
    
    # Effects on biography state
    affects_other: Optional[str] = None  # Name of Other involved
    wound_created: Optional[str] = None
    disposition_affected: Optional[str] = None
    
    # How was this integrated into the life narrative?
    narrative_integration: Optional[str] = None


# =============================================================================
# INTERNALIZED VOICES
# =============================================================================

@dataclass
class InternalizedVoice:
    """
    The voice of an Other that lives inside the subject's habitus.
    
    Bakhtin's polyphony: the self contains the voices of significant Others.
    These voices can be supportive, critical, demanding, or ambivalent.
    """
    source_other: str  # Who this voice came from
    tone: str          # "critical", "supportive", "demanding", "mocking", "loving"
    typical_message: str  # What this voice typically says
    
    # When does this voice activate?
    triggers: List[str] = field(default_factory=list)  # What encounters trigger it
    
    # How strong is this voice?
    intensity: float = 0.5  # 0.0: barely present, 1.0: dominant


# =============================================================================
# GENERATORS
# =============================================================================

# Archetypal Others for different life contexts
ARCHETYPAL_OTHERS = {
    "phd_program": [
        Other(
            name="The Demanding Advisor",
            role=RelationshipRole.MENTOR,
            description="Brilliant but exacting, recognition is hard-won",
            their_dominant_stances=["methodological rigor", "dismissive precision"],
            recognition_status=RecognitionStatus.WITHHOLDING,
            ethical_demand="Become worthy of this tradition"
        ),
        Other(
            name="The Brilliant Peer",
            role=RelationshipRole.RIVAL,
            description="Equally talented, competing for limited recognition",
            their_dominant_stances=["confident assertion", "strategic networking"],
            recognition_status=RecognitionStatus.CONTESTED,
        ),
        Other(
            name="The Struggling Colleague",
            role=RelationshipRole.ALLY,
            description="In the trenches together, mutual support",
            their_dominant_stances=["vulnerable honesty", "generous collaboration"],
            recognition_status=RecognitionStatus.MUTUAL,
        ),
    ],
    "tech_startup": [
        Other(
            name="The Visionary Cofounder",
            role=RelationshipRole.PARTNER,
            description="Shares the dream but clashes on execution",
            their_dominant_stances=["relentless optimism", "boundary-ignoring drive"],
            recognition_status=RecognitionStatus.AMBIVALENT,
            ethical_demand="Don't let the dream die"
        ),
        Other(
            name="The Angel Investor",
            role=RelationshipRole.MENTOR,
            description="Holds power over the venture's survival",
            their_dominant_stances=["calculated detachment", "pattern recognition"],
            recognition_status=RecognitionStatus.WITHHOLDING,
            ethical_demand="Prove you can deliver returns"
        ),
        Other(
            name="The Early Employee",
            role=RelationshipRole.ALLY,
            description="Believed when no one else did",
            their_dominant_stances=["loyal dedication", "quiet competence"],
            recognition_status=RecognitionStatus.AFFIRMING,
        ),
    ],
    "artistic_practice": [
        Other(
            name="The Established Master",
            role=RelationshipRole.MENTOR,
            description="Gatekeeps access to recognition and resources",
            their_dominant_stances=["aesthetic authority", "selective attention"],
            recognition_status=RecognitionStatus.WITHHOLDING,
            ethical_demand="Find your own voice, but honor the tradition"
        ),
        Other(
            name="The Envious Peer",
            role=RelationshipRole.SHADOW,
            description="Represents the path not taken, the compromises",
            their_dominant_stances=["bitter resentment", "market calculation"],
            recognition_status=RecognitionStatus.CONTESTED,
        ),
        Other(
            name="The True Believer",
            role=RelationshipRole.ALLY,
            description="Sees genius where others see nothing",
            their_dominant_stances=["fervent advocacy", "uncritical devotion"],
            recognition_status=RecognitionStatus.AFFIRMING,
        ),
    ],
    "parenthood": [
        Other(
            name="The Child",
            role=RelationshipRole.CHILD,
            description="Absolute ethical demand, infinite vulnerability",
            their_dominant_stances=["complete openness", "unfiltered presence"],
            recognition_status=RecognitionStatus.AFFIRMING,
            ethical_demand="I need you to be here, fully"
        ),
        Other(
            name="The Co-Parent",
            role=RelationshipRole.PARTNER,
            description="Navigating together the impossible task",
            their_dominant_stances=["exhausted devotion", "conflict avoidance"],
            recognition_status=RecognitionStatus.AMBIVALENT,
        ),
        Other(
            name="Your Own Parent",
            role=RelationshipRole.SHADOW,
            description="The internalized voice of how you were raised",
            their_dominant_stances=["critical comparison", "unmet expectations"],
            recognition_status=RecognitionStatus.AMBIVALENT,
            internalized=True,
            internalized_voice="You're doing it wrong, just like I said you would"
        ),
    ],
    "corporate_ladder": [
        Other(
            name="The Political Boss",
            role=RelationshipRole.ADVERSARY,
            description="Controls advancement, plays favorites",
            their_dominant_stances=["political calculation", "selective loyalty"],
            recognition_status=RecognitionStatus.WITHHOLDING,
        ),
        Other(
            name="The Burned-Out Mentor",
            role=RelationshipRole.MENTOR,
            description="Warns of the costs, regrets the path",
            their_dominant_stances=["cynical wisdom", "protective warning"],
            recognition_status=RecognitionStatus.AFFIRMING,
            internalized=True,
            internalized_voice="Is this really what you want your life to be?"
        ),
        Other(
            name="The Office Confidant",
            role=RelationshipRole.ALLY,
            description="Navigates the politics together",
            their_dominant_stances=["strategic friendship", "mutual protection"],
            recognition_status=RecognitionStatus.MUTUAL,
        ),
    ],
}

# Fortuna events by narrative mode
FORTUNA_EVENTS = {
    EmplotmentMode.TRAGEDY: [
        FortunaEvent(FortunaType.REVELATION, "discovers the very success was built on falsehood", 0, "", wound_created="the foundation was hollow"),
        FortunaEvent(FortunaType.BETRAYAL, "trusted ally reveals they were serving another interest all along", 0, "", wound_created="trust itself became suspect"),
        FortunaEvent(FortunaType.LOSS, "the mentor dies before bestowing final recognition", 0, "", wound_created="forever seeking what can never be given"),
    ],
    EmplotmentMode.COMEDY: [
        FortunaEvent(FortunaType.SERENDIPITY, "chance meeting with someone who changes everything", 0, ""),
        FortunaEvent(FortunaType.WINDFALL, "unexpected opportunity arrives at the darkest moment", 0, ""),
        FortunaEvent(FortunaType.REVELATION, "realizes the obstacle was a misunderstanding all along", 0, ""),
    ],
    EmplotmentMode.REDEMPTION: [
        FortunaEvent(FortunaType.CATASTROPHE, "public exposure of hidden failure", 0, "", wound_created="shame made visible"),
        FortunaEvent(FortunaType.ILLNESS, "body forces a confrontation with mortality", 0, ""),
        FortunaEvent(FortunaType.REVELATION, "understands the wound was necessary for transformation", 0, ""),
    ],
}


def get_others_for_institution(institution: str) -> List[Other]:
    """Get archetypal Others for an institution."""
    return ARCHETYPAL_OTHERS.get(institution, [
        Other(
            name="The Witness",
            role=RelationshipRole.STRANGER,
            description="A presence that observes without judgment",
            recognition_status=RecognitionStatus.AMBIVALENT,
            ethical_demand="I see you"
        )
    ])


def get_fortuna_for_mode(mode: EmplotmentMode, phase_progress: float) -> Optional[FortunaEvent]:
    """
    Possibly return a Fortuna event based on narrative mode and progress.
    
    Uses concordant_discordance from narrative config to determine probability.
    """
    config = NARRATIVE_CONFIGS.get(mode, NARRATIVE_CONFIGS[EmplotmentMode.BILDUNGSROMAN])
    
    # Check if we're at a turning point where fortuna might strike
    if abs(phase_progress - config.turning_point) < 0.15:
        if random.random() < config.concordant_discordance:
            events = FORTUNA_EVENTS.get(mode, [])
            if events:
                return random.choice(events)
    
    return None
