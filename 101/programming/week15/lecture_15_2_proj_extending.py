"""
Lecture 15.2: Extending Your Mini-Project — From One Condition to a Full Study
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

from dataclasses import dataclass, field
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np

# Week 15 simulation template — extend from your Week 14 project
from brian2 import *
from week11.lecture_11_7_NeuralAnalysisFramework import NeuralAnalysisFramework
from week12.lecture_12_2_isi import isi_statistics
from week13.lecture_13_7_oscillation_dynamics_alt import (
    compute_population_rate,
    compute_power_spectrum,
)
from week14.lecture_14_3_proj_implement import SimParams, run_ei_simulation

start_scope()
seed(42)


# Week 14 architecture (what you already have)
conditions = [
    SimParams(w_IE=0.3, label="low_inhibition"),
    SimParams(w_IE=0.6, label="high_inhibition"),
]

results = {}
for params in conditions:
    results[params.label] = run_ei_simulation(params)

# Week 15 extension: add a third named condition
conditions = [
    SimParams(w_IE=0.3, label="low_inhibition"),
    SimParams(w_IE=0.5, label="medium_inhibition"),
    SimParams(w_IE=0.8, label="high_inhibition"),
]

# These three named conditions become your "comparison figure" (Figure 1)
# They show the qualitative character of the three regime

# ----------------------
# Deepening the Analysis

# Example: applying three analysis types to each condition's spike data

for label, result in results.items():
    spike_times = result["spike_times_E"]
    spike_ids = result["spike_ids_E"]
    N = result["N_E"]
    duration = result["duration"]

    # Analysis type 1: ISI statistics (CV)
    isis, cv = isi_statistics(spike_times, spike_ids, N)
    mean_cv = np.nanmean(cv)

    # Analysis type 2: population firing rate
    t_pop, rate_pop = compute_population_rate(spike_times, spike_ids, N, duration, bin_size=0.01)

    # Analysis type 3: power spectrum of population rate
    freqs, power = compute_power_spectrum(rate_pop, fs=100.0)

    print(f"{label}: mean CV = {mean_cv:.3f}, " f"peak freq = {freqs[np.argmax(power)]:.1f} Hz")

# --------------------------------------------
# What to Keep from Week 14 and What to Change

# Generating descriptive sweep labels automatically
w_IE_values = np.linspace(0.2, 1.0, 8)

for w_IE in w_IE_values:
    label = f"sweep_wIE_{w_IE:.2f}".replace(".", "p")
    params = SimParams(w_IE=w_IE, label=label)
    results[label] = run_ei_simulation(params)
    print(f"Completed: {label}")
