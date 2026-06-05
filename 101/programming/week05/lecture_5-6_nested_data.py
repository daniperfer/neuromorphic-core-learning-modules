"""
Lecture 5.6: Nested Data Structures
"""
from typing import TypedDict


# A list where each item is a dictionary describing one neuron
# Think of this like a spreadsheet — each dictionary is one row
class Neuron(TypedDict):
    """Neuron typed dict"""

    id: int
    type: str
    voltage: float
    active: bool


neurons: list[Neuron] = [
    {"id": 1, "type": "pyramidal", "voltage": -70.0, "active": True},
    {"id": 2, "type": "interneuron", "voltage": -72.0, "active": False},
    {"id": 3, "type": "pyramidal", "voltage": -68.0, "active": True},
    {"id": 4, "type": "granule", "voltage": -75.0, "active": True},
]

# Access a specific neuron — use list index
print(neurons[0])  # The first neuron (id: 1)
print(neurons[0]["type"])  # "pyramidal" — first neuron's type

# Access all neurons of a particular type using list comprehension
active_neurons = [n for n in neurons if n["active"]]
print(f"Active neurons: {len(active_neurons)} out of {len(neurons)}")

# Extract a single property from every neuron at once
voltages = [n["voltage"] for n in neurons]
print(f"All voltages: {voltages}")
print(f"Average voltage: {sum(voltages) / len(voltages):.1f} mV")

# Filter by type
pyramidal = [n for n in neurons if n["type"] == "pyramidal"]
print(f"Number of Pyramidal neurons: {len(pyramidal)}")
print(f"Their IDs: {[n['id'] for n in pyramidal]}")
print()


# A dictionary where each key is a neuron ID
# and each value is a list of that neuron's spike times
spike_records = {
    "N001": [10.5, 25.3, 40.1, 55.8, 70.2],
    "N002": [5.2, 15.7, 30.4, 45.9],
    "N003": [20.1, 60.3, 100.5],
    "N004": [8.4, 18.9, 29.3, 40.1, 50.8, 61.2, 72.5],
}

# Access one neuron's spike times using the ID
print(spike_records["N001"])  # [10.5, 25.3, 40.1, 55.8, 70.2]
print(spike_records["N001"][0])  # 10.5 — first spike time for N001

# Loop through every neuron and calculate firing rate
print("\n=== FIRING RATE ANALYSIS ===")
for neuron_id, spikes in spike_records.items():
    duration_sec = 0.1  # 100ms recording window
    rate = len(spikes) / duration_sec
    avg_isi = (spikes[-1] - spikes[0]) / (len(spikes) - 1) if len(spikes) > 1 else 0
    print(f"{neuron_id}: {len(spikes)} spikes | " f"{rate:.0f} Hz | " f"Avg ISI: {avg_isi:.1f} ms")

# Find the most active neuron
most_active = max(spike_records, key=lambda n: len(spike_records[n]))
print(f"\nMost active neuron: {most_active} " f"({len(spike_records[most_active])} spikes)")

# Find neurons with fewer than 4 spikes (low activity)
low_activity = [nid for nid, spikes in spike_records.items() if len(spikes) < 4]
print(f"Low activity neurons: {low_activity}")
print()

# Combining both patterns — a complete neuron record
full_network = {
    "N001": {
        "type": "pyramidal",
        "region": "cortex",
        "voltage_history": [-70.0, -68.0, -55.0, 40.0, -70.0],
        "spike_times": [10.5, 25.3, 40.1],
    },
    "N002": {
        "type": "interneuron",
        "region": "hippocampus",
        "voltage_history": [-72.0, -71.0, -70.5],
        "spike_times": [5.2, 15.7, 30.4, 45.9],
    },
}

# Access deeply nested data
print(full_network["N001"]["spike_times"][0])  # 10.5 — first spike of N001
print(full_network["N002"]["type"])  # interneuron
