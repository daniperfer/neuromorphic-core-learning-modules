"""
Lecture 1.1: The Brain as a Computer
"""

# -------------------------------------
# The Neuron: Nature’s Signal Processor

"""
Dendrites are like antennas.
"""

# -----------------------------------------------
# What Makes a Neuron Different From a Transistor

"""
Two differences — spike-based communication and adaptive connections
— are the core ideas that neuromorphic engineers are trying to recreate in silicon.

The strength of a synapse — how much influence one neuron has over another
— changes based on experience.
"""

# --------------------------------
# Synapses: The Adjustable Weights

"""
The brain continuously adjusts them based on experience.
In Week 4 we will see exactly how — through a mechanism called
spike-timing-dependent plasticity (STDP).For now, just hold onto this:
learning in the brain is synaptic weight change.

Question...
Traditionally, in deep learning, the weights are adjusted dynamically during training
(e.g., through backpropagation). During inference, however, the weights remain fixed.

As I understand it, when training a neuromorphic network, the weights are also adjusted
according to some learning algorithm, whether through backpropagation, synaptic plasticity,
or another approach. However, during inference, do the weights remain fixed, or
can they continue to change as well?
"""

# ------------------------
# Common Mistakes to Avoid

"""
A second common confusion is treating synaptic weights as fixed parameters to be learned
once and then frozen, the way we might train a neural network and then deploy it.
Biological synapses keep changing throughout your life. The boundary between “learning”
and “inference” is much blurrier in biology than in conventional deep learning.
Neuromorphic systems like Intel Loihi are designed to blur this boundary on purpose
— they support online, continuous weight updates in a way that GPUs running backpropagation do not.

"""
