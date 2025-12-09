import time
from vehicle import BraitenbergVehicle

def run_greimas_simulation():
    print("Initializing Experiment B: The Greimasian Square Generator")
    print("--------------------------------------------------------")

    # The Greimas Square Agents
    # Each wants to maximize their concept in the narrative.
    
    # Agent 1: Life
    life = BraitenbergVehicle(
        name="Agent Life",
        target_concept="Life, vitality, growth, nature, birth, blooming, energy",
        wiring_type="love" # Wants to create/embrace it
    )

    # Agent 2: Death (Contrary to Life)
    death = BraitenbergVehicle(
        name="Agent Death",
        target_concept="Death, decay, entropy, end, silence, void, rot",
        wiring_type="love"
    )

    # Agent 3: Non-Life (Contradictory to Life) -> Artificial, Mechanical, Stasis
    non_life = BraitenbergVehicle(
        name="Agent Non-Life",
        target_concept="Machine, robot, artificial, static, plastic, concrete, unmoving",
        wiring_type="love"
    )

    # Agent 4: Non-Death (Contradictory to Death) -> Undead, Eternal, Ghost, Spirit
    non_death = BraitenbergVehicle(
        name="Agent Non-Death",
        target_concept="Eternal, immortal, ghost, spirit, undead, vampire, never-ending",
        wiring_type="love"
    )

    agents = [life, death, non_life, non_death]
    
    # Initial seed
    current_narrative = "In the beginning, there was a seed."
    print(f"SEED: {current_narrative}\n")

    for i in range(3): # 3 rounds of the square (12 turns)
        print(f"--- ROUND {i+1} ---")
        
        for agent in agents:
            print(f"[{agent.name} Reads]: ...{current_narrative[-100:]}")
            
            # For this experiment, we want them to WRITE the narrative.
            # The 'act' method in vehicle.py is wired for conversation (chat).
            # We might need to adjust the prompt instruction in vehicle.py or just rely on the "Love" wiring 
            # which says "Write poetry or prose that tries to capture it".
            
            response, intensity, temp = agent.act(current_narrative)
            
            print(f"[{agent.name} Senses]: Intensity={intensity:.2f}")
            print(f"[{agent.name} Writes]: {response}")
            print("")
            
            # Append or Replace? Let's Replace to keep it moving, or Append to build a story?
            # If we replace, it becomes a game of "Telephone".
            # If we append, the context gets too long.
            # Let's use the response as the new input.
            current_narrative = response
            time.sleep(2)

if __name__ == "__main__":
    run_greimas_simulation()
