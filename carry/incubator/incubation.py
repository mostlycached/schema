"""
Incubation Module: Core Incubation Analysis

Analyzes clusters for:
1. Transversal lines (alliances/oppositions across assemblages)
2. Collective tensions
3. Virtual capacity actualization potential
4. Fertility assessment
"""

import os
from dataclasses import dataclass, field
from typing import List, Dict, Optional, TYPE_CHECKING
from collections import defaultdict

import google.generativeai as genai
from dotenv import load_dotenv

from carry.incubator.proximity import ProximityMatrix, INTENSITY_DIMENSIONS
from carry.incubator.cluster import IncubationCluster
from carry.engine.interaction import (
    Assemblage,
    describe_assemblage,
    compute_intensity_relations,
    RelationType
)

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class TransversalLine:
    """A line of connection spanning multiple assemblages."""
    line_type: str  # "alliance", "opposition", "resonance"
    dimension: str  # What dimension this spans
    participating_assemblages: List[str]
    strength: float  # 0.0 to 1.0
    description: str


@dataclass
class CollectiveTension:
    """Tension arising from the collective incubation."""
    tension_type: str  # "intensity_clash", "space_incompatibility", "code_conflict"
    sources: List[str]  # Assemblage names involved
    severity: float  # 0.0 to 1.0
    description: str
    potential_resolution: str = ""


@dataclass
class ActualizationPotential:
    """Virtual capacity that could be actualized through incubation."""
    virtual_capacity_name: str
    source_assemblage: str
    trigger_assemblages: List[str]
    actualization_probability: float
    explanation: str


@dataclass
class FertilityAssessment:
    """Whether this incubation can give birth to a new assemblage."""
    is_fertile: bool
    fertility_score: float  # 0.0 to 1.0

    # Factors
    creative_tension_level: float
    resonance_foundation: float
    virtual_capacity_triggers: int

    # Emergence type if fertile
    emergence_type: str = ""  # "synthesis", "mutation", "transcendence", "hybrid"
    emergence_description: str = ""


@dataclass
class IncubationResult:
    """Full result of incubating a cluster of assemblages."""
    cluster: IncubationCluster

    transversal_lines: List[TransversalLine] = field(default_factory=list)
    collective_tensions: List[CollectiveTension] = field(default_factory=list)
    actualization_potentials: List[ActualizationPotential] = field(default_factory=list)

    fertility_assessment: Optional[FertilityAssessment] = None

    # Populated by emergence.py if fertile
    emerged_assemblage: Optional[Assemblage] = None


# =============================================================================
# TRANSVERSAL LINES
# =============================================================================

def detect_transversal_lines(
    cluster: IncubationCluster,
    proximity_matrix: ProximityMatrix
) -> List[TransversalLine]:
    """
    Detect lines of alliance/opposition that span multiple assemblages.
    """
    lines = []
    assemblages = cluster.assemblages
    n = len(assemblages)

    # 1. Intensity alliances: 3+ assemblages with similar values on same dimension
    for dim in INTENSITY_DIMENSIONS:
        values = [(a.name, a.intensity_field.get(dim, 0.5)) for a in assemblages]

        # Find high-value alliance (>= 0.7)
        high_group = [name for name, val in values if val >= 0.7]
        if len(high_group) >= 2:
            avg_val = sum(v for _, v in values if _ in high_group) / len(high_group)
            lines.append(TransversalLine(
                line_type="alliance",
                dimension=f"intensity:{dim}",
                participating_assemblages=high_group,
                strength=avg_val,
                description=f"High {dim} alliance ({avg_val:.2f})"
            ))

        # Find low-value alliance (<= 0.3)
        low_group = [name for name, val in values if val <= 0.3]
        if len(low_group) >= 2:
            avg_val = 1.0 - (sum(v for _, v in values if _ in low_group) / len(low_group))
            lines.append(TransversalLine(
                line_type="alliance",
                dimension=f"intensity:{dim}",
                participating_assemblages=low_group,
                strength=avg_val,
                description=f"Low {dim} alliance (shared restraint)"
            ))

        # Find opposition (high vs low)
        if high_group and low_group:
            lines.append(TransversalLine(
                line_type="opposition",
                dimension=f"intensity:{dim}",
                participating_assemblages=high_group + low_group,
                strength=0.8,
                description=f"{dim} opposition: {high_group} vs {low_group}"
            ))

    # 2. Becoming resonances: shared becoming vectors across 3+ assemblages
    becoming_map = defaultdict(list)
    for asm in assemblages:
        for bv in asm.becoming_vectors:
            becoming_map[bv].append(asm.name)

    for bv, names in becoming_map.items():
        if len(names) >= 2:
            lines.append(TransversalLine(
                line_type="resonance",
                dimension=f"becoming:{bv}",
                participating_assemblages=names,
                strength=len(names) / n,
                description=f"Shared {bv}"
            ))

    # 3. Space type alliances
    smooth_group = [a.name for a in assemblages
                   if sum(1 for t in a.territories if t.space_type == "smooth") >
                      sum(1 for t in a.territories if t.space_type == "striated")]
    striated_group = [a.name for a in assemblages
                     if sum(1 for t in a.territories if t.space_type == "striated") >
                        sum(1 for t in a.territories if t.space_type == "smooth")]

    if len(smooth_group) >= 2:
        lines.append(TransversalLine(
            line_type="alliance",
            dimension="space:smooth",
            participating_assemblages=smooth_group,
            strength=0.7,
            description="Smooth space alliance (nomadic, open)"
        ))

    if len(striated_group) >= 2:
        lines.append(TransversalLine(
            line_type="alliance",
            dimension="space:striated",
            participating_assemblages=striated_group,
            strength=0.7,
            description="Striated space alliance (organized, controlled)"
        ))

    if smooth_group and striated_group:
        lines.append(TransversalLine(
            line_type="opposition",
            dimension="space:type",
            participating_assemblages=smooth_group + striated_group,
            strength=0.6,
            description=f"Space type tension: smooth ({smooth_group}) vs striated ({striated_group})"
        ))

    return lines


# =============================================================================
# COLLECTIVE TENSIONS
# =============================================================================

def analyze_collective_tensions(
    cluster: IncubationCluster,
    model_name: str = "gemini-2.0-flash"
) -> List[CollectiveTension]:
    """
    Analyze tensions arising from bringing these assemblages together.
    """
    tensions = []
    assemblages = cluster.assemblages

    # 1. Intensity clashes
    for dim in INTENSITY_DIMENSIONS:
        values = [a.intensity_field.get(dim, 0.5) for a in assemblages]
        max_val = max(values)
        min_val = min(values)
        spread = max_val - min_val

        if spread > 0.5:
            high_asm = [a.name for a in assemblages
                       if a.intensity_field.get(dim, 0.5) >= max_val - 0.1]
            low_asm = [a.name for a in assemblages
                      if a.intensity_field.get(dim, 0.5) <= min_val + 0.1]

            tensions.append(CollectiveTension(
                tension_type="intensity_clash",
                sources=high_asm + low_asm,
                severity=min(1.0, spread * 1.2),
                description=f"{dim} clash: {high_asm} (high) vs {low_asm} (low)",
                potential_resolution=f"May resolve through {dim} modulation or specialization"
            ))

    # 2. Space incompatibility
    smooth_terrs = sum(sum(1 for t in a.territories if t.space_type == "smooth")
                       for a in assemblages)
    striated_terrs = sum(sum(1 for t in a.territories if t.space_type == "striated")
                         for a in assemblages)

    if smooth_terrs > 0 and striated_terrs > 0:
        ratio = min(smooth_terrs, striated_terrs) / max(smooth_terrs, striated_terrs)
        if ratio > 0.3:  # Significant mix
            tensions.append(CollectiveTension(
                tension_type="space_incompatibility",
                sources=[a.name for a in assemblages],
                severity=ratio * 0.7,
                description=f"Space type tension: {smooth_terrs} smooth vs {striated_terrs} striated territories",
                potential_resolution="May create hybrid spaces or territorial negotiation"
            ))

    # 3. Code conflicts (molar vs molecular)
    molar_codes = []
    molecular_codes = []
    for asm in assemblages:
        for code in asm.codes:
            if code.level == "molar":
                molar_codes.append((asm.name, code.name, code.content))
            else:
                molecular_codes.append((asm.name, code.name, code.content))

    # LLM-enhanced code conflict detection
    if molar_codes and molecular_codes and len(assemblages) <= 6:
        model = genai.GenerativeModel(model_name)

        prompt = f"""Analyze potential CODE CONFLICTS in this assemblage cluster.

MOLAR CODES (visible habits, social rules):
{chr(10).join(f'- {name}: {code} - "{content}"' for name, code, content in molar_codes[:10])}

MOLECULAR CODES (micro-level, subliminal):
{chr(10).join(f'- {name}: {code} - "{content}"' for name, code, content in molecular_codes[:10])}

Identify 1-3 significant conflicts where codes might clash.
For each, rate severity (0.0-1.0) and suggest resolution.

Format as JSON list:
[{{"conflict": "description", "severity": 0.5, "resolution": "how it might resolve"}}]
"""
        try:
            response = model.generate_content(prompt)
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            import json
            conflicts = json.loads(text)

            for c in conflicts[:3]:
                tensions.append(CollectiveTension(
                    tension_type="code_conflict",
                    sources=[asm.name for asm in assemblages],
                    severity=float(c.get("severity", 0.5)),
                    description=c.get("conflict", "Code conflict"),
                    potential_resolution=c.get("resolution", "")
                ))
        except Exception as e:
            print(f"Warning: LLM code conflict analysis failed: {e}")

    return tensions


# =============================================================================
# ACTUALIZATION POTENTIALS
# =============================================================================

def identify_actualization_potentials(
    cluster: IncubationCluster,
    model_name: str = "gemini-2.0-flash"
) -> List[ActualizationPotential]:
    """
    Find virtual capacities that could be actualized by this incubation.
    """
    potentials = []
    assemblages = cluster.assemblages

    for asm in assemblages:
        for vc in asm.virtual_capacities:
            # Check if other assemblages might provide the trigger
            trigger_candidates = []

            for other in assemblages:
                if other.name == asm.name:
                    continue

                # Check intensity alignment
                intensity_match = sum(
                    1 for dim in INTENSITY_DIMENSIONS
                    if abs(asm.intensity_field.get(dim, 0.5) -
                          other.intensity_field.get(dim, 0.5)) < 0.2
                ) / len(INTENSITY_DIMENSIONS)

                # Check becoming vector resonance
                shared_becomings = set(asm.becoming_vectors) & set(other.becoming_vectors)

                # Check component capacity overlap
                asm_caps = {c.capacity.lower() for c in asm.components}
                other_caps = {c.capacity.lower() for c in other.components}

                if intensity_match > 0.5 or shared_becomings or (asm_caps & other_caps):
                    trigger_candidates.append(other.name)

            if trigger_candidates:
                # Estimate probability
                prob = min(1.0, len(trigger_candidates) / (len(assemblages) - 1) + 0.2)

                potentials.append(ActualizationPotential(
                    virtual_capacity_name=vc.name,
                    source_assemblage=asm.name,
                    trigger_assemblages=trigger_candidates,
                    actualization_probability=prob,
                    explanation=f"{vc.reason_unactualized} - may be triggered by {trigger_candidates}"
                ))

    return potentials


# =============================================================================
# FERTILITY ASSESSMENT
# =============================================================================

def assess_fertility(
    cluster: IncubationCluster,
    transversal_lines: List[TransversalLine],
    collective_tensions: List[CollectiveTension],
    actualization_potentials: List[ActualizationPotential],
    model_name: str = "gemini-2.0-flash"
) -> FertilityAssessment:
    """
    Determine if this incubation can give birth to a new assemblage.

    Fertility requires the Goldilocks zone:
    - Creative tension: 0.3 < level < 0.7 (too low = stasis, too high = destruction)
    - Resonance foundation: > 0.4 (enough alliance to build on)
    - At least 1 virtual capacity trigger
    """
    # 1. Creative tension level
    if not collective_tensions:
        tension_level = 0.1 + cluster.tension_potential * 0.3
    else:
        tension_level = sum(t.severity for t in collective_tensions) / len(collective_tensions)

    # Boost for irreconcilable tensions
    irreconcilable = [t for t in collective_tensions if t.severity > 0.8]
    if irreconcilable:
        tension_level = min(1.0, tension_level + 0.15)

    # 2. Resonance foundation
    alliances = [l for l in transversal_lines if l.line_type in ("alliance", "resonance")]
    if not transversal_lines:
        resonance_score = cluster.internal_cohesion
    else:
        resonance_score = sum(l.strength for l in alliances) / len(transversal_lines)

    # 3. Virtual capacity triggers
    high_prob_triggers = [ap for ap in actualization_potentials if ap.actualization_probability > 0.5]
    trigger_count = len(high_prob_triggers)

    # 4. Fertility assessment
    is_fertile = (
        0.25 <= tension_level <= 0.75 and
        resonance_score > 0.35 and
        (trigger_count >= 1 or len(cluster.shared_becomings) >= 2)
    )

    fertility_score = 0.0
    if is_fertile:
        tension_ideal = 1.0 - abs(0.5 - tension_level) * 2
        fertility_score = (
            tension_ideal * 0.4 +
            resonance_score * 0.4 +
            min(trigger_count, 3) / 3 * 0.2
        )

    # 5. Determine emergence type
    emergence_type = ""
    if is_fertile:
        if cluster.diversity_score > 0.6:
            emergence_type = "transcendence"
        elif cluster.internal_cohesion > 0.7:
            emergence_type = "synthesis"
        elif trigger_count >= 2:
            emergence_type = "mutation"
        else:
            emergence_type = "hybrid"

    # 6. LLM description of emergence
    emergence_description = ""
    if is_fertile:
        model = genai.GenerativeModel(model_name)

        prompt = f"""This assemblage cluster is FERTILE and ready to give birth to a new assemblage.

CLUSTER MEMBERS:
{chr(10).join(f'- {a.name}: "{a.abstract_machine}"' for a in cluster.assemblages)}

SHARED BECOMINGS: {cluster.shared_becomings}
EMERGENCE TYPE: {emergence_type}

In 2-3 sentences, describe what kind of new assemblage could emerge from this incubation.
Focus on the abstract machine (the formula/diagram) of what could emerge.
"""
        try:
            response = model.generate_content(prompt)
            emergence_description = response.text.strip()
        except Exception as e:
            emergence_description = f"Emergence type: {emergence_type}"

    return FertilityAssessment(
        is_fertile=is_fertile,
        fertility_score=fertility_score,
        creative_tension_level=tension_level,
        resonance_foundation=resonance_score,
        virtual_capacity_triggers=trigger_count,
        emergence_type=emergence_type,
        emergence_description=emergence_description
    )


# =============================================================================
# MAIN INCUBATION FUNCTION
# =============================================================================

def incubate(
    cluster: IncubationCluster,
    proximity_matrix: ProximityMatrix,
    generate_emergence: bool = True,
    model_name: str = "gemini-2.0-flash"
) -> IncubationResult:
    """
    Full incubation process for a cluster of assemblages.
    """
    print(f"Incubating cluster {cluster.cluster_id} with {len(cluster.assemblages)} assemblages...")

    # 1. Detect transversal lines
    transversal_lines = detect_transversal_lines(cluster, proximity_matrix)
    print(f"  Found {len(transversal_lines)} transversal lines")

    # 2. Analyze collective tensions
    collective_tensions = analyze_collective_tensions(cluster, model_name)
    print(f"  Found {len(collective_tensions)} collective tensions")

    # 3. Identify actualization potentials
    actualization_potentials = identify_actualization_potentials(cluster, model_name)
    print(f"  Found {len(actualization_potentials)} actualization potentials")

    # 4. Assess fertility
    fertility = assess_fertility(
        cluster,
        transversal_lines,
        collective_tensions,
        actualization_potentials,
        model_name
    )
    print(f"  Fertile: {fertility.is_fertile} (score: {fertility.fertility_score:.3f})")

    result = IncubationResult(
        cluster=cluster,
        transversal_lines=transversal_lines,
        collective_tensions=collective_tensions,
        actualization_potentials=actualization_potentials,
        fertility_assessment=fertility
    )

    # 5. Generate emergence if fertile
    if fertility.is_fertile and generate_emergence:
        # Import here to avoid circular dependency
        from carry.incubator.emergence import generate_emerged_assemblage
        emergence_result = generate_emerged_assemblage(
            cluster,
            fertility,
            transversal_lines,
            actualization_potentials,
            model_name
        )
        result.emerged_assemblage = emergence_result.emerged_assemblage
        print(f"  Generated emerged assemblage: {emergence_result.emerged_assemblage.name}")

    return result


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    from pathlib import Path
    from carry.engine.interaction import load_assemblages
    from carry.incubator.proximity import build_proximity_matrix
    from carry.incubator.cluster import cluster_by_proximity

    carry_root = Path(__file__).parent.parent
    subjects_path = carry_root / "assemblages" / "subjects" / "hari.yaml"

    print("Loading subject assemblages...")
    subjects = load_assemblages(subjects_path)
    print(f"Loaded {len(subjects)} assemblages")

    if len(subjects) >= 3:
        print("\nBuilding proximity matrix...")
        matrix = build_proximity_matrix(subjects, use_llm_semantics=False)

        print("\nClustering...")
        clustering = cluster_by_proximity(subjects, matrix, threshold=0.4, min_cluster_size=2)

        if clustering.clusters:
            cluster = clustering.clusters[0]
            print(f"\nIncubating cluster with: {[a.name for a in cluster.assemblages]}")

            result = incubate(cluster, matrix, generate_emergence=False)

            print(f"\nTransversal Lines:")
            for line in result.transversal_lines[:5]:
                print(f"  - {line.line_type}: {line.dimension} ({line.strength:.2f})")

            print(f"\nCollective Tensions:")
            for t in result.collective_tensions[:3]:
                print(f"  - {t.tension_type}: {t.description} ({t.severity:.2f})")

            print(f"\nFertility Assessment:")
            print(f"  Is Fertile: {result.fertility_assessment.is_fertile}")
            print(f"  Tension Level: {result.fertility_assessment.creative_tension_level:.2f}")
            print(f"  Resonance: {result.fertility_assessment.resonance_foundation:.2f}")
