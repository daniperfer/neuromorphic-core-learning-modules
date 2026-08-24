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

# ---------------------
# SpikeMonitor in Depth

start_scope()
seed(42)

# Check default
print(f"Default dt: {defaultclock.dt}")  # 0.1 ms

# Halve the timestep for more accurate integration
defaultclock.dt = 1 * ms
print(f"Current dt: {defaultclock.dt}")

N = 10
tau = 20 * ms
v_rest = -65 * mV
v_thresh = -50 * mV
v_reset = -65 * mV

eqs = """
dv/dt = (v_rest - v + I) / tau : volt
I : volt
"""

neurons = NeuronGroup(N, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler")
neurons.v = v_rest
neurons.I = "(10.5 + 5 * rand()) * mV"  # Heterogeneous drive

spike_mon = SpikeMonitor(neurons)

# record=[0,1,2,3,4] — record all 5 neurons
# For large populations, use record=[0, 10, 20] to sample specific neurons
state_mon = StateMonitor(neurons, "v", record=True)

duration_ms = 1000 * ms
run(duration_ms)

# ── Basic SpikeMonitor attributes ─────────────────────────────
print(f"Total spikes recorded:      {spike_mon.num_spikes}")
print(f"spike_mon.t shape:          {spike_mon.t.shape}")
print(f"spike_mon.i shape:          {spike_mon.i.shape}")
print(f"First 10 spike times (ms):  {np.round(spike_mon.t[:10] / ms, 2)}")
print(f"First 10 neuron indices:    {spike_mon.i[:10]}")

# ── Per-neuron spike counts ────────────────────────────────────
# count attribute: array of length N, how many spikes each neuron fired
spike_counts = np.array(spike_mon.count)  # Already a plain integer array
print(f"\nSpike counts (first 10 neurons): {spike_counts[:10]}")
duration_s = duration_ms / second
print(f"Mean firing rate: {spike_counts.mean() / duration_s:.1f} Hz in {duration_s} seconds.")
print()

# ----------------------------------
# Extracting Per-Neuron Spike Trains

# ── Standard extraction pattern (use this every time) ─────────
spike_times_per_neuron = {}

for neuron_idx in range(N):
    # Boolean mask: which spikes belong to this neuron?
    mask = spike_mon.i == neuron_idx
    # Extract times, convert from Brian2 seconds to plain float array
    spike_times_per_neuron[neuron_idx] = np.array(spike_mon.t[mask] / second)

# Verify extraction
idx = np.nonzero(spike_counts)[0][0]
neuron_idx_spikes = spike_times_per_neuron[idx]
print(f"Neuron {idx}: {len(neuron_idx_spikes)} spikes")
print(f"Neuron {idx} spike times (s): {np.round(neuron_idx_spikes, 4)}")
print(f"Type: {type(neuron_idx_spikes)}, dtype: {neuron_idx_spikes.dtype}")
print()

# ---------------------------------
# Saving Spike Trains as .npy Files

# Save all spike trains as a dictionary
# Each key is a neuron index; each value is a 1D float array of spike times in seconds
filename = "week13_4_brian2_spike_trains.npy"
np.save(filename, spike_times_per_neuron)

# Load them back (allow_pickle=True for dict of arrays)
loaded = np.load(filename, allow_pickle=True).item()

print(f"Loaded {len(loaded)} spike trains")
print(f"Neuron {idx}: {len(loaded[idx])} spikes")

# Verify round-trip fidelity
original = spike_times_per_neuron[idx]
restored = loaded[idx]
print(f"Round-trip matches: {np.allclose(original, restored)}")
print()

# ---------------------
# StateMonitor in Depth

# ── Accessing StateMonitor data ────────────────────────────────
# state_mon.t : time array (same for all neurons)
# state_mon.v : 2D array, shape (N_recorded, N_timepoints)
# state_mon.v[k] : voltage trace of the k-th recorded neuron

print(f"state_mon.t shape: {state_mon.t.shape}")
print(f"state_mon.v shape: {state_mon.v.shape}")

# ── Plot voltage traces ────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 5))
colors = plt.cm.viridis(np.linspace(0, 1, N))
for k in range(N):
    ax.plot(
        state_mon.t / ms,
        state_mon.v[k] / mV,
        color=colors[k],
        alpha=0.8,
        label=f"Neuron {k} (I={np.linspace(8,16,N)[k]:.1f} mV)",
    )
ax.axhline(v_thresh / mV, color="red", linestyle="--", lw=1, label="Threshold")
ax.axhline(v_rest / mV, color="gray", linestyle=":", lw=1, label="Rest")
ax.set_xlabel("Time (ms)")
ax.set_ylabel("Membrane voltage (mV)")
ax.set_title("LIF voltage traces for 5 neurons with different input drives")
ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=8)
plt.tight_layout()
plt.savefig("figure_13-4-1_state_monitor.png", dpi=150, bbox_inches="tight")
print()

# ---------------------------
# Reproducibility with seed()

seed(42)  # Brian2's own seed function — use this for reproducibility

# -------------------------------
# Controlling Simulation Timestep
