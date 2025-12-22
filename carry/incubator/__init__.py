"""
Incubator Module: Assemblage Proximity, Clustering, and Emergence

Brings assemblages into proximity, analyzes collective dynamics,
and generates new hybrid assemblages from "fertile" incubations.

Usage:
    python -m carry.incubator --subjects <path> --encounters <path>

Example:
    python -m carry.incubator \
        --subjects carry/assemblages/subjects/hari.yaml \
        --encounters carry/assemblages/encounters \
        --threshold 0.5 \
        --output carry/incubator/results
"""

# Re-export main classes and functions
from carry.incubator.proximity import (
    ProximityScore,
    ProximityMatrix,
    SpaceCompatibility,
    compute_proximity,
    build_proximity_matrix,
    compute_intensity_distance,
    compute_space_type_proximity,
    compute_becoming_overlap,
    INTENSITY_DIMENSIONS,
    DEFAULT_WEIGHTS,
)

from carry.incubator.cluster import (
    IncubationCluster,
    ClusteringResult,
    cluster_by_proximity,
    compute_cluster_characteristics,
    suggest_incubation_groups,
)

from carry.incubator.incubation import (
    TransversalLine,
    CollectiveTension,
    ActualizationPotential,
    FertilityAssessment,
    IncubationResult,
    detect_transversal_lines,
    analyze_collective_tensions,
    identify_actualization_potentials,
    assess_fertility,
    incubate,
)

from carry.incubator.emergence import (
    EmergenceGenesis,
    EmergenceResult,
    generate_emerged_assemblage,
    validate_emergence,
    trace_genesis,
)

from carry.incubator.report import (
    generate_incubation_report,
    generate_cluster_summary,
    generate_proximity_heatmap,
)

from carry.incubator.viz import (
    build_proximity_network,
    build_cluster_network,
    build_incubation_network,
    visualize_proximity,
    visualize_clusters,
    visualize_incubation,
)

__all__ = [
    # Proximity
    "ProximityScore",
    "ProximityMatrix",
    "SpaceCompatibility",
    "compute_proximity",
    "build_proximity_matrix",
    "compute_intensity_distance",
    "compute_space_type_proximity",
    "compute_becoming_overlap",
    "INTENSITY_DIMENSIONS",
    "DEFAULT_WEIGHTS",
    # Cluster
    "IncubationCluster",
    "ClusteringResult",
    "cluster_by_proximity",
    "compute_cluster_characteristics",
    "suggest_incubation_groups",
    # Incubation
    "TransversalLine",
    "CollectiveTension",
    "ActualizationPotential",
    "FertilityAssessment",
    "IncubationResult",
    "detect_transversal_lines",
    "analyze_collective_tensions",
    "identify_actualization_potentials",
    "assess_fertility",
    "incubate",
    # Emergence
    "EmergenceGenesis",
    "EmergenceResult",
    "generate_emerged_assemblage",
    "validate_emergence",
    "trace_genesis",
    # Report
    "generate_incubation_report",
    "generate_cluster_summary",
    "generate_proximity_heatmap",
    # Viz
    "build_proximity_network",
    "build_cluster_network",
    "build_incubation_network",
    "visualize_proximity",
    "visualize_clusters",
    "visualize_incubation",
]


def main():
    """CLI entry point for the incubator module."""
    import argparse
    from pathlib import Path

    from carry.engine.interaction import load_assemblages, load_all_encounters

    parser = argparse.ArgumentParser(
        description="Incubator: Assemblage proximity, clustering, and emergence"
    )

    parser.add_argument(
        "--subjects", type=Path, required=True,
        help="Path to subject assemblages YAML file"
    )
    parser.add_argument(
        "--encounters", type=Path,
        help="Path to encounters directory (optional)"
    )
    parser.add_argument(
        "--output", type=Path,
        help="Output directory for reports and emerged assemblages"
    )

    # Proximity settings
    parser.add_argument(
        "--threshold", type=float, default=0.5,
        help="Proximity threshold for clustering (0.0-1.0, default: 0.5)"
    )
    parser.add_argument(
        "--min-cluster-size", type=int, default=2,
        help="Minimum assemblages per cluster (default: 2)"
    )
    parser.add_argument(
        "--no-llm", action="store_true",
        help="Disable LLM for semantic proximity (faster but less accurate)"
    )

    # Mode
    parser.add_argument(
        "--mode", choices=["cluster", "incubate", "full"], default="full",
        help="Mode: cluster (just cluster), incubate (analyze), full (with emergence)"
    )
    parser.add_argument(
        "--cluster-id", type=int,
        help="Only incubate a specific cluster by ID"
    )

    # Format
    parser.add_argument(
        "--format", choices=["markdown", "json"], default="markdown",
        help="Output format (default: markdown)"
    )

    # Visualization
    parser.add_argument(
        "--viz", action="store_true",
        help="Generate interactive HTML network visualizations"
    )

    args = parser.parse_args()

    # Load assemblages
    print("Loading assemblages...")
    subjects = load_assemblages(args.subjects)
    print(f"  Loaded {len(subjects)} subject assemblages from {args.subjects}")

    all_assemblages = list(subjects)

    if args.encounters:
        encounters = load_all_encounters(args.encounters)
        print(f"  Loaded {len(encounters)} encounter assemblages from {args.encounters}")
        all_assemblages.extend(encounters)

    print(f"  Total: {len(all_assemblages)} assemblages")

    # Build proximity matrix
    print("\nBuilding proximity matrix...")
    use_llm = not args.no_llm
    matrix = build_proximity_matrix(all_assemblages, use_llm_semantics=use_llm)
    print(f"  Computed {len(matrix.scores)} proximity scores")

    # Cluster
    print(f"\nClustering with threshold={args.threshold}, min_size={args.min_cluster_size}...")
    clustering = cluster_by_proximity(
        all_assemblages, matrix,
        threshold=args.threshold,
        min_cluster_size=args.min_cluster_size
    )
    print(f"  Found {len(clustering.clusters)} clusters, {len(clustering.noise)} noise")

    # Output clustering summary
    summary = generate_cluster_summary(clustering, format=args.format)
    print("\n" + summary)

    if args.mode == "cluster":
        if args.output:
            output_file = args.output / f"clusters.{args.format.replace('markdown', 'md')}"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(summary)
            print(f"\nSaved to {output_file}")

            # Generate visualizations for cluster mode
            if args.viz:
                print("\nGenerating visualizations...")

                prox_viz = args.output / "proximity.html"
                visualize_proximity(matrix, all_assemblages, prox_viz, threshold=args.threshold * 0.6)
                print(f"  Saved proximity network to {prox_viz}")

                cluster_viz = args.output / "clusters.html"
                visualize_clusters(clustering, cluster_viz)
                print(f"  Saved cluster network to {cluster_viz}")

                print("\nOpen the HTML files in a browser to explore interactively.")
        return

    # Incubate clusters
    generate_emergence = (args.mode == "full")

    for cluster in clustering.clusters:
        if args.cluster_id is not None and cluster.cluster_id != args.cluster_id:
            continue

        print(f"\n{'='*60}")
        print(f"Incubating Cluster {cluster.cluster_id}")
        print(f"{'='*60}")

        result = incubate(
            cluster, matrix,
            generate_emergence=generate_emergence
        )

        report = generate_incubation_report(
            result,
            include_emergence=generate_emergence,
            format=args.format
        )

        print("\n" + report)

        if args.output:
            output_file = args.output / f"cluster_{cluster.cluster_id}.{args.format.replace('markdown', 'md')}"
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(report)
            print(f"\nSaved to {output_file}")

            # Save emerged assemblage as YAML
            if result.emerged_assemblage and generate_emergence:
                import yaml
                emerged = result.emerged_assemblage
                emerged_data = {
                    "assemblages": [{
                        "name": emerged.name,
                        "abstract_machine": emerged.abstract_machine,
                        "entity_type": emerged.entity_type,
                        "territories": [
                            {"name": t.name, "function": t.function, "quality": t.quality, "space_type": t.space_type}
                            for t in emerged.territories
                        ],
                        "codes": [
                            {"name": c.name, "content": c.content, "type": c.type, "level": c.level}
                            for c in emerged.codes
                        ],
                        "components": [
                            {"name": c.name, "type": c.type, "capacity": c.capacity}
                            for c in emerged.components
                        ],
                        "intensity_field": emerged.intensity_field,
                        "becoming_vectors": emerged.becoming_vectors,
                        "stratification_depth": emerged.stratification_depth,
                    }]
                }
                emerged_file = args.output / f"emerged_{cluster.cluster_id}.yaml"
                emerged_file.write_text(yaml.dump(emerged_data, default_flow_style=False, allow_unicode=True))
                print(f"Saved emerged assemblage to {emerged_file}")

            # Generate visualization for this incubation
            if args.viz:
                viz_file = args.output / f"incubation_{cluster.cluster_id}.html"
                visualize_incubation(result, viz_file)
                print(f"Saved visualization to {viz_file}")

    # Generate overall visualizations
    if args.viz and args.output:
        print("\nGenerating visualizations...")

        # Proximity network
        prox_viz = args.output / "proximity.html"
        visualize_proximity(matrix, all_assemblages, prox_viz, threshold=args.threshold * 0.6)
        print(f"  Saved proximity network to {prox_viz}")

        # Cluster network
        cluster_viz = args.output / "clusters.html"
        visualize_clusters(clustering, cluster_viz)
        print(f"  Saved cluster network to {cluster_viz}")

        print("\nOpen the HTML files in a browser to explore interactively.")


if __name__ == "__main__":
    main()
