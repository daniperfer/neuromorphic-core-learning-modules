# Assignment 5: Neural Data Analyzer
# Student Name: [YOUR NAME]
# Date: [DATE]

# import random
from typing import TypedDict

print("=" * 60)
print("  NEURAL DATA ANALYZER")
print("=" * 60)
print()

# Network parameters (use a tuple - these are fixed!)
NETWORK_PARAMS = (20, -70.0, -55.0, 100)
N_NEURONS, V_REST, V_THRESH, N_STEPS = NETWORK_PARAMS


# TODO: Create neuron registry (dictionary)
# Each neuron should have: voltage, spike_times (list), type, region
class Neuron(TypedDict):
    """Neuron typed dict"""

    voltage: float
    spike_times: list
    type: str
    region: str


network: dict[str, Neuron] = {}
neuron_types = ["pyramidal", "interneuron", "granule"]
brain_regions = ["cortex", "hippocampus", "cerebellum"]

for i in range(N_NEURONS):
    neuron_id = f"N{i:03d}"
    # TODO: Add neuron to network dictionary
    pass

# TODO: Run simulation (N_STEPS time steps)
active_neurons: set[str] = set()  # Track which neurons have spiked

for step in range(N_STEPS):
    for neuron_id in network:
        # TODO: Add random input (0-4 mV)
        # TODO: Check for spike
        # TODO: Record spike time and reset voltage
        # TODO: Add to active_neurons set if spiked
        pass

# TODO: Analysis using list comprehensions
# 1. Get all spike counts
# 2. Find neurons above average firing rate
# 3. Group by type

# TODO: Display results
print("\n=== SIMULATION RESULTS ===")
print(f"Total neurons: {N_NEURONS}")
print(f"Active neurons: {len(active_neurons)}")
# Add more statistics...

print("\n=== TOP 5 MOST ACTIVE NEURONS ===")
# TODO: Sort and display top 5

print("\n=== NEURON TYPE BREAKDOWN ===")
# TODO: Show stats per neuron type
