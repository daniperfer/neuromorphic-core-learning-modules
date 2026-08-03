"""
Lecture 12.1: What Is a Spike Train? Representing Neural Firing in Python
"""

import matplotlib.pyplot as plt
import numpy as np

# Reproducible simulation — use this seed throughout Week 12
np.random.seed(42)

# Simulation parameters
recording_duration = 10.0  # seconds
mean_firing_rate = 20.0  # Hz (spikes per second)

# Draw interspike intervals from exponential distribution
# Expected number of spikes ≈ rate * duration = 200, generate extras for safety
n_spikes_expected = int(mean_firing_rate * recording_duration * 2)
isis = np.random.exponential(scale=1.0 / mean_firing_rate, size=n_spikes_expected)

# Cumulative sum gives spike times; keep only those within the recording window
spike_times = np.cumsum(isis)
spike_times = spike_times[spike_times < recording_duration]

print(f"Total spikes: {len(spike_times)}")
print(f"First five spike times (s): {spike_times[:5].round(4)}")
print(f"Last spike time (s): {spike_times[-1]:.4f}")
print(f"Empirical firing rate: {len(spike_times) / recording_duration:.2f} Hz")

# Save for use in subsequent lectures
filename = "week12_simulated_spikes"
np.save(f"{filename}.npy", spike_times)
print(f"Saved: {filename}.npy")
print()

# Load the spike train
spike_times = np.load(f"{filename}.npy")

# Basic metadata
recording_duration = 10.0  # seconds — stored separately, not in the array
n_spikes = len(spike_times)
firing_rate = n_spikes / recording_duration

print(f"Number of spikes:    {n_spikes}")
print(f"Recording duration:  {recording_duration:.1f} s")
print(f"Mean firing rate:    {firing_rate:.2f} Hz")
print(f"First spike at:      {spike_times[0]:.4f} s")
print(f"Last spike at:       {spike_times[-1]:.4f} s")
print(f"Array dtype:         {spike_times.dtype}")

# Sanity checks — always run these when loading a spike train
assert spike_times.ndim == 1, "Spike train must be 1D"
assert np.all(spike_times >= 0), "All spike times must be non-negative"
assert np.all(np.diff(spike_times) > 0), "Spike times must be strictly increasing"
assert spike_times[-1] < recording_duration, "Last spike must be within recording window"

print("All sanity checks passed.")
print()


spike_times = np.load(f"{filename}.npy")
recording_duration = 10.0

fig, axes = plt.subplots(2, 1, figsize=(12, 5))

# --- Top panel: raster plot ---
axes[0].eventplot(spike_times, lineoffsets=0, linelengths=0.8, color="black", linewidths=0.8)
axes[0].set_xlim(0, recording_duration)
axes[0].set_ylim(-1, 1)
axes[0].set_yticks([])
axes[0].set_xlabel("Time (s)")
axes[0].set_title("Raster Plot — Single Neuron, 10-Second Recording")

# --- Bottom panel: zoom into first second ---
mask = spike_times < 1.0
axes[1].eventplot(
    spike_times[mask], lineoffsets=0, linelengths=0.8, color="steelblue", linewidths=1.2
)
axes[1].set_xlim(0, 1.0)
axes[1].set_ylim(-1, 1)
axes[1].set_yticks([])
axes[1].set_xlabel("Time (s)")
axes[1].set_title("Zoomed: First Second (irregular spacing visible at this scale)")

plt.tight_layout()
plt.savefig("figure_12-1-1_raster_plot.png", dpi=150, bbox_inches="tight")
print()
