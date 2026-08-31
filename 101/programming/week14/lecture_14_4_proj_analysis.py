"""
Lecture 14.4: Analysis and Visualization — Telling the Story of Your Results
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

from typing import TypedDict

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

# -------------------------------
# Loading Your Saved Spike Trains


# Load spike trains for all conditions
class Condition(TypedDict):
    """typed dict"""

    label: str
    w_IE_mV: float
    color: str


conditions_meta: list[Condition] = [
    {"label": "balanced", "w_IE_mV": -0.55, "color": "#2c4a8c"},
    {"label": "mild_disinhibition", "w_IE_mV": -0.35, "color": "#e07b39"},
    {"label": "strong_disinhibition", "w_IE_mV": -0.10, "color": "#c0392b"},
]

all_spike_trains = {}
for cond in conditions_meta:
    label = cond["label"]
    all_spike_trains[label] = {
        "E": np.load(f"project_{label}_spikes_E.npy", allow_pickle=True).item(),
        "I": np.load(f"project_{label}_spikes_I.npy", allow_pickle=True).item(),
    }
    n_E_spikes = sum(len(st) for st in all_spike_trains[label]["E"].values())
    print(f"{label}: {n_E_spikes} total E spikes loaded")

# ------------------------------------------------------
# Computing Core Statistics with NeuralAnalysisFramework

# Assume NeuralAnalysisFramework and helper functions are imported
# from your Week 12/13 toolkit


def compute_condition_stats(spike_trains_E: dict, duration_ms: float, N_E: int) -> dict:
    """
    Compute core statistics for one simulation condition.

    Parameters
    ----------
    spike_trains_E : dict[int, np.ndarray]
        Excitatory spike trains (spike times in ms).
    duration_ms : float
        Simulation duration in ms.
    N_E : int
        Number of excitatory neurons.

    Returns
    -------
    dict with keys: 'mean_rate_Hz', 'isi_cv_values', 'mean_cv',
                    'pop_rate_Hz', 'pop_rate_times_ms', 'active_fraction'
    """
    duration_s = duration_ms / 1000.0

    # Per-neuron firing rates
    rates = np.array([len(spike_trains_E[i]) / duration_s for i in range(N_E)])
    mean_rate = np.mean(rates)
    active_fraction = np.mean(rates > 0.5)  # fraction firing > 0.5 Hz

    # ISI CV for active neurons only (need at least 2 spikes)
    isi_cv_values = []
    for i in range(N_E):
        spikes = spike_trains_E[i]
        if len(spikes) >= 3:
            isis = np.diff(np.sort(spikes))
            if np.mean(isis) > 0:
                cv = np.std(isis) / np.mean(isis)
                isi_cv_values.append(cv)
    isi_cv_values = np.array(isi_cv_values)
    mean_cv = np.mean(isi_cv_values) if len(isi_cv_values) > 0 else np.nan

    # Population firing rate (bin width 10 ms)
    bin_ms = 10.0
    bins = np.arange(0, duration_ms + bin_ms, bin_ms)
    all_spikes = np.concatenate(
        [spike_trains_E[i] for i in range(N_E) if len(spike_trains_E[i]) > 0]
    )
    counts, _ = np.histogram(all_spikes, bins=bins)
    # Convert to Hz: spikes per bin / (N neurons * bin duration in s)
    pop_rate_Hz = counts / (N_E * bin_ms / 1000.0)
    pop_rate_times_ms = bins[:-1] + bin_ms / 2

    return {
        "mean_rate_Hz": mean_rate,
        "rates_Hz": rates,
        "isi_cv_values": isi_cv_values,
        "mean_cv": mean_cv,
        "pop_rate_Hz": pop_rate_Hz,
        "pop_rate_times_ms": pop_rate_times_ms,
        "active_fraction": active_fraction,
    }


# Run statistics for all conditions
stats = {}
N_E = 320
duration_ms = 2000.0

for cond in conditions_meta:
    label = cond["label"]
    stats[label] = compute_condition_stats(
        spike_trains_E=all_spike_trains[label]["E"], duration_ms=duration_ms, N_E=N_E
    )
    print(f"{label}:")
    print(f"  Mean rate:  {stats[label]['mean_rate_Hz']:.1f} Hz")
    print(f"  Mean ISI CV: {stats[label]['mean_cv']:.3f}")
    print(f"  Active fraction: {stats[label]['active_fraction']:.2f}")

# ----------------------------
# Computing the Power Spectrum


def compute_power_spectrum(
    pop_rate_Hz: np.ndarray, bin_ms: float = 10.0, freq_max_Hz: float = 120.0
) -> tuple:
    """
    Compute power spectrum of population firing rate using Welch's method.

    Parameters
    ----------
    pop_rate_Hz : np.ndarray
        Population firing rate time series (Hz).
    bin_ms : float
        Bin width used to compute pop_rate_Hz (ms).
    freq_max_Hz : float
        Maximum frequency to return (Hz).

    Returns
    -------
    freqs : np.ndarray   — frequency axis (Hz)
    psd   : np.ndarray   — power spectral density
    peak_freq : float    — frequency of peak power (Hz)
    """
    fs = 1000.0 / bin_ms  # Sampling rate in Hz
    freqs, psd = signal.welch(
        pop_rate_Hz, fs=fs, nperseg=min(256, len(pop_rate_Hz) // 4), noverlap=None
    )

    # Restrict to frequencies below freq_max_Hz
    mask = freqs <= freq_max_Hz
    freqs = freqs[mask]
    psd = psd[mask]

    # Find peak (exclude DC component at 0 Hz)
    peak_idx = np.argmax(psd[freqs > 1.0])
    peak_freq = freqs[freqs > 1.0][peak_idx]

    return freqs, psd, peak_freq


# Compute power spectra for all conditions
spectra = {}
for cond in conditions_meta:
    label = cond["label"]
    freqs, psd, peak_freq = compute_power_spectrum(
        pop_rate_Hz=stats[label]["pop_rate_Hz"], bin_ms=10.0
    )
    spectra[label] = {"freqs": freqs, "psd": psd, "peak_freq": peak_freq}
    print(f"{label}: peak frequency = {peak_freq:.1f} Hz")

# -------------------------------
# Building the Multi-Panel Figure

fig = plt.figure(figsize=(14, 10))
fig.patch.set_facecolor("white")

# Color scheme matching conditions
colors = {cond["label"]: cond["color"] for cond in conditions_meta}
labels_display = {
    "balanced": "Balanced\n(w_IE = −0.55 mV)",
    "mild_disinhibition": "Mild disinhibition\n(w_IE = −0.35 mV)",
    "strong_disinhibition": "Strong disinhibition\n(w_IE = −0.10 mV)",
}

# ── Panel A: Raster plots (one per condition, stacked) ──────────────────────
for idx, cond in enumerate(conditions_meta):
    ax = fig.add_subplot(4, 3, idx + 1)
    label = cond["label"]
    spike_trains_E = all_spike_trains[label]["E"]

    # Show first 800 ms for clarity; plot 80 neurons
    for i in range(80):
        spikes = spike_trains_E[i]
        spikes_window = spikes[spikes <= 800]
        if len(spikes_window) > 0:
            ax.scatter(
                spikes_window, np.full_like(spikes_window, i), s=1.0, c=colors[label], alpha=0.7
            )

    ax.set_xlim(0, 800)
    ax.set_ylim(-1, 80)
    ax.set_xlabel("Time (ms)", fontsize=9)
    ax.set_ylabel("Neuron", fontsize=9)
    ax.set_title(labels_display[label], fontsize=9, fontweight="bold", color=colors[label])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

# ── Panel B: Population firing rate over time ────────────────────────────────
ax_rate = fig.add_subplot(4, 1, 2)
for cond in conditions_meta:
    label = cond["label"]
    times = stats[label]["pop_rate_times_ms"]
    rate = stats[label]["pop_rate_Hz"]
    ax_rate.plot(
        times,
        rate,
        color=colors[label],
        linewidth=1.2,
        label=labels_display[label].replace("\n", " "),
        alpha=0.85,
    )

ax_rate.set_xlabel("Time (ms)", fontsize=10)
ax_rate.set_ylabel("Population rate (Hz)", fontsize=10)
ax_rate.set_title("B. Population firing rate over time", fontsize=11, fontweight="bold", loc="left")
ax_rate.legend(fontsize=8, frameon=False)
ax_rate.spines["top"].set_visible(False)
ax_rate.spines["right"].set_visible(False)

# ── Panel C: ISI CV distributions ──────────────────────────────────────────
ax_cv = fig.add_subplot(4, 2, 5)
for cond in conditions_meta:
    label = cond["label"]
    cv_vals = stats[label]["isi_cv_values"]
    if len(cv_vals) > 0:
        ax_cv.hist(
            cv_vals,
            bins=30,
            range=(0, 2.5),
            color=colors[label],
            alpha=0.55,
            label=f"{label.replace('_',' ')} (mean={stats[label]['mean_cv']:.2f})",
        )

ax_cv.axvline(1.0, color="gray", linestyle="--", linewidth=1, label="CV = 1 (Poisson)")
ax_cv.set_xlabel("ISI coefficient of variation", fontsize=10)
ax_cv.set_ylabel("Number of neurons", fontsize=10)
ax_cv.set_title("C. ISI CV distributions", fontsize=11, fontweight="bold", loc="left")
ax_cv.legend(fontsize=7, frameon=False)
ax_cv.spines["top"].set_visible(False)
ax_cv.spines["right"].set_visible(False)

# ── Panel D: Power spectra ──────────────────────────────────────────────────
ax_psd = fig.add_subplot(4, 2, 6)
for cond in conditions_meta:
    label = cond["label"]
    freqs = spectra[label]["freqs"]
    psd = spectra[label]["psd"]
    peak = spectra[label]["peak_freq"]
    ax_psd.semilogy(
        freqs,
        psd,
        color=colors[label],
        linewidth=1.4,
        label=f"{label.replace('_',' ')} (peak {peak:.0f} Hz)",
    )

ax_psd.set_xlabel("Frequency (Hz)", fontsize=10)
ax_psd.set_ylabel("Power (Hz²/Hz)", fontsize=10)
ax_psd.set_title("D. Population rate power spectrum", fontsize=11, fontweight="bold", loc="left")
ax_psd.set_xlim(0, 120)
ax_psd.legend(fontsize=7, frameon=False)
ax_psd.spines["top"].set_visible(False)
ax_psd.spines["right"].set_visible(False)

plt.suptitle(
    "E/I Balance Perturbation: Network Dynamics Across Disinhibition Conditions",
    fontsize=13,
    fontweight="bold",
    y=1.01,
)
plt.tight_layout()
plt.savefig("figure_14-4-1_project_main_figure.png", dpi=150, bbox_inches="tight")
print()
print("Main figure saved: project_main_figure.png")

# ----------------------------
# The Summary Statistics Table

print("\n" + "=" * 65)
print(f"{'Condition':<25} {'Mean rate (Hz)':>14} {'Mean ISI CV':>12} {'Peak freq (Hz)':>14}")
print("-" * 65)
for cond in conditions_meta:
    label = cond["label"]
    r = stats[label]["mean_rate_Hz"]
    cv = stats[label]["mean_cv"]
    pf = spectra[label]["peak_freq"]
    print(f"{label:<25} {r:>14.1f} {cv:>12.3f} {pf:>14.1f}")
print("=" * 65)

# ------------------------------------------------------
# Adapting the Analysis Pipeline for Other Project Types

# For the F-I curve project, replace the multi-condition comparison with a line plot of firing rate vs. input current, with one line per parameter condition:

# F-I curve: collect mean firing rates across current steps
current_steps_pA = np.linspace(0, 500, 25)
mean_rates_by_condition = {}

for condition_name, tau_ms in [("tau_20ms", 20), ("tau_10ms", 10), ("tau_30ms", 30)]:
    rates = []
    for I_pA in current_steps_pA:
        spikes = np.load(
            f"project_fI_{condition_name}_I{I_pA:.0f}_spikes.npy", allow_pickle=True
        ).item()
        n_spikes = len(spikes.get(0, []))
        rate = n_spikes / (duration_ms / 1000.0)
        rates.append(rate)
    mean_rates_by_condition[condition_name] = np.array(rates)

# Plot F-I curves
fig, ax = plt.subplots(figsize=(7, 5))
for name, rates in mean_rates_by_condition.items():
    ax.plot(current_steps_pA, rates, linewidth=2, label=name)
ax.set_xlabel("Input current (pA)", fontsize=11)
ax.set_ylabel("Mean firing rate (Hz)", fontsize=11)
ax.set_title("F-I Curve Comparison", fontsize=12, fontweight="bold")
ax.legend(frameon=False)
plt.tight_layout()
plt.savefig("figure_14-4-2_project_fI_curves.png", dpi=150, bbox_inches="tight")

# For the population synchrony project, compute a cross-correlogram between neurons from the two populations:

# from your_week12_toolkit import cross_correlogram

# Compare cross-correlogram in shared-input vs. independent-input conditions
for condition in ["independent_input", "fully_shared_input"]:
    spikes = np.load(f"project_{condition}_spikes.npy", allow_pickle=True).item()

    # Cross-correlogram between neuron 0 and neuron 1
    lags, ccg = cross_correlogram(spikes[0], spikes[1], max_lag_ms=50, bin_ms=1)
    plt.plot(lags, ccg, label=condition)

plt.xlabel("Lag (ms)")
plt.ylabel("Coincidence rate (Hz)")
plt.title("Cross-correlogram: shared vs. independent input")
plt.legend(frameon=False)
plt.tight_layout()
plt.savefig("figure_14-4-3_project_synchrony_ccg.png", dpi=150, bbox_inches="tight")
