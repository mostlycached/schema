"""
Graph representation for memoir scenes.

This module provides data structures and operations for representing
memoir scenes as a directed graph with multiple node and edge types.
"""

import json
import yaml
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, field, asdict
from pathlib import Path
from datetime import datetime
import uuid


@dataclass
class Node:
    """Base class for graph nodes."""
    node_id: str = ""
    node_type: str = ""  # "scene", "world", "actor"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SceneNode(Node):
    """Node representing a memoir scene."""
    scene_id: str = ""
    title: str = ""
    date: str = ""
    location: str = ""
    tags: List[str] = field(default_factory=list)
    data: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self.node_type = "scene"
        if not self.node_id:
            self.node_id = self.scene_id or str(uuid.uuid4())
        if not self.scene_id:
            self.scene_id = self.node_id


@dataclass
class WorldNode(Node):
    """Node representing a world from WORLDS.md."""
    world_id: str = ""
    world_name: str = ""
    world_type: str = ""  # "novel" or "long-lasting"
    
    def __post_init__(self):
        self.node_type = "world"
        if not self.node_id:
            self.node_id = self.world_id or str(uuid.uuid4())


@dataclass
class ActorNode(Node):
    """Node representing an actor/inhabitant across scenes."""
    actor_id: str = ""
    name: str = ""
    roles: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        self.node_type = "actor"
        if not self.node_id:
            self.node_id = self.actor_id or str(uuid.uuid4())


@dataclass
class Edge:
    """Directed edge between nodes."""
    edge_id: str
    edge_type: str  # "temporal", "causal", "similar", "intersection", "opposition"
    source: str  # node_id
    target: str  # node_id
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class MemoirGraph:
    """
    Graph representation of memoir scenes and their relationships.
    
    Supports multiple node types (scenes, worlds, actors) and edge types
    (temporal, causal, similarity, intersection, opposition).
    """
    
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
        self.edges: Dict[str, Edge] = {}
        
    def add_node(self, node: Node) -> None:
        """Add a node to the graph."""
        self.nodes[node.node_id] = node
        
    def remove_node(self, node_id: str) -> None:
        """Remove a node and all its connected edges."""
        if node_id in self.nodes:
            del self.nodes[node_id]
        # Remove all edges connected to this node
        edges_to_remove = [
            edge_id for edge_id, edge in self.edges.items()
            if edge.source == node_id or edge.target == node_id
        ]
        for edge_id in edges_to_remove:
            del self.edges[edge_id]
            
    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph."""
        # Validate that both nodes exist
        if edge.source not in self.nodes:
            raise ValueError(f"Source node {edge.source} does not exist")
        if edge.target not in self.nodes:
            raise ValueError(f"Target node {edge.target} does not exist")
        self.edges[edge.edge_id] = edge
        
    def remove_edge(self, edge_id: str) -> None:
        """Remove an edge from the graph."""
        if edge_id in self.edges:
            del self.edges[edge_id]
            
    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node by its ID."""
        return self.nodes.get(node_id)
    
    def get_edges_from(self, node_id: str, edge_type: Optional[str] = None) -> List[Edge]:
        """Get all edges originating from a node, optionally filtered by type."""
        edges = [e for e in self.edges.values() if e.source == node_id]
        if edge_type:
            edges = [e for e in edges if e.edge_type == edge_type]
        return edges
    
    def get_edges_to(self, node_id: str, edge_type: Optional[str] = None) -> List[Edge]:
        """Get all edges pointing to a node, optionally filtered by type."""
        edges = [e for e in self.edges.values() if e.target == node_id]
        if edge_type:
            edges = [e for e in edges if e.edge_type == edge_type]
        return edges
    
    def get_neighbors(self, node_id: str, direction: str = "both") -> Set[str]:
        """
        Get neighboring node IDs.
        
        Args:
            node_id: The node to find neighbors for
            direction: "outgoing", "incoming", or "both"
        """
        neighbors = set()
        
        if direction in ["outgoing", "both"]:
            neighbors.update(e.target for e in self.get_edges_from(node_id))
        
        if direction in ["incoming", "both"]:
            neighbors.update(e.source for e in self.get_edges_to(node_id))
            
        return neighbors
    
    def get_temporal_sequence(self) -> List[SceneNode]:
        """Get all scene nodes sorted by date."""
        scene_nodes = [
            n for n in self.nodes.values() 
            if isinstance(n, SceneNode) and n.date
        ]
        return sorted(scene_nodes, key=lambda n: n.date)
    
    def find_scenes_by_tag(self, tag: str) -> List[SceneNode]:
        """Find all scenes with a specific tag."""
        return [
            n for n in self.nodes.values()
            if isinstance(n, SceneNode) and tag in n.tags
        ]
    
    def find_scenes_by_world(self, world_id: str) -> List[SceneNode]:
        """Find all scenes connected to a specific world."""
        scene_ids = {
            e.source for e in self.edges.values()
            if e.edge_type == "intersection" and e.target == world_id
        }
        return [
            self.nodes[sid] for sid in scene_ids
            if isinstance(self.nodes[sid], SceneNode)
        ]
    
    def detect_intersections(self, scene_id: str, worlds_data: Dict[str, Any]) -> List[str]:
        """
        Detect which worlds from WORLDS.md a scene intersects with.
        
        This is a heuristic-based matching using keywords and patterns.
        Returns list of world names that likely apply.
        """
        scene = self.get_node(scene_id)
        if not isinstance(scene, SceneNode):
            return []
        
        # Simple keyword matching for now
        # In a real implementation, this could use embeddings or LLM classification
        matches = []
        scene_text = json.dumps(scene.data).lower()
        
        for world_name, world_info in worlds_data.items():
            # Check if world characteristics appear in scene
            keywords = self._extract_keywords(world_info)
            if any(kw.lower() in scene_text for kw in keywords):
                matches.append(world_name)
        
        return matches
    
    def _extract_keywords(self, world_info: Dict[str, Any]) -> List[str]:
        """Extract keywords from world definition for matching."""
        keywords = []
        if isinstance(world_info, dict):
            # Extract from inhabitants, phenomenology, etc.
            for value in world_info.values():
                if isinstance(value, str):
                    keywords.extend(value.split())
        return keywords[:10]  # Limit to avoid over-matching
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get graph statistics."""
        scene_count = sum(1 for n in self.nodes.values() if n.node_type == "scene")
        world_count = sum(1 for n in self.nodes.values() if n.node_type == "world")
        actor_count = sum(1 for n in self.nodes.values() if n.node_type == "actor")
        
        edge_types = {}
        for edge in self.edges.values():
            edge_types[edge.edge_type] = edge_types.get(edge.edge_type, 0) + 1
        
        return {
            "total_nodes": len(self.nodes),
            "scenes": scene_count,
            "worlds": world_count,
            "actors": actor_count,
            "total_edges": len(self.edges),
            "edge_types": edge_types
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Export graph to dictionary format."""
        return {
            "nodes": [node.to_dict() for node in self.nodes.values()],
            "edges": [edge.to_dict() for edge in self.edges.values()]
        }
    
    def to_json(self, filepath: Path) -> None:
        """Export graph to JSON file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    def to_graphml(self, filepath: Path) -> None:
        """Export graph to GraphML format for visualization tools."""
        # GraphML XML generation
        lines = ['<?xml version="1.0" encoding="UTF-8"?>']
        lines.append('<graphml xmlns="http://graphml.graphdrawing.org/xmlns">')
        lines.append('  <graph id="memoir" edgedefault="directed">')
        
        # Add nodes
        for node in self.nodes.values():
            lines.append(f'    <node id="{node.node_id}">')
            lines.append(f'      <data key="type">{node.node_type}</data>')
            if isinstance(node, SceneNode):
                lines.append(f'      <data key="title">{node.title}</data>')
            lines.append('    </node>')
        
        # Add edges
        for edge in self.edges.values():
            lines.append(f'    <edge source="{edge.source}" target="{edge.target}">')
            lines.append(f'      <data key="type">{edge.edge_type}</data>')
            lines.append('    </edge>')
        
        lines.append('  </graph>')
        lines.append('</graphml>')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    def to_dot(self, filepath: Path) -> None:
        """Export graph to DOT format for Graphviz."""
        lines = ['digraph memoir {']
        lines.append('  rankdir=LR;')
        lines.append('  node [shape=box];')
        
        # Add nodes with labels
        for node in self.nodes.values():
            label = node.node_id
            if isinstance(node, SceneNode):
                label = node.title or node.scene_id
            lines.append(f'  "{node.node_id}" [label="{label}"];')
        
        # Add edges
        for edge in self.edges.values():
            style = ""
            if edge.edge_type == "temporal":
                style = ' [color=blue]'
            elif edge.edge_type == "causal":
                style = ' [color=red]'
            lines.append(f'  "{edge.source}" -> "{edge.target}"{style};')
        
        lines.append('}')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MemoirGraph':
        """Load graph from dictionary format."""
        graph = cls()
        
        # Load nodes
        for node_data in data.get('nodes', []):
            node_type = node_data['node_type']
            if node_type == 'scene':
                node = SceneNode(**node_data)
            elif node_type == 'world':
                node = WorldNode(**node_data)
            elif node_type == 'actor':
                node = ActorNode(**node_data)
            else:
                node = Node(**node_data)
            graph.add_node(node)
        
        # Load edges
        for edge_data in data.get('edges', []):
            edge = Edge(**edge_data)
            graph.add_edge(edge)
        
        return graph
    
    @classmethod
    def from_json(cls, filepath: Path) -> 'MemoirGraph':
        """Load graph from JSON file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)


if __name__ == "__main__":
    # Example usage
    graph = MemoirGraph()
    
    # Add a scene node
    scene1 = SceneNode(
        scene_id="scene1",
        title="Morning Commute",
        date="2024-01-15",
        location="NYC Subway",
        tags=["commute", "transit"],
        data={"phenomenology": {"emotional_tone": "anxiety"}}
    )
    graph.add_node(scene1)
    
    # Add another scene
    scene2 = SceneNode(
        scene_id="scene2",
        title="Lunch Break",
        date="2024-01-15",
        location="Office Cafeteria",
        tags=["work", "food"]
    )
    graph.add_node(scene2)
    
    # Add a temporal edge
    edge = Edge(
        edge_id="e1",
        edge_type="temporal",
        source="scene1",
        target="scene2",
        metadata={"direction": "before"}
    )
    graph.add_edge(edge)
    
    # Print statistics
    print("Graph Statistics:")
    stats = graph.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
