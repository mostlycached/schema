"""
Visualization Module: Assemblage Networks

Generates network diagrams showing how multiple assemblages
intersect and share components, territories, codes, and intensities.
"""

import json
from typing import List, Dict, Set
from dataclasses import dataclass

from carry.simulation.assemblage import Assemblage


@dataclass
class AssemblageNetwork:
    """Network of intersecting assemblages for one person."""
    subject_name: str
    assemblages: List[Assemblage]
    
    def find_shared_components(self) -> Dict[str, List[str]]:
        """Find components shared across assemblages."""
        component_to_assemblages = {}
        for asm in self.assemblages:
            for comp in asm.components:
                if comp.name not in component_to_assemblages:
                    component_to_assemblages[comp.name] = []
                component_to_assemblages[comp.name].append(asm.name)
        
        # Return only shared ones
        return {k: v for k, v in component_to_assemblages.items() if len(v) > 1}
    
    def find_shared_territories(self) -> Dict[str, List[str]]:
        """Find territories shared across assemblages."""
        territory_to_assemblages = {}
        for asm in self.assemblages:
            for terr in asm.territories:
                if terr.name not in territory_to_assemblages:
                    territory_to_assemblages[terr.name] = []
                territory_to_assemblages[terr.name].append(asm.name)
        
        return {k: v for k, v in territory_to_assemblages.items() if len(v) > 1}
    
    def find_intensity_conflicts(self) -> List[Dict]:
        """Find same intensity dimensions with conflicting values."""
        conflicts = []
        all_intensities = set()
        for asm in self.assemblages:
            all_intensities.update(asm.intensity_field.keys())
        
        for intensity in all_intensities:
            values = {}
            for asm in self.assemblages:
                if intensity in asm.intensity_field:
                    values[asm.name] = asm.intensity_field[intensity]
            
            if len(values) > 1:
                min_val = min(values.values())
                max_val = max(values.values())
                if max_val - min_val > 0.3:  # Significant difference
                    conflicts.append({
                        "intensity": intensity,
                        "assemblages": values
                    })
        
        return conflicts
    
    def detect_transversal_lines_of_flight(self) -> List['LineOfFlight']:
        """
        Detect lines of flight that emerge from CONFLICTS BETWEEN assemblages.
        These are Deleuze's "transversal" lines - they cut across assemblages.
        """
        from carry.simulation.assemblage import LineOfFlight
        
        transversal_lines = []
        
        # 1. Shared component conflicts (body can't sustain incompatible operations)
        shared_comps = self.find_shared_components()
        for comp_name, asm_names in shared_comps.items():
            if len(asm_names) >= 2:
                # Find the assemblages
                asms = [a for a in self.assemblages if a.name in asm_names]
                
                # Check for speed conflicts in how this component is used
                speeds = [(a.name, a.intensity_field.get('speed', 0)) for a in asms]
                if len(speeds) >= 2:
                    max_speed = max(s[1] for s in speeds)
                    min_speed = min(s[1] for s in speeds)
                    
                    if max_speed - min_speed > 0.4:  # Significant conflict
                        transversal_lines.append(LineOfFlight(
                            direction=f"Forced slowdown or injury ({comp_name})",
                            source_type="inter-assemblage conflict",
                            source_description=f"{comp_name} operates at incompatible speeds: {speeds[0][0]} ({speeds[0][1]:.1f}) vs {speeds[1][0]} ({speeds[1][1]:.1f}). Body can't sustain switching.",
                            trigger_conditions="Repetitive strain, pain, or exhaustion forces resolution"
                        ))
        
        # 2. Shared territory conflicts (space can't be both smooth and striated)
        shared_terrs = self.find_shared_territories()
        for terr_name, asm_names in shared_terrs.items():
            asms = [a for a in self.assemblages if a.name in asm_names]
            terrs = []
            for a in asms:
                for t in a.territories:
                    if t.name == terr_name:
                        terrs.append((a.name, t.space_type))
            
            # Check for smooth/striated conflicts
            space_types = set(t[1] for t in terrs)
            if len(space_types) > 1:  # Conflict!
                transversal_lines.append(LineOfFlight(
                    direction=f"Spatial separation or time segregation",
                    source_type="inter-assemblage conflict",
                    source_description=f"{terr_name} must be simultaneously {' and '.join(space_types)} for different assemblages. Same space can't support both.",
                    trigger_conditions="Scheduling conflict or spatial reorganization forced"
                ))
        
        # 3. Intensity field conflicts (incompatible rhythms)
        conflicts = self.find_intensity_conflicts()
        for conflict in conflicts:
            intensity = conflict['intensity']
            values = conflict['assemblages']
            
            if intensity == 'speed':  # Speed conflicts especially generative
                avg_speed = sum(values.values()) / len(values)
                transversal_lines.append(LineOfFlight(
                    direction=f"Hybrid practice at {avg_speed:.1f} speed",
                    source_type="inter-assemblage conflict",
                    source_description=f"Speed varies wildly across assemblages: {', '.join(f'{k} ({v:.1f})' for k,v in values.items())}. Forces creation of intermediate practice.",
                    trigger_conditions="Burnout from switching or discovery of middle way"
                ))
        
        return transversal_lines
    
    def detect_synergistic_lines_of_flight(self) -> List['LineOfFlight']:
        """
        Detect SYNERGISTIC lines of flight - opportunities from assemblage COMPOSITION.
        When assemblages intersect, new capacities emerge that neither had alone.
        """
        from carry.simulation.assemblage import LineOfFlight
        
        synergistic_lines = []
        
        # Look for pairs of assemblages with complementary capacities
        for i in range(len(self.assemblages)):
            for j in range(i+1, len(self.assemblages)):
                asm1 = self.assemblages[i]
                asm2 = self.assemblages[j]
                
                # Check if they share components (intersection point)
                shared = set([c.name for c in asm1.components]) & set([c.name for c in asm2.components])
                
                if shared:
                    # They intersect - look for synergies
                    
                    # Pattern 1: Technical + Creative = Technical Writing/Creative Coding
                    if ("Professional" in asm1.name or "Professional" in asm2.name) and \
                       ("Creative" in asm1.name or "Creative" in asm2.name):
                        synergistic_lines.append(LineOfFlight(
                            direction="Technical Writing / Documentation",
                            source_type="assemblage composition",
                            source_description=f"Intersection of {asm1.name} (technical expertise) and {asm2.name} (writing skills). New capacity emerges that neither has alone.",
                            trigger_conditions="Blog post request, documentation need, or teaching opportunity"
                        ))
                        synergistic_lines.append(LineOfFlight(
                            direction="Creative Coding / Computational Art",
                            source_type="assemblage composition",
                            source_description=f"Programming skills from {asm1.name} + aesthetic sense from {asm2.name} = generative art, interactive narratives.",
                            trigger_conditions="Encounter with p5.js, Processing, or creative coding community"
                        ))
                    
                    # Pattern 2: Professional + Athletic = Performance Optimization
                    if ("Professional" in asm1.name or "Professional" in asm2.name) and \
                       ("Runner" in asm1.name or "Athletic" in asm2.name or "Runner" in asm2.name or "Athletic" in asm1.name):
                        synergistic_lines.append(LineOfFlight(
                            direction="Performance Science / Body Optimization",
                            source_type="assemblage composition",
                            source_description=f"Optimization mindset from {asm1.name} + body knowledge from {asm2.name} = data-driven training, biohacking.",
                            trigger_conditions="Wearable tech access, training plateau, or quantified self discovery"
                        ))
                    
                    # Pattern 3: Creative + Athletic = Embodied Storytelling
                    if ("Creative" in asm1.name or "Creative" in asm2.name) and \
                       ("Runner" in asm1.name or "Athletic" in asm2.name or "Runner" in asm2.name or "Athletic" in asm1.name):
                        synergistic_lines.append(LineOfFlight(
                            direction="Embodied Storytelling / Movement Poetry",
                            source_type="assemblage composition",
                            source_description=f"Narrative capacity from {asm1.name} + movement knowledge from {asm2.name} = somatic writing, running memoirs.",
                            trigger_conditions="Writing retreat, trail narrative project, or performance invitation"
                        ))
        
        return synergistic_lines
    
    def actualize_synergistic_line(self, line_direction: str) -> Optional[Assemblage]:
        """
        Actualize a synergistic line of flight - create the new assemblage it would produce.
        Returns the new assemblage that emerges from this composition.
        """
        from carry.simulation.assemblage import Assemblage, Territory, Code, Component
        
        # Map line directions to new assemblages
        if "Technical Writing" in line_direction:
            return Assemblage(
                name="Technical-Writer",
                abstract_machine="(Code Knowledge + Writing Skill) => (Documentation + Teaching)",
                territories=[
                    Territory("Blog", "Technical writing", "Explanatory", "smooth"),
                    Territory("Documentation site", "Reference writing", "Structured", "striated")
                ],
                codes=[
                    Code("Weekly blog post", "Every Sunday", "ritual", "molar"),
                    Code("Code example creation", "Automatic while writing", "pattern", "molecular")
                ],
                components=[
                    Component("Hands", "organic", "Type tutorials"),
                    Component("Mind", "organic", "Translate expertise to prose")
                ],
                intensity_field={"clarity": 0.9, "speed": 0.5, "helpfulness": 0.8},
                becoming_vectors=["becoming-teacher", "becoming-explainer"],
                stratification_depth=0.5
            )
        
        elif "Creative Coding" in line_direction:
            return Assemblage(
                name="Creative-Coder",
                abstract_machine="(Algorithm + Aesthetics) => (Generative Art + Interactive Experience)",
                territories=[
                    Territory("p5.js editor", "Creative coding", "Playful", "smooth"),
                    Territory("Gallery/Exhibition space", "Showing work", "Curated", "striated")
                ],
                codes=[
                    Code("Daily sketch", "Generate one visual daily", "ritual", "molar"),
                    Code("Aesthetic refinement loop", "Tweak until feels right", "pattern", "molecular")
                ],
                components=[
                    Component("Hands", "organic", "Code + adjust parameters"),
                    Component("Eyes", "organic", "See patterns, judge aesthetics")
                ],
                intensity_field={"playfulness": 0.9, "speed": 0.5, "beauty": 0.8},
                becoming_vectors=["becoming-artist", "becoming-experimental"],
                stratification_depth=0.3
            )
        
        # Add more actualizations as needed
        return None
    
    def generate_recursive_states(self, max_depth=2) -> Dict:
        """
        Generate recursive future states: what happens when lines of flight actualize.
        Returns dict with states at different depths.
        """
        states = {
            0: {"network": self, "description": "Current state"},
            1: {},  # Future state 1
            2: {}   # Future state 2
        }
        
        # Level 1: Actualize some synergistic lines
        synergistic = self.detect_synergistic_lines_of_flight()
        for i, lof in enumerate(synergistic[:2]):  # Limit to 2 for clarity
            new_assemblage = self.actualize_synergistic_line(lof.direction)
            if new_assemblage:
                # Create new network with this assemblage added
                new_assemblages = self.assemblages + [new_assemblage]
                future_network = AssemblageNetwork(
                    f"{self.subject_name} (Future 1: {lof.direction[:20]}...)",
                    new_assemblages
                )
                states[1][lof.direction] = {
                    "network": future_network,
                    "trigger": lof.direction,
                    "new_assemblage": new_assemblage
                }
        
        # Level 2: From each future state, detect new lines and actualize
        for trigger, state1_data in states[1].items():
            network1 = state1_data["network"]
            syn1 = network1.detect_synergistic_lines_of_flight()
            
            if syn1:  # Only create level 2 if new lines emerge
                lof_level2 = syn1[0]  # Take first new line
                new_asm_level2 = network1.actualize_synergistic_line(lof_level2.direction)
                
                if new_asm_level2:
                    new_assemblages_level2 = network1.assemblages + [new_asm_level2]
                    future_network2 = AssemblageNetwork(
                        f"{network1.subject_name} (Future 2)",
                        new_assemblages_level2
                    )
                    states[2][f"{trigger} → {lof_level2.direction}"] = {
                        "network": future_network2,
                        "parent_trigger": trigger,
                        "trigger": lof_level2.direction,
                        "new_assemblage": new_asm_level2
                    }
        
        return states
    
    def to_mermaid(self) -> str:
        """Generate Mermaid diagram showing assemblage network."""
        mermaid = "graph TB\n"
        mermaid += f"    Person[\"{self.subject_name}\"]\n\n"
        
        # Add assemblages
        for i, asm in enumerate(self.assemblages):
            asm_id = f"ASM{i}"
            mermaid += f"    {asm_id}[\"{asm.name}\"]\n"
            mermaid += f"    Person --> {asm_id}\n"
        
        mermaid += "\n"
        
        # Add shared components
        shared_comps = self.find_shared_components()
        for comp_name, asm_names in shared_comps.items():
            comp_id = comp_name.replace(" ", "_").replace("-", "_")
            mermaid += f"    {comp_id}({comp_name})\n"
            for asm_name in asm_names:
                asm_id = f"ASM{[a.name for a in self.assemblages].index(asm_name)}"
                mermaid += f"    {asm_id} -.-> {comp_id}\n"
        
        return mermaid
    
    def to_json_network(self) -> Dict:
        """Generate JSON network for graph visualization tools with full details."""
        nodes = []
        edges = []
        
        # Central person node
        nodes.append({
            "id": "person",
            "label": self.subject_name,
            "type": "person",
            "size": 30
        })
        
        # Assemblage nodes with full data
        for i, asm in enumerate(self.assemblages):
            asm_id = f"asm_{i}"
            nodes.append({
                "id": asm_id,
                "label": asm.name,
                "type": "assemblage",
                "size": 20,
                "stratification": asm.stratification_depth,
                "abstract_machine": asm.abstract_machine,
                "intensity_field": asm.intensity_field,
                "becoming_vectors": asm.becoming_vectors,
                "lines_of_flight": [
                    {
                        "direction": lof.direction,
                        "source_type": lof.source_type,
                        "source_description": lof.source_description,
                        "trigger_conditions": lof.trigger_conditions
                    } for lof in asm.lines_of_flight
                ],
                "virtual_capacities": [
                    {
                        "name": vc.name,
                        "access_point": vc.access_point,
                        "reason_unactualized": vc.reason_unactualized,
                        "actualization_trigger": vc.actualization_trigger
                    } for vc in asm.virtual_capacities
                ],
                "codes": [{"name": c.name, "content": c.content, "level": c.level} for c in asm.codes],
                "territories": [{"name": t.name, "function": t.function, "space_type": t.space_type} for t in asm.territories],
                "components": [{"name": c.name, "type": c.type, "capacity": c.capacity} for c in asm.components]
            })
            edges.append({
                "source": "person",
                "target": asm_id,
                "type": "plugs_into"
            })
        
        # Component nodes (shared)
        shared_comps = self.find_shared_components()
        for comp_name, asm_names in shared_comps.items():
            comp_id = f"comp_{comp_name.replace(' ', '_')}"
            nodes.append({
                "id": comp_id,
                "label": comp_name,
                "type": "component",
                "size": 15,
                "shared_by": asm_names
            })
            for asm_name in asm_names:
                asm_idx = [a.name for a in self.assemblages].index(asm_name)
                edges.append({
                    "source": f"asm_{asm_idx}",
                    "target": comp_id,
                    "type": "uses"
                })
        
        # Transversal lines of flight - CONFLICT-BASED
        transversal_lines = self.detect_transversal_lines_of_flight()
        for i, lof in enumerate(transversal_lines):
            lof_id = f"transversal_{i}"
            nodes.append({
                "id": lof_id,
                "label": lof.direction,
                "type": "transversal_line",
                "size": 18,
                "source_type": lof.source_type,
                "source_description": lof.source_description,
                "trigger_conditions": lof.trigger_conditions
            })
            
            # Connect to all assemblages (represents the conflict across them)
            for j in range(len(self.assemblages)):
                edges.append({
                    "source": f"asm_{j}",
                    "target": lof_id,
                    "type": "generates"
                })
        
        # Synergistic lines of flight - OPPORTUNITY-BASED
        synergistic_lines = self.detect_synergistic_lines_of_flight()
        for i, lof in enumerate(synergistic_lines):
            lof_id = f"synergistic_{i}"
            nodes.append({
                "id": lof_id,
                "label": lof.direction,
                "type": "synergistic_line",
                "size": 18,
                "source_type": lof.source_type,
                "source_description": lof.source_description,
                "trigger_conditions": lof.trigger_conditions
            })
            
            # Connect to relevant assemblages
            for j in range(len(self.assemblages)):
                edges.append({
                    "source": f"asm_{j}",
                    "target": lof_id,
                    "type": "composes"
                })
        
        return {"nodes": nodes, "edges": edges}
    
    def to_json_network_with_futures(self, include_futures=True) -> Dict:
        """Generate JSON network including recursive future states."""
        all_nodes = []
        all_edges = []
        
        if not include_futures:
            return self.to_json_network()
        
        # Generate recursive states
        states = self.generate_recursive_states()
        
        # Add current state (depth 0)
        current_json = self.to_json_network()
        for node in current_json["nodes"]:
            node["depth"] = 0
            node["opacity"] = 1.0
            all_nodes.append(node)
        for edge in current_json["edges"]:
            edge["depth"] = 0
            all_edges.append(edge)
        
        # Add future state 1 (depth 1)
        for trigger, state_data in states[1].items():
            future_network = state_data["network"]
            new_asm = state_data["new_assemblage"]
            
            # Add only the NEW assemblage node
            asm_idx = len(self.assemblages)  # Index of new assemblage
            all_nodes.append({
                "id": f"future1_asm_{asm_idx}_{trigger[:10]}",
                "label": new_asm.name,
                "type": "assemblage",
                "size": 18,
                "depth": 1,
                "opacity": 0.7,
                "stratification": new_asm.stratification_depth,
                "abstract_machine": new_asm.abstract_machine,
                "intensity_field": new_asm.intensity_field,
                "becoming_vectors": new_asm.becoming_vectors,
                "codes": [{"name": c.name, "content": c.content, "level": c.level} for c in new_asm.codes],
                "territories": [{"name": t.name, "function": t.function, "space_type": t.space_type} for t in new_asm.territories],
                "components": [{"name": c.name, "type": c.type, "capacity": c.capacity} for c in new_asm.components],
                "lines_of_flight": [],
                "virtual_capacities": []
            })
            
            # Connect to person
            all_edges.append({
                "source": "person",
                "target": f"future1_asm_{asm_idx}_{trigger[:10]}",
                "type": "plugs_into",
                "depth": 1
            })
        
        # Add future state 2 (depth 2)  
        for combo_trigger, state_data in states[2].items():
            new_asm = state_data["new_assemblage"]
            asm_idx = len(self.assemblages) + len(states[1])  # Further index
            
            all_nodes.append({
                "id": f"future2_asm_{asm_idx}",
                "label": new_asm.name,
                "type": "assemblage",
                "size": 16,
                "depth": 2,
                "opacity": 0.4,
                "stratification": new_asm.stratification_depth,
                "abstract_machine": new_asm.abstract_machine,
                "intensity_field": new_asm.intensity_field,
                "becoming_vectors": new_asm.becoming_vectors,
                "codes": [{"name": c.name, "content": c.content, "level": c.level} for c in new_asm.codes],
                "territories": [{"name": t.name, "function": t.function, "space_type": t.space_type} for t in new_asm.territories],
                "components": [{"name": c.name, "type": c.type, "capacity": c.capacity} for c in new_asm.components],
                "lines_of_flight": [],
                "virtual_capacities": []
            })
            
            all_edges.append({
                "source": "person",
                "target": f"future2_asm_{asm_idx}",
                "type": "plugs_into",
                "depth": 2
            })
        
        return {"nodes": all_nodes, "edges": all_edges}
    
    def render_assemblage_card(self, assemblage: Assemblage) -> str:
        """Render complete assemblage as detailed card."""
        card = f"## {assemblage.name}\n\n"
        
        # Abstract Machine
        card += f"**Abstract Machine**: *{assemblage.abstract_machine}*\n\n"
        card += f"**Stratification Depth**: {assemblage.stratification_depth:.2f} "
        card += f"({'Rigid' if assemblage.stratification_depth > 0.7 else 'Fluid' if assemblage.stratification_depth < 0.4 else 'Mixed'})\n\n"
        
        # Territories
        card += "### Territories\n"
        for t in assemblage.territories:
            card += f"- **{t.name}** `[{t.space_type}]`\n"
            card += f"  - Function: {t.function}\n"
            card += f"  - Quality: {t.quality}\n"
        card += "\n"
        
        # Codes
        card += "### Codes\n"
        molar_codes = [c for c in assemblage.codes if c.level == "molar"]
        molecular_codes = [c for c in assemblage.codes if c.level == "molecular"]
        
        if molar_codes:
            card += "**Molar (Visible)**:\n"
            for c in molar_codes:
                card += f"- {c.name}: *{c.content}*\n"
        
        if molecular_codes:
            card += "\n**Molecular (Invisible)**:\n"
            for c in molecular_codes:
                card += f"- {c.name}: *{c.content}*\n"
        card += "\n"
        
        # Components
        card += "### Components\n"
        organic = [c for c in assemblage.components if c.type == "organic"]
        technical = [c for c in assemblage.components if c.type == "technical"]
        
        if organic:
            card += "**Organic**:\n"
            for c in organic:
                card += f"- {c.name}: {c.capacity}\n"
        
        if technical:
            card += "\n**Technical**:\n"
            for c in technical:
                card += f"- {c.name}: {c.capacity}\n"
        card += "\n"
        
        # Intensity Field
        if assemblage.intensity_field:
            card += "### Intensity Field (BwO)\n"
            card += "```\n"
            for key, val in sorted(assemblage.intensity_field.items()):
                bar = "█" * int(val * 10)
                card += f"{key:20s} [{val:.2f}] {bar}\n"
            card += "```\n\n"
        
        # Becoming Vectors
        if assemblage.becoming_vectors:
            card += "### Becoming Vectors\n"
            for bv in assemblage.becoming_vectors:
                card += f"- {bv}\n"
            card += "\n"
        
        # Lines of Flight
        if assemblage.lines_of_flight:
            card += "### Lines of Flight\n"
            for lof in assemblage.lines_of_flight:
                card += f"- → {lof}\n"
            card += "\n"
        
        # Virtual Capacities
        if assemblage.virtual_capacities:
            card += "### Virtual Capacities *(unactualized)*\n"
            for vc in assemblage.virtual_capacities:
                card += f"- {vc}\n"
            card += "\n"
        
        card += "---\n\n"
        return card
    
    def render_full_report(self) -> str:
        """Generate comprehensive markdown report."""
        report = f"# Assemblage Network: {self.subject_name}\n\n"
        
        # Network overview
        report += "## Network Overview\n\n"
        report += f"**Subject**: {self.subject_name}\n"
        report += f"**Total Assemblages**: {len(self.assemblages)}\n\n"
        
        # Shared elements analysis
        report += "### Shared Components\n"
        shared_comps = self.find_shared_components()
        if shared_comps:
            for comp, asms in shared_comps.items():
                report += f"- **{comp}**: {', '.join(asms)}\n"
        else:
            report += "*No shared components*\n"
        report += "\n"
        
        report += "### Shared Territories\n"
        shared_terrs = self.find_shared_territories()
        if shared_terrs:
            for terr, asms in shared_terrs.items():
                report += f"- **{terr}**: {', '.join(asms)}\n"
        else:
            report += "*No shared territories*\n"
        report += "\n"
        
        report += "### Intensity Conflicts\n"
        conflicts = self.find_intensity_conflicts()
        if conflicts:
            for conflict in conflicts:
                report += f"**{conflict['intensity']}**:\n"
                for asm, val in conflict['assemblages'].items():
                    report += f"  - {asm}: {val:.2f}\n"
                report += "\n"
        else:
            report += "*No significant conflicts*\n"
        report += "\n"
        
        # Transversal Lines of Flight (CONFLICT-BASED)
        report += "### Transversal Lines of Flight (Conflict)\n"
        report += "*Lines of flight from conflicts BETWEEN assemblages*\n\n"
        transversal = self.detect_transversal_lines_of_flight()
        if transversal:
            for lof in transversal:
                report += f"**→ {lof.direction}**\n"
                report += f"- Source: {lof.source_type}\n"
                report += f"- {lof.source_description}\n"
                report += f"- Trigger: {lof.trigger_conditions}\n\n"
        else:
            report += "*No conflict lines detected*\n"
        report += "\n"
        
        # Synergistic Lines of Flight (OPPORTUNITY-BASED)
        report += "### Synergistic Lines of Flight (Opportunity)\n"
        report += "*Lines of flight from COMPOSITION of assemblages - new capacities*\n\n"
        synergistic = self.detect_synergistic_lines_of_flight()
        if synergistic:
            for lof in synergistic:
                report += f"**→ {lof.direction}**\n"
                report += f"- Source: {lof.source_type}\n"
                report += f"- {lof.source_description}\n"
                report += f"- Trigger: {lof.trigger_conditions}\n\n"
        else:
            report += "*No synergistic lines detected*\n"
        report += "\n"
        
        report += "---\n\n"
        
        # Individual assemblage cards
        report += "## Assemblage Details\n\n"
        for asm in self.assemblages:
            report += self.render_assemblage_card(asm)
        
        return report


# =============================================================================
# EXAMPLE NETWORKS
# =============================================================================

def create_example_network() -> AssemblageNetwork:
    """Create a rich example network with overlapping assemblages."""
    from carry.simulation.assemblage import (
    Assemblage, Territory, Code, Component, LineOfFlight, VirtualCapacity
)
    
    # Professional Assemblage
    professional = Assemblage(
        name="Professional-Software-Engineer",
        abstract_machine="(Code + Deadline + Laptop) => (Shipped Product + Status)",
        territories=[
            Territory("Home Office", "Solo coding", "Focused", "striated"),
            Territory("Coffee Shop", "Deep work", "Ambient", "smooth"),
        ],
        codes=[
            Code("Morning standup", "9am daily", "ritual", "molar"),
            Code("Breath-holding while debugging", "Unconscious", "pattern", "molecular"),
        ],
        components=[
            Component("Hands", "organic", "Type, gesture"),
            Component("Laptop", "technical", "Compute, connect"),
            Component("Eyes", "organic", "Read, scan"),
        ],
        intensity_field={"speed": 0.8, "focus": 0.9, "tension": 0.7},
        becoming_vectors=["becoming-expert", "becoming-automated"],
        stratification_depth=0.7,
        lines_of_flight=[
            LineOfFlight(
                direction="Open source collaboration",
                source_type="tension",
                source_description="Stratification 0.7 feels constraining, corporate control conflicts with coding desire",
                trigger_conditions="Encounter with collaborative project or burnout"
            ),
            LineOfFlight(
                direction="Teaching/Mentorship",
                source_type="incompatibility",
                source_description="Accumulating expertise (becoming-expert) but no outlet for transmission",
                trigger_conditions="Junior developer asking for help, or blog post going viral"
            ),
            LineOfFlight(
                direction="Burnout escape",
                source_type="breaking_point",
                source_description="Speed 0.8 + Tension 0.7 + Stratification 0.7 creates unsustainable intensity",
                trigger_conditions="Health crisis, relationship breakdown, or deadline failure"
            )
        ],
        virtual_capacities=[
            VirtualCapacity(
                name="Management track",
                access_point="Senior developer status + 5 years tenure",
                reason_unactualized="No encounter with leadership opportunity, enjoys coding more",
                actualization_trigger="Manager quits, team growth forces decision"
            ),
            VirtualCapacity(
                name="AI/ML specialization",
                access_point="Python fluency + mathematical background",
                reason_unactualized="Current work is web dev, no trigger to pivot",
                actualization_trigger="Company AI initiative or personal curiosity encounter"
            ),
            VirtualCapacity(
                name="Startup founding",
                access_point="Technical skills + network + domain knowledge",
                reason_unactualized="Risk aversion, stable salary more attractive",
                actualization_trigger="Savings threshold reached or co-founder encounter"
            )
        ]
    )
    
    # Creative Assemblage
    creative = Assemblage(
        name="Creative-Writer",
        abstract_machine="(Observation + Solitude + Notebook) => (Story + Insight)",
        territories=[
            Territory("Coffee Shop", "Observing people", "Curious", "smooth"),
            Territory("Park Bench", "Reflection", "Meditative", "smooth"),
        ],
        codes=[
            Code("Morning pages", "Every morning", "ritual", "molar"),
            Code("Subliminal character voices", "Unconscious", "pattern", "molecular"),
        ],
        components=[
            Component("Hands", "organic", "Write, sketch"),
            Component("Notebook", "technical", "Capture thoughts"),
            Component("Eyes", "organic", "Observe, imagine"),
        ],
        intensity_field={"speed": 0.3, "focus": 0.8, "openness": 0.9},
        becoming_vectors=["becoming-observer", "becoming-storyteller"],
        stratification_depth=0.3,
        lines_of_flight=[
            LineOfFlight(
                direction="Publication",
                source_type="tension",
                source_description="Stories accumulating in notebooks but no audience, becoming-storyteller needs listeners",
                trigger_conditions="Writer's group invitation or contest deadline"
            ),
            LineOfFlight(
                direction="Performance/Podcast",
                source_type="incompatibility",
                source_description="Smooth observational space creates desire to break solitude, Coffee Shop watching wants interaction",
                trigger_conditions="Open mic invitation or recording equipment access"
            )
        ],
        virtual_capacities=[
            VirtualCapacity(
                name="Screenwriting",
                access_point="Narrative skills + visual imagination",
                reason_unactualized="Never encountered film medium, stuck in prose",
                actualization_trigger="Film festival attendance or screenwriting workshop"
            ),
            VirtualCapacity(
                name="Journalism",
                access_point="Observational capacity + writing skills",
                reason_unactualized="No outlet or commission, observes but doesn't report",
                actualization_trigger="Local paper solicitation or niche blog opportunity"
            )
        ]
    )
    
    # Athletic Assemblage  
    athletic = Assemblage(
        name="Weekend-Runner",
        abstract_machine="(Trail + Rhythm + Body) => (Endorphins + Clarity)",
        territories=[
            Territory("Park Trail", "Running", "Free", "smooth"),
        ],
        codes=[
            Code("Saturday morning run", "Every Sat 7am", "ritual", "molar"),
            Code("Breathing sync with footfall", "Automatic", "pattern", "molecular"),
        ],
        components=[
            Component("Legs", "organic", "Run, stabilize"),
            Component("Lungs", "organic", "Oxygenate"),
            Component("Eyes", "organic", "Navigate terrain"),
        ],
        intensity_field={"speed": 0.6, "energy": 0.9, "pain": 0.4},
        becoming_vectors=["becoming-stronger", "becoming-rhythmic"],
        stratification_depth=0.4,
        lines_of_flight=[
            LineOfFlight(
                direction="Trail racing",
                source_type="tension",
                source_description="Energy 0.9 + becoming-stronger exceeds recreational frame, solo running feels insufficient",
                trigger_conditions="Encounter with race flyer or running group"
            ),
            LineOfFlight(
                direction="Running community",
                source_type="incompatibility",
                source_description="Smooth solo practice conflicts with desire for shared rhythm, social body missing",
                trigger_conditions="Friend invitation to group run"
            )
        ],
        virtual_capacities=[
            VirtualCapacity(
                name="Marathon training",
                access_point="Weekly running habit + cardiovascular base",
                reason_unactualized="Never committed to structured program, recreational frame sufficient",
                actualization_trigger="Marathon registration or running buddy challenge"
            ),
            VirtualCapacity(
                name="Running group leadership",
                access_point="Trail knowledge + regular practice",
                reason_unactualized="Solo practice, no social connection to running community",
                actualization_trigger="Group formation opportunity or mentor request"
            )
        ]
    )
    
    return AssemblageNetwork("Alex", [professional, creative, athletic])


if __name__ == "__main__":
    network = create_example_network()
    
    print("=== GENERATING COMPREHENSIVE ASSEMBLAGE REPORT ===\n")
    
    # Generate full report
    full_report = network.render_full_report()
    
    # Save to file
    with open("carry/results/full_assemblage_report.md", "w") as f:
        f.write(full_report)
    
    print(f"Saved comprehensive report to: carry/results/full_assemblage_report.md")
    
    # Also save JSON network WITH FUTURES
    with open("carry/results/example_network.json", "w") as f:
        json.dump(network.to_json_network_with_futures(), f, indent=2)
    
    print(f"Saved network JSON (with futures) to: carry/results/example_network.json")
    
    print("\n" + "="*60)
    print(full_report[:2000] + "\n...\n(Full report saved to file)")
