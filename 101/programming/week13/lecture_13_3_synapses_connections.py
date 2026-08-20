"""
Lecture 13.3: Synapses in Brian2 — Connecting Neurons

In order to get rid of Brian2 warnings, you can use g++ compiler when launching the script:
> CC=gcc CXX=g++ python lecture_13_XXX.py
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

import matplotlib.pyplot as plt
import numpy as np
from brian2 import *

start_scope()

# ── Parameters ────────────────────────────────────────────────
N_E = 80  # 80 excitatory neurons
N_I = 20  # 20 inhibitory neurons

tau_m = 20 * ms  # membrane time constant
v_rest = -65 * mV
v_thresh = -50 * mV
v_reset = -65 * mV

tau_e = 5 * ms  # excitatory synaptic decay time constant
tau_i = 10 * ms  # inhibitory synaptic decay time constant

# originals not enough for demo purposes: w_e = 0.3*mV; w_i = -0.7*mV
w_e = 0.9 * mV  # excitatory synaptic weight (voltage units, absorbed into equation)
w_i = -0.1 * mV  # inhibitory synaptic weight (hyperpolarizing)
p_conn = 0.1  # connection probability (10%)

# ── Neuron equations ──────────────────────────────────────────
# We add two synaptic input terms: g_e and g_i
eqs = """
dv/dt  = (v_rest - v + g_e + g_i) / tau_m : volt
dg_e/dt = -g_e / tau_e : volt
dg_i/dt = -g_i / tau_i : volt
"""

excitatory = NeuronGroup(N_E, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler")
inhibitory = NeuronGroup(N_I, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler")

excitatory.v = "v_rest + rand() * 5 * mV"
inhibitory.v = "v_rest + rand() * 5 * mV"

# ── External drive (Poisson input) ────────────────────────────
# PoissonInput delivers random spike-like bumps at a given rate
# originals rate=10*Hz, weight=0.05*mV not enough for demo purposes
drive_E = PoissonInput(excitatory, "g_e", N=100, rate=30 * Hz, weight=0.8 * mV)
drive_I = PoissonInput(inhibitory, "g_e", N=100, rate=30 * Hz, weight=0.8 * mV)

# ── Synapses ──────────────────────────────────────────────────
# E → E connections
S_EE = Synapses(excitatory, excitatory, on_pre="g_e_post += w_e")
S_EE.connect(condition="i != j", p=p_conn)

# E → I connections
S_EI = Synapses(excitatory, inhibitory, on_pre="g_e_post += w_e")
S_EI.connect(p=p_conn)

# I → E connections
S_IE = Synapses(inhibitory, excitatory, on_pre="g_i_post += w_i")
S_IE.connect(p=p_conn)

# I → I connections
S_II = Synapses(
    inhibitory,
    inhibitory,
    on_pre="g_i_post += w_i",
)
S_II.connect(condition="i != j", p=p_conn)

# ── Monitors ──────────────────────────────────────────────────
spike_E = SpikeMonitor(excitatory)
spike_I = SpikeMonitor(inhibitory)

# ── Run ───────────────────────────────────────────────────────
run(500 * ms)

print(f"Excitatory spikes: {spike_E.num_spikes}")
print(f"Inhibitory spikes: {spike_I.num_spikes}")
print()


# ---------------------------------
# Connecting Neurons with connect()

start_scope()

N = 10
eqs = "dv/dt = -v / (10*ms) : volt"
source = NeuronGroup(N, eqs, threshold="v > 0.9*volt", reset="v = 0*volt", method="euler")
target = NeuronGroup(N, eqs, threshold="v > 0.9*volt", reset="v = 0*volt", method="euler")

# Pattern 1: All-to-all connectivity
S_all = Synapses(source, target, on_pre="v_post += 0.1*volt")
S_all.connect()  # Every source neuron connects to every target neuron

# Pattern 2: Random connectivity with probability p
S_random = Synapses(source, target, on_pre="v_post += 0.1*volt")
S_random.connect(p=0.1)  # Each pair connected with 10% probability

# Pattern 3: One-to-one (neuron i → neuron i)
S_one_to_one = Synapses(source, target, on_pre="v_post += 0.1*volt")
S_one_to_one.connect(j="i")  # Neuron 0→0, 1→1, 2→2, ...

# Pattern 4: Conditional — no self-connections
S_no_self = Synapses(source, source, on_pre="v_post += 0.1*volt")
S_no_self.connect(condition="i != j")  # Skip i==j pairs

# Pattern 5: Specific pairs
S_specific = Synapses(source, target, on_pre="v_post += 0.1*volt")
S_specific.connect(i=[0, 1, 2], j=[5, 6, 7])  # Neuron 0→5, 1→6, 2→7

# Check how many connections were formed
print(f"All-to-all: {len(S_all)} connections")
print(f"Random p=0.1: {len(S_random)} connections (expected ~{N*N*0.1:.0f})")
print(f"One-to-one: {len(S_one_to_one)} connections")
print()


# ------------------------------
# Heterogeneous Synaptic Weights

start_scope()

N = 20
eqs = """
dv/dt = (-v + g_e) / (20*ms) : volt
dg_e/dt = -g_e / (5*ms) : volt
"""
neurons = NeuronGroup(N, eqs, threshold="v > -0.05*volt", reset="v = -0.065*volt", method="euler")
neurons.v = -0.065 * volt

# Synapses with a per-synapse weight variable 'w'
S = Synapses(
    neurons, neurons, "w : volt", on_pre="g_e_post += w"  # Per-synapse weight variable
)  # Use per-synapse w in on_pre
S.connect(condition="i != j", p=0.3)

# Assign weights: positive (excitatory) with log-normal distribution
# Log-normal is a good fit for real cortical synapse weight distributions
mu, sigma = np.log(0.1e-3), 0.5  # parameters in log space
raw_weights = np.random.lognormal(mu, sigma, size=len(S))
S.w = raw_weights * volt  # Assign as Brian2 units

print(f"Number of synapses: {len(S)}")
print(f"Mean weight: {np.mean(S.w / mV):.3f} mV")
print(f"Std weight:  {np.std(S.w / mV):.3f} mV")
print()


# ------------------------------
# Visualizing the Synapse Effect

start_scope()

tau_m = 20 * ms
tau_e = 5 * ms
v_rest = -65 * mV
v_thresh = -50 * mV
v_reset = -65 * mV

eqs = """
dv/dt  = (v_rest - v + g_e) / tau_m : volt
dg_e/dt = -g_e / tau_e : volt
"""

# Pre: driven hard enough to fire regularly
pre = NeuronGroup(1, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler")
# Post: receives only synaptic drive (no external input)
post = NeuronGroup(1, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler")

pre.v = v_rest
post.v = v_rest
# original weight=0.2*mV not enough
# original rate=10*Hz not enough
pre_drive = PoissonInput(pre, "g_e", N=200, rate=50 * Hz, weight=2.0 * mV)

S = Synapses(pre, post, on_pre="g_e_post += 10.0*mV")  # original +=0.8 not enough
S.connect()

spike_pre = SpikeMonitor(pre)
spike_post = SpikeMonitor(post)
state_pre = StateMonitor(pre, ["v", "g_e"], record=True)
state_post = StateMonitor(post, ["v", "g_e"], record=True)

run(300 * ms)

print("Pre spikes:", spike_pre.num_spikes)
print("Post spikes:", spike_post.num_spikes)

fig, axes = plt.subplots(4, 1, figsize=(12, 8), sharex=True)

axes[0].vlines(spike_pre.t / ms, 0, 1, color="steelblue", lw=1.5, label="Pre spikes")
axes[0].set_ylabel("Pre spike")
axes[0].set_title("Presynaptic spikes → postsynaptic conductance → postsynaptic voltage")

axes[1].plot(state_pre.t / ms, state_pre.g_e[0] / mV, color="green")
axes[1].set_ylabel("g_e (mV)")
axes[1].set_title("Presynaptic conductance")

axes[2].plot(state_post.t / ms, state_post.g_e[0] / mV, color="green")
axes[2].set_ylabel("g_e (mV)")
axes[2].set_title("Postsynaptic conductance")

axes[3].plot(state_post.t / ms, state_post.v[0] / mV, color="darkorange")
axes[3].axhline(v_thresh / mV, color="red", linestyle="--", lw=1, label="Threshold")
axes[3].set_xlabel("Time (ms)")
axes[3].set_ylabel("Post voltage (mV)")
axes[3].set_title("Postsynaptic membrane voltage")
axes[3].legend()

plt.tight_layout()
plt.savefig("figure_13-3_synapse_demo.png", dpi=150, bbox_inches="tight")
print("Synapse demo example completed...")
