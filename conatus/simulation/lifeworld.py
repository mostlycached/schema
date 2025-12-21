"""
LifeWorld Module: The Concrete Particulars of a Life

This module provides the material/concrete layer that gives lives their
specific texture. While narrative.py handles the form (arc, emplotment),
and biography.py handles the disposition (habitus, stances), lifeworld.py
handles the *content* — what the life is actually about.

Key insight: Lives aren't just careers. They're organized around:
- Places (the apartment, the hometown, the hospital room)
- Bodies (chronic pain, pregnancy, aging, disability)
- Objects (the inherited piano, the broken car, the manuscript)
- Practices (AA meetings, morning pages, meditation, drinking)
- Relationships (the mother, the ex, the sponsor, the child)
- Works (what is made — meals, children, gardens, papers)
- Central Concerns (what the life is "about" at any given moment)
"""

import os
import json
import random
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from enum import Enum

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))


# =============================================================================
# LIFE ARCHETYPES
# =============================================================================

class LifeArchetype(Enum):
    """
    Archetypal patterns that organize a life — not careers, but modes of being.
    These aren't exclusive; a life may move between them.
    """
    BUILDER = "builder"         # Making something that lasts
    CARETAKER = "caretaker"     # Caring for others (parent, nurse, companion)
    SEEKER = "seeker"           # Searching for meaning, truth, healing
    SURVIVOR = "survivor"       # Getting through (trauma, addiction, illness)
    DRIFTER = "drifter"         # Without clear center — which is itself a structure
    CREATOR = "creator"         # Making art, music, writing
    PROFESSIONAL = "professional"  # Career-organized (but still with particulars)
    DEVOTEE = "devotee"         # Religious, spiritual, cause-driven
    LOVER = "lover"             # Life organized around a relationship
    EXILE = "exile"             # Displaced, diaspora, seeking belonging


# =============================================================================
# PLACES
# =============================================================================

@dataclass
class Place:
    """
    A specific location that matters to this life.
    
    Not just "a city" but "the apartment on Maple Street where the 
    marriage ended" or "Mom's kitchen where we had Sunday dinners."
    """
    name: str  # "The apartment on Maple Street"
    type: str  # "home", "workplace", "hospital", "family_home", "refuge"
    significance: str  # Why it matters
    
    # Sensory particulars
    details: List[str] = field(default_factory=list)  # "The creaky third step"
    
    # Temporal
    entered_at_age: Optional[float] = None
    left_at_age: Optional[float] = None
    
    # What happens here
    rituals: List[str] = field(default_factory=list)  # "Sunday dinners"


# =============================================================================
# BODIES
# =============================================================================

@dataclass
class BodyFact:
    """
    A fact about this body that shapes the life.
    
    Not abstract "health" but specific conditions, capacities, changes.
    Bodies are not just obstacles but ways of being in the world.
    """
    condition: str  # "chronic lower back pain", "pregnant", "recovering from surgery"
    emerged_at_age: float
    
    how_it_shapes: str  # How this affects daily life
    coping_practices: List[str] = field(default_factory=list)  # "morning stretches"
    
    # Can it change?
    permanent: bool = True
    resolved_at_age: Optional[float] = None


# =============================================================================
# OBJECTS
# =============================================================================

@dataclass
class Object:
    """
    A specific object that matters to this life.
    
    Objects carry meaning, history, value. They can be inherited,
    lost, fought over, cherished.
    """
    name: str  # "Dad's watch"
    type: str  # "heirloom", "tool", "artwork", "vehicle", "document"
    significance: str  # Why it matters
    
    # History
    origin: str = ""  # "Inherited when Dad died"
    current_status: str = "possessed"  # "possessed", "lost", "sold", "given_away"
    
    # Sensory
    details: List[str] = field(default_factory=list)  # "The scratched crystal"


# =============================================================================
# PRACTICES
# =============================================================================

@dataclass
class Practice:
    """
    A recurring practice that structures daily life.
    
    Not abstract "habits" but specific rituals with texture.
    """
    name: str  # "Morning pages"
    frequency: str  # "daily", "weekly", "sporadic"
    
    what_it_involves: str  # "Three pages of longhand writing before anything else"
    why_it_matters: str  # "Keeps the anxiety at bay"
    
    # Where and when
    place: Optional[str] = None  # "The kitchen table"
    time: Optional[str] = None  # "5:30am"
    
    # History
    started_at_age: Optional[float] = None
    ended_at_age: Optional[float] = None


# =============================================================================
# WORKS
# =============================================================================

@dataclass
class Work:
    """
    Something made or accomplished — broadly defined.
    
    Not just "career output" but anything that counts as having made
    a difference: a meal, a child raised, a garden, a friendship maintained.
    """
    name: str  # "The dissertation", "Raising Maya", "The vegetable garden"
    type: str  # "project", "relationship", "creation", "care", "contribution"
    
    description: str
    
    # Status
    status: str = "ongoing"  # "ongoing", "completed", "abandoned", "lost"
    started_at_age: Optional[float] = None
    completed_at_age: Optional[float] = None
    
    # What it took
    what_it_cost: Optional[str] = None  # "Three years and my marriage"
    what_it_gave: Optional[str] = None  # "A sense of finally being legitimate"


# =============================================================================
# EVENTS
# =============================================================================

@dataclass
class Event:
    """
    A defining event — something that happened and changed things.
    """
    name: str  # "The diagnosis", "The move", "The divorce"
    type: str  # "loss", "gain", "transition", "discovery", "catastrophe"
    
    description: str  # What happened
    age: float
    
    # Impact
    what_changed: str  # "I could never trust doctors again"
    wounds_created: List[str] = field(default_factory=list)
    freedoms_opened: List[str] = field(default_factory=list)


# =============================================================================
# LIFEWORLD
# =============================================================================

@dataclass
class LifeWorld:
    """
    The complete concrete world of one life — all its particulars.
    
    This is what makes Sophia Keller's life *Sophia Keller's* and not
    just "a PhD student's life." It includes her specific apartment,
    her mother's illness, her dissertation topic, her morning routine.
    """
    # What is this life fundamentally about right now?
    central_concern: str  # "Finishing the dissertation while Mom is dying"
    
    # Life type (can shift)
    archetype: LifeArchetype = LifeArchetype.PROFESSIONAL
    
    # The particulars
    places: List[Place] = field(default_factory=list)
    body_facts: List[BodyFact] = field(default_factory=list)
    objects: List[Object] = field(default_factory=list)
    practices: List[Practice] = field(default_factory=list)
    
    # What has been made
    works: List[Work] = field(default_factory=list)
    
    # What has happened
    defining_events: List[Event] = field(default_factory=list)
    
    # Domain-specific knowledge (if professional/creator)
    domain_field: Optional[str] = None  # "Condensed Matter Physics"
    subfield: Optional[str] = None  # "2D Materials"
    central_question: Optional[str] = None  # "Can topological qubits work at room temp?"
    jargon: List[str] = field(default_factory=list)  # Field-specific vocabulary


# =============================================================================
# LIFEWORLD GENERATORS
# =============================================================================

def generate_lifeworld(
    name: str,
    age: float,
    archetype: LifeArchetype,
    institution: str = None,
    model_name: str = "gemini-2.0-flash",
) -> LifeWorld:
    """
    Generate a complete LifeWorld for a biography subject.
    
    Uses LLM to create coherent, specific particulars appropriate
    to the archetype and starting context.
    """
    model = genai.GenerativeModel(model_name)
    
    archetype_prompts = {
        LifeArchetype.BUILDER: "building something lasting (a business, a house, a family legacy)",
        LifeArchetype.CARETAKER: "caring for someone (aging parent, disabled child, sick partner)",
        LifeArchetype.SEEKER: "searching for meaning (spiritual quest, therapeutic recovery, truth-seeking)",
        LifeArchetype.SURVIVOR: "getting through each day (trauma recovery, addiction, illness)",
        LifeArchetype.DRIFTER: "moving without clear direction (between jobs, places, relationships)",
        LifeArchetype.CREATOR: "making art or music or writing (the creative life)",
        LifeArchetype.PROFESSIONAL: "building a career (with all its specifics)",
        LifeArchetype.DEVOTEE: "serving a cause or faith",
        LifeArchetype.LOVER: "organized around a central relationship",
        LifeArchetype.EXILE: "displaced, seeking belonging",
    }
    
    prompt = f"""Generate the concrete particulars of {name}'s life at age {age}.

LIFE ARCHETYPE: {archetype.value} — {archetype_prompts.get(archetype, '')}
{"STARTING CONTEXT: " + institution if institution else ""}

Generate a rich, specific LifeWorld with:

1. CENTRAL_CONCERN: What is this life fundamentally about right now? (one sentence)

2. PLACES (2-3 specific locations):
   - Each with a NAME (specific, not generic: "The studio apartment on Delancey" not "apartment")
   - TYPE (home/workplace/family_home/refuge/hospital)
   - SIGNIFICANCE (why it matters)
   - DETAILS (2-3 sensory specifics: "the smell of turpentine", "the creaky floorboard")

3. BODY_FACTS (1-2 bodily conditions that shape this life):
   - CONDITION (be specific: "chronic insomnia since the breakup" not just "insomnia")
   - HOW_IT_SHAPES (how this affects daily life)
   - COPING_PRACTICES (what they do about it)

4. OBJECTS (2-3 meaningful objects):
   - NAME (specific: "Dad's 1972 Gibson Les Paul" not just "guitar")
   - SIGNIFICANCE (why it matters emotionally)
   - ORIGIN (how they got it)

5. PRACTICES (2-3 regular practices that structure the day/week):
   - NAME and WHAT_IT_INVOLVES
   - WHY_IT_MATTERS to this person
   - TIME and PLACE

6. If this is a PROFESSIONAL or CREATOR:
   - FIELD and SUBFIELD
   - CENTRAL_QUESTION (what drives their work specifically)
   - JARGON (5-7 field-specific terms they use)

Respond in JSON format:
{{
  "central_concern": "...",
  "places": [
    {{"name": "...", "type": "...", "significance": "...", "details": ["...", "..."]}}
  ],
  "body_facts": [
    {{"condition": "...", "how_it_shapes": "...", "coping_practices": ["..."]}}
  ],
  "objects": [
    {{"name": "...", "significance": "...", "origin": "..."}}
  ],
  "practices": [
    {{"name": "...", "what_it_involves": "...", "why_it_matters": "...", "time": "...", "place": "..."}}
  ],
  "field": "..." or null,
  "subfield": "..." or null,
  "central_question": "..." or null,
  "jargon": ["...", "..."] or []
}}"""

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.8,
                max_output_tokens=1500
            )
        )
        
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        data = json.loads(text)
        
        # Build LifeWorld from response
        lifeworld = LifeWorld(
            central_concern=data.get("central_concern", "Finding their way"),
            archetype=archetype,
            domain_field=data.get("field"),
            subfield=data.get("subfield"),
            central_question=data.get("central_question"),
            jargon=data.get("jargon", []),
        )
        
        # Parse places
        for p in data.get("places", []):
            lifeworld.places.append(Place(
                name=p["name"],
                type=p.get("type", "home"),
                significance=p.get("significance", ""),
                details=p.get("details", []),
                entered_at_age=age,
            ))
        
        # Parse body facts
        for b in data.get("body_facts", []):
            lifeworld.body_facts.append(BodyFact(
                condition=b["condition"],
                emerged_at_age=age - random.randint(1, 10),  # Emerged sometime before
                how_it_shapes=b.get("how_it_shapes", ""),
                coping_practices=b.get("coping_practices", []),
            ))
        
        # Parse objects
        for o in data.get("objects", []):
            lifeworld.objects.append(Object(
                name=o["name"],
                type="heirloom",
                significance=o.get("significance", ""),
                origin=o.get("origin", ""),
            ))
        
        # Parse practices
        for pr in data.get("practices", []):
            lifeworld.practices.append(Practice(
                name=pr["name"],
                frequency="daily" if "daily" in pr.get("what_it_involves", "").lower() else "regular",
                what_it_involves=pr.get("what_it_involves", ""),
                why_it_matters=pr.get("why_it_matters", ""),
                place=pr.get("place"),
                time=pr.get("time"),
                started_at_age=age - random.randint(0, 5),
            ))
        
        return lifeworld
        
    except Exception as e:
        # Fallback: minimal LifeWorld
        return LifeWorld(
            central_concern="Making their way through life",
            archetype=archetype,
        )


def generate_encounter_with_particulars(
    lifeworld: LifeWorld,
    phase_name: str,
    subject_name: str,
    age: float,
    model_name: str = "gemini-2.0-flash",
) -> str:
    """
    Generate an encounter that uses the specific particulars of this LifeWorld.
    
    Instead of "A routine challenge", this produces something like:
    "The scanning tunneling microscope in the Nakamura lab breaks down again,
    three days before her thesis defense, and Dr. Vasquez is unreachable."
    """
    model = genai.GenerativeModel(model_name)
    
    # Build context from LifeWorld
    places_str = ", ".join([f"{p.name} ({p.significance})" for p in lifeworld.places[:2]])
    objects_str = ", ".join([f"{o.name} ({o.significance})" for o in lifeworld.objects[:2]])
    practices_str = ", ".join([f"{p.name}" for p in lifeworld.practices[:2]])
    body_str = ", ".join([f"{b.condition}" for b in lifeworld.body_facts[:2]])
    
    prompt = f"""Generate a SPECIFIC encounter for {subject_name}, age {age}, in phase "{phase_name}".

This life is organized around: {lifeworld.central_concern}
Life archetype: {lifeworld.archetype.value}

PARTICULARS TO USE:
- Places: {places_str or 'none specified'}
- Objects: {objects_str or 'none specified'}
- Practices: {practices_str or 'none specified'}
- Body: {body_str or 'none specified'}
{f"- Field: {lifeworld.domain_field} / {lifeworld.subfield}" if lifeworld.domain_field else ""}
{f"- Central Question: {lifeworld.central_question}" if lifeworld.central_question else ""}

Generate an encounter that:
1. Uses SPECIFIC places, objects, or practices from above
2. Is grounded in the CENTRAL CONCERN of this life
3. Is vivid and particular (not abstract like "a challenge arises")
4. Names specific things, places, times

Write 2-3 sentences. Use the actual names of places/objects.
Example: "The letter from the nursing home arrives while she's in the middle 
of her morning pages at the kitchen table. Mom has had another fall."

ENCOUNTER:"""

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.8,
                max_output_tokens=200
            )
        )
        return response.text.strip()
    except:
        return f"A moment in {phase_name} that tests {subject_name}'s resolve"


def add_work_to_lifeworld(
    lifeworld: LifeWorld,
    name: str,
    work_type: str,
    description: str,
    age: float,
    status: str = "ongoing",
) -> Work:
    """Add a new work/project/accomplishment to the LifeWorld."""
    work = Work(
        name=name,
        type=work_type,
        description=description,
        status=status,
        started_at_age=age,
    )
    lifeworld.works.append(work)
    return work


def add_event_to_lifeworld(
    lifeworld: LifeWorld,
    name: str,
    event_type: str,
    description: str,
    age: float,
    what_changed: str,
) -> Event:
    """Add a defining event to the LifeWorld."""
    event = Event(
        name=name,
        type=event_type,
        description=description,
        age=age,
        what_changed=what_changed,
    )
    lifeworld.defining_events.append(event)
    return event
