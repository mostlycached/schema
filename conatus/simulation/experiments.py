"""
Experiments Module

Utilities for configuring and running simulations.
"""

from typing import List, Optional
import os

from conatus.simulation import (
    ConatusAgent, Simulation,
    EnvironmentConfig, CriticConfig,
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
    critic_mode: str = "materialist",
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
        critic_mode: Super-ego mode (deleuze, barthes, nietzschean, etc.)
        muse: Inspirational generator (whitman, nietzsche, bataille, serres, etc.)
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
        critic_config=CriticConfig(mode=critic_mode),
        force_novelty=force_novelty,
        use_vector_store=use_vector_store,
        muse=muse,
    )
    
    muse_str = f" / {muse}" if muse else ""
    print(f"\nRunning simulation: {context} / {critic_mode}{muse_str}...")
    sim.run(encounters)
    
    # Generate report
    timestamp = os.path.getmtime(__file__) # Use file access time just for uniqueness or standard ts
    import time
    filename = f"{context}_{critic_mode}_{int(time.time())}.md"
    path = os.path.join(output_dir, context, filename)
    
    generate_report(
        sim,
        f"{context.title()}: {critic_mode.title()} Critique",
        f"Context: {context}. Critic: {critic_mode}. Force Novelty: {force_novelty}",
        path
    )
    
    return path

# Alias for backward compatibility
run_experiment = run_simulation

if __name__ == "__main__":
    # Example run
    run_simulation(
        context="forge",
        critic_mode="nietzschean",
        encounters=["Heavy lift failed", "Injury occurred"],
        output_dir="conatus/simulation/results"
    )
