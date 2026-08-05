"""
Lecture 12.5: Cross-Correlogram and Synchrony Between Neurons
"""

import matplotlib.pyplot as plt
import numpy as np

np.random.seed(7)

spike_times_A = np.load("week12_simulated_spikes.npy")
recording_duration = 10.0

# --- Simulate Neuron B ---
# Neuron B fires independently at 15 Hz (baseline Poisson)
# plus has a 30% chance of firing ~5 ms after each spike in A (jittered)

baseline_rate = 15.0
n_expected = int(baseline_rate * recording_duration * 2)
isis_B = np.random.exponential(1.0 / baseline_rate, size=n_expected)
spike_times_B = np.cumsum(isis_B)
spike_times_B = spike_times_B[spike_times_B < recording_duration]
spike_times_B = list(spike_times_B)

# Add driven spikes: ~5 ms after each spike in A, with jitter ±1 ms
coupling_prob = 0.30
synaptic_delay_ms = 5.0
jitter_std_ms = 1.0

for t_A in spike_times_A:
    if np.random.rand() < coupling_prob:
        delay = (synaptic_delay_ms + np.random.randn() * jitter_std_ms) / 1000.0
        t_B = t_A + delay
        if 0 < t_B < recording_duration:
            spike_times_B.append(t_B)

spike_times_B = np.array(sorted(spike_times_B))

# Remove any duplicate or too-close spikes (refractory period ~1 ms)
min_isi = 0.001
keep = np.concatenate([[True], np.diff(spike_times_B) > min_isi])
spike_times_B = spike_times_B[keep]

np.save("week12_simulated_spikes_B.npy", spike_times_B)
np.save("week12_simulated_spikes_A.npy", spike_times_A)

print(f"Neuron A: {len(spike_times_A)} spikes  ({len(spike_times_A) / recording_duration:.1f} Hz)")
print(f"Neuron B: {len(spike_times_B)} spikes  ({len(spike_times_B) / recording_duration:.1f} Hz)")
print()

# -------------------
# The Autocorrelogram


def autocorrelogram(spike_times, max_lag_ms=100.0, bin_width_ms=1.0):
    """
    Compute the autocorrelogram of a single spike train.

    For each spike i, finds all other spikes j within ±max_lag_ms and
    records the lag (t_j - t_i). Returns a histogram of those lags,
    excluding zero (a spike cannot co-occur with itself).

    Params
    ------
    spike_times  : 1D array of spike timestamps in seconds
    max_lag_ms   : float, maximum lag in milliseconds
    bin_width_ms : float, bin width in milliseconds

    Returns
    -------
    lags_ms      : 1D array of bin centers in milliseconds
    counts       : 1D array of spike pair counts per bin
    """
    max_lag_s = max_lag_ms / 1000.0
    # bin_width_s = bin_width_ms / 1000.0
    edges_ms = np.arange(-max_lag_ms, max_lag_ms + bin_width_ms, bin_width_ms)

    all_lags = []
    for i, t_ref in enumerate(spike_times):
        # Consider only spikes within the lag window
        window = spike_times[(spike_times > t_ref - max_lag_s) & (spike_times < t_ref + max_lag_s)]
        lags = (window - t_ref) * 1000.0  # convert to ms
        lags = lags[lags != 0]  # exclude zero lag (same spike)
        all_lags.extend(lags)

    counts, edges = np.histogram(all_lags, bins=edges_ms)
    lags_ms = (edges[:-1] + edges[1:]) / 2
    return lags_ms, counts


lags_A, acg_A = autocorrelogram(spike_times_A, max_lag_ms=100.0, bin_width_ms=1.0)
lags_B, acg_B = autocorrelogram(spike_times_B, max_lag_ms=100.0, bin_width_ms=1.0)

fig, axes = plt.subplots(1, 2, figsize=(13, 4), sharey=False)

for ax, lags, acg, label, color in zip(
    axes,
    [lags_A, lags_B],
    [acg_A, acg_B],
    ["Neuron A (Poisson, ~20 Hz)", "Neuron B (Poisson + driven, ~18 Hz)"],
    ["steelblue", "coral"],
):
    ax.bar(lags, acg, width=1.0, color=color, edgecolor="none")
    ax.axvline(0, color="black", linewidth=0.8, linestyle="--")
    ax.set_xlabel("Lag (ms)")
    ax.set_ylabel("Spike pair count")
    ax.set_title(f"Autocorrelogram — {label}")

plt.tight_layout()
plt.savefig("figure_12-5-1_autocorrelogram.png", dpi=150, bbox_inches="tight")
print("Autocorrelogram example completed...")

# -
# The Cross-Correlogram CCG


def cross_correlogram(spike_times_ref, spike_times_target, max_lag_ms=100.0, bin_width_ms=1.0):
    """
    Compute the cross-correlogram between two spike trains.

    For each spike in spike_times_ref, finds all spikes in spike_times_target
    within ±max_lag_ms and records the lag (t_target - t_ref).

    Params
    ------
    spike_times_ref    : 1D array of reference neuron spike times (seconds)
    spike_times_target : 1D array of target neuron spike times (seconds)
    max_lag_ms         : float, maximum lag in milliseconds
    bin_width_ms       : float, bin width in milliseconds

    Returns
    -------
    lags_ms : 1D array of bin centers in milliseconds
    counts  : 1D array of spike pair counts per bin
    """
    max_lag_s = max_lag_ms / 1000.0
    edges_ms = np.arange(-max_lag_ms, max_lag_ms + bin_width_ms, bin_width_ms)

    all_lags = []
    for t_ref in spike_times_ref:
        window = spike_times_target[
            (spike_times_target > t_ref - max_lag_s) & (spike_times_target < t_ref + max_lag_s)
        ]
        lags = (window - t_ref) * 1000.0  # ms
        all_lags.extend(lags)

    counts, edges = np.histogram(all_lags, bins=edges_ms)
    lags_ms = (edges[:-1] + edges[1:]) / 2
    return lags_ms, counts


lags_AB, ccg_AB = cross_correlogram(spike_times_A, spike_times_B, max_lag_ms=50.0, bin_width_ms=0.5)

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(lags_AB, ccg_AB, width=0.5, color="mediumpurple", edgecolor="none")
ax.axvline(0, color="black", linewidth=0.9, linestyle="--", label="Zero lag")
ax.axvline(5, color="red", linewidth=1.2, linestyle=":", label="Expected peak (~5 ms)")
ax.set_xlabel("Lag: t_B − t_A  (ms)")
ax.set_ylabel("Spike pair count")
ax.set_title("Cross-Correlogram: Neuron A → Neuron B")
ax.legend()
plt.tight_layout()
plt.savefig("figure_12-5-2_cross_correlogram.png", dpi=150, bbox_inches="tight")
print("Cross-correlogram example completed...")

# -----------------------------------------
# Normalizing the CCG: The Baseline Problem


def normalize_ccg(lags_ms, counts, baseline_lag_range=(30, 50)):
    """
    Normalize CCG by subtracting the mean baseline count.

    Params
    ------
    lags_ms            : 1D array of bin centers in milliseconds
    counts             : 1D array of raw spike pair counts
    baseline_lag_range : tuple (min_abs_lag, max_abs_lag) in ms
                         defining the flanking region used as baseline

    Returns
    -------
    normalized : 1D array — baseline-subtracted CCG
    baseline   : float — mean baseline count per bin
    """
    lo, hi = baseline_lag_range
    baseline_mask = (np.abs(lags_ms) >= lo) & (np.abs(lags_ms) <= hi)
    baseline = counts[baseline_mask].mean()
    normalized = counts.astype(float) - baseline
    return normalized, baseline


norm_ccg, baseline = normalize_ccg(lags_AB, ccg_AB, baseline_lag_range=(30, 50))

fig, axes = plt.subplots(1, 2, figsize=(13, 4), sharey=False)

axes[0].bar(lags_AB, ccg_AB, width=0.5, color="mediumpurple", edgecolor="none")
axes[0].axhline(
    baseline, color="red", linestyle="--", linewidth=1.2, label=f"Baseline = {baseline:.1f}"
)
axes[0].set_title("Raw CCG")
axes[0].set_xlabel("Lag (ms)")
axes[0].set_ylabel("Spike pair count")
axes[0].legend()

axes[1].bar(
    lags_AB,
    norm_ccg,
    width=0.5,
    color=["coral" if v > 0 else "steelblue" for v in norm_ccg],
    edgecolor="none",
)
axes[1].axhline(0, color="black", linewidth=0.8)
axes[1].axvline(5, color="red", linewidth=1.2, linestyle=":", label="~5 ms peak")
axes[1].set_title("Baseline-Subtracted CCG")
axes[1].set_xlabel("Lag (ms)")
axes[1].set_ylabel("Excess spike pairs")
axes[1].legend()

plt.suptitle("Cross-Correlogram: Neuron A → Neuron B", fontsize=12)
plt.tight_layout()
plt.savefig("figure_12-5-3_ccg_normalized.png", dpi=150, bbox_inches="tight")

print(f"Baseline (mean flanking count): {baseline:.2f} pairs/bin")
print(f"Peak excess at ~5 ms:          {norm_ccg[np.argmax(norm_ccg)]:.2f} pairs/bin")
print()
