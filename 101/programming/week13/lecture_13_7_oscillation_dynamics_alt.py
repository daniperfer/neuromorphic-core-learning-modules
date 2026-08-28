"""
Lecture 13.7: Oscillations and Population Dynamics in Brian2

In order to get rid of Brian2 warnings, you can use g++ compiler when launching the script:
> CC=gcc CXX=g++ python lecture_13_XXX.py

"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

import builtins

import matplotlib.pyplot as plt
import numpy as np
from brian2 import *
from scipy import signal as sp_signal

# -----------------------------
# Population Dynamics: The PSTH


def compute_population_rate(spike_monitor, N_neurons, bin_size_ms=5.0, duration_ms=None):
    """
    Compute population-averaged firing rate as a function of time.

    Parameters
    ----------
    spike_monitor : SpikeMonitor
    N_neurons     : int, total number of neurons in the monitored group
    bin_size_ms   : float, bin width in milliseconds
    duration_ms   : float, total simulation duration in ms (inferred if None)

    Returns
    -------
    bin_centers : 1D array, time of bin centers in ms
    pop_rate    : 1D array, population firing rate in Hz
    """
    spike_times_ms = spike_monitor.t / ms
    if duration_ms is None:
        duration_ms = spike_times_ms.max() + bin_size_ms if len(spike_times_ms) > 0 else bin_size_ms

    bins = np.arange(0, duration_ms + bin_size_ms, bin_size_ms)
    counts, _ = np.histogram(spike_times_ms, bins=bins)
    pop_rate = counts / N_neurons / (bin_size_ms * 1e-3)  # Convert to Hz
    bin_centers = bins[:-1] + bin_size_ms / 2
    return bin_centers, pop_rate


# ----------------------------------------------
# Detecting Oscillations with the Power Spectrum


def compute_power_spectrum(pop_rate, bin_size_ms):
    """
    Compute the power spectrum of a population rate signal.

    Returns frequencies in Hz and power in arbitrary units.
    """
    fs = 1000.0 / bin_size_ms  # Sampling rate in Hz
    freqs, power = sp_signal.welch(pop_rate, fs=fs, nperseg=min(256, len(pop_rate) // 4))
    return freqs, power


# -----------------------------------
# Building a Gamma-Generating Network
def oscillation_dynamics(N_E=400, N_I=100, duration=2000 * ms, tau_i=10 * ms):
    """Pack code in a single function"""
    start_scope()
    seed(42)

    tau_m = 20 * ms
    tau_E_m = 15 * ms  # Excitatory neurons slightly faster
    v_rest = -65 * mV
    v_thresh = -50 * mV
    v_reset = -65 * mV

    tau_e = 5 * ms  # AMPA
    # tau_i = 10 * ms  # GABA-A

    # Stronger E→I drive to push interneurons into gamma regime
    w_EE = 0.10 * mV
    w_EI = 0.30 * mV  # Strong excitatory drive onto interneurons
    w_IE = -0.70 * mV  # Strong inhibition from interneurons back onto excitatory
    w_II = -0.40 * mV  # Mutual inhibition among interneurons — key for ING

    # ── Equations ─────────────────────────────────────────────────
    eqs_E = """
    dv/dt  = (v_rest - v + g_e + g_i) / tau_E_m : volt
    dg_e/dt = -g_e / tau_e : volt
    dg_i/dt = -g_i / tau_i : volt
    """
    eqs_I = """
    dv/dt  = (v_rest - v + g_e + g_i) / tau_m : volt
    dg_e/dt = -g_e / tau_e : volt
    dg_i/dt = -g_i / tau_i : volt
    """

    excitatory = NeuronGroup(
        N_E, eqs_E, threshold="v > v_thresh", reset="v = v_reset", method="euler", name="Excit"
    )
    inhibitory = NeuronGroup(
        N_I, eqs_I, threshold="v > v_thresh", reset="v = v_reset", method="euler", name="Inhib"
    )

    excitatory.v = "v_rest + rand() * 5*mV"
    inhibitory.v = "v_rest + rand() * 5*mV"

    # Background drive — strong enough to keep interneurons tonically active
    rate_E = 55 * Hz  # original 10 Hz
    rate_I = 60 * Hz  # original 12 Hz
    N_bg = 300  # original 200
    bg_weight_E = 0.18 * mV  # orignal 0.10
    bg_weight_I = 0.19 * mV  # orignal 0.12
    bg_E = PoissonInput(excitatory, "g_e", N=N_bg, rate=rate_E, weight=bg_weight_E)
    bg_I = PoissonInput(inhibitory, "g_e", N=N_bg, rate=rate_I, weight=bg_weight_I)

    # ── Connectivity ──────────────────────────────────────────────
    S_EE = Synapses(excitatory, excitatory, on_pre="g_e_post += w_EE")
    S_EE.connect(condition="i != j", p=0.1)
    S_EI = Synapses(excitatory, inhibitory, on_pre="g_e_post += w_EI")
    S_EI.connect(p=0.1)
    S_IE = Synapses(inhibitory, excitatory, on_pre="g_i_post += w_IE")
    S_IE.connect(p=0.1)
    S_II = Synapses(inhibitory, inhibitory, on_pre="g_i_post += w_II")
    S_II.connect(condition="i != j", p=0.3)
    # Higher I-I connectivity than E-E: more interneuron-interneuron connections for ING

    # ── Monitors ──────────────────────────────────────────────────
    spike_E = SpikeMonitor(excitatory)
    spike_I = SpikeMonitor(inhibitory)

    print(f"\nRunning gamma oscillation simulation tau_i={tau_i}...")
    run(duration)
    print(f"spike_E.num_spikes = {spike_E.num_spikes}")
    print(f"E: {spike_E.num_spikes / N_E / (duration/second):.1f} Hz mean")
    print(f"I: {spike_I.num_spikes / N_I / (duration/second):.1f} Hz mean")

    return spike_E, spike_I


# ---------------------------
# Visualizing the Oscillation

# ── Parameters ────────────────────────────────────────────────
N_E = 400  # Excitatory
N_I = 100  # Inhibitory (interneuron network)
duration = 2000 * ms

spike_E1, spike_I1 = oscillation_dynamics(N_E, N_I, duration, tau_i=10 * ms)

bin_size_ms = 4.0

# Compute population rates
t_E, rate_E = compute_population_rate(spike_E1, N_E, bin_size_ms, duration / ms)
t_I, rate_I = compute_population_rate(spike_I1, N_I, bin_size_ms, duration / ms)

# Compute power spectra
freqs_E, power_E = compute_power_spectrum(rate_E, bin_size_ms)
freqs_I, power_I = compute_power_spectrum(rate_I, bin_size_ms)
print(f"freqs_E.shape = {freqs_E.shape}")
print(f"power_E.shape = {power_E.shape}")

# Find peak frequencies
freq_range = (10, 120)  # Gamma band and beyond
mask = (freqs_E > freq_range[0]) & (freqs_E < freq_range[1])
peak_E = freqs_E[mask][np.argmax(power_E[mask])]
peak_I = freqs_I[mask][np.argmax(power_I[mask])]

print(f"Dominant peak oscillation frequency — Excitatory: {peak_E:.1f} Hz")
print(f"Dominant peak oscillation frequency — Inhibitory: {peak_I:.1f} Hz")

fig, axes = plt.subplots(4, 1, figsize=(14, 12))

# ── Raster (first 500 ms for clarity) ────────────────────────
t_max_plot = 500  # ms
mask_e = spike_E1.t / ms < t_max_plot
mask_i = spike_I1.t / ms < t_max_plot

axes[0].scatter((spike_E1.t / ms)[mask_e], spike_E1.i[mask_e], s=0.8, color="steelblue", alpha=0.5)
axes[0].scatter(
    (spike_I1.t / ms)[mask_i], spike_I1.i[mask_i] + N_E, s=0.8, color="crimson", alpha=0.5
)
axes[0].axhline(N_E, color="black", linestyle="--", lw=0.8)
axes[0].set_ylabel("Neuron index")
axes[0].set_title("E/I Network Raster (first 500 ms)")
axes[0].set_xlim([0, t_max_plot])

# ── Population rates (first 500 ms) ──────────────────────────
mask_t = t_E < t_max_plot
axes[1].plot(t_E[mask_t], rate_E[mask_t], color="steelblue", lw=1.5, label="Excitatory")
axes[1].plot(t_I[mask_t], rate_I[mask_t], color="crimson", lw=1.5, label="Inhibitory")
axes[1].set_ylabel("Population rate (Hz)")
axes[1].set_title("Population firing rates")
axes[1].legend()

# ── Power spectra ─────────────────────────────────────────────
axes[2].semilogy(
    freqs_E, power_E, color="steelblue", lw=1.5, label=f"Excitatory (peak {peak_E:.0f} Hz)"
)
axes[2].semilogy(
    freqs_I, power_I, color="crimson", lw=1.5, label=f"Inhibitory (peak {peak_I:.0f} Hz)"
)
axes[2].axvline(peak_E, color="steelblue", linestyle="--", lw=1, alpha=0.7)
axes[2].axvline(30, color="gray", linestyle=":", lw=1, label="Gamma onset (30 Hz)")
axes[2].axvline(80, color="gray", linestyle=":", lw=1, label="Gamma offset (80 Hz)")
axes[2].set_xlabel("Frequency (Hz)")
axes[2].set_ylabel("Power (log scale)")
axes[2].set_title("Power Spectrum — Gamma Oscillation")
axes[2].legend()
axes[2].set_xlim([0, 150])

# ── Phase relationship (E leads or lags I?) ───────────────────
# Zoom into a 200ms window to see individual oscillation cycles
window = (500, 700)
mask_w = (t_E >= window[0]) & (t_E <= window[1])
axes[3].plot(t_E[mask_w], rate_E[mask_w], color="steelblue", lw=2, label="Excitatory")
axes[3].plot(t_I[mask_w], rate_I[mask_w], color="crimson", lw=2, label="Inhibitory")
axes[3].set_xlabel("Time (ms)")
axes[3].set_ylabel("Population rate (Hz)")
axes[3].set_title(f"Oscillation cycles — {window[0]}–{window[1]} ms window")
axes[3].legend()

plt.tight_layout()
plt.savefig("figure_13-7-1_gamma_oscillation.png", dpi=150, bbox_inches="tight")
print("Gamma oscillation example completed...\n")

# --------------------------
# The E/I Phase Relationship


def measure_peak_frequency(tau_i_val, duration=2000 * ms, N_E=200, N_I=50):
    """Run a reduced E/I network and return the peak oscillation frequency."""
    start_scope()
    # seed(42)

    tau_m = 20 * ms  # org 20
    v_rest = -65 * mV  # org -65
    v_thresh = -50 * mV  # org -50
    v_reset = -65 * mV  # org -65
    tau_e = 5 * ms  # org 5

    tau_E_m = 15 * ms  # Excitatory neurons slightly faster

    # Stronger E→I drive to push interneurons into gamma regime
    w_EE = 0.10 * mV  # org 0.1
    w_EI = 0.30 * mV  # org 0.3
    w_IE = -0.70 * mV  # org -0.7
    w_II = -0.40 * mV  # org -0.4

    namespace = {
        "tau_m": tau_m,
        "tau_E_m": tau_E_m,
        "tau_e": tau_e,
        "tau_i_val": tau_i_val,
        "v_rest": v_rest,
        "v_thresh": v_thresh,
        "v_reset": v_reset,
        "w_EE": w_EE,
        "w_EI": w_EI,
        "w_IE": w_IE,
        "w_II": w_II,
    }

    eqs_E = """
    dv/dt  = (v_rest - v + g_e + g_i) / tau_E_m : volt
    dg_e/dt = -g_e / tau_e : volt
    dg_i/dt = -g_i / tau_i_val : volt
    """
    eqs_I = """
    dv/dt  = (v_rest - v + g_e + g_i) / tau_m : volt
    dg_e/dt = -g_e / tau_e : volt
    dg_i/dt = -g_i / tau_i_val : volt
    """

    exc = NeuronGroup(
        N_E,
        eqs_E,
        threshold="v > v_thresh",
        reset="v = v_reset",
        method="euler",
        namespace=namespace,
    )
    inh = NeuronGroup(
        N_I,
        eqs_I,
        threshold="v > v_thresh",
        reset="v = v_reset",
        method="euler",
        namespace=namespace,
    )
    exc.v = "v_rest + rand()*5*mV"
    inh.v = "v_rest + rand()*5*mV"

    rate_E = 55 * Hz  # original 10 Hz
    rate_I = 60 * Hz  # original 12 Hz
    N_bg = 300  # original 200
    bg_weight_E = 0.18 * mV  # orignal 0.10
    bg_weight_I = 0.19 * mV  # orignal 0.12
    PoissonInput(exc, "g_e", N=N_bg, rate=rate_E, weight=bg_weight_E)
    PoissonInput(inh, "g_e", N=N_bg, rate=rate_I, weight=bg_weight_I)

    S_EE = Synapses(exc, exc, on_pre="g_e_post += w_EE")
    S_EE.connect(condition="i != j", p=0.1)
    S_EI = Synapses(exc, inh, on_pre="g_e_post += w_EI")
    S_EI.connect(p=0.1)
    S_IE = Synapses(inh, exc, on_pre="g_i_post += w_IE")
    S_IE.connect(p=0.1)
    S_II = Synapses(inh, inh, on_pre="g_i_post += w_II")
    S_II.connect(condition="i != j", p=0.3)

    sm_E = SpikeMonitor(exc)
    sm_I = SpikeMonitor(inh)
    print(f"\nRunning simulation for tau_i_val={tau_i_val} ...")
    print(f"N_bg={N_bg}, rate_E={rate_E}, " f"weight_E={bg_weight_E}")
    run(duration)
    print(f"sm_E.num_spikes = {sm_E.num_spikes}")
    print(f"sm_I.num_spikes = {sm_I.num_spikes}")

    t_E, rate_E = compute_population_rate(sm_E, N_E, bin_size_ms=5.0, duration_ms=duration / ms)
    freqs, power = compute_power_spectrum(rate_E, 5.0)
    freq_mask = (freqs > 10) & (freqs < 150)
    print("Max power:", power[freq_mask].max())
    if power[freq_mask].max() < 1.0:
        print("No clear oscillation, returning 0")
        return 0.0  # No clear oscillation
    return freqs[freq_mask][np.argmax(power[freq_mask])]


# Vary inhibitory time constant from 5 to 20 ms
tau_i_values = np.arange(5, 22, 2) * ms
peak_freqs = []
for tau_i_val in tau_i_values:
    # f = measure_peak_frequency(tau_i_val, duration=duration, N_E=N_E, N_I=N_I)
    spike_Ei, spike_Ii = oscillation_dynamics(N_E, N_I, duration, tau_i=tau_i_val)
    t_E, rate_E = compute_population_rate(spike_Ei, N_E, bin_size_ms=5.0, duration_ms=duration / ms)
    freqs, power = compute_power_spectrum(rate_E, 5.0)
    freq_mask = (freqs > 10) & (freqs < 150)
    print("Max power:", power[freq_mask].max())
    f = freqs[freq_mask][np.argmax(power[freq_mask])]
    print(f"Peak oscillation f = {f}")
    if power[freq_mask].max() < 1.0:
        print("No clear oscillation, returning 0")
        f = 0.0
    peak_freqs.append(f)
    print(f"tau_i = {tau_i_val/ms:.0f} ms → peak frequency = {f:.1f} Hz")

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(tau_i_values / ms, peak_freqs, "o-", color="purple", markersize=8)
ax.axhspan(30, 80, color="lightyellow", alpha=0.5, label="Gamma band (30–80 Hz)")
ax.set_xlabel("Inhibitory synaptic time constant tau_i (ms)")
ax.set_ylabel("Peak oscillation frequency (Hz)")
ax.set_title("Gamma Frequency vs. Inhibitory Time Constant")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("figure_13-7-2_frequency_vs_tau.png", dpi=150, bbox_inches="tight")
print("Frequency vs tau example completed...\n")
print()


# ------------------------------------------
# Saving the Final Week 13 Simulation Output

# Save excitatory and inhibitory spike trains separately
spike_trains_E = {}
for idx in range(N_E):
    mask = spike_E1.i == idx
    spike_trains_E[idx] = np.array(spike_E1.t[mask] / second)

spike_trains_I = {}
for idx in range(N_I):
    mask = spike_I1.i == idx
    spike_trains_I[idx] = np.array(spike_I1.t[mask] / second)

filename_E = "week13_7_brian2_gamma_E_spikes.npy"
filename_I = "week13_7_brian2_gamma_I_spikes.npy"
np.save(f"{filename_E}", spike_trains_E)
np.save(f"{filename_I}", spike_trains_I)

print("Saved gamma oscillation spike trains.")

print(
    f"Excitatory: {N_E} neurons, {builtins.sum(len(v) for v in spike_trains_E.values())} total spikes"
)
print(
    f"Inhibitory: {N_I} neurons, {builtins.sum(len(v) for v in spike_trains_I.values())} total spikes"
)
print()
