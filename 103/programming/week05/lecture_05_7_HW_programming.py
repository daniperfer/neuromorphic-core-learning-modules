"""
Lecture 5.7: Programming Neuromorphic Hardware — From Network to Silicon
"""

# ---------------------------------------
# The Programming Stack for Each Platform

"""
Common conceptual structure:
1) a high-level description language,
2) a compiler that maps the logical network to physical cores,
3) a runtime layer that handles communication with the chip.

Intel Loihi — NxSDK and Lava.
NxSDK is a Python library to define neuron populations, synaptic connections, and learning rules,
then compile and deploy them to Loihi hardware.
For Loihi 2, Intel developed Lava, an open-source neuromorphic software framework
designed to be hardware-agnostic — Lava code describes a spiking process network,
and the Lava compiler targets Loihi 2, or a CPU simulator.
Lava is conceptually similar to PyTorch, but the underlying execution model is spike-based.

IBM TrueNorth — Corelet Programming and the TrueNorth Toolchain.
Begins with training a conventional neural network (on a GPU) and then converting it
to a spiking network with binary weights using IBM’s porting toolchain.
Converted network is expressed in the Corelet language, which specifies how neurosynaptic
cores are configured and connected.
TrueNorth compiler then assigns Corelets to physical cores, resolves the connectivity constraints,
and generates the binary configuration image that is loaded onto the chip.
TrueNorth’s programming model is the most constrained of the three
— you are essentially configuring hardware registers rather than writing a program.

SpiNNaker — PyNN and SpiNNaker Tools.
PyNN, a Python library designed to be a hardware-neutral description language
for spiking neural networks: define neuron model, populations and prjections.
SpiNNaker toolchain compiles and routes the network to the hardware.
SpiNNaker’s neuron models are software-defined, the most accessible platform for researchers.
"""

# -----------------------------
# The Neuron Allocation Problem

"""
Given a logical network (a graph of N neuron populations with E synaptic connections),
assign each neuron to a physical core such that:

1) No core exceeds its neuron capacity:
(128K / 256K per Loihi core; 256 per TrueNorth core; 1,000 per SpiNNaker ARM core)
2) No core exceeds its synaptic memory capacity.
3) Neurons that communicate frequently are placed on nearby cores to minimize
spike routing distance and latency.
4) The mapping is load-balanced so that no core is a computational bottleneck.

Graph partitioning problem:
Finding the optimal assignment of neurons to cores is NP-hard, meaning that
for large networks, compilers use heuristic algorithms rather than exact solvers.
The constraint is the synaptic memory budget: is the local memory for
synaptic weights that limits how you partition.
A neuron with many inputs must have all those synaptic weights stored in
the local memory of the core it is assigned to, otherwise the neuron must
be split (nputs are distributed across multiple cores).
"""

# -----------------------------------------------------------
# Multi-Chip Partitioning: Distributed Neuromorphic Computing

"""
When a network is too large for a single chip, it must be distributed across multiple chips.
This introduces a new challenge: inter-chip spike routing.
Within a chip, spikes travel at very low latency and energy cost. But between chips,
spikes must travel over a board-level interconnect
— higher latency, higher energy, and potentially bandwidth-limited.

The goal is to minimize the number of inter-chip spikes: assigning neurons that communicate
heavily with each other to cores on the same chip whenever possible.
"""

# ------------------------
# Common Mistakes to Avoid

"""
For large networks, neuromorphic compilation — solving the neuron allocation
and routing problems — can take minutes to hours.
This is the neuromorphic equivalent of circuit synthesis in VLSI design:
the hardware runs fast; the compilation step to get there is expensive.
"""
