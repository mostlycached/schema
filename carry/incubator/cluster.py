"""
Cluster Module: Assemblage Clustering by Proximity

Groups assemblages into incubation clusters using hierarchical clustering.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Dict, Optional

from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

from carry.incubator.proximity import (
    ProximityMatrix,
    ProximityScore,
    build_proximity_matrix,
    INTENSITY_DIMENSIONS
)
from carry.engine.interaction import Assemblage


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class IncubationCluster:
    """A group of assemblages close enough to incubate together."""
    cluster_id: int
    assemblages: List[Assemblage]
    centroid_intensities: Dict[str, float] = field(default_factory=dict)

    # Cluster characteristics
    internal_cohesion: float = 0.0
    dominant_space_type: str = "mixed"
    shared_becomings: List[str] = field(default_factory=list)

    # Fertility indicators
    diversity_score: float = 0.0
    tension_potential: float = 0.0


@dataclass
class ClusteringResult:
    """Result of clustering assemblages."""
    clusters: List[IncubationCluster]
    noise: List[Assemblage]  # Assemblages that didn't cluster
    proximity_matrix: ProximityMatrix

    # Parameters used
    proximity_threshold: float = 0.5
    min_cluster_size: int = 2


# =============================================================================
# CLUSTERING
# =============================================================================

def cluster_by_proximity(
    assemblages: List[Assemblage],
    proximity_matrix: ProximityMatrix,
    threshold: float = 0.5,
    min_cluster_size: int = 2,
    linkage_method: str = "average"
) -> ClusteringResult:
    """
    Cluster assemblages based on proximity scores using hierarchical clustering.

    Args:
        assemblages: List of assemblages to cluster
        proximity_matrix: Pre-computed proximity matrix
        threshold: Minimum proximity to be in same cluster (0.0-1.0)
        min_cluster_size: Minimum assemblages per cluster
        linkage_method: 'average', 'single', 'complete', 'ward'

    Returns:
        ClusteringResult with clusters and noise
    """
    n = len(assemblages)
    if n < 2:
        return ClusteringResult(
            clusters=[],
            noise=assemblages,
            proximity_matrix=proximity_matrix,
            proximity_threshold=threshold,
            min_cluster_size=min_cluster_size
        )

    names = [a.name for a in assemblages]
    name_to_asm = {a.name: a for a in assemblages}

    # Build condensed distance matrix (1 - proximity)
    distances = []
    for i in range(n):
        for j in range(i + 1, n):
            score = proximity_matrix.get_score(names[i], names[j])
            if score:
                dist = 1.0 - score.composite_score
            else:
                dist = 1.0  # Maximum distance if no score
            distances.append(dist)

    # Hierarchical clustering
    Z = linkage(distances, method=linkage_method)

    # Cut at threshold (convert proximity threshold to distance threshold)
    distance_threshold = 1.0 - threshold
    labels = fcluster(Z, t=distance_threshold, criterion='distance')

    # Group assemblages by cluster
    cluster_map = defaultdict(list)
    for asm, label in zip(assemblages, labels):
        cluster_map[label].append(asm)

    # Build IncubationClusters
    clusters = []
    noise = []
    cluster_id = 0

    for label, members in cluster_map.items():
        if len(members) >= min_cluster_size:
            cluster = IncubationCluster(
                cluster_id=cluster_id,
                assemblages=members
            )
            cluster = compute_cluster_characteristics(cluster, proximity_matrix)
            clusters.append(cluster)
            cluster_id += 1
        else:
            noise.extend(members)

    return ClusteringResult(
        clusters=clusters,
        noise=noise,
        proximity_matrix=proximity_matrix,
        proximity_threshold=threshold,
        min_cluster_size=min_cluster_size
    )


# =============================================================================
# CLUSTER CHARACTERISTICS
# =============================================================================

def compute_cluster_characteristics(
    cluster: IncubationCluster,
    proximity_matrix: ProximityMatrix
) -> IncubationCluster:
    """
    Compute cluster-level characteristics:
    - internal_cohesion: Average proximity between all pairs
    - dominant_space_type: Mode of space types across all territories
    - shared_becomings: Becoming vectors shared by 2+ members
    - diversity_score: Variance of intensity fields
    - tension_potential: Based on intensity extremes
    """
    assemblages = cluster.assemblages
    n = len(assemblages)

    # Centroid intensities
    centroid = {dim: 0.0 for dim in INTENSITY_DIMENSIONS}
    for asm in assemblages:
        for dim in INTENSITY_DIMENSIONS:
            centroid[dim] += asm.intensity_field.get(dim, 0.5)
    cluster.centroid_intensities = {dim: val / n for dim, val in centroid.items()}

    # Internal cohesion
    if n >= 2:
        total_proximity = 0.0
        pair_count = 0
        for i in range(n):
            for j in range(i + 1, n):
                score = proximity_matrix.get_score(
                    assemblages[i].name,
                    assemblages[j].name
                )
                if score:
                    total_proximity += score.composite_score
                    pair_count += 1
        cluster.internal_cohesion = total_proximity / pair_count if pair_count > 0 else 0.0
    else:
        cluster.internal_cohesion = 1.0

    # Dominant space type
    smooth_count = 0
    striated_count = 0
    for asm in assemblages:
        for t in asm.territories:
            if t.space_type == "smooth":
                smooth_count += 1
            else:
                striated_count += 1

    if smooth_count > striated_count * 1.5:
        cluster.dominant_space_type = "smooth"
    elif striated_count > smooth_count * 1.5:
        cluster.dominant_space_type = "striated"
    else:
        cluster.dominant_space_type = "mixed"

    # Shared becomings (appearing in 2+ assemblages)
    becoming_counts = defaultdict(int)
    for asm in assemblages:
        for bv in asm.becoming_vectors:
            becoming_counts[bv] += 1
    cluster.shared_becomings = [bv for bv, count in becoming_counts.items() if count >= 2]

    # Diversity score (variance of intensity fields)
    variance_sum = 0.0
    for dim in INTENSITY_DIMENSIONS:
        values = [asm.intensity_field.get(dim, 0.5) for asm in assemblages]
        mean = sum(values) / n
        variance = sum((v - mean) ** 2 for v in values) / n
        variance_sum += variance
    cluster.diversity_score = min(1.0, variance_sum / len(INTENSITY_DIMENSIONS) * 4)

    # Tension potential (based on intensity extremes within cluster)
    max_diff = 0.0
    for dim in INTENSITY_DIMENSIONS:
        values = [asm.intensity_field.get(dim, 0.5) for asm in assemblages]
        diff = max(values) - min(values)
        max_diff = max(max_diff, diff)
    cluster.tension_potential = max_diff

    return cluster


# =============================================================================
# INCUBATION GROUP SUGGESTION
# =============================================================================

def suggest_incubation_groups(
    subjects: List[Assemblage],
    encounters: List[Assemblage],
    proximity_matrix: ProximityMatrix,
    max_group_size: int = 5,
    min_proximity: float = 0.4
) -> List[IncubationCluster]:
    """
    Suggest groups for incubation by mixing subjects with encounters.

    Strategy:
    1. For each subject, find top-k nearest encounters
    2. Form clusters around each subject + its nearest encounters
    """
    clusters = []
    cluster_id = 0

    for subject in subjects:
        # Get nearest encounters
        neighbors = []
        for enc in encounters:
            score = proximity_matrix.get_score(subject.name, enc.name)
            if score and score.composite_score >= min_proximity:
                neighbors.append((enc, score.composite_score))

        neighbors.sort(key=lambda x: x[1], reverse=True)
        nearest = [enc for enc, _ in neighbors[:max_group_size - 1]]

        if nearest:
            cluster = IncubationCluster(
                cluster_id=cluster_id,
                assemblages=[subject] + nearest
            )
            cluster = compute_cluster_characteristics(cluster, proximity_matrix)
            clusters.append(cluster)
            cluster_id += 1

    return clusters


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    from pathlib import Path
    from carry.engine.interaction import load_assemblages

    carry_root = Path(__file__).parent.parent
    subjects_path = carry_root / "assemblages" / "subjects" / "hari.yaml"

    print("Loading subject assemblages...")
    subjects = load_assemblages(subjects_path)
    print(f"Loaded {len(subjects)} assemblages")

    if len(subjects) >= 2:
        print("\nBuilding proximity matrix (no LLM)...")
        matrix = build_proximity_matrix(subjects, use_llm_semantics=False)

        print("\nClustering with threshold=0.5...")
        result = cluster_by_proximity(subjects, matrix, threshold=0.5, min_cluster_size=2)

        print(f"\nFound {len(result.clusters)} clusters, {len(result.noise)} noise")

        for cluster in result.clusters:
            print(f"\nCluster {cluster.cluster_id}:")
            print(f"  Members: {[a.name for a in cluster.assemblages]}")
            print(f"  Cohesion: {cluster.internal_cohesion:.3f}")
            print(f"  Diversity: {cluster.diversity_score:.3f}")
            print(f"  Tension Potential: {cluster.tension_potential:.3f}")
            print(f"  Dominant Space: {cluster.dominant_space_type}")
            print(f"  Shared Becomings: {cluster.shared_becomings}")
