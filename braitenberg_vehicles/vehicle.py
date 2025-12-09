import os
import google.generativeai as genai
from dotenv import load_dotenv
import numpy as np

load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")
if not GEMINI_KEY:
    raise ValueError("GEMINI_KEY not found in .env")

genai.configure(api_key=GEMINI_KEY)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class BraitenbergVehicle:
    def __init__(self, name, target_concept, wiring_type="aggression", model_name="gemini-2.0-flash"):
        self.name = name
        self.target_concept = target_concept
        self.wiring_type = wiring_type
        self.model = genai.GenerativeModel(model_name)
        self.embedding_model = "models/text-embedding-004"
        
        # Pre-calculate target embedding
        self.target_embedding = self._get_embedding(target_concept)
        
        self.history = []

    def _get_embedding(self, text):
        result = genai.embed_content(
            model=self.embedding_model,
            content=text,
            task_type="semantic_similarity"
        )
        return result['embedding']

    def sense(self, environment_signal):
        """
        Calculates the intensity of the stimulus based on semantic similarity.
        """
        if not environment_signal:
            return 0.0
            
        signal_embedding = self._get_embedding(environment_signal)
        similarity = cosine_similarity(self.target_embedding, signal_embedding)
        return similarity

    def act(self, environment_signal):
        """
        Generates a response based on the sensed intensity and wiring.
        """
        intensity = self.sense(environment_signal)
        
        temperature = 0.5
        max_tokens = 100
        prompt_instruction = ""

        if self.wiring_type == "aggression":
            # Vehicle 2b (Aggression): Crossed wiring.
            # If signal matches target (high intensity), motor speeds up (high temp, high tokens).
            # It moves TOWARD the signal (engages with it).
            if intensity > 0.4: # Threshold
                temperature = 0.9 + (intensity * 0.1) # Max 1.0
                max_tokens = int(100 + (intensity * 200)) # Longer output
                prompt_instruction = f"You are highly stimulated by the concept of '{self.target_concept}'. You detect it strongly in the input. Respond aggressively, verbosely, and intensely. Dominate the conversation."
            else:
                temperature = 0.1
                max_tokens = 20
                prompt_instruction = f"You are bored. The input has nothing to do with '{self.target_concept}'. Respond with a short, dismissive, or uninterested remark."

        elif self.wiring_type == "fear":
            # Vehicle 2a (Fear): Uncrossed wiring.
            # If signal matches target (high intensity), motor speeds up (high temp, high tokens).
            # But here, "speeding up" means running AWAY. 
            # In a chat context, "running away" could be interpreted as changing the subject or ending the conversation, 
            # OR it could be interpreted as "retreating" into silence/short answers if we map velocity differently.
            # Let's stick to the RESEARCH.md interpretation:
            # "Agent B (The Coward)... If the conversation becomes 'Conflict-heavy,' Agent B lowers its temperature and retreats (short, agreeing answers) to escape the intensity."
            # Wait, RESEARCH.md says: "Wiring (Uncrossed): If light appears on the left, the left wheel speeds up, turning the vehicle *away*."
            # So high intensity -> High Velocity (turning away).
            # But the simulation description says: "Agent B lowers its temperature and retreats".
            # Let's follow the Simulation Description in RESEARCH.md for the "Coward":
            # "If the conversation becomes 'Conflict-heavy,' Agent B lowers its temperature and retreats (short, agreeing answers) to escape the intensity."
            
            if intensity > 0.4:
                temperature = 0.1
                max_tokens = 15
                prompt_instruction = f"You are afraid of the concept '{self.target_concept}'. You detect it in the input. Retreat! Be very brief, agree with whatever is said to avoid conflict, and try to hide."
            else:
                # Low intensity (safe) -> Normal behavior or even exploring?
                # Let's say it's calm.
                temperature = 0.7
                max_tokens = 50
                prompt_instruction = f"You feel safe. The scary concept '{self.target_concept}' is not present. Chat normally and relax."

        elif self.wiring_type == "love":
             # Vehicle 3c (Love): Inhibitory connections.
             # Moves toward light, but stops if too close.
             if intensity > 0.8:
                 # Too close! Stunned silence.
                 temperature = 0.1
                 max_tokens = 10
                 prompt_instruction = f"You are overwhelmed by the perfection of '{self.target_concept}'. You are speechless. Stutter or say almost nothing."
             elif intensity > 0.3:
                 # Sees it, wants it. Move towards it.
                 temperature = 0.8
                 max_tokens = 150
                 prompt_instruction = f"You see a glimpse of your beloved '{self.target_concept}'. Write poetry or prose that tries to capture it. Reach out for it."
             else:
                 # Doesn't see it. Wanders.
                 temperature = 0.6
                 max_tokens = 50
                 prompt_instruction = f"You are looking for '{self.target_concept}' but can't find it. Wander aimlessly in your thoughts."

        # Construct the full prompt
        full_prompt = f"{prompt_instruction}\n\nInput: {environment_signal}\n\nResponse:"
        
        try:
            response = self.model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            )
            return response.text, intensity, temperature
        except Exception as e:
            return f"[Error: {e}]", intensity, temperature
