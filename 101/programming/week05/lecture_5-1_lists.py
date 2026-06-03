"""
Lecture 5.1: Advanced List Operations
"""

# Basic list review
spike_times = [10.5, 23.1, 45.7, 67.2, 89.0]
print(spike_times[0])  # First item: 10.5
print(spike_times[-1])  # Last item: 89.0
print(len(spike_times))  # Length: 5
print()

neuron_voltages = [-70.0, -65.0, -60.0, -55.0]

# append() - add one item to the END of the list
# Use this when a new recording comes in
neuron_voltages.append(-50.0)
print(neuron_voltages)  # [-70.0, -65.0, -60.0, -55.0, -50.0]

# insert() - add an item at a SPECIFIC position
# Use this when you need to insert data at a precise location
neuron_voltages.insert(0, -75.0)  # Insert at beginning (index 0)
print(neuron_voltages)  # [-75.0, -70.0, -65.0, -60.0, -55.0, -50.0]

# remove() - remove the FIRST occurrence of a value
# Use this to clean up specific unwanted values
neuron_voltages.remove(-75.0)
print(neuron_voltages)  # [-70.0, -65.0, -60.0, -55.0, -50.0]

# pop() - remove and RETURN an item by index
# Use this when you want to take an item out AND use its value
last = neuron_voltages.pop()  # No index = removes last item
print(last)  # -50.0
print(neuron_voltages)  # [-70.0, -65.0, -60.0, -55.0]

print()
# sort() - arrange items in order (modifies the list directly!)
spike_times = [45.7, 10.5, 89.0, 23.1]
spike_times.sort()
print(spike_times)  # [10.5, 23.1, 45.7, 89.0]

# reverse() - flip the order of the list
spike_times.reverse()
print(spike_times)  # [89.0, 45.7, 23.1, 10.5]

# count() - count how many times a value appears
# Extremely useful for analyzing neuron types in a dataset
neuron_types = ["pyramidal", "interneuron", "pyramidal", "pyramidal"]
print(neuron_types.count("pyramidal"))  # 3

# index() - find the POSITION of a value
# Returns the index of the first match
print(neuron_types.index("interneuron"))  # 1

original = [45.7, 10.5, 89.0, 23.1]
sorted_copy = sorted(original)  # sorted() returns a NEW list, original unchanged
print(original)  # [45.7, 10.5, 89.0, 23.1] - unchanged!
print(sorted_copy)  # [10.5, 23.1, 45.7, 89.0] - new sorted list

print()
voltages = [-70, -65, -60, -55, -50, -45, -40]
#  index:    0    1    2    3    4    5    6

# Basic slice [start:stop] — items from index 1 up to (not including) index 4
print(voltages[1:4])  # [-65, -60, -55]

# Omit start — begins from the very beginning of the list
print(voltages[:3])  # [-70, -65, -60]

# Omit stop — goes all the way to the end
print(voltages[4:])  # [-50, -45, -40]

# Step of 2 — take every other item
print(voltages[::2])  # [-70, -60, -50, -40]

# Negative step — reverse the list!
print(voltages[::-1])  # [-40, -45, -50, -55, -60, -65, -70]

# Putting It Together: Spike Train Analysis
# Analyze spike times from a 40ms recording
# Times are in milliseconds
spike_train = [5.2, 10.1, 15.8, 20.3, 25.9, 30.4, 35.7, 40.2]

print()
print("=== SPIKE TRAIN ANALYSIS ===")
print(f"Total spikes recorded: {len(spike_train)}")
print(f"Recording duration: {spike_train[-1] - spike_train[0]:.1f} ms")
print()

# Get first 3 spikes (early response)
early_spikes = spike_train[:3]
print(f"Early spikes (first 3): {early_spikes}")

# Get last 3 spikes (late response)
late_spikes = spike_train[-3:]
print(f"Late spikes (last 3): {late_spikes}")
print()

# Calculate inter-spike intervals (ISI)
# ISI = time between consecutive spikes
# This tells us how regularly the neuron is firing
isi = []
for i in range(1, len(spike_train)):
    interval = spike_train[i] - spike_train[i - 1]
    isi.append(round(interval, 2))

print(f"Inter-spike intervals (ms): {isi}")
print(f"Average ISI: {sum(isi) / len(isi):.2f} ms")
print(f"Shortest ISI: {min(isi):.2f} ms")
print(f"Longest ISI: {max(isi):.2f} ms")

# Firing rate = 1000 / average ISI (converting ms to Hz)
firing_rate = 1000 / (sum(isi) / len(isi))
print(f"Average firing rate: {firing_rate:.1f} Hz")
