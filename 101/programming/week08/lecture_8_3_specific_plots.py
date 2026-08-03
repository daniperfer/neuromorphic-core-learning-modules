"""
Lecture 8.3: Neuroscience-Specific Visualizations
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_raster(spike_trains, title="Raster Plot"):
    """
    Draws vertical ticks for each spike in a trial
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    for trial_idx, spikes in enumerate(spike_trains):
        # Draw vertical ticks for each spike in this trial
        ax.vlines(spikes, trial_idx + 0.5, trial_idx + 1.5, colors="black", linewidth=0.8)

    ax.set_xlim(0, 1000)
    ax.set_ylim(0, len(spike_trains) + 1)
    ax.set_xlabel("Time (ms)", fontsize=12)
    ax.set_ylabel("Trial", fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.axvline(x=200, color="red", linestyle="--", linewidth=2, label="Stimulus onset")
    ax.legend()
    plt.tight_layout()
    plt.savefig("figure_8-3-1_spike_raster_plot.png", dpi=300, bbox_inches="tight")
    return fig, ax


# Simulate 30 trials
np.random.seed(42)
n_trials = 30
spike_trains = []

for trial in range(n_trials):
    background = np.sort(np.random.uniform(0, 1000, 5))  # ~5 Hz background
    response = np.sort(np.random.uniform(200, 400, np.random.poisson(8)))  # Burst after stimulus
    spikes = np.sort(np.concatenate([background, response]))
    spike_trains.append(spikes)

plot_raster(spike_trains, title="Spike Raster Plot")
print("Spike Raster Plot example completed...")


def plot_psth(spike_trains, duration=1000, bin_size=20, stimulus_time=200, title="PSTH"):
    """
    Build histogram bins and count spikes across all trials
    """
    bins = np.arange(0, duration + bin_size, bin_size)
    all_spikes = np.concatenate(spike_trains)
    counts, edges = np.histogram(all_spikes, bins=bins)

    # Convert to firing rate: spikes per trial per second
    n_trials = len(spike_trains)
    rates = (counts / n_trials) / (bin_size / 1000)
    bin_centers = (edges[:-1] + edges[1:]) / 2

    # Two-panel figure: raster on top, PSTH on bottom
    fig, axes = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={"height_ratios": [2, 1]})

    # Top panel: raster (first 20 trials for clarity)
    for trial_idx, spikes in enumerate(spike_trains[:20]):
        axes[0].vlines(spikes, trial_idx + 0.5, trial_idx + 1.5, colors="black", linewidth=0.5)
    axes[0].axvline(stimulus_time, color="red", linestyle="--", linewidth=2)
    axes[0].set_ylabel("Trial")
    axes[0].set_title(title)

    # Bottom panel: PSTH as a bar chart
    axes[1].bar(
        bin_centers, rates, width=bin_size * 0.9, color="steelblue", alpha=0.8, edgecolor="white"
    )
    axes[1].axvline(stimulus_time, color="red", linestyle="--", linewidth=2, label="Stimulus")
    axes[1].set_xlabel("Time (ms)")
    axes[1].set_ylabel("Firing Rate (Hz)")
    axes[1].legend()

    plt.tight_layout()
    plt.savefig("figure_8-3-2_raster_psth_plot.png", dpi=300, bbox_inches="tight")
    return fig


plot_psth(spike_trains, title="Raster & PSTH")
print("PSTH and Raster Plot examples completed...")

np.random.seed(42)
n_neurons = 20
n_bins = 100

# Simulate population activity: baseline Poisson noise
activity = np.random.poisson(3, (n_neurons, n_bins)).astype(float)

# Add a travelling wave: each neuron has a brief peak at a different time
for i in range(n_neurons):
    peak_time = int(i * (n_bins / n_neurons) + 20)
    if peak_time < n_bins:
        activity[i, max(0, peak_time - 5) : peak_time + 5] += 10

fig, ax = plt.subplots(figsize=(14, 8))

# imshow treats the array as an image: rows=neurons, columns=time bins
im = ax.imshow(
    activity,
    aspect="auto",  # Don't force square pixels
    cmap="hot",  # Dark=low, bright=high activity
    interpolation="nearest",
    extent=[0, 1000, n_neurons + 0.5, 0.5],
)  # Map pixels to real units

plt.colorbar(im, ax=ax, label="Spike Count")
ax.axvline(x=200, color="cyan", linestyle="--", linewidth=2, label="Stimulus")
ax.set_xlabel("Time (ms)", fontsize=12)
ax.set_ylabel("Neuron #", fontsize=12)
ax.set_title("Neural Population Activity Heatmap", fontsize=14)
ax.legend()
plt.tight_layout()
plt.savefig("figure_8-3-3_population_heatmap_plot.png", dpi=300, bbox_inches="tight")
print("Population Heatmap Plot example completed...")
