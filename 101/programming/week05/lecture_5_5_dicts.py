"""
Lecture 5.5: Dictionaries — Key-Value Storage
"""
from typing import TypedDict

# Creating a dictionary — each "key": value pair separated by commas
neuron = {
    "id": 1,
    "type": "pyramidal",
    "voltage": -70.0,
    "spike_count": 0,
    "brain_region": "cortex",
}

# Access values using the key in square brackets
print(neuron["type"])  # pyramidal
print(neuron["voltage"])  # -70.0

# Modify an existing value — just assign to the key
neuron["voltage"] = -65.0
print(neuron["voltage"])  # -65.0 — updated!

# Add a completely new key-value pair — same syntax as modifying
neuron["firing_rate"] = 15.5
print(neuron)
# {'id': 1, 'type': 'pyramidal', 'voltage': -65.0,
#  'spike_count': 0, 'brain_region': 'cortex', 'firing_rate': 15.5}
print()

# Methods
neuron = {"id": 1, "type": "pyramidal", "voltage": -70.0}

# keys() — get all the keys (the labels)
print(neuron.keys())  # dict_keys(['id', 'type', 'voltage'])

# values() — get all the values
print(neuron.values())  # dict_values([1, 'pyramidal', -70.0])

# items() — get both key and value together as pairs
# This is what you'll use most often when looping
print(neuron.items())  # dict_items([('id', 1), ('type', 'pyramidal'), ...])

# get() — returns the value, or a default if key is missing
print(neuron.get("voltage"))  # -70.0 — key exists, returns value
print(neuron.get("firing_rate"))  # None — key missing, returns None
print(neuron.get("firing_rate", 0))  # 0 — key missing, returns your default

# Check if a key exists before accessing
print("type" in neuron)  # True
print("firing_rate" in neuron)  # False
print()


# Iterations
class NeuronData(TypedDict):
    """Neuron Data typed dict"""

    type: str
    voltage: float
    spikes: int


neuron_network: dict[str, NeuronData] = {
    "N001": {"type": "pyramidal", "voltage": -70.0, "spikes": 15},
    "N002": {"type": "interneuron", "voltage": -72.0, "spikes": 42},
    "N003": {"type": "pyramidal", "voltage": -68.0, "spikes": 8},
    "N004": {"type": "granule", "voltage": -71.0, "spikes": 23},
}

# Loop through every neuron and display its status
print("Network Status:")
print("-" * 50)
for neuron_id, data in neuron_network.items():
    print(
        f"Neuron {neuron_id}: {data['type']}, "
        f"V={data['voltage']}mV, "
        f"Spikes={data['spikes']}"
    )
print()

# Find the most active neuron
# max() with a key function tells Python how to compare entries
most_active_id = max(neuron_network, key=lambda n: neuron_network[n]["spikes"])
print(
    f"Most active neuron: {most_active_id} " f"({neuron_network[most_active_id]['spikes']} spikes)"
)
# Most active neuron: N002 (42 spikes)

# Calculate average firing across the network
total_spikes = sum(int(data["spikes"]) for data in neuron_network.values())
avg_spikes = total_spikes / len(neuron_network)
print(f"Network average: {avg_spikes:.1f} spikes")

# Find all pyramidal neurons
pyramidal = [nid for nid, data in neuron_network.items() if data["type"] == "pyramidal"]
print(f"Pyramidal neurons: {pyramidal}")  # ['N001', 'N003']

# Find neurons with low activity (possible silent cells)
silent_neurons = [nid for nid, data in neuron_network.items() if int(data["spikes"]) < 10]
print(f"Low activity neurons: {silent_neurons}")  # ['N003']
