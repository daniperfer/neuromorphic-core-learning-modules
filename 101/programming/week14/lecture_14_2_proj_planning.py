"""
Lecture 14.2: Project Planning — From Science Question to Simulation Architecture
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

from brian2 import *

# ------------------------------------------------------
# From Question to Network: The Simplification Principle

# Standard LIF parameters — fix these unless your question requires varying them
tau = 20 * ms  # Membrane time constant
v_rest = -65 * mV  # Resting potential
v_thresh = -50 * mV  # Spike threshold
v_reset = -65 * mV  # Reset potential after spike
R = 10 * Mohm  # Membrane resistance

# -------------------------------------------
# Network Size: How Many Neurons Do You Need?

# Recommended network sizes by project type
# E/I balance, gamma tuning, sparse/dense connectivity:
N_E = 320  # Excitatory neurons (80%)
N_I = 80  # Inhibitory neurons (20%)
N = N_E + N_I  # Total: 400

# Population synchrony:
N_pop1 = 200  # Population 1
N_pop2 = 200  # Population 2

# F-I curve, single neuron dynamics:
N = 1  # or a small population of 50–100 identical neurons

# ------------------------------------
# Connectivity: What Connects to What?

# Standard connectivity — use as default unless your project varies it
p_EE = 0.1  # E → E connection probability
p_EI = 0.1  # E → I connection probability
p_IE = 0.1  # I → E connection probability
p_II = 0.1  # I → I connection probability

# Assignment 13 baseline weights — well-characterized, use as defaults
w_EE = 0.20 * mV  # Excitatory → Excitatory
w_EI = 0.30 * mV  # Excitatory → Inhibitory (drives interneurons)
w_IE = -0.55 * mV  # Inhibitory → Excitatory (key balance parameter)
w_II = -0.25 * mV  # Inhibitory → Inhibitory

# -----------------------------------
# Defining Your Conditions Explicitly

# E/I balance project: define conditions before any simulation code
conditions = {
    "balanced": {"w_IE": -0.55 * mV, "label": "Balanced (w_IE = -0.55 mV)", "color": "#2c4a8c"},
    "mild_disinhibition": {
        "w_IE": -0.35 * mV,
        "label": "Mild disinhibition (w_IE = -0.35 mV)",
        "color": "#e07b39",
    },
    "strong_disinhibition": {
        "w_IE": -0.10 * mV,
        "label": "Strong disinhibition (w_IE = -0.10 mV)",
        "color": "#c0392b",
    },
}

# ---------------------------------------------
# Structuring Your Code for Multiple Conditions


def run_simulation(
    w_IE,
    w_EE=0.20 * mV,
    w_EI=0.30 * mV,
    w_II=-0.25 * mV,
    N_E=320,
    N_I=80,
    sim_duration=2000 * ms,
    input_rate=8000 * Hz,
    condition_label="",
):
    """
    Run one condition of the E/I balance mini-project.

    Parameters
    ----------
    w_IE : Quantity
        Inhibitory-to-excitatory synaptic weight (mV). Negative = inhibitory.
    w_EE, w_EI, w_II : Quantity
        Remaining synaptic weights (mV).
    N_E, N_I : int
        Number of excitatory and inhibitory neurons.
    sim_duration : Quantity
        Total simulation duration (ms).
    input_rate : Quantity
        Poisson input rate per neuron (Hz).
    condition_label : str
        Human-readable label for this condition (used in saved filenames).

    Returns
    -------
    dict
        Keys: 'spike_trains_E', 'spike_trains_I', 'times', 'label'
    """
    start_scope()
    seed(42)

    # LIF parameters
    tau = 20 * ms
    v_rest = -65 * mV
    v_thresh = -50 * mV
    v_reset = -65 * mV
    R = 10 * Mohm

    eqs = """
    dv/dt = (v_rest - v + R*I_ext) / tau : volt
    I_ext : amp
    """

    N = N_E + N_I

    # Neuron groups
    neurons = NeuronGroup(N, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler")
    neurons.v = v_rest
    neurons.I_ext = 0 * amp

    E_neurons = neurons[:N_E]
    I_neurons = neurons[N_E:]

    # Connectivity
    p = 0.1
    syn_EE = Synapses(E_neurons, E_neurons, on_pre="v_post += w_EE")
    syn_EE.connect(condition="i != j", p=p)

    syn_EI = Synapses(E_neurons, I_neurons, on_pre="v_post += w_EI")
    syn_EI.connect(p=p)

    syn_IE = Synapses(I_neurons, E_neurons, on_pre="v_post += w_IE")
    syn_IE.connect(p=p)

    syn_II = Synapses(I_neurons, I_neurons, on_pre="v_post += w_II")
    syn_II.connect(condition="i != j", p=p)

    # Poisson input drive
    poisson_E = PoissonInput(E_neurons, "v", 1, input_rate, weight=0.15 * mV)
    poisson_I = PoissonInput(I_neurons, "v", 1, input_rate, weight=0.15 * mV)

    # Monitors
    spike_mon_E = SpikeMonitor(E_neurons)
    spike_mon_I = SpikeMonitor(I_neurons)

    run(sim_duration)

    # Extract spike trains
    spike_trains_E = {i: spike_mon_E.spike_trains()[i] / ms for i in range(N_E)}
    spike_trains_I = {i: spike_mon_I.spike_trains()[i] / ms for i in range(N_I)}

    return {
        "spike_trains_E": spike_trains_E,
        "spike_trains_I": spike_trains_I,
        "label": condition_label,
        "N_E": N_E,
        "N_I": N_I,
        "sim_duration_ms": sim_duration / ms,
    }


# With the function above defined, running all three conditions takes nine lines:

results = {}
for name, params in conditions.items():
    print(f"Running condition: {params['label']}...")
    results[name] = run_simulation(w_IE=params["w_IE"], condition_label=params["label"])
    # Save immediately — don't wait until all conditions are done
    np.save(f"project_{name}_spikes_E.npy", results[name]["spike_trains_E"])
    np.save(f"project_{name}_spikes_I.npy", results[name]["spike_trains_I"])
    print(f"  Done. Saved spike trains for: {params['label']}")

print("All conditions complete.")

# ---------------------------------
# Choosing Your Simulation Duration

# Duration recommendations by analysis type
sim_duration_rate = 2000 * ms  # Firing rate, ISI statistics
sim_duration_spectrum = 3000 * ms  # Power spectrum (more cycles = cleaner spectrum)
sim_duration_xcorr = 2000 * ms  # Cross-correlogram
sim_duration_fI = 1000 * ms  # F-I curve (run many times at different currents)

# -------------------------------
# Your Complete Architecture Plan

"""
PROJECT ARCHITECTURE PLAN
=========================
Scientific question: [one sentence]
Hypothesis: [one sentence — what do you predict and why?]

Network:
  - Neuron type: LIF
  - N_E: [number]   N_I: [number]
  - Connectivity: p = [value]
  - Fixed parameters: tau=20ms, v_thresh=-50mV, v_reset=-65mV
  - Varying parameter: [name] across [range or conditions]

Conditions:
  1. [Condition name]: [parameter value]
  2. [Condition name]: [parameter value]
  (3. [Condition name]: [parameter value])

Simulation duration: [value] ms
Input drive: PoissonInput, rate = [value] Hz

Analysis pipeline:
  - Primary measurement: [e.g., ISI CV, power spectrum, cross-correlogram]
  - Tools from NeuralAnalysisFramework: [list]
  - Expected result in condition 1: [one sentence]
  - Expected result in condition 2: [one sentence]

Output files:
  - project_[condition1]_spikes_E.npy
  - project_[condition1]_spikes_I.npy
  - project_[condition2]_spikes_E.npy
  - project_[condition2]_spikes_I.npy

Figures to produce:
  1. [Figure description]
  2. [Figure description]
  3. [Figure description]
"""
