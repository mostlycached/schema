import time
from vehicle import BraitenbergVehicle

def run_agon_simulation():
    print("Initializing Experiment A: The Deleuzian Agon")
    print("---------------------------------------------")

    # Agent A: The Aggressor
    # Target: Chaos. If it sees Chaos, it gets excited and adds MORE Chaos (Aggression).
    aggressor = BraitenbergVehicle(
        name="Aggressor",
        target_concept="Chaos, noise, shouting, complexity, confusion, verbosity",
        wiring_type="aggression"
    )

    # Agent B: The Coward
    # Target: Conflict. If it sees Conflict, it gets scared and retreats (Fear).
    coward = BraitenbergVehicle(
        name="Coward",
        target_concept="Conflict, anger, aggression, fighting, shouting",
        wiring_type="fear"
    )

    # Initial seed
    current_signal = "Hello, is anyone there? It's very quiet."
    print(f"SEED: {current_signal}\n")

    for i in range(10):
        print(f"--- TURN {i+1} ---")
        
        # Aggressor's Turn
        print(f"[Input to Aggressor]: {current_signal[:50]}...")
        response_a, intensity_a, temp_a = aggressor.act(current_signal)
        print(f"[Aggressor Senses]: Intensity={intensity_a:.2f} (Target: Chaos)")
        print(f"[Aggressor Acts]: Temp={temp_a:.2f} -> {response_a}")
        print("")
        
        # Pass Aggressor's output to Coward
        current_signal = response_a
        time.sleep(2) # Avoid rate limits

        # Coward's Turn
        print(f"[Input to Coward]: {current_signal[:50]}...")
        response_b, intensity_b, temp_b = coward.act(current_signal)
        print(f"[Coward Senses]: Intensity={intensity_b:.2f} (Target: Conflict)")
        print(f"[Coward Acts]: Temp={temp_b:.2f} -> {response_b}")
        print("")

        # Pass Coward's output back to Aggressor
        current_signal = response_b
        time.sleep(2)

if __name__ == "__main__":
    run_agon_simulation()
