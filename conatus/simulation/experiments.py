"""
Experiments Module

Utilities for configuring and running simulations.
"""

from typing import List, Optional
import os

from conatus.simulation import (
    ConatusAgent, Simulation,
    EnvironmentConfig,
    generate_report
)
from conatus.simulation.agent import FunctionalComponent, Stance
from conatus.simulation.components import ComponentVectorStore, BASE_COMPONENTS


# =============================================================================
# PRESETS
# =============================================================================

def create_agent(
    name: str,
    context: str,
    component_count: int = 20,
    use_vector_store: bool = False
) -> ConatusAgent:
    """Create a configured agent."""
    
    # Get components
    if use_vector_store:
        # Initial search query based on context
        store = ComponentVectorStore(persist_path=os.path.join(os.path.dirname(__file__), "component_db"))
        query = f"Capabilities for {context}"
        results = store.search(query, limit=component_count)
        components = [
            FunctionalComponent(c.name, c.description, c.modality)
            for c in results
        ]
    else:
        # Simple random subset from base
        import random
        subset = random.sample(BASE_COMPONENTS, min(len(BASE_COMPONENTS), component_count))
        components = [
            FunctionalComponent(c.name, c.description, c.modality)
            for c in subset
        ]

    # Create dummy initial stance (will be replaced or refined)
    initial_stance = Stance(
        name="Initial State",
        description=f"Baseline readiness for {context}",
        core_components=[c.name for c in components[:3]],
        active_weights={c.name: 0.8 for c in components[:3]},
        affect_register="neutral"
    )

    return ConatusAgent(
        name=name,
        context=context,
        functional_components=components,
        initial_stance=initial_stance,
    )


# =============================================================================
# EXPERIMENT RUNNER
# =============================================================================

def run_simulation(
    context: str = "forge",
    muse: str = None,
    encounters: List[str] = None,
    force_novelty: bool = True,
    use_vector_store: bool = True,
    output_dir: str = "conatus/simulation/results",
) -> str:
    """
    Run a full simulation experiment.
    
    Args:
        context: Environment context (forge, dance, arena, etc.)
        muse: Inspirational generator (whitman, nietzsche, bataille, serres, rilke, etc.)
              If None, a random muse is selected per step.
        encounters: List of challenges. If None, uses defaults.
        force_novelty: If True, always generate new stances.
        use_vector_store: If True, retrieve components per-encounter.
        output_dir: Where to save report.
        
    Returns:
        Path to generated report.
    """
    
    # Default encounters if not provided
    if not encounters:
        from conatus.simulation.environment import Environment
        env_gen = Environment(context)
        generated = env_gen.generate_encounter_sequence(3, pattern="escalating")
        encounters = [e.description for e in generated]
    
    # Create agent
    agent = create_agent(
        name=f"{context.title()} Practitioner",
        context=context,
        use_vector_store=use_vector_store
    )
    
    # Configure simulation
    sim = Simulation(
        agent=agent,
        env_config=EnvironmentConfig.for_context(context),
        force_novelty=force_novelty,
        use_vector_store=use_vector_store,
        muse=muse,
    )
    
    muse_name = muse or "random"
    print(f"\nRunning simulation: {context} / {muse_name}...")
    sim.run(encounters)
    
    # Generate report
    import time
    filename = f"{context}_{muse_name}_{int(time.time())}.md"
    path = os.path.join(output_dir, context, filename)
    
    generate_report(
        sim,
        f"{context.title()}: {muse_name.title()} Muse",
        f"Context: {context}. Muse: {muse_name}. Force Novelty: {force_novelty}",
        path
    )
    
    return path

# Alias for backward compatibility
run_experiment = run_simulation


# =============================================================================
# BIOGRAPHY RUNNER (LONGITUDINAL SIMULATION)
# =============================================================================

def run_biography(
    name: str = "Anonymous Subject",
    starting_age: int = 22,
    starting_institution: str = "phd_program",
    num_phases: int = 5,
    muse: str = None,
    narrative_mode: str = None,  # "tragedy", "comedy", "redemption", etc.
    life_archetype: str = None,  # "caretaker", "seeker", "builder", etc.
    output_dir: str = "conatus/simulation/results/biographies",
) -> str:
    """
    Run a longitudinal life simulation spanning years/decades.
    
    This extends the single-encounter simulation to track:
    - Habitus formation (repeated stances → dispositions)
    - Wounds from failures
    - Phase transitions through career/life stages
    - Accumulating repertoire
    - Relationships with significant Others
    - Narrative arc (tragedy/comedy/redemption/etc.)
    - LifeWorld particulars (places, objects, practices, body)
    
    Args:
        name: Name of the simulated subject
        starting_age: Age at simulation start
        starting_institution: Initial life context (from institutions.py)
        num_phases: Number of life phases to simulate
        muse: Inspirational generator for stance naming
        narrative_mode: Optional narrative arc ("tragedy", "comedy", "romance", 
                       "satire", "bildung", "redemption")
        life_archetype: Optional life type ("builder", "caretaker", "seeker",
                       "survivor", "drifter", "creator", "professional",
                       "devotee", "lover", "exile")
        output_dir: Where to save the biography report
        
    Returns:
        Path to generated biography report.
    """
    from conatus.simulation.biography import (
        Biography, LifePhase, PhaseArc, generate_biography_report
    )
    from conatus.simulation.institutions import get_institution, INSTITUTIONS
    
    # Get starting institution
    inst = get_institution(starting_institution)
    if not inst:
        available = ", ".join(INSTITUTIONS.keys())
        raise ValueError(f"Unknown institution: {starting_institution}. Available: {available}")
    
    # Create initial phase from institution
    initial_phase = LifePhase(
        name=f"Early {inst.name}",
        institution=starting_institution,
        age_start=starting_age,
        arc=PhaseArc.ASCENT,
        central_commitments=inst.expected_stances[:2],
        encounter_types=inst.encounter_patterns[:4],
    )
    
    # Create and run biography
    bio = Biography(
        name=name,
        starting_age=starting_age,
        context=starting_institution,
        muse=muse,
        narrative_mode=narrative_mode,
        life_archetype=life_archetype,
    )
    
    print(f"\n{'='*60}")
    print(f"BIOGRAPHY SIMULATION: {name}")
    print(f"Starting age: {starting_age}, Institution: {starting_institution}")
    print(f"Phases: {num_phases}, Muse: {muse or 'random'}")
    if narrative_mode:
        print(f"Narrative Arc: {narrative_mode.upper()}")
    if life_archetype:
        print(f"Life Archetype: {life_archetype.upper()}")
    if bio.state.lifeworld:
        print(f"Central Concern: {bio.state.lifeworld.central_concern}")
    print(f"{'='*60}")
    
    bio.run_biography(initial_phase, num_phases=num_phases)
    
    # Generate report
    import time
    filename = f"{name.lower().replace(' ', '_')}_{int(time.time())}.md"
    path = os.path.join(output_dir, filename)
    
    generate_biography_report(bio, path)
    
    # Summary
    print(f"\n{'='*60}")
    print(f"BIOGRAPHY COMPLETE")
    print(f"Final age: {bio.state.current_age:.0f}")
    print(f"Phases: {len(bio.phase_records)}")
    print(f"Repertoire: {len(bio.state.repertoire)} stances")
    print(f"Wounds: {len(bio.state.wounds)}")
    print(f"Report: {path}")
    print(f"{'='*60}")
    
    return path


# =============================================================================
# SCHIZOANALYTIC SIMULATION
# =============================================================================

def run_schizo(
    name: str = "Anonymous Process",
    initial_stratification: float = 0.5,
    num_operations: int = 25,
    output_dir: str = "conatus/simulation/results/schizo",
) -> str:
    """
    Run a schizoanalytic simulation.
    
    Unlike biography simulation, this:
    - Has no phases, only plateaus
    - Has no development, only intensity variations
    - Has no coherent self, only BwO inscriptions
    - Can break down (emptied BwO) or be recaptured (fully stratified)
    - Possible absolute deterritorialization (lines of flight)
    
    Args:
        name: Name for the process
        initial_stratification: 0-1, how stratified to start (0.5 = normal)
        num_operations: Number of cuts/jumps/destratifications to perform
        output_dir: Where to save the report
    
    Returns:
        Path to generated schizo-report.
    """
    from conatus.simulation.schizoanalysis import (
        run_schizo_process, generate_schizo_report
    )
    
    process = run_schizo_process(
        name=name,
        initial_intensity=initial_stratification,
        num_operations=num_operations,
    )
    
    # Generate report
    import time
    filename = f"{name.lower().replace(' ', '_')}_{int(time.time())}.md"
    path = os.path.join(output_dir, filename)
    
    generate_schizo_report(process, path)
    
    return path


if __name__ == "__main__":
    import sys
    
    # Check for biography mode
    if len(sys.argv) > 1 and sys.argv[1] == "biography":
        run_biography(
            name="Test Subject",
            starting_institution="phd_program",
            num_phases=4,
            muse="serres",
        )
    else:
        # Default: single simulation
        run_simulation(
            context="forge",
            muse="nietzsche",
            encounters=["Heavy lift failed", "Injury occurred"],
            output_dir="conatus/simulation/results"
        )

