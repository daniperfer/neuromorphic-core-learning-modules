"""
Lecture 12.3: Firing Rate Estimation — Bin Counting and Kernel Smoothing
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d

np.random.seed(42)

spike_times = np.load("week12_simulated_spikes.npy")
recording_duration = 10.0

# ------------------------------
# Method 1: Bin Count Histograms


def bin_firing_rate(spike_times, recording_duration, bin_width):
    """
    Estimate firing rate using non-overlapping time bins.

    Params
    ------
    spike_times        : 1D array of spike timestamps in seconds
    recording_duration : float, total recording duration in seconds
    bin_width          : float, bin width in seconds

    Returns
    -------
    bin_centers : 1D array of bin center times (seconds)
    rate_hz     : 1D array of firing rate estimates (Hz)
    """
    edges = np.arange(0, recording_duration + bin_width, bin_width)
    counts, _ = np.histogram(spike_times, bins=edges)
    rate_hz = counts / bin_width  # convert counts to Hz
    bin_centers = (edges[:-1] + edges[1:]) / 2
    # Keep only full bins within the recording
    n_full = int(recording_duration / bin_width)
    return bin_centers[:n_full], rate_hz[:n_full]


# Compare three bin widths
bin_widths = [0.05, 0.2, 0.5]  # 50 ms, 200 ms, 500 ms
colors = ["steelblue", "coral", "seagreen"]

fig, axes = plt.subplots(3, 1, figsize=(13, 8), sharex=True)

for ax, bw, color in zip(axes, bin_widths, colors):
    centers, rates = bin_firing_rate(spike_times, recording_duration, bw)
    ax.bar(
        centers,
        rates,
        width=bw * 0.9,
        color=color,
        alpha=0.75,
        label=f"Bin width = {bw * 1000:.0f} ms",
    )
    ax.axhline(
        len(spike_times) / recording_duration,
        color="black",
        linestyle="--",
        linewidth=1.0,
        label="Mean rate",
    )
    ax.set_ylabel("Firing Rate (Hz)")
    ax.legend(loc="upper right")
    ax.set_ylim(0, None)

axes[-1].set_xlabel("Time (s)")
axes[0].set_title("Bin-Count Firing Rate Estimates — Effect of Bin Width")
plt.tight_layout()
plt.savefig("figure_12-3-1_bin_firing_rate.png", dpi=150, bbox_inches="tight")
print("Bin counting example completed...")

# ---------------------------------------
# The Peri-Stimulus Time Histogram (PSTH)

recording_duration = 1.0  # 1 second per trial
n_trials = 30
baseline_rate = 10.0  # Hz before stimulus
response_rate = 60.0  # Hz during stimulus window
stimulus_onset = 0.3  # seconds into trial
response_duration = 0.15  # seconds


def simulate_trial(baseline_rate, response_rate, stimulus_onset, response_duration, duration):
    """Simulate one trial with a transient firing rate increase."""
    spikes = []
    t = 0.0
    while t < duration:
        # Rate depends on whether we are in the response window
        if stimulus_onset <= t < stimulus_onset + response_duration:
            rate = response_rate
        else:
            rate = baseline_rate
        isi = np.random.exponential(1.0 / rate)
        t += isi
        if t < duration:
            spikes.append(t)
    return np.array(spikes)


all_trials = [
    simulate_trial(
        baseline_rate, response_rate, stimulus_onset, response_duration, recording_duration
    )
    for _ in range(n_trials)
]

# Build PSTH: average spike count per bin across trials
bin_width = 0.02  # 20 ms bins
edges = np.arange(0, recording_duration + bin_width, bin_width)
psth_counts = np.zeros(len(edges) - 1)

for trial_spikes in all_trials:
    counts, _ = np.histogram(trial_spikes, bins=edges)
    psth_counts += counts

psth_rate = psth_counts / (n_trials * bin_width)
bin_centers = (edges[:-1] + edges[1:]) / 2

fig, axes = plt.subplots(2, 1, figsize=(12, 7))

# Raster plot
for i, trial_spikes in enumerate(all_trials):
    axes[0].eventplot(trial_spikes, lineoffsets=i, linelengths=0.7, color="black", linewidths=0.6)
axes[0].axvspan(
    stimulus_onset,
    stimulus_onset + response_duration,
    alpha=0.15,
    color="red",
    label="Stimulus window",
)
axes[0].set_xlim(0, recording_duration)
axes[0].set_ylabel("Trial")
axes[0].set_title("Raster Plot — 30 Trials Aligned to Stimulus Onset")
axes[0].legend()

# PSTH
axes[1].bar(bin_centers, psth_rate, width=bin_width * 0.9, color="steelblue", alpha=0.8)
axes[1].axvspan(
    stimulus_onset,
    stimulus_onset + response_duration,
    alpha=0.15,
    color="red",
    label="Stimulus window",
)
axes[1].set_xlabel("Time from stimulus onset (s)")
axes[1].set_ylabel("Firing Rate (Hz)")
axes[1].set_title(f"PSTH — {n_trials} Trials, {bin_width * 1000:.0f} ms Bins")
axes[1].legend()

plt.tight_layout()
plt.savefig("figure_12-3-2_psth.png", dpi=150, bbox_inches="tight")
print("PSTH example completed...")

# -----------------------------------
# Method 2: Gaussian Kernel Smoothing


def kernel_firing_rate(spike_times, recording_duration, sigma_ms, dt_ms=1.0):
    """
    Estimate firing rate using Gaussian kernel smoothing.

    Params
    ------
    spike_times        : 1D array of spike timestamps in seconds
    recording_duration : float, total recording duration in seconds
    sigma_ms           : float, Gaussian kernel width in milliseconds
    dt_ms              : float, time resolution of the output in milliseconds

    Returns
    -------
    time_axis : 1D array of time points (seconds)
    rate_hz   : 1D array of smoothed firing rate (Hz)
    """
    dt_s = dt_ms / 1000.0
    n_bins = int(recording_duration / dt_s)
    # Create binary spike train sampled at dt resolution
    binary = np.zeros(n_bins)
    indices = (spike_times / dt_s).astype(int)
    indices = indices[indices < n_bins]
    binary[indices] = 1.0

    # Convert sigma from ms to samples
    sigma_samples = sigma_ms / dt_ms

    # Gaussian smooth, then convert from spikes/sample to Hz
    smoothed = gaussian_filter1d(binary, sigma=sigma_samples)
    rate_hz = smoothed / dt_s

    time_axis = np.arange(n_bins) * dt_s
    return time_axis, rate_hz


fig, axes = plt.subplots(3, 1, figsize=(13, 8), sharex=True)

sigmas = [10, 50, 150]  # ms
colors = ["steelblue", "coral", "seagreen"]

for ax, sigma, color in zip(axes, sigmas, colors):
    t, rate = kernel_firing_rate(spike_times, recording_duration, sigma_ms=sigma)
    ax.plot(t, rate, color=color, linewidth=1.2, label=f"σ = {sigma} ms")
    ax.axhline(
        len(spike_times) / recording_duration,
        color="black",
        linestyle="--",
        linewidth=0.9,
        label="Mean rate",
    )
    ax.set_ylabel("Firing Rate (Hz)")
    ax.legend(loc="upper right")

axes[-1].set_xlabel("Time (s)")
axes[0].set_title("Gaussian Kernel Smoothing — Effect of Bandwidth (σ)")
plt.tight_layout()
plt.savefig("figure_12-3-3_kernel_smoothing.png", dpi=150, bbox_inches="tight")
print("Gaussian Kernel Smoothing example completed...")

# --------------------------------------
# Comparing Histogram and Kernel Methods

# Bin-count estimate
bin_width = 0.1  # 100 ms
edges = np.arange(0, recording_duration + bin_width, bin_width)
counts, _ = np.histogram(spike_times, bins=edges)
bin_rate = counts / bin_width
bin_centers = (edges[:-1] + edges[1:]) / 2

# Kernel estimate
t_kernel, rate_kernel = kernel_firing_rate(spike_times, recording_duration, sigma_ms=50)

fig, ax = plt.subplots(figsize=(13, 4))
ax.bar(
    bin_centers,
    bin_rate,
    width=bin_width * 0.9,
    color="steelblue",
    alpha=0.5,
    label="Histogram (100 ms bins)",
)
ax.plot(t_kernel, rate_kernel, color="coral", linewidth=2.0, label="Kernel smooth (σ=50 ms)")
ax.axhline(
    len(spike_times) / recording_duration,
    color="black",
    linestyle="--",
    linewidth=1.0,
    label="Mean rate",
)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Firing Rate (Hz)")
ax.set_title("Histogram vs Kernel Smoothing — Same Spike Train")
ax.legend()
plt.tight_layout()
plt.savefig("figure_12-3-4_histogram_vs_kernel.png", dpi=150, bbox_inches="tight")
print("Comparison example completed...")
