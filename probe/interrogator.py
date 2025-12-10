"""
Interactive interrogator module for capturing memoir scenes.

This module provides an interview-style interface for capturing rich
phenomenological, structural, and systemic data about life-world scenes.
"""

import os
import yaml
from typing import Dict, List, Optional, Any
from datetime import datetime
import uuid

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from memoir_manager import MemoirRepo


class InterviewSession:
    """
    Manages an interactive interview session to capture a memoir scene.
    
    Uses conversational prompting to guide the user through phenomenological,
    structural, and systemic reflection on their lived experience.
    """
    
    # Interview prompt templates
    INTRO_PROMPT = """
I'm here to help you capture a moment from your life in rich detail. 
We'll explore this scene through three lenses:
1. How you experienced it (phenomenology)
2. The social dynamics and power at play (structure)
3. Its function in a larger system

Let's begin. Please describe a scene from your life that feels significant to you.
It could be recent or from the past, ordinary or extraordinary.
"""

    PHENOMENOLOGY_PROMPTS = {
        "time": "How did you experience time in this scene? Was it stretched, compressed, cyclical, or fragmented?",
        "space": "How did you experience the space? Was it confined, open, virtual, liminal?",
        "attention": "What was your attention like? Were you hypervigilant, in flow, dissociated, scanning?",
        "emotions": "What was the dominant emotional tone? What feelings permeated the scene?",
        "shared_meanings": "What was understood by everyone without being said? What went without saying?",
        "body": "What physical sensations do you remember? How did your body feel?",
        "posture": "What was your posture or physical position?",
    }
    
    STRUCTURE_PROMPTS = {
        "capital": "What was valued or exchanged in this scene? This could be money, knowledge, connections, or prestige.",
        "doxa": "What beliefs or rules were taken for granted? What couldn't be questioned?",
        "taboos": "What couldn't be said or done? What would have been transgressive?",
        "habitus": "What automatic behaviors or habits did you notice? What did people do without thinking?",
        "hierarchy": "Where did you stand in the power dynamics? Were you subordinate, equal, or in authority?",
        "language": "How did people speak? What register, tone, or code-switching occurred?",
    }
    
    SYSTEM_PROMPTS = {
        "function": "What purpose did this scene serve? What was it FOR?",
        "binary_code": "What was the core distinction or choice at play? (e.g., legal/illegal, profit/loss, success/failure)",
        "boundaries": "What determined who belonged and who didn't? How could one enter or exit?",
        "medium": "What circulated or was exchanged? Money, power, truth, love?",
    }
    
    REFLECTION_PROMPTS = {
        "significance": "Why does this scene matter to you? What makes it worth remembering?",
        "patterns": "Does this scene repeat in your life? Are there patterns or rhythms to it?",
        "questions": "What questions does this scene raise for you? What remains unresolved?",
    }
    
    def __init__(self, use_llm: bool = True):
        """
        Initialize interview session.
        
        Args:
            use_llm: Whether to use LLM for conversational prompting (requires GEMINI_KEY in .env)
        """
        self.use_llm = use_llm and genai is not None
        self.scene_data: Dict[str, Any] = {}
        self.conversation_history: List[Dict[str, str]] = []
        
        if self.use_llm:
            self._init_llm()
    
    def _init_llm(self):
        """Initialize Gemini API for conversational prompting."""
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
        
        if not os.path.exists(env_file):
            print("Warning: No .env file found. Falling back to manual prompts.")
            self.use_llm = False
            return
        
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith("GEMINI_KEY="):
                    api_key = line.split("=", 1)[1].strip()
                    genai.configure(api_key=api_key)
                    self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
                    return
        
        print("Warning: GEMINI_KEY not found in .env. Falling back to manual prompts.")
        self.use_llm = False
    
    def _ask(self, prompt: str) -> str:
        """Ask a question and get user input."""
        print(f"\n{prompt}")
        response = input("> ").strip()
        
        self.conversation_history.append({
            "role": "interviewer",
            "content": prompt
        })
        self.conversation_history.append({
            "role": "user",
            "content": response
        })
        
        return response
    
    def _ask_with_llm_followup(self, initial_prompt: str, context: str) -> str:
        """
        Ask a question with LLM-generated follow-ups for deeper exploration.
        
        Args:
            initial_prompt: The initial question
            context: Context about what we're trying to capture
        """
        # Get initial response
        response = self._ask(initial_prompt)
        
        if not self.use_llm or not response:
            return response
        
        # Use LLM to generate a thoughtful follow-up
        system_prompt = f"""You are helping conduct a phenomenological interview.
The user is describing {context}.
They just answered: "{initial_prompt}"
Their response was: "{response}"

Generate ONE brief follow-up question to help them go deeper.
The question should be gentle, exploratory, and help them access sensory or emotional detail.
Keep it under 20 words."""
        
        try:
            chat = self.model.start_chat()
            followup_response = chat.send_message(system_prompt)
            followup = followup_response.text.strip()
            
            # Ask the follow-up
            if followup and len(followup) < 200:  # Safety check
                additional = self._ask(followup)
                if additional:
                    response = f"{response} {additional}"
        except Exception as e:
            # Silently fall back if LLM fails
            pass
        
        return response
    
    def conduct_interview(self) -> Dict[str, Any]:
        """
        Conduct the full interview and return structured scene data.
        """
        print("=" * 60)
        print("MEMOIR SCENE INTERROGATION")
        print("=" * 60)
        print(self.INTRO_PROMPT)
        
        # Initial narrative
        narrative = self._ask("Please describe the scene:")
        
        # Basic metadata
        print("\n" + "=" * 60)
        print("BASIC INFORMATION")
        print("=" * 60)
        
        title = self._ask("Give this scene a short title:")
        date = self._ask("When did this occur? (YYYY-MM-DD or description):")
        location = self._ask("Where did this take place?")
        duration = self._ask("How long did it last? (e.g., '2 hours', 'a moment', 'ongoing'):")
        tags_input = self._ask("Any tags to categorize this? (comma-separated):")
        tags = [t.strip() for t in tags_input.split(",") if t.strip()]
        
        # Phenomenology
        print("\n" + "=" * 60)
        print("PHENOMENOLOGY - How You Experienced It")
        print("=" * 60)
        
        phenomenology = {
            "cognitive_style": {
                "time_experience": self._ask_with_llm_followup(
                    self.PHENOMENOLOGY_PROMPTS["time"],
                    "their experience of time"
                ),
                "space_experience": self._ask_with_llm_followup(
                    self.PHENOMENOLOGY_PROMPTS["space"],
                    "their experience of space"
                ),
                "attention_mode": self._ask(self.PHENOMENOLOGY_PROMPTS["attention"])
            },
            "intersubjectivity": {
                "shared_meanings": self._ask(self.PHENOMENOLOGY_PROMPTS["shared_meanings"]).split(","),
                "emotional_tone": self._ask(self.PHENOMENOLOGY_PROMPTS["emotions"]),
                "intimacy_level": ""
            },
            "body_experience": {
                "sensations": self._ask(self.PHENOMENOLOGY_PROMPTS["body"]).split(","),
                "posture": self._ask(self.PHENOMENOLOGY_PROMPTS["posture"]),
                "mobility": ""
            }
        }
        
        # Structure
        print("\n" + "=" * 60)
        print("STRUCTURE - Social Dynamics and Power")
        print("=" * 60)
        
        structure = {
            "capital": {
                "economic": "",
                "cultural": "",
                "social": "",
                "symbolic": ""
            },
            "doxa": {
                "beliefs": self._ask(self.STRUCTURE_PROMPTS["doxa"]).split(","),
                "taboos": self._ask(self.STRUCTURE_PROMPTS["taboos"]).split(",")
            },
            "habitus": {
                "behaviors": self._ask(self.STRUCTURE_PROMPTS["habitus"]).split(","),
                "gestures": [],
                "language_style": self._ask(self.STRUCTURE_PROMPTS["language"])
            },
            "hierarchy": {
                "position": self._ask(self.STRUCTURE_PROMPTS["hierarchy"]),
                "mobility": ""
            }
        }
        
        # Simplified capital question
        capital_response = self._ask(self.STRUCTURE_PROMPTS["capital"])
        structure["capital"]["economic"] = capital_response
        
        # System
        print("\n" + "=" * 60)
        print("SYSTEM - Function and Boundaries")
        print("=" * 60)
        
        system = {
            "function": {
                "primary": self._ask(self.SYSTEM_PROMPTS["function"]),
                "secondary": []
            },
            "binary_code": {
                "code": self._ask(self.SYSTEM_PROMPTS["binary_code"]),
                "position": ""
            },
            "boundaries": {
                "entry_criteria": self._ask(self.SYSTEM_PROMPTS["boundaries"]).split(","),
                "exit_criteria": []
            },
            "communication": {
                "medium": self._ask(self.SYSTEM_PROMPTS["medium"]),
                "code_switching": []
            }
        }
        
        # Inhabitants
        print("\n" + "=" * 60)
        print("INHABITANTS - Who Was Present?")
        print("=" * 60)
        
        inhabitants = []
        while True:
            role = self._ask("Describe a role/person present (or 'done'):")
            if role.lower() in ['done', 'd', '']:
                break
            relationship = self._ask(f"  Your relationship to them:")
            inhabitants.append({
                "role": role,
                "relationship": relationship,
                "power": "",
                "name": ""
            })
        
        # Reflection
        print("\n" + "=" * 60)
        print("REFLECTION")
        print("=" * 60)
        
        reflection = {
            "significance": self._ask(self.REFLECTION_PROMPTS["significance"]),
            "patterns": self._ask(self.REFLECTION_PROMPTS["patterns"]).split(","),
            "questions": self._ask(self.REFLECTION_PROMPTS["questions"]).split(",")
        }
        
        # Compile scene data
        self.scene_data = {
            "scene_id": str(uuid.uuid4()),
            "title": title,
            "date": date,
            "location": location,
            "duration": duration,
            "tags": tags,
            "phenomenology": phenomenology,
            "structure": structure,
            "system": system,
            "inhabitants": inhabitants,
            "genealogy": {
                "origin": "",
                "influences": []
            },
            "tension": {
                "internal": "",
                "external": "",
                "trajectory": ""
            },
            "narrative": {
                "description": narrative,
                "key_moments": [],
                "turning_points": []
            },
            "reflection": reflection,
            "metadata": {
                "captured_at": datetime.now().isoformat(),
                "interview_mode": "llm" if self.use_llm else "manual"
            }
        }
        
        return self.scene_data
    
    def save_scene(self, repo: Optional[MemoirRepo] = None) -> str:
        """
        Save the captured scene to the memoir repository.
        
        Args:
            repo: MemoirRepo instance (creates one if not provided)
            
        Returns:
            scene_id of saved scene
        """
        if not self.scene_data:
            raise ValueError("No scene data to save. Run conduct_interview() first.")
        
        if repo is None:
            repo = MemoirRepo()
        
        return repo.save_scene(self.scene_data)
    
    def preview(self) -> str:
        """Generate a readable preview of the captured scene."""
        if not self.scene_data:
            return "No scene data captured yet."
        
        lines = []
        lines.append("=" * 60)
        lines.append(f"SCENE: {self.scene_data['title']}")
        lines.append("=" * 60)
        lines.append(f"Date: {self.scene_data['date']}")
        lines.append(f"Location: {self.scene_data['location']}")
        lines.append(f"Duration: {self.scene_data['duration']}")
        if self.scene_data['tags']:
            lines.append(f"Tags: {', '.join(self.scene_data['tags'])}")
        lines.append("")
        lines.append("NARRATIVE:")
        lines.append(self.scene_data['narrative']['description'])
        lines.append("")
        lines.append("PHENOMENOLOGY:")
        lines.append(f"  Time: {self.scene_data['phenomenology']['cognitive_style']['time_experience']}")
        lines.append(f"  Space: {self.scene_data['phenomenology']['cognitive_style']['space_experience']}")
        lines.append(f"  Emotion: {self.scene_data['phenomenology']['intersubjectivity']['emotional_tone']}")
        lines.append("")
        lines.append("REFLECTION:")
        lines.append(f"  {self.scene_data['reflection']['significance']}")
        lines.append("=" * 60)
        
        return "\n".join(lines)


def main():
    """Run an interactive interview session."""
    print("Welcome to the Memoir Interrogator\n")
    
    # Check if we should use LLM
    use_llm = input("Use AI-assisted prompting? (y/n, default=n): ").strip().lower() == 'y'
    
    # Conduct interview
    session = InterviewSession(use_llm=use_llm)
    scene_data = session.conduct_interview()
    
    # Preview
    print("\n\n")
    print(session.preview())
    
    # Save
    save = input("\nSave this scene to your memoir repository? (y/n): ").strip().lower()
    if save == 'y':
        try:
            repo = MemoirRepo()
            scene_id = session.save_scene(repo)
            print(f"\n✓ Scene saved successfully! (ID: {scene_id})")
        except Exception as e:
            print(f"\n✗ Error saving scene: {e}")
            print("\nYou can manually save the scene data:")
            print(yaml.dump(scene_data, default_flow_style=False))
    else:
        print("\nScene not saved. Here's the YAML data if you want to save it manually:")
        print("\n" + yaml.dump(scene_data, default_flow_style=False))


if __name__ == "__main__":
    main()
