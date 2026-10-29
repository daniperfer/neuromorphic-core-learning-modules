"""
Lecture 4.5: STDP and the LIF Neuron — Closing the Loop

This is the computational model behind
neuromorphic on-chip learning: a spiking neuron that learns
from its own activity history.

Understanding how STDP and LIF fit together — mechanistically
and computationally — is essential preparation for
everything in NEUR 201 and NEUR 202.
"""

# -----------------------------
# Spike Timing in the LIF Model

"""
This is a local computation. To update w_{ij}, synapse (i, j) only needs
to know two things: when did presynaptic neuron j last fire?
And when did postsynaptic neuron i last fire?

The weight update depends on the difference Δt = t_pre^j − t_post^i:
how many milliseconds before or after the postsynaptic neuron fired
did this particular presynaptic spike arrive?
"""

# -----------------------------------------------------------
# The Trace Variable: A Biologically Plausible Implementation

"""
Tracking the exact times of all previous spikes is computationally expensive.
A biologically plausible and hardware-efficient approximation
uses synaptic trace variables.

- postsynaptic trace x_i(t) increases by 1 each time the neuron fires
and decays exponentially between spikes: dx_i/dt = −x_i / τ_+
In practice, between spikes: x_i(t2) = x_i(t1)*e^(-(t2-t1)/τ_+)

- presynaptic neuron j maintains a presynaptic trace y_j(t) that increases
at each spike and decays with time constant τ_-: dy_j/dt = −y_j / τ_-
In practice, between spikes: y_j(t2) = y_j(t1)*e^(-(t2-t1)/τ_-)

When presynaptic neuron j fires: Δw_{ij} = −A_- · x_i(t),
the postsynaptic trace reflects recent postsynaptic spikes,
so this implements depression when post fired recently.

When postsynaptic neuron i fires: Δw_{ij} = +A_+ · y_j(t),
the presynaptic trace reflects recent presynaptic spikes,
so this implements potentiation when pre fired recently.
"""

# -------------------------------------------------------
# Worked Example: A Two-Neuron Circuit Learning Over Time

"""
Consider two LIF neurons, A (pre) and B (post), connected by a single synapse
with initial weight w = 0.3. Neuron A is driven by external input and fires
at a regular rate. Neuron B fires when its membrane potential, receiving
synaptic current from A, crosses threshold.

t (10 ms) Spike 1, A fires, y_A(10) = 0 + 1 (new pre spike)
(B hasn’t fired yet, its trace is 0)
Δw = −A_- · x_B(10) ≈ 0

t (15 ms) Spike 2, B fires, x_B(15) = 0 + 1 (new post spike)
A trace decay: y_A(15) = y_A(10) · e^(−(15-10)/20)
(A trace decay y_A during 5 ms: 1 · e^(−5/20) ≈ 0.7788)
Δw = +A_+ · y_A(15) = +0.01 · e^(−5/20) ≈ +0.0078

t (30 ms) Spike 3, A fires, y_A(30) = 1 + y_A(10) · e^(−20/20) ≈ 1.37 (decay + new pre spike)
B trace decay: x_B(30) = x_B(15) · e^(−(30-15)/20)
(B trace decay x_B during 15 ms: 1 · e^(−15/20) ≈ 0.4724)
Δw = −A_- · x_B(30) = −0.012 · e^(−15/20) ≈ −0.0057

t (35 ms) Spike 4, B fires, x_B(35) → 1 + x_B(15) e^(−20/20) ≈ 1.37 (decay + new pre spike)
A trace decay: y_A(35) = y_A(30) · e^(−(35-30)/20)
(A trace decay y_A during 5 ms: 1.37 · e^(−5/20) ≈ 1.067)
Δw = +A_+ · y_A(35) = +0.01 · 1.067 ≈ +0.01067

t (50 ms) Spike 5, A fires, y_A(50) = 1 + y_A(30) e^(−20/20) ≈ 1.5040 (decay + new pre spike)
B trace decay: x_B(50) = x_B(35) · e^(−(50-35)/20)
(B trace decay x_B during 20 ms: 1.37 · e^(−15/20) ≈ 0.6471)
Δw = −A_- · x_B(50) = −0.012 · 0.6471 ≈ −0.0078

Net weight change over 5 spikes: approximately:
0 + 0.0078 - 0.0057 + 0.01067 - 0.0078 = 0.00497
The synapse is slowly potentiating because A fires just
before B more often than B fires before A.
"""

# -----------------------------------------
# On-Chip Learning in Neuromorphic Hardware

"""
The trace-based STDP rule is hardware-friendly for two reasons.
1) each synapse only needs its own trace values (local).
2) weight updates only happen at spike times (sparse).

The STDP rule is not guaranteed to solve any particular supervised task
— it is an unsupervised rule that extracts correlational structure,
which may or may not align with what you want the network to do.

Looking ahead to NEUR 202:
That course is where you will implement STDP in networks of thousands
of neurons, analyze its convergence properties mathematically,
and explore more powerful learning rules that combine STDP
with supervised signals. This week gives you the biological and
conceptual foundation. NEUR 202 gives you the full formalism.
"""

# ------------------------
# Common Mistakes To Avoid

"""
The trace variable x(t) or y(t) is an abstract bookkeeping quantity that
tracks recent spike history for the purpose of computing weight updates.
A neuron has one membrane potential; each synapse has its own pair of traces.

The synaptic weight is a dimensionless multiplier;
the synaptic current is what flows into the postsynaptic neuron
when a presynaptic spike arrives, computed as I = w_{ij} · δ(t − t_pre).
STDP changes w_{ij}, which changes the magnitude of the
current injected by future presynaptic spikes.
"""
