"""
Memoir repository manager.

Handles interaction with the private memoir repository, including
initializing the repo structure, loading and saving scenes, and
maintaining privacy boundaries.
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

from graph import MemoirGraph, SceneNode, Edge


class MemoirRepo:
    """
    Manages the private memoir repository.
    
    The memoir repo contains personal scene data and should never be
    committed to the public schema repository.
    """
    
    def __init__(self, repo_path: Optional[str] = None):
        """
        Initialize memoir repository manager.
        
        Args:
            repo_path: Path to memoir repo. If None, reads from .env file.
        """
        if repo_path is None:
            repo_path = self._load_from_env()
        
        self.repo_path = Path(repo_path).expanduser().resolve()
        self.scenes_dir = self.repo_path / "scenes"
        self.graphs_dir = self.repo_path / "graphs"
        self.index_file = self.repo_path / "index.yaml"
        
        # Ensure we're not accidentally writing to the schema repo
        self._validate_path()
    
    def _load_from_env(self) -> str:
        """Load memoir repo path from .env file."""
        env_file = Path(__file__).parent.parent / ".env"
        
        if not env_file.exists():
            raise FileNotFoundError(
                f"No .env file found at {env_file}. "
                "Please create one with MEMOIR_REPO path."
            )
        
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line.startswith("MEMOIR_REPO="):
                    path = line.split("=", 1)[1].strip()
                    # Handle URLs vs local paths
                    if path.startswith("http"):
                        raise ValueError(
                            "MEMOIR_REPO should be a local path, not a URL. "
                            "Please clone the repo first."
                        )
                    return path
        
        raise ValueError("MEMOIR_REPO not found in .env file")
    
    def _validate_path(self):
        """Ensure memoir repo is separate from schema repo."""
        schema_repo = Path(__file__).parent.parent.resolve()
        
        # Check if memoir_path is inside schema repo
        try:
            self.repo_path.relative_to(schema_repo)
            raise ValueError(
                f"DANGER: Memoir repo ({self.repo_path}) is inside schema repo ({schema_repo}). "
                "This could leak private data! "
                "Please use a separate directory for memoir data."
            )
        except ValueError as e:
            if "DANGER" in str(e):
                raise
            # relative_to() raises ValueError if not relative - this is good
            pass
    
    def initialize(self) -> None:
        """Initialize the memoir repository structure."""
        self.repo_path.mkdir(parents=True, exist_ok=True)
        self.scenes_dir.mkdir(exist_ok=True)
        self.graphs_dir.mkdir(exist_ok=True)
        
        # Create initial index if it doesn't exist
        if not self.index_file.exists():
            initial_index = {
                "created": datetime.now().isoformat(),
                "scenes": {},
                "metadata": {
                    "total_scenes": 0,
                    "last_updated": datetime.now().isoformat()
                }
            }
            self._save_index(initial_index)
        
        print(f"Memoir repository initialized at: {self.repo_path}")
    
    def _load_index(self) -> Dict[str, Any]:
        """Load the index file."""
        if not self.index_file.exists():
            return {"scenes": {}, "metadata": {}}
        
        with open(self.index_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {"scenes": {}, "metadata": {}}
    
    def _save_index(self, index: Dict[str, Any]) -> None:
        """Save the index file."""
        index["metadata"]["last_updated"] = datetime.now().isoformat()
        with open(self.index_file, 'w', encoding='utf-8') as f:
            yaml.dump(index, f, default_flow_style=False, allow_unicode=True)
    
    def save_scene(self, scene_data: Dict[str, Any]) -> str:
        """
        Save a scene to the repository.
        
        Args:
            scene_data: Scene data dictionary conforming to SCHEMA.md
            
        Returns:
            scene_id of the saved scene
        """
        # Ensure repository is initialized
        if not self.scenes_dir.exists():
            self.initialize()
        
        # Generate scene_id if not present
        if "scene_id" not in scene_data:
            scene_data["scene_id"] = str(uuid.uuid4())
        
        scene_id = scene_data["scene_id"]
        
        # Generate filename from date and title
        date = scene_data.get("date", datetime.now().strftime("%Y-%m-%d"))
        title = scene_data.get("title", "untitled")
        # Sanitize title for filename
        safe_title = "".join(
            c if c.isalnum() or c in " -_" else "_" 
            for c in title
        ).lower().replace(" ", "_")
        
        filename = f"{date}_{safe_title}.yaml"
        filepath = self.scenes_dir / filename
        
        # Avoid overwriting - add suffix if file exists
        counter = 1
        while filepath.exists():
            filename = f"{date}_{safe_title}_{counter}.yaml"
            filepath = self.scenes_dir / filename
            counter += 1
        
        # Save scene file
        with open(filepath, 'w', encoding='utf-8') as f:
            yaml.dump(scene_data, f, default_flow_style=False, allow_unicode=True)
        
        # Update index
        index = self._load_index()
        index["scenes"][scene_id] = {
            "filename": filename,
            "title": scene_data.get("title", ""),
            "date": date,
            "tags": scene_data.get("tags", []),
            "created": datetime.now().isoformat()
        }
        index["metadata"]["total_scenes"] = len(index["scenes"])
        self._save_index(index)
        
        print(f"Scene saved: {filepath}")
        return scene_id
    
    def load_scene(self, scene_id: str) -> Optional[Dict[str, Any]]:
        """Load a scene by its ID."""
        index = self._load_index()
        
        if scene_id not in index["scenes"]:
            return None
        
        filename = index["scenes"][scene_id]["filename"]
        filepath = self.scenes_dir / filename
        
        if not filepath.exists():
            print(f"Warning: Scene file {filename} not found")
            return None
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def load_all_scenes(self) -> List[Dict[str, Any]]:
        """Load all scenes from the repository."""
        if not self.scenes_dir.exists():
            return []
        
        scenes = []
        for filepath in self.scenes_dir.glob("*.yaml"):
            with open(filepath, 'r', encoding='utf-8') as f:
                scene_data = yaml.safe_load(f)
                if scene_data:
                    scenes.append(scene_data)
        
        return scenes
    
    def list_scenes(self) -> List[Dict[str, str]]:
        """List all scenes with basic metadata."""
        index = self._load_index()
        return [
            {
                "scene_id": scene_id,
                **scene_info
            }
            for scene_id, scene_info in index["scenes"].items()
        ]
    
    def delete_scene(self, scene_id: str) -> bool:
        """Delete a scene by its ID."""
        index = self._load_index()
        
        if scene_id not in index["scenes"]:
            return False
        
        filename = index["scenes"][scene_id]["filename"]
        filepath = self.scenes_dir / filename
        
        if filepath.exists():
            filepath.unlink()
        
        del index["scenes"][scene_id]
        index["metadata"]["total_scenes"] = len(index["scenes"])
        self._save_index(index)
        
        print(f"Scene deleted: {scene_id}")
        return True
    
    def build_graph(self) -> MemoirGraph:
        """
        Build a graph from all scenes in the repository.
        
        Creates temporal edges automatically based on dates.
        """
        graph = MemoirGraph()
        scenes = self.load_all_scenes()
        
        # Add all scenes as nodes
        for scene_data in scenes:
            node = SceneNode(
                scene_id=scene_data.get("scene_id", str(uuid.uuid4())),
                title=scene_data.get("title", ""),
                date=scene_data.get("date", ""),
                location=scene_data.get("location", ""),
                tags=scene_data.get("tags", []),
                data=scene_data
            )
            graph.add_node(node)
        
        # Create temporal edges based on dates
        sorted_scenes = sorted(
            [n for n in graph.nodes.values() if isinstance(n, SceneNode) and n.date],
            key=lambda n: n.date
        )
        
        for i in range(len(sorted_scenes) - 1):
            edge = Edge(
                edge_id=f"temporal_{i}",
                edge_type="temporal",
                source=sorted_scenes[i].scene_id,
                target=sorted_scenes[i + 1].scene_id,
                metadata={"direction": "before"}
            )
            graph.add_edge(edge)
        
        return graph
    
    def save_graph(self, graph: MemoirGraph, name: str = "main") -> None:
        """Save a graph to the graphs directory."""
        if not self.graphs_dir.exists():
            self.initialize()
        
        filepath = self.graphs_dir / f"{name}_graph.json"
        graph.to_json(filepath)
        print(f"Graph saved: {filepath}")
    
    def load_graph(self, name: str = "main") -> Optional[MemoirGraph]:
        """Load a graph from the graphs directory."""
        filepath = self.graphs_dir / f"{name}_graph.json"
        
        if not filepath.exists():
            return None
        
        return MemoirGraph.from_json(filepath)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get repository statistics."""
        index = self._load_index()
        
        # Count tags
        tag_counts = {}
        for scene_info in index["scenes"].values():
            for tag in scene_info.get("tags", []):
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        return {
            "total_scenes": index["metadata"].get("total_scenes", 0),
            "total_tags": len(tag_counts),
            "popular_tags": sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            "repo_path": str(self.repo_path)
        }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Memoir repository manager")
    parser.add_argument("--init", action="store_true", help="Initialize memoir repository")
    parser.add_argument("--list-scenes", action="store_true", help="List all scenes")
    parser.add_argument("--stats", action="store_true", help="Show repository statistics")
    parser.add_argument("--build-graph", action="store_true", help="Build graph from all scenes")
    
    args = parser.parse_args()
    
    try:
        repo = MemoirRepo()
        
        if args.init:
            repo.initialize()
        
        elif args.list_scenes:
            scenes = repo.list_scenes()
            print(f"\nFound {len(scenes)} scenes:\n")
            for scene in scenes:
                print(f"  [{scene['date']}] {scene['title']} (ID: {scene['scene_id']})")
                if scene.get('tags'):
                    print(f"    Tags: {', '.join(scene['tags'])}")
        
        elif args.stats:
            stats = repo.get_statistics()
            print("\nRepository Statistics:")
            print(f"  Location: {stats['repo_path']}")
            print(f"  Total scenes: {stats['total_scenes']}")
            print(f"  Total tags: {stats['total_tags']}")
            if stats['popular_tags']:
                print("  Popular tags:")
                for tag, count in stats['popular_tags']:
                    print(f"    {tag}: {count}")
        
        elif args.build_graph:
            graph = repo.build_graph()
            stats = graph.get_statistics()
            print("\nGraph built successfully:")
            for key, value in stats.items():
                print(f"  {key}: {value}")
            
            # Save the graph
            repo.save_graph(graph)
            print("\nGraph saved to memoir repository")
        
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"Error: {e}")
