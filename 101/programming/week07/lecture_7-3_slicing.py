"""
Lecture 7.3: Array Indexing and Slicing
"""

import numpy as np

spike_times = np.array([5.2, 10.1, 15.8, 20.3, 25.9, 30.4, 35.7, 40.2])

print(spike_times[0])  # 5.2  — first spike
print(spike_times[-1])  # 40.2 — last spike
print(spike_times[2:5])  # [15.8 20.3 25.9] — spikes 2, 3, and 4
print(spike_times[:3])  # [5.2 10.1 15.8]  — first three spikes
print(spike_times[::2])  # [5.2 15.8 25.9 35.7] — every other spike
print()

# One important difference from lists: NumPy slices return a view, not a copy.
# If you modify the slice, you modify the original array.
# If you want an independent copy, call .copy() explicitly: spike_times[2:5].copy().

voltages = np.array([-70, -68, -65, -58, -52, -56, -70, -45, -70])
threshold = -55

# Select only voltages at or above threshold
above_threshold = voltages[voltages >= threshold]
print(f"Above threshold: {above_threshold}")  # [-52 -45]

# Find the indices where threshold was crossed
spike_indices = np.where(voltages >= threshold)[0]
print(f"Spike indices: {spike_indices}")  # [4 7]

# Count threshold crossings
n_spikes = np.sum(voltages >= threshold)
print(f"Number of spikes: {n_spikes}")  # 2

# Combine conditions with & (and) and | (or)
moderate = voltages[(voltages >= -65) & (voltages <= -55)]
print(f"Moderate voltages: {moderate}")  # [-65 -58 -56]
print()

# 4 neurons x 5 time bins — spike counts
activity = np.array(
    [
        [5, 10, 15, 8, 12],  # Neuron 0
        [3, 7, 20, 4, 9],  # Neuron 1
        [8, 12, 18, 6, 14],  # Neuron 2
        [2, 5, 8, 3, 6],  # Neuron 3
    ]
)

print(f"Shape: {activity.shape}")  # (4, 5) — 4 rows, 5 columns

print(activity[0, 2])  # 15  — Neuron 0 at time bin 2
print(activity[1, :])  # [ 3  7 20  4  9] — all time bins for Neuron 1
print(activity[:, 2])  # [15 20 18  8] — all neurons at time bin 2
print(activity[1:3, 2:4])  # Neurons 1-2, time bins 2-3 — a submatrix
print()

# Simulated voltage trace: 1000 time points at 1ms resolution
np.random.seed(42)
voltage_trace = np.random.normal(-70, 5, 1000)

# Simulate 5 stimulus onset times (in milliseconds)
stimulus_times = np.array([100, 250, 400, 600, 800])

# Extract a 100ms window (-20ms to +80ms) around each stimulus
pre = 20  # ms before stimulus
post = 80  # ms after stimulus

windows = []
for onset in stimulus_times:
    window = voltage_trace[onset - pre : onset + post]
    windows.append(window)

# Stack into a 2D array: trials x time points
trials = np.array(windows)
print(f"Trials shape: {trials.shape}")  # (5, 100)

# Average across trials — the event-related potential (ERP)
erp = trials.mean(axis=0)
print(f"ERP shape: {erp.shape}")  # (100,) — one value per time point
print(f"Peak ERP voltage: {erp.max():.2f} mV")
print()
