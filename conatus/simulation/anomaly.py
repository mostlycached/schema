"""
Anomaly Generator: Productive Noise for Over-Stratified Systems

This module provides a generative scaffold for introducing molecular
disruptions into systems that have become too stable, too coded, too molar.

The problem: Systems (lives, organizations, routines) tend toward
stratification. They become rigid, predictable, "captured." There's
very little noise — and noise is where life happens.

The solution: Generate anomalies that introduce productive noise
without destroying the system. These are molecular interventions:
small cracks, different rhythms, unexpected alliances.

Five types of anomalies (from D&G + your SCHIZO.md):
1. RHYTHM - a different tempo in a routine
2. SPEED - acceleration or deceleration where there was constancy
3. ALLIANCE - an unexpected coupling (the pack, the war machine)
4. SCRIPT-BREAK - disruption of an Oedipal/molar script
5. ANOMALOUS - embracing the outsider element, the useless skill
"""

import os
import json
import random
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple
from enum import Enum

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))


# =============================================================================
# ANOMALY TYPES
# =============================================================================

class AnomalyType(Enum):
    """
    Types of productive noise that can be introduced.
    Each corresponds to a different kind of molecular intervention.
    """
    RHYTHM = "rhythm"          # Different tempo, timing, pacing
    SPEED = "speed"            # Faster or slower than the norm
    ALLIANCE = "alliance"      # Unexpected connection, pack formation
    SCRIPT_BREAK = "script_break"  # Disrupting a molar script
    ANOMALOUS = "anomalous"    # The outsider element, the useless skill
    MATERIAL = "material"      # Introducing a new object, tool, substance
    SPATIAL = "spatial"        # Different place, different arrangement
    SENSORY = "sensory"        # A different sense takes over
    SILENCE = "silence"        # Subtracting rather than adding
    INVERSION = "inversion"    # Reversing a power relation or direction


# =============================================================================
# ANOMALY
# =============================================================================

@dataclass
class Anomaly:
    """
    A specific generative disruption.
    
    An anomaly is not random chaos — it's *productive* noise.
    It opens a crack without shattering the system.
    """
    type: AnomalyType
    
    # What it disrupts
    target: str  # "morning routine", "parent-child script", "work meeting"
    
    # The specific intervention
    intervention: str  # "Read the story from the middle, not the beginning"
    
    # The proposed effect
    what_might_open: str  # "A different rhythm of attention"
    
    # Danger level (per D&G's Art of Caution)
    intensity: float = 0.3  # 0-1, where high intensity = more destratifying
    
    # Is it reversible?
    reversible: bool = True
    
    # What stays stable (the "small plot of land")
    what_remains: str = ""  # "The bedtime ritual continues, just differently"


# =============================================================================
# SYSTEM PROFILE
# =============================================================================

@dataclass
class SystemProfile:
    """
    A profile of a system that might need productive noise.
    
    This could be a life (like Elena's), an organization, a routine,
    a relationship — anything that has become over-stratified.
    """
    name: str
    description: str
    
    # The molar structures (what's rigid)
    molar_patterns: List[str] = field(default_factory=list)
    # e.g., ["Morning Meds at 7am", "Parent reads to child", "I am the caretaker"]
    
    # Current stratification level (0-1)
    stratification: float = 0.7
    
    # Where are the existing cracks (if any)?
    existing_cracks: List[str] = field(default_factory=list)
    
    # The flows that move through this system
    flows: List[str] = field(default_factory=list)
    # e.g., ["care", "money", "language", "desire", "fatigue"]
    
    # What MUST remain stable (the organism needs to survive)
    non_negotiables: List[str] = field(default_factory=list)
    # e.g., ["Rosa receives medication", "Mateo is safe"]
    
    # Hidden anomalous elements (suppressed "useless" capacities)
    latent_anomalies: List[str] = field(default_factory=list)
    # e.g., ["Elena used to paint", "There's a piano in the basement"]
    
    # Plots of land (generated or specified)
    plots_of_land: List['PlotOfLand'] = field(default_factory=list)


# =============================================================================
# PLOTS OF LAND
# =============================================================================

class PlotType(Enum):
    """
    Types of stable ground that can anchor destratification.
    
    "You have to keep enough of the organism for it to reform each dawn;
    and you have to keep small supplies of significance and interpretation...
    small rations of subjectivity... to enable you to respond to the 
    dominant reality." — A Thousand Plateaus
    """
    BODILY = "bodily"           # Sleep, food, shelter, health basics
    RELATIONAL = "relational"   # Key relationships that can't be risked
    ECONOMIC = "economic"       # Income, housing, basic resources
    SPATIAL = "spatial"         # A physical place of safety
    TEMPORAL = "temporal"       # Time structures that anchor
    SYMBOLIC = "symbolic"       # Name, identity markers, credentials
    COMPETENCE = "competence"   # Skills that provide stability


@dataclass
class PlotOfLand:
    """
    A small plot of land — what must remain stable while experimenting.
    
    Per D&G: You need stable ground to destratify from. The schizo
    who has no ground at all doesn't fly — they shatter.
    
    This is NOT about conservatism. It's about tactical survival.
    The plot of land is what lets you experiment without dying.
    """
    type: PlotType
    
    # What specifically is this ground?
    description: str  # "The apartment on Maple Street — a place to return to"
    
    # Why is it essential?
    function: str  # "Provides basic shelter and a space to sleep"
    
    # What would happen if it were lost?
    if_lost: str  # "Homelessness, no base for any experimentation"
    
    # How fragile is it? (0-1, where 1 = very fragile, could be lost easily)
    fragility: float = 0.3
    
    # Can it be shared/distributed? (reduces individual burden)
    distributable: bool = False
    
    # What cracks CAN be introduced here without losing it?
    permissible_cracks: List[str] = field(default_factory=list)


def generate_plots_of_land(
    system: SystemProfile,
    model_name: str = "gemini-2.0-flash",
) -> List[PlotOfLand]:
    """
    Enumerate the plots of land for a system.
    
    These are the stable grounds that MUST remain while introducing
    anomalies. Without them, destratification becomes destruction.
    
    D&G's warning: "Staying stratified — organized, signified, subjected —
    is not the worst that can happen; the worst that can happen is if you
    throw the strata into demented or suicidal collapse."
    """
    model = genai.GenerativeModel(model_name)
    
    plot_types_str = ", ".join([t.value for t in PlotType])
    
    prompt = f"""Enumerate the "plots of land" for this system.

SYSTEM: {system.name}
DESCRIPTION: {system.description}

CONTEXT:
A "plot of land" (from Deleuze & Guattari) is stable ground that must remain
while experimenting with flows. Without it, destratification becomes collapse.

"You have to keep enough of the organism for it to reform each dawn."

MOLAR PATTERNS (current structures):
{chr(10).join(['- ' + p for p in system.molar_patterns]) or '- None specified'}

NON-NEGOTIABLES (already identified):
{chr(10).join(['- ' + n for n in system.non_negotiables]) or '- None specified'}

FLOWS:
{chr(10).join(['- ' + f for f in system.flows]) or '- None specified'}

---

Identify 5-7 PLOTS OF LAND for this system. These are:
- What MUST remain stable for survival
- The ground from which experimentation can happen
- What would cause collapse if lost

PLOT TYPES: {plot_types_str}

For each plot:
1. TYPE (one of the above)
2. DESCRIPTION (specific, not abstract)
3. FUNCTION (why it's essential for survival)
4. IF_LOST (what would happen — be concrete)
5. FRAGILITY (0.0-1.0, how easily could this be lost)
6. DISTRIBUTABLE (can others share this burden? true/false)
7. PERMISSIBLE_CRACKS (what small experiments CAN happen here without losing it)

Respond in JSON:
{{
  "plots": [
    {{
      "type": "<plot_type>",
      "description": "<specific anchor>",
      "function": "<why essential>",
      "if_lost": "<concrete consequence>",
      "fragility": <0.0-1.0>,
      "distributable": <true|false>,
      "permissible_cracks": ["<crack1>", "<crack2>"]
    }}
  ]
}}"""

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=1500
            )
        )
        
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        data = json.loads(text)
        
        plots = []
        for p in data.get("plots", []):
            try:
                plot_type = PlotType(p.get("type", "bodily"))
            except ValueError:
                plot_type = PlotType.BODILY
            
            plots.append(PlotOfLand(
                type=plot_type,
                description=p.get("description", ""),
                function=p.get("function", ""),
                if_lost=p.get("if_lost", ""),
                fragility=float(p.get("fragility", 0.3)),
                distributable=p.get("distributable", False),
                permissible_cracks=p.get("permissible_cracks", []),
            ))
        
        return plots
        
    except Exception as e:
        # Fallback
        return [
            PlotOfLand(
                type=PlotType.BODILY,
                description="Basic sleep and nutrition",
                function="Organism survival",
                if_lost="Physical collapse, inability to function",
                fragility=0.5,
            )
        ]


def display_plots_of_land(plots: List[PlotOfLand]) -> str:
    """Format plots of land for display."""
    lines = [
        "# Plots of Land",
        "",
        "> What must remain stable while experimenting with flows.",
        "> 'Keep enough of the organism for it to reform each dawn.'",
        "",
    ]
    
    icons = {
        PlotType.BODILY: "🫀",
        PlotType.RELATIONAL: "👥",
        PlotType.ECONOMIC: "💰",
        PlotType.SPATIAL: "🏠",
        PlotType.TEMPORAL: "⏰",
        PlotType.SYMBOLIC: "📛",
        PlotType.COMPETENCE: "🔧",
    }
    
    for i, p in enumerate(plots, 1):
        icon = icons.get(p.type, "📍")
        fragility_bar = "█" * int(p.fragility * 5) + "░" * (5 - int(p.fragility * 5))
        
        lines.extend([
            f"## {i}. {icon} {p.type.value.upper()}",
            "",
            f"**Ground**: {p.description}",
            "",
            f"**Function**: {p.function}",
            "",
            f"**If Lost**: ⚠️ {p.if_lost}",
            "",
            f"**Fragility**: {fragility_bar} ({p.fragility:.1f})",
            f"**Distributable**: {'Yes' if p.distributable else 'No'}",
            "",
        ])
        
        if p.permissible_cracks:
            lines.append("**Cracks permissible here**:")
            for crack in p.permissible_cracks:
                lines.append(f"  - {crack}")
            lines.append("")
        
        lines.extend(["---", ""])
    
    return "\n".join(lines)


# =============================================================================
# ANOMALY GENERATOR
# =============================================================================

def generate_anomalies(
    system: SystemProfile,
    count: int = 5,
    max_intensity: float = 0.5,
    model_name: str = "gemini-2.0-flash",
) -> List[Anomaly]:
    """
    Generate productive anomalies for a system.
    
    Uses LLM to create specific, contextual disruptions that
    could introduce molecular cracks without shattering.
    """
    model = genai.GenerativeModel(model_name)
    
    anomaly_types_str = ", ".join([t.value for t in AnomalyType])
    
    prompt = f"""Generate {count} productive anomalies for this system.

SYSTEM: {system.name}
DESCRIPTION: {system.description}

MOLAR PATTERNS (what's rigid, over-coded):
{chr(10).join(['- ' + p for p in system.molar_patterns]) or '- None specified'}

CURRENT FLOWS:
{chr(10).join(['- ' + f for f in system.flows]) or '- None specified'}

NON-NEGOTIABLES (what must stay stable):
{chr(10).join(['- ' + n for n in system.non_negotiables]) or '- None specified'}

LATENT ANOMALIES (hidden capacities, suppressed elements):
{chr(10).join(['- ' + a for a in system.latent_anomalies]) or '- None specified'}

EXISTING CRACKS (if any):
{chr(10).join(['- ' + c for c in system.existing_cracks]) or '- None'}

---

Generate PRODUCTIVE NOISE that could open molecular cracks.
These are NOT random disruptions but GENERATIVE interventions.

ANOMALY TYPES: {anomaly_types_str}

For each anomaly:
1. Choose a TYPE
2. Identify a TARGET (specific molar pattern to disrupt)
3. Describe the INTERVENTION (specific, actionable, small)
4. Describe WHAT MIGHT OPEN (the potential line of flight)
5. Rate INTENSITY (0.0-{max_intensity}, where higher = more destratifying)
6. Note WHAT REMAINS STABLE (the small plot of land)

IMPORTANT: 
- These must be SMALL CRACKS, not revolutions
- They must respect NON-NEGOTIABLES
- They should be specific to THIS system (not generic advice)
- They should use or activate LATENT ANOMALIES when possible

Respond in JSON:
{{
  "anomalies": [
    {{
      "type": "<anomaly_type>",
      "target": "<specific molar pattern>",
      "intervention": "<the specific small disruption>",
      "what_might_open": "<potential effect>",
      "intensity": <0.0-{max_intensity}>,
      "what_remains": "<what stays stable>"
    }}
  ]
}}"""

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.85,
                max_output_tokens=1500
            )
        )
        
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        data = json.loads(text)
        
        anomalies = []
        for a in data.get("anomalies", []):
            try:
                anomaly_type = AnomalyType(a.get("type", "rhythm"))
            except ValueError:
                anomaly_type = AnomalyType.RHYTHM
            
            anomalies.append(Anomaly(
                type=anomaly_type,
                target=a.get("target", ""),
                intervention=a.get("intervention", ""),
                what_might_open=a.get("what_might_open", ""),
                intensity=min(max_intensity, float(a.get("intensity", 0.3))),
                reversible=True,
                what_remains=a.get("what_remains", ""),
            ))
        
        return anomalies
        
    except Exception as e:
        # Fallback: generate simple anomalies
        return [
            Anomaly(
                type=AnomalyType.RHYTHM,
                target="daily routine",
                intervention="Introduce a 10-minute pause at an unexpected moment",
                what_might_open="A different relationship to time",
                intensity=0.2,
                what_remains="The routine continues, just with a gap",
            )
        ]


def generate_anomaly_for_encounter(
    encounter_description: str,
    lifeworld_context: str = "",
    model_name: str = "gemini-2.0-flash",
) -> Anomaly:
    """
    Generate a single anomaly that could be introduced into a specific encounter.
    
    Used to inject productive noise into the biography simulation.
    """
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""An encounter is happening:

ENCOUNTER: {encounter_description}

CONTEXT: {lifeworld_context or 'No additional context'}

Generate ONE small molecular disruption that could be introduced here.
NOT a different choice, but a different RHYTHM, SPEED, ALLIANCE, or SCRIPT-BREAK.

Something that keeps the situation intact but introduces a crack.

Example: If the encounter is "Morning meds round is interrupted when Rosa falls,"
the anomaly might be "Elena sits down next to Rosa on the floor instead of 
immediately picking her up. For thirty seconds, they are just two bodies on the floor."

Respond in JSON:
{{
  "type": "<rhythm|speed|alliance|script_break|anomalous|silence|inversion>",
  "intervention": "<the specific small crack>",
  "what_might_open": "<what could this allow?>"
}}"""

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.9,
                max_output_tokens=300
            )
        )
        
        text = response.text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        data = json.loads(text)
        
        try:
            anomaly_type = AnomalyType(data.get("type", "rhythm"))
        except ValueError:
            anomaly_type = AnomalyType.RHYTHM
        
        return Anomaly(
            type=anomaly_type,
            target=encounter_description[:50],
            intervention=data.get("intervention", ""),
            what_might_open=data.get("what_might_open", ""),
            intensity=0.3,
            reversible=True,
        )
        
    except:
        return Anomaly(
            type=AnomalyType.SILENCE,
            target=encounter_description[:50],
            intervention="A pause. A breath. Nothing happens for a moment.",
            what_might_open="Space",
            intensity=0.2,
        )


# =============================================================================
# SYSTEM PROFILE GENERATORS
# =============================================================================

def profile_from_lifeworld(
    name: str,
    lifeworld: 'LifeWorld',
    stratification: float = 0.7,
) -> SystemProfile:
    """
    Create a system profile from a LifeWorld (from lifeworld.py).
    """
    # Extract molar patterns from practices
    molar_patterns = []
    for p in lifeworld.practices:
        if p.time and p.name:
            molar_patterns.append(f"{p.name} at {p.time}")
        else:
            molar_patterns.append(p.name)
    
    # Add the central concern as a molar pattern
    molar_patterns.append(f"Central concern: {lifeworld.central_concern}")
    
    # Extract flows from body facts and central concern
    flows = ["care", "fatigue", "desire"]
    for b in lifeworld.body_facts:
        flows.append(b.condition.split()[0])  # First word of condition
    
    # Non-negotiables would need to be specified, but we can infer some
    non_negotiables = []
    if "child" in lifeworld.central_concern.lower() or "son" in lifeworld.central_concern.lower():
        non_negotiables.append("Child safety and basic care")
    if "mother" in lifeworld.central_concern.lower() or "parent" in lifeworld.central_concern.lower():
        non_negotiables.append("Elder care essentials")
    
    # Latent anomalies from objects and suppressed interests
    latent_anomalies = []
    for o in lifeworld.objects:
        if "old" in o.origin.lower() or "used to" in o.significance.lower():
            latent_anomalies.append(f"{o.name}: {o.significance}")
    
    return SystemProfile(
        name=name,
        description=lifeworld.central_concern,
        molar_patterns=molar_patterns,
        stratification=stratification,
        flows=flows,
        non_negotiables=non_negotiables,
        latent_anomalies=latent_anomalies,
    )


def quick_profile(
    name: str,
    description: str,
    patterns: List[str],
    flows: List[str] = None,
    non_negotiables: List[str] = None,
    latent: List[str] = None,
) -> SystemProfile:
    """
    Quick helper to create a system profile.
    """
    return SystemProfile(
        name=name,
        description=description,
        molar_patterns=patterns,
        flows=flows or ["desire", "energy", "money", "language"],
        non_negotiables=non_negotiables or [],
        latent_anomalies=latent or [],
    )


# =============================================================================
# DISPLAY
# =============================================================================

def display_anomalies(anomalies: List[Anomaly]) -> str:
    """
    Format anomalies for display.
    """
    lines = [
        "# Productive Noise Generator",
        "",
        "> Small cracks, not revolutions. Molecular, not molar.",
        "",
    ]
    
    for i, a in enumerate(anomalies, 1):
        icon = {
            AnomalyType.RHYTHM: "🎵",
            AnomalyType.SPEED: "⏱",
            AnomalyType.ALLIANCE: "🤝",
            AnomalyType.SCRIPT_BREAK: "📜✂️",
            AnomalyType.ANOMALOUS: "👾",
            AnomalyType.MATERIAL: "🔧",
            AnomalyType.SPATIAL: "📍",
            AnomalyType.SENSORY: "👁",
            AnomalyType.SILENCE: "🔇",
            AnomalyType.INVERSION: "🔄",
        }.get(a.type, "•")
        
        intensity_bar = "█" * int(a.intensity * 10) + "░" * (10 - int(a.intensity * 10))
        
        lines.extend([
            f"## {i}. {icon} {a.type.value.upper()}",
            "",
            f"**Target**: {a.target}",
            "",
            f"**Intervention**: *{a.intervention}*",
            "",
            f"**What might open**: {a.what_might_open}",
            "",
            f"**Intensity**: {intensity_bar} ({a.intensity:.1f})",
            "",
            f"**What remains stable**: {a.what_remains}" if a.what_remains else "",
            "",
            "---",
            "",
        ])
    
    return "\n".join(lines)
