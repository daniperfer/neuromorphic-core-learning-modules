"""
Assignment 15: Final Project — A Complete Computational Neuroscience Study
"""
# =============================================================================
# NEUR 101 — Week 15 Final Project Starter Code
# =============================================================================

# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

from dataclasses import dataclass
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
from brian2 import *
from week12.lecture_12_2_isi import isi_statistics
from week13.lecture_13_7_oscillation_dynamics_alt import (
    compute_population_rate,
    compute_power_spectrum,
)
from week14.lecture_14_3_proj_implement import SimParams, run_ei_simulation

# --- 1. DEFINE YOUR COLOR PALETTE ---
COLORS = {
    "excitatory": "#2c4a8c",
    "inhibitory": "#c0392b",
    "population": "#2c3e50",
    "sweep_line": "#2c4a8c",
    "sweep_marker": "#e74c3c",
    "reference": "#95a5a6",
    "condition_low": "#3498db",
    "condition_med": "#e67e22",
    "condition_high": "#8e44ad",
}

plt.rcParams.update(
    {
        "font.size": 11,
        "axes.labelsize": 12,
        "axes.titlesize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "savefig.dpi": 300,
    }
)

# --- 2. STANDARD LIF PARAMETERS ---
tau = 20 * ms
v_rest = -65 * mV
v_thresh = -50 * mV
v_reset = -65 * mV
R = 10 * Mohm


# --- 3. SIMULATION PARAMS DATACLASS ---
@dataclass
class SimulationParams:
    # Network size
    N_E: int = 400
    N_I: int = 100
    # Synaptic weights (nA)
    w_EE: float = 0.3
    w_EI: float = 0.3
    w_IE: float = 0.5  # ← your primary swept/varied parameter
    w_II: float = 0.2
    # External drive
    input_rate: float = 8.0  # Hz
    # Simulation
    duration: float = 2.0  # seconds
    # Label for output files
    label: str = "baseline"


# --- 4. RUN SIMULATION FUNCTION ---
def run_simulation(params: SimulationParams) -> dict:
    start_scope()
    seed(42)

    eqs = """
    dv/dt = (v_rest - v + R * I_ext) / tau : volt
    I_ext : amp
    """

    P_E = NeuronGroup(
        params.N_E, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler"
    )
    P_I = NeuronGroup(
        params.N_I, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler"
    )
    P_E.v = v_rest
    P_I.v = v_rest

    S_EE = Synapses(P_E, P_E, on_pre="I_ext += %f*nA" % params.w_EE)
    S_EI = Synapses(P_E, P_I, on_pre="I_ext += %f*nA" % params.w_EI)
    S_IE = Synapses(P_I, P_E, on_pre="I_ext -= %f*nA" % params.w_IE)
    S_II = Synapses(P_I, P_I, on_pre="I_ext -= %f*nA" % params.w_II)

    S_EE.connect(p=0.1)
    S_EI.connect(p=0.1)
    S_IE.connect(p=0.1)
    S_II.connect(p=0.1)

    PI_E = PoissonInput(P_E, "I_ext", 100, params.input_rate * Hz, weight=0.05 * nA)
    PI_I = PoissonInput(P_I, "I_ext", 100, params.input_rate * Hz, weight=0.05 * nA)

    spike_mon_E = SpikeMonitor(P_E)
    spike_mon_I = SpikeMonitor(P_I)

    run(params.duration * second)

    spike_times_E = np.array(spike_mon_E.t / second)
    spike_ids_E = np.array(spike_mon_E.i)
    spike_times_I = np.array(spike_mon_I.t / second)
    spike_ids_I = np.array(spike_mon_I.i)

    np.save(f"final_{params.label}_E_spikes.npy", spike_times_E)
    np.save(f"final_{params.label}_I_spikes.npy", spike_times_I)
    np.save(f"final_{params.label}_E_ids.npy", spike_ids_E)

    return {
        "spike_times_E": spike_times_E,
        "spike_ids_E": spike_ids_E,
        "spike_times_I": spike_times_I,
        "spike_ids_I": spike_ids_I,
        "params": params,
        "duration": params.duration,
        "N_E": params.N_E,
        "N_I": params.N_I,
    }


# --- 5. NAMED CONDITIONS (for your comparison figure) ---
# Replace these with your actual conditions
conditions = [
    SimuParams(w_IE=0.3, label="low_inhibition"),
    SimuParams(w_IE=0.5, label="medium_inhibition"),
    SimuParams(w_IE=0.9, label="high_inhibition"),
]

condition_results = {}
for params in conditions:
    print(f"Running condition: {params.label}")
    condition_results[params.label] = run_simulation(params)


# --- 6. PARAMETER SWEEP ---
# Replace the range and parameter with your sweep design
w_IE_values = np.linspace(0.2, 1.0, 8)

sweep_results = {}
mean_cv_values = []
mean_rate_values = []

for w_IE in w_IE_values:
    label = f"sweep_wIE_{w_IE:.3f}".replace(".", "p")
    params = SimulationParams(w_IE=w_IE, label=label)
    result = run_simulation(params)
    sweep_results[label] = result

    # Extract summary statistics
    spike_times = result["spike_times_E"]
    spike_ids = result["spike_ids_E"]
    N = result["N_E"]
    duration = result["duration"]

    isis, cv = isi_statistics(spike_times, spike_ids, N)
    mean_cv = np.nanmean(cv)
    mean_rate = len(spike_times) / (N * duration)

    mean_cv_values.append(mean_cv)
    mean_rate_values.append(mean_rate)
    print(f"  w_IE = {w_IE:.3f}: mean_cv = {mean_cv:.3f}, rate = {mean_rate:.2f} Hz")

mean_cv_values = np.array(mean_cv_values)
mean_rate_values = np.array(mean_rate_values)
print("\nSweep complete.")


# --- 7. ANALYSIS AND FIGURES ---
# Use the figure code from Lecture 15.5 as your template
# Figure 1: comparison figure (condition_results)
# Figure 2: sweep figure (w_IE_values, mean_cv_values, mean_rate_values)
# Figure 3: analysis figure (ISI histograms + power spectra)

print("All figures saved. Final project complete.")
