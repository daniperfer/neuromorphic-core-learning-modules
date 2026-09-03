# ============================================================
# NEUR 101 — Assignment 14: Mini-Project
# ============================================================
# Student name: [Your name]
# Project option: [A / B / C / D / E / F]
# Scientific question: [Your one-sentence question]
# ============================================================

# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

import warnings
from collections import Counter
from dataclasses import dataclass, field

import brian2
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from brian2 import *
from scipy import signal

warnings.filterwarnings("ignore")

# ── Confirm toolkit availability ─────────────────────────────
print("NEUR 101 Assignment 14 — Mini-Project")
print("=" * 45)
print(f"Brian2 version: {brian2.__version__}")
print(f"NumPy version:  {np.__version__}")

# ── NeuralAnalysisFramework (from Week 12) ───────────────────
# Paste your NeuralAnalysisFramework class here, or import it
# from your Week 12 module. All analysis methods should be
# available: isi_statistics(), bin_firing_rate(),
# kernel_firing_rate(), cross_correlogram().


# ── Helper functions (from Week 13) ─────────────────────────
def compute_population_rate(spike_trains: dict, duration_ms: float, bin_ms: float = 10.0) -> tuple:
    """
    Compute population firing rate histogram.

    Parameters
    ----------
    spike_trains : dict[int, np.ndarray]
        Spike times in ms, keyed by neuron index.
    duration_ms : float
        Simulation duration in ms.
    bin_ms : float
        Bin width in ms (default 10 ms).

    Returns
    -------
    times_ms : np.ndarray
        Bin center times (ms).
    rate_Hz : np.ndarray
        Population firing rate (Hz).
    """
    N = len(spike_trains)
    bins = np.arange(0, duration_ms + bin_ms, bin_ms)
    all_spikes = np.concatenate([spike_trains[i] for i in range(N) if len(spike_trains[i]) > 0])
    counts, _ = np.histogram(all_spikes, bins=bins)
    rate_Hz = counts / (N * bin_ms / 1000.0)
    times_ms = bins[:-1] + bin_ms / 2
    return times_ms, rate_Hz


def compute_power_spectrum(
    rate_Hz: np.ndarray, bin_ms: float = 10.0, freq_max_Hz: float = 120.0
) -> tuple:
    """
    Compute power spectral density of a firing rate time series.
    Uses Welch's method for reduced variance.

    Parameters
    ----------
    rate_Hz : np.ndarray
        Population firing rate time series (Hz).
    bin_ms : float
        Bin width used to compute rate_Hz (ms).
    freq_max_Hz : float
        Maximum frequency to return (Hz).

    Returns
    -------
    freqs : np.ndarray   — frequency axis (Hz)
    psd   : np.ndarray   — power spectral density (Hz²/Hz)
    peak_freq : float    — frequency of peak power above 1 Hz (Hz)
    """
    fs = 1000.0 / bin_ms
    freqs, psd = signal.welch(rate_Hz, fs=fs, nperseg=min(256, len(rate_Hz) // 4))
    mask = freqs <= freq_max_Hz
    freqs, psd = freqs[mask], psd[mask]
    above_dc = freqs > 1.0
    peak_freq = freqs[above_dc][np.argmax(psd[above_dc])]
    return freqs, psd, peak_freq


# ── Step 1: Project Proposal ─────────────────────────────────
# Write your answers to the four proposal questions as comments
# or as a markdown cell here before writing any simulation code.

# Q1 — Scientific question:
# [Your answer here]

# Q2 — Network description:
# [Your answer here]

# Q3 — Manipulation:
# [Your answer here]

# Q4 — Expected results:
# [Your answer here]


# ── Step 2: Parameter Dataclass ──────────────────────────────
@dataclass
class SimParams:
    """
    All parameters for one simulation condition.
    Replace default values with your project's parameters.
    Add or remove fields as needed for your project type.
    """

    # Network architecture
    N_E: int = 320
    N_I: int = 80
    p: float = 0.1

    # LIF parameters (fix unless your project varies them)
    tau_ms: float = 20.0
    v_rest_mV: float = -65.0
    v_thresh_mV: float = -50.0
    v_reset_mV: float = -65.0
    R_Mohm: float = 10.0

    # Synaptic weights — add the parameter you are manipulating
    w_EE_mV: float = 0.20
    w_EI_mV: float = 0.30
    w_IE_mV: float = -0.55  # ← manipulated in Option A
    w_II_mV: float = -0.25

    # Input drive
    input_rate_Hz: float = 8000.0
    input_weight_mV: float = 0.15

    # Simulation
    duration_ms: float = 2000.0
    seed_val: int = 42
    label: str = "unnamed"


# ── Step 3: Define All Conditions ────────────────────────────
# Define all conditions as a list of SimParams instances BEFORE
# writing any simulation code. Example for Option A:

conditions = [
    SimParams(w_IE_mV=-0.55, label="balanced"),
    SimParams(w_IE_mV=-0.35, label="mild_disinhibition"),
    SimParams(w_IE_mV=-0.10, label="strong_disinhibition"),
]

# Replace these with the conditions for your chosen project option.


# ── Step 4: Simulation Function ──────────────────────────────
def run_simulation(params: SimParams) -> dict:
    """
    Run one condition of your mini-project simulation.

    [Replace this docstring with a description of YOUR network,
    including: neuron type, number, connectivity, input drive,
    and what parameter is being manipulated.]

    Parameters
    ----------
    params : SimParams
        All network and simulation parameters.

    Returns
    -------
    dict with keys: 'spike_trains_E', 'spike_trains_I', 'params',
                    'n_spikes_E', 'n_spikes_I'
    """
    start_scope()  # ← ALWAYS first
    seed(params.seed_val)  # ← ALWAYS second

    # Unpack parameters
    tau = params.tau_ms * ms
    v_rest = params.v_rest_mV * mV
    v_thresh = params.v_thresh_mV * mV
    v_reset = params.v_reset_mV * mV
    R = params.R_Mohm * Mohm
    duration = params.duration_ms * ms

    w_EE = params.w_EE_mV * mV
    w_EI = params.w_EI_mV * mV
    w_IE = params.w_IE_mV * mV
    w_II = params.w_II_mV * mV

    input_rate = params.input_rate_Hz * Hz
    input_weight = params.input_weight_mV * mV

    N_E, N_I, N, p = params.N_E, params.N_I, params.N_E + params.N_I, params.p

    # ── Build your network here ──────────────────────────────
    eqs = """
    dv/dt = (v_rest - v + R*I_ext) / tau : volt
    I_ext : amp
    """

    neurons = NeuronGroup(N, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler")
    neurons.v = "v_rest + (v_thresh - v_rest) * rand()"
    neurons.I_ext = 0 * amp

    E_pop = neurons[:N_E]
    I_pop = neurons[N_E:]

    syn_EE = Synapses(E_pop, E_pop, on_pre="v_post += w_EE")
    syn_EE.connect(condition="i != j", p=p)

    syn_EI = Synapses(E_pop, I_pop, on_pre="v_post += w_EI")
    syn_EI.connect(p=p)

    syn_IE = Synapses(I_pop, E_pop, on_pre="v_post += w_IE")
    syn_IE.connect(p=p)

    syn_II = Synapses(I_pop, I_pop, on_pre="v_post += w_II")
    syn_II.connect(condition="i != j", p=p)

    poisson_E = PoissonInput(E_pop, "v", 1, input_rate, weight=input_weight)
    poisson_I = PoissonInput(I_pop, "v", 1, input_rate, weight=input_weight)

    spike_mon_E = SpikeMonitor(E_pop)
    spike_mon_I = SpikeMonitor(I_pop)

    run(duration, report="text")

    spike_trains_E = {i: np.array(spike_mon_E.spike_trains()[i] / ms) for i in range(N_E)}
    spike_trains_I = {i: np.array(spike_mon_I.spike_trains()[i] / ms) for i in range(N_I)}

    return {
        "spike_trains_E": spike_trains_E,
        "spike_trains_I": spike_trains_I,
        "params": params,
        "n_spikes_E": spike_mon_E.num_spikes,
        "n_spikes_I": spike_mon_I.num_spikes,
    }


# ── Step 5: Run All Conditions ───────────────────────────────
all_results = {}

for params in conditions:
    print(f"\nRunning condition: {params.label}")
    results = run_simulation(params)
    all_results[params.label] = results

    # Save immediately
    np.save(f"project_{params.label}_spikes_E.npy", results["spike_trains_E"])
    np.save(f"project_{params.label}_spikes_I.npy", results["spike_trains_I"])

    # Sanity check
    mean_rate_E = results["n_spikes_E"] / (params.N_E * params.duration_ms / 1000)
    print(f"  Mean E rate: {mean_rate_E:.1f} Hz  " f"(expected 5–30 Hz for physiological activity)")

print("\nAll conditions complete.")


# ── Step 6: Diagnostic Raster ────────────────────────────────
# Plot a quick raster for each condition BEFORE analysis.
# Verify firing looks qualitatively sensible before proceeding.

fig_diag, axes = plt.subplots(len(conditions), 1, figsize=(12, 3 * len(conditions)), sharex=True)
if len(conditions) == 1:
    axes = [axes]

for ax, params in zip(axes, conditions):
    spike_trains_E = all_results[params.label]["spike_trains_E"]
    for i in range(min(80, params.N_E)):
        spikes = spike_trains_E[i]
        spikes_w = spikes[spikes <= 800]
        if len(spikes_w) > 0:
            ax.scatter(spikes_w, np.full_like(spikes_w, i), s=1, c="#2c4a8c", alpha=0.7)
    ax.set_xlim(0, 800)
    ax.set_ylim(-1, 80)
    ax.set_ylabel("Neuron", fontsize=9)
    ax.set_title(f"Diagnostic raster — {params.label}", fontsize=9)

axes[-1].set_xlabel("Time (ms)", fontsize=10)
plt.tight_layout()
plt.savefig("project_diagnostic_rasters.png", dpi=150, bbox_inches="tight")
plt.show()
print("Diagnostic raster saved.")


# ── Step 7: Analysis Pipeline ────────────────────────────────
# Compute core statistics for all conditions.

stats = {}
for params in conditions:
    label = params.label
    st_E = all_results[label]["spike_trains_E"]
    N_E = params.N_E
    dur = params.duration_ms

    # Per-neuron firing rates
    rates = np.array([len(st_E[i]) / (dur / 1000.0) for i in range(N_E)])

    # ISI CV (neurons with >= 3 spikes only)
    cvs = []
    for i in range(N_E):
        spk = st_E[i]
        if len(spk) >= 3:
            isis = np.diff(np.sort(spk))
            if np.mean(isis) > 0:
                cvs.append(np.std(isis) / np.mean(isis))
    cvs = np.array(cvs)

    # Population rate and power spectrum
    times_ms, pop_rate = compute_population_rate(st_E, dur)
    freqs, psd, peak_f = compute_power_spectrum(pop_rate)

    stats[label] = {
        "rates_Hz": rates,
        "mean_rate_Hz": np.mean(rates),
        "isi_cv_values": cvs,
        "mean_cv": np.mean(cvs) if len(cvs) > 0 else np.nan,
        "pop_rate_Hz": pop_rate,
        "pop_rate_times_ms": times_ms,
        "freqs": freqs,
        "psd": psd,
        "peak_freq_Hz": peak_f,
    }

# ── Summary statistics table ─────────────────────────────────
print("\n" + "=" * 65)
print(f"{'Condition':<26} {'Rate (Hz)':>10} {'ISI CV':>8} {'Peak (Hz)':>10}")
print("-" * 65)
for params in conditions:
    s = stats[params.label]
    print(
        f"{params.label:<26} {s['mean_rate_Hz']:>10.1f} "
        f"{s['mean_cv']:>8.3f} {s['peak_freq_Hz']:>10.1f}"
    )
print("=" * 65)


# ── Step 8: Main Figure ──────────────────────────────────────
# Build your three- to four-panel results figure here.
# Use consistent colors across all panels for all conditions.
# Add axis labels, a title, and save as project_main_figure.png.

# Example color scheme — replace with colors meaningful for your project:
condition_colors = {
    "balanced": "#2c4a8c",
    "mild_disinhibition": "#e07b39",
    "strong_disinhibition": "#c0392b",
}

fig, axes = plt.subplots(2, 2, figsize=(13, 9))
fig.patch.set_facecolor("white")

# ── Panel A: Population firing rate over time ─────────────
ax = axes[0, 0]
for params in conditions:
    label = params.label
    color = condition_colors.get(label, "gray")
    ax.plot(
        stats[label]["pop_rate_times_ms"],
        stats[label]["pop_rate_Hz"],
        color=color,
        linewidth=1.2,
        alpha=0.85,
        label=label.replace("_", " "),
    )
ax.set_xlabel("Time (ms)", fontsize=10)
ax.set_ylabel("Population rate (Hz)", fontsize=10)
ax.set_title("A. Population firing rate", fontsize=11, fontweight="bold", loc="left")
ax.legend(fontsize=8, frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# ── Panel B: ISI CV distributions ────────────────────────
ax = axes[0, 1]
for params in conditions:
    label = params.label
    color = condition_colors.get(label, "gray")
    cvs = stats[label]["isi_cv_values"]
    if len(cvs) > 0:
        ax.hist(
            cvs,
            bins=30,
            range=(0, 2.5),
            color=color,
            alpha=0.5,
            label=f"{label.replace('_',' ')} (μ={stats[label]['mean_cv']:.2f})",
        )
ax.axvline(1.0, color="gray", linestyle="--", linewidth=1, label="CV=1 (Poisson)")
ax.set_xlabel("ISI coefficient of variation", fontsize=10)
ax.set_ylabel("Neuron count", fontsize=10)
ax.set_title("B. ISI CV distribution", fontsize=11, fontweight="bold", loc="left")
ax.legend(fontsize=7, frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# ── Panel C: Power spectrum ───────────────────────────────
ax = axes[1, 0]
for params in conditions:
    label = params.label
    color = condition_colors.get(label, "gray")
    ax.semilogy(
        stats[label]["freqs"],
        stats[label]["psd"],
        color=color,
        linewidth=1.4,
        label=f"{label.replace('_',' ')} " f"(peak {stats[label]['peak_freq_Hz']:.0f} Hz)",
    )
ax.set_xlabel("Frequency (Hz)", fontsize=10)
ax.set_ylabel("Power (Hz²/Hz)", fontsize=10)
ax.set_title("C. Population rate power spectrum", fontsize=11, fontweight="bold", loc="left")
ax.set_xlim(0, 120)
ax.legend(fontsize=7, frameon=False)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# ── Panel D: Summary bar chart ────────────────────────────
ax = axes[1, 1]
labels_list = [p.label for p in conditions]
mean_rates = [stats[l]["mean_rate_Hz"] for l in labels_list]
colors_list = [condition_colors.get(l, "gray") for l in labels_list]
x = np.arange(len(labels_list))
bars = ax.bar(x, mean_rates, color=colors_list, alpha=0.8, edgecolor="white")
ax.set_xticks(x)
ax.set_xticklabels([l.replace("_", "\n") for l in labels_list], fontsize=8)
ax.set_ylabel("Mean firing rate (Hz)", fontsize=10)
ax.set_title("D. Mean E firing rate by condition", fontsize=11, fontweight="bold", loc="left")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.suptitle("[Your project title here]", fontsize=13, fontweight="bold", y=1.01)
plt.tight_layout()
plt.savefig("project_main_figure.png", dpi=150, bbox_inches="tight")
plt.show()
print("Main figure saved: project_main_figure.png")


# ── Step 9: Methods Section ──────────────────────────────────
# Write your methods section as a multiline string or in a
# separate markdown cell. It must include:
#   1. Model description (neuron type, N, LIF parameters)
#   2. Connectivity (pattern, probability, synaptic weights)
#   3. Input drive (type, rate, weight)
#   4. Experimental conditions (what you varied and the values)
#   5. Analysis methods (what you computed and how)
#   6. Software (Brian2 version, random seed)

methods = """
METHODS
=======

[Replace this placeholder with your written methods section.
Three to five paragraphs. Every parameter value must be
stated explicitly. A reader with Python and Brian2 should
be able to replicate your simulation from this section alone.]

Model. We simulated ...

Connectivity. ...

Input drive. ...

Experimental conditions. ...

Analysis. ...
"""

print(methods)


# ── Step 10: Project Summary ─────────────────────────────────
summary = """
PROJECT SUMMARY
===============

[Replace this with your three- to five-sentence plain-English
summary: scientific question, main result, neuroscience
interpretation. No code. No jargon beyond what a
neuroscience undergraduate would know.]
"""

print(summary)
