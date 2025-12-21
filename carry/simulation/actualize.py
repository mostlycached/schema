"""
Actualization Module: Virtual → Actual Transformations

Models the Deleuzian process of actualizing virtual capacities.
Virtual capacities (subscriptions, access, credentials) become actualized
through use, transforming into active codes, territories, and becomings.
"""

from typing import List, Dict
from dataclasses import dataclass
from copy import deepcopy

from carry.simulation.assemblage import Assemblage, Code, Territory, Component


@dataclass
class ActualizationEvent:
    """Represents the actualization of a virtual capacity."""
    virtual_capacity: str  # What was virtual
    trigger: str  # What caused actualization (e.g., "Started using Coursera", "First gym visit")
    actualized_as: Dict  # What it became (codes, territories, intensities, becomings)


def actualize_virtual_capacity(
    assemblage: Assemblage,
    virtual_capacity: str,
    trigger_description: str
) -> Assemblage:
    """
    Actualize a virtual capacity in an assemblage.
    
    Virtual → Actual transformation:
    - Virtual: "Coursera subscription (unused)"
    - Trigger: "Decided to learn Python"
    - Actual: Code("Sunday learning ritual"), Intensity(focus: +0.3), Becoming("becoming-programmer")
    """
    
    after = deepcopy(assemblage)
    
    # Remove from virtual
    if virtual_capacity in after.virtual_capacities:
        after.virtual_capacities.remove(virtual_capacity)
    
    # Examples of actualization patterns
    # (In full implementation, this would be LLM-powered)
    
    if "coursera" in virtual_capacity.lower() or "learning" in virtual_capacity.lower():
        # Actualize as learning practice
        after.codes.append(Code(
            name="Weekly learning ritual",
            content=trigger_description,
            type="habit",
            level="molar"
        ))
        after.intensity_field["focus"] = after.intensity_field.get("focus", 0.5) + 0.2
        after.becoming_vectors.append("becoming-expert")
        
    elif "gym" in virtual_capacity.lower() or "fitness" in virtual_capacity.lower():
        # Actualize as physical practice
        after.codes.append(Code(
            name="Gym routine",
            content=trigger_description,
            type="habit",
            level="molar"
        ))
        after.territories.append(Territory(
            name="Gym",
            function="Physical training",
            quality="Disciplined",
            space_type="striated"
        ))
        after.intensity_field["energy"] = after.intensity_field.get("energy", 0.5) + 0.3
        after.becoming_vectors.append("becoming-stronger")
        
    elif "amazon" in virtual_capacity.lower():
        # Actualize as consumption pattern
        after.codes.append(Code(
            name="Online shopping habit",
            content=trigger_description,
            type="habit",
            level="molar"
        ))
        after.becoming_vectors.append("becoming-consumer")
        after.stratification_depth += 0.1  # More rigid/dependent
        
    return after


def suggest_actualization_candidates(assemblage: Assemblage) -> List[str]:
    """
    Identify virtual capacities that are ready to actualize.
    (In full implementation, this would analyze current context)
    """
    return assemblage.virtual_capacities


# =============================================================================
# EXAMPLE
# =============================================================================

if __name__ == "__main__":
    # Create assemblage with virtual capacities
    from carry.simulation.assemblage import generate_assemblages_for_subject
    
    print("Virtual capacities represent REAL but unactualized potentials.")
    print("Examples:")
    print("- Coursera subscription you haven't used")
    print("- Gym membership gathering dust")  
    print("- Library card never swiped")
    print("- Python installed but never coded")
    print("\nThey actualize when you START USING them.\n")
