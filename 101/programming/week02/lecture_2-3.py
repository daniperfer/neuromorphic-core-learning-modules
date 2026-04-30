# Simplified neuron integration simulation
voltage = -70.0       # Starting at resting potential (mV)
threshold = -55.0     # Action potential threshold (mV)
time = 0              # Current time (ms)
dt = 1.0              # Time step size (ms)
I_input = 2.0         # Constant input current (nanoamps)

print("Starting simulation...")

while voltage < threshold:
    voltage = voltage + I_input * dt  # Input current raises voltage each step
    time = time + dt
    print(f"Time: {time:.1f} ms, Voltage: {voltage:.1f} mV")

print(f"\n⚡ SPIKE at time {time:.1f} ms!")
