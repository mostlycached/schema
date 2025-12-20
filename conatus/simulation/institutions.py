"""
Institutions Module

Defines persistent social structures that shape encounter possibilities
and constrain available stances. Institutions generate encounters typical
to their domain and track how subjects progress through them.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class InstitutionType(Enum):
    """Categories of institutional contexts."""
    ACADEMIC = "academic"
    CORPORATE = "corporate"
    ARTISTIC = "artistic"
    DOMESTIC = "domestic"
    ATHLETIC = "athletic"
    THERAPEUTIC = "therapeutic"
    CIVIC = "civic"


@dataclass
class Institution:
    """
    A social structure that shapes encounter possibilities.
    
    Institutions define:
    - What encounters are typical
    - What stances are expected/rewarded
    - How one advances (or doesn't)
    - What causes exit
    """
    name: str
    type: InstitutionType
    description: str
    
    # Normative expectations
    expected_stances: List[str] = field(default_factory=list)  # What stances are rewarded
    forbidden_stances: List[str] = field(default_factory=list)  # What stances are punished
    
    # Encounter generation
    encounter_patterns: List[str] = field(default_factory=list)
    escalation_triggers: List[str] = field(default_factory=list)
    
    # Progression
    stages: List[str] = field(default_factory=list)  # e.g., ["junior", "mid", "senior"]
    promotion_criteria: List[str] = field(default_factory=list)
    
    # Exit
    exit_triggers: List[str] = field(default_factory=list)
    natural_duration_years: tuple[float, float] = (3, 10)


# =============================================================================
# PREDEFINED INSTITUTIONS
# =============================================================================

INSTITUTIONS = {
    # Academic
    "phd_program": Institution(
        name="PhD Program",
        type=InstitutionType.ACADEMIC,
        description="Graduate education in research methods and specialized knowledge",
        expected_stances=[
            "intellectual humility",
            "methodological rigor", 
            "patient persistence",
            "deference to expertise"
        ],
        forbidden_stances=[
            "impulsive certainty",
            "dismissive arrogance",
            "shortcuts over depth"
        ],
        encounter_patterns=[
            "Qualifying examination requiring synthesis of entire field",
            "Advisor meeting where expectations misalign",
            "Conference presentation to critical audience",
            "Writing deadline with impossible scope",
            "Imposter syndrome episode triggered by peer success",
            "Unexpected result that invalidates months of work",
            "Teaching assignment that competes with research time",
            "Departmental politics affecting funding"
        ],
        escalation_triggers=[
            "approaching candidacy deadline",
            "funding running low",
            "advisor relationship souring"
        ],
        stages=["first_year", "pre-candidacy", "ABD", "defending"],
        promotion_criteria=["qualifying exams", "dissertation proposal", "publications", "defense"],
        exit_triggers=["graduation", "dropout", "dismissal", "leave_of_absence"],
        natural_duration_years=(4, 8)
    ),
    
    "postdoc": Institution(
        name="Postdoctoral Research",
        type=InstitutionType.ACADEMIC,
        description="Transitional academic position focused on building independent research profile",
        expected_stances=[
            "productive independence",
            "strategic networking",
            "publication pressure tolerance"
        ],
        forbidden_stances=[
            "passive waiting",
            "comfort in dependence"
        ],
        encounter_patterns=[
            "Grant deadline with uncertain prospects",
            "Job market rejection",
            "Collaborator conflict over authorship",
            "Pressure to pivot research direction",
            "Junior colleague receiving offer you wanted"
        ],
        stages=["early", "mid", "late"],
        promotion_criteria=["publications", "grants", "job offers"],
        exit_triggers=["tenure_track_job", "industry_transition", "contract_end", "burnout"],
        natural_duration_years=(2, 5)
    ),
    
    # Corporate
    "tech_startup": Institution(
        name="Tech Startup",
        type=InstitutionType.CORPORATE,
        description="High-intensity, high-uncertainty venture with potential for rapid growth or failure",
        expected_stances=[
            "velocity over perfection",
            "ownership mentality",
            "comfortable ambiguity",
            "relentless optimism"
        ],
        forbidden_stances=[
            "bureaucratic caution",
            "narrow role definition",
            "work-life separation"
        ],
        encounter_patterns=[
            "Product launch with critical bugs discovered last minute",
            "Investor meeting where traction story is weak",
            "Key employee threatens to leave",
            "Pivot demanded by market feedback",
            "Runway running out, decisions required",
            "Cofounder conflict over direction",
            "Competitor launches similar product",
            "Success creates scaling problems"
        ],
        stages=["founding", "early", "growth", "scaling"],
        promotion_criteria=["impact", "ownership", "equity events"],
        exit_triggers=["acquisition", "ipo", "failure", "burnout", "exit_to_larger_company"],
        natural_duration_years=(2, 6)
    ),
    
    "corporate_ladder": Institution(
        name="Corporate Career",
        type=InstitutionType.CORPORATE,
        description="Traditional hierarchical organization with defined progression paths",
        expected_stances=[
            "professional composure",
            "political awareness",
            "measured ambition",
            "institutional loyalty"
        ],
        forbidden_stances=[
            "naive directness",
            "visible frustration",
            "disruptive innovation"
        ],
        encounter_patterns=[
            "Performance review with unexpected criticism",
            "Reorganization threatens position",
            "Promotion passed over for external hire",
            "High-visibility project with impossible deadline",
            "Ethical compromise requested by leadership",
            "New manager has different style",
            "Layoff anxiety permeates culture"
        ],
        stages=["entry", "mid-level", "senior", "executive"],
        promotion_criteria=["performance_reviews", "visibility", "sponsorship", "credentials"],
        exit_triggers=["promotion", "layoff", "resignation", "retirement", "burnout"],
        natural_duration_years=(3, 15)
    ),
    
    # Artistic
    "artistic_practice": Institution(
        name="Independent Artistic Practice",
        type=InstitutionType.ARTISTIC,
        description="Self-directed creative work with uncertain external validation",
        expected_stances=[
            "creative courage",
            "solitude tolerance",
            "rejection resilience",
            "authentic voice"
        ],
        forbidden_stances=[
            "market calculation",
            "approval seeking",
            "derivative safety"
        ],
        encounter_patterns=[
            "Extended creative block with no end in sight",
            "Harsh review of exhibited work",
            "Financial pressure to take commercial work",
            "Recognition finally comes but feels hollow",
            "Younger artist achieves what you dreamed of",
            "Major piece fails to find audience",
            "Success creates expectation pressure"
        ],
        stages=["emerging", "developing", "established", "legacy"],
        promotion_criteria=["exhibitions", "recognition", "sales", "influence"],
        exit_triggers=["breakthrough", "abandonment", "pivot_to_commercial", "teaching"],
        natural_duration_years=(5, 40)
    ),
    
    "music_conservatory": Institution(
        name="Music Conservatory",
        type=InstitutionType.ARTISTIC,
        description="Intensive classical music training with high technical demands",
        expected_stances=[
            "disciplined practice",
            "bodily precision",
            "interpretive depth",
            "competitive grace"
        ],
        encounter_patterns=[
            "Jury examination with livelihood at stake",
            "Performance anxiety before major recital",
            "Injury threatens technique",
            "Teacher-student relationship becomes toxic",
            "Competition loss to less talented but more confident peer"
        ],
        stages=["undergraduate", "graduate", "artist_diploma"],
        promotion_criteria=["juries", "competitions", "auditions"],
        exit_triggers=["graduation", "injury", "career_change", "professional_placement"],
        natural_duration_years=(4, 8)
    ),
    
    # Domestic
    "parenthood": Institution(
        name="Parenthood",
        type=InstitutionType.DOMESTIC,
        description="Raising children through their developmental stages",
        expected_stances=[
            "patient presence",
            "adaptive authority",
            "unconditional regard",
            "self-sacrifice balance"
        ],
        forbidden_stances=[
            "emotional reactivity",
            "rigid control",
            "absent preoccupation"
        ],
        encounter_patterns=[
            "Toddler tantrum in public space",
            "Child's serious illness or injury",
            "Adolescent rebellion and secrets",
            "School problems requiring intervention",
            "Child's mental health crisis",
            "Partner disagreement about parenting",
            "Work-family conflict during milestone moment"
        ],
        stages=["infant", "toddler", "school_age", "adolescent", "young_adult", "empty_nest"],
        promotion_criteria=["developmental_milestones", "relationship_quality"],
        exit_triggers=["children_independent", "death", "family_dissolution"],
        natural_duration_years=(18, 25)
    ),
    
    "marriage": Institution(
        name="Marriage/Partnership",
        type=InstitutionType.DOMESTIC,
        description="Long-term committed romantic partnership",
        expected_stances=[
            "generous interpretation",
            "repair capacity",
            "individual-couple balance",
            "honest vulnerability"
        ],
        encounter_patterns=[
            "Major life decision disagreement",
            "Trust breach requiring repair",
            "External stressor (job loss, illness) straining bond",
            "Growing apart without noticing",
            "Conflict pattern becomes entrenched",
            "Desire discrepancy",
            "In-law tension"
        ],
        stages=["honeymoon", "adjustment", "companionate", "renewal_or_decline"],
        promotion_criteria=["conflict_resolution", "intimacy_maintenance", "shared_meaning"],
        exit_triggers=["death", "divorce", "separation", "renewal"],
        natural_duration_years=(5, 50)
    ),
    
    # Athletic/Physical
    "competitive_athletics": Institution(
        name="Competitive Athletics",
        type=InstitutionType.ATHLETIC,
        description="High-level sport competition with physical and mental demands",
        expected_stances=[
            "pain tolerance",
            "competitive focus",
            "body awareness",
            "coach-ability"
        ],
        encounter_patterns=[
            "Competition with everything on the line",
            "Injury requiring long recovery",
            "Plateau in performance",
            "Younger competitor emerges",
            "Coach conflict over training approach",
            "Doping or cheating pressure"
        ],
        stages=["development", "competitive", "peak", "declining"],
        exit_triggers=["retirement", "injury", "career_best", "selection_failure"],
        natural_duration_years=(5, 20)
    ),
    
    # Therapeutic/Recovery
    "recovery_program": Institution(
        name="Recovery Program",
        type=InstitutionType.THERAPEUTIC,
        description="Structured recovery from addiction or major life crisis",
        expected_stances=[
            "radical honesty",
            "surrender",
            "one day at a time",
            "community reliance"
        ],
        forbidden_stances=[
            "ego maintenance",
            "isolation",
            "quick fixes"
        ],
        encounter_patterns=[
            "Trigger situation with substance available",
            "Relapse and recommitment",
            "Making amends to person who won't forgive",
            "Sponsor relationship challenge",
            "Anniversary milestone",
            "Life event tests sobriety"
        ],
        stages=["acute", "early_recovery", "maintenance", "long_term"],
        exit_triggers=["sustained_recovery", "relapse", "graduation", "death"],
        natural_duration_years=(1, 10)
    ),
}


def get_institution(name: str) -> Optional[Institution]:
    """Get an institution by name."""
    return INSTITUTIONS.get(name)


def list_institutions() -> List[str]:
    """List all available institution names."""
    return list(INSTITUTIONS.keys())


def get_institutions_by_type(inst_type: InstitutionType) -> List[Institution]:
    """Get all institutions of a given type."""
    return [inst for inst in INSTITUTIONS.values() if inst.type == inst_type]


def generate_career_path(
    starting_institution: str,
    num_phases: int = 4,
) -> List[str]:
    """
    Generate a plausible career path through institutions.
    
    Returns a list of institution names that could form a coherent
    life trajectory.
    """
    from conatus.simulation.biography import LifePhase, PhaseArc
    
    # Common trajectories
    trajectories = {
        "phd_program": ["postdoc", "corporate_ladder", "artistic_practice"],
        "postdoc": ["corporate_ladder", "tech_startup", "artistic_practice"],
        "tech_startup": ["corporate_ladder", "tech_startup", "artistic_practice"],
        "corporate_ladder": ["tech_startup", "artistic_practice", "parenthood"],
        "artistic_practice": ["corporate_ladder", "artistic_practice", "parenthood"],
        "music_conservatory": ["artistic_practice", "corporate_ladder", "parenthood"],
        "parenthood": ["corporate_ladder", "artistic_practice", "recovery_program"],
        "marriage": ["parenthood", "corporate_ladder", "recovery_program"],
        "competitive_athletics": ["corporate_ladder", "artistic_practice", "recovery_program"],
        "recovery_program": ["corporate_ladder", "artistic_practice", "parenthood"],
    }
    
    path = [starting_institution]
    current = starting_institution
    
    import random
    for _ in range(num_phases - 1):
        options = trajectories.get(current, list(INSTITUTIONS.keys()))
        # Avoid immediate repetition
        options = [o for o in options if o != current]
        if not options:
            options = list(INSTITUTIONS.keys())
        current = random.choice(options)
        path.append(current)
    
    return path
