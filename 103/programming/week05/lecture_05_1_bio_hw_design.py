"""
Lecture 5.1: From Biology to Silicon — The Design Translation Problem
"""

# ------------------------------------------------
# The Biological Ideal vs. the Engineering Reality

"""
Biological neural systems have a set of properties:
1. they process information asynchronously
2. they are massively parallel
3. they consume remarkably little powe
4. they learn continuously

Engineering a chip to reproduce all of these properties simultaneously
is not currently possible:

1) Analog vs. digital.
Biological neurons compute in continuous voltages. Digital hardware works with discrete bits.
Analog is power-efficient, but also noisy, hard to program, difficult to manufacture at scale.
Most modern chips are digital.

2) Continuous time vs. clocked time.
Biological spikes could happen at any point in continuous time.
Clocked hardware quantizes time, which simplifies design but introduces temporal approximation.

3) Infinite precision vs. finite bits.
The synaptic weights in your NEUR 102 matrices were 64-bit floating-point numbers.
Real biological synapses do not have 64 bits of precision — but they do have more than 1 bit.
TrueNorth uses 1-bit binary weights. Loihi uses 9-bit integer weights.
The tradeoff is computational expressiveness vs. power and area cost.

4) Fixed structure vs. plasticity.
When running a model on GPU, no learning happens on the device during inference.
Loihi implements on-chip STDP: the chip learns as it runs.
TrueNorth does not. SpiNNaker supports on-chip plasticity in its second generation.
"""

# --------------------------------------------
# Worked Example: Counting the Cost of a Spike

"""
In a biological system, energy cost is approximately 10 femtojoules (10 × 10⁻¹⁵ J)
per synaptic event — extraordinarily small.

GPU performs a full dense matrix multiplication to compute synaptic inputs.
For a network of N neurons, this costs O(N²) operations per timestep regardless of activity.
If 1% of neurons are active, you are still paying for 100% of the computation.

Loihi only computes when a spike arrives. If a neuron fires, only the downstream neurons
connected to it receive an update.
GPU and Loihi are solving different problems.

The key figure of merit that captures this is synaptic operations per second per watt (SOPS/W).
Loihi achieves approximately 10¹² SOPS/W for sparse workloads.
"""
