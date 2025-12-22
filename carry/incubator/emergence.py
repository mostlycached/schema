"""
Emergence Module: Generate New Assemblages from Fertile Incubation

Creates hybrid/transcendent assemblages when incubation is fertile.
"""

import os
import json
import yaml
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional

import google.generativeai as genai
from dotenv import load_dotenv

from carry.incubator.cluster import IncubationCluster
from carry.incubator.incubation import (
    TransversalLine,
    ActualizationPotential,
    FertilityAssessment
)
from carry.engine.interaction import (
    Assemblage,
    Territory,
    Code,
    Component,
    VirtualCapacity,
    describe_assemblage
)

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class EmergenceGenesis:
    """Describes how the new assemblage emerged."""
    parent_assemblages: List[str]
    territories_inherited: Dict[str, str] = field(default_factory=dict)
    territories_mutated: List[str] = field(default_factory=list)
    codes_synthesized: List[str] = field(default_factory=list)
    components_hybrid: List[str] = field(default_factory=list)

    # The creative act
    abstract_machine_emergence: str = ""
    becoming_vectors_novel: List[str] = field(default_factory=list)


@dataclass
class EmergenceResult:
    """Result of generating a new assemblage from fertile incubation."""
    emerged_assemblage: Assemblage
    genesis: EmergenceGenesis

    coherence_score: float = 0.0
    viability_assessment: str = ""


# =============================================================================
# ASSEMBLAGE GENERATION
# =============================================================================

def format_assemblages_for_prompt(assemblages: List[Assemblage]) -> str:
    """Format assemblages for LLM prompt."""
    lines = []
    for asm in assemblages:
        lines.append(f"### {asm.name}")
        lines.append(f'Abstract Machine: "{asm.abstract_machine}"')
        lines.append(f"Territories: {[t.name for t in asm.territories]}")
        lines.append(f"Codes: {[c.name for c in asm.codes]}")
        lines.append(f"Components: {[c.name for c in asm.components]}")
        lines.append(f"Intensity Field: {asm.intensity_field}")
        lines.append(f"Becoming Vectors: {asm.becoming_vectors}")
        if asm.virtual_capacities:
            lines.append(f"Virtual Capacities: {[vc.name for vc in asm.virtual_capacities]}")
        lines.append("")
    return "\n".join(lines)


def format_transversal_lines(lines: List[TransversalLine]) -> str:
    """Format transversal lines for LLM prompt."""
    if not lines:
        return "None detected"

    result = []
    for line in lines:
        result.append(f"- {line.line_type.upper()} on {line.dimension}")
        result.append(f"  Participants: {line.participating_assemblages}")
        result.append(f"  Strength: {line.strength:.2f}")
        result.append(f"  {line.description}")
    return "\n".join(result)


def format_actualization_potentials(potentials: List[ActualizationPotential]) -> str:
    """Format actualization potentials for LLM prompt."""
    if not potentials:
        return "None detected"

    result = []
    for ap in potentials:
        result.append(f"- {ap.virtual_capacity_name} (from {ap.source_assemblage})")
        result.append(f"  Triggers: {ap.trigger_assemblages}")
        result.append(f"  Probability: {ap.actualization_probability:.2f}")
    return "\n".join(result)


def parse_assemblage_yaml(text: str) -> Optional[Assemblage]:
    """Parse YAML output from LLM into Assemblage."""
    try:
        # Clean up text
        if "```yaml" in text:
            text = text.split("```yaml")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]

        data = yaml.safe_load(text)

        if not data:
            return None

        territories = [Territory(**t) for t in data.get('territories', [])]
        codes = [Code(**c) for c in data.get('codes', [])]
        components = [Component(**c) for c in data.get('components', [])]

        virtual_caps = []
        for vc in data.get('virtual_capacities', []):
            if isinstance(vc, dict):
                virtual_caps.append(VirtualCapacity(**vc))
            elif isinstance(vc, str):
                virtual_caps.append(VirtualCapacity(
                    name=vc,
                    access_point="",
                    reason_unactualized=""
                ))

        return Assemblage(
            name=data.get('name', 'Emerged-Assemblage'),
            abstract_machine=data.get('abstract_machine', ''),
            entity_type=data.get('entity_type', 'emerged'),
            territories=territories,
            codes=codes,
            components=components,
            intensity_field=data.get('intensity_field', {}),
            becoming_vectors=data.get('becoming_vectors', []),
            stratification_depth=data.get('stratification_depth', 0.5),
            virtual_capacities=virtual_caps
        )

    except Exception as e:
        print(f"Warning: Failed to parse assemblage YAML: {e}")
        return None


def generate_emerged_assemblage(
    cluster: IncubationCluster,
    fertility: FertilityAssessment,
    transversal_lines: List[TransversalLine],
    actualization_potentials: List[ActualizationPotential],
    model_name: str = "gemini-2.0-flash"
) -> EmergenceResult:
    """
    Generate a new hybrid assemblage from fertile incubation.
    """
    model = genai.GenerativeModel(model_name)

    emergence_guidance = {
        "synthesis": "Synthesize the parent assemblages into a coherent new form that preserves the best of each while creating something unified.",
        "mutation": "Create a radically transformed form where one assemblage mutates dramatically under pressure from the others.",
        "transcendence": "Transcend all parent assemblages with a genuinely new abstract machine that goes beyond any of them individually.",
        "hybrid": "Mix and match components from parents into a viable hybrid that combines their capacities."
    }

    prompt = f"""You are a Deleuzian ontologist facilitating the EMERGENCE of a new assemblage.

PARENT ASSEMBLAGES IN INCUBATION CHAMBER:
{format_assemblages_for_prompt(cluster.assemblages)}

TRANSVERSAL LINES (alliances/oppositions spanning these assemblages):
{format_transversal_lines(transversal_lines)}

VIRTUAL CAPACITIES READY TO ACTUALIZE:
{format_actualization_potentials(actualization_potentials)}

FERTILITY ASSESSMENT:
- Type: {fertility.emergence_type}
- Creative Tension Level: {fertility.creative_tension_level:.2f}
- Resonance Foundation: {fertility.resonance_foundation:.2f}
- Shared Becomings: {cluster.shared_becomings}

---

Generate a NEW ASSEMBLAGE that EMERGES from this incubation.

EMERGENCE TYPE: {fertility.emergence_type}
{emergence_guidance.get(fertility.emergence_type, '')}

Requirements:
1. The abstract_machine MUST be genuinely novel, not just a combination of words from parents
2. Create 2-3 NEW territories that reflect the new logic (can inherit/transform from parents)
3. Create 2-3 codes that govern this new assemblage
4. Include at least 1 actualized virtual capacity as a new component
5. Becoming vectors should include at least 1 genuinely novel vector not in any parent
6. Intensity field should reflect the synthesis/tension resolution of parents
7. Give it a meaningful hyphenated name ending in "-Assemblage"

Output ONLY valid YAML with this exact structure:
```yaml
name: [Name]-Assemblage
abstract_machine: "The driving formula of this new assemblage"
entity_type: emerged
territories:
  - name: "Territory Name"
    function: "What happens here"
    quality: "single-word"
    space_type: "smooth" # or "striated"
codes:
  - name: "Code Name"
    content: "What the code prescribes"
    type: "habit" # or "social_rule", "biological_rhythm"
    level: "molar" # or "molecular"
components:
  - name: "Component Name"
    type: "organic" # or "technical", "sign"
    capacity: "What it can do"
intensity_field:
  focus: 0.0
  patience: 0.0
  abstraction: 0.0
  speed: 0.0
  tactility: 0.0
  social: 0.0
becoming_vectors:
  - "becoming-something"
stratification_depth: 0.5
virtual_capacities:
  - name: "Remaining virtual capacity"
    access_point: "What enables it"
    reason_unactualized: "Why it hasn't happened yet"
```
"""

    try:
        response = model.generate_content(prompt)
        emerged = parse_assemblage_yaml(response.text)

        if not emerged:
            # Fallback: create minimal emerged assemblage
            emerged = Assemblage(
                name=f"{cluster.assemblages[0].name.split('-')[0]}-Emerged-Assemblage",
                abstract_machine=fertility.emergence_description or "Emergent synthesis",
                entity_type="emerged",
                territories=[Territory(
                    name="Incubation-Ground",
                    function="Where emergence happened",
                    quality="liminal",
                    space_type="smooth"
                )],
                codes=[Code(
                    name="Emergence-Code",
                    content="Integrate through tension",
                    type="habit",
                    level="molar"
                )],
                components=[Component(
                    name="Hybrid-Core",
                    type="sign",
                    capacity="Synthesize parent capacities"
                )],
                intensity_field=cluster.centroid_intensities,
                becoming_vectors=cluster.shared_becomings + ["becoming-emergent"],
                stratification_depth=0.4,
                virtual_capacities=[]
            )

    except Exception as e:
        print(f"Warning: LLM emergence generation failed: {e}")
        emerged = Assemblage(
            name="Failed-Emergence-Assemblage",
            abstract_machine="Emergence failed",
            entity_type="emerged"
        )

    # Trace genesis
    genesis = trace_genesis(emerged, cluster.assemblages)

    # Validate emergence
    coherence, viability = validate_emergence(emerged, cluster.assemblages, model_name)

    return EmergenceResult(
        emerged_assemblage=emerged,
        genesis=genesis,
        coherence_score=coherence,
        viability_assessment=viability
    )


# =============================================================================
# VALIDATION
# =============================================================================

def validate_emergence(
    emerged: Assemblage,
    parents: List[Assemblage],
    model_name: str = "gemini-2.0-flash"
) -> Tuple[float, str]:
    """
    Validate the coherence and viability of an emerged assemblage.
    """
    # Basic structural validation
    structural_score = 0.0

    if emerged.abstract_machine and len(emerged.abstract_machine) > 10:
        structural_score += 0.2
    if len(emerged.territories) >= 2:
        structural_score += 0.2
    if len(emerged.codes) >= 2:
        structural_score += 0.2
    if len(emerged.components) >= 2:
        structural_score += 0.2
    if emerged.becoming_vectors:
        structural_score += 0.2

    # LLM coherence check
    model = genai.GenerativeModel(model_name)

    prompt = f"""Assess the COHERENCE and VIABILITY of this emerged assemblage.

EMERGED ASSEMBLAGE:
Name: {emerged.name}
Abstract Machine: "{emerged.abstract_machine}"
Territories: {[t.name for t in emerged.territories]}
Codes: {[c.name for c in emerged.codes]}
Components: {[c.name for c in emerged.components]}
Becoming Vectors: {emerged.becoming_vectors}

PARENT ASSEMBLAGES IT EMERGED FROM:
{', '.join(p.name for p in parents)}

Questions:
1. Is the abstract_machine coherent with the territories, codes, and components?
2. Does this assemblage make sense as an emergence from the parents?
3. Could this assemblage actually persist and function?

Provide a coherence score (0.0-1.0) and a brief viability assessment.

Format:
SCORE: [0.0-1.0]
VIABILITY: [1-2 sentences]
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()

        # Parse score
        llm_score = 0.5
        if "SCORE:" in text:
            score_line = [l for l in text.split("\n") if "SCORE:" in l][0]
            score_str = score_line.split("SCORE:")[1].strip()
            llm_score = float(score_str.split()[0])
            llm_score = max(0.0, min(1.0, llm_score))

        # Parse viability
        viability = ""
        if "VIABILITY:" in text:
            viability = text.split("VIABILITY:")[1].strip()

        coherence = (structural_score + llm_score) / 2
        return (coherence, viability)

    except Exception as e:
        print(f"Warning: Validation failed: {e}")
        return (structural_score, "Validation incomplete")


def trace_genesis(
    emerged: Assemblage,
    parents: List[Assemblage]
) -> EmergenceGenesis:
    """
    Trace which elements of the emerged assemblage came from which parents.
    """
    genesis = EmergenceGenesis(
        parent_assemblages=[p.name for p in parents]
    )

    # Trace territories
    parent_territory_names = {}
    for p in parents:
        for t in p.territories:
            parent_territory_names[t.name.lower()] = p.name

    for t in emerged.territories:
        t_lower = t.name.lower()
        if t_lower in parent_territory_names:
            genesis.territories_inherited[t.name] = parent_territory_names[t_lower]
        else:
            # Check for partial matches
            matched = False
            for pt_name, p_name in parent_territory_names.items():
                if pt_name in t_lower or t_lower in pt_name:
                    genesis.territories_inherited[t.name] = f"{p_name} (mutated)"
                    matched = True
                    break
            if not matched:
                genesis.territories_mutated.append(t.name)

    # Trace codes
    parent_code_names = set()
    for p in parents:
        for c in p.codes:
            parent_code_names.add(c.name.lower())

    for c in emerged.codes:
        if c.name.lower() not in parent_code_names:
            genesis.codes_synthesized.append(c.name)

    # Trace components
    parent_component_names = set()
    for p in parents:
        for c in p.components:
            parent_component_names.add(c.name.lower())

    for c in emerged.components:
        if c.name.lower() not in parent_component_names:
            genesis.components_hybrid.append(c.name)

    # Trace novel becoming vectors
    parent_becomings = set()
    for p in parents:
        parent_becomings.update(p.becoming_vectors)

    genesis.becoming_vectors_novel = [
        bv for bv in emerged.becoming_vectors
        if bv not in parent_becomings
    ]

    # Abstract machine emergence
    genesis.abstract_machine_emergence = emerged.abstract_machine

    return genesis


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    from pathlib import Path
    from carry.engine.interaction import load_assemblages
    from carry.incubator.proximity import build_proximity_matrix
    from carry.incubator.cluster import cluster_by_proximity, IncubationCluster
    from carry.incubator.incubation import (
        detect_transversal_lines,
        identify_actualization_potentials,
        assess_fertility
    )

    carry_root = Path(__file__).parent.parent
    subjects_path = carry_root / "assemblages" / "subjects" / "hari.yaml"

    print("Loading subject assemblages...")
    subjects = load_assemblages(subjects_path)
    print(f"Loaded {len(subjects)} assemblages")

    if len(subjects) >= 3:
        # Take first 3 as a test cluster
        test_assemblages = subjects[:3]

        print(f"\nTest cluster: {[a.name for a in test_assemblages]}")

        # Build matrix for the subset
        matrix = build_proximity_matrix(test_assemblages, use_llm_semantics=False)

        # Create cluster
        cluster = IncubationCluster(
            cluster_id=0,
            assemblages=test_assemblages,
            centroid_intensities={dim: 0.5 for dim in ['focus', 'patience', 'abstraction', 'speed', 'tactility', 'social']}
        )

        # Detect lines and potentials
        lines = detect_transversal_lines(cluster, matrix)
        potentials = identify_actualization_potentials(cluster)

        # Force fertility for testing
        fertility = FertilityAssessment(
            is_fertile=True,
            fertility_score=0.7,
            creative_tension_level=0.5,
            resonance_foundation=0.6,
            virtual_capacity_triggers=1,
            emergence_type="synthesis",
            emergence_description="Test synthesis"
        )

        print("\nGenerating emerged assemblage...")
        result = generate_emerged_assemblage(cluster, fertility, lines, potentials)

        print(f"\nEmerged: {result.emerged_assemblage.name}")
        print(f"Abstract Machine: {result.emerged_assemblage.abstract_machine}")
        print(f"Coherence Score: {result.coherence_score:.2f}")
        print(f"Viability: {result.viability_assessment}")

        print(f"\nGenesis:")
        print(f"  Parent assemblages: {result.genesis.parent_assemblages}")
        print(f"  Territories inherited: {result.genesis.territories_inherited}")
        print(f"  Territories mutated: {result.genesis.territories_mutated}")
        print(f"  Novel becomings: {result.genesis.becoming_vectors_novel}")
