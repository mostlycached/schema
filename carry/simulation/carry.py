"""
Carry Module: Bare Objects for Assemblage Injection

This module provides MINIMAL object definitions. Following Deleuze/Guattari:
- Assemblages are defined by RELATIONS, not properties
- Elements retain autonomy and can be inserted into different assemblages
- Meaning/effect emerges from the ENCOUNTER, not from the object itself

A carry object is just: a name and physical facts. Nothing more.
No animism, no modifications, no prescribed meaning.
"""

from dataclasses import dataclass

@dataclass
class BareObject:
    """
    A bare object for assemblage injection.
    
    No prescribed meaning. No pre-assigned effects.
    Just physical facts. The rest emerges from encounter.
    """
    name: str  # "Walking cane", "Smartphone", "A theorem"
    
    # Physical facts only — what it IS, not what it DOES
    material: str = ""  # "wood", "metal", "abstract"
    form: str = ""  # "rod", "rectangle", "concept"
    weight: str = ""  # "light", "heavy", "weightless"
    
    # How it persists in the assemblage
    persistence: str = ""  # "worn", "pocketed", "environmental", "mental"
    
    # Origin — how it entered, not what it means
    origin: str = ""  # "found", "given", "purchased", "emerged"


# =============================================================================
# BARE OBJECT CATALOG
# =============================================================================

BARE_OBJECTS = {
    "cane": BareObject(
        name="Walking cane",
        material="wood",
        form="rod, handled",
        weight="light",
        persistence="carried",
        origin="found",
    ),
    
    "smartphone": BareObject(
        name="Smartphone",
        material="glass and metal",
        form="thin rectangle",
        weight="light",
        persistence="pocketed",
        origin="purchased",
    ),
    
    "ring": BareObject(
        name="Ring",
        material="metal",
        form="band",
        weight="negligible",
        persistence="worn",
        origin="given",
    ),
    
    "notebook": BareObject(
        name="Notebook",
        material="paper",
        form="bound pages",
        weight="light",
        persistence="carried",
        origin="purchased",
    ),
    
    "concept": BareObject(
        name="A philosophical concept",
        material="abstract",
        form="proposition",
        weight="weightless",
        persistence="mental",
        origin="encountered",
    ),
    
    "diagnosis": BareObject(
        name="A diagnosis",
        material="abstract",
        form="category",
        weight="weightless",
        persistence="mental",
        origin="received",
    ),
    
    "keys": BareObject(
        name="Set of keys",
        material="metal",
        form="irregular cluster",
        weight="light",
        persistence="pocketed",
        origin="accumulated",
    ),
    
    "glasses": BareObject(
        name="Eyeglasses",
        material="glass and metal",
        form="lens frames",
        weight="light",
        persistence="worn",
        origin="prescribed",
    ),
}


def get_bare_object(key: str) -> BareObject:
    """Retrieve a bare object by key."""
    if key not in BARE_OBJECTS:
        available = ", ".join(BARE_OBJECTS.keys())
        raise ValueError(f"Unknown object: {key}. Available: {available}")
    return BARE_OBJECTS[key]
