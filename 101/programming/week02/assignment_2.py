# Assignment 2: Neural Network Spike Counter
# Student Name: [YOUR NAME]
# Date: [DATE]

import random

print("=" * 60)
print("  NEURAL NETWORK SPIKE COUNTER")
print("=" * 60)
print()

# ── Parameters ──────────────────────────────────────────────
num_neurons = 10
num_steps   = 100
threshold   = -55.0   # Spike threshold (mV)
V_reset     = -70.0   # Reset voltage after spike (mV)

# ── Initialize neurons ───────────────────────────────────────
# All neurons start at resting potential with zero spikes recorded
voltages     = []
spike_counts = []

for i in range(num_neurons):
    voltages.append(-70.0)   # Resting potential (mV)
    spike_counts.append(0)   # No spikes yet

print(f"Simulating {num_neurons} neurons for {num_steps} time steps...")

# ── TODO 1: Simulation loop ──────────────────────────────────
# Use nested loops: outer loop over time steps, inner loop over neurons
# Hint: for step in range(num_steps): → for neuron in range(num_neurons):

for step in range(num_steps):
    for neuron in range(num_neurons):

        # TODO 2: Add random input to this neuron's voltage
        # Each neuron gets a different random input each step
        # Hint: random.uniform(0, 5) generates a random float between 0 and 5
        # Add it directly to voltages[neuron]


        # TODO 3: Check whether this neuron has reached threshold
        # If voltages[neuron] >= threshold:
        #   - Add 1 to spike_counts[neuron]
        #   - Reset voltages[neuron] to V_reset
        #   - Print a ⚡ character (use print("⚡", end="", flush=True) — no newline)


        pass  # Remove this line once you've added your code

print("  Simulation complete!\n")

# ── TODO 4: Display results ──────────────────────────────────
# For each neuron, print its spike count as a row of ⚡ symbols
# Then calculate and print the statistics below

print("=" * 60)
print("  SIMULATION RESULTS")
print("=" * 60)
print()
print("Spike Counts per Neuron:")

# TODO 5: Loop through each neuron and print:
# "Neuron X: ⚡⚡⚡ (N spikes)"
# Hint: "⚡" * spike_counts[neuron] repeats the symbol


# TODO 6: Calculate statistics
# You'll need: total spikes, average, max, min
# And the index of the most/least active neuron
# Hint: spike_counts.index(max(spike_counts)) finds the index of the highest value


print()
print("Statistics:")
print("-" * 60)
# Print your statistics here


print()
print("=" * 60)
