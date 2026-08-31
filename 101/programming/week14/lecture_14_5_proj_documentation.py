"""
Lecture 14.5: Documentation and Scientific Communication
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined


import numpy as np
from brian2 import *

# -------------------------------------------------------
# Internal Documentation: Commenting Your Simulation Code

# Version 1 — describes what (useless)
w_IE = -0.55 * mV  # set w_IE to -0.55 mV

# Version 2 — describes why (useful)
w_IE = -0.55 * mV  # Baseline inhibitory weight from Assignment 13;
# produces balanced asynchronous irregular dynamics
# (Brunel 2000 regime II). Manipulated across conditions.


# Docstrings
def run_ei_simulation(params) -> dict:
    """
    Run one condition of the E/I balance mini-project.

    Network: 320 excitatory + 80 inhibitory LIF neurons (4:1 ratio,
    consistent with cortical anatomy). Random connectivity at p=0.1,
    matching sparse local connectivity in rodent neocortex (Holmgren
    et al. 2003). Poisson drive at 8 kHz approximates background
    synaptic bombardment from upstream cortical areas.

    The key manipulation is w_IE (inhibitory-to-excitatory weight),
    which is varied across conditions to simulate progressive
    disinhibition as a model of focal seizure initiation.

    Parameters
    ----------
    params : SimParams
        All network and simulation parameters. See SimParams dataclass
        for full documentation of each field.

    Returns
    -------
    dict
        'spike_trains_E': excitatory spike trains (dict, ms)
        'spike_trains_I': inhibitory spike trains (dict, ms)
        'params': the SimParams used (for provenance tracking)
        'n_spikes_E': total excitatory spikes recorded
        'n_spikes_I': total inhibitory spikes recorded
    """
    start_scope()
    seed(params.seed_val)
    # seed(42) ensures identical random connectivity and Poisson input
    # sequences across conditions, so differences between conditions
    # reflect only the parameter manipulation, not stochastic variation.
    return {}


# ---------------------------------
# Inline Comments for Analysis Code
N_E = 400
spike_trains_E = [np.ones((1, 10))]

# Compute ISI CV for active neurons.
# We exclude neurons with fewer than 3 spikes because CV is
# unreliable with fewer than ~10 ISIs; 3 spikes is a conservative
# minimum. Neurons firing < 0.5 Hz are physiologically silent and
# excluded from the distribution.
isi_cv_values = []
for i in range(N_E):
    spikes = spike_trains_E[i]
    if len(spikes) >= 3:  # need at least 2 ISIs
        isis = np.diff(np.sort(spikes))
        if np.mean(isis) > 0:  # guard against zero-duration ISIs
            cv = np.std(isis) / np.mean(isis)
            isi_cv_values.append(cv)

# Sanity check: CV should be near 1.0 for balanced asynchronous irregular
# firing (Poisson-like), < 0.5 for regular firing, > 1.5 for burst firing.
mean_cv = np.mean(isi_cv_values)
print(f"Mean ISI CV: {mean_cv:.3f}  (expected ~1.0 for balanced condition)")
assert 0.0 < mean_cv < 3.0, f"CV out of range: {mean_cv:.3f} — check simulation"

# ---------------------------
# Writing the Methods Section

"""
Model. We simulated a randomly connected network of 400 leaky integrate-and-fire (LIF)
neurons consisting of 320 excitatory (E) and 80 inhibitory (I) neurons (4:1 E/I ratio,
consistent with the approximate composition of mammalian neocortex). Membrane dynamics
followed the standard LIF equation with membrane time constant τ = 20 ms, resting
potential v_rest = −65 mV, spike threshold v_thresh = −50 mV, and reset potential
v_reset = −65 mV. Membrane resistance was R = 10 MΩ.

Connectivity. Recurrent connectivity was random with connection probability p = 0.1 for
all pairs (E→E, E→I, I→E, I→I), excluding self-connections. Synaptic interactions were
modeled as instantaneous voltage increments (delta synapses). Baseline synaptic weights
were w_EE = +0.20 mV, w_EI = +0.30 mV, w_IE = −0.55 mV (baseline), and w_II = −0.25 mV.

Input drive. Each neuron received independent Poisson spike input at 8,000 Hz with per-spike
weight 0.15 mV, simulating background synaptic bombardment from upstream cortical areas.
All neurons were initialized at uniformly random membrane potentials between v_rest and
v_thresh to prevent artifactual synchrony at simulation onset.

Experimental conditions. We varied the inhibitory-to-excitatory synaptic weight w_IE across
three conditions: balanced (w_IE = −0.55 mV), mild disinhibition (w_IE = −0.35 mV), and strong
disinhibition (w_IE = −0.10 mV). All other parameters were held constant across conditions.

Analysis. Each condition was simulated for 2,000 ms.
Mean excitatory firing rates were computed as total spike count divided by
neuron count and simulation duration. ISI coefficient of variation
(CV = σ_ISI / μ_ISI) was computed for all neurons with at least 3 recorded spikes.
Population firing rate was estimated by binning all excitatory spikes in 10 ms
windows and dividing by neuron count and bin duration. Power spectral density of
the population rate was computed using Welch’s method (scipy.signal.welch,
segment length 256 bins). All simulations used Brian2 v2.x with random seed 42 for reproducibility.
"""

# -----------------------
# Writing Figure Captions

"""
Here is a caption for the four-panel E/I balance figure from Lecture 14.4:

Figure 1. Progressive disinhibition drives a transition from asynchronous irregular
to synchronous high-frequency dynamics.
(A) Raster plots of excitatory population spiking
(80 of 320 neurons shown, first 800 ms) for balanced (blue), mildly disinhibited (orange),
and strongly disinhibited (red) conditions. Spike density increases with disinhibition,
and vertical banding (synchrony) emerges in the strongly disinhibited condition.
(B) Population excitatory firing rate over time (10 ms bins), showing progressive rate
elevation and emergence of oscillatory fluctuations under strong disinhibition.
(C) ISI coefficient of variation (CV) distributions for each condition.
CV near 1.0 indicates Poisson-like irregular firing (dashed line); CV below 0.5
indicates regular or burst-like firing. Disinhibition shifts the CV distribution toward lower values.
(D) Power spectral density of the population firing rate. The balanced condition shows
a 1/f-like spectrum; strong disinhibition reveals a peak near 80 Hz, consistent with
gamma-frequency synchrony driven by disinhibited recurrent excitation.
All conditions: N_E = 320, N_I = 80, simulation duration 2,000 ms, random seed 42.
"""

# -------------------------------------------------
# The Project Summary: Connecting to the Literature

"""
Here is a summary example for the E/I balance project:

This project investigated how reducing inhibitory synaptic strength affects population
dynamics in a randomly connected cortical network. Using a 400-neuron LIF network with
Poisson input drive, we compared firing statistics and spectral properties across three
conditions spanning a range of inhibitory weights from balanced to strongly disinhibited.
Progressive disinhibition increased mean excitatory firing rates, shifted ISI distributions
toward more regular firing, and drove the network into a gamma-frequency synchronous regime
detectable as a peak near 80 Hz in the population rate power spectrum. These results are
consistent with computational models of focal seizure initiation, in which reduction of
GABAergic inhibition unmasks recurrent excitatory connectivity and produces the
high-frequency synchronous activity observed in ictal cortex. The simulation provides
a tractable computational model for exploring how E/I balance perturbations, as occur
in conditions such as GABAergic interneuron loss, shape the transition from normal to
pathological network dynamics.
"""

# ----------------------------------------
# Organizing Your Final Project Submission

"""
project_submission/
├── simulation.py          ← All Brian2 simulation code
├── analysis.py            ← All analysis and visualization code
├── project_main_figure.png
├── project_diagnostic_rasters.png
├── project_balanced_spikes_E.npy
├── project_balanced_spikes_I.npy
├── project_mild_disinhibition_spikes_E.npy
├── project_mild_disinhibition_spikes_I.npy
├── project_strong_disinhibition_spikes_E.npy
├── project_strong_disinhibition_spikes_I.npy
├── project_balanced_summary.txt
├── project_mild_disinhibition_summary.txt
├── project_strong_disinhibition_summary.txt
└── methods_section.md     ← Written methods section + figure captions
"""
