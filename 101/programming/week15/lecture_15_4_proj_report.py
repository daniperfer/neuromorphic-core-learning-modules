"""
Lecture 15.4: Writing the Scientific Report — Methods, Results, and Discussion
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

"""
EXAMPLE ABSTRACT (185 words):

Cortical networks are thought to operate near a transition between
asynchronous irregular and synchronous regular firing states, with
the balance of excitation and inhibition as the key control parameter.
We investigated how inhibitory synaptic strength affects firing
regularity and oscillatory structure in a balanced leaky integrate-and-
fire network. We simulated a network of 400 excitatory and 100
inhibitory neurons with sparse recurrent connectivity (10% connection
probability), sweeping inhibitory synaptic weight from 0.2 to 1.0 nA
across eight conditions. Firing regularity was quantified by mean
coefficient of variation (CV) of interspike intervals; oscillatory
structure was assessed via power spectrum of the population firing rate.
Mean CV decreased from 1.31 ± 0.18 to 0.41 ± 0.09 as inhibitory weight
increased, with a transition near w_IE = 0.55 nA. Power spectrum
analysis revealed an emerging 35 Hz peak above the transition point.
These results reproduce key features of the Brunel (2000) phase diagram
in a simpler architecture and suggest that gamma-band oscillations
emerge specifically within the synchronous irregular regime.
"""

# Methods section template — parameters to list for your LIF network

"""
METHODS

Network Architecture
---------------------
We simulated a recurrent network of N_E = 400 excitatory (E) and
N_I = 100 inhibitory (I) leaky integrate-and-fire (LIF) neurons.
Membrane potential dynamics followed:

    tau * dv/dt = (v_rest - v) + R * I_ext

where tau = 20 ms (membrane time constant), v_rest = -65 mV (resting
potential), R = 10 MΩ (membrane resistance), and I_ext is the total
synaptic current. Spikes were generated when v exceeded v_thresh = -50 mV;
membrane potential was reset to v_reset = -65 mV immediately after.

Recurrent Connectivity
-----------------------
All-to-all connectivity was implemented with probability p = 0.1 for
all four synapse types (E→E, E→I, I→E, I→I). Synaptic weights were
w_EE = 0.3 nA, w_EI = 0.3 nA, w_IE = [varied], w_II = 0.2 nA.
Excitatory synapses added weight to I_ext; inhibitory synapses
subtracted weight.

External Input
--------------
Each neuron received Poisson spike input at [X] Hz via 100 independent
channels, each contributing 0.05 nA per spike, providing background
excitatory drive.

Simulation
----------
All simulations used Brian2 (Stimberg et al., 2019) with the Euler
integration method and a fixed time step of 0.1 ms. Each simulation
ran for 2 s. Random seeds were fixed (seed=42) for reproducibility.

Parameter Sweep
---------------
Inhibitory synaptic weight w_IE was varied from 0.2 to 1.0 nA across
8 evenly spaced values using numpy.linspace. All other parameters were
held constant at the values listed above.

Analysis
--------
Interspike intervals (ISIs) were computed for each excitatory neuron
with at least two spikes. Coefficient of variation (CV) was calculated
as std(ISI) / mean(ISI) per neuron; mean CV was averaged across all
qualifying neurons per condition.

Population firing rate was estimated by binning all excitatory spike
times in 10 ms bins and dividing by (N_E * bin_size). Power spectral
density was computed from the population rate time series using
numpy.fft.rfft, with frequency resolution of 0.5 Hz.

Software
--------
All analyses used NumPy 1.24 and Matplotlib 3.7. Simulations used
Brian2 2.5. Code is available upon request.
"""

"""
EXAMPLE RESULTS PARAGRAPH (for a comparison figure):

Figure 1 shows raster plots and population firing rate traces for three
representative conditions (w_IE = 0.3, 0.5, and 0.9 nA). At low
inhibitory weight (w_IE = 0.3 nA), spikes were distributed irregularly
across neurons with no apparent temporal structure in the population
rate. At medium inhibitory weight (w_IE = 0.5 nA), sparse synchronous
events were visible in the raster plot, corresponding to a modest peak
in the population rate. At high inhibitory weight (w_IE = 0.9 nA),
firing was highly synchronous, with sharp, periodic population rate
bursts at approximately 35 Hz. Mean CV values were 1.31 ± 0.18,
0.94 ± 0.12, and 0.41 ± 0.09 for the three conditions respectively.

Notice that this paragraph describes the figures objectively.
It does not say “the network showed gamma oscillations” (an interpretation)
— it says “the population rate showed periodic bursts at 35 Hz” (a description).
It does not say “inhibition stabilized the network”
— it says “mean CV decreased as inhibitory weight increased.”
The interpretation goes in the discussion.
"""

"""
DISCUSSION STRUCTURE TEMPLATE:

Paragraph 1: Connect primary finding to literature.
  - "The transition from irregular to regular firing as inhibitory
    weight increased is consistent with the phase diagram described
    by Brunel (2000), who showed that..."

Paragraph 2: Connect secondary finding (e.g., gamma oscillation)
  to literature.
  - "The emergence of 35 Hz oscillations in the synchronous
    irregular regime is broadly consistent with the E/I loop
    mechanism described by Wang and Buzsáki (1996)..."

Paragraph 3: Acknowledge model limitations.
  - Single-compartment LIF neurons, no plasticity, no
    neuromodulation, identical neurons within each population...

Paragraph 4: Suggest future directions.
  - Specific, mechanistic suggestions connected to your findings.

Paragraph 5 (optional): Broader significance.
  - One sentence on what this means for understanding neural
    computation or cortical dynamics.
"""

"""
The References Section
At minimum, your references section must include Brian2 and one relevant neuroscience paper.
The standard citations are:

Stimberg, M., Brette, R., & Goodman, D.F. (2019).
Brian 2, an intuitive and efficient neural simulator. eLife, 8, e47314.

Brunel, N. (2000).
Dynamics of sparsely connected networks of excitatory and inhibitory spiking neurons.
Journal of Computational Neuroscience, 8(3), 183–208.

Wang, X.J., & Buzsáki, G. (1996).
Gamma oscillation by synaptic inhibition in a hippocampal interneuronal network model.
Journal of Neuroscience, 16(20), 6402–6413.

Mainen, Z.F., & Sejnowski, T.J. (1995).
Reliability of spike timing in neocortical neurons. Science, 268(5216), 1503–1506.

Use whichever of these is relevant to your specific question.
If your project addressed firing regularity, cite Mainen and Sejnowski (1995).
If it addressed network dynamics and synchrony, cite Brunel (2000).
If it addressed gamma oscillations, cite Wang and Buzsáki (1996).
"""
