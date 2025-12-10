"""
Example: Programmatic usage of the memoir probe modules.

This demonstrates how to use the memoir probe modules in your own scripts
without the interactive interview interface.
"""

from probe.memoir_manager import MemoirRepo
from probe.graph import MemoirGraph, SceneNode, Edge
from datetime import datetime
import uuid


def example_create_scene_programmatically():
    """Create and save a scene without the interactive interview."""
    
    # Define scene data manually
    scene_data = {
        "scene_id": str(uuid.uuid4()),
        "title": "Morning Coffee Ritual",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "location": "Home kitchen",
        "duration": "15 minutes",
        "tags": ["morning", "ritual", "solitude"],
        
        "phenomenology": {
            "cognitive_style": {
                "time_experience": "slow, meditative",
                "space_experience": "warm, enclosed, safe",
                "attention_mode": "present, focused on sensations"
            },
            "intersubjectivity": {
                "shared_meanings": ["morning silence is sacred"],
                "emotional_tone": "calm, grateful",
                "intimacy_level": "solitary"
            },
            "body_experience": {
                "sensations": ["warmth of the cup", "aroma of coffee", "quiet"],
                "posture": "sitting at table",
                "mobility": "still"
            }
        },
        
        "structure": {
            "capital": {
                "economic": "cost of coffee beans",
                "cultural": "knowledge of brewing technique",
                "social": "none, private ritual",
                "symbolic": "status as a 'morning person'"
            },
            "doxa": {
                "beliefs": ["mornings are for slowness"],
                "taboos": ["rushing through this"]
            },
            "habitus": {
                "behaviors": ["automatic brewing motions", "sitting in same chair"],
                "gestures": ["careful pour", "slow sip"],
                "language_style": "internal monologue"
            },
            "hierarchy": {
                "position": "autonomous, self-directed",
                "mobility": "complete freedom"
            }
        },
        
        "system": {
            "function": {
                "primary": "transition from sleep to wakefulness",
                "secondary": ["self-care", "ritual maintenance"]
            },
            "binary_code": {
                "code": "peaceful/rushed",
                "position": "peaceful"
            },
            "boundaries": {
                "entry_criteria": ["being awake", "having time"],
                "exit_criteria": ["coffee finished", "ready for day"]
            },
            "communication": {
                "medium": "self-reflection",
                "code_switching": ["sleep-mode to day-mode"]
            }
        },
        
        "inhabitants": [
            {
                "role": "self",
                "relationship": "subject",
                "power": "complete control",
                "name": ""
            }
        ],
        
        "narrative": {
            "description": "Wake up, pad to kitchen, grind beans, pour water. Sit in quiet. Watch light change. Sip slowly.",
            "key_moments": ["first sip", "moment of gratitude"],
            "turning_points": []
        },
        
        "reflection": {
            "significance": "This daily ritual anchors me and creates a pocket of peace before the chaos",
            "patterns": ["repeated daily"],
            "questions": ["What would it feel like to skip this?"]
        }
    }
    
    # Save to memoir repo
    repo = MemoirRepo()
    scene_id = repo.save_scene(scene_data)
    
    print(f"Scene created and saved: {scene_id}")
    return scene_id


def example_query_scenes():
    """Query and analyze scenes from the repository."""
    
    repo = MemoirRepo()
    
    # Get all scenes
    all_scenes = repo.load_all_scenes()
    print(f"Total scenes: {len(all_scenes)}")
    
    # Build graph
    graph = repo.build_graph()
    
    # Get statistics
    stats = graph.get_statistics()
    print(f"\nGraph statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Find scenes by tag
    morning_scenes = graph.find_scenes_by_tag("morning")
    print(f"\nMorning scenes: {len(morning_scenes)}")
    
    # Get temporal sequence
    temporal = graph.get_temporal_sequence()
    if temporal:
        print(f"\nEarliest scene: {temporal[0].title} ({temporal[0].date})")
        print(f"Latest scene: {temporal[-1].title} ({temporal[-1].date})")


def example_custom_graph():
    """Build a custom graph with additional edges."""
    
    repo = MemoirRepo()
    
    # Start with automatic graph
    graph = repo.build_graph()
    
    # Add custom edges (e.g., similarity edges)
    scenes = list(graph.nodes.values())
    if len(scenes) >= 2:
        # Add a similarity edge between first two scenes
        edge = Edge(
            edge_id="custom_similar_1",
            edge_type="similar",
            source=scenes[0].node_id,
            target=scenes[1].node_id,
            metadata={
                "similarity_type": "phenomenological",
                "description": "Both involve morning solitude"
            }
        )
        graph.add_edge(edge)
    
    # Save the enhanced graph
    repo.save_graph(graph, name="custom")
    print("Custom graph saved")


if __name__ == "__main__":
    print("=" * 60)
    print("MEMOIR PROBE - PROGRAMMATIC EXAMPLE")
    print("=" * 60)
    
    # Example 1: Create a scene programmatically
    print("\n1. Creating a scene programmatically...")
    example_create_scene_programmatically()
    
    # Example 2: Query scenes
    print("\n2. Querying scenes...")
    example_query_scenes()
    
    # Example 3: Custom graph
    print("\n3. Creating custom graph...")
    example_custom_graph()
    
    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)
