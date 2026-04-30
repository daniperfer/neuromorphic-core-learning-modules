# Neuron state classifier
# Membrane voltages are in millivolts (mV)

# Define thresholds as named constants (ALL CAPS signals they won't change)
SPIKE_THRESHOLD = -55.0
RESTING_POTENTIAL = -70.0
HYPERPOLARIZED_THRESHOLD = -80.0

voltage = float(input("Enter membrane voltage (mV): "))

if voltage >= SPIKE_THRESHOLD:
    state = "SPIKING"
    indicator = "🔴"
elif voltage > RESTING_POTENTIAL:
    state = "DEPOLARIZED"
    indicator = "🟡"
elif voltage >= HYPERPOLARIZED_THRESHOLD:
    state = "RESTING"
    indicator = "🟢"
else:
    state = "HYPERPOLARIZED"
    indicator = "🔵"

print(f"{indicator} Neuron state: {state} at {voltage} mV")
