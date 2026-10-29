"""
Lecture 4.6: Homeostatic Plasticity

Homeostatic plasticity are a separate set of mechanisms that counteract
Hebb-driven instability and keep neural activity in a functional range.
Avoid a positive feedback loop to dominate all activity.
"""

# -------------------------------
# What Is Homeostatic Plasticity?

"""
It refers to mechanisms that stabilize neural activity around a target level,
compensating for disturbances (like Hebb-driven potentiation)
that push activity too high or too low.

1) Synaptic scaling:
Adjusts all synaptic weights multiplicatively, up or down, to bring
the neuron’s average firing rate back toward a target.
It is multiplicative — it preserves the relative differences between weights
(the learned pattern) while adjusting the overall gain.
It is as if you turned the volume knob on all inputs simultaneously,
without changing the mix.

2) Intrinsic excitability homeostasis:
Changes the neuron’s own properties rather than its synaptic inputs.
"""

# -------------------------------
# The Multiplicative Scaling Rule

"""
Synaptic scaling can be written as:
w_ij → w_ij · (r_target / r_average)^α

where:
r_target is the neuron’s target firing rate,
r_average is the neuron’s measured average firing rate over recent history (typically hours),
α is a sensitivity parameter.

It stabilizes activity without destroying what has been learned.
"""

# ------------------------------------------------
# Homeostasis and the Stability-Plasticity Dilemma

"""
The stability-plasticity dilemma: the brain must be plastic enough to learn new things quickly,
but stable enough not to destroy what it has already learned.
Pure Hebbian learning solves the plasticity side but fails the stability side.
Pure homeostasis gives maximal stability, zero plasticity.

The brain operates between these extremes.
Hebbian and STDP plasticity happen on fast timescales (milliseconds to minutes).
Homeostatic plasticity operates on slow timescales (hours to days).

Loihi’s on-chip STDP operates at spike timescales. A software layer running on
the chip’s embedded x86 management cores could implement slow homeostatic normalization
by periodically auditing neuron firing rates and adjusting weights.
Current neuromorphic systems are exploring how to implement this efficiently,
and it is an active research area.
"""

# -------------------------------------------
# Why Inhibitory Neurons Matter for Stability

"""
Inhibitory interneurons is another stabilizing mechanism in the brain.
This is related to the E/I balance you encountered in Week 3’s discussion of LIF networks.
Dale’s law (every neuron is either purely excitatory or inhibitory) combined with
the architecture of cortical circuits — roughly 80% excitatory, 20% inhibitory —
creates a system in which inhibitory neurons are homeostatic regulators.
Disruptions to this E/I balance are associated with pathological states.
"""

# ------------------------
# Common Mistakes to Avoid

"""
Homeostatic plasticity is not anti-Hebbian; it is orthogonal to Hebbian learning,
operating on a different timescale and affecting different properties.
(anti-Hebbian learning would erase the memory)
"""
