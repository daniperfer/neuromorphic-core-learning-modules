# Assignment 5: Neural Data Analyzer
# Student Name: Daniel Pereira
# Date: June 5, 2026

import random
from typing import TypedDict

print("=" * 60)
print("  NEURAL DATA ANALYZER")
print("=" * 60)
print()

# Network parameters (use a tuple - these are fixed!)
NETWORK_PARAMS = (20, -70.0, -55.0, 100)
N_NEURONS, V_REST, V_THRESH, N_STEPS = NETWORK_PARAMS


# Create neuron registry (dictionary)
# Each neuron should have: voltage, spike_times (list), type, region
class Neuron(TypedDict):
    """Neuron typed dict"""

    voltage: float
    spike_times: list
    type: str
    region: str


network: dict[str, Neuron] = {}
neuron_types = ["pyramidal", "interneuron", "granule"]  # Should this be a tuple?
brain_regions = ["cortex", "hippocampus", "cerebellum"]

for i in range(N_NEURONS):
    neuron_id = f"N{i:03d}"
    # Add neuron to network dictionary
    network[neuron_id] = {
        "voltage": V_REST,
        "spike_times": [],
        "type": neuron_types[random.randint(0, len(neuron_types) - 1)],
        "region": brain_regions[random.randint(0, len(brain_regions) - 1)],
    }

# Run simulation (N_STEPS time steps)
active_neurons = set()  # Track which neurons have spiked

for step in range(N_STEPS):
    for neuron_id, neuron in network.items():
        # Add random input (0-4 mV)
        neuron["voltage"] += random.uniform(0, 4)

        # Check for spike
        if neuron["voltage"] >= V_THRESH:
            # Record spike time and reset voltage
            neuron["spike_times"].append(step)
            neuron["voltage"] = V_REST
            # Also Add to active_neurons set if spiked
            active_neurons.add(neuron_id)

# TODO: Analysis using list comprehensions
# 1. Get all spike counts
# 2. Find neurons above average firing rate
# 3. Group by type

# Display results
print("\n=== SIMULATION RESULTS ===")
print(f"Total neurons: {N_NEURONS}")
print(f"Active neurons: {len(active_neurons)}")

total_spikes = sum([len(n["spike_times"]) for n in network.values()])
print(f"Total spikes: {total_spikes}")
print(f"Average firing rate: {total_spikes / N_STEPS * 1000} Hz")  # N_STEPS in ms?

active_regions = []
for region in brain_regions:
    region_count = len([nid for nid in active_neurons if network[nid]["region"] is region])
    active_regions.append((region, region_count))

sorted_active_regions = sorted(active_regions, key=lambda n: n[1], reverse=True)
print(f"Most active region: {sorted_active_regions[0]}")
print(f"Second active region: {sorted_active_regions[1]}")
print(f"Last active region: {sorted_active_regions[-1]}")

print("\n=== TOP 5 MOST ACTIVE NEURONS ===")
# Sort --by len spike times-- and display top 5
neuron_list = [(k, len(v["spike_times"])) for k, v in network.items()]
sorted_neuron_list = sorted(neuron_list, key=lambda n: n[1], reverse=True)
for k in range(0, 5):
    nid = sorted_neuron_list[k][0]
    print(
        f"{k}. {nid} ({network[nid]['type']}, {network[nid]['region']}): "
        f"{len(network[nid]['spike_times'])} spikes"
    )

print("\n=== NEURON TYPE BREAKDOWN ===")
# Show stats per neuron type: filter in list comprehension
total_spikes_per_type = 0
for neuron_type in neuron_types:
    type_count = len([n for n in network.values() if n["type"] is neuron_type])
    spike_count = sum([len(n["spike_times"]) for n in network.values() if n["type"] is neuron_type])
    print(
        f"{neuron_type} \t#{type_count}: "
        f"\tavg {1. * spike_count / type_count:.2f} spikes, total {spike_count}"
    )
    total_spikes_per_type += spike_count
print(f"\nSum of total spikes per type: {total_spikes_per_type}")
