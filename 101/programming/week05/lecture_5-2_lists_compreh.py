"""
Lecture 5.2: List Comprehensions
"""

voltages = [-70, -65, -60, -55, -50]

# Traditional way - 4 lines
depolarized = []
for v in voltages:
    depolarized.append(v + 10)
print(depolarized)  # [-60, -55, -50, -45, -40]

# List comprehension - same result, one line!
depolarized = [v + 10 for v in voltages]
print(depolarized)  # [-60, -55, -50, -45, -40]
print()

voltages = [-70, -65, -60, -55, -50, -45]
threshold = -55

# Traditional way - 5 lines
above_threshold = []
for v in voltages:
    if v >= threshold:
        above_threshold.append(v)

# List comprehension with condition - 1 line, same result
above_threshold = [v for v in voltages if v >= threshold]
print(above_threshold)  # [-55, -50, -45]

print()
# Convert millivolts to microvolts (multiply by 1000)
mv_readings = [-70.0, -65.5, -60.2, -55.8, -50.1]
uv_readings = [v * 1000 for v in mv_readings]
print(uv_readings)  # [-70000.0, -65500.0, -60200.0, -55800.0, -50100.0]

print()
# Raw voltage recording — most values are subthreshold noise
all_voltages = [-70, -68, -65, -58, -52, -56, -70, -45, -70]
threshold = -55

# Extract only the spike voltages
spike_voltages = [v for v in all_voltages if v >= threshold]
print(f"Spike voltages: {spike_voltages}")  # [-52, -45]
print(f"Spikes detected: {len(spike_voltages)} out of {len(all_voltages)} readings")

print()
# Generate IDs for 10 neurons: N001, N002, ... N010
# f"N{i:03d}" formats the number with leading zeros to 3 digits
neuron_ids = [f"N{i:03d}" for i in range(1, 11)]
print(neuron_ids)  # ['N001', 'N002', 'N003', ..., 'N010']

print()
# Spike counts for 8 neurons over a 10-second recording
spike_counts = [15, 23, 8, 31, 19, 42, 5, 27]
duration = 10  # seconds

# Calculate firing rate (Hz) for every neuron at once
firing_rates = [count / duration for count in spike_counts]
print(firing_rates)  # [1.5, 2.3, 0.8, 3.1, 1.9, 4.2, 0.5, 2.7]

# Find only the fast-firing neurons (above 2 Hz)
fast_neurons = [rate for rate in firing_rates if rate > 2.0]
print(f"Fast-firing neurons: {fast_neurons}")  # [2.3, 3.1, 4.2, 2.7]
print(f"Count: {len(fast_neurons)} out of {len(firing_rates)} neurons")

# Format the rates nicely for a report
formatted_rates = [f"{rate:.1f} Hz" for rate in firing_rates]
print(formatted_rates)
