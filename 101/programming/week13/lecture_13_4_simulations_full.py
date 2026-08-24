"""
Lecture 13.4: Running Simulations and Recording Spike Trains

In order to get rid of Brian2 warnings, you can use g++ compiler when launching the script:
> CC=gcc CXX=g++ python lecture_13_XXX.py
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

import matplotlib.pyplot as plt
import numpy as np
from brian2 import *

# ── 1. Always start here ───────────────────────────────────────
start_scope()
seed(42)

# ── 2. Parameters with units ───────────────────────────────────
N = 100
tau = 20 * ms
v_rest = -65 * mV
v_thresh = -50 * mV
v_reset = -65 * mV
duration = 2000 * ms  # 2 seconds

# ── 3. Equations ───────────────────────────────────────────────
eqs = """
dv/dt = (v_rest - v + I) / tau : volt
I : volt
"""

# ── 4. NeuronGroup ─────────────────────────────────────────────
neurons = NeuronGroup(N, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler")
neurons.v = v_rest
neurons.I = "(8 + 8 * rand()) * mV"

# ── 5. Monitors (SpikeMonitor always; StateMonitor selectively) ─
spike_mon = SpikeMonitor(neurons)
state_mon = StateMonitor(neurons, "v", record=[0, 1, 2])  # Sample 3 neurons

# ── 6. Run ─────────────────────────────────────────────────────
run(duration)
print(f"Simulation complete: {spike_mon.num_spikes} total spikes")

# ── 7. Extract spike trains ────────────────────────────────────
spike_trains = {}
for idx in range(N):
    mask = spike_mon.i == idx
    spike_trains[idx] = np.array(spike_mon.t[mask] / second)

# ── 8. Save ────────────────────────────────────────────────────
filename = "week13_4_full_brian2_spike_trains.npy"
np.save(filename, spike_trains)

# ── 9. Quick visualization ─────────────────────────────────────
fig, axes = plt.subplots(2, 1, figsize=(12, 6), sharex=True)

axes[0].scatter(spike_mon.t / ms, spike_mon.i, s=1.5, color="black", alpha=0.5)
axes[0].set_ylabel("Neuron index")
axes[0].set_title("Population spike raster")

firing_rates = np.array([len(spike_trains[i]) / (duration / second) for i in range(N)])
time_bins = np.arange(0, duration / ms, 50)  # 50 ms bins
pop_rate = np.zeros(len(time_bins) - 1)
for i in range(N):
    hist, _ = np.histogram(spike_trains[i] * 1000, bins=time_bins)
    pop_rate += hist
pop_rate = pop_rate / N / (50e-3)  # Normalize to Hz

axes[1].plot(time_bins[:-1], pop_rate, color="steelblue")
axes[1].set_xlabel("Time (ms)")
axes[1].set_ylabel("Mean firing rate (Hz)")
axes[1].set_title("Population firing rate (50 ms bins)")

plt.tight_layout()
plt.savefig("figure_13-4-2_complete_pipeline.png", dpi=150, bbox_inches="tight")
print()

print(f"\nMean firing rate: {firing_rates.mean():.1f} Hz")
print(f"Spike trains saved to brian2_spike_trains.npy")
