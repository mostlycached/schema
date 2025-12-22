"""
Report Module: Generate Incubation Reports

Creates markdown and JSON reports for incubation results.
"""

import json
from typing import List, Optional
from dataclasses import asdict

from carry.incubator.cluster import IncubationCluster, ClusteringResult
from carry.incubator.incubation import IncubationResult
from carry.incubator.emergence import EmergenceResult
from carry.incubator.proximity import ProximityMatrix


# =============================================================================
# INCUBATION REPORT
# =============================================================================

def generate_incubation_report(
    result: IncubationResult,
    include_emergence: bool = True,
    format: str = "markdown"
) -> str:
    """
    Generate a comprehensive incubation report.
    """
    if format == "json":
        return _generate_json_report(result, include_emergence)
    return _generate_markdown_report(result, include_emergence)


def _generate_markdown_report(result: IncubationResult, include_emergence: bool) -> str:
    """Generate markdown report."""
    lines = []
    cluster = result.cluster

    # Header
    lines.append(f"# Incubation Report: Cluster {cluster.cluster_id}")
    lines.append("")

    # Incubation Chamber
    lines.append("## Incubation Chamber")
    lines.append("")
    lines.append(f"**{len(cluster.assemblages)} assemblages** in incubation:")
    lines.append("")

    for asm in cluster.assemblages:
        lines.append(f"### {asm.name}")
        lines.append(f"*{asm.abstract_machine}*")
        lines.append("")
        lines.append(f"- **Territories**: {', '.join(t.name for t in asm.territories)}")
        lines.append(f"- **Becoming Vectors**: {', '.join(asm.becoming_vectors)}")
        lines.append(f"- **Intensity Profile**: focus={asm.intensity_field.get('focus', 0.5):.1f}, "
                    f"patience={asm.intensity_field.get('patience', 0.5):.1f}, "
                    f"speed={asm.intensity_field.get('speed', 0.5):.1f}")
        lines.append("")

    # Cluster Characteristics
    lines.append("---")
    lines.append("## Cluster Characteristics")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Internal Cohesion | {cluster.internal_cohesion:.3f} |")
    lines.append(f"| Diversity Score | {cluster.diversity_score:.3f} |")
    lines.append(f"| Tension Potential | {cluster.tension_potential:.3f} |")
    lines.append(f"| Dominant Space Type | {cluster.dominant_space_type} |")
    lines.append("")

    if cluster.shared_becomings:
        lines.append(f"**Shared Becomings**: {', '.join(cluster.shared_becomings)}")
        lines.append("")

    # Transversal Lines
    lines.append("---")
    lines.append("## Transversal Lines")
    lines.append("")

    if result.transversal_lines:
        alliances = [l for l in result.transversal_lines if l.line_type in ("alliance", "resonance")]
        oppositions = [l for l in result.transversal_lines if l.line_type == "opposition"]

        if alliances:
            lines.append("### Alliances & Resonances")
            lines.append("")
            for line in alliances:
                emoji = "🤝" if line.line_type == "alliance" else "🔄"
                lines.append(f"- {emoji} **{line.dimension}** ({line.strength:.2f})")
                lines.append(f"  - Participants: {', '.join(line.participating_assemblages)}")
                lines.append(f"  - {line.description}")
            lines.append("")

        if oppositions:
            lines.append("### Oppositions")
            lines.append("")
            for line in oppositions:
                lines.append(f"- ⚡ **{line.dimension}** ({line.strength:.2f})")
                lines.append(f"  - {line.description}")
            lines.append("")
    else:
        lines.append("*No significant transversal lines detected*")
        lines.append("")

    # Collective Tensions
    lines.append("---")
    lines.append("## Collective Tensions")
    lines.append("")

    if result.collective_tensions:
        for tension in result.collective_tensions:
            severity_bar = "█" * int(tension.severity * 10) + "░" * (10 - int(tension.severity * 10))
            lines.append(f"### {tension.tension_type.replace('_', ' ').title()}")
            lines.append(f"**Severity**: [{severity_bar}] {tension.severity:.2f}")
            lines.append("")
            lines.append(f"{tension.description}")
            lines.append("")
            if tension.potential_resolution:
                lines.append(f"*Resolution*: {tension.potential_resolution}")
                lines.append("")
    else:
        lines.append("*No significant collective tensions detected*")
        lines.append("")

    # Actualization Potentials
    lines.append("---")
    lines.append("## Virtual Capacities Ready to Actualize")
    lines.append("")

    if result.actualization_potentials:
        for ap in result.actualization_potentials:
            prob_bar = "█" * int(ap.actualization_probability * 10) + "░" * (10 - int(ap.actualization_probability * 10))
            lines.append(f"### {ap.virtual_capacity_name}")
            lines.append(f"**Source**: {ap.source_assemblage}")
            lines.append(f"**Probability**: [{prob_bar}] {ap.actualization_probability:.2f}")
            lines.append(f"**Triggers**: {', '.join(ap.trigger_assemblages)}")
            lines.append("")
            lines.append(f"_{ap.explanation}_")
            lines.append("")
    else:
        lines.append("*No actualization potentials identified*")
        lines.append("")

    # Fertility Assessment
    lines.append("---")
    lines.append("## Fertility Assessment")
    lines.append("")

    fertility = result.fertility_assessment
    if fertility:
        if fertility.is_fertile:
            lines.append("### ✅ FERTILE")
            lines.append("")
            lines.append(f"**Fertility Score**: {fertility.fertility_score:.3f}")
        else:
            lines.append("### ❌ NOT FERTILE")
            lines.append("")

        lines.append("")
        lines.append("| Factor | Value | Threshold |")
        lines.append("|--------|-------|-----------|")
        lines.append(f"| Creative Tension | {fertility.creative_tension_level:.2f} | 0.25-0.75 |")
        lines.append(f"| Resonance Foundation | {fertility.resonance_foundation:.2f} | > 0.35 |")
        lines.append(f"| Virtual Triggers | {fertility.virtual_capacity_triggers} | >= 1 |")
        lines.append("")

        if fertility.is_fertile:
            lines.append(f"**Emergence Type**: {fertility.emergence_type.upper()}")
            lines.append("")
            if fertility.emergence_description:
                lines.append("**Emergence Description**:")
                lines.append(f"> {fertility.emergence_description}")
                lines.append("")

    # Emerged Assemblage
    if include_emergence and result.emerged_assemblage:
        lines.append("---")
        lines.append("## Emerged Assemblage")
        lines.append("")

        emerged = result.emerged_assemblage
        lines.append(f"### {emerged.name}")
        lines.append(f"*{emerged.abstract_machine}*")
        lines.append("")

        lines.append("**Territories**:")
        for t in emerged.territories:
            lines.append(f"- **{t.name}** ({t.space_type}): {t.function}")
        lines.append("")

        lines.append("**Codes**:")
        for c in emerged.codes:
            lines.append(f"- **{c.name}** [{c.level}]: \"{c.content}\"")
        lines.append("")

        lines.append("**Components**:")
        for c in emerged.components:
            lines.append(f"- **{c.name}** ({c.type}): {c.capacity}")
        lines.append("")

        lines.append("**Intensity Field**:")
        lines.append("```")
        for dim, val in emerged.intensity_field.items():
            bar = "█" * int(val * 10) + "░" * (10 - int(val * 10))
            lines.append(f"  {dim:12s}: [{bar}] {val:.2f}")
        lines.append("```")
        lines.append("")

        lines.append(f"**Becoming Vectors**: {', '.join(emerged.becoming_vectors)}")
        lines.append("")
        lines.append(f"**Stratification Depth**: {emerged.stratification_depth:.2f}")
        lines.append("")

    lines.append("---")
    lines.append("*Generated by Incubator Engine*")

    return "\n".join(lines)


def _generate_json_report(result: IncubationResult, include_emergence: bool) -> str:
    """Generate JSON report."""
    data = {
        "cluster": {
            "id": result.cluster.cluster_id,
            "assemblages": [a.name for a in result.cluster.assemblages],
            "internal_cohesion": result.cluster.internal_cohesion,
            "diversity_score": result.cluster.diversity_score,
            "tension_potential": result.cluster.tension_potential,
            "dominant_space_type": result.cluster.dominant_space_type,
            "shared_becomings": result.cluster.shared_becomings,
        },
        "transversal_lines": [
            {
                "line_type": l.line_type,
                "dimension": l.dimension,
                "participating_assemblages": l.participating_assemblages,
                "strength": l.strength,
                "description": l.description,
            }
            for l in result.transversal_lines
        ],
        "collective_tensions": [
            {
                "tension_type": t.tension_type,
                "sources": t.sources,
                "severity": t.severity,
                "description": t.description,
                "potential_resolution": t.potential_resolution,
            }
            for t in result.collective_tensions
        ],
        "actualization_potentials": [
            {
                "virtual_capacity_name": ap.virtual_capacity_name,
                "source_assemblage": ap.source_assemblage,
                "trigger_assemblages": ap.trigger_assemblages,
                "actualization_probability": ap.actualization_probability,
                "explanation": ap.explanation,
            }
            for ap in result.actualization_potentials
        ],
        "fertility_assessment": None,
        "emerged_assemblage": None,
    }

    if result.fertility_assessment:
        data["fertility_assessment"] = {
            "is_fertile": result.fertility_assessment.is_fertile,
            "fertility_score": result.fertility_assessment.fertility_score,
            "creative_tension_level": result.fertility_assessment.creative_tension_level,
            "resonance_foundation": result.fertility_assessment.resonance_foundation,
            "virtual_capacity_triggers": result.fertility_assessment.virtual_capacity_triggers,
            "emergence_type": result.fertility_assessment.emergence_type,
            "emergence_description": result.fertility_assessment.emergence_description,
        }

    if include_emergence and result.emerged_assemblage:
        emerged = result.emerged_assemblage
        data["emerged_assemblage"] = {
            "name": emerged.name,
            "abstract_machine": emerged.abstract_machine,
            "territories": [
                {"name": t.name, "function": t.function, "space_type": t.space_type}
                for t in emerged.territories
            ],
            "codes": [
                {"name": c.name, "content": c.content, "level": c.level}
                for c in emerged.codes
            ],
            "components": [
                {"name": c.name, "type": c.type, "capacity": c.capacity}
                for c in emerged.components
            ],
            "intensity_field": emerged.intensity_field,
            "becoming_vectors": emerged.becoming_vectors,
            "stratification_depth": emerged.stratification_depth,
        }

    return json.dumps(data, indent=2)


# =============================================================================
# CLUSTER SUMMARY
# =============================================================================

def generate_cluster_summary(
    clustering_result: ClusteringResult,
    format: str = "markdown"
) -> str:
    """
    Generate summary of clustering results.
    """
    if format == "json":
        return _generate_cluster_json(clustering_result)
    return _generate_cluster_markdown(clustering_result)


def _generate_cluster_markdown(result: ClusteringResult) -> str:
    """Generate markdown cluster summary."""
    lines = []

    lines.append("# Clustering Summary")
    lines.append("")
    lines.append(f"**Total Assemblages**: {len(result.proximity_matrix.assemblage_names)}")
    lines.append(f"**Clusters Found**: {len(result.clusters)}")
    lines.append(f"**Noise (unclustered)**: {len(result.noise)}")
    lines.append(f"**Proximity Threshold**: {result.proximity_threshold}")
    lines.append(f"**Minimum Cluster Size**: {result.min_cluster_size}")
    lines.append("")

    for cluster in result.clusters:
        lines.append("---")
        lines.append(f"## Cluster {cluster.cluster_id}")
        lines.append("")
        lines.append(f"**Members** ({len(cluster.assemblages)}):")
        for asm in cluster.assemblages:
            lines.append(f"- {asm.name}")
        lines.append("")

        lines.append("| Metric | Value |")
        lines.append("|--------|-------|")
        lines.append(f"| Cohesion | {cluster.internal_cohesion:.3f} |")
        lines.append(f"| Diversity | {cluster.diversity_score:.3f} |")
        lines.append(f"| Tension Potential | {cluster.tension_potential:.3f} |")
        lines.append(f"| Space Type | {cluster.dominant_space_type} |")
        lines.append("")

        if cluster.shared_becomings:
            lines.append(f"**Shared Becomings**: {', '.join(cluster.shared_becomings)}")
            lines.append("")

        # Fertility hint
        if cluster.tension_potential > 0.3 and cluster.internal_cohesion > 0.4:
            lines.append("⚗️ *This cluster shows fertility potential*")
            lines.append("")

    if result.noise:
        lines.append("---")
        lines.append("## Unclustered Assemblages")
        lines.append("")
        for asm in result.noise:
            lines.append(f"- {asm.name}")

    return "\n".join(lines)


def _generate_cluster_json(result: ClusteringResult) -> str:
    """Generate JSON cluster summary."""
    data = {
        "total_assemblages": len(result.proximity_matrix.assemblage_names),
        "clusters_found": len(result.clusters),
        "noise_count": len(result.noise),
        "proximity_threshold": result.proximity_threshold,
        "min_cluster_size": result.min_cluster_size,
        "clusters": [
            {
                "id": c.cluster_id,
                "members": [a.name for a in c.assemblages],
                "internal_cohesion": c.internal_cohesion,
                "diversity_score": c.diversity_score,
                "tension_potential": c.tension_potential,
                "dominant_space_type": c.dominant_space_type,
                "shared_becomings": c.shared_becomings,
            }
            for c in result.clusters
        ],
        "noise": [a.name for a in result.noise],
    }
    return json.dumps(data, indent=2)


# =============================================================================
# PROXIMITY MATRIX VISUALIZATION
# =============================================================================

def generate_proximity_heatmap(matrix: ProximityMatrix, format: str = "markdown") -> str:
    """
    Generate a text-based proximity heatmap.
    """
    names = matrix.assemblage_names
    n = len(names)

    # Shorten names for display
    short_names = [name[:15] + "..." if len(name) > 18 else name for name in names]

    lines = []
    lines.append("# Proximity Matrix")
    lines.append("")

    # Header
    header = "| " + " | ".join([""] + short_names) + " |"
    lines.append(header)
    lines.append("|" + "|".join(["---"] * (n + 1)) + "|")

    # Rows
    for i, name_i in enumerate(names):
        row = [short_names[i]]
        for j, name_j in enumerate(names):
            if i == j:
                row.append("1.00")
            else:
                score = matrix.get_score(name_i, name_j)
                if score:
                    row.append(f"{score.composite_score:.2f}")
                else:
                    row.append("-")
        lines.append("| " + " | ".join(row) + " |")

    return "\n".join(lines)


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("Report module ready. Use generate_incubation_report() or generate_cluster_summary().")
