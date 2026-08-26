"""
Lecture 13.6: Building a Small Network — Excitatory and Inhibitory Populations

In order to get rid of Brian2 warnings, you can use g++ compiler when launching the script:
> CC=gcc CXX=g++ python lecture_13_XXX.py

"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

import matplotlib.pyplot as plt
import numpy as np
from brian2 import *

start_scope()
seed(42)

# ── Network parameters ────────────────────────────────────────
N_E = 800  # Excitatory neurons (80%)
N_I = 200  # Inhibitory neurons (20%)

# Membrane parameters (same for both populations for simplicity)
tau_m = 20 * ms
v_rest = -65 * mV
v_thresh = -50 * mV
v_reset = -65 * mV

# Synaptic time constants
tau_e = 5 * ms  # AMPA-like: fast
tau_i = 10 * ms  # GABA-like: slower

# Synaptic weights — inhibitory is stronger to enforce E/I balance
w_EE = 0.15 * mV  # E → E original 0.15
w_EI = 0.20 * mV  # E → I (strong excitatory drive to inhibitory cells) orignal 0.2
w_IE = -0.45 * mV  # I → E (inhibitory suppression) original -0.45
w_II = -0.30 * mV  # I → I (inhibitory-to-inhibitory, prevents over-suppression) original -0.3

# Connection probability
p_conn = 0.1  # 10% — sparse, biologically realistic

# Background input rate (simulating thalamic / feedforward input)
bg_rate = 50 * Hz  # original = 8
bg_weight_E = 0.185 * mV  # orignal 0.08
bg_weight_I = 0.185 * mV  # orignal 0.08
N_bg = 300  # Number of background Poisson sources original 200

duration = 3000 * ms  # 3 seconds

# ── Neuron equations ──────────────────────────────────────────
eqs = """
dv/dt  = (v_rest - v + g_e + g_i) / tau_m : volt
dg_e/dt = -g_e / tau_e : volt
dg_i/dt = -g_i / tau_i : volt
"""

# ── NeuronGroups ──────────────────────────────────────────────
excitatory = NeuronGroup(
    N_E, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler", name="excitatory"
)

inhibitory = NeuronGroup(
    N_I, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler", name="inhibitory"
)

# Random initial voltages near rest (prevents burst at t=0)
excitatory.v = "v_rest + rand() * 5 * mV"
inhibitory.v = "v_rest + rand() * 5 * mV"

# ── Background Poisson input ──────────────────────────────────
bg_E = PoissonInput(excitatory, "g_e", N=N_bg, rate=bg_rate, weight=bg_weight_E)
bg_I = PoissonInput(inhibitory, "g_e", N=N_bg, rate=bg_rate, weight=bg_weight_I)

# ── Synapses ──────────────────────────────────────────────────
S_EE = Synapses(excitatory, excitatory, on_pre="g_e_post += w_EE", name="S_EE")
S_EI = Synapses(excitatory, inhibitory, on_pre="g_e_post += w_EI", name="S_EI")
S_IE = Synapses(inhibitory, excitatory, on_pre="g_i_post += w_IE", name="S_IE")
S_II = Synapses(inhibitory, inhibitory, on_pre="g_i_post += w_II", name="S_II")

S_EE.connect(condition="i != j", p=p_conn)
S_EI.connect(p=p_conn)
S_IE.connect(p=p_conn)
S_II.connect(condition="i != j", p=p_conn)

print(f"Connections formed:")
print(f"  E → E: {len(S_EE)}")
print(f"  E → I: {len(S_EI)}")
print(f"  I → E: {len(S_IE)}")
print(f"  I → I: {len(S_II)}")

# ── Monitors ──────────────────────────────────────────────────
spike_E = SpikeMonitor(excitatory, name="spike_E")
spike_I = SpikeMonitor(inhibitory, name="spike_I")
# Record voltage from 5 neurons of each type
state_E = StateMonitor(excitatory, "v", record=[0, 100, 200, 300, 400])
state_I = StateMonitor(inhibitory, "v", record=[0, 25, 50, 75, 99])

# ── Run ───────────────────────────────────────────────────────
print("Running simulation...")
run(duration)
print("Simulation Done!")

# ── Summary statistics ────────────────────────────────────────
rate_E = spike_E.num_spikes / N_E / (duration / second)
rate_I = spike_I.num_spikes / N_I / (duration / second)

print(f"\nExcitatory population: {rate_E:.1f} Hz mean")
print(f"Inhibitory population: {rate_I:.1f} Hz mean")
print(f"I/E rate ratio: {rate_I / max(rate_E, 0.01):.2f}")
print()

# ---------------------------
# Visualizing the E/I Network

fig, axes = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

# ── Raster plot: E and I populations ──────────────────────────
# Offset inhibitory indices so they appear above excitatory
exc_times = spike_E.t / ms
exc_idx = spike_E.i

inh_times = spike_I.t / ms
inh_idx = spike_I.i + N_E  # Shift inhibitory neuron indices upward

axes[0].scatter(
    exc_times,
    exc_idx,
    s=0.8,
    color="steelblue",
    alpha=0.5,
    label=f"Excitatory (mean {rate_E:.1f} Hz)",
)
axes[0].scatter(
    inh_times,
    inh_idx,
    s=0.8,
    color="crimson",
    alpha=0.5,
    label=f"Inhibitory (mean {rate_I:.1f} Hz)",
)
axes[0].axhline(N_E, color="black", linestyle="--", lw=0.8)
axes[0].set_ylabel("Neuron index")
axes[0].set_title("E/I Network Spike Raster (blue=excitatory, red=inhibitory)")
axes[0].legend(loc="upper right", markerscale=5)

# ── Population firing rates (50 ms bins) ──────────────────────
bin_size_ms = 50
bins = np.arange(0, duration / ms, bin_size_ms)
rate_E_hist, _ = np.histogram(exc_times, bins=bins)
rate_I_hist, _ = np.histogram(inh_times, bins=bins)

rate_E_hz = rate_E_hist / N_E / (bin_size_ms * 1e-3)
rate_I_hz = rate_I_hist / N_I / (bin_size_ms * 1e-3)
bin_centers = bins[:-1] + bin_size_ms / 2

axes[1].plot(bin_centers, rate_E_hz, color="steelblue", lw=1.5, label="Excitatory")
axes[1].plot(bin_centers, rate_I_hz, color="crimson", lw=1.5, label="Inhibitory")
axes[1].set_ylabel("Population firing rate (Hz)")
axes[1].set_title("Population firing rates (50 ms bins)")
axes[1].legend()

# ── Voltage traces for sample neurons ─────────────────────────
time_ms = state_E.t / ms
for k in range(3):
    axes[2].plot(time_ms, state_E.v[k] / mV, color="steelblue", alpha=0.6, lw=0.8)
for k in range(3):
    axes[2].plot(time_ms, state_I.v[k] / mV, color="crimson", alpha=0.6, lw=0.8)
axes[2].axhline(v_thresh / mV, color="gray", linestyle="--", lw=0.8)
axes[2].set_xlabel("Time (ms)")
axes[2].set_ylabel("Voltage (mV)")
axes[2].set_title("Sample voltage traces (blue=E, red=I)")

plt.tight_layout()
plt.savefig("figure_13-6-1_ei_network.png", dpi=150, bbox_inches="tight")
print("E/I network example completed...\n")

# ---------------------
# Analyzing E/I Balance

# ── Per-neuron firing rates ────────────────────────────────────
e_rates = np.array([np.sum(spike_E.i == k) for k in range(N_E)]) / (duration / second)
i_rates = np.array([np.sum(spike_I.i == k) for k in range(N_I)]) / (duration / second)

print("Excitatory population:")
print(f"  Mean rate: {e_rates.mean():.1f} Hz")
print(f"  Std rate:  {e_rates.std():.1f} Hz")
print(f"  Fraction silent: {np.mean(e_rates == 0):.1%}")

print("\nInhibitory population:")
print(f"  Mean rate: {i_rates.mean():.1f} Hz")
print(f"  Std rate:  {i_rates.std():.1f} Hz")
print(f"  Fraction silent: {np.mean(i_rates == 0):.1%}")

# ── ISI statistics for a representative excitatory neuron ─────
spike_trains_E = {}
for idx in range(N_E):
    mask = spike_E.i == idx
    spike_trains_E[idx] = np.array(spike_E.t[mask] / second)

# Find the median-rate neuron for a "typical" example
median_idx = np.argsort(e_rates)[N_E // 2]
median_spikes = spike_trains_E[median_idx]

if len(median_spikes) > 2:
    isis = np.diff(median_spikes) * 1000
    cv = np.std(isis) / np.mean(isis)
    print(f"\nMedian-rate excitatory neuron (#{median_idx}):")
    print(f"  Rate: {e_rates[median_idx]:.1f} Hz")
    print(f"  CV:   {cv:.3f}  (1.0 = Poisson; closer to 1.0 = realistic)")

# ── Save excitatory population for further analysis ───────────
filename = "week13_6_brian2_ei_spike_trains_E.npy"
np.save(f"{filename}", spike_trains_E)
print(f"\nSaved excitatory spike trains to {filename}\n")

# ----------------------
# Perturbing E/I Balance


def run_ei_network(w_inhibitory, label, duration=2000 * ms):
    """Run the E/I network with a specified inhibitory weight and return spike data."""
    start_scope()
    seed(42)

    N_E, N_I = 400, 100  # Smaller for faster sweeps
    tau_m = 20 * ms
    v_rest = -65 * mV
    v_thresh = -50 * mV
    v_reset = -65 * mV
    tau_e = 5 * ms
    tau_i = 10 * ms

    eqs = """
    dv/dt  = (v_rest - v + g_e + g_i) / tau_m : volt
    dg_e/dt = -g_e / tau_e : volt
    dg_i/dt = -g_i / tau_i : volt
    """
    exc = NeuronGroup(N_E, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler")
    inh = NeuronGroup(N_I, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler")
    exc.v = "v_rest + rand() * 5 * mV"
    inh.v = "v_rest + rand() * 5 * mV"

    # Background input rate (simulating thalamic / feedforward input)
    bg_rate = 60 * Hz  # original = 8
    bg_weight_E = 0.185 * mV  # orignal 0.08
    bg_weight_I = 0.185 * mV  # orignal 0.06
    N_bg = 300  # Number of background Poisson sources original 200

    PoissonInput(exc, "g_e", N=N_bg, rate=bg_rate, weight=bg_weight_E)
    PoissonInput(inh, "g_e", N=N_bg, rate=bg_rate, weight=bg_weight_I)

    # Synaptic weights — inhibitory is stronger to enforce E/I balance
    w_EE = 0.15 * mV  # E → E original 0.15
    w_EI = 0.20 * mV  # E → I (strong excitatory drive to inhibitory cells) orignal 0.2
    w_IE = -0.45 * mV  # I → E (inhibitory suppression) original -0.45
    w_II = -0.30 * mV  # I → I (inhibitory-to-inhibitory, prevents over-suppression) original -0.3

    p_conn = 0.1
    S_EE = Synapses(exc, exc, on_pre="g_e_post += w_EE")
    S_EE.connect(condition="i != j", p=p_conn)
    S_EI = Synapses(exc, inh, on_pre="g_e_post += w_EI")
    S_EI.connect(p=p_conn)
    S_IE = Synapses(inh, exc, "w_inh : volt", on_pre=f"g_i_post += w_inh")
    S_IE.connect(p=p_conn)
    S_IE.w_inh = w_inhibitory
    S_II = Synapses(inh, inh, on_pre="g_i_post += w_II")
    S_II.connect(condition="i != j", p=p_conn)

    sm_E = SpikeMonitor(exc)
    print(f"Running simulation {label}...")
    run(duration)

    rate_E = sm_E.num_spikes / N_E / (duration / second)
    return rate_E, sm_E.t / ms, sm_E.i


# Sweep inhibitory weight
inh_weights = [-0.20, -0.35, -0.45, -0.55]
results = []
for w in inh_weights:
    r, t, idx = run_ei_network(w * mV, f"w_I={w}")
    results.append((w, r, t, idx))
    print(f"w_I = {w:.2f} mV → E rate = {r:.1f} Hz\n")
