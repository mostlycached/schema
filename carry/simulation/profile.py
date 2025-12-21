"""
Profile Module: Natural Language Questionnaire for Assemblage Profiling

Maps ordinary questions about life patterns to Deleuzian assemblage concepts.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass, field
import json

from carry.simulation.assemblage import (
    Assemblage, Territory, Code, Component
)


@dataclass
class AssemblageProfile:
    """A completed profile of a person's assemblages."""
    subject_name: str
    assemblages: List[Assemblage]
    raw_responses: Dict = field(default_factory=dict)


# =============================================================================
# RESPONSE PARSER (Maps natural language to Deleuzian concepts)
# =============================================================================

def parse_natural_language_responses(responses: Dict) -> Assemblage:
    """
    Convert natural language questionnaire responses into Assemblage.
    
    Maps:
    - Q4 places with "Controlled/Free" -> Territories with smooth/striated
    - Q5 visible habits -> Codes (molar level)
    - Q6 invisible patterns -> Codes (molecular level)  
    - Q7 tools/body parts -> Components
    - Q8 feelings ratings -> Intensity field
    - Q9 becoming statements -> Becoming vectors
    - Q10 structure rating (0-10) -> Stratification depth (0.0-1.0)
    """
    
    # Parse territories (Q4)
    territories = []
    for line in responses.get("places", "").strip().split('\n'):
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 3:
                name, function, freedom = parts[0], parts[1], parts[2]
                space_type = "smooth" if "free" in freedom.lower() else "striated"
                territories.append(Territory(
                    name=name,
                    function=function,
                    quality=freedom,
                    space_type=space_type
                ))
    
    # Parse codes
    codes = []
    
    # Q5: Visible habits (molar)
    for line in responses.get("visible_habits", "").strip().split('\n'):
        if '|' in line:
            habit, when = [p.strip() for p in line.split('|', 1)]
            codes.append(Code(
                name=habit,
                content=when,
                type="habit",
                level="molar"
            ))
    
    # Q6: Invisible patterns (molecular)
    for line in responses.get("invisible_patterns", "").strip().split('\n'):
        if '|' in line:
            pattern, desc = [p.strip() for p in line.split('|', 1)]
            codes.append(Code(
                name=pattern,
                content=desc,
                type="unconscious_pattern",
                level="molecular"
            ))
    
    # Parse components (Q7)
    components = []
    for line in responses.get("tools", "").strip().split('\n'):
        if '|' in line:
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 2:
                name, capacity = parts[0], parts[1]
                # Infer type from context
                comp_type = "technical"
                if any(word in name.lower() for word in ["hand", "foot", "eye", "body", "breath"]):
                    comp_type = "organic"
                components.append(Component(
                    name=name,
                    type=comp_type,
                    capacity=capacity
                ))
    
    # Parse intensity field (Q8)
    intensity_field = {}
    feelings_map = {
        "speed/rushed": "speed",
        "tension/stress": "tension",
        "focus/concentration": "focus",
        "energy/aliveness": "energy",
        "control/discipline": "control",
        "connection to others": "connection",
        "physical sensation": "tactility"
    }
    
    for feeling, key in feelings_map.items():
        rating = responses.get(f"feeling_{key}", "")
        try:
            intensity_field[key] = float(rating) / 10.0  # Convert 0-10 to 0.0-1.0
        except (ValueError, TypeError):
            pass
    
    # Parse becomings (Q9)
    becoming_text = responses.get("becomings", "").strip()
    becoming_vectors = [
        line.strip() 
        for line in becoming_text.split('\n') 
        if line.strip() and not line.startswith('Example')
    ]
    
    # Parse stratification (Q10): 0-10 scale -> 0.0-1.0
    try:
        stratification_depth = float(responses.get("structure_rating", 5)) / 10.0
    except (ValueError, TypeError):
        stratification_depth = 0.5
    
    return Assemblage(
        name=responses.get("name", "Unnamed-Assemblage"),
        abstract_machine=responses.get("driving_force", "Unknown formula"),
        territories=territories,
        codes=codes,
        components=components,
        intensity_field=intensity_field,
        becoming_vectors=becoming_vectors,
        stratification_depth=stratification_depth
    )


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("Questionnaire available at: carry/questionnaire.md")
    print("\nExample usage:")
    print("1. Fill out questionnaire.md by hand")
    print("2. Create a Python dict with responses")
    print("3. Call parse_natural_language_responses(responses)")
    print("4. Get back an Assemblage object ready for simulation")
