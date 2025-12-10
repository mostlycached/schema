#!/usr/bin/env python3
"""
Quick script to capture a scene without the full interactive interview.
Edit the scene_data dictionary below with your experience, then run:
    python3 quick_capture.py
"""

from memoir_manager import MemoirRepo
from datetime import datetime
import uuid

# Edit this scene data with your experience
scene_data = {
    "scene_id": str(uuid.uuid4()),
    "title": "Working on Memoir Probe",  # Change this
    "date": datetime.now().strftime("%Y-%m-%d"),
    "location": "Home office",  # Change this
    "duration": "2 hours",
    "tags": ["work", "coding", "project"],  # Change these
    
    "phenomenology": {
        "cognitive_style": {
            "time_experience": "Flow state, time compressed",
            "space_experience": "Focused on screen, room fades away",
            "attention_mode": "Deep focus with occasional context switching"
        },
        "intersubjectivity": {
            "shared_meanings": ["coding conventions", "git workflow"],
            "emotional_tone": "Engaged, curious, satisfied",
            "intimacy_level": "Working with AI assistant, collaborative"
        },
        "body_experience": {
            "sensations": ["seated", "typing", "eyes on screen"],
            "posture": "Leaning forward at desk",
            "mobility": "Stationary"
        }
    },
    
    "structure": {
        "capital": {
            "economic": "Time invested in skill development",
            "cultural": "Programming knowledge, system design",
            "social": "Collaboration with AI",
            "symbolic": "Building something meaningful"
        },
        "doxa": {
            "beliefs": ["Good documentation matters", "Test before deploying"],
            "taboos": ["Hardcoding secrets", "Skipping validation"]
        },
        "habitus": {
            "behaviors": ["Check terminal output", "Read error messages carefully"],
            "gestures": ["Quick keyboard shortcuts", "Copy-paste patterns"],
            "language_style": "Technical, precise"
        },
        "hierarchy": {
            "position": "Creator/designer, autonomous",
            "mobility": "Complete control over implementation"
        }
    },
    
    "system": {
        "function": {
            "primary": "Building a memoir capture tool",
            "secondary": ["Learning", "Documenting life-worlds"]
        },
        "binary_code": {
            "code": "working/broken",
            "position": "Working (after debugging)"
        },
        "boundaries": {
            "entry_criteria": ["Having the idea", "Starting the implementation"],
            "exit_criteria": ["Completion", "User satisfaction"]
        },
        "communication": {
            "medium": "Code, documentation, conversation",
            "code_switching": ["Human language to code", "Abstract concepts to concrete implementation"]
        }
    },
    
    "inhabitants": [
        {
            "role": "Self as developer",
            "relationship": "primary actor",
            "power": "Full agency",
            "name": ""
        },
        {
            "role": "AI assistant",
            "relationship": "Collaborator",
            "power": "Supportive, generative",
            "name": ""
        }
    ],
    
    "genealogy": {
        "origin": "Thesis concept about capturing life-worlds",
        "influences": ["Phenomenology", "Sociology", "Previous work on WORLDS.md"]
    },
    
    "tension": {
        "internal": "Balancing completeness with pragmatism",
        "external": "Time constraints",
        "trajectory": "Growth - building momentum"
    },
    
    "narrative": {
        "description": "Started by reviewing THESIS.md requirements. Designed schema capturing phenomenological, structural, and systemic dimensions. Built Python modules for graph representation, repository management, and interactive interviews. Tested each component. Created comprehensive documentation. The system works.",
        "key_moments": [
            "Understanding the three-lens framework",
            "Fixing the dataclass inheritance bug",
            "Seeing the graph statistics output successfully"
        ],
        "turning_points": [
            "Realizing the privacy validation was critical"
        ]
    },
    
    "reflection": {
        "significance": "First implementation of the Adjacent Rooms architecture - the interrogator that captures where I am now",
        "patterns": ["Building -> Testing -> Documenting cycle"],
        "questions": [
            "What scenes from my life should I capture next?",
            "What patterns will emerge from multiple scenes?",
            "How will this help navigate to adjacent possible rooms?"
        ]
    },
    
    "metadata": {
        "captured_at": datetime.now().isoformat(),
        "interview_mode": "programmatic"
    }
}

if __name__ == "__main__":
    # Save the scene
    repo = MemoirRepo()
    scene_id = repo.save_scene(scene_data)
    
    print(f"\n✓ Scene captured successfully!")
    print(f"  ID: {scene_id}")
    print(f"  Title: {scene_data['title']}")
    print(f"  Date: {scene_data['date']}")
    print(f"\nTo view all scenes:")
    print(f"  python3 probe/memoir_manager.py --list-scenes")
