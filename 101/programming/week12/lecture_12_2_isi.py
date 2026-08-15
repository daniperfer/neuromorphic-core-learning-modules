"""
Lecture 12.2: Interspike Interval Analysis
"""

import matplotlib.pyplot as plt
import numpy as np

spike_times = np.load("week12_simulated_spikes.npy")
recording_duration = 10.0

isis = np.diff(spike_times)

print(f"Number of spikes:       {len(spike_times)}")
print(f"Number of ISIs:         {len(isis)}")
print(f"Mean ISI:               {isis.mean() * 1000:.2f} ms")
print(f"Median ISI:             {np.median(isis) * 1000:.2f} ms")
print(f"Min ISI:                {isis.min() * 1000:.2f} ms")
print(f"Max ISI:                {isis.max() * 1000:.2f} ms")
print()

recording_duration = 10.0
isis = np.diff(spike_times)

fig, axes = plt.subplots(1, 2, figsize=(13, 4))

# --- Left panel: ISI histogram in milliseconds ---
axes[0].hist(isis * 1000, bins=40, color="steelblue", edgecolor="white", linewidth=0.5)
axes[0].set_xlabel("Interspike Interval (ms)")
axes[0].set_ylabel("Count")
axes[0].set_title("ISI Histogram — Poisson Spike Train (~20 Hz)")

# Overlay the theoretical exponential distribution
mean_rate = len(spike_times) / recording_duration
x_ms = np.linspace(0, isis.max() * 1000, 300)
x_s = x_ms / 1000
n_isis = len(isis)
bin_width_ms = (isis.max() * 1000) / 40
theoretical = n_isis * bin_width_ms / 1000 * mean_rate * np.exp(-mean_rate * x_s)
axes[0].plot(x_ms, theoretical, "r--", linewidth=2, label="Theoretical exponential")
axes[0].legend()

# --- Right panel: log-scale ISI histogram (linearizes the exponential) ---
counts, edges = np.histogram(isis * 1000, bins=40)
centers = (edges[:-1] + edges[1:]) / 2
nonzero = counts > 0
axes[1].bar(
    centers[nonzero],
    np.log(counts[nonzero]),
    width=np.diff(edges)[0],
    color="coral",
    edgecolor="white",
    linewidth=0.5,
)
axes[1].set_xlabel("Interspike Interval (ms)")
axes[1].set_ylabel("log(Count)")
axes[1].set_title("ISI Histogram (Log Scale) — Exponential Appears Linear")

plt.tight_layout()
plt.savefig("figure_12-2-1_isi_histogram.png", dpi=150, bbox_inches="tight")
print()


cv = isis.std() / isis.mean()
print(f"Mean ISI:   {isis.mean() * 1000:.2f} ms")
print(f"Std ISI:    {isis.std() * 1000:.2f} ms")
print(f"CV (coefficient of variation): {cv:.4f}")

if cv < 0.5:
    regime = "highly regular (clock-like)"
elif cv < 0.8:
    regime = "sub-Poisson (moderately regular)"
elif cv < 1.2:
    regime = "approximately Poisson (random)"
else:
    regime = "super-Poisson (bursty or irregular)"

print(f"Firing regime: {regime}")

# -----------
# Fano factor


def fano_factor(spike_times, recording_duration, window_size=0.5):
    """
    Compute Fano factor using non-overlapping windows.

    Params
    ------
    spike_times      : 1D array of spike timestamps in seconds
    recording_duration : float, total recording length in seconds
    window_size      : float, width of each counting window in seconds

    Returns
    -------
    fano : float
    counts : 1D array of spike counts per window
    """
    edges = np.arange(0, recording_duration + window_size, window_size)
    counts, _ = np.histogram(spike_times, bins=edges)
    # Drop the last bin if it is shorter than window_size
    n_full = int(recording_duration / window_size)
    counts = counts[:n_full]
    fano = counts.var() / counts.mean()
    return fano, counts


window_size = 0.5
fano, counts = fano_factor(spike_times, recording_duration, window_size=window_size)

print(f"Window size:        {window_size} s")
print(f"Number of windows:  {len(counts)}")
print(f"Mean spike count:   {counts.mean():.2f} per window")
print(f"Var spike count:    {counts.var():.2f}")
print(f"Fano factor:        {fano:.4f}")
print()

window_sizes = [0.1, 0.25, 0.5, 1.0, 2.0, 3.0]
fano_values = []
for ws in window_sizes:
    f, _ = fano_factor(spike_times, recording_duration, window_size=ws)
    fano_values.append(f)

fig, ax = plt.subplots(figsize=(7, 4))
ax.semilogx(window_sizes, fano_values, "o-", color="steelblue", markersize=7)
ax.axhline(1.0, color="red", linestyle="--", linewidth=1.2, label="Poisson baseline (FF=1)")
ax.axhline(cv, color="green", linestyle=":", linewidth=1.2, label=f"CV = {cv:.2f}")
ax.set_xlabel("Window Size (s, log scale)")
ax.set_ylabel("Fano Factor")
ax.set_title("Fano Factor vs Window Size")
ax.legend()
plt.tight_layout()
plt.savefig("figure_12-2-2_fano_vs_window.png", dpi=150, bbox_inches="tight")
print()

# ------------------------
# An ISI Analysis function


def isi_statistics(spike_times, recording_duration):
    """
    Compute ISI statistics for a single spike train.

    Params
    ------
    spike_times        : 1D array of spike timestamps in seconds (sorted, non-negative)
    recording_duration : float, total recording duration in seconds

    Returns
    -------
    stats : dict with keys:
        n_spikes, mean_firing_rate, mean_isi_ms, median_isi_ms,
        std_isi_ms, min_isi_ms, max_isi_ms, cv, fano_factor
    """
    n_spikes = len(spike_times)
    isis = np.diff(spike_times)

    # Fano factor with 0.5 s windows
    edges = np.arange(0, recording_duration + 0.5, 0.5)
    counts = np.histogram(spike_times, bins=edges)[0]
    n_full = int(recording_duration / 0.5)
    counts = counts[:n_full]
    fano = counts.var() / counts.mean() if counts.mean() > 0 else np.nan

    stats = {
        "n_spikes": n_spikes,
        "mean_firing_rate": n_spikes / recording_duration,
        "mean_isi_ms": isis.mean() * 1000,
        "median_isi_ms": np.median(isis) * 1000,
        "std_isi_ms": isis.std() * 1000,
        "min_isi_ms": isis.min() * 1000,
        "max_isi_ms": isis.max() * 1000,
        "cv": isis.std() / isis.mean(),
        "fano_factor": fano,
    }
    return stats


# Demo
spike_times = np.load("week12_simulated_spikes.npy")
stats = isi_statistics(spike_times, recording_duration=10.0)

print("ISI Statistics Summary")
print("=" * 35)
for key, val in stats.items():
    if isinstance(val, float):
        print(f"  {key:<22} {val:.4f}")
    else:
        print(f"  {key:<22} {val}")
print()
