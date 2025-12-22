"""
Proximity Module: Multi-Dimensional Assemblage Proximity Computation

Computes closeness between assemblages using:
1. Intensity field distance (Euclidean in 6D)
2. Space type compatibility (smooth vs striated)
3. Semantic similarity of component capacities (LLM, cached)
4. Becoming vector overlap (Jaccard + semantic boost)
"""

import os
from math import sqrt
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from enum import Enum

# Optional LLM support
try:
    import google.generativeai as genai
    HAS_GENAI = True
except ImportError:
    genai = None
    HAS_GENAI = False

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Import from existing engine
import sys
_carry_root = Path(__file__).parent.parent.parent
if str(_carry_root) not in sys.path:
    sys.path.insert(0, str(_carry_root))

from carry.engine.interaction import Assemblage, load_assemblages, load_all_encounters

if HAS_GENAI:
    genai.configure(api_key=os.getenv("GEMINI_KEY"))


# =============================================================================
# DATA STRUCTURES
# =============================================================================

class SpaceCompatibility(Enum):
    """Space type compatibility levels."""
    BOTH_SMOOTH = "both_smooth"
    BOTH_STRIATED = "both_striated"
    MIXED = "mixed"
    OPPOSING = "opposing"


@dataclass
class ProximityScore:
    """Multi-dimensional proximity between two assemblages."""
    assemblage_a: str
    assemblage_b: str

    # Individual dimension scores (0.0 = far, 1.0 = close)
    intensity_proximity: float
    space_type_proximity: float
    semantic_proximity: float
    becoming_overlap: float

    # Composite score
    composite_score: float

    # Explanatory metadata
    shared_becomings: List[str] = field(default_factory=list)
    space_compatibility: SpaceCompatibility = SpaceCompatibility.MIXED


@dataclass
class ProximityMatrix:
    """Full proximity matrix for a set of assemblages."""
    assemblage_names: List[str]
    scores: Dict[Tuple[str, str], ProximityScore] = field(default_factory=dict)

    def get_score(self, a: str, b: str) -> Optional[ProximityScore]:
        """Get proximity score between two assemblages (order-independent)."""
        key = tuple(sorted([a, b]))
        return self.scores.get(key)

    def get_nearest_neighbors(self, name: str, k: int = 5) -> List[Tuple[str, float]]:
        """Get k nearest assemblages to a given one."""
        neighbors = []
        for other in self.assemblage_names:
            if other != name:
                score = self.get_score(name, other)
                if score:
                    neighbors.append((other, score.composite_score))
        neighbors.sort(key=lambda x: x[1], reverse=True)
        return neighbors[:k]


# =============================================================================
# INTENSITY PROXIMITY
# =============================================================================

INTENSITY_DIMENSIONS = ['focus', 'patience', 'abstraction', 'speed', 'tactility', 'social']


def compute_intensity_distance(a: Assemblage, b: Assemblage) -> float:
    """
    Compute Euclidean distance in 6D intensity space.
    Returns normalized proximity (0.0 = maximum distance, 1.0 = identical).
    """
    vec_a = [a.intensity_field.get(d, 0.5) for d in INTENSITY_DIMENSIONS]
    vec_b = [b.intensity_field.get(d, 0.5) for d in INTENSITY_DIMENSIONS]

    euclidean_dist = sqrt(sum((va - vb) ** 2 for va, vb in zip(vec_a, vec_b)))
    max_dist = sqrt(len(INTENSITY_DIMENSIONS))  # Maximum in unit hypercube

    return 1.0 - (euclidean_dist / max_dist)


# =============================================================================
# SPACE TYPE PROXIMITY
# =============================================================================

def compute_space_type_proximity(a: Assemblage, b: Assemblage) -> Tuple[float, SpaceCompatibility]:
    """
    Analyze territory space type compatibility.
    Returns (proximity_score, compatibility_type).
    """
    def get_dominance(asm: Assemblage) -> str:
        if not asm.territories:
            return "mixed"
        smooth = sum(1 for t in asm.territories if t.space_type == "smooth")
        striated = len(asm.territories) - smooth
        if smooth > striated:
            return "smooth"
        elif striated > smooth:
            return "striated"
        return "mixed"

    a_dom = get_dominance(a)
    b_dom = get_dominance(b)

    if a_dom == b_dom:
        if a_dom == "smooth":
            return (0.9, SpaceCompatibility.BOTH_SMOOTH)
        elif a_dom == "striated":
            return (0.9, SpaceCompatibility.BOTH_STRIATED)
        else:
            return (0.6, SpaceCompatibility.MIXED)
    elif "mixed" in [a_dom, b_dom]:
        return (0.5, SpaceCompatibility.MIXED)
    else:
        return (0.2, SpaceCompatibility.OPPOSING)


# =============================================================================
# BECOMING VECTOR OVERLAP
# =============================================================================

# Semantic pairs for becoming vector similarity
SEMANTIC_BECOMING_PAIRS = [
    ("becoming-slow", "becoming-patient"),
    ("becoming-witness", "becoming-attentive"),
    ("becoming-fluid", "becoming-nomad"),
    ("becoming-precise", "becoming-attentive"),
    ("becoming-resonant", "becoming-embodied"),
    ("becoming-mortal", "becoming-small"),
    ("becoming-rootless", "becoming-nomad"),
    ("becoming-gesture", "becoming-embodied"),
]


def compute_becoming_overlap(a: Assemblage, b: Assemblage) -> Tuple[float, List[str]]:
    """
    Compute Jaccard similarity of becoming vectors with semantic boost.
    Returns (overlap_score, shared_becomings).
    """
    set_a = set(a.becoming_vectors)
    set_b = set(b.becoming_vectors)

    shared = set_a & set_b
    union = set_a | set_b

    if not union:
        return (0.0, [])

    jaccard = len(shared) / len(union)

    # Semantic boost for similar becomings
    semantic_boost = 0.0
    for v_a in set_a:
        for v_b in set_b:
            if v_a != v_b and ((v_a, v_b) in SEMANTIC_BECOMING_PAIRS or
                              (v_b, v_a) in SEMANTIC_BECOMING_PAIRS):
                semantic_boost += 0.1

    return (min(1.0, jaccard + semantic_boost), list(shared))


# =============================================================================
# SEMANTIC PROXIMITY (LLM)
# =============================================================================

def compute_semantic_proximity(
    a: Assemblage,
    b: Assemblage,
    cache: Optional[Dict[Tuple[str, str], float]] = None,
    model_name: str = "gemini-2.0-flash"
) -> float:
    """
    LLM-computed semantic similarity of component capacities.
    Results are cached to avoid repeated API calls.
    """
    key = tuple(sorted([a.name, b.name]))

    if cache is not None and key in cache:
        return cache[key]

    capacities_a = [c.capacity for c in a.components]
    capacities_b = [c.capacity for c in b.components]

    if not capacities_a or not capacities_b:
        return 0.5  # Neutral if no components

    if not HAS_GENAI:
        raise ImportError("google.generativeai is required for semantic proximity")

    model = genai.GenerativeModel(model_name)

    prompt = f"""Rate the semantic similarity between these two sets of component capacities on a scale of 0.0 to 1.0.

SET A (from {a.name}):
{chr(10).join(f'- {c}' for c in capacities_a)}

SET B (from {b.name}):
{chr(10).join(f'- {c}' for c in capacities_b)}

Consider:
- Do they operate on similar materials or domains?
- Do they share similar functional orientations?
- Could they work together or do they oppose each other?

Return ONLY a single decimal number between 0.0 and 1.0.
0.0 = completely unrelated or opposing capacities
0.5 = neutral, neither related nor opposing
1.0 = highly related, complementary capacities
"""

    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        score = float(text)
        score = max(0.0, min(1.0, score))
    except Exception as e:
        print(f"Warning: LLM semantic proximity failed: {e}")
        score = 0.5

    if cache is not None:
        cache[key] = score

    return score


def batch_compute_semantic_proximity(
    assemblages: List[Assemblage],
    model_name: str = "gemini-2.0-flash"
) -> Dict[Tuple[str, str], float]:
    """
    Pre-compute semantic proximity for all pairs.
    More efficient than individual calls.
    """
    cache = {}
    n = len(assemblages)
    total_pairs = n * (n - 1) // 2

    print(f"Computing semantic proximity for {total_pairs} pairs...")

    for i in range(n):
        for j in range(i + 1, n):
            a, b = assemblages[i], assemblages[j]
            key = tuple(sorted([a.name, b.name]))
            cache[key] = compute_semantic_proximity(a, b, cache=None, model_name=model_name)

    print(f"Cached {len(cache)} semantic proximity scores")
    return cache


# =============================================================================
# COMPOSITE PROXIMITY
# =============================================================================

DEFAULT_WEIGHTS = {
    'intensity': 0.35,
    'space': 0.20,
    'semantic': 0.25,
    'becoming': 0.20
}


def compute_proximity(
    a: Assemblage,
    b: Assemblage,
    weights: Optional[Dict[str, float]] = None,
    semantic_cache: Optional[Dict[Tuple[str, str], float]] = None,
    use_llm_semantics: bool = True,
    model_name: str = "gemini-2.0-flash"
) -> ProximityScore:
    """
    Compute full multi-dimensional proximity between two assemblages.
    """
    weights = weights or DEFAULT_WEIGHTS

    # 1. Intensity proximity
    intensity_prox = compute_intensity_distance(a, b)

    # 2. Space type proximity
    space_prox, space_compat = compute_space_type_proximity(a, b)

    # 3. Becoming overlap
    becoming_prox, shared_becomings = compute_becoming_overlap(a, b)

    # 4. Semantic proximity
    if use_llm_semantics:
        semantic_prox = compute_semantic_proximity(a, b, semantic_cache, model_name)
    else:
        semantic_prox = 0.5  # Neutral default

    # 5. Composite score
    composite = (
        weights['intensity'] * intensity_prox +
        weights['space'] * space_prox +
        weights['semantic'] * semantic_prox +
        weights['becoming'] * becoming_prox
    )

    return ProximityScore(
        assemblage_a=a.name,
        assemblage_b=b.name,
        intensity_proximity=intensity_prox,
        space_type_proximity=space_prox,
        semantic_proximity=semantic_prox,
        becoming_overlap=becoming_prox,
        composite_score=composite,
        shared_becomings=shared_becomings,
        space_compatibility=space_compat
    )


# =============================================================================
# PROXIMITY MATRIX BUILDER
# =============================================================================

def build_proximity_matrix(
    assemblages: List[Assemblage],
    weights: Optional[Dict[str, float]] = None,
    use_llm_semantics: bool = True,
    model_name: str = "gemini-2.0-flash"
) -> ProximityMatrix:
    """
    Build full proximity matrix for all assemblage pairs.
    """
    names = [a.name for a in assemblages]
    name_to_asm = {a.name: a for a in assemblages}

    # Pre-compute semantic cache if using LLM
    semantic_cache = None
    if use_llm_semantics:
        semantic_cache = batch_compute_semantic_proximity(assemblages, model_name)

    # Compute all pairs
    scores = {}
    n = len(assemblages)

    for i in range(n):
        for j in range(i + 1, n):
            a, b = assemblages[i], assemblages[j]
            key = tuple(sorted([a.name, b.name]))

            scores[key] = compute_proximity(
                a, b,
                weights=weights,
                semantic_cache=semantic_cache,
                use_llm_semantics=use_llm_semantics,
                model_name=model_name
            )

    return ProximityMatrix(assemblage_names=names, scores=scores)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    from pathlib import Path

    carry_root = Path(__file__).parent.parent
    subjects_path = carry_root / "assemblages" / "subjects" / "hari.yaml"

    print("Loading subject assemblages...")
    subjects = load_assemblages(subjects_path)
    print(f"Loaded {len(subjects)} assemblages")

    # Test proximity between first two assemblages
    if len(subjects) >= 2:
        a, b = subjects[0], subjects[1]
        print(f"\nComputing proximity: {a.name} <-> {b.name}")

        score = compute_proximity(a, b, use_llm_semantics=False)

        print(f"  Intensity proximity: {score.intensity_proximity:.3f}")
        print(f"  Space type proximity: {score.space_type_proximity:.3f}")
        print(f"  Becoming overlap: {score.becoming_overlap:.3f}")
        print(f"  Composite score: {score.composite_score:.3f}")
        print(f"  Space compatibility: {score.space_compatibility.value}")
        print(f"  Shared becomings: {score.shared_becomings}")
