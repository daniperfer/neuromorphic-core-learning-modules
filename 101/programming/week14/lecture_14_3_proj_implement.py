"""
Lecture 14.3: Implementation Patterns — Reusable Brian2 Simulation Code
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

from dataclasses import dataclass, field

from brian2 import *

# -------------------------------
# The Parameter Dataclass Pattern


@dataclass
class SimParams:
    """
    All parameters for one simulation condition.
    Centralizing parameters here means there are no magic numbers
    scattered through the simulation code.
    """

    # Network architecture
    N_E: int = 320  # Excitatory neurons
    N_I: int = 80  # Inhibitory neurons
    p: float = 0.1  # Connection probability (all pairs)

    # LIF neuron parameters (fixed — do not vary unless your project requires it)
    tau_ms: float = 20.0  # Membrane time constant (ms)
    v_rest_mV: float = -65.0  # Resting potential (mV)
    v_thresh_mV: float = -50.0  # Spike threshold (mV)
    v_reset_mV: float = -65.0  # Reset potential (mV)
    R_Mohm: float = 10.0  # Membrane resistance (MOhm)

    # Synaptic weights
    w_EE_mV: float = 0.20  # E → E weight (mV)
    w_EI_mV: float = 0.30  # E → I weight (mV)
    w_IE_mV: float = -0.55  # I → E weight (mV) — key balance parameter
    w_II_mV: float = -0.25  # I → I weight (mV)

    # Input drive
    input_rate_Hz: float = 8000.0  # Poisson input rate per neuron (Hz)
    input_weight_mV: float = 0.15  # Poisson input weight (mV)

    # Simulation
    duration_ms: float = 2000.0  # Total simulation duration (ms)
    seed_val: int = 42  # Random seed for reproducibility

    # Metadata
    label: str = "unnamed"  # Human-readable condition label


# Define all conditions up front — one dataclass instance per condition
params_balanced = SimParams(w_IE_mV=-0.55, label="balanced")

params_mild = SimParams(w_IE_mV=-0.35, label="mild_disinhibition")

params_strong = SimParams(w_IE_mV=-0.10, label="strong_disinhibition")

all_conditions = [params_balanced, params_mild, params_strong]

# -------------------------------
# Writing the Simulation Function


def run_ei_simulation(params: SimParams) -> dict:
    """
    Run one condition of an E/I network simulation.

    Uses standard LIF dynamics with Poisson input drive and
    random recurrent connectivity. Always calls start_scope()
    and sets the random seed before building the network.

    Parameters
    ----------
    params : SimParams
        All network and simulation parameters for this condition.

    Returns
    -------
    dict with keys:
        'spike_trains_E' : dict[int, np.ndarray]  — spike times in ms, per E neuron
        'spike_trains_I' : dict[int, np.ndarray]  — spike times in ms, per I neuron
        'params'         : SimParams               — the params used (for provenance)
        'n_spikes_E'     : int                     — total E spikes
        'n_spikes_I'     : int                     — total I spikes
    """
    # CRITICAL: always call start_scope() before building a new network
    start_scope()
    seed(params.seed_val)

    # Unpack parameters with Brian2 units
    tau = params.tau_ms * ms
    v_rest = params.v_rest_mV * mV
    v_thresh = params.v_thresh_mV * mV
    v_reset = params.v_reset_mV * mV
    R = params.R_Mohm * Mohm
    duration = params.duration_ms * ms

    w_EE = params.w_EE_mV * mV
    w_EI = params.w_EI_mV * mV
    w_IE = params.w_IE_mV * mV
    w_II = params.w_II_mV * mV

    input_rate = params.input_rate_Hz * Hz
    input_weight = params.input_weight_mV * mV

    N_E = params.N_E
    N_I = params.N_I
    N = N_E + N_I
    p = params.p

    # LIF equations
    eqs = """
    dv/dt = (v_rest - v + R*I_ext) / tau : volt
    I_ext : amp
    """

    # Neuron groups
    neurons = NeuronGroup(N, eqs, threshold="v > v_thresh", reset="v = v_reset", method="euler")
    neurons.v = "v_rest + (v_thresh - v_rest) * rand()"
    neurons.I_ext = 0 * amp

    E_pop = neurons[:N_E]
    I_pop = neurons[N_E:]

    # Recurrent synapses
    syn_EE = Synapses(E_pop, E_pop, on_pre="v_post += w_EE")
    syn_EE.connect(condition="i != j", p=p)

    syn_EI = Synapses(E_pop, I_pop, on_pre="v_post += w_EI")
    syn_EI.connect(p=p)

    syn_IE = Synapses(I_pop, E_pop, on_pre="v_post += w_IE")
    syn_IE.connect(p=p)

    syn_II = Synapses(I_pop, I_pop, on_pre="v_post += w_II")
    syn_II.connect(condition="i != j", p=p)

    # Poisson input drive
    poisson_E = PoissonInput(E_pop, "v", 1, input_rate, weight=input_weight)
    poisson_I = PoissonInput(I_pop, "v", 1, input_rate, weight=input_weight)

    # Monitors
    spike_mon_E = SpikeMonitor(E_pop)
    spike_mon_I = SpikeMonitor(I_pop)

    # Run
    run(duration, report="text")

    # Extract spike trains as plain numpy arrays (ms)
    spike_trains_E = {i: np.array(spike_mon_E.spike_trains()[i] / ms) for i in range(N_E)}
    spike_trains_I = {i: np.array(spike_mon_I.spike_trains()[i] / ms) for i in range(N_I)}

    return {
        "spike_trains_E": spike_trains_E,
        "spike_trains_I": spike_trains_I,
        "params": params,
        "n_spikes_E": spike_mon_E.num_spikes,
        "n_spikes_I": spike_mon_I.num_spikes,
    }


# --------------------------------
# Handling start_scope() Correctly


# CORRECT: start_scope() and seed() are the first two lines of the function
def run_simulation(params):
    start_scope()  # ← Always first
    seed(params.seed_val)  # ← Always second
    # ... rest of function
    return


# INCORRECT: calling start_scope() outside the function
start_scope()  # ← This will be called only once, not before each simulation
seed(42)
result1 = run_simulation(params_balanced)  # OK
result2 = run_simulation(params_mild)  # WRONG — no start_scope() before this one

# -----------------------
# Saving Outputs Reliably


def save_condition_results(results: dict, output_dir: str = "."):
    """
    Save spike trains and metadata for one simulation condition.

    Parameters
    ----------
    results : dict
        Output from run_ei_simulation().
    output_dir : str
        Directory to save files in. Defaults to current directory.
    """
    import os

    label = results["params"].label

    # Save spike trains
    np.save(os.path.join(output_dir, f"project_{label}_spikes_E.npy"), results["spike_trains_E"])
    np.save(os.path.join(output_dir, f"project_{label}_spikes_I.npy"), results["spike_trains_I"])

    # Save a plain-text summary for quick reference
    summary_path = os.path.join(output_dir, f"project_{label}_summary.txt")
    with open(summary_path, "w") as f:
        p = results["params"]
        f.write(f"Condition: {label}\n")
        f.write(f"N_E={p.N_E}, N_I={p.N_I}, p={p.p}\n")
        f.write(f"w_IE={p.w_IE_mV} mV  (key manipulation parameter)\n")
        f.write(f"duration={p.duration_ms} ms, seed={p.seed_val}\n")
        f.write(f"Total E spikes: {results['n_spikes_E']}\n")
        f.write(f"Total I spikes: {results['n_spikes_I']}\n")
        mean_rate_E = results["n_spikes_E"] / (p.N_E * p.duration_ms / 1000)
        f.write(f"Mean E firing rate: {mean_rate_E:.1f} Hz\n")

    print(
        f"Saved: project_{label}_spikes_E.npy, project_{label}_spikes_I.npy, "
        f"project_{label}_summary.txt"
    )


# --------------------------------
# Running All Conditions in a Loop

all_results = {}

for params in all_conditions:
    print(f"\n{'='*50}")
    print(f"Running: {params.label}")
    print(f"  w_IE = {params.w_IE_mV} mV")
    print(f"{'='*50}")

    results = run_ei_simulation(params)
    save_condition_results(results)
    all_results[params.label] = results

    # Quick sanity check after each condition
    n_E = results["n_spikes_E"]
    n_I = results["n_spikes_I"]
    mean_rate_E = n_E / (params.N_E * params.duration_ms / 1000)
    mean_rate_I = n_I / (params.N_I * params.duration_ms / 1000)
    print(f"  Mean E rate: {mean_rate_E:.1f} Hz")
    print(f"  Mean I rate: {mean_rate_I:.1f} Hz")

print("\nAll conditions complete.")

# --------------------------------------------
# The Quick Raster Plot: Your First Diagnostic


def plot_raster_quick(
    spike_trains: dict,
    duration_ms: float,
    n_neurons: int = 100,
    title: str = "",
    color: str = "#2c4a8c",
    ax=None,
):
    """
    Quick diagnostic raster plot. Shows the first n_neurons neurons.

    Parameters
    ----------
    spike_trains : dict[int, np.ndarray]
        Spike times in ms, keyed by neuron index.
    duration_ms : float
        Simulation duration (ms) — sets x-axis limits.
    n_neurons : int
        Number of neurons to display (default 100).
    title : str
        Plot title.
    color : str
        Spike marker color.
    ax : matplotlib Axes or None
        If None, creates a new figure.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 4))

    for i in range(min(n_neurons, len(spike_trains))):
        spikes = spike_trains[i]
        if len(spikes) > 0:
            ax.scatter(spikes, np.full_like(spikes, i), s=1, c=color, alpha=0.6)

    ax.set_xlim(0, duration_ms)
    ax.set_ylim(-1, n_neurons)
    ax.set_xlabel("Time (ms)", fontsize=11)
    ax.set_ylabel("Neuron index", fontsize=11)
    ax.set_title(title, fontsize=12, fontweight="bold")
    return ax


# Diagnostic raster for all conditions — run this before any analysis
fig, axes = plt.subplots(len(all_conditions), 1, figsize=(12, 3 * len(all_conditions)), sharex=True)

for ax, params in zip(axes, all_conditions):
    results = all_results[params.label]
    plot_raster_quick(
        spike_trains=results["spike_trains_E"],
        duration_ms=params.duration_ms,
        n_neurons=100,
        title=f"E population raster — {params.label}  (w_IE = {params.w_IE_mV} mV)",
        color="#2c4a8c",
        ax=ax,
    )

plt.tight_layout()
plt.savefig("figure_14-3-1_project_diagnostic_rasters.png", dpi=150, bbox_inches="tight")
print()
print("Diagnostic raster saved.")

# --------------------------------------------
# Adapting the Pattern for Other Project Types


# For the F-I curve project, the varying parameter is input current rather than a synaptic weight:
@dataclass
class FICurveParams:
    """Parameters for one point on the F-I curve."""

    N: int = 1  # Single neuron
    I_ext_pA: float = 0.0  # Applied current (pA) — the x-axis of the F-I curve
    duration_ms: float = 1000.0
    seed_val: int = 42
    label: str = "unnamed"


# Build a list of conditions spanning the subthreshold-to-saturation range
fI_conditions = [
    FICurveParams(I_ext_pA=I, label=f"I_{I:.0f}pA")
    for I in np.linspace(0, 500, 25)  # 25 current steps from 0 to 500 pA
]


# For the population synchrony project, the varying parameter is whether neurons share inputs:
@dataclass
class SynchronyParams:
    """Parameters for shared vs. independent input synchrony study."""

    N: int = 200
    shared_fraction: float = 0.0  # 0.0 = independent; 1.0 = fully shared
    duration_ms: float = 2000.0
    seed_val: int = 42
    label: str = "unnamed"


sync_conditions = [
    SynchronyParams(shared_fraction=0.0, label="independent_input"),
    SynchronyParams(shared_fraction=0.5, label="half_shared_input"),
    SynchronyParams(shared_fraction=1.0, label="fully_shared_input"),
]
