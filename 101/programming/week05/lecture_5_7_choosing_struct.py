"""
Lecture 5.7: Choosing the Right Data Structure
"""
import random
from typing import TypedDict

# LIST: ordered, changeable, allows duplicates
# Use when: sequence of items that may grow, shrink, or be reordered
spike_times = [10.5, 23.1, 45.7]  # ✅ Order matters, will grow during recording

# TUPLE: ordered, unchangeable, allows duplicates
# Use when: fixed data that should never be modified
coordinates = (3.5, 7.2, 1.8)  # ✅ Physical location — permanently fixed

# SET: unordered, unique items only
# Use when: membership testing, deduplication, comparing groups
active_neurons = {1, 3, 5, 7}  # ✅ Need unique IDs, fast "is X active?" checks

# DICTIONARY: key-value pairs, fast lookup by name
# Use when: associating properties with subjects
neuron_data = {"N001": -70.0}  # ✅ Look up any neuron by its ID instantly
print()


"""
Complete Neural Network Data Manager
Demonstrates all four data structures working together
in a realistic neuroscience simulation
"""

# ── TUPLE ──────────────────────────────────────────────
# Network configuration — fixed biological and simulation parameters
# These never change during the simulation, so a tuple is perfect
NETWORK_PARAMS = (100, -70.0, -55.0, 20.0)  # (n_neurons, V_rest, V_thresh, tau)
N_NEURONS, V_REST, V_THRESH, TAU = NETWORK_PARAMS
# Unpacking immediately makes the values easy to use by name


# ── DICTIONARY of DICTIONARIES ─────────────────────────
# Neuron registry — each neuron needs multiple properties
# Dictionary lets us look up any neuron instantly by its ID
class Neuron(TypedDict):
    """Neuron typed dict"""

    voltage: float
    spike_times: list
    type: str
    active: bool


network: dict[str, Neuron] = {}
for i in range(5):  # Small example with 5 neurons
    neuron_id = f"N{i:03d}"
    network[neuron_id] = {
        "voltage": V_REST,  # Starts at resting potential
        "spike_times": [],  # LIST — will grow as neuron fires
        "type": "pyramidal" if i % 2 == 0 else "interneuron",
        "active": True,
    }
    # Note: spike_times is a LIST inside the dictionary
    # because it starts empty and grows — that's exactly what lists are for

# ── LIST ───────────────────────────────────────────────
# Spike event log — a chronological record of every spike
# Order matters (we want events in time order) so a list is correct
spike_events = []  # Will contain (time, neuron_id) tuples

# ── SIMULATION ─────────────────────────────────────────
print("Running simulation...")
for t in range(10):  # 10 time steps
    for neuron_id, neuron in network.items():
        # Random synaptic input arriving at this time step
        I_input = random.uniform(0, 5)
        neuron["voltage"] += float(I_input)

        # Check if voltage crossed the firing threshold
        if neuron["voltage"] >= V_THRESH:
            # Record spike in the neuron's personal spike list
            neuron["spike_times"].append(t)
            # Also add to the global event log as a tuple (time, id)
            # Tuple because this event record is complete and won't change
            spike_events.append((t, neuron_id))
            # Reset voltage to resting potential
            neuron["voltage"] = V_REST

# ── ANALYSIS ───────────────────────────────────────────
print("\n=== NETWORK SIMULATION RESULTS ===\n")

# SET — which unique neurons fired at least once?
# Set comprehension automatically handles duplicates
# (a neuron that fired 5 times still appears only once)
spiking_neurons = {event[1] for event in spike_events}
silent_neurons = set(network.keys()) - spiking_neurons

print(f"Neurons that spiked: {spiking_neurons}")
print(f"Silent neurons: {silent_neurons if silent_neurons else 'None'}")
print()

# Detailed breakdown per neuron
print("Spike counts:")
for neuron_id, neuron in network.items():
    count = len(neuron["spike_times"])
    bar = "⚡" * count if count > 0 else "── silent"
    print(f"  {neuron_id} ({neuron['type']:12}): {bar} ({count})")

# Summary statistics
total = sum(len(n["spike_times"]) for n in network.values())
print(f"\nTotal network spikes: {total}")
print(f"Average per neuron: {total / len(network):.1f}")
print(f"Network participation: {len(spiking_neurons)}/{len(network)} neurons fired")
print()
