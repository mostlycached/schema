with open("agon_simulation.wav", "rb") as f:
    header = f.read(20)
    print(f"Header: {header}")
    print(f"Hex: {header.hex()}")
