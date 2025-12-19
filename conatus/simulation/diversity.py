"""
MAP-Elites Stance Archive

Implements Quality-Diversity algorithms for stance generation:
1. MAP-Elites: Maintains archive of elites across behavioral feature space
2. Semantic Distance: Requires new stances to be sufficiently different

This prevents mode collapse where the LLM generates the same stance repeatedly.
"""

import os
import json
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
import numpy as np

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))


# =============================================================================
# BEHAVIORAL FEATURE SPACE
# =============================================================================

@dataclass
class BehavioralDescriptor:
    """
    Position in behavioral feature space.
    Each dimension is 0.0 to 1.0.
    """
    # Physical vs Cognitive focus
    physical_cognitive: float = 0.5
    
    # Individual vs Social orientation
    individual_social: float = 0.5
    
    # Reactive vs Proactive mode
    reactive_proactive: float = 0.5
    
    # Defensive vs Assertive posture
    defensive_assertive: float = 0.5
    
    def to_vector(self) -> np.ndarray:
        return np.array([
            self.physical_cognitive,
            self.individual_social,
            self.reactive_proactive,
            self.defensive_assertive,
        ])
    
    def distance_to(self, other: 'BehavioralDescriptor') -> float:
        """Euclidean distance in feature space."""
        return float(np.linalg.norm(self.to_vector() - other.to_vector()))
    
    def cell_index(self, resolution: int = 3) -> Tuple[int, ...]:
        """Get discrete cell index for MAP-Elites grid."""
        vec = self.to_vector()
        indices = tuple(min(int(v * resolution), resolution - 1) for v in vec)
        return indices


@dataclass  
class ArchivedStance:
    """A stance stored in the archive with its behavioral descriptor."""
    name: str
    description: str
    affect_register: str
    components: List[str]
    descriptor: BehavioralDescriptor
    embedding: Optional[List[float]] = None
    fitness: float = 0.0  # Super-ego score or viability
    encounter_context: str = ""


# =============================================================================
# MAP-ELITES ARCHIVE
# =============================================================================

class StanceArchive:
    """
    MAP-Elites archive for diverse stance generation.
    
    Maintains a grid of behavioral niches, storing the best stance
    found for each niche. New stances must either:
    1. Fill an empty niche, OR
    2. Outperform the existing elite in that niche
    
    Additionally enforces semantic distance requirements.
    """
    
    def __init__(
        self,
        resolution: int = 3,
        min_semantic_distance: float = 0.15,
    ):
        """
        Args:
            resolution: Grid resolution per dimension (3 = 3^4 = 81 cells)
            min_semantic_distance: Minimum cosine distance from existing stances
        """
        self.resolution = resolution
        self.min_semantic_distance = min_semantic_distance
        
        # MAP-Elites grid: cell_index -> ArchivedStance
        self.grid: Dict[Tuple[int, ...], ArchivedStance] = {}
        
        # All stances for semantic distance checking
        self.all_stances: List[ArchivedStance] = []
        
        self.model = genai.GenerativeModel("gemini-2.0-flash")
    
    def _embed(self, text: str) -> List[float]:
        """Get embedding for semantic similarity."""
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="semantic_similarity",
        )
        return result['embedding']
    
    def _compute_descriptor(self, stance_desc: str, components: List[str]) -> BehavioralDescriptor:
        """Use LLM to compute behavioral descriptor for a stance."""
        prompt = f"""Analyze this stance and rate it on 4 behavioral dimensions (0.0 to 1.0):

STANCE: {stance_desc}
COMPONENTS: {', '.join(components)}

Rate each dimension:
1. physical_cognitive: 0.0 = purely physical/motor, 1.0 = purely cognitive/mental
2. individual_social: 0.0 = self-focused, 1.0 = other-focused/relational
3. reactive_proactive: 0.0 = defensive/reactive, 1.0 = initiating/proactive
4. defensive_assertive: 0.0 = protective/cautious, 1.0 = assertive/bold

Respond ONLY with JSON:
{{"physical_cognitive": 0.X, "individual_social": 0.X, "reactive_proactive": 0.X, "defensive_assertive": 0.X}}"""

        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.2,
                    max_output_tokens=200,
                )
            )
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            data = json.loads(text)
            return BehavioralDescriptor(
                physical_cognitive=float(data.get("physical_cognitive", 0.5)),
                individual_social=float(data.get("individual_social", 0.5)),
                reactive_proactive=float(data.get("reactive_proactive", 0.5)),
                defensive_assertive=float(data.get("defensive_assertive", 0.5)),
            )
        except Exception as e:
            print(f"Descriptor error: {e}")
            return BehavioralDescriptor()  # Default center
    
    def _cosine_distance(self, a: List[float], b: List[float]) -> float:
        """Compute cosine distance (1 - cosine_similarity)."""
        a_arr = np.array(a)
        b_arr = np.array(b)
        similarity = np.dot(a_arr, b_arr) / (np.linalg.norm(a_arr) * np.linalg.norm(b_arr))
        return 1.0 - similarity
    
    def check_novelty(self, stance_text: str) -> Tuple[bool, float, Optional[str]]:
        """
        Check if a stance is sufficiently novel.
        
        Returns:
            (is_novel, min_distance, most_similar_stance_name)
        """
        if not self.all_stances:
            return True, 1.0, None
        
        embedding = self._embed(stance_text)
        
        min_dist = float('inf')
        most_similar = None
        
        for archived in self.all_stances:
            if archived.embedding is not None:
                dist = self._cosine_distance(embedding, archived.embedding)
                if dist < min_dist:
                    min_dist = dist
                    most_similar = archived.name
        
        is_novel = min_dist >= self.min_semantic_distance
        return is_novel, min_dist, most_similar
    
    def try_add(
        self,
        name: str,
        description: str,
        affect_register: str,
        components: List[str],
        fitness: float,
        encounter_context: str = "",
    ) -> Tuple[bool, str]:
        """
        Try to add a stance to the archive.
        
        Returns:
            (success, reason)
        """
        stance_text = f"{name}: {description}"
        
        # Check semantic novelty
        is_novel, distance, similar_to = self.check_novelty(stance_text)
        if not is_novel:
            return False, f"Too similar to '{similar_to}' (distance={distance:.3f}, min={self.min_semantic_distance})"
        
        # Compute behavioral descriptor
        descriptor = self._compute_descriptor(description, components)
        cell = descriptor.cell_index(self.resolution)
        
        # Get embedding
        embedding = self._embed(stance_text)
        
        archived = ArchivedStance(
            name=name,
            description=description,
            affect_register=affect_register,
            components=components,
            descriptor=descriptor,
            embedding=embedding,
            fitness=fitness,
            encounter_context=encounter_context,
        )
        
        # MAP-Elites: check if cell is empty or new stance is better
        if cell not in self.grid:
            self.grid[cell] = archived
            self.all_stances.append(archived)
            return True, f"Added to new niche {cell}"
        
        existing = self.grid[cell]
        if fitness > existing.fitness:
            self.grid[cell] = archived
            self.all_stances.append(archived)
            return True, f"Replaced '{existing.name}' in niche {cell} (fitness {existing.fitness:.2f} -> {fitness:.2f})"
        
        # Still add to all_stances for semantic checking, but not to grid
        self.all_stances.append(archived)
        return False, f"Niche {cell} already has better elite '{existing.name}' (fitness={existing.fitness:.2f})"
    
    def get_used_stance_names(self) -> List[str]:
        """Get list of all stance names in archive."""
        return [s.name for s in self.all_stances]
    
    def get_negative_prompt(self) -> str:
        """Generate prompt text listing stances to avoid."""
        if not self.all_stances:
            return ""
        
        names = self.get_used_stance_names()
        return f"\n\nDO NOT propose any of these stances (already used):\n- " + "\n- ".join(names)
    
    def get_diversity_guidance(self) -> str:
        """Generate prompt guidance based on archive coverage."""
        if not self.grid:
            return ""
        
        # Find underrepresented regions
        covered_cells = set(self.grid.keys())
        total_cells = self.resolution ** 4
        coverage = len(covered_cells) / total_cells
        
        guidance = f"\n\nARCHIVE STATUS: {len(covered_cells)}/{total_cells} behavioral niches filled ({coverage:.0%})"
        
        # Suggest underrepresented directions
        if covered_cells:
            avg_descriptor = np.mean([
                self.grid[c].descriptor.to_vector() for c in covered_cells
            ], axis=0)
            
            if avg_descriptor[0] > 0.6:
                guidance += "\n→ Consider MORE PHYSICAL stances (current bias: cognitive)"
            elif avg_descriptor[0] < 0.4:
                guidance += "\n→ Consider MORE COGNITIVE stances (current bias: physical)"
            
            if avg_descriptor[1] > 0.6:
                guidance += "\n→ Consider MORE INDIVIDUAL-FOCUSED stances (current bias: social)"
            elif avg_descriptor[1] < 0.4:
                guidance += "\n→ Consider MORE SOCIAL stances (current bias: individual)"
            
            if avg_descriptor[2] > 0.6:
                guidance += "\n→ Consider MORE REACTIVE stances (current bias: proactive)"
            elif avg_descriptor[2] < 0.4:
                guidance += "\n→ Consider MORE PROACTIVE stances (current bias: reactive)"
        
        return guidance
    
    def get_summary(self) -> Dict:
        """Get archive summary."""
        total_cells = self.resolution ** 4
        return {
            "total_stances": len(self.all_stances),
            "grid_coverage": len(self.grid),
            "total_cells": total_cells,
            "coverage_pct": len(self.grid) / total_cells,
            "stance_names": self.get_used_stance_names(),
        }


# =============================================================================
# INTEGRATION WITH STANCE GENERATION
# =============================================================================

def generate_novel_stance(
    model: genai.GenerativeModel,
    archive: StanceArchive,
    encounter: str,
    context: str,
    active_components: List[str],
    dormant_components: List[str],
    max_attempts: int = 5,
    rejected_names: List[str] = None,
) -> Optional[Dict]:
    """
    Generate a stance that is guaranteed to be novel.
    
    Uses archive's negative prompt and diversity guidance to push
    the LLM toward unexplored behavioral regions.
    
    Args:
        rejected_names: Additional stance names to avoid (from current step's rejections)
    """
    negative_prompt = archive.get_negative_prompt()
    diversity_guidance = archive.get_diversity_guidance()
    
    # Add step-specific rejections
    if rejected_names:
        negative_prompt += f"\n\nALSO DO NOT propose these (rejected this step):\n- " + "\n- ".join(rejected_names)
    
    active_desc = "\n".join([f"- {c}" for c in active_components])
    dormant_desc = "\n".join([f"- {c}" for c in dormant_components])
    
    for attempt in range(max_attempts):
        prompt = f"""Generate a NOVEL stance for this agent facing a challenge.

CONTEXT: {context}
ENCOUNTER: {encounter}

ACTIVE COMPONENTS (can be reduced):
{active_desc}

DORMANT COMPONENTS (can be activated):
{dormant_desc}
{negative_prompt}
{diversity_guidance}

CRITICAL: Your stance must be SEMANTICALLY DIFFERENT from previously used stances.
The stance will be rejected if it is too similar to existing ones.

Generate a stance with:
1. A UNIQUE name (not similar to used names)
2. A description of what it CAN DO
3. Component activation/inhibition
4. An affect register

Respond in JSON:
{{
  "name": "<unique stance name>",
  "description": "<what this stance enables>",
  "components_active": ["<component names>"],
  "affect_register": "<the felt-sense>"
}}"""

        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.8,  # Higher for diversity
                    max_output_tokens=500,
                )
            )
            
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            data = json.loads(text)
            
            # Check novelty before returning
            stance_text = f"{data['name']}: {data['description']}"
            is_novel, distance, similar = archive.check_novelty(stance_text)
            
            if is_novel:
                return data
            else:
                print(f"  Attempt {attempt+1}: Too similar to '{similar}' (d={distance:.3f})")
                
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
    
    return None


# =============================================================================
# TEST
# =============================================================================

if __name__ == "__main__":
    print("Testing MAP-Elites Stance Archive")
    print("=" * 60)
    
    archive = StanceArchive(resolution=3, min_semantic_distance=0.15)
    
    # Add some test stances
    test_stances = [
        ("Primal Surge", "Maximal physical power output overriding caution", "Explosive Force", ["grip_strength", "core_bracing"]),
        ("Analytical Patience", "Slow methodical problem-solving with careful observation", "Calm Precision", ["focused_attention", "pattern_recognition"]),  
        ("Social Shield", "Using group dynamics and others' support for protection", "Collective Strength", ["attunement", "turn_taking"]),
        ("Adaptive Flow", "Flexible response adapting to changing circumstances", "Fluid Readiness", ["proprioception", "arousal_regulation"]),
    ]
    
    for name, desc, affect, comps in test_stances:
        success, reason = archive.try_add(
            name=name,
            description=desc,
            affect_register=affect,
            components=comps,
            fitness=0.7,
        )
        print(f"{'✓' if success else '✗'} {name}: {reason}")
    
    print("\n" + "=" * 60)
    print("ARCHIVE SUMMARY")
    print(json.dumps(archive.get_summary(), indent=2))
    
    print("\n" + "=" * 60)
    print("DIVERSITY GUIDANCE")
    print(archive.get_diversity_guidance())
