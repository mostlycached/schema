"""
Assemblage Module: Pure Deleuzian Simulation

This module replaces the "LifeWorld" concept with the "Assemblage".
An assemblage is not a collection of substances, but a layout of:
1. Territories (spatial/functional boundaries)
2. Codes (rules, semiotics, habits)
3. Components (heterogeneous elements: organic, technical, signs)

A subject is not ONE assemblage, but MULTIPLE assemblages intersecting at a body.
"""

import os
import json
from typing import List, Optional, Dict
from dataclasses import dataclass, field
from copy import deepcopy

import google.generativeai as genai
from dotenv import load_dotenv

from carry.simulation.carry import BareObject, get_bare_object

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))


# =============================================================================
# DELEUZIAN DATA STRUCTURES
# =============================================================================

@dataclass
class Territory:
    """A bounded domain of function or meaning."""
    name: str
    function: str
    quality: str  # The "expressive" quality (e.g. "sanctuary", "fast-paced")
    space_type: str = "striated"  # "smooth" or "striated"

@dataclass
class Code:
    """A rule, habit, or semiotic constraint."""
    name: str
    content: str  # What the code prescribes
    type: str     # "habit", "social_rule", "biological_rhythm"
    level: str = "molar"  # "molar" (macro) or "molecular" (micro)

@dataclass
class Component:
    """Heterogeneous element in the assemblage."""
    name: str
    type: str     # "organic", "technical", "sign"
    capacity: str # What it CAN DO (not what it is)

@dataclass
class LineOfFlight:
    """A vector of escape, rupture, or transformation with its source."""
    direction: str  # Where it leads (e.g., "Open source collaboration", "Burnout escape")
    source_type: str  # "tension", "incompatibility", "breaking_point", "conflict"
    source_description: str  # What generates this line (e.g., "Speed 0.8 + Tension 0.7 unsustainable")
    trigger_conditions: str = ""  # What would actualize it (optional)

@dataclass
class VirtualCapacity:
    """Real but unactualized potential with its structural basis."""
    name: str  # What could be actualized
    access_point: str  # The structural position that makes it real (e.g., "Senior developer status")
    reason_unactualized: str  # Why it hasn't been triggered yet
    actualization_trigger: str = ""  # What would actualize it (optional)

@dataclass
class Assemblage:
    """
    A machinic arrangement of bodies, tools, and signs.
    Defined by what connections it holds together.
    """
    name: str  # "Marcus-Corporate-Assemblage"
    abstract_machine: str  # The diagram/formula (e.g. "Accumulating status through speed")
    
    territories: List[Territory] = field(default_factory=list)
    codes: List[Code] = field(default_factory=list)
    components: List[Component] = field(default_factory=list)
    
    lines_of_flight: List[LineOfFlight] = field(default_factory=list)  # Vectors of escape with sources
    
    # Extended Deleuzian concepts
    intensity_field: Dict[str, float] = field(default_factory=dict)  # BwO: raw capacities/intensities
    becoming_vectors: List[str] = field(default_factory=list)  # Ongoing transformations
    stratification_depth: float = 0.5  # 0 = pure BwO, 1 = fully stratified
    
    # Virtual/Actual distinction
    virtual_capacities: List[VirtualCapacity] = field(default_factory=list)  # Real but unactualized potentials

    def describe(self) -> str:
        """Text description for LLM prompting."""
        return json.dumps({
            "abstract_machine": self.abstract_machine,
            "territories": [{"name": t.name, "function": t.function} for t in self.territories],
            "codes": [{"name": c.name, "content": c.content} for c in self.codes],
            "components": [{"name": c.name, "capacity": c.capacity} for c in self.components]
        }, indent=2)


@dataclass
class ReconfigurationResult:
    """The result of an operator modifying an assemblage."""
    before: Assemblage
    after: Assemblage
    operator: BareObject
    
    # Delta tracking
    deterritorialized: List[str] = field(default_factory=list)
    reterritorialized: List[str] = field(default_factory=list)
    decoded: List[str] = field(default_factory=list)
    recoded: List[str] = field(default_factory=list)
    new_components: List[str] = field(default_factory=list)


# =============================================================================
# GENERATORS
# =============================================================================

def generate_assemblages_for_subject(
    subject_name: str,
    context: str,
    model_name: str = "gemini-2.0-flash",
) -> List[Assemblage]:
    """
    Generate MULTIPLE distinct assemblages that intersect at the subject.
    A subject is not one thing, but a traffic jam of multiple machines.
    """
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""Decompose the subject '{subject_name}' into multiple DISTINCT Deleuzian Assemblages.
Context: {context}

Do not create a monolithic "person". Create the SEPARATE machines they plug into.

For EACH assemblage, define EXTENDED Deleuzian concepts:

1. Name (e.g. "Marcus-Professional-Assemblage")
2. Abstract Machine (The formula driving it)
3. Territories with SPACE TYPE:
   - "smooth" (open, nomadic, continuous variation - e.g. open park, improvisation)
   - "striated" (gridded, organized, controlled - e.g. office cubicles, scheduled time)
4. Codes with LEVEL:
   - "molar" (macro-level: visible habits, social roles, identities)
   - "molecular" (micro-level: breathing rhythms, micro-gestures, subliminal desires)
5. Components (Working parts)
6. Intensity Field (BwO): Dict of raw capacities/affects with intensity 0.0-1.0
   Example: {{"speed": 0.8, "tension": 0.6, "tactility": 0.3}}
7. Becoming Vectors: Ongoing transformations (e.g. "becoming-machine", "becoming-slower")
8. Stratification Depth (0.0 = pure BwO/chaos, 1.0 = fully rigid/organized)
9. Virtual Capacities: Real but unactualized potentials
   Example: ["Coursera subscription (unused)", "Gym membership (dormant)", "Access to Python library"]

JSON Format:
{{
  "assemblages": [
    {{
      "name": "...",
      "abstract_machine": "...",
      "territories": [{{"name": "...", "function": "...", "quality": "...", "space_type": "smooth/striated"}}],
      "codes": [{{"name": "...", "content": "...", "type": "...", "level": "molar/molecular"}}],
      "components": [{{"name": "...", "type": "...", "capacity": "..."}}],
      "intensity_field": {{"speed": 0.0, "tension": 0.0}},
      "becoming_vectors": ["..."],
      "stratification_depth": 0.5,
      "virtual_capacities": ["..."]
    }},
    ...
  ]
}}
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```json" in text: text = text.split("```json")[1].split("```")[0]
        elif "```" in text: text = text.split("```")[1].split("```")[0]
        data = json.loads(text)
        
        results = []
        for asm_data in data.get("assemblages", []):
            results.append(Assemblage(
                name=asm_data["name"],
                abstract_machine=asm_data["abstract_machine"],
                territories=[Territory(**t) for t in asm_data["territories"]],
                codes=[Code(**c) for c in asm_data["codes"]],
                components=[Component(**c) for c in asm_data["components"]],
                lines_of_flight=[],
                intensity_field=asm_data.get("intensity_field", {}),
                becoming_vectors=asm_data.get("becoming_vectors", []),
                stratification_depth=asm_data.get("stratification_depth", 0.5),
                virtual_capacities=asm_data.get("virtual_capacities", [])
            ))
        return results
        
    except Exception as e:
        print(f"Error generating assemblages: {e}")
        return []


def insert_operator(
    assemblage: Assemblage,
    operator: BareObject,
    model_name: str = "gemini-2.0-flash"
) -> ReconfigurationResult:
    """
    Insert a BareObject (Operator) into a SPECIFIC Assemblage.
    """
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""You are a Deleuzian Machine.
    
CURRENT ASSEMBLAGE:
{assemblage.describe()}
Current Stratification Depth: {assemblage.stratification_depth}
Current Intensity Field: {assemblage.intensity_field}
Current Becoming Vectors: {assemblage.becoming_vectors}

NEW OPERATOR ENTERING:
Name: {operator.name}
Material: {operator.material}
Form: {operator.form}
Persistence: {operator.persistence}
Origin: {operator.origin}

The operator forces reconfiguration across MULTIPLE DELEUZIAN DIMENSIONS:

1. TERRITORIES: Does it smooth striated space? Striate smooth space?
2. CODES: Does it break molar codes into molecular flows? Recode molecular processes into molar habits?
3. INTENSITY FIELD (BwO): How do raw capacities shift? (speed, tension, tactility, etc.) 
4. BECOMING VECTORS: What transformations does it trigger? (becoming-slower, becoming-animal, becoming-imperceptible)
5. STRATIFICATION DEPTH: Does it destratify (toward 0.0 chaos/BwO) or restratify (toward 1.0 rigid/organized)?

JSON Format:
{{
  "new_abstract_machine": "...",
  "new_stratification_depth": 0.5,
  
  "territories_transformed": [
    {{"name": "Territory Name", "new_function": "...", "change_type": "deterritorialized/reterritorialized", "new_space_type": "smooth/striated"}}
  ],
  "territories_added": [
    {{"name": "...", "function": "...", "quality": "...", "space_type": "smooth/striated"}}
  ],
  
  "codes_broken": ["Name of code broken"],
  "codes_formed": [
    {{"name": "...", "content": "...", "type": "...", "level": "molar/molecular"}}
  ],
  
  "intensity_field_changes": {{"speed": 0.0, "tension": 0.0, "tactility": 0.0}},
  "becoming_vectors_added": ["becoming-...", "..."],
  
  "components_added": [
    {{"name": "...", "type": "technical/organic", "capacity": "..."}}
  ],
  "lines_of_flight_opened": ["..."]
}}
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        if "```json" in text: text = text.split("```json")[1].split("```")[0]
        elif "```" in text: text = text.split("```")[1].split("```")[0]
        data = json.loads(text)
        
        # Construct AFTER assemblage
        after = deepcopy(assemblage)
        after.abstract_machine = data["new_abstract_machine"]
        after.stratification_depth = data.get("new_stratification_depth", assemblage.stratification_depth)
        
        # Apply transformation logic
        transformed_map = {t["name"]: t for t in data.get("territories_transformed", [])}
        for t in after.territories:
            if t.name in transformed_map:
                t.function = transformed_map[t.name]["new_function"]
                if "new_space_type" in transformed_map[t.name]:
                    t.space_type = transformed_map[t.name]["new_space_type"]
        
        for t in data.get("territories_added", []):
            after.territories.append(Territory(**t))
            
        broken_names = set(data.get("codes_broken", []))
        after.codes = [c for c in after.codes if c.name not in broken_names]
        
        for c in data.get("codes_formed", []):
            after.codes.append(Code(**c))
        
        # Update intensity field
        for key, delta in data.get("intensity_field_changes", {}).items():
            current = after.intensity_field.get(key, 0.0)
            after.intensity_field[key] = max(0.0, min(1.0, current + delta))
        
        # Add becoming vectors
        after.becoming_vectors.extend(data.get("becoming_vectors_added", []))
            
        after.components.append(Component(operator.name, "technical", "Operator"))
        for c in data.get("components_added", []):
            after.components.append(Component(**c))
            
        after.lines_of_flight = data.get("lines_of_flight_opened", [])
        
        return ReconfigurationResult(
            before=assemblage,
            after=after,
            operator=operator,
            deterritorialized=[t["name"] for t in data.get("territories_transformed", []) if "de" in t["change_type"]],
            reterritorialized=[t["name"] for t in data.get("territories_transformed", []) if "re" in t["change_type"]],
            decoded=list(broken_names),
            recoded=[c["name"] for c in data.get("codes_formed", [])],
        )
        
    except Exception as e:
        print(f"Error in reconfiguration: {e}")
        return ReconfigurationResult(assemblage, assemblage, operator)


def report_assemblage_morph(result: ReconfigurationResult) -> str:
    """Generate a comparison report with extended Deleuzian dimensions."""
    
    report = f"""## {result.before.name}
    
**Abstract Machine Shift**
*{result.before.abstract_machine}* 
⬇
*{result.after.abstract_machine}*

**Stratification**: {result.before.stratification_depth:.2f} → {result.after.stratification_depth:.2f}
"""
    
    # Intensity Field (BwO)
    if result.before.intensity_field or result.after.intensity_field:
        report += "\n**Intensity Field (BwO)**\n"
        all_keys = set(result.before.intensity_field.keys()) | set(result.after.intensity_field.keys())
        for key in all_keys:
            before_val = result.before.intensity_field.get(key, 0.0)
            after_val = result.after.intensity_field.get(key, 0.0)
            if before_val != after_val:
                report += f"- {key}: {before_val:.2f} → {after_val:.2f}\n"

    # Territorial Shifts
    report += "\n**Territorial Shifts**\n"
    if not result.deterritorialized and not result.reterritorialized:
        report += "- *No significant territorial shifts*\n"
    
    for t_name in result.deterritorialized:
        # Find space type change
        before_t = next((t for t in result.before.territories if t.name == t_name), None)
        after_t = next((t for t in result.after.territories if t.name == t_name), None)
        if before_t and after_t and before_t.space_type != after_t.space_type:
            report += f"- **{t_name}**: DETERRITORIALIZED ({before_t.space_type} → {after_t.space_type})\n"
        else:
            report += f"- **{t_name}**: DETERRITORIALIZED\n"
            
    for t_name in result.reterritorialized:
        before_t = next((t for t in result.before.territories if t.name == t_name), None)
        after_t = next((t for t in result.after.territories if t.name == t_name), None)
        if before_t and after_t and before_t.space_type != after_t.space_type:
            report += f"- **{t_name}**: RETERRITORIALIZED ({before_t.space_type} → {after_t.space_type})\n"
        else:
            report += f"- **{t_name}**: RETERRITORIALIZED\n"

    # Code Shifts (with molar/molecular indicators)
    report += "\n**Code Shifts**\n"
    if not result.decoded and not result.recoded:
        report += "- *No significant code shifts*\n"

    for c_name in result.decoded:
        before_c = next((c for c in result.before.codes if c.name == c_name), None)
        level_str = f" [{before_c.level}]" if before_c else ""
        report += f"- ~~{c_name}{level_str}~~ (Decoded)\n"
        
    for c_name in result.recoded:
        after_c = next((c for c in result.after.codes if c.name == c_name), None)
        level_str = f" [{after_c.level}]" if after_c else ""
        report += f"- **{c_name}{level_str}** (Recoded)\n"

    # Becoming Vectors
    if result.after.becoming_vectors:
        report += "\n**Becoming Vectors**\n"
        for bv in result.after.becoming_vectors:
            report += f"- {bv}\n"

    # Lines of Flight
    report += "\n**Lines of Flight**\n"
    if result.after.lines_of_flight:
        for l in result.after.lines_of_flight:
            report += f"- -> {l}\n"
    else:
        report += "- *None*\n"
    
    # Virtual Capacities (unactualized potentials)
    if result.after.virtual_capacities:
        report += "\n**Virtual Capacities** *(latent, unactualized)*\n"
        for vc in result.after.virtual_capacities:
            report += f"- {vc}\n"
        
    report += "\n---\n"
    return report


if __name__ == "__main__":
    print("Generating Assemblages for Marcus...\n")
    assemblages = generate_assemblages_for_subject(
        "Marcus", 
        "Software engineer, ambitious, lives in SF, follows strict optimization routines. Weekend hiker."
    )
    
    print(f"Generated {len(assemblages)} assemblages:")
    for asm in assemblages:
        print(f"  - {asm.name}")
    
    cane = get_bare_object("cane")
    print(f"\nInserting Operator: {cane.name}\n")
    
    full_report = f"# Multi-Assemblage Analysis: Marcus + {cane.name}\n\n"
    full_report += f"**Operator**: {cane.name} ({cane.material}, {cane.form})\n\n---\n\n"
    
    for asm in assemblages:
        print(f"Processing {asm.name}...")
        result = insert_operator(asm, cane)
        full_report += report_assemblage_morph(result)
    
    print("\n" + full_report)
    
    with open("carry/results/multi_assemblage_cane.md", "w") as f:
        f.write(full_report)
    
    print("\nSaved to carry/results/multi_assemblage_cane.md")
