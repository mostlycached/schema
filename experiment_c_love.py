import time
from vehicle import BraitenbergVehicle

def run_love_simulation():
    print("Initializing Experiment C: The Braitenberg 'Love' Loop")
    print("----------------------------------------------------")

    # Agent: The Lover
    # Target: Perfect Poetry.
    # Wiring: Love (Vehicle 3c). Moves towards it, but stops if too close.
    lover = BraitenbergVehicle(
        name="Lover",
        target_concept="Sublime, transcendent, perfect, aching beauty, divine poetry, absolute truth",
        wiring_type="love"
    )

    # Initial seed - something mundane to start the movement
    current_signal = "The cat sat on the mat."
    print(f"SEED: {current_signal}\n")

    for i in range(10):
        print(f"--- TURN {i+1} ---")
        
        print(f"[Lover Reads]: ...{current_signal[-50:]}")
        
        response, intensity, temp = lover.act(current_signal)
        
        print(f"[Lover Senses]: Intensity={intensity:.2f}")
        print(f"[Lover Acts]: Temp={temp:.2f} -> {response}")
        print("")
        
        # The output becomes the input for the next turn (Self-Loop)
        current_signal = response
        time.sleep(2)

if __name__ == "__main__":
    run_love_simulation()
