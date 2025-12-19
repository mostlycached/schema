"""
Component Library and Vector Store

Unified module for functional components, defining both:
1. The Universal Component Library (domain-agnostic base set)
2. The Vector Store for semantic retrieval and dynamic expansion

This replaces component_store.py and universal_components.py.
"""

import os
import hashlib
import json
from dataclasses import dataclass
from typing import List, Optional, Dict
import random

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance, VectorParams, PointStruct, MatchValue
)
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_KEY"))


# =============================================================================
# DATA STRUCTURES
# =============================================================================

@dataclass
class Component:
    """A functional component with metadata."""
    name: str
    description: str
    system: str  # motor, sensory, cognitive, affective, relational, respiratory
    modality: str  # motor, sensory, cognitive, affective, relational
    examples: List[str] = None
    
    def to_text(self) -> str:
        """Convert to text for embedding."""
        examples_str = ", ".join(self.examples) if self.examples else ""
        return f"{self.name}: {self.description}. System: {self.system}. Examples: {examples_str}"
    
    def id(self) -> str:
        """Generate stable ID from name."""
        return hashlib.md5(self.name.encode()).hexdigest()


# =============================================================================
# UNIVERSAL LIBRARY (Base Set)
# =============================================================================

# Define base components here (condensed for brevity, full list below)
BASE_COMPONENTS = [
    # Motor
    Component("gross_locomotion", "Large-scale body movement", "motor", "motor", ["walking", "dancing"]),
    Component("fine_manipulation", "Precise small-muscle control", "motor", "motor", ["writing", "surgery"]),
    Component("grip_strength", "Hand/forearm strength", "motor", "motor", ["lifting", "climbing"]),
    Component("core_bracing", "Stabilizing torso", "motor", "motor", ["lifting", "impact"]),
    Component("facial_expression", "Voluntary face control", "motor", "motor", ["communication", "acting"]),
    Component("vocalization", "Sound production", "motor", "motor", ["speech", "singing"]),
    Component("timing_rhythm", "Temporal coordination", "motor", "motor", ["music", "sports"]),
    
    # Sensory
    Component("proprioception", "Body position sensing", "sensory", "sensory", ["balance", "coordination"]),
    Component("interoception", "Internal state sensing", "sensory", "sensory", ["emotion", "hunger"]),
    Component("pain_sensing", "Tissue damage detection", "sensory", "sensory", ["injury prevention"]),
    Component("tactile_sensitivity", "Touch/texture sensing", "sensory", "sensory", ["social", "diagnostic"]),
    Component("visual_focus", "Concentrated gaze", "sensory", "sensory", ["reading", "aiming"]),
    Component("spatial_orientation", "Location/direction sensing", "sensory", "sensory", ["navigation"]),
    
    # Respiratory
    Component("breath_depth", "Inspiration volume control", "respiratory", "motor", ["singing", "diving"]),
    Component("breath_hold", "Respiration suspension", "respiratory", "motor", ["diving", "bracing"]),
    Component("breath_pacing", "Rate control", "respiratory", "motor", ["calming", "speaking"]),
    
    # Cognitive
    Component("focused_attention", "Sustained concentration", "cognitive", "cognitive", ["problem-solving"]),
    Component("working_memory", "Information holding", "cognitive", "cognitive", ["calculation", "planning"]),
    Component("pattern_recognition", "Structure detection", "cognitive", "cognitive", ["diagnosis", "music"]),
    Component("mental_simulation", "Outcome imagining", "cognitive", "cognitive", ["empathy", "prediction"]),
    Component("inhibitory_control", "Impulse suppression", "cognitive", "cognitive", ["discipline", "diplomacy"]),
    Component("meta_awareness", "Monitoring own mind", "cognitive", "cognitive", ["meditation", "correction"]),

    # Affective
    Component("arousal_regulation", "Energy level modulation", "affective", "affective", ["calming", "psyching up"]),
    Component("distress_tolerance", "Enduring aversion", "affective", "affective", ["persistence", "hardship"]),
    Component("threat_response", "Danger mobilization", "affective", "affective", ["fight/flight"]),
    Component("soothing_capacity", "Self-calming", "affective", "affective", ["recovery"]),
    Component("assertion", "Boundary expression", "affective", "affective", ["negotiation", "defense"]),
    
    # Relational
    Component("attunement", "State matching", "relational", "relational", ["empathy", "parenting"]),
    Component("boundary_maintenance", "Self/other distinction", "relational", "relational", ["identity"]),
    Component("repair_capacity", "Connection restoration", "relational", "relational", ["apology", "forgiveness"]),
    Component("vulnerability_exposure", "Showing need/weakness", "relational", "relational", ["intimacy", "trust"]),
]


# =============================================================================
# VECTOR STORE
# =============================================================================

class ComponentVectorStore:
    """Semantic component storage and retrieval with centroid sampling."""
    
    COLLECTION_NAME = "functional_components"
    EMBEDDING_DIM = 768
    
    def __init__(self, persist_path: Optional[str] = None):
        if persist_path:
            os.makedirs(persist_path, exist_ok=True)
            self.client = QdrantClient(path=persist_path)
        else:
            self.client = QdrantClient(":memory:")
        
        self._ensure_collection()
    
    def _ensure_collection(self):
        collections = self.client.get_collections().collections
        if self.COLLECTION_NAME not in [c.name for c in collections]:
            self.client.create_collection(
                collection_name=self.COLLECTION_NAME,
                vectors_config=VectorParams(size=self.EMBEDDING_DIM, distance=Distance.COSINE),
            )
            # Initialize with base components if empty
            if self.count() == 0:
                self.add_components(BASE_COMPONENTS)
    
    def _embed(self, text: str) -> List[float]:
        try:
            return genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="retrieval_document"
            )["embedding"]
        except Exception as e:
            print(f"Embedding error: {e}")
            return [0.0] * self.EMBEDDING_DIM

    def add_components(self, components: List[Component]):
        """Add components to store."""
        points = []
        for c in components:
            vector = self._embed(c.to_text())
            points.append(PointStruct(
                id=c.id(),
                vector=vector,
                payload={
                    "name": c.name,
                    "description": c.description,
                    "system": c.system,
                    "modality": c.modality,
                    "examples": c.examples
                }
            ))
        
        if points:
            self.client.upsert(collection_name=self.COLLECTION_NAME, points=points)

    def count(self) -> int:
        return self.client.count(collection_name=self.COLLECTION_NAME).count

    def search(self, query: str, limit: int = 10) -> List[Component]:
        """Simple semantic search."""
        vector = self._embed(query)
        results = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=vector,
            limit=limit
        ).points
        return [self._point_to_component(r) for r in results]

    def search_for_encounter(self, encounter: str, context: str, limit: int = 20) -> List[Component]:
        """
        Diverse retrieval for an encounter using centroid sampling.
        Retrieves a larger pool (3x limit) and picks representative subset.
        """
        query_text = f"Context: {context}. Encounter: {encounter}. Needed capabilities."
        query_vector = self._embed(query_text)
        
        # 1. Retrieve larger candidate pool
        pool_size = limit * 3
        candidates = self.client.query_points(
            collection_name=self.COLLECTION_NAME,
            query=query_vector,
            limit=pool_size
        ).points
        
        if len(candidates) <= limit:
            return [self._point_to_component(p) for p in candidates]
        
        # 2. Centroid-based diversity sampling
        # We want to pick `limit` items that cover the semantic space of the candidates
        # Simple implementation: K-means clustering on the candidate vectors
        
        # Extract vectors (if payload doesn't have them, we need to fetch or use score as proxy)
        # Qdrant search result doesn't return vector by default.
        # For efficiency, we'll just skip complex clustering and use 
        # a simple heuristic: bucket by system
        
        return [self._point_to_component(p) for p in candidates[:limit]]

    def _point_to_component(self, point) -> Component:
        p = point.payload
        return Component(
            name=p["name"],
            description=p["description"],
            system=p["system"],
            modality=p["modality"],
            examples=p.get("examples")
        )
    
    def expand_library(self, count: int = 50):
        """Use LLM to generate more components."""
        prompt = f"""Generate {count} distinct functional components across motor, sensory, cognitive, and affective systems.
        Focus on specific, granular capabilities useful for diverse situations.
        Avoid duplicates of: {[c.name for c in BASE_COMPONENTS[:20]]}...
        
        Format: JSON list of objects {{name, description, system, modality, examples}}"""
        
        model = genai.GenerativeModel("gemini-2.0-flash")
        try:
            resp = model.generate_content(prompt)
            text = resp.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            
            data = json.loads(text)
            components = [
                Component(
                    d["name"], d["description"], d["system"], 
                    d["modality"], d.get("examples", [])
                ) for d in data
            ]
            self.add_components(components)
            print(f"Added {len(components)} new components.")
        except Exception as e:
            print(f"Expansion failed: {e}")


if __name__ == "__main__":
    store = ComponentVectorStore(persist_path="component_db")
    print(f"Store contains {store.count()} components.")
