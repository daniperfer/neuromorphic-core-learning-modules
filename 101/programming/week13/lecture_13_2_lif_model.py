"""
Lecture 13.2: Neurons in Brian2 — The Leaky Integrate-and-Fire Model

In order to get rid of Brian2 warnings, you can use g++ compiler when launching the script:
> CC=gcc CXX=g++ python lecture_13_2_lif_model.py
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

import matplotlib.pyplot as plt
import numpy as np
from brian2 import *

start_scope()

print(prefs.codegen.target)

# ── Parameters ────────────────────────────────────────────────
tau = 20 * ms  # membrane time constant (~20 ms for cortical neurons)
v_rest = -65 * mV  # resting membrane potential
v_thresh = -50 * mV  # action potential threshold
v_reset = -65 * mV  # post-spike reset voltage
R = 10 * Mohm  # membrane resistance

# Input current (constant for now — we'll explore time-varying later)
I_input = 1.51 * nA  # suprathreshold drive

# ── Neuron equations ──────────────────────────────────────────
# Brian2 equations are written as a multi-line string.
# Each line: d<var>/dt = <expression> : <units>
# Or for static parameters:  <var> : <units>
eqs = """
dv/dt = (v_rest - v + R * I) / tau : volt
I : amp
"""

# ── NeuronGroup ───────────────────────────────────────────────
# NeuronGroup(N, equations, threshold, reset, method)
# N = number of neurons
# threshold = condition string evaluated at each timestep
# reset = assignment string applied when threshold is met
neuron = NeuronGroup(
    1,  # Single neuron
    eqs,
    threshold="v > v_thresh",  # Spike when voltage exceeds threshold
    reset="v = v_reset",  # Reset voltage after spike
    method="euler",  # Numerical integration method
)

# ── Initial conditions ────────────────────────────────────────
# Must set initial values before run(); unset state variables default to 0
neuron.v = v_rest  # Start at rest
neuron.I = I_input  # Set constant input current

# ── Monitors ──────────────────────────────────────────────────
# SpikeMonitor records spike times (t) and neuron indices (i)
spike_mon = SpikeMonitor(neuron)

# StateMonitor records continuous state variables over time
# record=True means record all neurons; record=[0,1,2] for specific indices
state_mon = StateMonitor(neuron, "v", record=True)

# ── Run ───────────────────────────────────────────────────────
run(500 * ms)

# ── Analyze output ────────────────────────────────────────────
n_spikes = spike_mon.num_spikes
mean_isi = np.mean(np.diff(spike_mon.t / ms)) if n_spikes > 1 else float("nan")
mean_rate = n_spikes / (500e-3)  # spikes per second

print(f"Spikes fired:    {n_spikes}")
print(f"Mean firing rate: {mean_rate:.1f} Hz")
print(f"Mean ISI:         {mean_isi:.2f} ms")
print(f"Spike times (ms): {np.round(spike_mon.t / ms, 1)}")

fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

# Voltage trace
axes[0].plot(state_mon.t / ms, state_mon.v[0] / mV, color="steelblue", lw=1.5)
axes[0].axhline(
    v_thresh / mV, color="crimson", linestyle="--", lw=1, label=f"Threshold ({v_thresh/mV:.0f} mV)"
)
axes[0].axhline(v_rest / mV, color="gray", linestyle=":", lw=1, label=f"Rest ({v_rest/mV:.0f} mV)")
axes[0].set_ylabel("Membrane voltage (mV)")
axes[0].set_title(f"LIF Neuron — {n_spikes} spikes in 500 ms ({mean_rate:.1f} Hz)")
axes[0].legend(loc="upper right")
axes[0].set_ylim([-70, -45])

# Spike raster
axes[1].vlines(spike_mon.t / ms, 0, 1, color="black", lw=2)
axes[1].set_xlabel("Time (ms)")
axes[1].set_ylabel("Spike")
axes[1].set_title("Spike train")
axes[1].set_yticks([])

plt.tight_layout()
plt.savefig("figure_13-2-1_lif_single.png", dpi=150, bbox_inches="tight")
print("LIF Single example completed...")

# --------------------------
# Populations of LIF Neurons

start_scope()

N = 100  # 100 neurons
tau = 20 * ms
v_rest = -65 * mV
v_thresh = -50 * mV
v_reset = -65 * mV
R = 10 * Mohm

eqs = """
dv/dt = (v_rest - v + R * I) / tau : volt
I : amp
"""

neurons = NeuronGroup(N, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler")

# Start all neurons at rest
neurons.v = v_rest

# Heterogeneous input: each neuron receives a different constant current
# drawn from a uniform distribution between 0.8 and 2.0 nA
neurons.I = "(0.8 + 1.2 * rand()) * nA"
# Brian2 evaluates this string for each neuron, where rand() ~ Uniform(0,1)

spike_mon = SpikeMonitor(neurons)
state_mon = StateMonitor(neurons, "v", record=[0, 25, 50, 75, 99])

run(500 * ms)

# Population-level statistics
firing_rates = np.zeros(N)
for neuron_idx in range(N):
    mask = spike_mon.i == neuron_idx
    firing_rates[neuron_idx] = np.sum(mask) / 0.5  # spikes / 500ms = Hz

print(f"Mean population firing rate: {firing_rates.mean():.1f} Hz")
print(f"Std of firing rates:          {firing_rates.std():.1f} Hz")
print(f"Min / Max firing rates:       {firing_rates.min():.1f} / {firing_rates.max():.1f} Hz")

# Raster plot of population
fig, ax = plt.subplots(figsize=(12, 5))
ax.scatter(spike_mon.t / ms, spike_mon.i, s=2, color="black", alpha=0.6)
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Neuron index")
ax.set_title(f"Population raster — {N} LIF neurons with heterogeneous inputs")
ax.set_xlim([0, 500])
ax.set_ylim([-1, N])
plt.tight_layout()
plt.savefig("figure_13-2-2_lif_population.png", dpi=150, bbox_inches="tight")
print("LIF Population example completed...")

# --------------------------------------------
# The F-I Curve: Firing Rate vs. Input Current

start_scope()

tau = 20 * ms
v_rest = -65 * mV
v_thresh = -50 * mV
v_reset = -65 * mV
R = 10 * Mohm

eqs = """
dv/dt = (v_rest - v + R * I) / tau : volt
I : amp
"""

# Test a range of input currents
I_values = np.linspace(0.0, 3.0, 31) * nA
firing_rates = []

for I_test in I_values:
    start_scope()  # Critical: reset between simulations
    n = NeuronGroup(1, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler")
    n.v = v_rest
    n.I = I_test
    sm = SpikeMonitor(n)
    run(1000 * ms)  # 1 second for stable rate estimate
    firing_rates.append(sm.num_spikes / 1.0)  # Hz

firing_rates = np.array(firing_rates)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(I_values / nA, firing_rates, "o-", color="steelblue", markersize=5)
ax.set_xlabel("Input current (nA)")
ax.set_ylabel("Firing rate (Hz)")
ax.set_title("LIF Neuron F-I Curve")
ax.axhline(0, color="gray", linestyle="--", lw=0.8)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("figure_13-2-3_fi_curve.png", dpi=150, bbox_inches="tight")
print("FI curve example completed...")
