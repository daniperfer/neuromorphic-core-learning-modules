"""
Lecture 13.5: Analyzing Brian2 Output with the SpikeTrainPipeline

In order to get rid of Brian2 warnings, you can use g++ compiler when launching the script:
> CC=gcc CXX=g++ python lecture_13_XXX.py

Launch from the project root folder as:
> CC=gcc CXX=g++ python -m week13.lecture_13_5_analyzing_brian2_output
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

import sys

import matplotlib.pyplot as plt
import numpy as np
from brian2 import *
from week11.lecture_11_7_NeuralAnalysisFramework import (
    NeuralAnalysisFramework,
    NeuralPipeline,
)
from week12.lecture_12_2_isi import isi_statistics
from week12.lecture_12_3_firing_rate import bin_firing_rate, kernel_firing_rate
from week12.lecture_12_5_cross_correlogram import cross_correlogram
from week12.lecture_12_SpikeTrainPipeline import SpikeTrainPipeline

# from week12.lecture_12_7_multineuron_analysis import population_vector_decode

# -----------------------------------------------
# Step 1: Run a Brian2 Simulation and Save Output

start_scope()
seed(42)

N = 50
tau = 20 * ms
v_rest = -65 * mV
v_thresh = -50 * mV
v_reset = -65 * mV
duration = 5000 * ms  # 5 seconds — enough for reliable statistics

eqs = """
dv/dt = (v_rest - v + I) / tau : volt
I : volt
"""

neurons = NeuronGroup(N, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler")
neurons.v = v_rest

# Heterogeneous Poisson-like drive: neurons receive different input levels
neurons.I = "(8 + 8 * rand()) * mV"

# Add sparse recurrent excitatory connections
S = Synapses(neurons, neurons, on_pre="v_post += 1.5*mV")
S.connect(condition="i != j", p=0.05)

spike_mon = SpikeMonitor(neurons)
run(duration)

# ── Extract spike trains ───────────────────────────────────────
spike_trains = {}
for idx in range(N):
    mask = spike_mon.i == idx
    spike_trains[idx] = np.array(spike_mon.t[mask] / second)

# ── Save ───────────────────────────────────────────────────────
filename = "week13/week13_5_brian2_spike_trains.npy"
np.save(f"{filename}", spike_trains)
print(f"Saved {N} spike trains from {spike_mon.num_spikes} total spikes.")
print(f"Mean firing rate: {spike_mon.num_spikes / N / (duration/second):.1f} Hz")
print()

# ----------------------------------------------------------------
# Step 2: Load into SpikeTrainPipeline via NeuralAnalysisFramework

# Load the saved spike trains
brian2_data = np.load(f"{filename}", allow_pickle=True).item()

# For pipeline compatibility, work with a single reference neuron
# (or wrap the population analysis below)
# We'll analyze neuron with len(spike_times) > 1 as a single unit example first
first_idx = 0
second_idx = 0
third_idx = 0

for idx in range(N):
    if len(brian2_data[idx]) > 1:
        spike_times_0 = brian2_data[idx]
        first_idx = idx
        break

for idx in range(first_idx + 1, N):
    if len(brian2_data[idx]) > 1:
        spike_times_1 = brian2_data[idx]
        second_idx = idx
        break

for idx in range(N - 1, second_idx, -1):
    if len(brian2_data[idx]) > 1:
        spike_times_2 = brian2_data[idx]
        third_idx = idx
        break

duration_s = duration / second
print(f"Duration (seconds): {duration_s}")

print(
    f"Neuron {first_idx}: {len(spike_times_0)} spikes over {duration_s} s → {len(spike_times_0)/duration_s:.1f} Hz"
)
print(
    f"Neuron {first_idx}: from {spike_times_0[0]} to {spike_times_0[-1]} s, span {spike_times_0[-1] - spike_times_0[0]}"
)
print(
    f"Neuron {second_idx}: {len(spike_times_1)} spikes over {duration_s} s → {len(spike_times_1)/duration_s:.1f} Hz"
)
print(
    f"Neuron {second_idx}: from {spike_times_1[0]} to {spike_times_1[-1]} s, span {spike_times_1[-1] - spike_times_1[0]}"
)

# ── ISI Analysis ───────────────────────────────────────────────
isi_stats_0 = isi_statistics(spike_times_0, (duration / second))
isi_stats_1 = isi_statistics(spike_times_1, (duration / second))

print(f"\nNeuron {first_idx} ISI Statistics:")
print(f"  Mean ISI:   {isi_stats_0['mean_isi_ms']:.2f} ms")
print(f"  Std  ISI:   {isi_stats_0['std_isi_ms']:.3f}")
print(f"  CV:         {isi_stats_0['cv']:.3f}")
print(f"  Median ISI: {isi_stats_0['median_isi_ms']:.2f} ms")

print(f"\nNeuron {second_idx} ISI Statistics:")
print(f"  Mean ISI:   {isi_stats_1['mean_isi_ms']:.2f} ms")
print(f"  Std  ISI:   {isi_stats_1['std_isi_ms']:.3f}")
print(f"  CV:         {isi_stats_1['cv']:.3f}")
print()

# ----------------------------
# Step 3: Firing Rate Analysis

# ── Binned firing rate for neuron 0 ───────────────────────────
times_0, rates_0 = bin_firing_rate(spike_times_0, bin_width=0.1, recording_duration=duration_s)

# ── Kernel-smoothed firing rate for neuron 0 ──────────────────
times_0k, rates_0k = kernel_firing_rate(spike_times_0, sigma_ms=0.2, recording_duration=duration_s)

fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

axes[0].bar(times_0, rates_0, width=0.1, color="steelblue", alpha=0.7, label="Binned (100 ms)")
axes[0].plot(times_0k, rates_0k, color="crimson", lw=2, label="Kernel-smoothed (σ=200 ms)")
axes[0].set_ylabel("Firing rate (Hz)")
axes[0].set_title(f"Neuron {first_idx} — Brian2 simulation output, firing rate analysis")
axes[0].legend()

# ── Population mean firing rate ───────────────────────────────
N = 50
pop_rate = np.zeros(len(times_0))
for idx in range(N):
    if len(brian2_data[idx]) > 0:
        _, rates_i = bin_firing_rate(brian2_data[idx], bin_width=0.1, recording_duration=duration_s)
        pop_rate += rates_i
pop_rate /= N

axes[1].plot(times_0, pop_rate, color="darkorange", lw=2)
axes[1].set_xlabel("Time (s)")
axes[1].set_ylabel("Population mean rate (Hz)")
axes[1].set_title("Population mean firing rate — all 50 neurons")

plt.tight_layout()
plt.savefig("week13/figure_13-5-1_firing_rates.png", dpi=150, bbox_inches="tight")
print("Firing rates example completed...")
print()

# ---------------------------------------------------------------------
# Step 4: ISI Distributions — Is the Model Firing in a Cortical Regime?

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

neuron_samples = [first_idx, second_idx, third_idx]
colors = ["steelblue", "darkorange", "green"]

for ax, idx, color in zip(axes, neuron_samples, colors):
    spikes = brian2_data[idx]
    if len(spikes) < 3:
        ax.set_title(f"Neuron {idx}: insufficient spikes")
        continue

    isis = np.diff(spikes) * 1000  # Convert to ms
    stats = isi_statistics(spikes, (duration / second))

    ax.hist(isis, bins=30, color=color, alpha=0.7, edgecolor="white", density=True)
    ax.axvline(
        stats["mean_isi_ms"],
        color="black",
        linestyle="--",
        lw=1.5,
        label=f"Mean = {stats['mean_isi_ms']:.1f} ms",
    )
    ax.set_xlabel("ISI (ms)")
    ax.set_ylabel("Density")
    ax.set_title(
        f"Neuron {idx}\n" f"Rate = {len(spikes)/duration_s:.1f} Hz | CV = {stats['cv']:.2f}"
    )
    ax.legend(fontsize=8)

plt.suptitle("ISI Distributions — Brian2 LIF Simulation", y=1.02, fontsize=12)
plt.tight_layout()
plt.savefig("week13/figure_13-5-2_isi_distributions.png", dpi=150, bbox_inches="tight")
print("ISI distribution example completed...")

# --------------------------------------------------
# Step 5: Cross-Correlogram — Detecting Shared Input

# Compare two pairs: one with known shared drive, one drawn randomly
spikes_a = brian2_data[first_idx]
spikes_b = brian2_data[second_idx]  # same input distribution range, independent
spikes_c = brian2_data[third_idx]  # another independent neuron

lags_ab, cc_ab = cross_correlogram(spikes_a, spikes_b, max_lag_ms=100, bin_width_ms=2)
lags_ac, cc_ac = cross_correlogram(spikes_a, spikes_c, max_lag_ms=100, bin_width_ms=2)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].bar(lags_ab, cc_ab, width=2, color="steelblue", alpha=0.7)
axes[0].set_xlabel("Lag (ms)")
axes[0].set_ylabel("Coincidence count")
axes[0].set_title("Cross-correlogram: Neurons 0 vs 1")
axes[0].axvline(0, color="red", linestyle="--", lw=1)

axes[1].bar(lags_ac, cc_ac, width=2, color="darkorange", alpha=0.7)
axes[1].set_xlabel("Lag (ms)")
axes[1].set_ylabel("Coincidence count")
axes[1].set_title("Cross-correlogram: Neurons 0 vs 25")
axes[1].axvline(0, color="red", linestyle="--", lw=1)

plt.suptitle("Cross-correlograms — Brian2 Simulation Output", fontsize=12)
plt.tight_layout()
plt.savefig("week13/figure_13-5-3_cross_correlograms.png", dpi=150, bbox_inches="tight")
print("Cross correlogram example completed...")
print()

# ------------------------------------------------------------
# Step 6: Using NeuralAnalysisFramework for Population Summary

# Classify neurons by firing rate quartile
firing_rates = np.array([len(brian2_data[i]) / 5.0 for i in range(50)])
high_threshold = np.percentile(firing_rates, 75)
low_threshold = np.percentile(firing_rates, 25)

# Representative high-rate and low-rate neurons
high_rate_idx = np.argmax(firing_rates)
low_rate_idx = np.argmin(firing_rates[firing_rates > 0]) if np.any(firing_rates > 0) else 0

print(f"Highest firing neuron: #{high_rate_idx} at {firing_rates[high_rate_idx]:.1f} Hz")
print(f"Lowest active neuron:  #{low_rate_idx} at {firing_rates[low_rate_idx]:.1f} Hz")

# Save individual spike trains for pipeline
file_high = "week13/week13_5_brian2_high_rate.npy"
file_low = "week13/week13_5_brian2_low_rate.npy"
np.save(f"{file_high}", brian2_data[high_rate_idx])
np.save(f"{file_low}", brian2_data[low_rate_idx])

# Now use NeuralAnalysisFramework (as defined in your Week 12 code)
framework = NeuralAnalysisFramework()

freq_sampl = 1000.0 / (defaultclock.dt / ms)
print(f"Sampling freq.: {freq_sampl} Hz")

pipeline_high = SpikeTrainPipeline(recording_duration=duration_s, sampling_rate=freq_sampl)
pipeline_high.load_data(f"{file_high}")

pipeline_low = SpikeTrainPipeline(recording_duration=duration_s, sampling_rate=freq_sampl)
pipeline_low.load_data(f"{file_low}")

framework.add_pipeline("high_rate_neuron", pipeline_high)
framework.add_pipeline("low_rate_neuron", pipeline_low)

framework.run_all()

framework.compare()
framework.print_summary()
print("Comparison example completed...")
