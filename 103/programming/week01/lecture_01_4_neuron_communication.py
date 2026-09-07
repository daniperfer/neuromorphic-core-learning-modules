"""
Lecture 1.4: How Neurons Communicate — Spikes, Synapses, and Signals
"""

# ------------------------------
# The Action Potential in Detail

"""
A neuron either fires a full action potential or it does not fire at all.
There is no such thing as a “half spike” or a “weak spike.”
This all-or-nothing property is what makes spikes events rather than values.
The spike carries no amplitude information — all spikes from a given neuron are identical.
What varies is when the spike occurs and how often.
Timing and rate are the coding dimensions; amplitude is not.

value-based vs. event-based communication is one of the fundamental divides
between conventional and neuromorphic computing.
"""

# -----------------------
# Arriving at the Synapse

"""
When an action potential reaches the presynaptic terminal, it triggers a PSP (positive,
excitatory; or negative, inhibitory).
The magnitude of the PSP (postsynaptic potential) depends on the synapse’s weight
— how many receptors are present, how sensitive they are,
how much neurotransmitter was released. This is the biological
instantiation of the weight in a weight matrix.
"""

# ------------------------------------------------------
# Integration: The Neuron as a Temporal Summation Device

"""
A single PSP is typically not enough to fire a neuron. Firing requires the summation of many inputs.
Summation happens in two ways.
Spatial summation occurs when multiple synapses on the same neuron are active simultaneously
— their PSPs add together.
Temporal summation occurs when a single synapse fires repeatedly in quick succession.
PSPs decay exponentially with time — if the membrane is not pushed further,
the voltage returns toward resting. This decay is characterized by the membrane time constant (τ).
For two PSPs to summate temporally, they must arrive within roughly one time constant of each other.
Temporal structure matters — not just which synapses fire, but when.
"""

# ------------------------
# Common Mistakes to Avoid

"""
Action potential vs. PSP (postsynaptic potential):
The action potential is a large, all-or-nothing voltage spike in the sending neuron.
The PSP is a small, graded voltage change in the receiving neuron.
The action potential is the event that triggers neurotransmitter release;
the PSP is the result of that release in the next cell.
"""

# -------
# Summary

"""
Action potentials are all-or-nothing voltage spikes that propagate down axons
and trigger neurotransmitter release at synapses. The resulting postsynaptic potentials
are small and graded; firing requires summation — spatial (many synapses at once) or
temporal (one synapse repeatedly). The membrane time constant sets the integration window,
and the synapse weight determines the amplitude of each PSP.

Together, these mechanisms implement a computation: a weighted,
leaky temporal integral of incoming spike trains, with a threshold decision at the end.
This is the biological algorithm that neuromorphic chips are implementing in silicon.
"""
