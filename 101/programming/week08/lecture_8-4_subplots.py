"""
Lecture 8.4: Subplots and Figure Layout
"""

import matplotlib.pyplot as plt
import numpy as np

np.random.seed(42)

fig, axes = plt.subplots(2, 3, figsize=(15, 10))
fig.suptitle("Complete Neuron Analysis", fontsize=16, fontweight="bold")

# --- Panel [0,0]: Raw membrane potential ---
t = np.linspace(0, 100, 1000)
voltage = -70 + np.random.randn(1000) * 2
axes[0, 0].plot(t, voltage, "k-", linewidth=0.8)
axes[0, 0].set_title("Membrane Potential")
axes[0, 0].set_xlabel("Time (ms)")
axes[0, 0].set_ylabel("Voltage (mV)")

# --- Panel [0,1]: Spike count distribution across trials ---
spike_counts = np.random.poisson(15, 100)
axes[0, 1].hist(spike_counts, bins=15, color="steelblue", edgecolor="white")
axes[0, 1].set_title("Spike Count Distribution")
axes[0, 1].set_xlabel("Spikes per Trial")
axes[0, 1].set_ylabel("Count")

# --- Panel [0,2]: Interspike interval distribution ---
isi = np.random.exponential(50, 200)
axes[0, 2].hist(isi, bins=20, color="coral", edgecolor="white")
axes[0, 2].set_title("ISI Distribution")
axes[0, 2].set_xlabel("ISI (ms)")
axes[0, 2].set_ylabel("Count")

# --- Panel [1,0]: Firing rate over time ---
time_bins = np.arange(0, 100, 10)
rates = np.random.uniform(10, 30, len(time_bins))
axes[1, 0].bar(time_bins, rates, width=8, color="green", alpha=0.7)
axes[1, 0].set_title("Firing Rate Over Time")
axes[1, 0].set_xlabel("Time (ms)")
axes[1, 0].set_ylabel("Rate (Hz)")

# --- Panel [1,1]: Stimulus-response scatter ---
stim = np.random.uniform(0, 100, 50)
response = stim * 0.4 + np.random.randn(50) * 5
axes[1, 1].scatter(stim, response, alpha=0.6, color="purple")
axes[1, 1].set_title("Stimulus-Response")
axes[1, 1].set_xlabel("Stimulus Intensity")
axes[1, 1].set_ylabel("Firing Rate (Hz)")

# --- Panel [1,2]: Direction tuning curve ---
angles = np.linspace(0, 360, 37)
tuning = 20 + 15 * np.cos(np.radians(angles - 90))
axes[1, 2].plot(angles, tuning, "r-o", markersize=4)
axes[1, 2].set_title("Direction Tuning Curve")
axes[1, 2].set_xlabel("Direction (degrees)")
axes[1, 2].set_ylabel("Firing Rate (Hz)")

plt.tight_layout()
plt.savefig("figure_8-4-1_plot_grid.png", dpi=300, bbox_inches="tight")
print("Plot grid example completed...")

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Flatten to a 1D list for easy iteration
axes_flat = axes.flatten()

# Now you can index sequentially: axes_flat[0] through axes_flat[5]
for i, ax in enumerate(axes_flat):
    ax.set_title(f"Panel {i + 1}")
    ax.text(
        0.5,
        0.5,
        f"Plot {i + 1}",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=14,
        color="gray",
    )

for ax, letter in zip(axes_flat, "ABCDEF"):
    ax.text(-0.1, 1.05, letter, transform=ax.transAxes, fontsize=14, fontweight="bold")

plt.tight_layout()
plt.savefig("figure_8-4-2_flatten_grid.png", dpi=300, bbox_inches="tight")
print("Flatten grid example completed")

# All panels share the same x-axis (time)
fig, axes = plt.subplots(3, 1, figsize=(12, 9), sharex=True)

t = np.linspace(0, 500, 5000)

axes[0].plot(t, -70 + np.random.randn(5000) * 2, "k-", linewidth=0.5)
axes[0].set_ylabel("Voltage (mV)")
axes[0].set_title("Multi-Channel Recording")

axes[1].plot(t, np.random.randn(5000) * 0.5, "b-", linewidth=0.5)
axes[1].set_ylabel("LFP (mV)")

axes[2].plot(t, np.cumsum(np.random.poisson(0.05, 5000)), "g-", linewidth=1)
axes[2].set_ylabel("Cumulative Spikes")
axes[2].set_xlabel("Time (ms)")

plt.tight_layout()
plt.savefig("figure_8-4-3_shared_axes.png", dpi=300, bbox_inches="tight")
print("Shared axes  example completed")
