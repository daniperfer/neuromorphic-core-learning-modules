"""
Lecture 15.1: Final Project Overview — Scope, Expectations, and Choosing Your Question
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

from dataclasses import dataclass, field
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

# Week 15 simulation template — extend from your Week 14 project
from brian2 import *

start_scope()
seed(42)

# Standard LIF parameters — same as Weeks 13-14
tau = 20 * ms
v_rest = -65 * mV
v_thresh = -50 * mV
v_reset = -65 * mV
R = 10 * Mohm


@dataclass
class SimulationParams:
    """Parameters for Week 15 final project simulation."""

    # Network architecture
    N_E: int = 400  # excitatory neurons
    N_I: int = 100  # inhibitory neurons
    # Synaptic weights
    w_EE: float = 0.3  # E→E weight (nA)
    w_EI: float = 0.3  # E→I weight
    w_IE: float = 0.5  # I→E weight
    w_II: float = 0.2  # I→I weight
    # External drive
    input_rate: float = 8.0  # Hz — Poisson input rate
    # Simulation duration
    duration: float = 2.0  # seconds
    # Label for output files and figures
    label: str = "baseline"


def run_simulation(params: SimulationParams) -> dict:
    """
    Run one simulation with the given parameters.
    Returns spike data and metadata.
    """
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

    # Synapses
    S_EE = Synapses(P_E, P_E, on_pre="I_ext += %f*nA" % params.w_EE)
    S_EI = Synapses(P_E, P_I, on_pre="I_ext += %f*nA" % params.w_EI)
    S_IE = Synapses(P_I, P_E, on_pre="I_ext -= %f*nA" % params.w_IE)
    S_II = Synapses(P_I, P_I, on_pre="I_ext -= %f*nA" % params.w_II)

    S_EE.connect(p=0.1)
    S_EI.connect(p=0.1)
    S_IE.connect(p=0.1)
    S_II.connect(p=0.1)

    # External drive
    PI_E = PoissonInput(P_E, "I_ext", 100, params.input_rate * Hz, weight=0.05 * nA)
    PI_I = PoissonInput(P_I, "I_ext", 100, params.input_rate * Hz, weight=0.05 * nA)

    # Monitors
    spike_mon_E = SpikeMonitor(P_E)
    spike_mon_I = SpikeMonitor(P_I)

    run(params.duration * second)

    spike_times_E = np.array(spike_mon_E.t / second)
    spike_ids_E = np.array(spike_mon_E.i)
    spike_times_I = np.array(spike_mon_I.t / second)
    spike_ids_I = np.array(spike_mon_I.i)

    result = {
        "spike_times_E": spike_times_E,
        "spike_ids_E": spike_ids_E,
        "spike_times_I": spike_times_I,
        "spike_ids_I": spike_ids_I,
        "params": params,
        "duration": params.duration,
        "N_E": params.N_E,
        "N_I": params.N_I,
    }

    # Save to file
    np.save(f"final_{params.label}_E_spikes.npy", spike_times_E)
    np.save(f"final_{params.label}_I_spikes.npy", spike_times_I)

    return result
