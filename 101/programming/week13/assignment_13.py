"""
Assignment 13: E/I Network Simulation with Brian2
NEUR 101 — Introduction to Programming with Python for Neuroscience

Student name: _______________
Date: _______________

import matplotlib.pyplot as plt

"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

import numpy as np
from brian2 import *
from scipy import signal as sp_signal

# ── Paste your Week 12 SpikeTrainPipeline and NeuralAnalysisFramework here ──


# ─── Helper: population rate ─────────────────────────────────
def compute_population_rate(spike_monitor, N_neurons, bin_size_ms=5.0, duration_ms=None):
    """Population-averaged firing rate as a function of time."""
    spike_times_ms = spike_monitor.t / ms
    if duration_ms is None:
        duration_ms = (
            float(spike_times_ms.max()) + bin_size_ms if len(spike_times_ms) > 0 else bin_size_ms
        )
    bins = np.arange(0, duration_ms + bin_size_ms, bin_size_ms)
    counts, _ = np.histogram(spike_times_ms, bins=bins)
    pop_rate = counts / N_neurons / (bin_size_ms * 1e-3)
    bin_centers = bins[:-1] + bin_size_ms / 2
    return bin_centers, pop_rate


# ─── Helper: power spectrum ───────────────────────────────────
def compute_power_spectrum(pop_rate, bin_size_ms):
    """Compute the power spectrum of a population rate signal."""
    fs = 1000.0 / bin_size_ms
    freqs, power = sp_signal.welch(pop_rate, fs=fs, nperseg=min(256, len(pop_rate) // 4))
    return freqs, power


# ─── Network parameters ───────────────────────────────────────
N_E = 400
N_I = 100

# ── YOUR CODE STARTS HERE ─────────────────────────────────────

# Part 1: balanced network
# ...

# Part 2: disinhibited network
# ...

# Part 3: power spectrum
# ...

# Part 4: SpikeTrainPipeline
# ...
