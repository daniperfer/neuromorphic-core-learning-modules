"""
Lecture 5.3: Tuples — Immutable Sequences
"""

# Creating tuples
neuron_position = (3.5, 7.2, 1.8)  # (x, y, z) coordinates in mm
print(neuron_position)
print(type(neuron_position))  # <class 'tuple'>

# Access items exactly like a list — using index numbers
print(neuron_position[0])  # 3.5 (x coordinate)
print(neuron_position[-1])  # 1.8 (z coordinate)

# But try to change it — Python will stop you immediately
# neuron_position[0] = 5.0  # ❌ TypeError: 'tuple' object does not support item assignment

# TUPLES — fixed biological and experimental constants
RESTING_POTENTIAL = (-70.0,)  # Fixed biological value
THRESHOLD = (-55.0,)  # Fixed threshold
BRAIN_REGIONS = ("cortex", "hippocampus", "cerebellum", "thalamus")
ELECTRODE_POSITION = (3.5, 7.2, 1.8)  # Physical location — won't move

# LISTS — data that changes as the experiment runs
current_voltages = [-70.0, -70.0, -70.0]  # Will change during simulation
spike_times: list[float] = []  # Will grow as neuron fires
active_neurons: list[int] = []  # Changes based on activity
print()

# UNPACKING
# A tuple containing data about one neuron
neuron_data = ("pyramidal", -70.0, 42)

# Traditional way to access — verbose and repetitive
neuron_type = neuron_data[0]
voltage = neuron_data[1]
neuron_id = neuron_data[2]

# Tuple unpacking — clean and readable
neuron_type, voltage, neuron_id = neuron_data

print(neuron_type)  # pyramidal
print(voltage)  # -70.0
print(neuron_id)  # 42
print()


def get_neuron_stats(spike_times):
    """
    Analyze a spike train and return key statistics.
    Returns a tuple of (min_time, max_time, average_time, firing_rate)
    """
    min_t = min(spike_times)
    max_t = max(spike_times)
    avg_t = sum(spike_times) / len(spike_times)
    duration = max_t - min_t
    firing_rate = len(spike_times) / (duration / 1000)  # Convert to Hz

    return min_t, max_t, avg_t, firing_rate  # Python automatically packs these into a tuple


# Call the function and unpack the results immediately
spikes = [10.5, 23.1, 45.7, 67.2, 89.0]
min_t, max_t, avg_t, rate = get_neuron_stats(spikes)

print(f"First spike: {min_t} ms")
print(f"Last spike: {max_t} ms")
print(f"Average spike time: {avg_t:.1f} ms")
print(f"Firing rate: {rate:.1f} Hz")
print()

# Tuple of tuples:
# Multi-electrode array — positions fixed at implant
# Each tuple is (x, y, z) position in millimeters
electrode_array = (
    (0.0, 0.0, 0.5),  # Electrode 1
    (0.0, 0.2, 0.5),  # Electrode 2
    (0.2, 0.0, 0.5),  # Electrode 3
    (0.2, 0.2, 0.5),  # Electrode 4
)

print(f"Number of electrodes: {len(electrode_array)}")

# Access individual electrode positions
for i, position in enumerate(electrode_array):
    x, y, z = position  # Unpack each coordinate
    print(f"Electrode {i + 1}: x={x}mm, y={y}mm, depth={z}mm")
print()
