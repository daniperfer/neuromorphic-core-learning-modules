num_neurons = 5

print("Initializing neural network...")

for neuron_id in range(num_neurons):
    voltage = -70.0  # All neurons start at resting potential
    print(f"Neuron {neuron_id}: {voltage} mV")

print("Network initialized!")

print()
# Simulate membrane voltage rising over 10 ms
dt = 1.0        # Time step in milliseconds
duration = 10   # Total simulation duration in ms

print("Time-stepped simulation:")

for time_step in range(int(duration / dt)):
    time = time_step * dt          # Convert step number to actual time in ms
    voltage = -70 + time * 0.5    # Voltage rises 0.5 mV each millisecond
    print(f"t={time:.1f} ms:  V={voltage:.1f} mV")
