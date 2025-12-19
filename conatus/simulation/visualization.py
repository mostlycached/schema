"""
Visualization: Tools for rendering simulation results

This module provides console output, Mermaid diagram generation,
and matplotlib plots for visualizing agent dynamics.
"""

from typing import Optional
import sys


def print_simulation_summary(agent) -> None:
    """Print a rich summary of the simulation run."""
    summary = agent.get_summary()
    
    print("\n" + "=" * 60)
    print("SIMULATION SUMMARY")
    print("=" * 60)
    print(f"Total Steps: {summary['total_steps']}")
    print(f"Stance Transitions: {summary['transitions']}")
    print(f"Stances Discovered: {summary['stances_discovered']}")
    print(f"Average Viability: {summary['avg_viability']:.2f}")
    print(f"Final Stance: {summary['final_stance']}")
    print(f"Final Affect: {summary['final_affect']}")
    
    print("\n--- Stance History ---")
    prev = None
    for i, stance in enumerate(summary['stance_history']):
        marker = " → " if stance != prev else "   "
        if stance != prev:
            print(f"{marker}[{i+1}] {stance}")
        prev = stance
    
    print("\n--- Discovered Affect Registers ---")
    for affect in summary['all_affect_registers']:
        print(f"  • {affect}")
    print("=" * 60)


def render_mermaid_diagram(events: list, title: str = "Stance Transitions") -> str:
    """
    Generate a Mermaid flowchart showing stance transitions.
    
    Args:
        events: List of SimulationEvent objects
        title: Diagram title
    
    Returns:
        Mermaid diagram as string
    """
    lines = [
        "graph TD",
        f"    subgraph \"{title}\"",
    ]
    
    # Track unique stances and transitions
    stances_seen = set()
    transitions = []
    current_stance = None
    
    for event in events:
        stances_seen.add(event.stance_name)
        
        if event.transition_occurred and event.new_stance_name:
            from_stance = current_stance or event.stance_name
            to_stance = event.new_stance_name
            transitions.append((from_stance, to_stance, event.timestep))
            stances_seen.add(to_stance)
        
        current_stance = event.stance_name
    
    # Create nodes for each stance
    stance_ids = {}
    for i, stance in enumerate(stances_seen):
        stance_id = f"S{i}"
        stance_ids[stance] = stance_id
        # Sanitize stance name for Mermaid
        safe_name = stance.replace('"', "'").replace("(", "[").replace(")", "]")
        lines.append(f'    {stance_id}["{safe_name}"]')
    
    # Create transition edges
    for from_s, to_s, step in transitions:
        from_id = stance_ids.get(from_s, "S?")
        to_id = stance_ids.get(to_s, "S?")
        lines.append(f'    {from_id} -->|"Step {step}: Trauma"| {to_id}')
    
    # Mark initial and final
    if events:
        initial = events[0].stance_name
        final = events[-1].stance_name
        initial_id = stance_ids.get(initial, "S?")
        final_id = stance_ids.get(final, "S?")
        
        lines.append(f'    START(("Start")) --> {initial_id}')
        lines.append(f'    {final_id} --> END(("End"))')
    
    lines.append("    end")
    
    # Add styling
    lines.extend([
        "",
        "    style START fill:#90EE90",
        "    style END fill:#FFB6C1",
    ])
    
    return "\n".join(lines)


def render_state_diagram(events: list) -> str:
    """
    Generate a Mermaid state diagram showing mode transitions.
    
    Args:
        events: List of SimulationEvent objects
    
    Returns:
        Mermaid state diagram as string
    """
    lines = [
        "stateDiagram-v2",
        "    [*] --> ADOPTION",
        "",
    ]
    
    # Track mode sequences
    for i, event in enumerate(events):
        mode = event.mode.value.upper()
        next_mode = events[i + 1].mode.value.upper() if i < len(events) - 1 else None
        
        if next_mode and mode != next_mode:
            if mode == "ADOPTION" and next_mode == "NOVELTY_SEARCH":
                lines.append(f'    ADOPTION --> NOVELTY_SEARCH : Step {event.timestep} (V={event.viability:.2f})')
            elif mode == "NOVELTY_SEARCH" and next_mode == "ADOPTION":
                lines.append(f'    NOVELTY_SEARCH --> ADOPTION : New stance discovered')
    
    lines.append("    ADOPTION --> [*]")
    
    return "\n".join(lines)


def plot_viability_timeline(
    events: list,
    threshold: float = 0.4,
    save_path: Optional[str] = None,
    show: bool = True,
) -> None:
    """
    Plot viability scores over time with transition markers.
    
    Args:
        events: List of SimulationEvent objects
        threshold: Viability threshold line
        save_path: Path to save the plot (optional)
        show: Whether to display the plot
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not available. Install with: pip install matplotlib")
        return
    
    timesteps = [e.timestep for e in events]
    viabilities = [e.viability for e in events]
    transitions = [(e.timestep, e.viability) for e in events if e.transition_occurred]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Plot viability line
    ax.plot(timesteps, viabilities, 'b-o', linewidth=2, markersize=8, label='Viability')
    
    # Plot threshold line
    ax.axhline(y=threshold, color='r', linestyle='--', linewidth=1.5, label=f'Threshold ({threshold})')
    
    # Mark transitions
    if transitions:
        trans_x, trans_y = zip(*transitions)
        ax.scatter(trans_x, trans_y, color='red', s=200, marker='*', zorder=5, label='Stance Transition')
    
    # Color regions
    for i, event in enumerate(events):
        if event.viability < threshold:
            ax.axvspan(event.timestep - 0.4, event.timestep + 0.4, 
                      alpha=0.2, color='red')
    
    # Labels and title
    ax.set_xlabel('Timestep', fontsize=12)
    ax.set_ylabel('Viability', fontsize=12)
    ax.set_title('Agent Viability Over Time', fontsize=14)
    ax.legend(loc='upper right')
    ax.set_ylim(0, 1.1)
    ax.grid(True, alpha=0.3)
    
    # Annotations for stances
    current_stance = None
    for event in events:
        if event.stance_name != current_stance:
            ax.annotate(
                event.stance_name[:15] + "..." if len(event.stance_name) > 15 else event.stance_name,
                xy=(event.timestep, event.viability),
                xytext=(event.timestep, event.viability + 0.1),
                fontsize=8,
                ha='center',
                arrowprops=dict(arrowstyle='->', color='gray', lw=0.5)
            )
            current_stance = event.stance_name
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    
    if show:
        plt.show()


def rich_console_output(event, use_color: bool = True) -> str:
    """
    Generate rich console output for a single event.
    
    Args:
        event: SimulationEvent object
        use_color: Whether to use ANSI color codes
    
    Returns:
        Formatted string
    """
    if use_color:
        RESET = "\033[0m"
        BOLD = "\033[1m"
        GREEN = "\033[92m"
        YELLOW = "\033[93m"
        RED = "\033[91m"
        BLUE = "\033[94m"
        CYAN = "\033[96m"
    else:
        RESET = BOLD = GREEN = YELLOW = RED = BLUE = CYAN = ""
    
    mode_color = GREEN if event.mode.value == "adoption" else YELLOW
    viability_color = GREEN if event.viability >= 0.4 else RED
    
    lines = [
        f"{BOLD}[Step {event.timestep}]{RESET}",
        f"  {mode_color}Mode: {event.mode.value.upper()}{RESET}",
        f"  {BLUE}Encounter: {event.encounter[:60]}...{RESET}",
        f"  {CYAN}Stance: {event.stance_name}{RESET}",
        f"  {viability_color}Viability: {event.viability:.2f}{RESET}",
    ]
    
    if event.transition_occurred:
        lines.append(f"  {RED}{BOLD}→ TRANSITION to: {event.new_stance_name}{RESET}")
        lines.append(f"  {CYAN}New Affect: {event.affect_register}{RESET}")
    
    return "\n".join(lines)


def export_to_markdown(events: list, agent, output_path: str) -> None:
    """
    Export simulation results to a markdown file.
    
    Args:
        events: List of SimulationEvent objects
        agent: ConatusAgent instance
        output_path: Path for output file
    """
    summary = agent.get_summary()
    mermaid = render_mermaid_diagram(events)
    
    content = [
        f"# Simulation Results: {agent.name}",
        "",
        f"**Context**: {agent.context}",
        f"**Total Steps**: {summary['total_steps']}",
        f"**Transitions**: {summary['transitions']}",
        f"**Final Stance**: {summary['final_stance']}",
        f"**Final Affect**: {summary['final_affect']}",
        "",
        "## Stance Transition Diagram",
        "",
        "```mermaid",
        mermaid,
        "```",
        "",
        "## Event Log",
        "",
        "| Step | Mode | Stance | Viability | Transition |",
        "|------|------|--------|-----------|------------|",
    ]
    
    for event in events:
        trans = f"→ {event.new_stance_name}" if event.transition_occurred else "-"
        content.append(
            f"| {event.timestep} | {event.mode.value} | {event.stance_name} | {event.viability:.2f} | {trans} |"
        )
    
    content.extend([
        "",
        "## Discovered Affect Registers",
        "",
    ])
    
    for affect in summary['all_affect_registers']:
        content.append(f"- **{affect}**")
    
    with open(output_path, "w") as f:
        f.write("\n".join(content))
    
    print(f"Results exported to {output_path}")
