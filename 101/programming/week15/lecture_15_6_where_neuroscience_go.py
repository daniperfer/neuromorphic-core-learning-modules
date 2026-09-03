"""
Lecture 15.6: The Broader Landscape — Where Computational Neuroscience Goes From Here
"""
# flake8: noqa: F403,F405
# mypy: disable-error-code=name-defined

# AdEx model equations (Brian2) — compare to your LIF equations
# The transition from LIF requires only changing the equations string

from brian2 import *

adex_eqs = """
dv/dt  = (g_L*(E_L - v) + g_L*delta_T*exp((v - v_T)/delta_T) - w + I_ext) / C_m : volt
dw/dt  = (a*(v - E_L) - w) / tau_w : amp
I_ext  : amp
"""

# Parameters (typical cortical RS cell)
g_L = 10 * nS  # leak conductance
E_L = -70 * mV  # leak reversal potential
C_m = 200 * pF  # membrane capacitance
delta_T = 2 * mV  # spike slope factor
v_T = -50 * mV  # spike threshold
a = 2 * nS  # subthreshold adaptation
tau_w = 100 * ms  # adaptation time constant

# The rest of the Brian2 setup (NeuronGroup, Synapses, etc.) is identical to your LIF code

# ---------------------------
# Large-Scale Brain Simulation

"""
The LIF networks you have built this term have a few hundred neurons.
Contemporary large-scale simulation projects work at a different scale entirely.

The Human Brain Project (HBP), a ten-year European initiative that concluded in 2023,
attempted to build a biologically detailed simulation of the entire mouse cortex
— roughly 75 million neurons — using supercomputer clusters. The computational
infrastructure they developed (the EBRAINS platform, the PyNN interface, the NEST simulator)
is publicly accessible. NEST (Neural Simulation Technology) is to large-scale simulations
what Brian2 is to smaller-scale ones: a dedicated spiking neural network simulator optimized
for networks of millions of neurons.
"""

# -----------------------------------------
# Neuromorphic Computing: Brains in Silicon

"""
A parallel development to large-scale brain simulation is neuromorphic computing
— the design of hardware that implements neural computation directly in silicon,
rather than simulating it on conventional CPUs. This is the domain of NEUR 103
and the core research area of neuromorphiccore.ai.

Intel’s Loihi 2 chip implements spiking neural networks with on-chip learning rules
(including spike-timing-dependent plasticity) in ultra-low-power hardware.
Where running your Brian2 simulations required CPU time and kilowatts of power,
Loihi 2 can run the same network at microwatt power levels — a factor of roughly a million.
This is because biological computation is fundamentally event-driven: neurons only communicate
when they spike, and spikes are rare. Conventional silicon wastes energy clocking billions
of transistors every cycle whether or not anything is happening. Neuromorphic hardware fires
its circuits only when a spike propagates.

IBM’s TrueNorth and the BrainScaleS system at Heidelberg represent different architectural
approaches to the same problem. The BrainScaleS system is actually faster-than-real-time:
its analog circuits implement conductance-based neural dynamics at 1000x biological speed,
making it useful for studying long-timescale phenomena (like synaptic plasticity over days
of simulated time) in minutes.

Intel’s Lava software framework, the successor to the Nengo library, provides a Python interface
to neuromorphic hardware that will feel immediately familiar after NEUR 101. Networks are defined
as graphs of nodes (neurons) and connections (synapses), run with a method call, and produce
spike output that can be analyzed with the same NumPy functions you have been using all term.
"""

# --------------------------------------------
# Spiking Neural Networks for Machine Learning

"""
The snnTorch library provides a PyTorch-like interface for building and training
spiking neural networks. It uses the same LIF dynamics you have learned,
adds surrogate gradient methods to make the networks trainable by backpropagation,
and produces networks that can run on neuromorphic hardware. If you are interested in
the intersection of deep learning and neuroscience, snnTorch is a natural next step
from NEUR 101.
"""

# -----------------------------
# The NEUR Curriculum from Here

"""
NEUR 101:
has given you the programming and simulation toolkit.
The other courses in the NEUR curriculum provide the mathematical and scientific
foundations that deepen everything you have done.

NEUR 102: Linear Algebra for Neuromorphic Computing
gives you the tools for population coding and dimensionality reduction.
When you have recordings from 400 neurons, you want to know whether
they are acting as 400 independent channels or whether the activity lives in a
lower-dimensional subspace. Principal component analysis (PCA) and related methods
answer this question. The population vector decoding you touched in Week 12 is an
application of linear algebra — NEUR 102 will give you the foundations that make the
whole area of neural population geometry accessible.

NEUR 103: Introduction to Neuromorphic Computing
goes directly into the hardware side of the field — Intel Loihi, BrainScaleS,
neuromorphic chip design, and the programming models that connect software to silicon.
If you are interested in the hardware implementation of neural computation, NEUR 103 is
the natural next step.

NEUR 104: Calculus for Neural Dynamics provides the mathematical foundations for everything
you have simulated. Every Brian2 equation you wrote is a differential equation
— NEUR 104 gives you the tools to analyze differential equations analytically,
understand their stability properties, and see why the LIF neuron integrates
to a fixed point below threshold and diverges above it. The Hodgkin-Huxley model,
the AdEx, and every other conductance-based model become genuinely transparent
once you have the tools from NEUR 104.

NEUR 105: Neuroscience for Engineers provides the biological context for everything in NEUR 101.
You have been building models of neurons and networks all term — NEUR 105 connects those models
to the actual biology: how real neurons are structured, how synaptic transmission works at the
molecular level, what the evidence is for the role of oscillations in cognition, and what the
relationship between firing rate and sensory coding actually is in different brain areas.
If NEUR 101 taught you to build the models, NEUR 105 teaches you why the models are built
the way they are.
"""
