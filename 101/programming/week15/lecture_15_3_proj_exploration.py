"""
Lecture 15.3: Parameter Sweeps and Systematic Exploration
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

import matplotlib.pyplot as plt
import numpy as np
from brian2 import *
from week12.lecture_12_2_isi import isi_statistics
from week13.lecture_13_7_oscillation_dynamics_alt import (
    compute_population_rate,
    compute_power_spectrum,
)
from week14.lecture_14_3_proj_implement import SimParams, run_ei_simulation

# ---------------------------------------------
# np.linspace() and Generating Parameter Ranges


# Generate 8 evenly spaced values of inhibitory weight from 0.2 to 1.0
w_IE_values = np.linspace(0.2, 1.0, 8)
print(w_IE_values)
# [0.2        0.314... 0.428... 0.542... 0.657... 0.771... 0.885... 1.0      ]

# For a finer sweep around a region of interest (e.g., near a transition at 0.5)
w_IE_fine = np.linspace(0.35, 0.65, 10)

# For an input rate sweep
input_rates = np.linspace(2.0, 15.0, 8)  # Hz

# ----------------------
# The Sweep Loop Pattern

# --- Step 1: Define the sweep range ---
w_IE_values = np.linspace(0.2, 1.0, 8)

# --- Step 2: Run one simulation per sweep value ---
sweep_results = {}

for w_IE in w_IE_values:
    label = f"sweep_wIE_{w_IE:.3f}".replace(".", "p")
    params = SimParams(w_IE=w_IE, label=label)
    sweep_results[label] = run_ei_simulation(params)
    print(f"  Completed sweep step: w_IE = {w_IE:.3f}")

print(f"\nSweep complete: {len(sweep_results)} simulations run.")

# ------------------------------
# Extracting a Summary Statistic

# After running the sweep, extract a summary statistic from each result
mean_cv_values = []
mean_rate_values = []
peak_freq_values = []

for w_IE in w_IE_values:
    label = f"sweep_wIE_{w_IE:.3f}".replace(".", "p")
    result = sweep_results[label]

    spike_times = result["spike_times_E"]
    spike_ids = result["spike_ids_E"]
    N = result["N_E"]
    duration = result["duration"]

    # Summary statistic 1: mean CV
    isis, cv = isi_statistics(spike_times, spike_ids, N)
    mean_cv = np.nanmean(cv)
    mean_cv_values.append(mean_cv)

    # Summary statistic 2: mean firing rate
    mean_rate = len(spike_times) / (N * duration)
    mean_rate_values.append(mean_rate)

    # Summary statistic 3: peak frequency of population rate spectrum
    t_pop, rate_pop = compute_population_rate(spike_times, spike_ids, N, duration, bin_size=0.01)
    freqs, power = compute_power_spectrum(rate_pop, fs=100.0)
    peak_freq = freqs[np.argmax(power)]
    peak_freq_values.append(peak_freq)

# Convert to arrays for plotting
mean_cv_values = np.array(mean_cv_values)
mean_rate_values = np.array(mean_rate_values)
peak_freq_values = np.array(peak_freq_values)

# -------------------------
# Plotting the Sweep Figure

# Use a consistent color scheme throughout your final project
SWEEP_COLOR = "#2c4a8c"  # dark blue for sweep line
MARKER_COLOR = "#e74c3c"  # red for individual sweep points

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle(
    "Parameter Sweep: Effect of Inhibitory Weight on Network Dynamics",
    fontsize=14,
    fontweight="bold",
)

# Panel A: mean CV vs w_IE
ax = axes[0]
ax.plot(
    w_IE_values,
    mean_cv_values,
    "-o",
    color=SWEEP_COLOR,
    markerfacecolor=MARKER_COLOR,
    linewidth=2,
    markersize=7,
)
ax.set_xlabel("Inhibitory Synaptic Weight w_IE (nA)", fontsize=12)
ax.set_ylabel("Mean Coefficient of Variation (CV)", fontsize=12)
ax.set_title("A: Firing Regularity vs. Inhibitory Weight", fontsize=11)
ax.axhline(y=1.0, color="gray", linestyle="--", linewidth=1.0, label="CV = 1 (Poisson)")
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3)

# Panel B: mean firing rate vs w_IE
ax = axes[1]
ax.plot(
    w_IE_values,
    mean_rate_values,
    "-o",
    color=SWEEP_COLOR,
    markerfacecolor=MARKER_COLOR,
    linewidth=2,
    markersize=7,
)
ax.set_xlabel("Inhibitory Synaptic Weight w_IE (nA)", fontsize=12)
ax.set_ylabel("Mean Firing Rate (Hz)", fontsize=12)
ax.set_title("B: Firing Rate vs. Inhibitory Weight", fontsize=11)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("figure_15-3-1_final_sweep_figure.png", dpi=300, bbox_inches="tight")
print()
print("Sweep figure saved.")

# -----------------------------------------------
# The Difference Between a Sweep and a Comparison

# Example of how named conditions and sweep values can be aligned
# The named conditions are specific points along the sweep
named_conditions = {
    "low_inhibition": SimParams(w_IE=0.3, label="low_inhibition"),
    "medium_inhibition": SimParams(w_IE=0.5, label="medium_inhibition"),
    "high_inhibition": SimParams(w_IE=0.9, label="high_inhibition"),
}

# The sweep covers the same range with finer resolution
w_IE_sweep = np.linspace(0.2, 1.0, 8)

# In your sweep figure, you can mark the named conditions
# with vertical lines or special markers to show where Figure 1 came from
ax.axvline(x=0.3, color="lightgray", linestyle=":", linewidth=1.5, label="Low condition")
ax.axvline(x=0.5, color="lightgray", linestyle=":", linewidth=1.5, label="Medium condition")
ax.axvline(x=0.9, color="lightgray", linestyle=":", linewidth=1.5, label="High condition")
