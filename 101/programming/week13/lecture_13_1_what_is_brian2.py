"""
Lecture 13.1: What Is Brian2? Spiking Neural Network Simulation in Python
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

import brian2
import matplotlib.pyplot as plt
from brian2 import *  # noqa: F403,F405

print(f"brian2 version: {brian2.__version__}")

start_scope()  # Reset Brian2's internal state — always do this first
print(f"Default timestep: {defaultclock.dt}")

# Brian2 units are written as multiplication by the unit symbol
tau = 20 * ms  # 20 milliseconds — a time constant
v_rest = -65 * mV  # -65 millivolts — resting potential
v_thresh = -50 * mV  # -50 millivolts — spike threshold
v_reset = -65 * mV  # -65 millivolts — post-spike reset voltage
I_input = 0.7 * nA  # 0.7 nanoamps — injected current
g_syn = 1.0 * nS  # 1.0 nanosiemens — synaptic conductance
R = 10 * Mohm  # membrane resistance

# Brian2 will refuse to add incompatible units:
try:
    bad = tau + v_rest  # This raises a DimensionMismatchError — good!
except DimensionMismatchError:
    print("DimensionMismatchError")

# You can inspect units
print(tau)  # 20. ms
print(v_rest)  # -65. mV

# A single neuron with the LIF membrane equation
eqs = """
dv/dt = (v_rest - v + I_injected) / tau : volt
I_injected : volt
"""

neuron = NeuronGroup(1, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler")
neuron.v = v_rest
neuron.I_injected = 15.25 * mV  # Constant depolarizing drive

# Monitors: one for spikes, one for voltage trace
spike_mon = SpikeMonitor(neuron)
state_mon = StateMonitor(neuron, "v", record=True)

# Run for 200 ms
run(200 * ms)

# Plot the voltage trace
fig, axes = plt.subplots(2, 1, figsize=(10, 6))
axes[0].plot(state_mon.t / ms, state_mon.v[0] / mV, color="steelblue")
axes[0].axhline(v_thresh / mV, color="red", linestyle="--", label="Threshold")
axes[0].set_ylabel("Membrane voltage (mV)")
axes[0].set_title("Single LIF Neuron — Voltage Trace")
axes[0].legend()

axes[1].vlines(spike_mon.t / ms, 0, 1, color="black", linewidth=1.5)
axes[1].set_xlabel("Time (ms)")
axes[1].set_ylabel("Spike")
axes[1].set_title(f"Spike raster — {spike_mon.num_spikes} spikes fired")

plt.tight_layout()
plt.savefig("figure_13-1_first_simulation.png", dpi=150, bbox_inches="tight")
print()

print("Simulation complete.")
print(f"Total spikes fired: {spike_mon.num_spikes}")
print(f"Spike times (ms): {spike_mon.t / ms}")
